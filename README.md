# slides-modelo-infnet

Skill para colocar apresentações do Google Slides no modelo visual da Faculdade Infnet.
Trata só de design e layout (grade, cores, tipografia, componentes, capa e encerramento), não do conteúdo dos slides.

## Estrutura

```
skill/                 texto do skill
  SKILL.md             instruções (é o que vai para o Claude)
  scripts/
    slides_modelo.py   gera os requests da API do Slides (cartões, faixas, tags, barras…)
    medir_texto.py     mede e quebra textos em Montserrat
assets/                binários usados pelos slides
  fundo-capa.jpg
  logo-faculdade-infnet-branco.png
  onda-claro.png
  onda-escuro.png
  icone-microfone.png
  icone-documento.png
```

Os binários ficam separados do texto do skill: o `SKILL.md` aponta para eles pelo endereço deste repositório.

## Observações

- A API do Slides insere imagens pelo endereço, que precisa abrir sem login. Com o repositório privado, o skill continua valendo como guia, mas as imagens só entram duplicando um slide que já as tenha.
- Os ícones vêm do conjunto Material Icons, do Google (licença Apache 2.0).
- A fonte Montserrat não está aqui: o Slides já a oferece, e o medidor de texto a baixa pelo npm (`@fontsource/montserrat`, licença OFL).
