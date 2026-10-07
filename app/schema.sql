-- Esquema da base de dados (SQLite). Seguro de executar várias vezes.

CREATE TABLE IF NOT EXISTS users (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    email                   TEXT    NOT NULL UNIQUE COLLATE NOCASE,
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
