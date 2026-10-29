"""Todos os textos que o utilizador vê na aplicação.

COMO ALTERAR UM TEXTO
1. Encontre o texto neste ficheiro (Ctrl+F no VS Code).
2. Mude apenas o que está entre aspas. Não mude o nome em MAIÚSCULAS à esquerda do "=".
3. Palavras entre chavetas, como {email} ou {horas}, são preenchidas pela aplicação:
   pode mudá-las de sítio na frase, mas não as apague nem lhes mude o nome.
4. Guarde o ficheiro e recarregue a página no navegador (com a aplicação a correr em
   modo --debug, a alteração aparece logo).
5. Corra os testes: python -m unittest discover -s tests -t .

Os textos estão agrupados pela página onde aparecem, pela ordem em que surgem no ecrã.
"""

# ---------------------------------------------------------------------------
# Geral: aparece em todas as páginas
# ---------------------------------------------------------------------------

# Nome da aplicação: barra do topo e separador do navegador.
APP_NAME = "OptaBem: escolher curso"

# Marca: nome curto na barra do topo e no painel das páginas de entrada.
BRAND_NAME = "OptaBem"
# Frase grande e frase de apoio no painel com o percurso (criar conta, iniciar sessão, confirmar email).
BRAND_TAGLINE = "Escolha o curso com ajuda, sem decidir às cegas."
BRAND_SUPPORT = "Compare cursos de várias instituições e decida com a opinião de outros alunos."

# ---------------------------------------------------------------------------
# Página de apresentação (/), para quem ainda não tem sessão iniciada
# ---------------------------------------------------------------------------

LANDING_TITLE = "Escolher curso"
# Barra do topo da apresentação: fica presa ao topo ao percorrer a página, por isso é o único
# sítio com «Entrar» e «Criar conta» (decisão do PO de 22/10: antes havia 2 e 3 de cada).
# Desde 23/10 ficam no menu do ícone de conta (NAV_CONTA), ao lado da lupa (NAV_PROCURAR).
LANDING_NAV_CURSOS = "Cursos"
LANDING_NAV_COMO = "Como funciona"
LANDING_NAV_PARA_QUEM = "Para quem"
LANDING_NAV_LOGIN = "Entrar"
LANDING_NAV_REGISTER = "Criar conta"

# Pesquisa de cursos (dados reais do catálogo da DGES, dados/catalogo-cursos-mvp.csv).
LANDING_SEARCH_NOTE = "comece por aqui"   # escrito à mão por cima da caixa de pesquisa
LANDING_SEARCH_LABEL = "Procure um curso, uma instituição ou uma cidade"
LANDING_SEARCH_PLACEHOLDER = "Ex.: informática, gestão, Porto…"
LANDING_SEARCH_BUTTON = "Procurar"
LANDING_SEARCH_AREAS = "Ou veja por área:"
# Os números {cursos}, {instituicoes} e {vagas} são contados a partir do catálogo.
LANDING_STATS = "{cursos} licenciaturas de {instituicoes} instituições, com {vagas} vagas no concurso de 2026."
LANDING_RESULTS_SAMPLE = "Alguns cursos do catálogo"
LANDING_RESULTS_FOUND = "Resultados para «{termo}»"
LANDING_RESULTS_COUNT = "A mostrar {mostrados} de {total}."
LANDING_NO_RESULTS = "Nenhum curso encontrado para «{termo}». Experimente uma área ou uma cidade."
LANDING_CARD_VAGAS = "Vagas em 2026"
LANDING_CARD_NOTA = "Último colocado em 2025"
LANDING_CARD_NO_NOTA = "Sem dados"
LANDING_CARD_SOURCE = "Ver na DGES"
LANDING_DATA_SOURCE = "Dados públicos da DGES: vagas do concurso nacional de 2026 e nota do último colocado na 1.ª fase de 2025 (escala 0–200)."

# Página do catálogo (/cursos/): a pesquisa acima numa página própria, também para quem tem sessão
# iniciada (ligação «Procurar no catálogo» da conversa de orientação, US30). Os filtros, a ficha
# e a comparação de cursos são a US05.
# ---------------------------------------------------------------------------
# Escolher curso e linha do tempo das decisões (/percurso, US31).
# ---------------------------------------------------------------------------

# Botão em cada ficha de curso (cursos sugeridos e catálogo).
CURSO_ESCOLHER = "Escolher este curso"
PERCURSO_ESCOLHER_TITLE = "Escolher curso"
# RN10: a escolha só fica registada depois de confirmar.
PERCURSO_ESCOLHER_INTRO = "Confirme a sua escolha. Pode mudar de curso mais tarde: cada mudança fica registada."
# {curso} e {instituicao} são o curso atual.
PERCURSO_CURSO_ATUAL = "O seu curso atual é {curso}, {instituicao}. Ao confirmar, passa a ser este."
PERCURSO_JA_ESCOLHIDO = "Este já é o seu curso."
# Ponto 15 dos requisitos (decisão do PO de 20/10): depois de escolher, a conversa é apagada.
PERCURSO_CONVERSA_APAGADA = (
    "Ao confirmar, a sua conversa com o assistente é apagada. Ficam guardados só a data, os cursos "
    "sugeridos e o curso que escolheu."
)
PERCURSO_CONFIRMAR = "Confirmar a escolha"
PERCURSO_CANCELAR = "Voltar sem escolher"
PERCURSO_ESCOLHA_REGISTADA = "Escolha registada: {curso}, {instituicao}."
PERCURSO_JA_E_O_SEU_CURSO = "Esse curso já é o seu curso atual: não foi registada uma nova decisão."

PERCURSO_TITLE = "As minhas decisões"
PERCURSO_INTRO = "Cada vez que escolhe ou muda de curso, a decisão fica registada aqui, da mais recente para a mais antiga."
PERCURSO_VAZIO = "Ainda não escolheu nenhum curso."
PERCURSO_ATUAL = "Curso atual"
# {data} vem no formato dia/mês/ano.
PERCURSO_DATA = "Escolhido a {data}"
PERCURSO_DA_SUGESTAO = "Escolhido entre os cursos sugeridos pelo assistente."
PERCURSO_DO_CATALOGO = "Escolhido no catálogo."
PERCURSO_SUGERIDOS = "Cursos sugeridos nessa altura:"
PERCURSO_MUDAR_TITULO = "Mudar de curso"
PERCURSO_NOVA_CONVERSA = "Nova conversa com o assistente"
PERCURSO_PROCURAR = "Procurar no catálogo"

