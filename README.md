# Zaparolli Tattoo · Thiago Zaparolli

Site do tatuador **Thiago “Zapa” Zaparolli** (@zaparollitattoo), dark art e realismo preto e cinza, estúdio privado em São José, SC. WhatsApp (48) 99810-0176.

Versão 1 (22/10/2026), no mesmo esquema do site do Fernando Fernandes, com a identidade puxada do Instagram dele:

- **Hero (v4, 22/10)**: a arte das costas como xerox chiado (`assets/js/xerox.js`, na linha do v1 do Samtto): cópia branca e cinza, cópia vermelha fora de registro, grão em saltos de 12 qps, varredura e cortes horizontais; MP4 `xerox-*` no toque. O meio-tom anterior continua em `meio-tom.js` e abre com `?hero=meiotom`. Antes: as costas de 5 dias (guest no Obscuro) em **meio-tom**, o pontilhado sépia dos 3 posts fixados, com uma fumaça lenta que engorda e afina os pontos, sem interação com o mouse. No desktop roda em WebGL (`assets/js/meio-tom.js`). Em celular, tablet e telas de toque toca um MP4 em loop do mesmo shader: `meio-tom-celular.mp4` em pé (720×1560) e `meio-tom-deitado.mp4` deitado (1280×590), 12 s. Por cima, a pilha "ZAPA BR / REALISMO BR…", o X com fio e o nome numa caixa de contorno, como o "AGENDAR" dos fixados.
- **Tipos**: Archivo expandida 900 com desgaste (a letra larga e grossa dos fixados), também nos chapéus de seção em caixa de contorno, e Oswald nos rótulos condensados. A fonte arranhada dos destaques saiu na v2 (22/10), a pedido.
- **Paleta** (pedido do cliente em 22/10): branco #f2f2f0, cinzas, preto #0b0b0b e vermelho #d42a1e. O meio-tom do hero tem pontos brancos e cinza na caveira e fumaça em pontos vermelhos; botões principais, filtros ativos e detalhes do hero em vermelho. Fotos de apoio em preto e cinza com grão. O portfólio fica com a cor original e sem contagens (pedido em 22/10).
- **Portfólio** em grade rígida 4:5 com filtros (dark art, realismo, fechamentos, coberturas) e tela cheia (sem numeração) com gesto e botão "Quero algo assim" já com o nome da obra no WhatsApp. 70 obras.
- Seções: A origem (antes "História"; texto do próprio Thiago, enviado em 22/10, com frases em vermelho; ao lado, o reel fixado "Lápides e árvores secas" (DM8o1YERQQ5) narrado por ele, em `assets/video/historia.mp4` 576×1024, mudo em loop com botão para ouvir com som), Processo criativo (texto dele; título + frase em duas colunas, 4 pilares em linha, texto em colunas e fecho), Portfólio, Coberturas ("o diferencial", com 4 coberturas e link para portfolio.html?f=cob), Gente que cruza o mapa, Tattoo Week (só ela, sem a lista de prêmios), Como agendar + formulário de agendamento (vira mensagem pronta no WhatsApp), Estúdio e Contato.

Páginas: `index.html`, `portfolio.html`, `404.html`.

## Fontes do conteúdo

Só o Instagram dele (extraído em 22/10/2026): bio, 674 legendas, fotos e os destaques ORÇAMENTOS e PRÉ/PÓS SESSÃO (lidos por captura). Nada de terceiros.

## Ferramentas

- `tools/processar.py` gera `assets/obras`, `assets/js/obras.js`, `assets/img`, a textura `desgaste.png`, favicons e `og.jpg` a partir de `../_ref/ig` (fora do repositório). Para trocar o portfólio, edite `PORTFOLIO` e rode `python tools/processar.py`.
- `tools/gerar_video.py` renderiza os MP4 do celular e o pôster a partir de `meio-tom.js` (Playwright + Brave + ffmpeg do imageio-ffmpeg). Rodar de novo se mexer no shader.

- `tools/gerar_og.py` gera o `og.jpg` (prévia do link no WhatsApp/Instagram) com o meio-tom do hero e a tipografia do site; precisa do servidor local `python -m http.server 8811` na pasta do projeto. As metatags usam a URL absoluta do Pages: trocar ao mudar de domínio.

## CONFIRMAR antes do domínio

1. **Estúdio**: o texto (prédio comercial com vista para o mar, um cliente por dia, alvará sanitário) vem de um post de março/2022. Continua igual? O site não mostra endereço, só "privado, em São José; o endereço vai junto com o agendamento".
2. **Prêmios**: nos números da História aparece "15 prêmios em convenções, nos estilos realismo, dark art e cobertura" (informado pelo cliente em 22/10). Fora isso, só a Tattoo Week tem destaque. Ele faz só cobertura, nada de "reforma".
3. **Trajetória**: o texto dele fala em 12 anos; o site usa "12 anos".
4. **Relatos** (Califórnia, Nicole de Brusque, Natan): tirados das legendas. Os clientes topam aparecer pelo primeiro nome?
5. **Atendimento pela equipe** no WhatsApp: veio do destaque de orçamentos (antigo). Continua assim?
6. **Logo**: no destaque aparece um logo em script "Zaparolli Tattoo". Se ele mandar o arquivo vetorial, dá para usar no topo e no favicon (hoje é um "Z" na Archivo).
7. Domínio e remoção do `noindex`/`robots.txt` quando for ao ar.
