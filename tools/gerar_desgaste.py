"""Gera assets/img/titulo-desgaste.webp, a máscara dos títulos principais, a partir da textura de
concreto rachado gerada por IA (Figma, gpt-image) em ../_ref/textura-ia/concreto-1.png: creme vira
letra, os pretos (respingos, lascas, rachaduras e os cortes diagonais) viram falha, e as manchas
cinza ficam meio transparentes. O ladrilho é fechado sem costura (mistura com a versão deslocada).
Uso: python tools/gerar_desgaste.py"""
import os
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
FONTE = os.path.join(os.path.dirname(SITE), '_ref', 'textura-ia', 'concreto-1.png')
SAIDA = os.path.join(SITE, 'assets', 'img', 'titulo-desgaste.webp')


def main():
    im = Image.open(FONTE).convert('L')
    a = np.asarray(im, np.float32) / 255
    H, W = a.shape
    # sem costura: mistura com a versão deslocada meio ladrilho, pesando o centro de cada uma
    rol = np.roll(np.roll(a, H // 2, 0), W // 2, 1)
    yy, xx = np.mgrid[0:H, 0:W]
    m = (np.sin(np.pi * (yy + .5) / H) * np.sin(np.pi * (xx + .5) / W)) ** .7
    a = a * m + rol * (1 - m)
    # curva: creme = opaco; cinza das manchas = meio; preto = falha
    alfa = np.clip((a - .18) / .5, 0, 1) ** 1.15
    rgba = np.dstack([np.full((H, W), 255, np.uint8)] * 3 + [(alfa * 255).astype(np.uint8)])
    out = Image.fromarray(rgba, 'RGBA')
    out = out.resize((1280, round(1280 * H / W)), Image.LANCZOS)
    out.save(SAIDA, 'WEBP', quality=80, alpha_quality=80, method=6)
    print(SAIDA, out.size, round(os.path.getsize(SAIDA) / 1024), 'KB')


if __name__ == '__main__':
    main()
