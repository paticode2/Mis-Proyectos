# Arma vivo.template.html a partir de archivo.template.html: misma web Archivo, más sigilos
# rosa (cybersigilism) que crecen y se borran, letras que cambian con el ritmo, líneas de construcción y sonido generado en la página.
# Uso (desde 06-web/sitio): python3 vivo_from_archivo.py && python3 page_build.py vivo [salida.html]
t = open("archivo.template.html").read()

def rep(a, b):
    global t
    assert t.count(a) == 1, a[:60]
    t = t.replace(a, b)

rep("<title>Patricia · Archivo</title>", "<title>Patricia · Archivo en vivo</title>")
rep("family=Arimo:wght@400;700&display=swap", "family=Arimo:wght@400;700&family=UnifrakturMaguntia&display=swap")

rep("</style>", """
/* ---------- en vivo: pintura, retícula, sonido ---------- */
:root{--rosa:#E0508C;--rosa-luz:#FFC4DA;--hair:#9A9A9A}
#paint{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:20;mix-blend-mode:multiply}
.cover-art{position:relative}
.wip{display:flex;justify-content:space-between;gap:8px;font-size:10px;color:var(--grey);border-bottom:1px solid var(--hair);padding-bottom:4px;margin-bottom:6px;white-space:nowrap;overflow:hidden}
.wip span:first-child{overflow:hidden;text-overflow:ellipsis}
.ruler{height:8px;margin-bottom:6px;background:repeating-linear-gradient(90deg,var(--hair) 0 1px,transparent 1px 10px) bottom/100% 4px no-repeat,repeating-linear-gradient(90deg,var(--hair) 0 1px,transparent 1px 50px) bottom/100% 8px no-repeat}
.cover-art .stage{position:relative}
.cover-art svg.construct{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.construct line,.construct rect,.construct circle{fill:none;stroke:var(--hair);stroke-width:.6;vector-effect:non-scaling-stroke}
.construct .node{fill:var(--paper);stroke:#E0508C}
.sound{position:fixed;z-index:30;right:max(16px,env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));
  display:flex;align-items:center;gap:10px;background:var(--paper);color:var(--ink);border:1px solid var(--ink);
  font:700 13px/1 var(--grot);padding:10px 14px;cursor:pointer;box-shadow:4px 4px 0 var(--rosa)}
.sound:hover{background:var(--ink);color:var(--paper)}
.sound .bars{display:flex;align-items:flex-end;gap:2px;height:14px}
.sound .bars i{width:3px;height:3px;background:currentColor;transition:height .08s}
.sound[aria-pressed="true"]{background:var(--rosa);color:var(--ink);border-color:var(--ink)}
.work .im canvas{transition:filter .1s}
.work.hit .im canvas{filter:invert(1)}
</style>""")

rep("""  <div class="page">
    <canvas id="glitch" role="img" aria-label="El nombre Patricia Díaz repetido en cascada, cortado y pixelado"></canvas>
  </div>""", """  <div class="page cover-art">
    <div class="wip"><span>PatriciaDiaz_Archivo_2026_WIP_5.ai @ 25 % (RGB/Contorno)</span><span>Caguas, PR</span></div>
    <div class="ruler" aria-hidden="true"></div>
    <div class="stage">
      <canvas id="glitch" role="img" aria-label="El nombre Patricia Díaz en letras gigantes que cambian de forma, cortadas y pixeladas"></canvas>
      <svg class="construct" viewBox="0 0 400 500" preserveAspectRatio="none" aria-hidden="true">
        <rect x="18" y="22" width="364" height="456"/><rect x="58" y="70" width="284" height="210"/><rect x="40" y="300" width="150" height="160"/><rect x="210" y="300" width="150" height="160"/>
        <line x1="18" y1="22" x2="382" y2="478"/><line x1="382" y1="22" x2="18" y2="478"/><line x1="58" y1="70" x2="342" y2="280"/><line x1="342" y1="70" x2="58" y2="280"/>
        <line x1="200" y1="0" x2="200" y2="500"/><line x1="0" y1="290" x2="400" y2="290"/><line x1="40" y1="460" x2="360" y2="300"/><line x1="40" y1="300" x2="360" y2="460"/>
        <circle class="node" cx="200" cy="175" r="3"/><circle class="node" cx="200" cy="290" r="3"/><circle class="node" cx="115" cy="380" r="3"/><circle class="node" cx="285" cy="380" r="3"/><circle class="node" cx="18" cy="22" r="3"/><circle class="node" cx="382" cy="478" r="3"/>
      </svg>
    </div>
  </div>""")

