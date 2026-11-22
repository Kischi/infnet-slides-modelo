---
name: slides-modelo-infnet
description: Coloca apresentações do Google Slides no modelo visual da Faculdade Infnet (grade, cores, tipografia, cartões, faixas, tags, capa e encerramento). Use ao pedirem para padronizar, redesenhar ou criar slides "no modelo", "no padrão visual" ou "com o layout da apresentação do reconhecimento". Trata só de design e layout, não do conteúdo.
---

# Slides no modelo visual da Faculdade Infnet

Este skill descreve **como os slides devem parecer** e **como montá-los pela API do Google Slides**. Ele não diz o que escrever: textos, números e nomes vêm do usuário ou da apresentação de origem.

## Regras de trabalho

1. **Não mexa no conteúdo.** Ao redesenhar, mantenha textos, números e nomes como estão. Se o novo layout exigir cortar, fundir ou reescrever algo, diga exatamente o que mudou. Dado novo só entra com fonte.
2. **Um slide-piloto antes de replicar.** Quando o pedido vale para vários slides (um tag, um rodapé, um novo tipo de cartão), faça em um, mostre a imagem e só replique depois do aceite.
3. **Confira pela miniatura.** Depois de cada alteração, leia a miniatura do slide (tamanho LARGE) e olhe o resultado. Coordenadas certas no papel não garantem quebra de linha certa.
4. **Releia a ordem dos slides antes de agir por número.** O usuário reordena o deck; "slide 17" só vale depois de ler a lista atual de páginas.
5. **Fundo claro para conteúdo.** Fundo escuro fica só na capa e no encerramento.
6. Envie os requests em lotes de até 60 por chamada, na ordem.

## Fundamentos

- **Página:** 960 × 540 pt (12.192.000 × 6.858.000 EMU). 1 pt = 12.700 EMU.
- **Fonte:** Montserrat em tudo. Negrito = peso 700; seminegrito = 600 (`weightedFontFamily`).
- **Fundo dos slides de conteúdo:** `F4F5FA`.
- **Margens:** conteúdo entre x = 64 e x = 896 (largura útil 832).
- **Faixas verticais:** kicker em y = 64; título em y = 86,4; corpo de y = 133,27 a y = 511,27 (altura 378).
- **Calha:** 16 pt entre colunas e entre linhas de cartões.

| Grade | Largura da coluna | x das colunas |
|---|---|---|
| 4 colunas | 196 | 64 · 276 · 488 · 700 |
| 3 colunas | 266,67 | 64 · 346,66 · 629,33 |
| 2 colunas | 408 | 64 · 488 |
| 2/3 + 1/3 | 549,34 + 266,67 | 64 · 629,33 |

Dentro de um cartão o texto começa 16 pt para dentro (largura de texto = largura do cartão − 32) e 18 a 19 pt abaixo do topo.

## Paleta

| Uso | Hex |
|---|---|
| Azul-marinho: títulos, faixas, cartão em destaque | `1C3665` |
| Azul: kicker, números, barra dos cartões, links | `106DB6` |
| Azul-claro: barra secundária, terceiro tom de gráficos | `689CCB` |
| Azul-pálido: texto secundário sobre escuro, ladrilho de ícone | `D4EAFF` |
| Amarelo: destaque pontual (barra sobre marinho, faixa de chamada) | `FFCC2E` |
| Amarelo da capa: barrinha e nomes na capa e no encerramento | `FEDA0C` |
| Fundo claro | `F4F5FA` |
| Fundo escuro (capa e encerramento) | `14305C` |
| Branco: cartões e tags | `FFFFFF` |
| Tinta: texto corrido | `0E1A31` |
| Cinza: fontes, legendas, linhas neutras | `5A6B86` |
| Trilha: divisórias, fundo de barras, linhas de tabela | `E9EEF6` |
| Pílula | fundo `E2EEF9`, texto `106DB6` |
| Barra neutra (linha sem destaque) | `B8C2D1` |

Use o amarelo com parcimônia: no máximo um elemento por slide.

## Tipografia

Há duas densidades. Escolha uma por slide e não misture.

| Papel | Normal | Denso |
|---|---|---|
| Kicker (caixa alta) | 12 negrito `106DB6` | igual |
| Título do slide (caixa alta) | 24 negrito `1C3665`, entrelinha 112 | igual |
| Título de cartão | 15 a 18 negrito `1C3665` | 10,5 negrito `106DB6` |
| Texto de cartão | 12 a 14 `0E1A31`, entrelinha 138 | 9 a 9,5 `0E1A31`, entrelinha 115 |
| Número em destaque | 28 negrito `106DB6` (36 para um número-herói) | 22 negrito `106DB6` |
| Fonte do dado | 12 `5A6B86` | 8 `5A6B86` |
| Rótulo pequeno (cabeçalho de coluna, eixo) | 10 negrito `106DB6` | 8 negrito `5A6B86` |

