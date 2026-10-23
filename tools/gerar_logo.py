"""Gera o logo ZAPAROLLI em imagem (assets/img/logo-zaparolli.webp e .png), no estilo do
mockup que o cliente mandou: letra condensada pesada, letras quase encostadas, textura de
concreto creme com manchas cinza, respingos e lascas nas bordas, e dois riscos longos na
diagonal atravessando a palavra. Fundo transparente.
Base tipográfica: Anton (../_ref/Anton.ttf). Uso: python tools/gerar_logo.py"""
import os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
REF = os.path.join(os.path.dirname(SITE), '_ref')

TXT = 'ZAPAROLLI'
TAM = 520            # corpo da letra em px
ESPACO = -14         # letras quase encostadas
MARGEM = 40
rng = np.random.default_rng(23)
random.seed(23)


def ruido(w, h, escala, sigma=0):
    """Ruído suave em [0,1] com grão de `escala` px."""
    n = rng.random((max(2, h // escala), max(2, w // escala)))
    im = Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    if sigma:
        im = im.filter(ImageFilter.GaussianBlur(sigma))
    return np.asarray(im, dtype=np.float32) / 255


def main():
    fonte = ImageFont.truetype(os.path.join(REF, 'Anton.ttf'), TAM)
    larguras = [fonte.getlength(c) for c in TXT]
    W = int(sum(larguras) + ESPACO * (len(TXT) - 1) + 2 * MARGEM)
    x0, y0, x1, y1 = fonte.getbbox(TXT)
    H = int(y1 - y0 + 2 * MARGEM)

    # 1. máscara das letras
    m = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(m)
    x = MARGEM
    for c, lg in zip(TXT, larguras):
        d.text((x, MARGEM - y0), c, font=fonte, fill=255)
        x += lg + ESPACO
    a = np.asarray(m, dtype=np.float32) / 255

    # 2. bordas roídas: desfoca, soma ruído fino e corta de novo
    borda = np.asarray(m.filter(ImageFilter.GaussianBlur(1.3)), dtype=np.float32) / 255
    a = ((borda + (ruido(W, H, 3) - .5) * .3 + (ruido(W, H, 22) - .5) * .18) > .5).astype(np.float32)

    # 3. lascas: pedaços tirados das bordas e respingos (furos) por dentro
    furos = Image.new('L', (W, H), 0)
    fd = ImageDraw.Draw(furos)
    for _ in range(62):    # respingos em grupos, com pedaços irregulares
        gx, gy = random.uniform(0, W), random.uniform(0, H)
        for _ in range(random.randint(3, 14)):
            cx, cy = gx + random.gauss(0, 22), gy + random.gauss(0, 16)
            r = random.choice((1.5, 2, 3, 4, 6))
            pts = [(cx + r * random.uniform(.5, 1.6) * np.cos(t), cy + r * random.uniform(.5, 1.6) * np.sin(t)) for t in np.linspace(0, 6.28, 7)[:-1]]
            fd.polygon(pts, fill=255)
    for _ in range(160):   # pontos soltos pequenos
        cx, cy = random.uniform(0, W), random.uniform(0, H); r = random.choice((1, 1.5, 2))
        fd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    for _ in range(90):    # lascas nas bordas e no miolo
        cx, cy = random.uniform(0, W), random.uniform(0, H)
        pts = [(cx + random.uniform(-12, 12), cy + random.uniform(-7, 7)) for _ in range(4)]
        fd.polygon(pts, fill=255)
    for _ in range(18):    # arranhões curtos
        cx, cy = random.uniform(0, W), random.uniform(0, H)
        L = random.uniform(20, 120); ang = random.uniform(-.5, .2)
        fd.line((cx, cy, cx + L, cy + L * ang), fill=255, width=random.choice((1, 2)))
    # 4. riscos longos na diagonal (de baixo à esquerda para cima à direita)
    for xa, ya, xb, yb, w in [(-.05, .82, .72, .12, 6), (.36, 1.04, 1.06, .3, 5), (.0, .66, .4, .36, 2)]:
        n = 80
        pts = []
        for i in range(n + 1):
            t = i / n
            pts.append((W * (xa + (xb - xa) * t) + random.uniform(-2, 2), H * (ya + (yb - ya) * t) + random.uniform(-2, 2)))
        fd.line(pts, fill=255, width=w)
    f = np.asarray(furos.filter(ImageFilter.GaussianBlur(.6)), dtype=np.float32) / 255
    a = np.clip(a - f * 1.2, 0, 1)

    # 5. textura de concreto: creme com manchas cinza e pontinhos escuros
    creme = np.array([236, 228, 214], np.float32)
    cinza = np.array([150, 144, 135], np.float32)
    escuro = np.array([70, 66, 61], np.float32)
    manchas = ruido(W, H, 90, 8) * .55 + ruido(W, H, 26, 2) * .3 + ruido(W, H, 6) * .15
    mancha = np.clip((manchas - .48) * 4, 0, 1)[..., None] * .9
    riscos_v = np.clip((ruido(W, H, 1, 0)[:, :1].repeat(W, 1) * 0 + (np.asarray(Image.fromarray((rng.random((8, W)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), dtype=np.float32) / 255) - .82) * 4, 0, 1)[..., None] * .3
    pont = (ruido(W, H, 2) > .965).astype(np.float32)[..., None] * .5
    veio = np.clip((ruido(W, H, 5, 1) - .7) * 4, 0, 1)[..., None] * .35
    cor = creme * (1 - mancha) + cinza * mancha
    cor = cor * (1 - pont) + escuro * pont
    cor = cor * (1 - veio) + escuro * veio
    cor = cor * (1 - riscos_v) + cinza * riscos_v
    # leve variação de luz da esquerda para a direita
    cor *= (0.94 + .08 * ruido(W, H, 300, 20))[..., None]

    rgba = np.dstack([np.clip(cor, 0, 255), (a * 255)]).astype(np.uint8)
    im = Image.fromarray(rgba, 'RGBA')
    # corta a sobra
    bb = im.getbbox()
    im = im.crop((max(0, bb[0] - 6), max(0, bb[1] - 6), min(W, bb[2] + 6), min(H, bb[3] + 6)))
    saida = os.path.join(SITE, 'assets', 'img')
    im.save(os.path.join(saida, 'logo-zaparolli.png'), optimize=True)
    im.save(os.path.join(saida, 'logo-zaparolli.webp'), 'WEBP', quality=90, method=6)
    pequeno = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    pequeno.save(os.path.join(saida, 'logo-zaparolli-1200.webp'), 'WEBP', quality=90, method=6)
    print(im.size, round(os.path.getsize(os.path.join(saida, 'logo-zaparolli.webp')) / 1024), 'KB')

    # prova sobre fundo escuro
    prova = Image.new('RGB', (im.width + 80, im.height + 80), (12, 11, 10))
    prova.paste(im, (40, 40), im)
    prova.save(os.path.join(REF, 'logo-prova.png'))


if __name__ == '__main__':
    main()
