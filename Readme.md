# Script para execução de backup: 
- Deve ser executado no servidor de armazenamento de backup
- Utiliza rsync para fazer a cópia dos dados nos servidores de origem, salvando na pasta de destino
```bash
# python3 main.py
```
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
- Em caso de erro na execução de backup ele envia um email informando

## Configurações:
- Lista de servidores e pastas à serem backupeadas no arquivo "servidores.json" em formato json
- Configurações gerais no arquivo "config.py", conforme comentários
### Exemplo de configuração de servidores com uma ou mais pastas de origem:
```json
{

  "server1": {
    "origembkp": ["/etc", "/usr/local"],
    "destinobkp": "/dir/destino/bkp"
  },

   "server2": {
    "origembkp": ["/etc/dhcp"],
    "destinobkp": "/dir/destino/bkp"
  }

}
```
