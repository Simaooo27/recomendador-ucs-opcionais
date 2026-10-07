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
APP_NAME = "Recomendador de UCs opcionais"

# Como o título de cada página aparece no separador do navegador.
PAGE_TITLE_FORMAT = "{pagina} · {aplicacao}"

# Botão na barra do topo quando há sessão iniciada.
LOGOUT_BUTTON = "Terminar sessão"

# ---------------------------------------------------------------------------
# Página «Criar conta» (/auth/registo)
# ---------------------------------------------------------------------------

REGISTER_TITLE = "Criar conta"
REGISTER_INTRO = "Use o seu email institucional. Vamos enviar-lhe uma ligação para confirmar a conta."

REGISTER_EMAIL_LABEL = "Email institucional"
REGISTER_EMAIL_HINT = "Terminado em {dominios}."

REGISTER_PASSWORD_LABEL = "Palavra-passe"
REGISTER_PASSWORD_HINT = "Pelo menos {minimo} caracteres, com uma letra e um número."

REGISTER_PASSWORD_CONFIRM_LABEL = "Repita a palavra-passe"

# A expressão «política de privacidade» é a ligação para a página da política.
REGISTER_PRIVACY_BEFORE_LINK = "Li e aceito a "
REGISTER_PRIVACY_LINK = "política de privacidade"
REGISTER_PRIVACY_AFTER_LINK = "."

REGISTER_BUTTON = "Criar conta"

# Ligação por baixo do formulário, para quem já tem conta.
REGISTER_HAVE_ACCOUNT = "Já tem conta? "
REGISTER_LOGIN_LINK = "Inicie sessão"

# Mensagens de erro do formulário de registo.
ERROR_EMAIL_REQUIRED = "Indique o seu email institucional."
ERROR_EMAIL_DOMAIN = "Use o seu email institucional (terminado em {dominios})."
ERROR_EMAIL_DUPLICATE = "Já existe uma conta com este email. Se é a sua, inicie sessão."
ERROR_PASSWORD_REQUIRED = "Escolha uma palavra-passe."
ERROR_PASSWORD_TOO_SHORT = "A palavra-passe deve ter pelo menos {minimo} caracteres."
ERROR_PASSWORD_TOO_LONG = "A palavra-passe não pode ter mais de {maximo} caracteres."
ERROR_PASSWORD_COMPOSITION = "A palavra-passe deve incluir pelo menos uma letra e um número."
ERROR_PASSWORD_MISMATCH = "As palavras-passe não coincidem."
ERROR_PRIVACY_REQUIRED = "É necessário aceitar a política de privacidade para criar a conta."
ERROR_EMAIL_SEND_FAILED = "Não foi possível enviar o email de confirmação. Tente de novo dentro de alguns minutos."

# ---------------------------------------------------------------------------
# Página «Iniciar sessão» (/auth/entrar)
# ---------------------------------------------------------------------------

LOGIN_TITLE = "Iniciar sessão"
LOGIN_INTRO = "Entre com o email e a palavra-passe com que criou a conta."
LOGIN_EMAIL_LABEL = "Email"
LOGIN_PASSWORD_LABEL = "Palavra-passe"
LOGIN_BUTTON = "Entrar"
LOGIN_NO_ACCOUNT = "Ainda não tem conta? "
LOGIN_REGISTER_LINK = "Crie uma conta"

# A mesma mensagem para email inexistente e palavra-passe errada (não revela que emails têm conta).
ERROR_LOGIN_INVALID = "Email ou palavra-passe incorretos."
ERROR_LOGIN_INACTIVE = "Ainda não confirmou o seu email. Abra a ligação que lhe enviámos para ativar a conta."

# ---------------------------------------------------------------------------
# Página inicial do aluno (/inicio), depois de iniciar sessão
# ---------------------------------------------------------------------------

HOME_TITLE = "Início"
HOME_GREETING = "Olá, {email}"
HOME_INTRO = "Tem a sessão iniciada. As recomendações de UCs opcionais vão aparecer aqui."

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

# ---------------------------------------------------------------------------
# Email de confirmação
# ---------------------------------------------------------------------------

CONFIRMATION_EMAIL_SUBJECT = "Confirme o seu registo"
CONFIRMATION_EMAIL_BODY = (
    "Olá,\n\n"
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
# Página «Política de privacidade» (/privacidade)
# ---------------------------------------------------------------------------

PRIVACY_TITLE = "Política de privacidade"
PRIVACY_VERSION = "Versão {versao}"
# Texto provisório: a equipa substitui pelo texto final da política (RNF01).
PRIVACY_BODY = (
    "Texto provisório. A política final descreve que dados são recolhidos (email, percurso e "
    "avaliações), com que finalidade (recomendar opcionais), como são protegidos (avaliações "
    "pseudonimizadas e nunca mostradas individualmente) e como exercer os direitos de acesso, "
    "exportação e apagamento."
)

# ---------------------------------------------------------------------------
# Páginas de erro
# ---------------------------------------------------------------------------

ERROR_PAGE_TITLE = "Erro"
NOT_FOUND_TITLE = "Página não encontrada"
NOT_FOUND_MESSAGE = "A página que procura não existe."
BAD_REQUEST_TITLE = "Pedido inválido"
ERROR_BACK_LINK = "Voltar ao registo"
