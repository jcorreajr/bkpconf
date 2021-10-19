## Arquivo de configuração

# Log de erros
logfile = '/backup/log/bkpconf.log'

# Log com o sumário das tarefas executadas
logsumario = '/backup/log/sumario.log'

# Diretório para armazenamento do histórico de backup compactado
dirhistorico = '/backup/historico/'

# Manter quantos dias de histórico
manterhistdias = 4

# Modo interativo; Faz perguntas de confirmação em cada backup S/N [v0.2]
interativo = 'S'

# Porta utilizada pelo SSH [v0.3]
portassh = '2225'

## Configuração de email [v0.4]
emailhost = 'servidor.email.com.br'
emailport = 587
emailfrom = 'origem@dominio.com.br'
emailto = 'destino@dominio.com.br'
