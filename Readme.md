# Script para execução de backup: 
- Deve ser executado no servidor de armazenamento de backup
- Utiliza rsync para fazer a cópia dos dados nos servidores de origem, salvando na pasta de destino

## Requisitos:
- Programas: rsync (armazenador e alvo), tar
- Conta com acesso <sem senha> por ssh no servidor de origem dos arquivos
  - Usar por exemplo o ssh-copy-id para isso

## Funcionalidades:
- Lê arquivo "servidores.json" com nome do servidor + ip para conexão + origem do bkp1 + origem do bkp*
- Faz cópia dos arquivos para destino backup
- Guarda log detalhado em caso de erros
- Guarda data_hora + status do backup se ok ou não em arquivo .log
- Após backup de todos os servidores:
  - Faz compactação individual por pasta
  - Mantem arquivos com 'x' dias

## Configurações:
- Lista de servidores e pastas à serem backupeadas no arquivo "servidores.json" em formato json
- Configurações gerais no arquivo "config.py", conforme comentários
### Exemplo de configuração de servidores com uma ou mais pastas de origem:

