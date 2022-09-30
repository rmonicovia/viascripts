#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os


'''
Arquivo de configuração:

perfis:
  monico:
    empresaFuncionario: 49
    empresaFilial: 21
    filial: 1000
    bandeira: 1
    username: 60000723
    password: xxx
    scope: webclient
    grant_type: password
    canalVenda: ViaMais
    padrao: true
    ambientes:
      - prd:
          padrao: true

ambientes:
  - prd:
      url: http://api-jornada.casasbahia.net/uaa/oauth/token


A entrada "perfis" também é obrigatória, deve conter perfis válidos.
Os nomes dos perfis podem ser arbitrários, porém,dentro de um perfil é obrigatório existir as entradas 'padrao' e 'ambientes'. As demais são todas opcionais (mas sem elas o request de geração de token não vai funcionar).
A entrada "ambientes" é obrigatória. Porém pode estar vazia (nesse caso deve passar o parâmetro --ambiente.

O arquivo de configuração deve ficar localizado em $HOME/.config/viatoken/config.yaml
'''


def _log(level, message):
    print(f'[{level.upper()}]  {message}')

def _warn(message):
    _log('warn', message)

def _error(message, exit_code=1):
    _log('error', message)
    sys.exit(exit_code)


try:
    import requests
except ModuleNotFoundError:
    _error('Módulo "requests" não instalado', -1)


import shutil

if not shutil.which('xclip'):
    _error('Comando "xclip" não encontrado, finalizando...')


# Disable breakpoints
# breakpoint = lambda: None


def _parse_command_line():
    '''
    Reference: https://docs.python.org/3/library/argparse.html
    '''
    parser = argparse.ArgumentParser(
        description='Gera um token para o vendedor online')

    parser.add_argument('-p', '--profile', help='Perfil que será usado para logar no Via+')
    # parser.add_argument('-l', '--list', help='Apenas lista os perfis disponíveis')
    parser.add_argument('-u', '--url', help='URL onde a token será gerado')
    parser.add_argument('-e', '--environment', help='Seleciona o ambiente onde o token é gerado')
    parser.add_argument('-c', '--clipboard', help='Salva o token para a área de transferência')
    parser.add_argument('--password', help='Override profile password')

    # TODO
    # parser.add_argument('--file', help='Salva o token para um arquivo')
    # parser.add_argument('--stdout', help='Imprime o token para a saída padrão')

    return parser.parse_args()


def _getConfigFile():
    return '{HOME}/.config/viatoken/config.yml'.format(**os.environ)


def _getPerfilConfig(nome_perfil, configs):
    for nome, perfil in configs.get('perfis').items():
        if nome != nome_perfil and not perfil.get('padrao', False):
            continue

        if args.password:
            p = dict(perfil)
            p['password'] = args.password
            return p
        else:
            return perfil

    _error(f'Perfil não encontrado: {nome_perfil}')


def _getAmbientePadrao(ambientes):
    # FIXME Se não existir uma entrada de ambientes no perfil selecionado, dá erro aqui
    for ambiente in ambientes:
        if isinstance(ambiente, dict):
            l = list(ambiente.items())
            if l[0][1].get('padrao', False):
                return l[0][0]

    return None


def _getUrl(args, ambientes_perfil, ambientes):
    if args.url:
        return args.url

    amb = args.environment or _getAmbientePadrao(ambientes_perfil)

    if not amb:
        raise Exception('"--amb" ou um ambiente padrão deve ser definido')

    for ambiente in ambientes:
        nome_ambientes = list(ambiente.keys())[0]

        if nome_ambientes == amb:
            return ambiente.get(amb).get('url')

    raise Exception('Ambiente não encontrado: "{}"', amb)


def _makeRequestArgs(empresaFuncionario, empresaFilial, filial, bandeira, username, password, url):
    headers = {
        "Authorization": "Basic Y2xpZW50YXBwOnBhc3N3b3Jk",
    }

    body = {
        "empresaFuncionario": empresaFuncionario,
        "empresaFilial": empresaFilial,
        "filial": filial,
        "bandeira": bandeira,
        "username": username,
        "password": password,
        "scope": "webclient",
        "grant_type": "password",
        "canalVenda": "ViaMais",
    }

    return {
        "url": url,
        "data": body,
        "headers": headers,
        # TODO Gerar um certificado SSL
        "verify": False,
    }


def _getRequestArgs(args, configs):
    profile = _getPerfilConfig(args.profile, configs)

    url = _getUrl(args, profile['ambientes'], configs.get('ambientes'))

    params = profile
    params.pop('ambientes')
    params.pop('padrao')

    return params


def _copy_to_clipboard(contents):
    from tempfile import TemporaryFile

    with TemporaryFile() as temp_file:
        temp_file.write(contents.encode())

        temp_file.seek(0)

        import subprocess

        process = subprocess.run('xclip -selection clipboard'.split(' '), stdin=temp_file)


    if process.returncode != 0:
        _error(f'Comando "xclip" retornou status não-zero ({process.returncode})', 1)


class GeracaoTokenException(Exception):

    def __init__(self, response):
        super(Exception, self).__init__(f'Erro gerando token: {response.text}, status http: {response.status_code}')
        self.response = response


PRD_URL = 'http://api-jornada.casasbahia.net/uaa/oauth/token'

def generate(empresaFuncionario, empresaFilial, filial, bandeira, username, password, url=PRD_URL):
    request_args = _makeRequestArgs(empresaFuncionario, empresaFilial, filial, bandeira, username, password, url)

    with requests.post(**request_args) as response:
        if response.status_code != 200:
            raise GeracaoTokenException(response)

        response_body = response.json()

    return response_body['access_token']


def _main():
    global args

    args = _parse_command_line()

    with open(_getConfigFile()) as f:
        import yaml

        configs = yaml.safe_load(f)

    request_args = _getRequestArgs(args, configs)

    try:
        token = generate(**request_args)
    except GeracaoTokenException as e:
        _error(str(e), 1)

    if args.clipboard:
        _copy_to_clipboard(token)
        print('Token copiado para a área de transferência')
    else:
        print(token)



if __name__ == '__main__':
    _main()

