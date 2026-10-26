"""Gera coberturas.html (página só de coberturas, aprovada em 24/10) com o cabeçalho, o rodapé
e a tela cheia da página do portfólio. O comparador e o texto vêm da seção de coberturas da home.
Uso: python tools/gerar_coberturas.py"""
import os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)

# (arquivo em assets/img/cob, descrição, o que havia antes)
TRABALHOS = [
    ('mascara-gas', 'Máscara de gás', 'desenho antigo no ombro'),
    ('espartano-corvo', 'Espartano e corvo', 'dragão colorido nas costas'),
    ('noiva-cadaver', 'Noiva Cadáver e casa assombrada', 'braço de anime'),
    ('vampira', 'Vampira com vela', 'gato no antebraço'),
    ('viking', 'Viking de tapa-olho', 'braço fechado escuro'),
    ('corvo', 'Corvo sob a lua', 'corvo antigo sem contraste'),
]

ZAP_COB = 'https://wa.me/5548998100176?text=Ol%C3%A1%2C%20Zapa!%20Vim%20pelo%20site%20e%20tenho%20uma%20tattoo%20que%20quero%20cobrir.%20Vou%20mandar%20a%20foto%20e%20as%20medidas.'


def main():
    home = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()
    sec = home[home.index('<!-- COBERTURAS -->'):home.index('<!-- QUEM VIAJA -->')]
    texto = sec[sec.index('<blockquote class="citacao">'):sec.index('<a class="btn claro"')].strip()
    comparador = sec[sec.index('<figure class="antes-depois'):sec.index('</figure>') + len('</figure>')]
    comparador = comparador.replace('loading="lazy" ', '')

    grade = ''.join(f'''        <li class="surge"><figure><img src="assets/img/cob/{n}-640.webp" srcset="assets/img/cob/{n}-640.webp 640w, assets/img/cob/{n}-1080.webp 1080w" sizes="(max-width: 860px) 92vw, 620px" alt="{t}, cobrindo {a}" loading="lazy" decoding="async" width="640" height="640"><span class="rot-a" aria-hidden="true">Antes</span><span class="rot-d" aria-hidden="true">Depois</span></figure><p class="cob-leg"><b>{t}</b> sobre {a}</p></li>
''' for n, t, a in TRABALHOS)

    corpo = f'''<main>
  <section class="secao pontos pagina-topo" id="coberturas">
    <div class="wrap">
      <div class="cobertura">
        <div class="texto surge">
          <p class="chapeu">A arte de transformar</p>
          <h1 class="titulo"><span class="desgaste">Coberturas&nbsp;| Cover-up</span></h1>
          {texto}
          <a class="btn claro" href="{ZAP_COB}" target="_blank" rel="noopener">Mandar foto da tattoo antiga<span class="seta" aria-hidden="true">→</span></a>
        </div>
        {comparador}
      </div>
    </div>
  </section>

  <section class="secao cob-etapas">
    <div class="wrap">
      <p class="chapeu surge">Como funciona</p>
      <h2 class="titulo surge"><span class="desgaste">Da tattoo antiga à nova arte</span></h2>
      <ol class="passos">
        <li class="surge"><span class="n">1</span><h3>Avaliação</h3><p>Você manda fotos da tatuagem antiga, com boa luz, e as medidas aproximadas. Cada caso é avaliado pela pigmentação, pela pele e pelo que é possível cobrir de verdade.</p></li>
        <li class="surge"><span class="n">2</span><h3>Projeto</h3><p>A nova arte é desenhada em cima da antiga, usando contraste, profundidade e composição para que ela desapareça dentro do desenho novo.</p></li>
        <li class="surge"><span class="n">3</span><h3>Primeira sessão</h3><p>Cria a base e neutraliza o trabalho antigo.</p></li>
        <li class="surge"><span class="n">4</span><h3>Cicatrização e reforço</h3><p>Depois de cicatrizar, uma nova camada reforça a cobertura, constrói contraste e volume e fecha os detalhes.</p></li>
      </ol>
    </div>
  </section>

  <section class="secao pontos" id="trabalhos">
    <div class="wrap">
      <div class="cab">
        <p class="chapeu surge">Antes e depois</p>
        <h2 class="titulo surge"><span class="desgaste">Coberturas feitas pelo Zapa</span></h2>
        <p class="olho surge">Toque numa foto para ver em tela cheia.</p>
      </div>
      <ul class="coberturas-grade coberturas-pagina">
{grade}      </ul>
    </div>
  </section>

  <section class="secao" style="padding-top: 0;">
    <div class="wrap">
      <div class="chamada surge" style="max-width: 760px; margin: 0 auto; text-align: center;">
        <span class="xis" aria-hidden="true"></span>
        <p class="grande">Tem uma tattoo que não te representa mais?</p>
        <p>Mande fotos da tatuagem antiga e as medidas aproximadas. A avaliação começa pela conversa.</p>
        <div class="hero-acoes" style="justify-content: center; margin: 18px auto 0;">
          <a class="btn claro" href="{ZAP_COB}" target="_blank" rel="noopener">Avaliar minha cobertura<span class="seta" aria-hidden="true">→</span></a>
          <a class="btn" href="index.html#agendar">Agendar orçamento<span class="seta" aria-hidden="true">→</span></a>
        </div>
      </div>
    </div>
  </section>
</main>'''

    base = open(os.path.join(SITE, 'portfolio.html'), encoding='utf-8').read()
    cab = base[:base.index('<main>')]
    pe = base[base.index('</main>') + len('</main>'):]
    cab = re.sub(r'<title>.*?</title>', '<title>Coberturas · Zaparolli Tattoo · Cover-up em dark art e preto e cinza</title>', cab)
    cab = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Coberturas (cover-up) de Thiago Zaparolli em São José, SC: tatuagens antigas transformadas em dark art e preto e cinza. Avaliação pelo WhatsApp.">', cab)
    cab = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Coberturas · Zaparolli Tattoo">', cab)
    cab = cab.replace('portfolio.html">', 'coberturas.html">')
    pe = pe.replace('<script src="assets/js/obras.js"></script>\n', '')
    open(os.path.join(SITE, 'coberturas.html'), 'w', encoding='utf-8').write(cab + corpo + pe)
    print('coberturas.html')


if __name__ == '__main__':
    main()
