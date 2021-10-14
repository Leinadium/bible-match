from argparse import ArgumentParser, Namespace
import logging
from typing import Union
import json
from html import unescape

import match
from match import get_dict_compilado, detecta_texto


def _create_args():
    parser = ArgumentParser(description="Processa comentarios contendo referencias biblicas")
    parser.add_argument('-s', '--silent', action='store_true', help='executa sem exibir nenhum comando no terminal')
    parser.add_argument('-u', '--url', action='store', default='http://biblecast.net.br/resources/comentarios.json', help='url para acessar o json')
    parser.add_argument('-l', '--local', action='store', nargs=1, help='especifica um arquivo json local para acessar. Ignorado se URL for especificada')
    parser.add_argument('-o', '--output', action='store', default='resultado.json', help='saída contendo os resultados')
    parser.add_argument('-c', '--with_comment', action='store_true', help='salva tambem os comentarios no output')
    return parser.parse_args()


def fetch_json(local=Union[str, None], url=Union[str, None]) -> Union[dict, None]:
    """
    Coleta o json, transformando para um dicionario
    :param local: path para arquivo local. Ignorado se url não for nula
    :param url: url para coletar o json.
    :return: dicionario contendo as mensagens
    """
    ret:dict = {}

    if url:
        try:
            logging.info("Acessando %s" % url)
            import requests
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}
            r = requests.get(url, headers=headers)
            # r.encoding = 'ISO-8859-1'
            try:
                ret = r.json()
            except (json.JSONDecodeError, ValueError) as e:
                logging.error("Arquivo JSON inválido. Não foi possível decodificar o GET em um json: %s" % str(e))
                exit(1)

        except ModuleNotFoundError:
            logging.error("Módulo 'requests' não encontrado. Instale usando 'python -m pip install requests' ou 'python3 -m pip3 install requests'.")
            exit(1)

    elif local:
        try:
            logging.info("Abrindo arquivo %s" % local)
            with open(local, 'r', encoding='ISO-8859-1') as f:
                ret = json.load(f)
        except OSError:
            logging.error(f"Arquivo {local} não encontrado")
            exit(1)
        except json.JSONDecodeError:
            logging.error("Arquivo JSON inválido")
            exit(1)

    logging.info("Arquivo json coletado [%d items]" % len(ret.keys()))
    return ret


def parse_dict(d:dict, with_comments:bool) -> dict:
    """
    Faz o parsing do dicionario contendo os comentarios.

    :param d: dicionario na forma { 'mensagem', 'observacoes' }
    :return: dicionario na forma { 'mensagem': ['match1', 'match2', ..., 'matchX'] }
    """

    ret = {}

    for count, key in enumerate(d):
        if count % 300 == 0:
            logging.info("Examinadas %s mensagens" % (300 * count // 300))
        line = d[key]
        if type(line) != str:
            logging.error("Arquivo JSON invalido. Campo %s não contem string (%s)" % (key, str(line)))
            exit(1)

        line_normalizada = unescape(line)   # normaliza
        detectado = match.detecta_texto(line_normalizada)
        if with_comments:
            ret[key] = {'comentario': line_normalizada, 'detectado': detectado}
        else:
            ret[key] = detectado

    return ret


def store_dict(d:dict, path:str):
    """
    Salva o dicionario em um arquivo json
    :param d: dicionario para ser guardado
    :param path: path do arquivo JSON a ser gerado ou sobrescrito
    """

    with open(path, 'w+', encoding='utf-8') as f:
        json.dump(d, f, indent=2)
    return


if __name__ == "__main__":
    args = vars(_create_args())
    if args.get('silent'):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    # print(args)
    dicionario = fetch_json(local=args.get('local'), url=args.get('url'))
    expressoes = get_dict_compilado()
    resultado = parse_dict(dicionario, args.get('with_comment'))
    store_dict(resultado, args.get('output'))