Use o denso só quando o slide tiver nove ou mais informações. Não desça abaixo de 7,5 pt.

## Cabeçalho de todo slide de conteúdo

- **Onda decorativa:** imagem `onda-claro.png` em x = 460, y = 0, 500 × 75, atrás de tudo.
- **Kicker:** caixa em (64, 64), 857 × 16,4; nome da seção em caixa alta.
- **Título:** caixa em (64, 86,4), 857 × 28,9; uma linha, caixa alta.
- **Tag do orador (opcional):** etiqueta branca de 18 pt de altura, encostada em x = 896, y = 62,4. Ícone de microfone 10 × 10 a 7 pt da borda esquerda e 4 pt do topo; nome em 8 negrito `0E1A31`, caixa alta, com recuo de parágrafo de 13,8 pt. Largura = largura do nome + 31,5. Agrupe etiqueta e ícone.

Para criar um slide novo em um deck que já está no modelo, **duplique um slide de conteúdo existente** (`duplicateObject` com mapa de IDs), apague o que não serve e troque kicker e título com `replaceAllText` limitado à página. Isso preserva a onda e o espaçamento entre letras do kicker, que a API não consegue criar.

## Componentes

**Cartão.** Retângulo branco com raio de 7 pt e barra de 3 pt no topo (`106DB6`; `689CCB` para cartões secundários). Monte em tiras para o raio não variar com o tamanho:
1. barra: `ROUND_RECTANGLE` em (x + 0,5, y), largura − 1, altura 42, na cor da barra;
2. topo: `ROUND_RECTANGLE` branco em (x, y + 3), altura 42;
3. base: `ROUND_RECTANGLE` branco em (x, y + altura − 42), altura 42;
4. miolo: `RECTANGLE` branco em (x, y + 15), altura = altura − 27;
5. agrupe os quatro.

**Cartão em destaque.** Mesmo formato com fundo `1C3665`, título `F4F5FA` e texto `D4EAFF`. No máximo um por slide.

**Faixa.** Retângulo arredondado `1C3665` de largura total (64 a 896) encostado em y = 511,27, com 46 a 65 pt de altura. Texto de 9,5 a 12 pt em `F4F5FA`, trecho-chave em branco negrito, fonte em `D4EAFF`. Com duas mensagens, divida ao meio com um fio vertical `2A4780`. Variante de chamada: fundo `FFCC2E`, texto `1C3665`, número em 34 negrito.

**Bloco de dado.** Número em destaque, legenda logo abaixo e fonte em cinza. No modo denso a fonte fica à direita, na linha de base do número. Entre blocos empilhados, fio de 0,75 pt em `E9EEF6`.

**Barras horizontais.** Rótulo à esquerda (9 pt), trilha `E9EEF6` de 7 pt de altura, barra `106DB6` proporcional e valor à direita em 9 negrito `1C3665`. Passo de 19 pt entre linhas. Valor de referência (média, meta) em cinza `5A6B86`.

**Barra segmentada.** Altura 10, segmentos proporcionais com 3 pt de vão, nas cores `1C3665`, `106DB6`, `689CCB`. Legendas abaixo: a primeira alinhada à esquerda, as do meio centralizadas no segmento, a última alinhada à direita.

**Tabela.** Sem bordas verticais nem externas; só fios horizontais de 1 pt em `E9EEF6`. Cabeçalho com fundo `F4F5FA`, 9,5 negrito `5A6B86`, 28 pt de altura. Linhas de 44 pt, conteúdo centralizado na vertical, primeira coluna em 11,5 peso 600 e as demais em 11,5 peso 400. Marcações dentro da célula em 9,5 negrito `106DB6`.

**Linha de agenda.** Cartão de 408 × 46 com passo vertical de 53. Fio vertical de 3,5 × 24 a 12 pt da esquerda; hora em 14 negrito com "até…" em 8,5 logo abaixo; título em 11,5 negrito com subtítulo em 9. Pílula opcional à direita (60 × 17, texto 7 negrito). Três estados: normal (branco, fio `106DB6`, texto `1C3665`), destaque (fundo `1C3665`, fio `FFCC2E`, texto branco) e neutro (sem fundo, fio `B8C2D1`, texto `5A6B86` sem negrito). Cabeçalho de coluna em 10 negrito `106DB6`, em y = 128.