CATALOGO_TITLE = "Catálogo de cursos"
CATALOGO_VOLTAR = "Voltar à conversa de orientação"
# Filtros do catálogo (US05). Funcionam sem JavaScript: «Aplicar filtros» recarrega a página.
CATALOGO_INTRO = "Filtre por área, instituição ou localidade, abra a ficha de cada curso e compare até {maximo} cursos lado a lado."
CATALOGO_FILTROS = "Filtrar cursos"
CATALOGO_FILTRO_AREA = "Área"
CATALOGO_FILTRO_INSTITUICAO = "Instituição"
CATALOGO_FILTRO_LOCALIDADE = "Localidade"
CATALOGO_FILTRO_TODAS = "Todas"
CATALOGO_APLICAR = "Aplicar filtros"
CATALOGO_LIMPAR = "Limpar filtros"
CATALOGO_CONTA = "{mostrados} de {total} cursos"
CATALOGO_CONTA_TODOS = "Todos os {total} cursos do catálogo"
CATALOGO_VAZIO = "Nenhum curso corresponde a estes filtros. Experimente tirar um deles."
# Paginação do catálogo (US04: o catálogo completo tem mais de mil cursos; 24 por página).
CATALOGO_PAGINAS = "Páginas do catálogo"
CATALOGO_PAGINA = "Página {numero} de {paginas}"
CATALOGO_ANTERIOR = "← Anterior"
CATALOGO_SEGUINTE = "Seguinte →"
# Comparar: cada ficha tem uma caixa «Comparar»; o botão leva à comparação lado a lado.
CATALOGO_COMPARAR_CAIXA = "Comparar"
CATALOGO_COMPARAR_BOTAO = "Comparar os cursos marcados"
CATALOGO_COMPARAR_AJUDA = "Marque 2 ou {maximo} cursos e carregue em «Comparar os cursos marcados»."
# Substitui a ajuda acima quando há cursos marcados (só com JavaScript). {n} é o número de cursos
# marcados (preenchido por app/static/app.js) e {maximo} o máximo que se compara.
CATALOGO_COMPARAR_MARCADOS = "Cursos marcados: {n} de {maximo}."
CATALOGO_VER_FICHA = "Ver ficha completa"

# Ficha de um curso (/cursos/<curso>, US05).
FICHA_VOLTAR = "Voltar ao catálogo"
FICHA_SOBRE = "Sobre o curso"
FICHA_SAIDAS = "Saídas profissionais"
FICHA_ACESSO = "Acesso"
FICHA_DADOS = "Dados do curso"
FICHA_INSTITUICAO = "Instituição"
FICHA_UNIDADE = "Escola ou faculdade"
FICHA_LOCALIDADE = "Localidade"
FICHA_TIPO = "Tipo de ensino"
FICHA_GRAU = "Grau"
FICHA_DURACAO = "Duração"
FICHA_DURACAO_VALOR = "{semestres} semestres"
FICHA_ECTS = "Créditos (ECTS)"
FICHA_AREA_OFICIAL = "Área de estudo oficial (CNAEF)"
FICHA_FONTES = "Fontes"
FICHA_FONTE_DGES = "Vagas e notas: página do curso na DGES"
FICHA_FONTE_DESCRICAO = "Descrição: página da instituição"
FICHA_COMPARAR = "Comparar com outros cursos"
FICHA_SEM_DADOS = "Sem dados"

# Comparação lado a lado (/cursos/comparar, US05).
COMPARAR_TITLE = "Comparar cursos"
COMPARAR_INTRO = "Os cursos lado a lado, com os dados oficiais da DGES e a descrição de cada instituição."
COMPARAR_POUCOS = "Para comparar, escolha pelo menos {minimo} cursos do catálogo."
COMPARAR_A_MAIS = "Só se comparam {maximo} cursos de cada vez: ficaram os primeiros {maximo} que marcou."
COMPARAR_IGNORADOS = "Alguns cursos não foram encontrados no catálogo e ficaram de fora."
COMPARAR_CURSO = "Curso"
COMPARAR_DESLIZAR = "Deslize a tabela para o lado para ver todos os cursos."   # só no telemóvel
COMPARAR_ESCOLHER_OUTROS = "Escolher outros cursos"
# Grupos de linhas da comparação (revisão estética de 23/10).
COMPARAR_GRUPO_NUMEROS = "Em números"
COMPARAR_GRUPO_ONDE = "Onde e como"
COMPARAR_GRUPO_CURSO = "O curso"
COMPARAR_DURACAO = "{anos} anos ({semestres} semestres)"
COMPARAR_VER_DGES = "Ver na DGES"

LANDING_HOW_TITLE = "Como funciona"
# Os três passos, pela ordem em que acontecem.
LANDING_STEPS = [
    {"titulo": "Converse com o assistente", "texto": "Algumas perguntas sobre os seus interesses, o tipo de trabalho que imagina e onde quer estudar."},
    {"titulo": "Compare os cursos sugeridos", "texto": "Cursos de várias instituições, lado a lado, com vagas, nota do último colocado e saídas profissionais, e o motivo de cada sugestão."},
    {"titulo": "Escolha e registe o seu percurso", "texto": "A decisão fica guardada na linha do tempo do seu percurso. Se mudar de ideias, pode escolher outro curso."},
]

LANDING_FOR_TITLE = "Para quem:"
LANDING_FOR = [
    {"titulo": "Ainda não escolheu o curso", "texto": "Explore cursos de várias instituições e receba sugestões a partir dos seus interesses."},
    {"titulo": "Já escolheu, mas tem dúvidas", "texto": "Volte a conversar com o assistente ou procure no catálogo. Se escolher outro curso, a decisão anterior fica na linha do tempo."},
]

LANDING_FOOTER = "Projeto académico de Metodologias Ágeis (Scrum)."
LANDING_PRIVACY_LINK = "Política de privacidade"

# Como o título de cada página aparece no separador do navegador.
PAGE_TITLE_FORMAT = "{pagina} · {aplicacao}"

# Ícone de olho junto dos campos de palavra-passe (texto lido por leitores de ecrã e ao passar o rato).
SHOW_PASSWORD = "Mostrar palavra-passe"
HIDE_PASSWORD = "Esconder palavra-passe"

