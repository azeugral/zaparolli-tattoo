(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const ZAP = '5548998100176';
  const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const zapLink = msg => `https://wa.me/${ZAP}?text=${encodeURIComponent(msg)}`;

  const ano = $('#ano');
  if (ano) ano.textContent = new Date().getFullYear();

  /* entrada do hero depois das fontes */
  const hero = $('.hero');
  if (hero) {
    const entrar = () => requestAnimationFrame(() => hero.classList.add('entrou'));
    (document.fonts ? Promise.race([document.fonts.ready, new Promise(r => setTimeout(r, 1200))]) : Promise.resolve()).then(entrar);
  }


  /* topo: sólido depois do hero, some ao descer e volta ao subir; WhatsApp flutuante */
  const topo = $('#topo'), zap = $('.zap');
  let yAnt = scrollY, formaVista = false;
  const ficha = $('#agendar');
  if (ficha && 'IntersectionObserver' in window) {
    new IntersectionObserver(([e]) => { formaVista = e.isIntersecting; rolar(); }, { rootMargin: '0px 0px -30% 0px' }).observe(ficha);
  }
  function rolar() {
    const y = scrollY;
    const limite = hero ? hero.offsetHeight * .7 : 80;
    if (topo) {
      topo.classList.toggle('solido', y > 30 || !hero);
      const gavetaAberta = gaveta && gaveta.classList.contains('aberta');
      topo.classList.toggle('escondido', !gavetaAberta && y > limite && y > yAnt + 4);
      if (y < yAnt - 4 || y <= limite) topo.classList.remove('escondido');
    }
    zap && zap.classList.toggle('visivel', (!hero || y > limite) && !formaVista);
    yAnt = y;
  }
  addEventListener('scroll', rolar, { passive: true });

  /* link ativo no menu */
  const links = $$('.topo nav a[href^="#"]');
  if (links.length) {
    const io = new IntersectionObserver(ents => ents.forEach(e => {
      if (e.isIntersecting) links.forEach(a => a.toggleAttribute('aria-current', a.getAttribute('href') === '#' + e.target.id));
    }), { rootMargin: '-45% 0px -50% 0px' });
    $$('main section[id]').forEach(s => io.observe(s));
  }

  /* menu do celular */
  const gaveta = $('#gaveta'), menuBtn = $('.menu-btn');
  let gavetaTimer;
  function gavetaAbrir(abrir) {
    if (!gaveta) return;
    clearTimeout(gavetaTimer);
    if (abrir) {
      gaveta.hidden = false;
      requestAnimationFrame(() => requestAnimationFrame(() => gaveta.classList.add('aberta')));
      $('.fechar', gaveta).focus({ preventScroll: true });
    } else {
      gaveta.classList.remove('aberta');
      gavetaTimer = setTimeout(() => { gaveta.hidden = true; }, 420);
      menuBtn && menuBtn.focus({ preventScroll: true });
    }
    gaveta.setAttribute('aria-hidden', String(!abrir));
    menuBtn && menuBtn.setAttribute('aria-expanded', String(abrir));
    document.documentElement.style.overflow = abrir ? 'hidden' : '';
  }
  menuBtn && menuBtn.addEventListener('click', () => gavetaAbrir(true));
  gaveta && $('.fechar', gaveta).addEventListener('click', () => gavetaAbrir(false));
  gaveta && $$('a', gaveta).forEach(a => a.addEventListener('click', () => gavetaAbrir(false)));
  rolar();

  /* entradas ao rolar */
  const io = 'IntersectionObserver' in window && !reduz
    ? new IntersectionObserver(ents => ents.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('visto'); io.unobserve(e.target); }
      }), { rootMargin: '0px 0px -8% 0px' })
    : null;
  const observar = el => io ? io.observe(el) : el.classList.add('visto');
  $$('.surge').forEach(observar);

  /* vídeo da história: toca mudo (tem legenda) só quando está na tela; o botão liga o som e volta ao início */
  const vh = $('#video-historia'), somBtn = $('.som');
  if (vh) {
    let comSom = false;
    const tocar = () => { const p = vh.play(); if (p && p.catch) p.catch(() => {}); };
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(([e]) => {
        if (e.isIntersecting) { if (vh.preload === 'none') vh.preload = 'auto'; if (!reduz || comSom) tocar(); }
        else vh.pause();
      }, { threshold: .35 }).observe(vh);
    }
    somBtn && somBtn.addEventListener('click', () => {
      comSom = !comSom;
      vh.muted = !comSom;
      if (comSom) { vh.currentTime = 0; vh.loop = false; tocar(); } else vh.loop = true;
      somBtn.setAttribute('aria-pressed', String(comSom));
      $('.txt', somBtn).textContent = comSom ? 'Tirar o som' : 'Ouvir com som';
    });
    vh.addEventListener('ended', () => {
      comSom = false; vh.muted = true; vh.loop = true; tocar();
      if (somBtn) { somBtn.setAttribute('aria-pressed', 'false'); $('.txt', somBtn).textContent = 'Ouvir com som'; }
    });
  }

  /* portfólio: grade 4:5 com filtros */
  const CATS = { todos: 'Todos', dark: 'Dark art', cob: 'Coberturas', real: 'Realismo', fech: 'Fechamentos' };
  const galeria = $('#galeria');
  const obras = window.OBRAS || [];
  let visiveis = [];
  if (galeria && obras.length) {
    const limite = +galeria.dataset.limite || Infinity;
    galeria.innerHTML = obras.map((o, i) => `<button class="obra" type="button" data-c="${o.c}" data-i="${i}" aria-label="Ampliar: ${o.t}">
      <span class="moldura"><img src="assets/obras/${o.f}-640.webp" srcset="assets/obras/${o.f}-640.webp 640w, assets/obras/${o.f}-1080.webp 1080w" sizes="(max-width: 640px) 48vw, (max-width: 1100px) 32vw, 300px" alt="${o.t}" loading="lazy" decoding="async" width="640" height="800" onload="this.classList.add('carregou')"></span>
      <span class="leg"><small>${CATS[o.c]}</small><span>${o.t}</span></span></button>`).join('');
    const filtros = $('.filtros');
    filtros.innerHTML = Object.entries(CATS).map(([k, v], i) =>
      `<button type="button" data-f="${k}" aria-pressed="${i === 0}">${v}</button>`).join('');
    function filtrar(cat, animar) {
      let n = 0;
      $$('.obra', galeria).forEach(b => {
        const ok = cat === 'todos' || b.dataset.c === cat;
        const mostra = ok && n < limite;
        b.classList.toggle('oculta', !mostra);
        if (mostra) {
          if (animar && !reduz) {
            b.classList.remove('visto');
            b.style.transitionDelay = (n % 8) * 45 + 'ms';
            requestAnimationFrame(() => requestAnimationFrame(() => b.classList.add('visto')));
          }
          n++;
        }
      });
      visiveis = $$('.obra:not(.oculta)', galeria);
      $$('button', filtros).forEach(b => b.setAttribute('aria-pressed', String(b.dataset.f === cat)));
    }
    filtros.addEventListener('click', e => { const b = e.target.closest('button'); if (b) filtrar(b.dataset.f, true); });
    const inicial = new URLSearchParams(location.search).get('f');
    filtrar(CATS[inicial] ? inicial : 'todos');
    $$('.obra', galeria).forEach((b, i) => { b.style.transitionDelay = (i % 4) * 70 + 'ms'; observar(b); });
  }

  /* tela cheia: serve ao portfólio e a qualquer imagem do site.
     `lista` é [{src, alt, cat, zap}]; o portfólio monta a lista dos filtros visíveis,
     as outras imagens usam as fotos da mesma seção. */
  const luz = $('#luz'), luzImg = $('#luz-img'), luzLeg = $('#luz-leg'), luzZap = $('#luz-zap');
  let lista = [], li = 0, ultimoFoco = null, luzTimer;
  function pintarLuz() {
    const o = lista[li]; if (!o) return;
    luzImg.style.opacity = 0;
    const tmp = new Image(); tmp.src = o.src;
    const mostrar = () => { luzImg.src = o.src; luzImg.alt = o.alt; luzImg.style.opacity = 1; };
    tmp.decode ? tmp.decode().then(mostrar, mostrar) : mostrar();
    luzLeg.innerHTML = o.cat ? `<small>${o.cat}</small>${o.alt}` : o.alt;
    luz.classList.toggle('unica', lista.length < 2);
    luz.classList.toggle('sem-zap', !o.zap);
    if (luzZap && o.zap) {
      luzZap.href = zapLink(`Olá, Zapa! Vim pelo site e curti o trabalho "${o.alt}". Quero um orçamento para algo nessa linha.`);
      luzZap.target = '_blank'; luzZap.rel = 'noopener';
    }
  }
  function abrirLuz(nova, i) {
    if (!luz || i < 0 || !nova.length) return;
    clearTimeout(luzTimer);
    ultimoFoco = document.activeElement;
    lista = nova; li = i; pintarLuz();
    luz.hidden = false;
    requestAnimationFrame(() => requestAnimationFrame(() => luz.classList.add('aberta')));
    luz.setAttribute('aria-hidden', 'false');
    document.documentElement.style.overflow = 'hidden';
    $('.fechar-luz', luz).focus({ preventScroll: true });
  }
  function fecharLuz() {
    luz.classList.remove('aberta'); luz.setAttribute('aria-hidden', 'true');
    luzTimer = setTimeout(() => { luz.hidden = true; }, 360);
    document.documentElement.style.overflow = '';
    ultimoFoco && ultimoFoco.focus({ preventScroll: true });
  }
  function passo(d) { if (lista.length < 2) return; li = (li + d + lista.length) % lista.length; pintarLuz(); }
  if (galeria && obras.length) {
    galeria.addEventListener('click', e => {
      const b = e.target.closest('.obra'); if (!b) return;
      const itens = visiveis.map(v => { const o = obras[+v.dataset.i]; return { src: `assets/obras/${o.f}-1080.webp`, alt: o.t, cat: CATS[o.c], zap: true }; });
      abrirLuz(itens, visiveis.indexOf(b));
    });
  }
  /* as outras imagens: maior versão do srcset; tatuagens (pasta obras) levam o botão do WhatsApp */
  const maior = img => {
    const ss = img.getAttribute('srcset');
    if (!ss) return (img.getAttribute('src') || '').replace(/(\/obras\/z\d+)-640\.webp$/, '$1-1080.webp');
    return ss.split(',').map(x => x.trim().split(/\s+/)).sort((a, b) => parseInt(b[1]) - parseInt(a[1]))[0][0];
  };
  const alvos = $$('main img').filter(img => !img.closest('.hero, .obra, .antes-depois, .nome, .gigante, picture'));
  alvos.forEach(img => {
    const caixa = img.parentElement;
    caixa.classList.add('amplia');
    caixa.setAttribute('role', 'button'); caixa.tabIndex = 0;
    caixa.setAttribute('aria-label', 'Ampliar: ' + (img.alt || 'foto'));
    const abrir = () => {
      const sec = img.closest('section') || document.body;
      const grupo = alvos.filter(x => (x.closest('section') || document.body) === sec);
      const itens = grupo.map(x => {
        const fonte = maior(x);
        const fig = x.closest('figure'); const leg = fig && $('figcaption', fig);
        const titulo = $('.de', x.closest('article') || document.createElement('i'));
        const alt = x.alt || (titulo && titulo.textContent) || (leg && leg.textContent) || '';
        return { src: fonte, alt: alt, zap: /\/(obras|cob)\//.test(fonte) };
      });
      abrirLuz(itens, grupo.indexOf(img));
    };
    caixa.addEventListener('click', e => { if (!e.target.closest('a, button:not(.amplia)')) abrir(); });
    caixa.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); abrir(); } });
  });
  if (luz) {
    $('.fechar-luz', luz).addEventListener('click', fecharLuz);
    $('.ant', luz).addEventListener('click', () => passo(-1));
    $('.prox', luz).addEventListener('click', () => passo(1));
    luz.addEventListener('click', e => { if (e.target === luz || e.target.classList.contains('luz-palco')) fecharLuz(); });
    addEventListener('keydown', e => {
      if (e.key === 'Escape') { if (luz.classList.contains('aberta')) fecharLuz(); else if (gaveta && gaveta.classList.contains('aberta')) gavetaAbrir(false); }
      if (!luz.classList.contains('aberta')) return;
      if (e.key === 'ArrowLeft') passo(-1);
      if (e.key === 'ArrowRight') passo(1);
    });
    let x0 = null, y0 = null;
    luz.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
    luz.addEventListener('touchend', e => {
      if (x0 === null) return;
      const dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
      if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) passo(dx < 0 ? 1 : -1);
      else if (dy > 90 && Math.abs(dy) > Math.abs(dx)) fecharLuz();
      x0 = y0 = null;
    });
  }

  /* antes e depois (esquema da WRM): arrasta pela alça ou pelo palco. No toque só conta como
     arraste quando o dedo anda mais na horizontal que na vertical; rolar a página não mexe na
     divisa e um toque solto não pula. O range escondido serve ao teclado. */
  $$('[data-comparar]').forEach(fig => {
    const ctl = $('input', fig), palco = $('.antes-depois__palco', fig) || fig;
    const definir = v => { v = Math.max(0, Math.min(100, v)); ctl.value = v; fig.style.setProperty('--pos', `${v}%`); };
    ctl.addEventListener('input', () => definir(+ctl.value));
    const pela = x => { const r = palco.getBoundingClientRect(); return (x - r.left) / r.width * 100; };
    let ini = null, arrasto = false;
    palco.addEventListener('pointerdown', e => {
      ini = { x: e.clientX, y: e.clientY, id: e.pointerId, tipo: e.pointerType, alca: !!e.target.closest('.antes-depois__alca') };
      arrasto = e.pointerType === 'mouse' || ini.alca;
      if (arrasto) { palco.setPointerCapture(e.pointerId); fig.classList.add('arrastando'); definir(pela(e.clientX)); }
    });
    palco.addEventListener('pointermove', e => {
      if (!ini || e.pointerId !== ini.id) return;
      if (!arrasto) {
        const dx = Math.abs(e.clientX - ini.x), dy = Math.abs(e.clientY - ini.y);
        if (dy > 8 && dy > dx) { ini = null; return; }          // rolagem: larga
        if (dx > 10 && dx > dy * 1.4) { arrasto = true; palco.setPointerCapture(e.pointerId); fig.classList.add('arrastando'); }
        else return;
      }
      definir(pela(e.clientX));
    });
    const soltar = () => { ini = null; arrasto = false; fig.classList.remove('arrastando'); };
    palco.addEventListener('pointerup', soltar);
    palco.addEventListener('pointercancel', soltar);
    definir(+ctl.value);
    /* dica de uso: a divisa balança uma vez quando o comparador aparece */
    if ('IntersectionObserver' in window && !reduz) {
      const io = new IntersectionObserver(([en]) => {
        if (!en.isIntersecting) return;
        io.disconnect();
        setTimeout(() => definir(36), 500); setTimeout(() => definir(64), 1100); setTimeout(() => definir(50), 1700);
      }, { threshold: .6 });
      io.observe(fig);
    }
  });


  /* agendamento -> mensagem pronta no WhatsApp */
  const form = $('#agendar');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const d = new FormData(form);
      const v = k => (d.get(k) || '').toString().trim();
      const exigir = [['nome', '#f-nome'], ['ideia', '#f-ideia']];
      for (const [k, sel] of exigir) {
        const campo = $(sel).closest('.campo');
        campo.classList.toggle('erro', !v(k));
        if (!v(k)) { $(sel).focus(); return; }
      }
      const alt = v('altura').replace(/\D/g, ''), larg = v('largura').replace(/\D/g, '');
      const tamanho = alt || larg ? `${alt || '?'} x ${larg || '?'} cm` : 'Ainda não sei';
      const msg = [
        `Olá, Zapa! Sou ${v('nome')}${v('cidade') ? `, de ${v('cidade')}` : ''}, e vim pelo site.`, '',
        `*Quero:* ${v('tipo')}`,
        `*Local do corpo:* ${v('local')}`,
        `*Tamanho aproximado:* ${tamanho}`,
        `*Estilo:* ${v('estilo')}`,
        `*Quando:* ${v('quando')}`, '',
        `*Ideia:* ${v('ideia')}`, '',
        'Vou mandar a foto do local demarcado e as referências aqui na conversa.',
      ].join('\n');
      form.classList.remove('enviada'); void form.offsetWidth; form.classList.add('enviada');
      window.open(zapLink(msg), '_blank', 'noopener');
    });
    $$('input, textarea', form).forEach(el => el.addEventListener('input', () => el.closest('.campo').classList.remove('erro')));
  }
})();