rep("<script>", """<canvas id="paint" aria-hidden="true"></canvas>
<button class="sound" id="sound" type="button" aria-pressed="false"><span class="bars" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span><span id="soundlabel">Sonido</span></button>

<script>""")

# the cover glitch becomes a function of (seed, mode) so it can change on the beat
start = t.index("// cover: the name falling")
end = t.index("// contact: the address block")
t = t[:start] + r"""// cover: giant letters that change shape on the beat, then sliced, shifted and pixelated.
// mode 0 = the name falling down the page; mode 1 = a grid of huge letters, some in blackletter, some mirrored
const FRAK = '"UnifrakturMaguntia", serif', GROT = 'Arimo, Helvetica, Arial, sans-serif';
function glitch(seed = 5, mode = 0){
  const c = document.getElementById("glitch"); const dpr = Math.min(2, devicePixelRatio || 1);
  const [W, H] = fitCanvas(c, dpr); const g = c.getContext("2d"), R = rng(seed);
  g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = "#fff"; g.fillRect(0, 0, W, H); g.fillStyle = "#0A0A0A"; g.textBaseline = "top";
  if (mode === 0){
    const fs = W * .125; g.font = `700 ${fs}px ${GROT}`;
    const words = ["Patricia", "Díaz", "(01)", "Patricia", "Díaz"];
    for (let i = 0; i < 30; i++){
      const tt = i / 29, y = tt * (H - fs) + (R() - .5) * fs * .3;
      const x = W * (.42 - .3 * Math.sin(tt * Math.PI * 1.15)) + (R() - .5) * W * .22;
      g.fillText(words[i % words.length], x, y);
    }
  } else {
    const letters = [..."PATRICIADÍAZ"], cols = 3, rows = 4, cw = W / cols, ch = H / rows;
    const off = Math.floor(R() * letters.length);
    for (let r = 0; r < rows; r++) for (let k = 0; k < cols; k++){
      const L = letters[(off + r * cols + k) % letters.length], frak = R() < .45;
      g.save(); g.textBaseline = "middle"; g.textAlign = "center";
      g.font = frak ? `${ch * 1.15}px ${FRAK}` : `700 ${ch * 1.05}px ${GROT}`;
      g.translate(k * cw + cw / 2 + (R() - .5) * cw * .25, r * ch + ch / 2);
      if (R() < .3) g.scale(-1, 1);
      g.scale(1 + R() * .5, 1);
      g.fillText(L, 0, 0); g.restore();
      if (R() < .35){ const s = ch * .22, x = k * cw + R() * cw, y = r * ch + R() * ch; g.fillRect(x - s / 2, y - s / 10, s, s / 5); g.fillRect(x - s / 10, y - s / 2, s / 5, s); }
    }
  }
  // horizontal tears
  for (let y = 0; y < H; ){
    const h = Math.round((3 + R() * 22) * dpr);
    if (R() < .3){ const dx = Math.round((R() - .5) * W * .16); const strip = g.getImageData(0, y, W, h); g.fillStyle = "#fff"; g.fillRect(0, y, W, h); g.putImageData(strip, dx, y); }
    y += h;
  }
  // blocky patches
  const tmp = document.createElement("canvas"), tg = tmp.getContext("2d");
  for (let k = 0; k < 22; k++){
    const bw = Math.round((30 + R() * 140) * dpr), bh = Math.round((8 + R() * 40) * dpr);
    const x = Math.round(R() * (W - bw)), y = Math.round(R() * (H - bh)), f = 5 + Math.round(R() * 6);
    tmp.width = Math.max(1, bw / f | 0); tmp.height = Math.max(1, bh / f | 0);
    tg.imageSmoothingEnabled = true; tg.drawImage(c, x, y, bw, bh, 0, 0, tmp.width, tmp.height);
    g.imageSmoothingEnabled = false; g.drawImage(tmp, 0, 0, tmp.width, tmp.height, x, y, bw, bh);
  }
  // back to pure black and white
  const id = g.getImageData(0, 0, W, H), d = id.data;
  for (let i = 0; i < d.length; i += 4){ const v = lum(d, i) < .55 ? 10 : 255; d[i] = d[i+1] = d[i+2] = v; }
  g.putImageData(id, 0, 0);
}

""" + t[end:]