# Barra do topo quando há sessão iniciada.
LOGOUT_BUTTON = "Terminar sessão"
# Aviso na página inicial depois de terminar a sessão (desde 23/10 volta-se à apresentação).
LOGOUT_FEITO = "Sessão terminada. Até breve!"
NAV_LABEL = "Menu"
# Ícones à direita da barra do topo, em todas as páginas (revisão estética de 23/10, pedido do PO).
# A lupa abre uma caixa de pesquisa no catálogo; o ícone de conta abre um menu com «Entrar» e
# «Criar conta» (sem sessão) ou «A minha conta» e «Terminar sessão» (com sessão). Os textos são
# lidos por leitores de ecrã e aparecem ao passar o rato.
NAV_PROCURAR = "Procurar cursos"
NAV_CONTA = "Conta"
NAV_MINHA_CONTA = "A minha conta"
# Menu dos alunos, na barra do topo (app/templates/base.html).
NAV_INICIO = "Início"
NAV_CONVERSA = "Conversa"
NAV_CATALOGO = "Catálogo"
NAV_CANDIDATURA = "Candidatura"

# ---------------------------------------------------------------------------
# Página «Criar conta» (/auth/registo)
# ---------------------------------------------------------------------------

REGISTER_TITLE = "Criar conta"
REGISTER_INTRO = "Use o seu email pessoal. Vamos enviar-lhe uma ligação para confirmar a conta."

REGISTER_NOME_LABEL = "Nome"
REGISTER_NOME_HINT = "Como gostava de ser tratado no OptaBem, por exemplo «Ana Silva»."

REGISTER_EMAIL_LABEL = "Email"
REGISTER_EMAIL_HINT_ANY = "Por exemplo, nome@gmail.com."
# Só aparece se a equipa restringir os domínios aceites (ALLOWED_EMAIL_DOMAINS em app/config.py).
REGISTER_EMAIL_HINT = "Terminado em {dominios}."

REGISTER_PASSWORD_LABEL = "Palavra-passe"
REGISTER_PASSWORD_HINT = "Pelo menos {minimo} caracteres, com uma letra e um número."

REGISTER_PASSWORD_CONFIRM_LABEL = "Repita a palavra-passe"

# Lista que se vai marcando enquanto escreve a palavra-passe (só aparece com JavaScript).
REGISTER_RULE_LENGTH = "Pelo menos {minimo} caracteres"
REGISTER_RULE_LETTER = "Uma letra"
REGISTER_RULE_NUMBER = "Um número"
REGISTER_RULE_MATCH = "As duas palavras-passe coincidem"

# A expressão «política de privacidade» é a ligação para a página da política.
REGISTER_PRIVACY_BEFORE_LINK = "Li e aceito a "
REGISTER_PRIVACY_LINK = "política de privacidade"
REGISTER_PRIVACY_AFTER_LINK = "."

REGISTER_BUTTON = "Criar conta"

# Ligação por baixo do formulário, para quem já tem conta.
REGISTER_HAVE_ACCOUNT = "Já tem conta? "
REGISTER_LOGIN_LINK = "Inicie sessão"

# Mensagens de erro do formulário de registo.
ERROR_NOME_REQUIRED = "Indique o seu nome."
ERROR_NOME_INVALID = "Use só letras, espaços, hífens e apóstrofos (até {maximo} caracteres)."
ERROR_EMAIL_REQUIRED = "Indique o seu email."
ERROR_EMAIL_INVALID = "Indique um email válido, por exemplo nome@gmail.com."
ERROR_EMAIL_DOMAIN = "Use um email terminado em {dominios}."
ERROR_EMAIL_DUPLICATE = "Já existe uma conta com este email. Se é a sua, inicie sessão."
ERROR_PASSWORD_REQUIRED = "Escolha uma palavra-passe."
ERROR_PASSWORD_TOO_SHORT = "A palavra-passe deve ter pelo menos {minimo} caracteres."
ERROR_PASSWORD_TOO_LONG = "A palavra-passe não pode ter mais de {maximo} caracteres."
ERROR_PASSWORD_COMPOSITION = "A palavra-passe deve incluir pelo menos uma letra e um número."
ERROR_PASSWORD_MISMATCH = "As palavras-passe não coincidem."
ERROR_PRIVACY_REQUIRED = "É necessário aceitar a política de privacidade para criar a conta."
ERROR_EMAIL_SEND_FAILED = "Não foi possível enviar o email de confirmação. Tente de novo dentro de alguns minutos."

# ---------------------------------------------------------------------------
# Página «Iniciar sessão» (/auth/entrar) — a mesma para alunos e administradores
# Os administradores escrevem o nome de utilizador no campo «Email». O rótulo diz só «Email»
# para a gestão continuar invisível aos alunos; pode mudar-se para «Email ou nome de utilizador».
# ---------------------------------------------------------------------------

LOGIN_TITLE = "Iniciar sessão"
LOGIN_INTRO = "Entre com o email e a palavra-passe com que criou a conta."
LOGIN_EMAIL_LABEL = "Email"
LOGIN_PASSWORD_LABEL = "Palavra-passe"
LOGIN_BUTTON = "Entrar"
LOGIN_NO_ACCOUNT = "Ainda não tem conta? "
LOGIN_REGISTER_LINK = "Crie uma conta"

# A mesma mensagem para email inexistente e palavra-passe errada (não revela que emails têm conta).
# Também é a mensagem dos administradores, para o formulário não revelar que a gestão existe.
ERROR_LOGIN_INVALID = "Email ou palavra-passe incorretos."
ERROR_LOGIN_INACTIVE = "Ainda não confirmou o seu email. Abra a ligação que lhe enviámos para ativar a conta."

# ---------------------------------------------------------------------------
# Página inicial do aluno (/inicio), depois de iniciar sessão
# ---------------------------------------------------------------------------

HOME_TITLE = "Início"
HOME_GREETING = "Olá!"
# Com nome (desde 23/10): {nome} é o primeiro nome indicado no registo.
HOME_GREETING_NOME = "Olá, {nome}!"
# Contas criadas antes de 23/10 ainda não têm nome: um convite para o indicar.
HOME_SEM_NOME = "Diga-nos como gostava de ser tratado em "
HOME_SEM_NOME_LIGACAO = "A minha conta"
# Atalhos por baixo do percurso (revisão estética de 23/10). «destino» é a página (endpoint do Flask).
HOME_ATALHOS_TITULO = "O que pode fazer"
HOME_ATALHOS = [
    {"titulo": "Conversar com o assistente", "texto": "Fale dos seus interesses e receba 2 a 3 cursos sugeridos.", "destino": "orientacao.pagina"},
    {"titulo": "Explorar o catálogo", "texto": "Filtre, abra a ficha de cada curso e compare até 3 lado a lado.", "destino": "catalogo.lista"},
    {"titulo": "Plano de candidatura", "texto": "Calcule a sua nota de candidatura e ordene as suas 6 opções.", "destino": "candidatura.plano"},
]

