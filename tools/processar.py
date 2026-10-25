"""Gera as imagens do site a partir de ../_ref/ig (Instagram @zaparollitattoo, 22/10/2026).
- portfólio em assets/obras (640 e 1080 px, recorte 4:5) + assets/js/obras.js
- fotos de apoio em assets/img (tom sépia e grão, como nos posts dele)
- fonte do meio-tom do hero, textura de desgaste dos títulos, favicons e og.jpg
Uso: python tools/processar.py"""
import os, json, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance, ImageChops

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
REF = os.path.join(os.path.dirname(SITE), '_ref')
IG = os.path.join(REF, 'ig')
IMG = os.path.join(SITE, 'assets', 'img')
OBRAS = os.path.join(SITE, 'assets', 'obras')

# (post, foto do carrossel, categoria, legenda, foco vertical do recorte)
PORTFOLIO = [
    (14, 9, 'fech', 'Costas em 5 dias, guest em SP', .5),
    (11, 15, 'dark', 'Collab com Gus Tattoo', .5),
    (61, 0, 'dark', 'A escuridão inspira', .45),
    (7, 0, 'dark', 'Saturno, releitura de Goya', .42),
    (4, 0, 'dark', 'A criatura que respira com a pele', .45),
    (48, 0, 'cob', 'Cobertura: antes e depois', .5),
    (28, 0, 'fech', '30 horas em 4 dias seguidos', .45),
    (1, 0, 'dark', 'Entre túmulos e sombras', .45),
    (6, 0, 'dark', 'Onde existe instinto', .45),
    (9, 0, 'dark', 'Vivendo dentro da escuridão', .45),
    (64, 0, 'dark', 'O abraço do mal', .45),
    (83, 0, 'dark', 'Médico da peste', .45),
    (77, 0, 'fech', 'Máscara Hannya', .45),
    (10, 0, 'dark', 'A verdadeira morte', .45),
    (19, 0, 'dark', 'Portas irreversíveis', .45),
    (20, 0, 'real', 'Caveira e capacete', .45),
    (26, 0, 'dark', 'Luz e trevas, cicatrizado', .45),
    (30, 0, 'real', 'O sagrado', .45),
    (31, 0, 'dark', 'A sombra do que vai morrer', .45),
    (33, 0, 'dark', 'Feita em São Paulo', .45),
    (35, 0, 'real', 'Entre a luz e o abismo', .45),
    (36, 0, 'dark', 'Biomecânico', .45),
    (37, 0, 'dark', 'Entre sombras e ossos', .45),
    (42, 0, 'dark', 'O rei da escuridão eterna', .45),
    (43, 0, 'dark', 'Destino entre ossos', .45),
    (44, 0, 'dark', 'Nossos demônios', .45),
    (50, 0, 'dark', 'Entre sombras e mistérios', .45),
    (51, 0, 'dark', 'Demônios que acompanham', .45),
    (53, 0, 'dark', 'Ícone do horror', .45),
    (54, 0, 'dark', 'No escuro, me encontrei', .45),
    (56, 0, 'real', 'Passagem bíblica', .45),
    (59, 0, 'dark', 'Dez anos de espera', .45),
    (65, 0, 'dark', 'O mal triunfou', .45),
    (68, 0, 'dark', 'O pavor no olhar', .45),
    (73, 0, 'dark', 'Nas sombras das velas', .45),
    (75, 0, 'real', 'Caveira Harley-Davidson', .45),
    (92, 0, 'dark', 'Jack Skellington', .45),
    (162, 0, 'fech', 'Piratas do Caribe', .45),
]

# fotos de apoio: nome -> (post_foto, recorte (l, t, r, b) relativo ou None, proporção, larguras)
APOIO = {
    'tattoo-week': ('034_0', None, (4, 5), (640, 1080)),
    'costas-5-dias': ('014_7', None, (4, 5), (640, 1080)),
}


# fotos em alta enviadas pelo cliente (24/10, ../_ref/hq-cliente), no lugar das do Instagram
HQ = {'014_9': 'IMG_6314.jpg.jpeg', '051_0': 'IMG_2159.JPG.jpeg', '077_0': 'IMG_2160.JPG.jpeg', '028_0': 'IMG_2161.JPG.jpeg',
      '053_0': 'IMG_3330 2.JPG.jpeg', '065_0': 'IMG_3334.JPG.jpeg', '073_0': 'IMG_3335 2.JPG.jpeg', '031_0': 'IMG_8896.JPG.jpeg'}