**Cartão com rodapé azul.** Em grade de 4 colunas, 140 a 150 pt de altura: destaque no topo (nome em negrito, ou ano em 20 negrito `106DB6`), texto em 12 com entrelinha 138 e uma tira `106DB6` na base com texto pequeno ou ícones em branco.

**Cartão com ícone.** Ícone de 20 × 20 à esquerda do título (título deslocado 28 pt), texto abaixo ocupando a largura toda.

**Cartão de mensagem única.** Um cartão ocupando o corpo inteiro, com o conteúdo centralizado: ladrilho `D4EAFF` de 64 × 64 com ícone de 36, chamada em 11 negrito `106DB6` caixa alta, frase principal em 30 negrito `106DB6` e uma linha de apoio em 14 `0E1A31`.

## Capa e encerramento

Fundo da página `14305C`, com `fundo-capa.jpg` cobrindo a página inteira (0, 0, 960 × 540).

- **Logo:** `logo-faculdade-infnet-branco.png` em (0, 27), 350 × 100.
- **Barrinha:** retângulo arredondado `FEDA0C` em (64, 122), 48 × 4.
- **Capa:** saudação em 20 `D4EAFF` (nomes em negrito `FEDA0C`) em y = 134,9; título em 48 negrito `F4F5FA`, entrelinha 92, em y = 166,3; linha de apoio em 16 `F4F5FA` em y = 277,3.
- **Rodapé da capa:** faixa `0E1A31` com alfa 0,55 em (0, 502), 960 × 38. Dentro, textos em 10 negrito `D4EAFF`: um alinhado à esquerda em x = 64 e outro alinhado à direita em x = 896, ambos em y = 514,9.
- **Encerramento:** frase em 48 negrito `F4F5FA` em y = 140; linha de apoio em 15 em y = 206,8; endereço em 12 negrito `689CCB` em y = 235,8.

A capa leva pouco texto: saudação, título e uma linha. O resto vai para o rodapé.

**Slide de conteúdo escuro (só se o usuário pedir).** Fundo `14305C`, `onda-escuro.png` no cabeçalho, título em `F4F5FA`, painéis `1C3665` com barra `689CCB`, trilhas de gráfico em `2A4780`, texto em `F4F5FA` e `D4EAFF`.

## Binários

Os arquivos ficam em `https://raw.githubusercontent.com/Kischi/infnet-slides-modelo/main/assets/`:

| Arquivo | Uso | Tamanho no slide |
|---|---|---|
| `fundo-capa.jpg` | fundo da capa e do encerramento | 960 × 540 em (0, 0) |
| `logo-faculdade-infnet-branco.png` | logo sobre fundo escuro | 350 × 100 em (0, 27) |
| `onda-claro.png` | onda do cabeçalho, slides claros | 500 × 75 em (460, 0) |
| `onda-escuro.png` | onda do cabeçalho, slides escuros | 500 × 75 em (460, 0) |
| `icone-microfone.png` | tag do orador | 10 × 10 |
| `icone-documento.png` | cartão de mensagem única | 36 × 36 |

O `createImage` do Slides baixa a imagem pelo endereço, então o endereço precisa abrir sem login. Se o repositório estiver privado, as imagens não entram: nesse caso duplique um slide que já as tenha. Os ícones só existem em preto; por isso o texto ao lado usa a tinta `0E1A31`.

## Receitas da API do Slides

