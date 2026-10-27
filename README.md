# Zaparolli Tattoo · Thiago Zaparolli

Site do tatuador **Thiago “Zapa” Zaparolli** (@zaparollitattoo), dark art e realismo preto e cinza, estúdio privado em São José, SC. WhatsApp (48) 99810-0176.

Domínio: **https://thiagozaparolli.com.br/** (metatags, canonical, JSON-LD, sitemap e robots já apontam para ele; indexação liberada). Enquanto o DNS não estiver pronto, o site segue em https://azeugral.github.io/zaparolli-tattoo/. Estado em 27/10/2026:

- **Topo**: fiel ao mockup do cliente (aprovado em 23/10). Arte das costas (foto em alta `IMG_6314`) parada ao fundo em preto, cinza quente e creme, bordas suavizadas por máscara, fumaça realista e escura subindo pelo lado esquerdo (ver Fumaça abaixo). Nome = logo oficial enviado pelo cliente (original em `../_ref/logo-cliente/logo-original.png`, versões web `assets/img/logo-zaparolli*.webp`), também no rodapé e na prévia do link. Coluna lateral com duas cruzes finas, lema com "autênticas." em vermelho, tags com ✕, botões creme e contorno com seta, linha com estúdio e 12 anos. Cabe exatamente em 100svh no PC e no celular.
- **Fumaça** (26/10): shader de ruído torcido em `assets/js/fumaca.js`, na versão suave (pouca torção, fios apagados, sobe devagar): véus cinza quente, luz cor de osso e brasa vermelha bem leve embaixo, somados com `mix-blend-mode: screen`. Hero: lado esquerdo, força 1.6, ciclo de 40 s. Como agendar: rente às laterais, força .8, ciclo de 64 s; no celular fica na última tela da seção, atrás da ficha. Desktop roda ao vivo em WebGL (meia resolução, baixa sozinho se pesar); telas de toque tocam os MP4 `assets/video/fumaca-*.mp4`, gerados por `python tools/gerar_fumaca.py` (rodar de novo se mexer no shader ou nos `data-forca`/`data-ciclo`). No celular (tela menor que 600 px, toque) o hero usa fumaça PRETA: `fumaca-hero-celular-preta.mp4` (modo 2 do shader, no alto por cima da arte, invertido pelo `gerar_fumaca.py`) somado com `mix-blend-mode: multiply` (classe `.fumaca--preta`); o Como agendar continua com a fumaça clara. Uma versão de partículas volumétricas foi testada e reprovada; a primeira versão, mais forte, foi achada "líquida demais".
- **Paleta**: creme #ece4d6, carvão #0c0b0a, vermelho #cc2a1f. Nada de pontilhado ou grão em fundos e fotos.
- **Tipos**: Archivo expandida 900 nos títulos, com a máscara de desgaste `titulo-desgaste.webp` (textura de concreto gerada por IA), e Oswald nos rótulos. Fontes hospedadas no próprio site.
- **Ornamentos** dark art (galho com corvo, lua, galhos pendurados, cruz com corvo), um por seção, estáticos, gerados por IA (`tools/gerar_ornamentos.py`, originais em `../_ref/ornamentos`).
- **Portfólio** em grade 4:5 com filtros (dark art, coberturas, realismo, fechamentos), legenda só com o estilo e tela cheia com "Quero algo assim" já com o nome da obra no WhatsApp. 47 obras (29 dark art, 7 coberturas, 6 realismo, 5 fechamentos). Toda imagem do site abre em tela cheia.
- **Seções da home**: A origem (texto do Thiago e o reel narrado "Lápides e árvores secas" em `assets/video/historia.mp4`), Processo criativo, Portfólio, faixa de agendamento, Coberturas (comparador antes e depois do médico da peste), Gente que cruza o mapa (feedback: em destaque os reels do Lucas, DbmGxAmqpXN, e do Carlos, DW2OT6QkaPX, em `assets/video/feedback-*.mp4` 540×960, mudos em loop com botão de som, um com som por vez; originais em `../_ref/reels-feedback`; abaixo, os 3 relatos escritos em cartões menores), Tattoo Week (jurado em 2025), Como agendar + formulário que vira mensagem pronta no WhatsApp, Estúdio (texto e fotos do Zapa) e Contato.

Páginas: `index.html`, `portfolio.html`, `coberturas.html`, `privacidade.html`, `termos.html` e `404.html` (com `<base>` calculado: funciona no Pages e no domínio próprio).