# Página «A minha conta» (/auth/conta), no menu do ícone de conta. Desde 23/10 é aqui que fica
# «Apagar a minha conta» (US17), em vez de no fundo da página inicial (decisão do PO).
CONTA_TITLE = "A minha conta"
CONTA_EMAIL = "Email"
CONTA_NOME = "Nome"
CONTA_NOME_SEM = "Ainda não indicou o seu nome."
CONTA_NOME_ALTERAR = "Guardar nome"
CONTA_NOME_GUARDADO = "Nome guardado."
CONTA_DESDE = "Conta criada a"
# Desde 23/10 «As minhas decisões» (US31) não está no menu: fica aqui e no passo «Escolher curso» do início.
CONTA_DECISOES = "As minhas decisões"
CONTA_DECISOES_TEXTO = "Os cursos que foi escolhendo e quando."
CONTA_APAGAR_TITULO = "Apagar a conta"
CONTA_APAGAR_TEXTO = "Apaga a conta e todos os dados do seu percurso. Não pode ser desfeito."
HOME_CONTA_APAGAR = "Apagar a minha conta e todos os meus dados"

# Página «Apagar a minha conta» (/auth/conta/apagar, US17).
APAGAR_TITLE = "Apagar a minha conta"
APAGAR_INTRO = "Esta ação não pode ser desfeita. São apagados para sempre:"
APAGAR_ITENS = [
    "a sua conta e o seu email;",
    "a conversa de orientação, se ainda existir;",
    "todas as decisões do seu percurso (cursos escolhidos);",
    "o registo de pedidos ao assistente.",
]
APAGAR_PASSWORD_LABEL = "Para confirmar, escreva a sua palavra-passe"
APAGAR_BOTAO = "Apagar a minha conta"
APAGAR_CANCELAR = "Cancelar e voltar à minha conta"
APAGAR_ERRO_PASSWORD = "A palavra-passe não está certa. A conta não foi apagada."
APAGAR_FEITO = "A sua conta e todos os seus dados foram apagados."
HOME_INTRO = "Este é o seu percurso. Cada passo concluído fica registado aqui."

# Linha do tempo «O seu percurso» (app/percurso/__init__.py decide em que passo está cada pessoa).
HOME_PATH_TITLE = "O seu percurso"
# Cada passo: «titulo», «texto» (enquanto está por fazer) e, opcionalmente, «feito» (o texto
# depois de concluído). O texto do passo «Escolher curso» concluído é HOME_CURSO_ESCOLHIDO.
HOME_PATH_STEPS = [
    {"titulo": "Conta criada", "texto": "O seu email está confirmado."},
    {"titulo": "Conversa de orientação", "texto": "Responda a algumas perguntas sobre os seus interesses para receber sugestões de curso.",
     "feito": "Pode voltar a conversar com o assistente sempre que quiser."},
    {"titulo": "Escolher curso", "texto": "Compare os cursos sugeridos e registe a sua escolha."},
    {"titulo": "Preparar a candidatura", "texto": "Indique as suas notas, veja a sua nota em cada curso e ordene as suas 6 opções."},
]
HOME_ACTION_CANDIDATURA = "Preparar a candidatura"
HOME_STEP_DONE = "Concluído"
HOME_STEP_CURRENT = "Próximo passo"
HOME_STEP_LATER = "Depois"
HOME_NEXT_SOON = "Disponível em breve."
# Botão no passo atual da linha do tempo (só nos passos que já existem).
HOME_ACTION_CONVERSA = "Começar a conversa"
HOME_ACTION_CONTINUAR = "Ver os cursos sugeridos"
# Depois de escolher o curso (US31): o passo «Escolher curso» mostra-o. {curso} e {instituicao} vêm do catálogo.
HOME_CURSO_ESCOLHIDO = "Escolheu {curso}, {instituicao}."
HOME_ACTION_VER_PERCURSO = "Ver as minhas decisões"

# ---------------------------------------------------------------------------
# Conversa de orientação (/orientacao, US29): o assistente (LLM) faz as perguntas.
# O que o assistente diz vem do LLM; as instruções que ele segue estão em
# app/orientacao/instrucoes.md.
# ---------------------------------------------------------------------------

ORIENTACAO_TITLE = "Conversa de orientação"
# {maximo} é o número máximo de perguntas (LIMITE_PERGUNTAS em app/orientacao/conversa.py).
ORIENTACAO_INTRO = (
    "O assistente faz-lhe algumas perguntas (no máximo {maximo}) sobre o que gosta e o que imagina fazer. "
    "No fim, sugere 2 a 3 cursos do catálogo."
)
# Aviso de privacidade (RNF12), sempre visível nesta página.
ORIENTACAO_AVISO = (
    "Não escreva dados pessoais, como o nome, o email ou o telefone. As suas respostas são enviadas a um "
    "serviço externo de inteligência artificial, sem o seu email nem o seu nome."
)
# Ponto 14 dos requisitos, decidido a 20/10: protótipo da equipa, com este aviso (os termos do Gemini excluem menores de 18).
ORIENTACAO_IDADE = "Por agora, esta conversa destina-se a maiores de 18 anos."
ORIENTACAO_COMECAR = "Começar a conversa"
# Assistente que conhece as minhas notas (US37): só com autorização, numa caixa ao começar a conversa.
ORIENTACAO_NOTAS_CAIXA = "Usar os exames que fiz e a minha média, para o assistente não me sugerir cursos a que não posso concorrer"
# {exames}: os nomes dos exames; {media}: ORIENTACAO_NOTAS_INTERVALO ou ORIENTACAO_NOTAS_SEM_MEDIA.
ORIENTACAO_NOTAS_O_QUE = (
    "O assistente recebe só isto: os exames que fez ({exames}) e a sua média do secundário {media}. "
    "Nunca recebe a média exata nem a nota de cada exame."
)
ORIENTACAO_NOTAS_INTERVALO = "entre {inicio} e {fim} valores"
ORIENTACAO_NOTAS_SEM_MEDIA = "(ainda não a indicou)"
ORIENTACAO_NOTAS_SEM_BEFORE_LINK = "Se indicar os exames que fez no "
ORIENTACAO_NOTAS_SEM_LINK = "plano de candidatura"
ORIENTACAO_NOTAS_SEM_AFTER_LINK = ", o assistente pode tê-los em conta (só se autorizar)."
ORIENTACAO_NOTAS_LIGADO = (
    "Nesta conversa, o assistente sabe os exames que fez e a sua média aproximada. Para deixar de os usar, "
    "recomece a conversa."
)
# Num curso sugerido a que falta uma prova de ingresso (US37). {provas}: «Matemática A e Física e Química A».
ORIENTACAO_FALTA_PROVA = "Atenção: para concorrer a este curso falta-lhe o exame de {provas}."
ORIENTACAO_FALTA_PROVA_JUNTAR = " e "
ORIENTACAO_ASSISTENTE = "Assistente"
ORIENTACAO_VOCE = "Você"
# {numero} é a pergunta atual e {maximo} o limite.
ORIENTACAO_PROGRESSO = "Pergunta {numero} de, no máximo, {maximo}"
ORIENTACAO_RESPOSTA_LABEL = "A sua resposta"
ORIENTACAO_RESPOSTA_HINT = "Até {maximo} caracteres. Emails e números de telefone são apagados antes de enviar."
ORIENTACAO_ENVIAR = "Enviar"
ORIENTACAO_TENTAR_DE_NOVO = "Tentar de novo"
ORIENTACAO_A_ESPERA = "O assistente não chegou a responder. A sua resposta está guardada: tente de novo."
ORIENTACAO_RECOMECAR = "Recomeçar a conversa"

