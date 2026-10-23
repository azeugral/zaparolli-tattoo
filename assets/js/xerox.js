/* Fundo do hero (v2): a arte das costas do Zapa como cópia de xerox chiada, na linha do
   v1 do Samtto. Cópia em branco e cinza, uma segunda cópia em vermelho fora de registro,
   grão que muda em saltos, linhas de varredura e cortes horizontais de vez em quando.
   `a` é a fase do loop (0 a 2π, só mexe na respiração da imagem) e `p` é o passo do chiado
   (inteiro: cada passo sorteia um grão novo). Usado ao vivo no desktop e por
   tools/gerar_video.py para os MP4 do celular. */
window.XEROX_FS = `precision highp float;
uniform vec2 r;uniform float a;uniform float p;uniform float ta;uniform sampler2D t;
float h(vec2 q){return fract(sin(dot(q,vec2(127.1,311.7)))*43758.5453);}
float h1(float x){return fract(sin(x*91.17+7.3)*43758.5453);}
float asp;
float img(vec2 q){
  bool deitado=asp>1.05;
  float H=(deitado?1.12:.80)*(1.+.012*sin(a));
  vec2 centro=deitado?vec2(asp*.70,.5):vec2(asp*.5,.64);
  vec2 u=(q-centro)/vec2(ta*H,H)+.5;
  if(u.x<0.||u.x>1.||u.y<0.||u.y>1.)return 0.;
  float l=texture2D(t,vec2(u.x,1.-u.y)).r;
  float borda=smoothstep(0.,deitado?.3:.1,u.x)*smoothstep(1.,.9,u.x)*smoothstep(0.,.14,u.y)*smoothstep(1.,.86,u.y);
  return l*borda;
}
void main(){
  asp=r.x/r.y;
  bool deitado=asp>1.05;
  vec2 px=gl_FragCoord.xy, uv=px/r.y;
  float fx=uv.x/asp;
  /* cortes horizontais: só em alguns passos, em algumas faixas */
  float faixa=floor(px.y/(r.y*.028));
  float corte=step(.9,h1(faixa*1.31+p*7.13))*step(.72,h1(p*3.37));
  float desl=(h1(faixa*2.7+p)-.5)*.07*corte;
  vec2 tremor=vec2(h1(p*1.71)-.5,h1(p*2.93)-.5)*.0035;
  vec2 q=uv+tremor+vec2(desl,0.);
  float l=img(q);
  float lv=img(q+vec2(.014,-.009)+tremor*2.);
  /* cópia de xerox: limiar com grão grosso que muda a cada passo */
  vec2 gp=floor(px/1.7);
  float n=h(gp+p*13.7), n2=h(gp*1.37+p*5.11);
  float limiar=.30+.34*n;
  float branco=smoothstep(.0,.06,l*1.3-limiar);
  float cinza=smoothstep(.0,.06,l*1.3-(limiar-.16))*(1.-branco);
  float verm=smoothstep(.0,.07,lv*1.25-(.34+.34*n2));
  /* escurece onde fica o texto */
  float area=deitado?mix(.14,1.,smoothstep(.2,.6,fx)):mix(.1,.95,smoothstep(.36,.74,uv.y));
  vec2 vc=gl_FragCoord.xy/r-.5; float vinheta=1.-.85*dot(vc,vc);
  vec3 col=vec3(.042);
  col=mix(col,vec3(.80,.12,.08),verm*.8*area*vinheta);
  col=mix(col,vec3(.50),cinza*.85*area*vinheta);
  col=mix(col,vec3(.88,.88,.86),branco*area*vinheta);
  /* chiado: pontos soltos, varredura e um véu que pisca */
  float pontos=step(.986,h(floor(px/1.5)*.71+p*3.1));
  float grao=(h(floor(px/1.2)*.37+p*1.3)-.5)*.07;
  float varre=.035*step(.5,fract(px.y/3.))+.05*smoothstep(.0,.02,abs(fract(uv.y*.5-p*.037)-.5)-.48);
  float pisca=.015*h1(p*9.7);
  col+=vec3(pontos*.3+pisca+grao)*vinheta;
  col-=varre*.5;
  col+=corte*.025*step(.5,h1(faixa+p*1.9));
  gl_FragColor=vec4(clamp(col,0.,1.),1.);
}`;

/* Liga o shader num canvas com a foto já carregada. Devolve {desenhar(fase, passo)} ou null. */
window.xeroxGL = function (tela, foto, opcoes) {
  const gl = tela.getContext('webgl', Object.assign({ antialias: false, powerPreference: 'low-power' }, opcoes || {}));
  if (!gl) return null;
  const sh = (tipo, src) => { const o = gl.createShader(tipo); gl.shaderSource(o, src); gl.compileShader(o); return gl.getShaderParameter(o, gl.COMPILE_STATUS) ? o : null; };
  const v = sh(gl.VERTEX_SHADER, 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}');
  const f = sh(gl.FRAGMENT_SHADER, window.XEROX_FS);
  if (!v || !f) return null;
  const pr = gl.createProgram(); gl.attachShader(pr, v); gl.attachShader(pr, f); gl.linkProgram(pr);
  if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) return null;
  gl.useProgram(pr);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const lp = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(lp); gl.vertexAttribPointer(lp, 2, gl.FLOAT, false, 0, 0);
  const tex = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, tex);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.LUMINANCE, gl.LUMINANCE, gl.UNSIGNED_BYTE, foto);
  const u = n => gl.getUniformLocation(pr, n);
  const uR = u('r'), uA = u('a'), uP = u('p');
  gl.uniform1i(u('t'), 0);
  gl.uniform1f(u('ta'), foto.width / foto.height);
  return {
    desenhar(fase, passo) {
      gl.viewport(0, 0, tela.width, tela.height);
      gl.uniform2f(uR, tela.width, tela.height);
      gl.uniform1f(uA, fase);
      gl.uniform1f(uP, passo % 997);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    }
  };
};
