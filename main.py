# TODO: Script para backup de configuração dos servidores Linux
'''
* Requisitos *
- Programas: rsync (armazenador e alvo), tar
- Conta com acesso <sem senha> por ssh no servidor de origem dos arquivos
-- Usar por exemplo o ssh-copy-id para isso

* Bugs *

* FALTA desenvolver *
- opção de porta SSH no .conf
- tratamento de erro de conexão com timeout partindo para próximo host
- Alguma segurança para não subscrever a origem do backup caso inverta na configuração


-------------------  Funcionalidades
. Lê arquivo .json com nome do servidor + ip para conexão + origem do bkp1 + origem do bkp*

. Faz cópia dos arquivos para destino backup

. guarda log detalhado em caso de erros

. guarda data_hora + status do backup se ok ou não em arquivo .log

. Após backup de todos os servidores:
. Faz compactação individual por pasta
. Mantem arquivos com 'x' dias

'''

from config import *
import shlex
import os
import subprocess
import datetime
import json
from pathlib import Path

cont = 0
now = datetime.datetime.now()

def bkprsync(fhostbkp, forigembkp, fdestinobkp):
    global cont
    forigembkplista = ''

    cont += 1
    # Verifica se existe pasta de destino
    try:
        os.makedirs(fdestinobkp)
        if interativo in ['s', 'S']:
            print("Diretório ", fdestinobkp, " criado ")
    except FileExistsError:
        if interativo in ['s', 'S']:
            print()

    # Montagem do comando de execução
    forigembkplista = 'root@' + fhostbkp + ':' + forigembkp
    cmd = shlex.split('rsync -av --delete -e "ssh -p 2225"' + ' ' + forigembkplista + ' ' + fdestinobkp)
    if interativo in ['s', 'S']:
        print(f'...Debug (Comando):.. \n{cmd}')
    retorno = subprocess.run(cmd, capture_output=True)
    dataexecucao = datetime.datetime.now().isoformat()
    if retorno.returncode == 0:
        statusexec = 'OK'
    else:
        statusexec = 'ERRO'
        errolog(fhostbkp, retorno, dataexecucao)

    # Grava sumário com saída
    sumariolog(fhostbkp, forigembkp, statusexec, dataexecucao)
    return retorno


def sumariolog(fhostbkp, f2origembkp, fstatusbkp, fdataexecucao):
    if cont == 1:
        file = open(f'{logsumario}', 'w+')
    else:
        file = open(f'{logsumario}', 'a+')
    file.write(f'{fstatusbkp} - {fhostbkp} - {f2origembkp} - {fdataexecucao}\n')
    file.close()


def errolog(fhostbkp, ferrobkp, fdataexecucao):
    file = open(f'{logfile}', 'a+')
    file.write(f'--------\n')
    file.write(f'Erro no backup:.. {fdataexecucao} Servidor:.. {fhostbkp} Erro:.. {ferrobkp}\n')
    file.write(f'--------\n')
    file.close()


def verifica(fhostbkp, forigembkp, fdestinobkp):
    ''' Verifica se os dados estão OK para iniciar o backup '''
    if fhostbkp and forigembkp and fdestinobkp != '':
        if interativo in ['S', 's']:
            print('')
            print(f'Host a ser backupeado:.. {fhostbkp}')
            print(f'Pasta(s) de origem de backup:.. ')
            print(f'-'*20)
            for v in forigembkp:
                print(f'→ {v}')
            print(f'-'*20)
            print(f'Pasta de destino de backup:.. {fdestinobkp}')
            confirma = input('Fazer backup? (S/N):.. ')
            confirma = confirma.upper()
            return confirma
        else:
            confirma = 'S'
            return confirma


def carregajson():
    # carrega arquivo json
    with open('servidores.json', 'r') as file:
        d1_json = file.read()
        d1_dict = json.loads(d1_json)
    return d1_dict

def executa():
    # carrega variaveis
    dict_servers = carregajson()

    # separa variaveis do dicionário
    for k, v in dict_servers.items():
        hostbkp = k
        for k1, v1 in v.items():
            if k1 == 'destinobkp':
                destinobkp = v1 + '/' + hostbkp
            if k1 == 'origembkp':
                origembkp = v1
        # para cada variável faz verificacao:
        verificacao = verifica(hostbkp, origembkp, destinobkp)
        #  .. Se verifica OK faz bkprsync
        if verificacao == 'S':
            if interativo in ['s', 'S']:
                print(f'\n... Executando bkp de {hostbkp}, origem: {origembkp}, destino {destinobkp}')

            # Faz for e executa o comando rsync para cada origem analisando saida de cada rsync
            for vorigembkp in origembkp:
                bkprsync(hostbkp, vorigembkp, destinobkp)

            # Compacta backup
            destinobkpcomp = dirhistorico + hostbkp + "_" + now.strftime("%Y%m%d_%H%M%S") + ".tar.gz"
            fazertarfile(destinobkpcomp, destinobkp)

            # Remove backups antigos no histórico
            manterhistorico(hostbkp)

        else:
            if interativo in ['s', 'S']:
                print('.. saindo ..')


def fazertarfile(output_filename, source_dir):
    try:
        cmd = ['tar', 'Pczf', output_filename, source_dir]
        output = subprocess.run(cmd, capture_output=True, text=True)
        if output.returncode != 0:
            errolog('Error Tar', output.stderr, datetime.datetime.now().isoformat())
            errolog('Error Saida padrão', output.stdout, datetime.datetime.now().isoformat())
    except (IOError, EOFError, Exception) as e:
        errolog('Error tar IO', e, datetime.datetime.now().isoformat())
        pass


def manterhistorico(fhostbkp):
    past_time = datetime.date.today() - datetime.timedelta(days=manterhistdias)
    for path in Path(dirhistorico).iterdir():
        timestamp = datetime.date.fromtimestamp(path.stat().st_mtime)
        if past_time > timestamp:
            if fhostbkp + '_' in str(path) and '.tar.gz' in str(path):
                try:
                    if interativo in ['s', 'S']:
                        print(f'arquivo apagado {path}')
                    os.remove(path)
                except OSError as e:
                    if interativo in ['s', 'S']:
                        print(f"Error:{e.strerror}")
                    errolog(fhostbkp, e.strerror, datetime.datetime.now().isoformat())


executa()