# Pedir as sugestões antes do fim (US30). O pedido fica na conversa como mensagem do aluno
# e é também o que o assistente recebe.
ORIENTACAO_VER_SUGESTOES = "Ver sugestões já"
ORIENTACAO_VER_SUGESTOES_HINT = "Se já disse o suficiente, o assistente sugere cursos agora, sem mais perguntas."
ORIENTACAO_PEDIDO_SUGESTAO = "Prefiro ver já as sugestões de curso."

# Cursos sugeridos no fim da conversa (US30). Os cursos e os números vêm do catálogo;
# a explicação de cada curso vem do assistente.
ORIENTACAO_SUGESTOES_TITULO = "Cursos sugeridos para si"
ORIENTACAO_PORQUE = "Porque combina consigo"
# RN10: nenhum curso é escolhido automaticamente; a escolha é a US31.
ORIENTACAO_ESCOLHA_DEPOIS = (
    "Nenhum curso fica escolhido por si. Compare-os com calma e, quando decidir, escolha um destes "
    "ou outro do catálogo."
)
# Menos de 2 cursos do catálogo (os outros foram descartados, RN09).
ORIENTACAO_POUCAS_SUGESTOES = (
    "O assistente não encontrou cursos suficientes no catálogo que combinem com as suas respostas. "
    "Pode continuar a conversa, para lhe dar mais pistas, ou procurar no catálogo."
)
ORIENTACAO_CONTINUAR_CONVERSA = "Continuar a conversa"
ORIENTACAO_VER_CATALOGO = "Procurar no catálogo"

ORIENTACAO_ERRO_VAZIA = "Escreva uma resposta antes de enviar."
ORIENTACAO_ERRO_LONGA = "A resposta pode ter até {maximo} caracteres. Encurte-a um pouco."
# O limite do serviço externo é partilhado por todos os utilizadores (por minuto e por dia).
ORIENTACAO_ERRO_LIMITE = (
    "O assistente está com muitos pedidos neste momento. Tente de novo dentro de um minuto; "
    "se continuar, o limite diário foi atingido e volta a funcionar amanhã."
)
ORIENTACAO_ERRO_LLM = "Não foi possível falar com o assistente. A sua conversa está guardada: tente de novo."
# Limite de pedidos ao assistente por aluno e por dia (ORIENTACAO_MAX_PEDIDOS_DIA em app/config.py).
ORIENTACAO_ERRO_LIMITE_ALUNO = (
    "Já fez muitos pedidos ao assistente hoje. A sua conversa está guardada: pode continuar amanhã."
)

# ---------------------------------------------------------------------------
# Área de gestão (administradores, US03). Endereço em ADMIN_URL_PREFIX (por omissão /gestao).
# Nenhuma destas páginas tem ligações a partir das páginas dos alunos.
# ---------------------------------------------------------------------------

ADMIN_AREA_NAME = "Gestão"
ADMIN_NAV_DASHBOARD = "Painel"
ADMIN_NAV_ADMINS = "Administradores"
# Ativar contas por confirmar (23/10): enquanto o site não envia emails reais, um administrador ativa-as aqui.
ADMIN_NAV_CONTAS = "Contas por confirmar"
ADMIN_CONTAS_TITULO = "Contas por confirmar"
ADMIN_CONTAS_INTRO = (
    "Enquanto o OptaBem não envia emails a sério, as contas novas ficam aqui até um administrador as ativar. "
    "Ative só contas de pessoas que conhece: ativar salta a confirmação do email."
)
ADMIN_CONTAS_VAZIO = "Não há contas por confirmar."
ADMIN_COL_NOME = "Nome"
ADMIN_COL_EMAIL = "Email"
ADMIN_COL_REGISTO = "Registo"
ADMIN_ATIVAR = "Ativar"
ADMIN_ATIVAR_ROTULO = "Ativar a conta {email}"
ADMIN_CONTA_ATIVADA = "Conta {email} ativada: já pode iniciar sessão."

# Os administradores entram pela página «Iniciar sessão» dos alunos, com o nome de utilizador
# no campo do email (app/auth/perfis.py). Estes rótulos são do formulário «Novo administrador».
ADMIN_USERNAME_LABEL = "Nome de utilizador"
ADMIN_PASSWORD_LABEL = "Palavra-passe"

ADMIN_DASHBOARD_TITLE = "Painel de gestão"
ADMIN_DASHBOARD_GREETING = "Olá, {nome}."
# Indicadores no topo do painel.
ADMIN_STATS_TITLE = "Neste momento"
ADMIN_STAT_STUDENTS = "Alunos com conta ativa"
ADMIN_STAT_PENDING = "Contas por confirmar"
ADMIN_STAT_ADMINS = "Administradores"
ADMIN_STAT_LAST_SIGNUP = "Último registo"
ADMIN_STAT_NONE = "Ainda nenhum"
ADMIN_DASHBOARD_INTRO = "Nos próximos sprints, esta área vai permitir:"
# Uma linha por funcionalidade prevista (pode acrescentar ou retirar linhas).
ADMIN_UPCOMING = [
    "Importar o catálogo de cursos e UCs a partir de um ficheiro CSV.",
    "Abrir e fechar os períodos de avaliação.",
    "Moderar comentários.",
]

