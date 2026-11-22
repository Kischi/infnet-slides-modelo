"""Gerador de requests (Slides API batchUpdate) para o modelo visual da Faculdade Infnet.

Uso:
    from slides_modelo import *
    d = Deck('idDaPagina')            # todas as funcoes escrevem em d.R
    d.cartao('c0', 64, 133.27, 266.67, 146)
    d.texto('t0', 80, 152, 234.67, 13, [[('Titulo', 10.5, AZUL, True)]])
    for lote in d.lotes(): ...        # envie cada lote em um batchUpdate

Unidades: pontos (pt). Pagina 960 x 540 pt. So gera JSON; nao chama a API.
"""
import json

EMU = 12700          # 1 pt
BASE = 3_000_000     # tamanho-base (EMU) de toda forma lida de volta pela API
RECUO = 7.2          # recuo interno (pt) de TEXT_BOX criado pela API

# Paleta
MARINHO = '1C3665'; AZUL = '106DB6'; AZUL_CLARO = '689CCB'; AZUL_PALIDO = 'D4EAFF'
AMARELO = 'FFCC2E'; AMARELO_CAPA = 'FEDA0C'
FUNDO = 'F4F5FA'; FUNDO_ESCURO = '14305C'; BRANCO = 'FFFFFF'
TINTA = '0E1A31'; CINZA = '5A6B86'; TRILHA = 'E9EEF6'; TRILHA_ESCURA = '2A4780'
PILULA = 'E2EEF9'; NEUTRO = 'B8C2D1'

# Grade
MARGEM_E, MARGEM_D = 64, 896
Y_KICKER, Y_TITULO, Y_CORPO, Y_FIM = 64, 86.4, 133.27, 511.27
CALHA = 16
COL4 = dict(w=196, x=[64, 276, 488, 700])
COL3 = dict(w=266.67, x=[64, 346.66, 629.33])
COL2 = dict(w=408, x=[64, 488])


def cor(h):
    return {'rgbColor': {'red': round(int(h[0:2], 16) / 255, 4),
                         'green': round(int(h[2:4], 16) / 255, 4),
                         'blue': round(int(h[4:6], 16) / 255, 4)}}


def _pt(v):
    return round(v, 2)


