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

  /* fundo do hero: a arte das costas, sem interação. Padrão: meio-tom fino com fumaça
     vermelha (meio-tom.js); ?hero=xerox mostra o xerox chiado (xerox.js), guardado.
     Desktop: WebGL ao vivo. Toque/celular: MP4 renderizado do mesmo shader. */
  const tela = $('#meio-tom'), video = $('#meio-tom-video');
  const MEIOTOM = new URLSearchParams(location.search).get('hero') !== 'xerox';
  if (!MEIOTOM && video) {
    video.poster = 'assets/img/xerox-poster.webp';
    video.dataset.emPe = 'assets/video/xerox-celular.mp4';
    video.dataset.deitado = 'assets/video/xerox-deitado.mp4';
    if (hero) hero.style.backgroundImage = 'url(assets/img/xerox-poster.webp)';
  }
  const celular = matchMedia('(max-width: 760px), (hover: none) and (pointer: coarse)');
  const deitado = matchMedia('(orientation: landscape)');
  let glAtivo = false, videoAtivo = false;
  const ouvir = (mq, fn) => mq.addEventListener ? mq.addEventListener('change', fn) : mq.addListener(fn);
  function escolherFundo() {
    if (!hero) return;
    if (celular.matches) { if (!videoAtivo) iniciarVideo(); }
    else if (!glAtivo) iniciarShader();
  }
  function iniciarVideo() {
    if (!video) return;
    videoAtivo = true;
    video.muted = true;
    video.preload = 'auto';
    video.addEventListener('playing', () => video.classList.add('pronto'), { once: true });
    trocarVideo();
    ouvir(deitado, trocarVideo);
  }
  function trocarVideo() {
    const src = deitado.matches ? video.dataset.deitado : video.dataset.emPe;
    if (video.getAttribute('src') !== src) {
      const t = video.currentTime || 0;
      video.src = src;
      video.addEventListener('loadedmetadata', () => { try { video.currentTime = t % (video.duration || 12); } catch (e) {} }, { once: true });
    }
    const p = video.play();
    if (p && p.catch) p.catch(() => {});
  }
  function iniciarShader() {
    const criar = MEIOTOM ? window.meioTomGL : window.xeroxGL;
    if (!tela || !criar) return;
    glAtivo = true;
    const foto = new Image();
    foto.onload = () => {
      const t = criar(tela, foto);
      if (!t) return;
      const PERIODO = 18, RAIO = .45, QPS = 12;
      /* o xerox fica em 1x de propósito: o grão chiado é mais grosso e pesa menos */
      const dpr = MEIOTOM ? Math.min(devicePixelRatio || 1, 2) : 1;
      function medir() {
        const w = Math.max(1, Math.round(tela.clientWidth * dpr)), h = Math.max(1, Math.round(tela.clientHeight * dpr));
        if (tela.width !== w || tela.height !== h) { tela.width = w; tela.height = h; }
      }
      medir(); addEventListener('resize', medir);
      let visivel = true, ultimo = -1;
      new IntersectionObserver(([e]) => { visivel = e.isIntersecting; }).observe(hero);
      const t0 = performance.now();
      function quadro(agora) {
        if (visivel && !celular.matches && !document.hidden) {
          const seg = reduz ? 1 : (agora - t0) / 1000;
          const fase = (seg / PERIODO) * Math.PI * 2;
          if (MEIOTOM) { medir(); t.desenhar(fase, RAIO, 3.2 * dpr); }
          else {
            const passo = Math.floor(seg * QPS);
            if (passo !== ultimo) { ultimo = passo; medir(); t.desenhar(fase, passo); }
          }
          tela.classList.add('pronto');
        }
        if (!reduz) requestAnimationFrame(quadro);
      }
      requestAnimationFrame(quadro);
    };
    foto.src = 'assets/img/meio-tom-fonte.jpg';
  }
  escolherFundo();
  ouvir(celular, escolherFundo);

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
      <span class="moldura"><img src="assets/obras/${o.f}-640.webp" alt="${o.t}" loading="lazy" decoding="async" width="640" height="800"></span>
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
    galeria.addEventListener('click', e => { const b = e.target.closest('.obra'); if (b) abrirLuz(visiveis.indexOf(b)); });
  }

  /* tela cheia */
  const luz = $('#luz'), luzImg = $('#luz-img'), luzLeg = $('#luz-leg'), luzZap = $('#luz-zap');
  let li = 0, ultimoFoco = null, luzTimer;
  function pintarLuz() {
    const b = visiveis[li]; if (!b) return;
    const o = obras[+b.dataset.i];
    luzImg.style.opacity = 0;
    const src = `assets/obras/${o.f}-1080.webp`;
    const tmp = new Image(); tmp.src = src;
    const mostrar = () => { luzImg.src = src; luzImg.alt = o.t; luzImg.style.opacity = 1; };
    tmp.decode ? tmp.decode().then(mostrar, mostrar) : mostrar();
    luzLeg.innerHTML = `<small>${CATS[o.c]}</small>${o.t}`;
    if (luzZap) {
      luzZap.href = zapLink(`Olá, Zapa! Vim pelo site e curti o trabalho "${o.t}". Quero um orçamento para algo nessa linha.`);
      luzZap.target = '_blank'; luzZap.rel = 'noopener';
    }
  }
  function abrirLuz(i) {
    if (!luz || i < 0) return;
    clearTimeout(luzTimer);
    ultimoFoco = document.activeElement;
    li = i; pintarLuz();
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
  function passo(d) { li = (li + d + visiveis.length) % visiveis.length; pintarLuz(); }
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