ADMIN_LIST_TITLE = "Administradores"
ADMIN_LIST_INTRO = "Os administradores têm contas próprias, separadas das contas dos alunos."
ADMIN_COL_USERNAME = "Nome de utilizador"
ADMIN_COL_CREATED = "Criado em"
ADMIN_COL_CREATED_BY = "Criado por"
ADMIN_COL_LAST_LOGIN = "Última entrada"
ADMIN_CREATED_BY_TERMINAL = "terminal"
ADMIN_NEVER = "nunca"
ADMIN_YOU = "(você)"
ADMIN_REMOVE_BUTTON = "Remover"
ADMIN_NEW_TITLE = "Novo administrador"
ADMIN_USERNAME_HINT = "3 a 30 caracteres: letras minúsculas, números, ponto, hífen ou sublinhado."
ADMIN_PASSWORD_HINT = "Pelo menos {minimo} caracteres, com uma letra e um número."
ADMIN_PASSWORD_CONFIRM_LABEL = "Repita a palavra-passe"
ADMIN_CREATE_BUTTON = "Criar administrador"
ADMIN_CREATED = "Administrador «{nome}» criado."
ADMIN_REMOVED = "Administrador «{nome}» removido."
ERROR_ADMIN_REMOVE_SELF = "Não pode remover a sua própria conta. Peça a outro administrador."
ERROR_ADMIN_USERNAME_REQUIRED = "Indique um nome de utilizador."
ERROR_ADMIN_USERNAME_FORMAT = "Use 3 a 30 caracteres: letras minúsculas, números, ponto, hífen ou sublinhado."
ERROR_ADMIN_USERNAME_TAKEN = "Já existe um administrador com este nome."

# Comandos de terminal (create-admin, list-admins).
CLI_ADMIN_USERNAME_PROMPT = "Nome de utilizador"
CLI_ADMIN_PASSWORD_PROMPT = "Palavra-passe"
CLI_ADMIN_PASSWORD_CONFIRM_PROMPT = "Repita a palavra-passe"
CLI_ADMIN_CREATED = "Administrador «{nome}» criado. Inicie sessão em {endereco} com este nome no campo do email."
CLI_NO_ADMINS = "Ainda não há administradores. Use: flask --app app create-admin"

# ---------------------------------------------------------------------------
# Página «Confirme o seu email» (depois de criar a conta)
# ---------------------------------------------------------------------------

PENDING_TITLE = "Confirme o seu email"
PENDING_SENT_TO = "Enviámos uma ligação de confirmação para"
PENDING_SENT_TO_END = ". Abra-a para ativar a conta."
PENDING_SENT_GENERIC = "Enviámos uma ligação de confirmação para o seu email. Abra-a para ativar a conta."
PENDING_HELP_BEFORE_LINK = "Não chegou? Veja a pasta de spam. Se a ligação expirar, volte a "
PENDING_HELP_LINK = "criar a conta"
PENDING_HELP_AFTER_LINK = " com o mesmo email para receber uma nova."

# Só aparece em desenvolvimento (MAIL_BACKEND=console), quando não é enviado email real.
DEV_LINK_NOTE = "Modo de desenvolvimento: não foi enviado nenhum email real. Use a ligação abaixo para confirmar a conta (também aparece no terminal)."
DEV_LINK_BUTTON = "Confirmar a conta agora"

# ---------------------------------------------------------------------------
# Email de confirmação
# ---------------------------------------------------------------------------

CONFIRMATION_EMAIL_SUBJECT = "Confirme o seu registo"
CONFIRMATION_EMAIL_HELLO = "Olá,\n\n"
CONFIRMATION_EMAIL_HELLO_NOME = "Olá, {nome},\n\n"
CONFIRMATION_EMAIL_BODY = (
    "Recebemos um pedido de registo com este email. Para ativar a conta, abra a "
    "ligação abaixo nas próximas {horas} horas:\n\n"
    "{ligacao}\n\n"
    "Se não fez este pedido, ignore esta mensagem: a conta não será ativada.\n"
)

# ---------------------------------------------------------------------------
# Página de resultado da confirmação (quando o aluno abre a ligação do email)
# ---------------------------------------------------------------------------

CONFIRMATION_PAGE_TITLE = "Confirmação de email"

CONFIRMED_TITLE = "Conta ativada"
CONFIRMED_MESSAGE = "O seu email foi confirmado e a conta está ativa."
CONFIRMED_LOGIN_LINK = "Iniciar sessão"

ALREADY_CONFIRMED_TITLE = "Conta já ativa"
ALREADY_CONFIRMED_MESSAGE = "Este email já tinha sido confirmado. Não precisa de fazer mais nada."

EXPIRED_TITLE = "Ligação expirada"
EXPIRED_MESSAGE = "Esta ligação já não é válida."
EXPIRED_HELP_LINK = "Crie a conta de novo"
EXPIRED_HELP_AFTER_LINK = " com o mesmo email para receber uma ligação nova."

INVALID_TITLE = "Ligação inválida"
INVALID_MESSAGE = "Não foi possível confirmar o email com esta ligação."
INVALID_HELP_BEFORE_LINK = "Copie a ligação completa do email que recebeu ou "
INVALID_HELP_LINK = "crie a conta de novo"
INVALID_HELP_AFTER_LINK = " para receber uma nova."

# ---------------------------------------------------------------------------
# Plano de candidatura (/candidatura, protótipo de 23/10): notas, nota por curso e as 6 opções
# do Concurso Nacional de Acesso. As contas estão em app/candidatura/calculos.py.
# ---------------------------------------------------------------------------