- **Formas lidas de volta têm base de 3.000.000 EMU.** Para mover ou redimensionar uma forma existente com `updatePageElementTransform` em modo `ABSOLUTE`, use `scaleX = largura_pt × 12700 / 3000000` (idem para a altura) e `translate` em EMU. Passar escala 1 deixa a forma com 236 pt.
- **Formas novas:** crie com `size` em PT e escala 1.
- **Caixa de texto criada pela API tem recuo de 7,2 pt** em cada lado. Para o texto começar em (x, y) com largura w, crie a caixa em (x − 7,2, y − 7,2) com largura w + 14,4. As caixas que vieram do arquivo original têm recuo zero.
- **IDs de objeto** precisam de 5 a 50 caracteres.
- **Contorno:** toda forma nova nasce com contorno; desligue com `outline.propertyState = NOT_RENDERED`.
- **`ROUND_RECTANGLE` novo** tem raio igual a um sexto do lado menor. Daí a montagem em tiras de 42 pt (raio 7).
- **Transparência:** `shapeBackgroundFill.solidFill.alpha`, incluído em `fields`.
- **Ordem:** objeto novo nasce na frente. Para pôr um fundo atrás de textos que já existem, use `updatePageElementsZOrder` com `SEND_TO_BACK` (ou `BRING_TO_FRONT` nos textos).
- **`duplicateObject`** copia dentro da mesma página, ou a página inteira. Não leva um elemento para outro slide.
- **Texto com vários estilos:** insira o texto todo e aplique `updateTextStyle` por intervalo (`FIXED_RANGE`). `replaceAllText` aceita `\u000b` para quebra de linha sem novo parágrafo e texto vazio para apagar um trecho.
- **Espaço:** use espaço comum. Espaço não separável (NBSP) em Montserrat altera o espaçamento visível.
- **Tabelas:** `updateTableColumnProperties` (largura), `updateTableRowProperties` (`minRowHeight`), `updateTableBorderProperties` (pinte `ALL` de branco e depois `INNER_HORIZONTAL` de `E9EEF6`), `updateTableCellProperties` (fundo e `contentAlignment`). Estilo de texto é por célula, com `cellLocation`. Tabela se move com escala 1.
- **Link:** `updateTextStyle` com `link.url`; reaplique cor e negrito depois, porque o link troca o estilo.
- **Notas do orador:** `deleteText` no corpo das notas apaga tudo. Slide duplicado herda as notas do original.
- **Miniatura:** leia com tamanho LARGE (1600 px); 1 pt = 1,667 px.

## Medir o texto antes de posicionar

Quebra de linha decide o layout. Meça com as fontes reais:

```bash
npm pack @fontsource/montserrat && tar xzf fontsource-montserrat-*.tgz
pip install fonttools brotli --break-system-packages
```

```python
from fontTools.ttLib import TTFont
F = {p: TTFont(f'package/files/montserrat-latin-{p}-normal.woff2') for p in (400, 700)}
def largura(texto, tamanho, peso=400):
    f = F[peso]; cmap = f.getBestCmap(); hm = f['hmtx']
    return sum(hm[cmap.get(ord(c), '.notdef')][0] for c in texto) * tamanho / f['head'].unitsPerEm
```

- Altura de linha = 1,219 × tamanho × entrelinha. Linha de base a 0,968 × tamanho do topo da linha.
- Para alinhar um texto pequeno à linha de base de um número grande: topo do pequeno = topo do número + 0,968 × (tamanho do número − tamanho do pequeno).
- Deixe 2% de folga na largura. Linha órfã de uma palavra se resolve com quebra manual ou meio ponto a menos.

## Código de apoio

O repositório traz em `skill/scripts/` uma biblioteca que gera os requests (`slides_modelo.py`: cartão em tiras, caixa de texto com recuo compensado, bloco de dado, barras, faixa, tag do orador, rodapé da capa, divisão em lotes) e o medidor de texto (`medir_texto.py`). Endereço: `https://raw.githubusercontent.com/Kischi/infnet-slides-modelo/main/skill/scripts/`. Se não houver acesso ao repositório, as medidas e receitas acima bastam para montar tudo à mão.

## Passo a passo para pôr uma apresentação no modelo

1. Leia a apresentação: páginas na ordem, textos, imagens e posições. Liste os slides com o tipo de conteúdo de cada um.
2. Escolha, para cada slide, o componente que serve ao conteúdo: comparação de itens → cartões em grade; números → blocos de dado ou barras; lista de pessoas ou marcos → cartões com rodapé azul; horários → linhas de agenda; lista nominal → tabela; um recado só → cartão de mensagem única. Um slide, uma ideia.
3. Planeje no papel: grade, alturas, tamanhos. Meça os textos e ajuste até caber sem órfãs.
4. Monte o slide-piloto, leia a miniatura e mostre ao usuário.
5. Replique nos demais, conferindo cada um.
6. Ao final, informe o que mudou de layout e, em separado, qualquer texto que precisou ser alterado.

## Conferência final de cada slide

- Tudo dentro de x = 64 a 896 e y = 133,27 a 511,27 (fora o cabeçalho).
- Cartões da mesma linha com a mesma altura; calhas de 16 pt.
- Um tamanho por papel de texto; nenhuma mistura de densidades.
- Corpo ocupado até embaixo ou fechado por uma faixa; sem metade vazia.
- Nenhuma palavra órfã, texto cortado ou sobreposição na miniatura.
- Todo dado com sua fonte.
