# Zaparolli Tattoo · Thiago Zaparolli

Site do tatuador **Thiago “Zapa” Zaparolli** (@zaparollitattoo), dark art e realismo preto e cinza, estúdio privado em São José, SC. WhatsApp (48) 99810-0176.

Versão 1 (22/10/2026), no mesmo esquema do site do Fernando Fernandes, com a identidade puxada do Instagram dele:

- **Hero**: as costas de 5 dias (guest no Obscuro) em **meio-tom**, o pontilhado sépia dos 3 posts fixados, com uma fumaça lenta que engorda e afina os pontos, sem interação com o mouse. No desktop roda em WebGL (`assets/js/meio-tom.js`). Em celular, tablet e telas de toque toca um MP4 em loop do mesmo shader: `meio-tom-celular.mp4` em pé (720×1560) e `meio-tom-deitado.mp4` deitado (1280×590), 12 s. Por cima, a pilha "ZAPA BR / REALISMO BR…", o X com fio e o nome numa caixa de contorno, como o "AGENDAR" dos fixados.
- **Tipos**: Archivo expandida 900 com desgaste (a letra larga e grossa dos fixados), também nos chapéus de seção em caixa de contorno, e Oswald nos rótulos condensados. A fonte arranhada dos destaques saiu na v2 (22/10), a pedido.
- **Paleta**: carvão #0c0a09, fuligem #141110, osso #ece4d6 e sangue #cf3a24 só em detalhes. Fotos de apoio em sépia com grão, como os posts dele; o portfólio fica com a cor original.
- **Portfólio** em grade rígida 4:5 com filtros (dark art, realismo, fechamentos, coberturas) e tela cheia com gesto e botão "Quero algo assim" já com o nome da obra no WhatsApp. 70 obras.
- Seções: História (texto do próprio Thiago, enviado em 22/10, com frases em vermelho; ao lado, o reel fixado "Lápides e árvores secas" (DM8o1YERQQ5) narrado por ele, em `assets/video/historia.mp4` 576×1024, mudo em loop com botão para ouvir com som), Portfólio, Coberturas, Gente que cruza o mapa, Tattoo Week (só ela, sem a lista de prêmios), Estúdio, Como agendar + formulário de agendamento (vira mensagem pronta no WhatsApp) e Contato.

Páginas: `index.html`, `portfolio.html`, `404.html`.

## Fontes do conteúdo

Só o Instagram dele (extraído em 22/10/2026): bio, 674 legendas, fotos e os destaques ORÇAMENTOS e PRÉ/PÓS SESSÃO (lidos por captura). Nada de terceiros.

## Ferramentas

- `tools/processar.py` gera `assets/obras`, `assets/js/obras.js`, `assets/img`, a textura `desgaste.png`, favicons e `og.jpg` a partir de `../_ref/ig` (fora do repositório). Para trocar o portfólio, edite `PORTFOLIO` e rode `python tools/processar.py`.
- `tools/gerar_video.py` renderiza os MP4 do celular e o pôster a partir de `meio-tom.js` (Playwright + Brave + ffmpeg do imageio-ffmpeg). Rodar de novo se mexer no shader.

## CONFIRMAR antes do domínio

1. **Estúdio**: o texto (prédio comercial com vista para o mar, um cliente por dia, alvará sanitário) vem de um post de março/2022. Continua igual? O site não mostra endereço, só "privado, em São José; o endereço vai junto com o agendamento".
2. **Prêmios**: só a Tattoo Week aparece (pedido em 22/10). Os outros (Trifronteira, Barroso, Tattoo Citi, Expo Tattoo BC, Barravas) ficaram de fora. Ele faz só cobertura, nada de "reforma".
3. **Trajetória**: o texto dele fala em 12 anos; o site usa "12 anos".
4. **Relatos** (Califórnia, Nicole de Brusque, Natan): tirados das legendas. Os clientes topam aparecer pelo primeiro nome?
5. **Atendimento pela equipe** no WhatsApp: veio do destaque de orçamentos (antigo). Continua assim?
6. **Logo**: no destaque aparece um logo em script "Zaparolli Tattoo". Se ele mandar o arquivo vetorial, dá para usar no topo e no favicon (hoje é um "Z" na Archivo).
7. Domínio e remoção do `noindex`/`robots.txt` quando for ao ar.