class Deck:
    def __init__(self, pagina):
        self.P = pagina
        self.R = []

    # ---------- primitivas ----------
    def forma(self, oid, tipo, x, y, w, h, c, alpha=None):
        """Forma sem contorno. tipo: RECTANGLE, ROUND_RECTANGLE (raio = menor lado / 6)..."""
        self.R.append({'createShape': {'objectId': oid, 'shapeType': tipo, 'elementProperties': {
            'pageObjectId': self.P,
            'size': {'width': {'magnitude': _pt(w), 'unit': 'PT'}, 'height': {'magnitude': _pt(h), 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': _pt(x), 'translateY': _pt(y), 'unit': 'PT'}}}})
        fill = {'color': cor(c)}
        campos = 'shapeBackgroundFill.solidFill.color,outline.propertyState'
        if alpha is not None:
            fill['alpha'] = alpha
            campos += ',shapeBackgroundFill.solidFill.alpha'
        self.R.append({'updateShapeProperties': {'objectId': oid, 'shapeProperties': {
            'shapeBackgroundFill': {'solidFill': fill}, 'outline': {'propertyState': 'NOT_RENDERED'}},
            'fields': campos}})

    def texto(self, oid, x, y, w, h, paragrafos, alinhar=None, vertical=None, entrelinha=100, depois=0):
        """Caixa de texto cuja AREA DE TEXTO fica em (x, y, w, h); o recuo de 7,2 pt e compensado.
        paragrafos: lista de paragrafos; cada paragrafo e uma lista de trechos (texto, tamanho, cor, negrito).
        entrelinha/depois valem para todos; use self.paragrafo() para ajustar um intervalo."""
        self.R.append({'createShape': {'objectId': oid, 'shapeType': 'TEXT_BOX', 'elementProperties': {
            'pageObjectId': self.P,
            'size': {'width': {'magnitude': _pt(w + 2 * RECUO), 'unit': 'PT'},
                     'height': {'magnitude': _pt(h + 2 * RECUO), 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': _pt(x - RECUO), 'translateY': _pt(y - RECUO),
                          'unit': 'PT'}}}})
        self.R.append({'insertText': {'objectId': oid, 'text': '\n'.join(''.join(t[0] for t in p) for p in paragrafos)}})
        i = 0
        for p in paragrafos:
            for t, tam, c, neg in p:
                self.R.append({'updateTextStyle': {'objectId': oid,
                    'textRange': {'type': 'FIXED_RANGE', 'startIndex': i, 'endIndex': i + len(t)},
                    'style': {'fontFamily': 'Montserrat', 'fontSize': {'magnitude': tam, 'unit': 'PT'},
                              'foregroundColor': {'opaqueColor': cor(c)}, 'bold': neg},
                    'fields': 'fontFamily,fontSize,foregroundColor,bold'}})
                i += len(t)
            i += 1
        est = {'lineSpacing': entrelinha, 'spaceAbove': {'magnitude': 0, 'unit': 'PT'},
               'spaceBelow': {'magnitude': depois, 'unit': 'PT'}}
        campos = 'lineSpacing,spaceAbove,spaceBelow'
        if alinhar:
            est['alignment'] = alinhar
            campos += ',alignment'
        self.R.append({'updateParagraphStyle': {'objectId': oid, 'textRange': {'type': 'ALL'}, 'style': est,
                                                'fields': campos}})
        if vertical:
            self.R.append({'updateShapeProperties': {'objectId': oid, 'shapeProperties': {'contentAlignment': vertical},
                                                     'fields': 'contentAlignment'}})

    def paragrafo(self, oid, ini, fim, entrelinha=100, depois=0):
        self.R.append({'updateParagraphStyle': {'objectId': oid,
            'textRange': {'type': 'FIXED_RANGE', 'startIndex': ini, 'endIndex': fim},
            'style': {'lineSpacing': entrelinha, 'spaceBelow': {'magnitude': depois, 'unit': 'PT'}},
            'fields': 'lineSpacing,spaceBelow'}})

    def imagem(self, oid, url, x, y, w, h):
        """url precisa ser publica (o Slides baixa a imagem na hora)."""
        self.R.append({'createImage': {'objectId': oid, 'url': url, 'elementProperties': {
            'pageObjectId': self.P,
            'size': {'width': {'magnitude': _pt(w), 'unit': 'PT'}, 'height': {'magnitude': _pt(h), 'unit': 'PT'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': _pt(x), 'translateY': _pt(y), 'unit': 'PT'}}}})

    def agrupar(self, gid, ids):
        self.R.append({'groupObjects': {'groupObjectId': gid, 'childrenObjectIds': ids}})

    def para_tras(self, ids):
        self.R.append({'updatePageElementsZOrder': {'pageElementObjectIds': ids, 'operation': 'SEND_TO_BACK'}})

    def para_frente(self, ids):
        self.R.append({'updatePageElementsZOrder': {'pageElementObjectIds': ids, 'operation': 'BRING_TO_FRONT'}})

    def mover(self, oid, x, y, w, h):
        """Reposiciona/redimensiona uma forma JA EXISTENTE (base 3.000.000 EMU). Nao use em tabelas nem grupos."""
        self.R.append({'updatePageElementTransform': {'objectId': oid, 'applyMode': 'ABSOLUTE', 'transform': {
            'scaleX': round(w * EMU / BASE, 6), 'scaleY': round(h * EMU / BASE, 6),
            'translateX': round(x * EMU), 'translateY': round(y * EMU), 'unit': 'EMU'}}})

    # ---------- componentes ----------
    def cartao(self, pref, x, y, w, h, corpo=BRANCO, destaque=AZUL):
        """Cartao com barra de 3 pt no topo e raio fixo de 7 pt, feito em tiras e agrupado como <pref>."""
        ids = [f'{pref}_ac', f'{pref}_bt', f'{pref}_bb', f'{pref}_bm']
        self.forma(ids[0], 'ROUND_RECTANGLE', x + 0.5, y, w - 1, 42, destaque)
        self.forma(ids[1], 'ROUND_RECTANGLE', x, y + 3, w, 42, corpo)
        self.forma(ids[2], 'ROUND_RECTANGLE', x, y + h - 42, w, 42, corpo)
        self.forma(ids[3], 'RECTANGLE', x, y + 15, w, h - 27, corpo)
        self.agrupar(pref, ids)

    def faixa(self, oid, y, h, c=MARINHO, x=MARGEM_E, w=832):
        """Faixa de largura total na base do corpo. Para h entre 42 e 65 o raio fica perto de 7 pt."""
        self.forma(oid, 'ROUND_RECTANGLE', x, y, w, h, c)

    def divisoria(self, oid, x, y, w, c=TRILHA):
        self.forma(oid, 'RECTANGLE', x, y - 0.38, w, 0.75, c)

    def numero(self, pref, x, y, w, numero, legenda, fonte=None, tam=22, tam_leg=9.5):
        """Bloco de dado: numero grande, legenda embaixo e fonte a direita, na linha do numero."""
        self.texto(f'{pref}n', x, y, w, 68, [[(numero, tam, AZUL, True)], [(legenda, tam_leg, TINTA, False)]])
        self.paragrafo(f'{pref}n', 0, len(numero), 100, 2)
        self.paragrafo(f'{pref}n', len(numero) + 1, len(numero) + 1 + len(legenda), 115, 0)
        if fonte:
            self.texto(f'{pref}s', x + w - 130, y + 0.968 * tam - 0.968 * 8, 130, 9.75,
                       [[(fonte, 8, CINZA, False)]], alinhar='END')

    def barras(self, pref, x, y, w, linhas, passo=19, col_rotulo=84, col_valor=44, maximo=None, referencia=0):
        """Barras horizontais. linhas: [(rotulo, valor)]. A linha de indice `referencia` sai em cinza
        (use referencia=None para nenhuma)."""
        maximo = maximo or max(v for _, v in linhas)
        esp = round(passo - 9 * 1.219, 2)
        fmt = lambda v: f'{v:,}'.replace(',', '.')
        self.texto(f'{pref}L', x, y, col_rotulo, passo * len(linhas),
                   [[(r, 9, CINZA if i == referencia else TINTA, False)] for i, (r, _) in enumerate(linhas)], depois=esp)
        self.texto(f'{pref}V', x + w - col_valor, y, col_valor, passo * len(linhas),
                   [[(fmt(v), 9, CINZA if i == referencia else MARINHO, True)] for i, (_, v) in enumerate(linhas)],
                   alinhar='END', depois=esp)
        bx = x + col_rotulo + 2
        bw = w - col_rotulo - col_valor - 6
        for i, (_, v) in enumerate(linhas):
            self.forma(f'{pref}t{i}', 'RECTANGLE', bx, y + i * passo + 2, bw, 7, TRILHA)
            self.forma(f'{pref}b{i}', 'RECTANGLE', bx, y + i * passo + 2, bw * v / maximo, 7,
                       CINZA if i == referencia else AZUL)

    def tag_orador(self, pref, nome, url_microfone, largura_texto):
        """Etiqueta do orador no canto superior direito. largura_texto: largura do nome em 8 pt negrito."""
        w = int(largura_texto + 31.5) + 1
        x = MARGEM_D - w
        self.forma(f'{pref}_b', 'ROUND_RECTANGLE', x, 62.4, w, 18, BRANCO)
        self.R.append({'updateShapeProperties': {'objectId': f'{pref}_b', 'shapeProperties': {'contentAlignment': 'MIDDLE'},
                                                 'fields': 'contentAlignment'}})
        self.R.append({'insertText': {'objectId': f'{pref}_b', 'text': nome}})
        self.R.append({'updateTextStyle': {'objectId': f'{pref}_b', 'textRange': {'type': 'ALL'},
            'style': {'fontFamily': 'Montserrat', 'fontSize': {'magnitude': 8, 'unit': 'PT'},
                      'foregroundColor': {'opaqueColor': cor(TINTA)}, 'bold': True},
            'fields': 'fontFamily,fontSize,foregroundColor,bold'}})
        self.R.append({'updateParagraphStyle': {'objectId': f'{pref}_b', 'textRange': {'type': 'ALL'},
            'style': {'alignment': 'START', 'lineSpacing': 100, 'spaceAbove': {'magnitude': 0, 'unit': 'PT'},
                      'spaceBelow': {'magnitude': 0, 'unit': 'PT'}, 'indentStart': {'magnitude': 13.8, 'unit': 'PT'},
                      'indentFirstLine': {'magnitude': 13.8, 'unit': 'PT'}},
            'fields': 'alignment,lineSpacing,spaceAbove,spaceBelow,indentStart,indentFirstLine'}})
        self.imagem(f'{pref}_m', url_microfone, x + 7, 66.4, 10, 10)
        self.agrupar(pref, [f'{pref}_b', f'{pref}_m'])

    def rodape_capa(self, pref, esquerda, direita):
        """Faixa semitransparente na base da capa, com um texto a esquerda e outro a direita."""
        self.forma(f'{pref}_f', 'RECTANGLE', 0, 502, 960, 38, TINTA, alpha=0.55)
        self.texto(f'{pref}_e', 64, 514.9, 832, 13, [[(esquerda, 10, AZUL_PALIDO, True)]])
        self.texto(f'{pref}_d', 64, 514.9, 832, 13, [[(direita, 10, AZUL_PALIDO, True)]], alinhar='END')

    # ---------- envio ----------
    def lotes(self, n=60):
        """Divide os requests em lotes para enviar em sequencia (um batchUpdate por lote)."""
        return [self.R[i:i + n] for i in range(0, len(self.R), n)]

    def json(self, lote):
        return json.dumps(lote, ensure_ascii=False, separators=(',', ':'))
