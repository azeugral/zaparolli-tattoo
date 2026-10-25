"""Gera os ornamentos laterais das seções (assets/img/orn/*.webp) a partir das ilustrações
geradas por IA sobre preto puro (../_ref/ornamentos, Figma "Zaparolli - texturas"): o preto vira
transparente (alfa pelo brilho), a cor é recuperada sem o preto e as bordas do quadro somem.
Uso: python tools/gerar_ornamentos.py"""
import os
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
FONTE = os.path.join(os.path.dirname(SITE), '_ref', 'ornamentos')
SAIDA = os.path.join(SITE, 'assets', 'img', 'orn')
LARG = {'galho-corvo': 560, 'cruz-corvo': 520, 'lua': 520, 'galhos-pendurados': 560}


def main():
    os.makedirs(SAIDA, exist_ok=True)
    for nome, larg in LARG.items():
        a = np.asarray(Image.open(os.path.join(FONTE, nome + '.png')).convert('RGB'), np.float32) / 255
        mx = a.max(2)
        alfa = np.clip((mx - .035) / .55, 0, 1) ** .9
        rgb = np.where(alfa[..., None] > .01, np.clip(a / np.maximum(alfa[..., None], 1e-3), 0, 1), 0)
        # tira o que encostar nas bordas do quadro sem querer (fade de 3%)
        H, W = alfa.shape
        yy, xx = np.mgrid[0:H, 0:W]
        borda = np.minimum.reduce([xx / (W * .03), (W - 1 - xx) / (W * .03), yy / (H * .03), (H - 1 - yy) / (H * .03)]).clip(0, 1)
        if nome in ('cruz-corvo',):          # encosta no chão de propósito
            borda = np.minimum.reduce([xx / (W * .03), (W - 1 - xx) / (W * .03), yy / (H * .03)]).clip(0, 1)
        if nome in ('galhos-pendurados',):   # pende do topo de propósito
            borda = np.minimum.reduce([xx / (W * .03), (W - 1 - xx) / (W * .03), (H - 1 - yy) / (H * .03)]).clip(0, 1)
        if nome in ('galho-corvo',):         # entra pela esquerda de propósito
            borda = np.minimum.reduce([(W - 1 - xx) / (W * .03), yy / (H * .03), (H - 1 - yy) / (H * .03)]).clip(0, 1)
        alfa = alfa * borda
        im = Image.fromarray(np.dstack([rgb * 255, alfa * 255]).astype(np.uint8), 'RGBA')
        im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 6 else 0).getbbox())
        im = im.resize((larg, round(larg * im.height / im.width)), Image.LANCZOS)
        im.save(os.path.join(SAIDA, nome + '.webp'), 'WEBP', quality=82, alpha_quality=85, method=6)
        print(nome, im.size, round(os.path.getsize(os.path.join(SAIDA, nome + '.webp')) / 1024), 'KB')


if __name__ == '__main__':
    main()