Histórico do topo: v1–v5 tiveram meio-tom e xerox em shader (reprovados; código em `../_ref/aposentado`), v6 a arte com zoom lento (zoom reprovado) e v7 o layout atual do mockup. Detalhes de cada rodada estão no histórico do git.

## Fontes do conteúdo

Só o Instagram dele (extraído em 22/10/2026): bio, 674 legendas, fotos e os destaques ORÇAMENTOS e PRÉ/PÓS SESSÃO (lidos por captura). Nada de terceiros.

## Ferramentas

- `tools/processar.py` gera `assets/obras`, `assets/js/obras.js`, `assets/img`, a textura `desgaste.png` e os favicons a partir de `../_ref/ig` (fora do repositório). Para trocar o portfólio, edite `PORTFOLIO` e rode `python tools/processar.py`.
- `tools/gerar_ornamentos.py` tira o fundo preto das ilustrações de `../_ref/ornamentos` e gera `assets/img/orn/*.webp`.
- `tools/gerar_coberturas.py` e `tools/gerar_legais.py` geram `coberturas.html`, `privacidade.html` e `termos.html` a partir do cabeçalho da home.
- O antigo `gerar_video.py` (vídeos do meio-tom) está aposentado em `../_ref/aposentado`.

- `tools/gerar_og.py` gera o `og.jpg` (prévia do link no WhatsApp/Instagram) com a arte do topo, o logo oficial e a tipografia do site; precisa do servidor local `python -m http.server 8811` na pasta do projeto. As metatags usam a URL absoluta do domínio (https://thiagozaparolli.com.br/).

## Fotos em alta e jurídico (24/10)

- Fotos em alta enviadas pelo cliente em `../_ref/hq-cliente`: trocam as do Instagram no portfólio e no topo (`HQ` em `tools/processar.py`, casadas por ORB com `../_ref/casar.py`) e entram 3 obras novas (`NOVAS`). As 5 coberturas também foram trocadas pelas versões em alta (as antigas ficaram em `../_ref/coberturas-cliente/baixa`).
- `privacidade.html` e `termos.html` são gerados por `tools/gerar_legais.py` (textos e data de vigência lá dentro). Aviso de cookies em `assets/js/zaparolli.js` (chave `zap-consent` no localStorage).
- Fontes hospedadas no próprio site (`assets/fontes`, `assets/css/fontes.css`): nenhuma requisição a terceiros ao abrir as páginas.

## Reorganização e otimização (24/10)

- Home: faixa de agendamento depois do portfólio (a faixa corrida e a de autoridade abaixo do topo saíram a pedido em 24/10). JSON-LD de TattooParlor completo.
- `coberturas.html` (gerada por `tools/gerar_coberturas.py`): comparador, passo a passo da cobertura e os 6 antes e depois; o menu e o botão da home levam a ela.
- Otimização: fontes no próprio site, vídeo da História 20% menor (540×960), shaders e vídeos do meio-tom e do xerox aposentados em `../_ref/aposentado` (−10 MB no repositório). `sitemap.xml` e `robots.txt` no domínio; CSS/JS com `?v=N` (subir o N a cada mudança); máscara dos títulos só com alfa (−45%) e fumaça preta do celular em 1,3 MB.

## CONFIRMAR antes do domínio

0. **Jurídico**: o Zapa tem CNPJ ou atende como pessoa física? Tem e-mail para pedidos de dados (LGPD)? Política de atendimento a menores? Com isso os textos de privacidade e termos ficam completos. Vale uma revisão de advogado antes de ir ao domínio.

1. **Estúdio**: resolvido em 26/10 (fotos e texto do próprio Zapa).
2. **Prêmios**: nos números da História aparece "15 prêmios em convenções, nos estilos realismo, dark art e cobertura" (informado pelo cliente em 22/10). Fora isso, só a Tattoo Week tem destaque. Ele faz só cobertura, nada de "reforma".
3. **Trajetória**: o texto dele fala em 12 anos; o site usa "12 anos".
4. **Relatos** (Califórnia, Nicole de Brusque, Natan): tirados das legendas. Os clientes topam aparecer pelo primeiro nome?
5. **Atendimento pela equipe** no WhatsApp: veio do destaque de orçamentos (antigo). Continua assim?
6. **Logo**: no destaque aparece um logo em script "Zaparolli Tattoo". Se ele mandar o arquivo vetorial, dá para usar no topo e no favicon (hoje é um "Z" na Archivo).
7. Domínio: repositório pronto. Falta o DNS no registro.br (A para 185.199.108.153, .109, .110 e .111; CNAME `www` para `azeugral.github.io`) e depois ligar o domínio nas configurações do Pages com HTTPS.
