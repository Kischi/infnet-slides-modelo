"""Mede e quebra textos em Montserrat para planejar o layout antes de enviar a API.

Preparo (uma vez):
    npm pack @fontsource/montserrat && tar xzf fontsource-montserrat-*.tgz
    pip install fonttools brotli --break-system-packages
Uso:
    from medir_texto import largura, quebrar
    largura('NOME DO ORADOR', 8, 700)               -> pontos
    quebrar('frase longa...', 9.5, 234.67)          -> lista de linhas

Altura de linha da Montserrat = 1,219 x tamanho x entrelinha. Linha de base a 0,968 x tamanho do topo.
O kerning nao entra na conta: a largura real costuma ser um pouco menor que a medida.
"""
import os
from fontTools.ttLib import TTFont

PASTA = os.environ.get('MONTSERRAT_DIR', 'package/files')
_F = {}


def _fonte(peso):
    if peso not in _F:
        _F[peso] = TTFont(os.path.join(PASTA, f'montserrat-latin-{peso}-normal.woff2'))
    return _F[peso]


def largura(texto, tamanho, peso=400):
    f = _fonte(peso)
    cmap = f.getBestCmap()
    hm = f['hmtx']
    upm = f['head'].unitsPerEm
    return sum(hm[cmap.get(ord(ch), '.notdef')][0] for ch in texto) * tamanho / upm


def quebrar(texto, tamanho, largura_max, peso=400):
    linhas, atual = [], ''
    for palavra in texto.split(' '):
        tentativa = f'{atual} {palavra}' if atual else palavra
        if largura(tentativa, tamanho, peso) <= largura_max:
            atual = tentativa
        else:
            linhas.append(atual)
            atual = palavra
    linhas.append(atual)
    return linhas