CANDIDATURA_TITULO = "Plano de candidatura"
CANDIDATURA_INTRO = (
    "Junte até 6 cursos pela ordem em que os quer: na candidatura, fica colocado na primeira opção "
    "em que a sua nota chegue. A candidatura em si faz-se no site da DGES."
)
CANDIDATURA_AVISO_ESTIMATIVA = (
    "As contas são uma estimativa para o contingente geral da 1.ª fase, com as regras publicadas pela DGES. "
    "A nota do último colocado muda todos os anos: é uma referência, não uma garantia."
)
CANDIDATURA_AS_MINHAS_NOTAS = "As minhas notas"
CANDIDATURA_MEDIA_RESUMO = "Média do secundário: {media}"
CANDIDATURA_EXAMES_RESUMO = "Exames: {exames}"
CANDIDATURA_SEM_EXAMES = "Ainda não indicou exames."
CANDIDATURA_SEM_NOTAS = "Indique a sua média do secundário e os exames que fez para ver a sua nota em cada curso."
CANDIDATURA_INDICAR_NOTAS = "Indicar as minhas notas"
CANDIDATURA_MUDAR_NOTAS = "Mudar as notas"
CANDIDATURA_AS_MINHAS_OPCOES = "As minhas opções ({n} de {maximo})"
CANDIDATURA_VAZIO = "Ainda não juntou nenhum curso. Abra a ficha de um curso no catálogo e carregue em «Juntar ao plano»."
CANDIDATURA_JUNTAR_ESCOLHIDO = "Juntar {curso} ({instituicao}) como 1.ª opção"
CANDIDATURA_PROCURAR = "Procurar cursos no catálogo"
CANDIDATURA_OPCAO = "{posicao}.ª opção"
CANDIDATURA_A_SUA_NOTA = "A sua nota"
CANDIDATURA_ULTIMO = "Último colocado 2025"
CANDIDATURA_SUBIR = "Subir"
CANDIDATURA_DESCER = "Descer"
CANDIDATURA_RETIRAR = "Retirar"
CANDIDATURA_SUBIR_ROTULO = "Subir {curso}"
CANDIDATURA_DESCER_ROTULO = "Descer {curso}"
CANDIDATURA_RETIRAR_ROTULO = "Retirar {curso} do plano"
CANDIDATURA_AVISOS_TITULO = "Antes de submeter"
CANDIDATURA_AVISO_NAO_CONTAM = "{n} opção(ões) não conta(m) para a colocação: veja o que falta em cada uma."
CANDIDATURA_AVISO_SEM_SEGURA = (
    "Nenhuma opção está claramente acima do último colocado. Pense em juntar pelo menos um curso onde fique acima, "
    "para não arriscar ficar sem colocação."
)
CANDIDATURA_AVISO_ORDEM = (
    "A 1.ª opção ({curso}) é das mais fáceis de entrar. Se ficar colocado nela, as opções seguintes já não contam: "
    "ponha primeiro os cursos de que mais gosta, mesmo que sejam mais difíceis."
)
CANDIDATURA_AVISO_MENOS_DE_6 = "Tem {n} opção(ões). Pode juntar mais {livres}: usar as 6 não prejudica as primeiras."
CANDIDATURA_AVISO_PRE_REQUISITOS = "Há opções com pré-requisitos (por exemplo, atestados médicos ou provas físicas): confirme-os no site da DGES."
CANDIDATURA_SUGESTOES_TITULO = "Outros cursos de {area} onde tem hipóteses"
CANDIDATURA_JUNTAR = "Juntar ao plano"
CANDIDATURA_NO_PLANO = "Já está no seu plano"
CANDIDATURA_VER_PLANO = "Ver o meu plano"
CANDIDATURA_JUNTADO = "{curso} juntado ao plano de candidatura."
CANDIDATURA_CHEIO = "O plano já tem {maximo} opções: retire uma antes de juntar outra."
CANDIDATURA_FORA_DO_CONCURSO = (
    "Este curso é do ensino privado e não entra nas 6 opções do concurso nacional: "
    "a candidatura faz-se diretamente na instituição."
)
CANDIDATURA_NOTAS_GUARDADAS = "Notas guardadas."

# Que exames me abrem mais portas? (23/10): combinações de até 3 exames para as opções do plano.
EXAMES_TITULO = "Que exames lhe abrem mais portas?"
EXAMES_INTRO = "Com estes exames nacionais, pode concorrer a mais opções do seu plano. Ajuda a decidir que exames fazer."
EXAMES_ABRE = "Dá para {n} de {total} opções"
EXAMES_FALTA = "Não dá para: {cursos}"
EXAMES_TODAS = "Dá para todas as opções do plano."
EXAMES_JA_FEZ = "Já fez: {provas}"

# Plano B: 2.ª fase (23/10).
PLANO_B_TITULO = "Plano B: 2.ª fase"
PLANO_B_INTRO = (
    "Se não ficar colocado na 1.ª fase, estes cursos das mesmas áreas tiveram vagas na 2.ª fase de 2025 "
    "e a sua nota chegava ao último colocado dessa fase. As vagas da 2.ª fase são as que sobram da 1.ª: mudam todos os anos."
)
PLANO_B_VAZIO = (
    "Ainda não há um plano B: nenhum outro curso das áreas do seu plano teve vagas na 2.ª fase de 2025 "
    "a que a sua nota chegasse. Quando o catálogo tiver todas as licenciaturas da DGES, aparecerão mais cursos."
)
PLANO_B_DETALHE = "Vagas na 2.ª fase de 2025: {vagas} · último colocado: {ultimo}"
PLANO_B_SOBRARAM = "Vagas na 2.ª fase de 2025: {vagas} · sobraram lugares"

# Partilhar o plano (23/10): ligação só de leitura.
PARTILHA_SECCAO = "Partilhar o plano"
PARTILHA_EXPLICACAO = (
    "Crie uma ligação para mostrar o plano a quem o ajuda a decidir (pais, explicador, um colega). "
    "Quem a abrir vê o seu primeiro nome, as opções, a nota de candidatura e a situação em cada uma. "
    "Não vê o seu email, a média nem as notas dos exames."
)
PARTILHA_CRIAR = "Criar ligação de partilha"
PARTILHA_LIGACAO = "Ligação para partilhar"
PARTILHA_COPIAR = "Selecione e copie a ligação. Qualquer pessoa com ela vê o plano, sem iniciar sessão."
PARTILHA_DESLIGAR = "Deixar de partilhar"
PARTILHA_LIGADA = "Ligação de partilha criada."
PARTILHA_DESLIGADA = "A ligação deixou de funcionar."
PARTILHA_TITULO = "Plano de candidatura de {nome}"
PARTILHA_TITULO_SEM_NOME = "Plano de candidatura"
PARTILHA_INTRO = "Plano partilhado no OptaBem, só de leitura. As opções estão pela ordem em que a pessoa as quer."
PARTILHA_VAZIO = "Este plano ainda não tem opções."
PARTILHA_NOTA = "Nota de candidatura"
PARTILHA_CONVITE = "Também está a escolher curso? Experimente o OptaBem."

# Situação de cada opção (CANDIDATURA_SITUACAO_ + o valor de Situacao em app/candidatura/calculos.py).
# {diferenca} já vem com sinal e vírgula (ex.: «+7,7»).
CANDIDATURA_SITUACAO_ACIMA = "Acima do último colocado ({diferenca})"
CANDIDATURA_SITUACAO_PERTO = "Perto do último colocado ({diferenca})"
CANDIDATURA_SITUACAO_ABAIXO = "Abaixo do último colocado ({diferenca})"
CANDIDATURA_SITUACAO_SEM_REFERENCIA = "Cumpre os mínimos (sem nota do último colocado em 2025)"
CANDIDATURA_SITUACAO_ABAIXO_DO_MINIMO = "Abaixo da classificação mínima"
CANDIDATURA_SITUACAO_FALTA_PROVA = "Falta-lhe uma prova de ingresso"
CANDIDATURA_SITUACAO_SEM_NOTAS = "Indique as suas notas para ver a sua nota"
CANDIDATURA_SITUACAO_SEM_REGRAS = "A DGES não publica as condições de acesso deste curso"
CANDIDATURA_SITUACAO_FORA_DO_CONCURSO = "Ensino privado: não entra no concurso nacional (candidatura na instituição)"
CANDIDATURA_FALTA = "Falta: {provas}"
CANDIDATURA_MINIMO_PROVA = "Abaixo do mínimo de {minimo} pontos: {provas}"
CANDIDATURA_MINIMO_NOTA = "A nota de candidatura fica abaixo do mínimo de {minimo} pontos."
CANDIDATURA_CONJUNTO_USADO = "Conta com: {provas}"

