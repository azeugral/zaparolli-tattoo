"""Gera og.jpg (1200x630), a imagem que aparece quando o link é compartilhado.
Monta uma página com o meio-tom do hero (assets/js/meio-tom.js) e a tipografia do site
e fotografa com Playwright + Brave. Precisa de um servidor local na pasta do projeto:
    python -m http.server 8811   (rodado em PROJETOS LRGZ/Zaparolli Tattoo)
Uso: python tools/gerar_og.py"""
import os
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
BRAVE = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
BASE = 'http://localhost:8811/site/'

HTML = """<!doctype html><html><head><meta charset="utf-8">
<base href="%s">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Oswald:wght@500&display=swap">
<style>
:root { --carvao:#0c0a09; --osso:#ece4d6; --cinza:#a39888; --sangue:#cf3a24; }
* { box-sizing:border-box; margin:0; }
body { width:1200px; height:630px; background:var(--carvao); overflow:hidden; position:relative; font-family:'Archivo'; }
canvas { position:absolute; inset:0; width:1200px; height:630px; }
.veu { position:absolute; inset:0; background:linear-gradient(90deg, rgba(12,10,9,.96) 0%%, rgba(12,10,9,.85) 38%%, rgba(12,10,9,0) 66%%); }
.moldura { position:absolute; inset:22px; border:1px solid rgba(236,228,214,.22); }
.conteudo { position:absolute; left:70px; top:66px; bottom:62px; width:700px; display:flex; flex-direction:column; }
.pilha { font:500 21px/1.03 'Oswald'; text-transform:uppercase; color:var(--osso); }
.pilha sup { font-size:.5em; margin-left:.12em; vertical-align:.9em; }
.linha-x { display:flex; align-items:center; gap:22px; margin:auto 0 18px; }
.xis { position:relative; width:46px; height:46px; }
.xis::before,.xis::after { content:''; position:absolute; left:50%%; top:50%%; width:118%%; height:21%%; background:var(--osso); transform:translate(-50%%,-50%%) rotate(45deg); }
.xis::after { transform:translate(-50%%,-50%%) rotate(-45deg); }
.fio { height:2px; width:420px; background:var(--osso); }
.sobre { font:500 19px/1 'Oswald'; letter-spacing:.12em; text-transform:uppercase; color:var(--cinza); margin-bottom:14px; }
.caixa { position:relative; display:inline-block; align-self:flex-start; padding:10px 22px 4px; font-stretch:125%%; font-weight:900; font-size:88px; line-height:1; text-transform:uppercase; color:var(--osso); }
.caixa::before { content:''; position:absolute; inset:0; border:2.5px solid var(--osso); }
.desgaste { -webkit-mask-image:url(assets/img/desgaste.png); mask-image:url(assets/img/desgaste.png); -webkit-mask-size:520px auto; mask-size:520px auto; }
.lema { margin-top:20px; font:500 23px/1.2 'Oswald'; letter-spacing:.03em; text-transform:uppercase; color:var(--osso); }
.lema b { color:var(--sangue); font-weight:500; }
.tags { display:flex; gap:10px; margin-top:22px; }
.tags span { border:1.5px solid var(--osso); padding:7px 12px 6px; font:500 15px/1.1 'Oswald'; text-transform:uppercase; color:var(--osso); background:rgba(12,10,9,.5); }
.selo { position:absolute; right:58px; bottom:56px; text-align:right; }
.selo .t { display:inline-block; border:1.5px solid var(--osso); padding:7px 12px 6px; font-stretch:125%%; font-weight:900; font-size:13px; letter-spacing:.09em; text-transform:uppercase; color:var(--osso); background:rgba(12,10,9,.7); }
.selo .s { display:inline-block; margin-top:8px; padding:6px 10px 5px; background:var(--carvao); font:500 15px/1 'Oswald'; letter-spacing:.1em; text-transform:uppercase; color:var(--sangue); }
</style></head><body>
<canvas id="c" width="2400" height="1260"></canvas>
<div class="veu"></div>
<div class="moldura"></div>
<div class="conteudo">
  <div class="pilha">Zapa<sup>BR</sup><br>Realismo<sup>BR</sup><br>Preto<sup>BR</sup><br>Cinza<sup>BR</sup></div>
  <div class="linha-x"><span class="xis"></span><span class="fio"></span></div>
  <div class="sobre">Thiago Zaparolli · Tatuador</div>
  <div class="caixa"><span class="desgaste">Zaparolli</span></div>
  <div class="lema">Dark art <b>✕</b> Realismo preto e cinza <b>✕</b> Coberturas</div>
  <div class="tags"><span>Projetos autorais</span><span>Estúdio privado · São José, SC</span></div>
</div>
<div class="selo"><div class="t desgaste">Jurado Tattoo Week 2025</div><div class="s">Agende pelo WhatsApp</div></div>
<script src="assets/js/meio-tom.js"></script>
<script>
const im = new Image();
im.onload = () => { const t = meioTomGL(document.getElementById('c'), im, {preserveDrawingBuffer:true}); t.desenhar(1.1, .45, 12); document.fonts.ready.then(() => { document.title = 'pronto'; }); };
im.src = 'assets/img/meio-tom-fonte.jpg';
</script></body></html>""" % BASE


def main():
    pagina = os.path.join(SITE, '_og.html')
    with open(pagina, 'w', encoding='utf-8') as f:
        f.write(HTML)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=BRAVE, args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
            pg = b.new_page(viewport={'width': 1200, 'height': 630}, device_scale_factor=1)
            pg.goto(BASE + '_og.html')
            pg.wait_for_function("document.title === 'pronto'", timeout=20000)
            pg.wait_for_timeout(600)
            png = os.path.join(SITE, '_og.png')
            pg.screenshot(path=png)
            b.close()
        from PIL import Image
        Image.open(png).convert('RGB').save(os.path.join(SITE, 'og.jpg'), quality=88, optimize=True, progressive=True)
        os.remove(png)
    finally:
        os.remove(pagina)
    print('og.jpg', round(os.path.getsize(os.path.join(SITE, 'og.jpg')) / 1024), 'KB')


if __name__ == '__main__':
    main()
