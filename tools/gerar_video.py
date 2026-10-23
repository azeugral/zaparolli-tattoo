"""Renderiza o fundo do hero dos aparelhos de toque, em pé e deitado, e o pôster.
Modo padrão: meio-tom fino (assets/js/meio-tom.js). Com --xerox: o xerox chiado
(assets/js/xerox.js), 12 quadros por segundo, cada quadro com um chiado novo.
Quadro a quadro num Chromium headless (Playwright + Brave), ffmpeg do imageio-ffmpeg.
Uso: python tools/gerar_video.py [--xerox]"""
import os, sys, subprocess, base64
from playwright.sync_api import sync_playwright
import imageio_ffmpeg

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
SAIDA = os.path.join(SITE, 'assets', 'video')
BRAVE = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'

# nome, largura, altura, tamanho da célula do pontilhado em px do vídeo
MEIOTOM = '--xerox' not in sys.argv
if MEIOTOM:
    VERSOES = [('meio-tom-celular', 720, 1560, 5.5), ('meio-tom-deitado', 1280, 590, 4.5)]
    FPS, SEGUNDOS, SCRIPT, FUNC, POSTER = 24, 12, 'meio-tom.js', 'meioTomGL', 'meio-tom-poster.webp'
else:
    # resolução menor de propósito: o chiado pesa no vídeo e o grão grosso combina com o xerox
    VERSOES = [('xerox-celular', 450, 976, 0), ('xerox-deitado', 880, 406, 0)]
    FPS, SEGUNDOS, SCRIPT, FUNC, POSTER = 12, 12, 'xerox.js', 'xeroxGL', 'xerox-poster.webp'
RAIO = .3                       # mesma velocidade do desktop (raio .45 em 18 s)


def renderizar(nome, LARG, ALT, CEL, poster=False):
    quadros = FPS * SEGUNDOS
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    mp4 = os.path.join(SAIDA, nome + '.mp4')
    enc = subprocess.Popen([ff, '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'png', '-i', '-',
                            '-c:v', 'libx264', '-preset', 'slow', '-crf', '26' if MEIOTOM else '31', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
                            '-movflags', '+faststart', '-an', mp4], stdin=subprocess.PIPE)
    with open(os.path.join(SITE, 'assets', 'img', 'meio-tom-fonte.jpg'), 'rb') as f:
        foto = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=BRAVE, args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        pg = b.new_page(viewport={'width': LARG, 'height': ALT})
        pg.set_content(f'<body style="margin:0"><canvas id="c" width="{LARG}" height="{ALT}"></canvas></body>')
        pg.add_script_tag(path=os.path.join(SITE, 'assets', 'js', SCRIPT))
        pg.evaluate("""src => new Promise(ok => { const im = new Image(); im.onload = () => {
            window.T = window[FUNC](document.getElementById('c'), im, {preserveDrawingBuffer: true}); ok(); }; im.src = src; })""".replace('FUNC', repr(FUNC)), foto)
        for i in range(quadros):
            fase = i / quadros * 6.283185307179586
            args = f'{fase}, {RAIO}, {CEL}' if MEIOTOM else f'{fase}, {i}'
            dado = pg.evaluate(f"(T.desenhar({args}), document.getElementById('c').toDataURL('image/png'))")
            png = base64.b64decode(dado.split(',', 1)[1])
            enc.stdin.write(png)
            if i == 0 and poster:
                with open(os.path.join(SAIDA, 'poster.png'), 'wb') as f:
                    f.write(png)
        b.close()
    enc.stdin.close(); enc.wait()
    if poster:
        from PIL import Image
        Image.open(os.path.join(SAIDA, 'poster.png')).convert('RGB').save(os.path.join(SITE, 'assets', 'img', POSTER), 'WEBP', quality=78)
        os.remove(os.path.join(SAIDA, 'poster.png'))
    print(mp4, round(os.path.getsize(mp4) / 1e6, 2), 'MB')


def main():
    os.makedirs(SAIDA, exist_ok=True)
    for i, (nome, w, h, c) in enumerate(VERSOES):
        renderizar(nome, w, h, c, poster=(i == 0))


if __name__ == '__main__':
    main()