# Formulário das notas (/candidatura/notas)
CANDIDATURA_NOTAS_TITULO = "As minhas notas"
CANDIDATURA_NOTAS_INTRO = "Só servem para as contas do plano. Pode mudá-las quando quiser, e saem com a conta se a apagar."
CANDIDATURA_MEDIA = "Média do secundário"
CANDIDATURA_MEDIA_DICA = "De 9,5 a 20 valores, por exemplo 15,2."
CANDIDATURA_EXAMES = "Exames nacionais (provas de ingresso)"
CANDIDATURA_EXAMES_DICA = (
    "Preencha só os que fez, de 0 a 200 pontos (ou de 0 a 20 valores: 14,5 conta como 145). "
    "Na Matemática, indique o exame que fez: a Matemática A também conta para as provas de Matemática e de MACS."
)
CANDIDATURA_GUARDAR = "Guardar e ver o plano"
CANDIDATURA_VOLTAR = "Voltar ao plano"
CANDIDATURA_ERRO_MEDIA_VAZIA = "Indique a sua média do secundário."
CANDIDATURA_ERRO_MEDIA = "A média tem de estar entre 9,5 e 20 valores."
CANDIDATURA_ERRO_EXAME = "Use um número de 0 a 200 (ou de 0 a 20)."

# «Quanto preciso no exame?» (23/10): ficha do curso e opções do plano a que falta uma prova.
FICHA_PRECISA_TITULO = "Quanto precisa no exame?"
FICHA_PRECISA = "Para chegar a {alvo} ({referencia}), precisa de {pontos} pontos ({valores} valores) em {provas}."
FICHA_PRECISA_REF_ULTIMO = "o último colocado em 2025"
FICHA_PRECISA_REF_MINIMO = "a nota mínima do curso"
FICHA_PRECISA_VARIAS = "Faltando mais de uma prova, a conta supõe a mesma nota em todas."
FICHA_PRECISA_IMPOSSIVEL = "Com a sua média, mesmo com 200 pontos nas provas a nota fica em {maximo}, abaixo de {alvo} ({referencia})."
FICHA_PRECISA_SEM_MEDIA = "Indique a sua média do secundário para saber quanto precisa nos exames."
CANDIDATURA_PRECISA = "Precisa de {pontos} em {provas}"

# Tendência do último colocado e procura (23/10), na ficha do curso e no plano.
FICHA_HISTORICO = "Último colocado (1.ª fase)"
FICHA_TENDENCIA_SOBE = "A subir"
FICHA_TENDENCIA_DESCE = "A descer"
FICHA_TENDENCIA_ESTAVEL = "Estável"
FICHA_PROCURA = "Procura em 2025"
FICHA_PROCURA_SOBRARAM = "Sobraram vagas na 1.ª fase"
FICHA_PROCURA_MUITA = "Muito procurado"
FICHA_PROCURA_MEDIA = "Procurado"
FICHA_PROCURA_POUCA = "Pouco escolhido em 1.ª opção"
FICHA_PROCURA_DETALHE = "{candidatos} candidatos para {vagas} vagas; {primeira} puseram-no em 1.ª opção e ficaram {colocados} colocados."

# Ficha do curso: condições de acesso (dados da DGES)
FICHA_ACESSO = "Condições de acesso"
FICHA_PROVAS = "Provas de ingresso"
FICHA_PROVAS_UM_DE = "Basta um destes conjuntos:"
FICHA_FORMULA = "Fórmula da nota de candidatura"
FICHA_FORMULA_VALOR = "{secundario}% média do secundário + {provas}% provas de ingresso"
FICHA_MINIMOS = "Classificações mínimas"
FICHA_MINIMOS_VALOR = "{candidatura} pontos na nota de candidatura e {provas} em cada prova"
FICHA_PRE_REQUISITOS = "Pré-requisitos"
FICHA_FORA_DO_CONCURSO = (
    "Ensino privado: este curso não entra no Concurso Nacional de Acesso. A candidatura faz-se diretamente "
    "na instituição, com as regras dela; as condições abaixo são as que a DGES publica."
)
FICHA_SEM_ACESSO = "A DGES ainda não tem as condições de acesso deste curso no OptaBem. Consulte a página da DGES."
FICHA_A_SUA_NOTA = "A sua nota neste curso"
FICHA_ENTRE_PARA_SIMULAR = "Inicie sessão para calcular a sua nota de candidatura a este curso."

# ---------------------------------------------------------------------------
# Página «Política de privacidade» (/privacidade)
# ---------------------------------------------------------------------------

PRIVACY_TITLE = "Política de privacidade"
PRIVACY_VERSION = "Versão {versao}"
# Texto provisório: a equipa substitui pelo texto final da política (RNF01).
PRIVACY_BODY = (
    "Texto provisório. A política final descreve que dados são recolhidos (nome, email, conversa de "
    "orientação, cursos escolhidos e, no plano de candidatura, as notas que a pessoa indica; o plano só é visto por outras pessoas se ela criar uma ligação de partilha, que pode desligar a qualquer momento), com que finalidade (sugerir cursos), como são protegidos "
    "(a conversa é enviada ao assistente sem emails nem números e é apagada depois de escolher o "
    "curso) e como exercer os direitos de acesso e de apagamento: cada aluno pode apagar a conta e "
    "todos os seus dados em «A minha conta» («Apagar a minha conta»)."
)

# ---------------------------------------------------------------------------
# Páginas de erro
# ---------------------------------------------------------------------------

ERROR_PAGE_TITLE = "Erro"
NOT_FOUND_TITLE = "Página não encontrada"
NOT_FOUND_MESSAGE = "A página que procura não existe."
BAD_REQUEST_TITLE = "Pedido inválido"
NOT_FOUND_HINT = "Este caminho não leva a lado nenhum. Volte ao início e escolha outro."
ERROR_BACK_LINK = "Voltar ao início"