rep("  glitch(); fitGiant();", "  glitch(5, 0); fitGiant();")

rep("""    f.innerHTML = `<div class="im">""", """    f.addEventListener("pointerenter", () => { blip(); f.classList.add("hit"); setTimeout(() => f.classList.remove("hit"), 90); });
    f.innerHTML = `<div class="im">""")

# new behaviour appended at the end of the script
t = t[:t.rindex("</script>")] + r"""
// ---------- cybersigils: sharp, mirrored, thorny line marks that grow, hold and fade ----------
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const paint = document.getElementById("paint"), pg = paint.getContext("2d");
let PW = 0, PH = 0;
function sizePaint(){ const d = Math.min(2, devicePixelRatio || 1); PW = innerWidth; PH = innerHeight; paint.width = PW * d; paint.height = PH * d; pg.setTransform(d, 0, 0, d, 0, 0); }
sizePaint(); addEventListener("resize", () => { sizePaint(); if (reduce) drawSigils(performance.now() / 1000); });
let sigSeed = 101;
const sigils = [];
const cubic = (p, t) => { const u = 1 - t; return [u*u*u*p[0][0] + 3*u*u*t*p[1][0] + 3*u*t*t*p[2][0] + t*t*t*p[3][0], u*u*u*p[0][1] + 3*u*u*t*p[1][1] + 3*u*t*t*p[2][1] + t*t*t*p[3][1]]; };
function makeSigil(x, y, s){
  const R = rng(sigSeed += 13), strokes = [];
  // the spine: one vertical stroke, thick in the middle and sharp at both ends
  const sw = (R() - .5) * s * .25;
  strokes.push({ p: [[0, -s], [sw, -s * .3], [-sw, s * .3], [0, s]], W: s * (.035 + R() * .03), spine: true, thorns: [] });
  // arms that leave the spine, curl outward and end in a sharp tip; each one is mirrored
  const n = 3 + Math.floor(R() * 3);
  for (let i = 0; i < n; i++){
    const y0 = (R() - .5) * 1.5 * s, dir = R() < .5 ? -1 : 1;
    const p = [[s * .02, y0], [s * (.25 + R() * .5), y0 + dir * R() * s * .5], [s * (.5 + R() * .6), y0 - dir * R() * s * .9], [s * (.25 + R() * .95), y0 + (R() - .5) * s * 1.7]];
    const thorns = []; const k = Math.floor(R() * 4);
    for (let j = 0; j < k; j++) thorns.push({ t: .25 + R() * .55, len: s * (.07 + R() * .16), side: R() < .5 ? -1 : 1 });
    const W = s * (.025 + R() * .045);
    strokes.push({ p, W, thorns }, { p: p.map(([a, b]) => [-a, b]), W, thorns: thorns.map(h => ({ ...h, side: -h.side })) });
  }
  return { x, y, s, rot: (R() - .5) * .35, strokes, born: performance.now() / 1000, grow: .55, hold: 2.2 + R() * 1.6, fade: 1.1, ink: R() < .22 ? "#0A0A0A" : "#E0508C" };
}
function drawStroke(st, prog){
  const N = 34, L = [], Rr = [], pts = [];
  for (let i = 0; i <= N; i++){ const t = i / N * prog; pts.push([t, cubic(st.p, t)]); }
  for (let i = 0; i <= N; i++){
    const [t, [x, y]] = pts[i], [, [x2, y2]] = pts[Math.min(N, i + 1)], [, [x0, y0]] = pts[Math.max(0, i - 1)];
    let tx = x2 - x0, ty = y2 - y0; const l = Math.hypot(tx, ty) || 1; tx /= l; ty /= l;
    const w = st.spine ? st.W * Math.pow(Math.sin(Math.PI * t), .8) : st.W * Math.pow(1 - t, .9) * Math.min(1, t * 7 + .25);
    L.push([x - ty * w, y + tx * w]); Rr.push([x + ty * w, y - tx * w]);
  }
  pg.beginPath(); pg.moveTo(L[0][0], L[0][1]); L.forEach(q => pg.lineTo(q[0], q[1])); for (let i = Rr.length - 1; i >= 0; i--) pg.lineTo(Rr[i][0], Rr[i][1]); pg.closePath(); pg.fill();
  for (const h of st.thorns){
    if (h.t > prog) continue;
    const [x, y] = cubic(st.p, h.t), [x2, y2] = cubic(st.p, Math.min(1, h.t + .02));
    let tx = x2 - x, ty = y2 - y; const l = Math.hypot(tx, ty) || 1; tx /= l; ty /= l;
    const b = st.W * .9, nx = -ty * h.side, ny = tx * h.side;
    pg.beginPath(); pg.moveTo(x - tx * b, y - ty * b); pg.lineTo(x + nx * h.len + tx * h.len * .45, y + ny * h.len + ty * h.len * .45); pg.lineTo(x + tx * b, y + ty * b); pg.closePath(); pg.fill();
  }
}
function drawSigils(now){
  pg.clearRect(0, 0, PW, PH);
  for (let i = sigils.length - 1; i >= 0; i--){
    const g = sigils[i], a = now - g.born;
    const prog = reduce ? 1 : Math.min(1, 1 - Math.pow(1 - Math.min(1, a / g.grow), 3));
    const alpha = reduce ? 1 : a < g.grow + g.hold ? 1 : 1 - (a - g.grow - g.hold) / g.fade;
    if (alpha <= 0){ sigils.splice(i, 1); continue; }
    pg.save(); pg.globalAlpha = alpha * .95; pg.fillStyle = g.ink; pg.translate(g.x, g.y); pg.rotate(g.rot);
    g.strokes.forEach(st => drawStroke(st, prog)); pg.restore();
  }
}
const SR = rng(77);
function spawnSigil(big){
  const k = Math.max(.55, Math.min(1, PW / 1100)), s = (big ? 120 + SR() * 110 : 55 + SR() * 90) * k;   // smaller on phones
  sigils.push(makeSigil(SR() * PW, SR() * PH, s)); if (sigils.length > 10) sigils.shift();
}

// ---------- the beat: visuals follow it, with or without sound ----------
const BPM = 140, STEP = 60 / BPM / 4;          // 16th notes
let gSeed = 5, gMode = 0, beatCount = 0;
function onBeat(step){
  if (step % 4 === 0) spawnSigil(step === 0);
  if (step % 8 === 0){ beatCount++; gSeed += 7; gMode = beatCount % 3 === 0 ? 0 : 1; glitch(gSeed, gMode); }
}
let silentStep = 0, silentTimer = null;
function silentClock(){ silentTimer = setInterval(() => { onBeat(silentStep); silentStep = (silentStep + 4) % 16; }, STEP * 4 * 1000 * 2); }
function loop(){ if (!document.hidden) drawSigils(performance.now() / 1000); requestAnimationFrame(loop); }
for (let i = 0; i < 4; i++) spawnSigil(i === 0);
if (reduce){ drawSigils(performance.now() / 1000); }
else { requestAnimationFrame(loop); silentClock(); }

// ---------- sound: a 140 bpm loop in the spirit of Crystal Castles / Snow Strippers, made in the page ----------
// distorted four-on-the-floor kick, claps, open hats, a pumping supersaw pad drowned in reverb,
// a bit-crushed square arpeggio with echo, and an offbeat saw bass. No audio files.
let AC = null, master, analyser, padBus, arpBus, verb, nextTime = 0, step16 = 0, bar = 0, timer = null, playing = false, noiseBuf;
const N = m => 440 * Math.pow(2, (m - 69) / 12);
const PROG = [[54, 57, 61], [50, 54, 57], [57, 61, 64], [52, 56, 59]];   // F#m · D · A · E
const ARP = [0, 1, 2, 3, 2, 1, 0, 2, 1, 3, 2, 1, 0, 1, 2, 3];
function crusher(levels){ const sh = AC.createWaveShaper(), c = new Float32Array(2048); for (let i = 0; i < 2048; i++){ const x = i / 1024 - 1; c[i] = Math.round(Math.tanh(x * 1.6) * levels) / levels; } sh.curve = c; return sh; }
function setupAudio(){
  AC = new (window.AudioContext || window.webkitAudioContext)();
  const comp = AC.createDynamicsCompressor(); comp.threshold.value = -16; comp.ratio.value = 6;
  master = AC.createGain(); master.gain.value = .5;
  const lofi = crusher(28), lp = AC.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 9000;
  analyser = AC.createAnalyser(); analyser.fftSize = 64;
  master.connect(lofi); lofi.connect(comp); comp.connect(lp); lp.connect(analyser); analyser.connect(AC.destination);
  // long dark reverb made from decaying noise
  verb = AC.createConvolver(); const len = AC.sampleRate * 2.8, ir = AC.createBuffer(2, len, AC.sampleRate);
  for (let ch = 0; ch < 2; ch++){ const d = ir.getChannelData(ch); for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 2.6); }
  verb.buffer = ir; const vg = AC.createGain(); vg.gain.value = .55; verb.connect(vg); vg.connect(master);
  padBus = AC.createGain(); padBus.connect(master); padBus.connect(verb);
  // arp: crushed square with a dotted-eighth echo
  arpBus = AC.createGain(); arpBus.gain.value = .5; const cr = crusher(6), dl = AC.createDelay(1), fb = AC.createGain();
  dl.delayTime.value = STEP * 3; fb.gain.value = .38; arpBus.connect(cr); cr.connect(master); cr.connect(dl); dl.connect(fb); fb.connect(dl); dl.connect(verb); dl.connect(master);
  noiseBuf = AC.createBuffer(1, AC.sampleRate, AC.sampleRate); const nd = noiseBuf.getChannelData(0); for (let i = 0; i < nd.length; i++) nd[i] = Math.random() * 2 - 1;
}
function env(gn, t, a, peak, d){ gn.gain.setValueAtTime(0, t); gn.gain.linearRampToValueAtTime(peak, t + a); gn.gain.exponentialRampToValueAtTime(.0008, t + a + d); }
function kick(t){
  const o = AC.createOscillator(), g = AC.createGain(), dist = crusher(10);
  o.frequency.setValueAtTime(160, t); o.frequency.exponentialRampToValueAtTime(44, t + .14); env(g, t, .001, 1, .3);
  o.connect(dist); dist.connect(g); g.connect(master); o.start(t); o.stop(t + .4);
  // sidechain: the pad ducks on every kick
  padBus.gain.cancelScheduledValues(t); padBus.gain.setValueAtTime(.12, t); padBus.gain.linearRampToValueAtTime(1, t + STEP * 3.2);
}
function noise(t, type, f, q, peak, d, dest = master){ const s = AC.createBufferSource(), b = AC.createBiquadFilter(), g = AC.createGain(); s.buffer = noiseBuf; b.type = type; b.frequency.value = f; b.Q.value = q; env(g, t, .001, peak, d); s.connect(b); b.connect(g); g.connect(dest); s.start(t); s.stop(t + d + .05); }
function clap(t){ [0, .012, .024].forEach(o => noise(t + o, "bandpass", 1500, 1.2, .55, .05)); noise(t + .03, "bandpass", 1300, .8, .35, .16, verb); }
function pad(t, chord, dur){
  const f = AC.createBiquadFilter(), g = AC.createGain(); f.type = "lowpass"; f.frequency.value = 2400; f.Q.value = 2;
  g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(.075, t + .04); g.gain.setValueAtTime(.075, t + dur - .05); g.gain.linearRampToValueAtTime(0, t + dur);
  chord.forEach(m => [-14, -7, 0, 7, 14].forEach(dt => { const o = AC.createOscillator(); o.type = "sawtooth"; o.frequency.value = N(m); o.detune.value = dt; o.connect(f); o.start(t); o.stop(t + dur + .02); }));
  f.connect(g); g.connect(padBus);
}
function arp(t, m){ const o = AC.createOscillator(), g = AC.createGain(); o.type = "square"; o.frequency.value = N(m); env(g, t, .002, .16, STEP * .9); o.connect(g); g.connect(arpBus); o.start(t); o.stop(t + STEP); }
function bass(t, m){ const o = AC.createOscillator(), f = AC.createBiquadFilter(), g = AC.createGain(); o.type = "sawtooth"; o.frequency.value = N(m - 24); f.type = "lowpass"; f.frequency.setValueAtTime(900, t); f.frequency.exponentialRampToValueAtTime(160, t + STEP * 1.6); env(g, t, .003, .3, STEP * 1.6); o.connect(f); f.connect(g); g.connect(master); o.start(t); o.stop(t + STEP * 2); }
function riser(t){ const s = AC.createBufferSource(), b = AC.createBiquadFilter(), g = AC.createGain(), d = STEP * 16; s.buffer = noiseBuf; s.loop = true; b.type = "bandpass"; b.Q.value = 3; b.frequency.setValueAtTime(400, t); b.frequency.exponentialRampToValueAtTime(9000, t + d); g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(.18, t + d); g.gain.linearRampToValueAtTime(0, t + d + .02); s.connect(b); b.connect(g); g.connect(master); g.connect(verb); s.start(t); s.stop(t + d + .05); }
function schedule(){
  while (nextTime < AC.currentTime + .12){
    const s = step16, t = nextTime, chord = PROG[bar % 4];
    if (s === 0) pad(t, chord, STEP * 16);
    if (s === 0 && bar % 4 === 3) riser(t);
    if (s % 4 === 0) kick(t);
    if (s === 4 || s === 12) clap(t);
    if (s % 4 === 2) noise(t, "highpass", 8000, .7, .14, .11);
    if (s % 2 === 1) noise(t, "highpass", 10000, .7, .05, .025);
    if (s % 4 === 2 || s === 15) bass(t, chord[0]);
    const tones = [chord[0] + 12, chord[1] + 12, chord[2] + 12, chord[0] + 24];
    arp(t, tones[ARP[s]] + (bar % 8 >= 4 ? 12 : 0));
    if (s % 4 === 0) setTimeout(() => onBeat(s), Math.max(0, (t - AC.currentTime) * 1000));
    step16 = (s + 1) % 16; if (step16 === 0) bar++; nextTime += STEP;
  }
}
function blip(){
  if (!playing) return;
  const t = AC.currentTime, o = AC.createOscillator(), g = AC.createGain(); o.type = "square";
  o.frequency.setValueAtTime(N(78 + Math.floor(Math.random() * 12)), t); o.frequency.exponentialRampToValueAtTime(90, t + .08); env(g, t, .001, .12, .08);
  o.connect(g); g.connect(arpBus); o.start(t); o.stop(t + .1);
}
const btn = document.getElementById("sound"), bars = btn.querySelectorAll(".bars i"), meter = new Uint8Array(32);
function drawMeter(){
  if (!playing){ bars.forEach(b => b.style.height = "3px"); return; }
  analyser.getByteFrequencyData(meter); bars.forEach((b, i) => b.style.height = (3 + meter[i * 3 + 1] / 255 * 11).toFixed(1) + "px");
  requestAnimationFrame(drawMeter);
}
btn.addEventListener("click", async () => {
  if (!AC) setupAudio();
  if (!playing){
    await AC.resume(); playing = true; clearInterval(silentTimer); nextTime = AC.currentTime + .05; step16 = 0; bar = 0;
    timer = setInterval(schedule, 25); btn.setAttribute("aria-pressed", "true"); document.getElementById("soundlabel").textContent = "Silencio"; drawMeter();
  } else {
    playing = false; clearInterval(timer); await AC.suspend(); btn.setAttribute("aria-pressed", "false"); document.getElementById("soundlabel").textContent = "Sonido";
    if (!reduce) silentClock(); drawMeter();
  }
});
</script>
"""
open("vivo.template.html", "w").write(t)
print("ok")
