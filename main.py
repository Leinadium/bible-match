import argparse
import logging
from typing import Union
import json
from html import unescape

from match import detecta_texto


def _create_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path_or_url', action='store', help='path do arquivo ou url de acesso (default: url)', metavar='XXX')
    parser.add_argument('-s', '--silent', action='store_true', help='executa sem exibir nenhum comando no terminal')
    parser.add_argument('-u', '--url', action='store_true', help='XXX é a url para acessar o json.')
    parser.add_argument('-l', '--local', action='store_true', help='XXX é o arquivo json local para acessar. Ignorado se -u for usada')
    parser.add_argument('-o', '--output', action='store', type=argparse.FileType('w+', encoding='utf8'), help='saída contendo os resultados')
    parser.add_argument('-c', '--with_comment', action='store_true', help='salva tambem os comentarios no output')
    return parser.parse_args()


def fetch_json(path:str, tipo:str) -> Union[dict, None]:
    """
    Coleta o json, transformando para um dicionario
    :param path: path para arquivo local ou url
    :param tipo: 'url' ou 'path'
    :return: dicionario contendo as mensagens
    """
    ret:dict = {}

    if tipo == 'url':
        try:
            # adicionado http em path
            if not path.startswith('http://'):
                path = 'http://' + path
            logging.info("Acessando %s" % path)
            import requests
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}
                r = requests.get(path, headers=headers)
                if r.status_code > 400:
                    logging.error("Erro ao conectar em %s, recebi código %d" % (path, r.status_code))
                    exit(-1)
                r.encoding = 'ISO-8859-1'
                ret = r.json()
            except (json.JSONDecodeError, ValueError) as e:
                logging.error("Arquivo JSON inválido. Não foi possível decodificar o GET em um json: %s" % str(e))
                exit(1)
            except requests.ConnectionError:
                logging.error("Erro ao conectar em %s" % path)

        except ModuleNotFoundError:
            logging.error("Módulo 'requests' não encontrado. Instale usando 'python -m pip install requests' ou 'python3 -m pip3 install requests'.")
            exit(1)

    elif tipo == 'local':
        try:
            logging.info("Abrindo arquivo %s" % path)
            with open(path, 'r', encoding='ISO-8859-1') as f:
                ret = json.load(f)
        except OSError:
            logging.error(f"Arquivo {path} não encontrado")
            exit(1)
        except json.JSONDecodeError:
            logging.error("Arquivo JSON inválido")
            exit(1)

    logging.info("Arquivo json coletado [%d items]" % len(ret.keys()))
    return ret


def parse_dict(d:dict, with_comments:bool) -> dict:
    """
    Faz o parsing do dicionario contendo os comentarios.

    :param with_comments: caso seja True, coloca os comentarios originais no dicionario final
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
        detectado = detecta_texto(line_normalizada)
        if with_comments:
            ret[key] = {'comentario': line_normalizada, 'detectado': detectado}
        else:
            ret[key] = detectado

    return ret


def store_dict(d:dict, file):
    """
    Salva o dicionario em um arquivo json
    :param d: dicionario para ser guardado
    :param file: arquivo JSON a ser gerado ou sobrescrito
    """

    json.dump(d, file, indent=2)
    file.close()
    return


def main():
    args = vars(_create_args())
    if args.get('silent'):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    p = args.get('path_or_url')
    t = 'url' if args.get('url') else 'local'
    if args.get('output') is None:
        o = open('resultado.json', 'w+', encoding='utf8')
    else:
        o = args.get('output')
    w = args.get('with_comment')

    dicionario = fetch_json(path=p, tipo=t)
    resultado = parse_dict(dicionario, w)
    store_dict(resultado, o)


if __name__ == "__main__":
    main()
