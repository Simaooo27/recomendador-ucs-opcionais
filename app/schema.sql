-- Esquema da base de dados (SQLite). Seguro de executar várias vezes.

CREATE TABLE IF NOT EXISTS users (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    email                   TEXT    NOT NULL UNIQUE COLLATE NOCASE,
    -- Nome pedido no registo (23/10, decisão do PO), para tratar a pessoa pelo nome e não pelo email.
    -- Contas criadas antes ficam com '' até a pessoa o indicar em «A minha conta».
    nome                    TEXT    NOT NULL DEFAULT '',
    password_hash           TEXT    NOT NULL,
    role                    TEXT    NOT NULL DEFAULT 'aluno'
                                    CHECK (role IN ('aluno', 'admin')),
    is_active               INTEGER NOT NULL DEFAULT 0 CHECK (is_active IN (0, 1)),
    -- Muda a cada registo; invalida ligações de confirmação anteriores.
    confirmation_nonce      TEXT    NOT NULL,
    privacy_policy_version  TEXT    NOT NULL,
    privacy_accepted_at     TEXT    NOT NULL,  -- UTC, ISO 8601
    created_at              TEXT    NOT NULL,  -- UTC, ISO 8601
    confirmed_at            TEXT               -- UTC, ISO 8601
);

-- Administradores (US03): contas próprias, separadas dos alunos e sem email.
-- O primeiro é criado no terminal (flask --app app create-admin); os seguintes, na área de gestão.
CREATE TABLE IF NOT EXISTS admins (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT    NOT NULL UNIQUE COLLATE NOCASE,
    password_hash   TEXT    NOT NULL,
    created_at      TEXT    NOT NULL,  -- UTC, ISO 8601
    created_by      TEXT,              -- nome de quem o criou; vazio = criado no terminal
    last_login_at   TEXT               -- UTC, ISO 8601
);

-- Conversa de orientação com o LLM (US29). Uma por aluno; apagada quando recomeça.
-- Fica no servidor porque não cabe no cookie de sessão (4 KB). O texto do aluno é guardado
-- já sem emails nem números longos (o mesmo que é enviado ao LLM, RNF12).
CREATE TABLE IF NOT EXISTS conversas_orientacao (
    user_id         INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    mensagens       TEXT    NOT NULL,  -- JSON: [{"papel": "assistente" | "utilizador", "texto": "..."}]
    sugestao        TEXT,              -- JSON da sugestão final (US30); vazio enquanto a conversa decorre
    atualizada_em   TEXT    NOT NULL,  -- UTC, ISO 8601
    -- US37: a pessoa autorizou, ao começar, que o LLM receba as provas feitas e o intervalo da média.
    usar_notas      INTEGER NOT NULL DEFAULT 0 CHECK (usar_notas IN (0, 1))
);

-- Pedidos ao LLM por aluno e por dia (revisão de 22/10): o limite do fornecedor é partilhado por
-- todos, e este contador impede que uma só conta o gaste (ORIENTACAO_MAX_PEDIDOS_DIA).
CREATE TABLE IF NOT EXISTS pedidos_llm (
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    dia         TEXT    NOT NULL,  -- UTC, AAAA-MM-DD
    total       INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, dia)
);

-- Decisões do percurso (US31): cada escolha de curso é uma linha; o curso do perfil é o da
-- decisão mais recente (RF03). O nome do curso e da instituição ficam guardados como estavam no
-- momento da escolha, para a linha do tempo não mudar se o catálogo mudar (RF35).
CREATE TABLE IF NOT EXISTS decisoes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    curso_chave     TEXT    NOT NULL,  -- identificador do catálogo (instituição-curso)
    curso           TEXT    NOT NULL,
    instituicao     TEXT    NOT NULL,
    origem          TEXT    NOT NULL CHECK (origem IN ('sugestao', 'catalogo')),
    sugeridos       TEXT    NOT NULL,  -- JSON: cursos sugeridos pelo assistente nessa altura ([] se nenhum)
    decidida_em     TEXT    NOT NULL   -- UTC, ISO 8601
);
CREATE INDEX IF NOT EXISTS decisoes_por_utilizador ON decisoes (user_id, decidida_em);

-- Plano de candidatura (23/10, protótipo): as notas do aluno e as até 6 opções, por ordem.
-- Uma linha por aluno; sai com a conta (US17). As notas só servem para as contas do OptaBem.
CREATE TABLE IF NOT EXISTS planos_candidatura (
    user_id         INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    media           REAL,              -- média do secundário, 0 a 20 (vazio = ainda não indicou)
    exames          TEXT    NOT NULL DEFAULT '{}',  -- JSON: {"18": 140.0, …} (código da prova -> 0 a 200)
    opcoes          TEXT    NOT NULL DEFAULT '[]',  -- JSON: chaves do catálogo, pela ordem da candidatura
    partilha        TEXT    UNIQUE,    -- código aleatório da ligação só de leitura (vazio = não partilhado)
    atualizado_em   TEXT    NOT NULL   -- UTC, ISO 8601
);

-- Correções ao catálogo feitas na gestão (US39). Ficam por cima dos dados da DGES
-- (dados/catalogo-cursos.csv): uma recolha nova reescreve o CSV, mas não esta tabela.
-- Uma linha por curso corrigido ou escondido; vazio (NULL) = usa o texto da DGES.
CREATE TABLE IF NOT EXISTS correcoes_cursos (
    curso_chave     TEXT    PRIMARY KEY,           -- identificador do catálogo (instituição-curso)
    descricao       TEXT,
    saidas          TEXT,                          -- saídas profissionais, separadas por «;» (como no CSV)
    escondido       INTEGER NOT NULL DEFAULT 0 CHECK (escondido IN (0, 1)),
    alterado_por    TEXT    NOT NULL,              -- nome do administrador
    alterado_em     TEXT    NOT NULL               -- UTC, ISO 8601
);

-- Quem alterou o quê e quando (US39). Guarda o nome do administrador, que fica mesmo se a conta
-- dele for removida. Não tem dados de alunos.
CREATE TABLE IF NOT EXISTS historico_catalogo (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    curso_chave     TEXT    NOT NULL,
    alteracao       TEXT    NOT NULL,              -- códigos separados por vírgula: descricao, saidas, escondido, visivel, reposto
    alterado_por    TEXT    NOT NULL,
    alterado_em     TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS historico_por_curso ON historico_catalogo (curso_chave, alterado_em);
