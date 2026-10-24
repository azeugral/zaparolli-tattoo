"""Gera assets/img/desgaste-titulo.png, a máscara dos títulos principais, fiel à referência
que o cliente aprovou: manchas cinza grandes e suaves (meia transparência), pontinhos pretos
em losango e em gota, rachaduras finas e tortas e cortes diagonais que atravessam as letras.
Branco opaco = tinta; transparente = falha. Uso: python tools/gerar_desgaste.py"""
import os, random, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), 'assets', 'img', 'desgaste-titulo.png')
W, H = 1400, 700
random.seed(31)


def main():
    falha = Image.new('L', (W, H), 0)          # 0 = nada tirado, 255 = tirado
    d = ImageDraw.Draw(falha)

    # manchas grandes e suaves (tiram só parte da tinta: viram cinza)
    manchas = Image.new('L', (W, H), 0)
    dm = ImageDraw.Draw(manchas)
    for _ in range(170):
        x, y = random.uniform(0, W), random.uniform(0, H)
        r = random.uniform(9, 26)
        dm.ellipse((x - r, y - r * random.uniform(.8, 1.15), x + r, y + r), fill=random.randint(70, 150))
    manchas = manchas.filter(ImageFilter.GaussianBlur(3.2))

    # pontinhos pretos: losangos e gotas (tiram tudo)
    for _ in range(520):
        x, y = random.uniform(0, W), random.uniform(0, H)
        r = random.choice((2.5, 3, 3.5, 4, 5, 6))
        if random.random() < .45:
            d.polygon([(x, y - r * 1.3), (x + r, y), (x, y + r * 1.3), (x - r, y)], fill=255)
        else:
            d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    for _ in range(900):                            # poeira fina
        x, y = random.uniform(0, W), random.uniform(0, H); r = random.choice((1, 1.4, 1.8))
        d.ellipse((x - r, y - r, x + r, y + r), fill=random.randint(150, 255))

    # rachaduras finas e tortas (curtas, em várias direções)
    for _ in range(46):
        x, y = random.uniform(0, W), random.uniform(0, H)
        ang = random.uniform(-.6, .6) + (math.pi if random.random() < .5 else 0)
        pts = [(x, y)]
        for _ in range(random.randint(5, 12)):
            ang += random.uniform(-.45, .45)
            L = random.uniform(8, 22)
            x += math.cos(ang) * L; y += math.sin(ang) * L * .5
            pts.append((x, y))
        d.line(pts, fill=255, width=random.choice((1, 1, 2)))

    # cortes diagonais longos, como os riscos do logo (subindo da esquerda para a direita)
    for _ in range(9):
        x0 = random.uniform(-200, W); y0 = random.uniform(H * .2, H * 1.1)
        L = random.uniform(260, 700); ang = random.uniform(-.42, -.18)
        n = 40
        pts = [(x0 + math.cos(ang) * L * i / n + random.uniform(-1.2, 1.2), y0 + math.sin(ang) * L * i / n + random.uniform(-1.2, 1.2)) for i in range(n + 1)]
        d.line(pts, fill=255, width=random.choice((2, 2, 3)))

    falha = np.maximum(np.asarray(falha, np.float32), np.asarray(manchas, np.float32))
    alpha = 255 - falha
    rgba = np.dstack([np.full((H, W), 255, np.uint8)] * 3 + [alpha.clip(0, 255).astype(np.uint8)])
    Image.fromarray(rgba, 'RGBA').save(SAIDA, optimize=True)
    print(SAIDA, round(os.path.getsize(SAIDA) / 1024), 'KB')


if __name__ == '__main__':
    main()
