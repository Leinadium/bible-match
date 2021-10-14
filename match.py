import re
import json
from os import path, getcwd
import logging

from typing import List

RE_PATH = path.join(getcwd(), 're.json')
# LOG_PATH = path.join(getcwd(), 'log.txt')
LIVROS_COM_UM_CAPITULO = ['OBA', 'FLM', '2JO', '3JO', 'JUD']
_DICT_COMPILADO = None


def get_dict_compilado() -> dict:
    """
    Cria o dicionario contendo as expressões regulares para cada livro da bíblia.
    Se o dicionario já tiver sido criado, apenas retorna
    :return: dicionario na forma {"XXX": expressão_compilada}
    """
    global _DICT_COMPILADO
    if _DICT_COMPILADO is None:
        try:
            with open(RE_PATH, 'r', encoding='utf-8') as f:
                j: dict = json.load(f)
        except FileNotFoundError:
            logging.error("Arquivo re.json não encontrado")
            exit(1)

        logging.info("Compilando expressões regulares")
        try:
            _DICT_COMPILADO = {x: re.compile(y, re.IGNORECASE) for x, y in j.items()}
        except Exception as e:
            logging.error("Erro compilando expressões: %s", str(e))
            exit(1)

    return _DICT_COMPILADO


def detecta_texto(texto: str) -> List[str]:
    """
    Tenta detectar alguma referência a bíblia no texto
    :param texto: string para ser explorada
    :return: lista contendo as referencias. Pode ser vazia
    """

    d = get_dict_compilado()
    ret = []
    flag_cartas_joao = False
    flag_evangelho_joao = False
    livro_ou_abr, capitulo = "", ""
    for nome, p in d.items():
        i = 0
        while (m := p.search(texto, pos=i)) is not None:
            try:
                livro_ou_abr, capitulo = m.groups()
                if nome in LIVROS_COM_UM_CAPITULO:  # verifica se so tem um capitulo (ignora "capitulo")
                    s = "%s%03d" % (nome, 0)
                elif len(livro_ou_abr) < 4 and capitulo is None and livro_ou_abr != "JOB":
                    # verifica se so pegou a abreviacao (exceto jo)
                    break
                elif capitulo is None or not capitulo:
                    s = "%s%03d" % (nome, 0)
                else:
                    s = "%s%03d" % (nome, int(capitulo))
                if nome == 'JOA':
                    flag_evangelho_joao = True
                elif nome.endswith('JO'):
                    flag_cartas_joao = True
                ret.append(s)
                i = m.end(0)
            except ValueError as e:
                logging.error("Match invalido!\ntexto: [%s], livro: [%s], capitulo: [%s], m: [%s]\ne -> %s",
                            texto, livro_ou_abr, capitulo, str(m), e)
                exit(1)

    # verificando subgrupo (JOA está contido em 1JO)
    if flag_evangelho_joao and flag_cartas_joao:
        ret = [a for a in ret if not a.startswith('JOA')]  # removendo JOAO

    return ret
