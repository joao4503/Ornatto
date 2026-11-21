# Tabela de preços · Cafés Ornatto

- `tabela-precos.html`: arquivo-fonte (edite textos, preços e cores aqui; as cores ficam em `:root`).
- `gerar-pdf.js`: gera `output/TabelaPrecos_Ornatto.pdf` (A4) e a prévia `output/TabelaPrecos_Ornatto.png`.
- `assets/`: logos oficiais em vetor (`logo-ornatto-color.svg` no cabeçalho, `logo-ornatto-verde.svg` para fundos claros) e QR code do Instagram.
- `fonts/`: DM Serif Display, Source Serif 4, Instrument Sans e Oswald (licença SIL OFL).

## Gerar o PDF

```
npm i playwright   # se ainda não tiver
node gerar-pdf.js
```

A prévia PNG precisa do `pdftoppm` (poppler-utils). O script avisa se o conteúdo passar de uma página.

Barra de pontuação SCA: `width = (pontos − 80) × 10 %` (escala de 80 a 90).
