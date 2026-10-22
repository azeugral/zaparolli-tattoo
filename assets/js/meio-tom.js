/* Fundo do hero: a foto das costas em meio-tom (o pontilhado dos posts fixados),
   com uma fumaça lenta que engorda e afina os pontos. Usado ao vivo no desktop e por
   tools/gerar_video.py para o MP4 do celular. `a` é a fase do loop (0 a 2π) e `k` o raio
   do movimento: o quadro em a = 2π é igual ao de a = 0, então o vídeo fecha sem emenda. */
window.MEIOTOM_FS = `precision highp float;
uniform vec2 r;uniform float a;uniform float k;uniform float c;uniform float ta;uniform sampler2D t;
float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);
return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}
float fbm(vec2 p){float v=0.,b=.5;mat2 R=mat2(.8,.6,-.6,.8);for(int i=0;i<5;i++){v+=b*n(p);p=R*p*2.03;b*=.5;}return v;}
void main(){
  float asp=r.x/r.y;
  const float s=.70710678;
  vec2 px=gl_FragCoord.xy;
  vec2 g=vec2(s*px.x+s*px.y,-s*px.x+s*px.y)/c;
  vec2 cel=floor(g)+.5, fr=g-cel;
  vec2 cp=c*vec2(s*cel.x-s*cel.y,s*cel.x+s*cel.y);
  vec2 p=cp/r.y;
  bool deitado=asp>1.05;
  float H=deitado?1.12:.78;
  H*=1.+.025*sin(a);
  vec2 centro=deitado?vec2(asp*.70,.5):vec2(asp*.5,.66);
  vec2 u=(p-centro)/vec2(ta*H,H)+.5;
  float lum=0.;
  if(u.x>0.&&u.x<1.&&u.y>0.&&u.y<1.)lum=texture2D(t,vec2(u.x,1.-u.y)).r;
  float borda=smoothstep(0.,deitado?.32:.12,u.x)*smoothstep(1.,deitado?.9:.88,u.x)*smoothstep(0.,.14,u.y)*smoothstep(1.,.86,u.y);
  lum*=borda;
  vec2 o1=vec2(cos(a),sin(a))*k, o2=vec2(sin(a),cos(a))*k*.8;
  vec2 q=vec2(fbm(p*1.5+o1),fbm(p*1.5+vec2(4.1,2.7)-o2));
  float fum=fbm(p*1.25+2.2*q+o2*.6);
  float v=lum*(.62+.75*fum)+smoothstep(.45,.95,fum)*.22;
  if(deitado)v*=mix(.32,1.,smoothstep(asp*.18,asp*.58,p.x));
  else v*=mix(.16,.95,smoothstep(.28,.72,p.y));
  vec2 vc=gl_FragCoord.xy/r-.5; v*=1.-.9*dot(vc*vec2(.9,1.),vc*vec2(.9,1.));
  v=clamp(v,0.,1.);
  float raio=sqrt(v)*.66;
  float aa=1.4/c;
  float pt=smoothstep(raio+aa*.5,raio-aa*.5,length(fr));
  vec3 osso=vec3(.92,.88,.81), sep=vec3(.55,.41,.31);
  vec3 tinta=mix(sep,osso,smoothstep(.15,.85,v));
  vec3 fundo=vec3(.045,.037,.032)+(h(px+fract(a))-.5)*.018;
  float dobra=exp(-pow((gl_FragCoord.y/r.y-.47)*r.y/2.2,2.))*.05;
  vec3 col=mix(fundo,tinta,pt*.9)+dobra;
  gl_FragColor=vec4(col,1.);
}`;

/* Liga o shader num canvas com a foto já carregada. Devolve {desenhar(fase, raio)} ou null. */
window.meioTomGL = function (tela, foto, opcoes) {
  const gl = tela.getContext('webgl', Object.assign({ antialias: false, powerPreference: 'low-power' }, opcoes || {}));
  if (!gl) return null;
  const sh = (tipo, src) => { const o = gl.createShader(tipo); gl.shaderSource(o, src); gl.compileShader(o); return gl.getShaderParameter(o, gl.COMPILE_STATUS) ? o : null; };
  const v = sh(gl.VERTEX_SHADER, 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}');
  const f = sh(gl.FRAGMENT_SHADER, window.MEIOTOM_FS);
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
  const uR = u('r'), uA = u('a'), uK = u('k'), uC = u('c'), uTa = u('ta');
  gl.uniform1i(u('t'), 0);
  gl.uniform1f(uTa, foto.width / foto.height);
  return {
    desenhar(fase, raio, celula) {
      gl.viewport(0, 0, tela.width, tela.height);
      gl.uniform2f(uR, tela.width, tela.height);
      gl.uniform1f(uA, fase);
      gl.uniform1f(uK, raio);
      gl.uniform1f(uC, celula || 7);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    }
  };
};