# obras novas, só em alta: (arquivo, categoria, legenda, foco do recorte, depois de qual post entra)
NOVAS = [('IMG_6313.jpg.jpeg', 'fech', 'Costas com o ceifador e a casa', .4, 14),
         ('IMG_5374.jpg.jpeg', 'dark', 'Médico da peste, cicatrizado', .4, 83),
         ('IMG_3337 2.JPG.jpeg', 'real', 'Kratos', .45, 20)]


def abrir_hq(arquivo):
    return ImageOps.exif_transpose(Image.open(os.path.join(REF, 'hq-cliente', arquivo))).convert('RGB')


def abrir(nome):
    return Image.open(os.path.join(IG, nome + '.jpg')).convert('RGB')


def recortar(im, prop, foco=.45):
    return ImageOps.fit(im, (im.width, round(im.width * prop[1] / prop[0])) if im.width * prop[1] / prop[0] <= im.height
                        else (round(im.height * prop[0] / prop[1]), im.height), Image.LANCZOS, centering=(.5, foco))


def grao(im, forca=10, semente=1):
    """Grão de filme leve, igual ao acabamento dos posts dele."""
    rng = np.random.default_rng(semente)
    a = np.asarray(im, dtype=np.float32)
    a += rng.normal(0, forca, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def sepia(im, quanto=.55):
    """Puxa a foto para o preto e cinza do site (antes era sépia)."""
    cinza = ImageOps.grayscale(im)
    tom = ImageOps.colorize(cinza, black=(10, 10, 10), mid=(118, 118, 116), white=(242, 242, 240))
    return Image.blend(im, tom, quanto)


def salvar(im, nome, larguras, pasta=IMG, q=86):
    for w in larguras:
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(os.path.join(pasta, f'{nome}-{w}.webp'), 'WEBP', quality=q, method=6)


def fonte(tam, peso=900, largura=125, arquivo='Archivo.ttf'):
    f = ImageFont.truetype(os.path.join(REF, arquivo), tam)
    try:
        f.set_variation_by_axes([peso, largura] if 'Archivo' in arquivo else [peso])
    except Exception:
        pass
    return f


def main():
    for p in (IMG, OBRAS):
        os.makedirs(p, exist_ok=True)

    dados = []
    fila = []
    for post, k, cat, leg, foco in PORTFOLIO:
        fila.append((f'{post:03d}_{k}', cat, leg, foco, f'z{post:03d}'))
        for arq, ncat, nleg, nfoco, depois in NOVAS:
            if depois == post:
                fila.append((None, ncat, nleg, nfoco, 'n' + arq.split('.')[0].replace(' ', '').lower().replace('img_', ''), arq))
    for item in fila:
        orig, cat, leg, foco, f = item[:5]
        if orig is None:
            origem = abrir_hq(item[5])
        elif orig in HQ:
            origem = abrir_hq(HQ[orig])
        else:
            origem = abrir(orig)
        # a foto das costas em alta é de corpo inteiro: no portfólio, o recorte fecha na tatuagem
        if orig == '014_9':
            origem = origem.crop((round(origem.width * .05), round(origem.height * .08), round(origem.width * .93), round(origem.height * .96)))
        im = recortar(origem, (4, 5), foco)
        im.resize((640, 800), Image.LANCZOS).save(os.path.join(OBRAS, f + '-640.webp'), 'WEBP', quality=86, method=6)
        larg = min(1080, im.width)
        im.resize((larg, round(larg * 1.25)), Image.LANCZOS).save(os.path.join(OBRAS, f + '-1080.webp'), 'WEBP', quality=88, method=6)
        dados.append({'f': f, 'c': cat, 't': leg})
    # coberturas com antes e depois enviadas pelo cliente (24/10): na grade, recorte 4:5 do centro;
    # na tela cheia (1080), a foto inteira com o antes e o depois lado a lado
    COBS = [('medico-peste', 'Médico da peste sobre a carpa colorida'), ('mascara-gas', 'Máscara de gás sobre o desenho antigo'),
            ('espartano-corvo', 'Espartano e corvo sobre o dragão colorido'), ('vampira', 'Vampira com vela sobre o gato'),
            ('viking', 'Viking de tapa-olho sobre o braço fechado'),
            ('noiva-cadaver', 'Noiva Cadáver e casa assombrada sobre o braço de anime')]
    pos = next(i for i, d in enumerate(dados) if d['c'] == 'cob') + 1
    for nome, leg in reversed(COBS):
        im = Image.open(os.path.join(REF, 'coberturas-cliente', nome + '.jpg')).convert('RGB')
        f = 'c-' + nome
        ImageOps.fit(im, (640, 800), Image.LANCZOS, centering=(.5, .5)).save(os.path.join(OBRAS, f + '-640.webp'), 'WEBP', quality=86, method=6)
        larg = min(1080, im.width)
        im.resize((larg, round(larg * im.height / im.width)), Image.LANCZOS).save(os.path.join(OBRAS, f + '-1080.webp'), 'WEBP', quality=88, method=6)
        dados.insert(pos, {'f': f, 'c': 'cob', 't': leg})
    with open(os.path.join(SITE, 'assets', 'js', 'obras.js'), 'w', encoding='utf-8') as fp:
        fp.write('/* gerado por tools/processar.py */\nwindow.OBRAS = ' + json.dumps(dados, ensure_ascii=False, indent=0) + ';\n')

    for nome, (orig, box, prop, larguras) in APOIO.items():
        im = abrir(orig)
        if box:
            im = im.crop((round(box[0] * im.width), round(box[1] * im.height), round(box[2] * im.width), round(box[3] * im.height)))
        im = recortar(im, prop)
        im = sepia(im, .5)
        salvar(im, nome, larguras)

    # arte do hero (v7): as costas de 5 dias, sem a borda vermelha do post, no tom quente
    # da referência do cliente (preto, cinza quente e creme); grão fino para não formar degraus
    alta = abrir_hq(HQ['014_9'])
    arte = alta.crop((round(alta.width * .06), round(alta.height * .1), round(alta.width * .9), round(alta.height * .93)))
    arte = ImageOps.grayscale(arte)
    arte = ImageOps.autocontrast(arte, cutoff=(1.5, .3))
    # profundidade como na tatuagem original (24/10): sombras afundadas no preto puro,
    # meio-tons mais baixos e os brilhos do osso preservados (curva só nas sombras + contraste local)
    lut = []
    for v in range(256):
        x = max(0, (v / 255 - .05) / .95)
        # abaixo de 24%: afunda no preto (expoente 1,8); acima: segue linear até o branco
        y = .24 * (x / .24) ** 1.8 if x < .24 else .24 + (x - .24) * 1.0
        lut.append(max(0, min(255, round(y * 255))))
    arte = arte.point(lut)
    # contraste local: separa o osso das sombras, dá volume como na foto da sessão
    arte = arte.filter(ImageFilter.UnsharpMask(radius=38, percent=55, threshold=0))
    arte = ImageOps.colorize(arte, black=(5, 4, 4), mid=(118, 110, 100), white=(242, 233, 218))
    arte = grao(arte, 3, 3)
    salvar(arte, 'hero-arte', (720, 1020), q=90)
    w, h = arte.size
    salvar(arte.crop((round(w * .1), round(h * .13), round(w * .95), round(h * .98))), 'hero-arte-m', (720, 860), q=90)

    # coberturas enviadas pelo cliente (24/10), em ../_ref/coberturas-cliente: cada foto junta
    # o antes (esquerda) e o depois (direita).
    COB = os.path.join(REF, 'coberturas-cliente')
    # médico da peste: metades separadas, ombro e contorno do braço alinhados, para o comparador
    peste = Image.open(os.path.join(COB, 'medico-peste.jpg')).convert('RGB')
    for nome, caixa in (('cobertura-antes', (16, 144, 975, 1903)), ('cobertura-depois', (1071, 144, 2030, 1903))):
        salvar(peste.crop(caixa), nome, (480, 600, 900), q=88)
    # as outras quatro entram inteiras (antes | depois), em quadrado
    os.makedirs(os.path.join(IMG, 'cob'), exist_ok=True)
    for nome in ('mascara-gas', 'espartano-corvo', 'vampira', 'viking'):
        im = Image.open(os.path.join(COB, nome + '.jpg')).convert('RGB')
        lado = min(im.size)
        im = ImageOps.fit(im, (lado, lado), Image.LANCZOS, centering=(.5, .5))
        salvar(im, nome, (640, 1080), pasta=os.path.join(IMG, 'cob'), q=86)

    # fotos do estúdio enviadas pelo cliente (24/10), convertidas de HEIC em ../_ref/estudio-cliente/jpg
    EST = os.path.join(REF, 'estudio-cliente', 'jpg')
    os.makedirs(os.path.join(IMG, 'estudio'), exist_ok=True)
    for nome, foco in (('IMG_6290', .55), ('IMG_6300', .5), ('IMG_6286', .5), ('IMG_6287', .55), ('IMG_6288', .5), ('IMG_6291', .45),
                       ('IMG_6295', .5), ('IMG_6297', .45), ('IMG_6299', .5), ('IMG_6302', .5)):
        im = Image.open(os.path.join(EST, nome + '.jpg')).convert('RGB')
        im = ImageOps.fit(im, (im.width, round(im.width * 1.25)) if im.width * 1.25 <= im.height else (round(im.height * .8), im.height), Image.LANCZOS, centering=(.5, foco))
        salvar(im, nome.lower().replace('img_', 'est-'), (640, 1080), pasta=os.path.join(IMG, 'estudio'), q=86)

    # logo oficial ZAPAROLLI enviado pelo cliente (23/10): só recorta a sobra transparente
    logo = Image.open(os.path.join(REF, 'logo-cliente', 'logo-original.png')).convert('RGBA')
    logo = logo.crop(logo.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())
    logo.save(os.path.join(IMG, 'logo-zaparolli.webp'), 'WEBP', quality=90, method=6)
    logo.resize((1200, round(logo.height * 1200 / logo.width)), Image.LANCZOS).save(os.path.join(IMG, 'logo-zaparolli-1200.webp'), 'WEBP', quality=90, method=6)
    print('logo', logo.size)

    # fonte do meio-tom do hero: as costas de 5 dias, em cinza com contraste puxado
    hf = ImageOps.grayscale(abrir('014_9'))
    hf = ImageOps.autocontrast(hf, cutoff=1)
    hf = ImageEnhance.Contrast(hf).enhance(1.25)
    hf = hf.filter(ImageFilter.GaussianBlur(1.2))
    hf.save(os.path.join(IMG, 'meio-tom-fonte.jpg'), quality=86)

    # textura de desgaste dos títulos (máscara: branco = tinta, transparente = falha)
    W, H = 1200, 300
    random.seed(7)
    m = Image.new('L', (W, H), 255)
    d = ImageDraw.Draw(m)
    for _ in range(2600):
        x, y, r = random.uniform(0, W), random.uniform(0, H), random.choice((.6, .8, 1, 1.2, 1.6, 2.2))
        d.ellipse((x - r, y - r, x + r, y + r), fill=random.randint(0, 120))
    for _ in range(90):
        x, y = random.uniform(0, W), random.uniform(0, H)
        L, ang = random.uniform(12, 70), random.uniform(-.35, .35)
        d.line((x, y, x + L, y + L * ang), fill=random.randint(30, 140), width=1)
    nuvem = Image.effect_noise((W // 6, H // 6), 90).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    nuvem = nuvem.point(lambda v: 255 if v > 112 else int(150 + v * .8))
    m = ImageChops.multiply(m, nuvem)
    rgba = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    rgba.putalpha(m)
    rgba.save(os.path.join(IMG, 'desgaste.png'), optimize=True)

    # favicon: X sobre carvão
    fav = Image.new('RGB', (512, 512), (11, 11, 11))
    d = ImageDraw.Draw(fav)
    d.text((256, 262), 'Z', font=fonte(380), fill=(242, 242, 240), anchor='mm')
    fav.resize((32, 32), Image.LANCZOS).save(os.path.join(SITE, 'favicon-32.png'))
    fav.resize((180, 180), Image.LANCZOS).save(os.path.join(SITE, 'apple-touch-icon.png'))
    fav.save(os.path.join(SITE, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])

    # og.jpg 1200x630
    og = Image.new('RGB', (1200, 630), (11, 11, 11))
    foto = grao(sepia(ImageOps.fit(abrir('014_9'), (520, 630), centering=(.5, .45)), .45), 8)
    og.paste(foto, (680, 0))
    d = ImageDraw.Draw(og)
    d.rectangle((54, 196, 640, 318), outline=(242, 242, 240), width=3)
    d.text((80, 257), 'ZAPAROLLI', font=fonte(84), fill=(242, 242, 240), anchor='lm')
    d.text((60, 120), 'THIAGO ZAPAROLLI', font=fonte(34, 500, arquivo='Oswald.ttf'), fill=(170, 158, 145))
    d.text((60, 360), 'DARK ART · PRETO E CINZA · COBERTURAS', font=fonte(30, 500, arquivo='Oswald.ttf'), fill=(212, 42, 30))
    d.text((60, 410), 'São José, Santa Catarina', font=fonte(30, 400, arquivo='Oswald.ttf'), fill=(170, 158, 145))
    og.save(os.path.join(SITE, 'og.jpg'), quality=86)
    print(len(dados), 'obras')


if __name__ == '__main__':
    main()
