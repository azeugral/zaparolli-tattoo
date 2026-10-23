"""Gera og.jpg (1200x630), a imagem que aparece quando o link é compartilhado.
Monta uma página com o xerox chiado do hero (assets/js/xerox.js) e a tipografia do site
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
:root { --carvao:#0b0b0b; --osso:#f2f2f0; --cinza:#9c9c9a; --sangue:#d42a1e; }
* { box-sizing:border-box; margin:0; }
body { width:1200px; height:630px; background:var(--carvao); overflow:hidden; position:relative; font-family:'Archivo'; }
/* a caveira fica centrada atrás do texto: o canvas é maior que a página e deslocado */
canvas { position:absolute; left:-1114px; top:-135px; width:2449px; height:900px; }
.veu { position:absolute; inset:0; background:radial-gradient(ellipse 360px 270px at 50%% 52%%, rgba(11,11,11,.9), rgba(11,11,11,.62) 65%%, rgba(11,11,11,.1) 100%%), linear-gradient(180deg, rgba(11,11,11,.35), rgba(11,11,11,0) 30%%, rgba(11,11,11,0) 70%%, rgba(11,11,11,.55)); }
.moldura { position:absolute; inset:22px; border:1px solid rgba(242,242,240,.22); }
.centro { position:absolute; left:300px; width:600px; top:0; bottom:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }
.sobre { font:500 18px/1 'Oswald'; letter-spacing:.16em; text-transform:uppercase; color:var(--osso); opacity:.8; margin-bottom:18px; }
.linha-x { display:flex; align-items:center; gap:18px; margin-bottom:20px; }
.fio { height:2px; width:120px; background:var(--osso); }
.xis { position:relative; width:40px; height:40px; }
.xis::before,.xis::after { content:''; position:absolute; left:50%%; top:50%%; width:118%%; height:21%%; background:var(--sangue); transform:translate(-50%%,-50%%) rotate(45deg); }
.xis::after { transform:translate(-50%%,-50%%) rotate(-45deg); }
.caixa { position:relative; display:inline-block; padding:9px 18px 3px; font-stretch:125%%; font-weight:900; font-size:64px; line-height:1; text-transform:uppercase; color:var(--osso); background:rgba(11,11,11,.55); }
.caixa::before { content:''; position:absolute; inset:0; border:2.5px solid var(--osso); }
.desgaste { -webkit-mask-image:url(assets/img/desgaste.png); mask-image:url(assets/img/desgaste.png); -webkit-mask-size:520px auto; mask-size:520px auto; }
.lema { margin-top:20px; font:500 21px/1.2 'Oswald'; letter-spacing:.04em; text-transform:uppercase; color:var(--osso); }
.lema b { color:var(--sangue); font-weight:500; margin:0 .25em; }
.selo { margin-top:22px; display:inline-block; border:1.5px solid var(--sangue); padding:8px 13px 7px; font-stretch:125%%; font-weight:900; font-size:13px; letter-spacing:.1em; text-transform:uppercase; color:var(--osso); background:rgba(11,11,11,.75); }
.pilha { position:absolute; left:58px; top:54px; font:500 21px/1.03 'Oswald'; text-transform:uppercase; color:var(--osso); text-align:left; }
.pilha sup { font-size:.5em; margin-left:.12em; vertical-align:.9em; color:var(--sangue); }
.local { position:absolute; right:58px; bottom:52px; text-align:right; font:500 16px/1.4 'Oswald'; letter-spacing:.1em; text-transform:uppercase; color:var(--osso); }
.local b { display:block; color:var(--sangue); font-weight:500; }
</style></head><body>
<canvas id="c" width="2449" height="900"></canvas>
<div class="veu"></div>
<div class="moldura"></div>
<div class="pilha">Zapa<sup>BR</sup><br>Realismo<sup>BR</sup><br>Preto<sup>BR</sup><br>Cinza<sup>BR</sup></div>
<div class="centro">
  <div class="sobre">Thiago Zaparolli · <b style="color:var(--sangue);font-weight:500">Tatuador</b></div>
  <div class="linha-x"><span class="fio"></span><span class="xis"></span><span class="fio"></span></div>
  <div class="caixa"><span class="desgaste">Zaparolli</span></div>
  <div class="lema">Dark art<b>✕</b>Coberturas</div>
  <div class="selo desgaste">Jurado Tattoo Week 2025</div>
</div>
<div class="local">São José · SC<b>Agende pelo WhatsApp</b></div>
<script src="assets/js/xerox.js"></script>
<script>
const im = new Image();
im.onload = () => { const t = xeroxGL(document.getElementById('c'), im, {preserveDrawingBuffer:true}); t.desenhar(1.1, 7); document.fonts.ready.then(() => { document.title = 'pronto'; }); };
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
