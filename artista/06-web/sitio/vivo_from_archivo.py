# Arma vivo.template.html a partir de archivo.template.html: misma web Archivo, más pintura rosa
# en movimiento, letras que cambian con el ritmo, líneas de construcción y sonido generado en la página.
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
// ---------- pink paint: glossy strokes that crawl over the page ----------
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const paint = document.getElementById("paint"), pg = paint.getContext("2d");
let PW = 0, PH = 0;
function sizePaint(){ const d = Math.min(2, devicePixelRatio || 1); PW = innerWidth; PH = innerHeight; paint.width = PW * d; paint.height = PH * d; pg.setTransform(d, 0, 0, d, 0, 0); pg.lineCap = pg.lineJoin = "round"; }
sizePaint(); addEventListener("resize", sizePaint);
const PR = rng(21);
function worm(x, y){ return { x: x ?? PR() * PW, y: y ?? PR() * PH, a: PR() * Math.PI * 2, v: 1.2 + PR() * 2.2, w: 10 + PR() * 22, life: 140 + PR() * 260, t: PR() * 100 }; }
let worms = Array.from({ length: 7 }, () => worm());
function stepPaint(){
  pg.globalCompositeOperation = "destination-out"; pg.fillStyle = "rgba(0,0,0,.012)"; pg.fillRect(0, 0, PW, PH);
  pg.globalCompositeOperation = "source-over";
  worms.forEach((m, i) => {
    m.t += .02; m.a += Math.sin(m.t * 1.7 + i) * .09 + Math.sin(m.t * .37) * .05;
    const nx = m.x + Math.cos(m.a) * m.v, ny = m.y + Math.sin(m.a) * m.v, w = m.w * (.7 + .3 * Math.sin(m.t * 3));
    pg.strokeStyle = "rgba(224,80,140,.92)"; pg.lineWidth = w; pg.beginPath(); pg.moveTo(m.x, m.y); pg.lineTo(nx, ny); pg.stroke();
    pg.strokeStyle = "rgba(255,196,218,.75)"; pg.lineWidth = w * .28; pg.beginPath(); pg.moveTo(m.x - w * .18, m.y - w * .18); pg.lineTo(nx - w * .18, ny - w * .18); pg.stroke();
    m.x = nx; m.y = ny; m.life--;
    if (m.life < 0 || m.x < -60 || m.y < -60 || m.x > PW + 60 || m.y > PH + 60) worms[i] = worm();
  });
}
function splat(x = PR() * PW, y = PR() * PH, n = 9){
  pg.fillStyle = "rgba(224,80,140,.9)";
  for (let i = 0; i < n; i++){ const a = PR() * Math.PI * 2, d = PR() * 40, r = 3 + PR() * 16; pg.beginPath(); pg.arc(x + Math.cos(a) * d, y + Math.sin(a) * d, r, 0, Math.PI * 2); pg.fill(); }
  pg.fillStyle = "rgba(255,196,218,.8)"; pg.beginPath(); pg.arc(x - 4, y - 4, 4, 0, Math.PI * 2); pg.fill();
  if (worms.length < 9) worms.push(worm(x, y));
}

// ---------- the beat: visuals follow it, with or without sound ----------
const BPM = 152, STEP = 60 / BPM / 4;          // 16th notes
let gSeed = 5, gMode = 0, beatCount = 0;
function onBeat(step){
  if (step % 4 === 0) splat(undefined, undefined, 6 + (step === 0 ? 8 : 0));
  if (step % 8 === 0){ beatCount++; gSeed += 7; gMode = beatCount % 3 === 0 ? 0 : 1; glitch(gSeed, gMode); }
}
let silentStep = 0, silentTimer = null;
function silentClock(){ silentTimer = setInterval(() => { onBeat(silentStep); silentStep = (silentStep + 4) % 16; }, STEP * 4 * 1000 * 2); }
function loop(){ if (!document.hidden) stepPaint(); requestAnimationFrame(loop); }
if (reduce){ for (let i = 0; i < 400; i++) stepPaint(); }
else { requestAnimationFrame(loop); silentClock(); }

// ---------- sound: a small 152 bpm loop made in the page (no audio files) ----------
let AC = null, master, analyser, nextTime = 0, step16 = 0, timer = null, playing = false, noiseBuf;
const CHORDS = [[293.7, 440, 466.2], [261.6, 392, 415.3], [233.1, 349.2, 466.2], [261.6, 392, 466.2]];
const PAT = { kick: [0, 6, 8, 11], snare: [4, 12], stab: [0, 3, 6, 10, 13], tick: [2, 7, 9, 15] };
function setupAudio(){
  AC = new (window.AudioContext || window.webkitAudioContext)();
  master = AC.createGain(); master.gain.value = .55;
  const shaper = AC.createWaveShaper(), curve = new Float32Array(1024);
  for (let i = 0; i < 1024; i++){ const x = i / 512 - 1; curve[i] = Math.round(Math.tanh(x * 2.2) * 24) / 24; }   // soft clip + a little bit-crush
  shaper.curve = curve;
  const lp = AC.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 7000;
  analyser = AC.createAnalyser(); analyser.fftSize = 64;
  master.connect(shaper); shaper.connect(lp); lp.connect(analyser); analyser.connect(AC.destination);
  noiseBuf = AC.createBuffer(1, AC.sampleRate * .5, AC.sampleRate); const nd = noiseBuf.getChannelData(0); for (let i = 0; i < nd.length; i++) nd[i] = Math.random() * 2 - 1;
}
function env(node, t, a, peak, d){ node.gain.setValueAtTime(0, t); node.gain.linearRampToValueAtTime(peak, t + a); node.gain.exponentialRampToValueAtTime(.0008, t + a + d); }
function kick(t){ const o = AC.createOscillator(), g = AC.createGain(); o.frequency.setValueAtTime(190, t); o.frequency.exponentialRampToValueAtTime(52, t + .16); env(g, t, .002, .9, .22); o.connect(g); g.connect(master); o.start(t); o.stop(t + .3); }
function noise(t, type, f, q, peak, d){ const s = AC.createBufferSource(), b = AC.createBiquadFilter(), g = AC.createGain(); s.buffer = noiseBuf; b.type = type; b.frequency.value = f; b.Q.value = q; env(g, t, .001, peak, d); s.connect(b); b.connect(g); g.connect(master); s.start(t); s.stop(t + d + .05); }
function snare(t){ noise(t, "bandpass", 1900, .8, .7, .16); const o = AC.createOscillator(), g = AC.createGain(); o.type = "triangle"; o.frequency.value = 200; env(g, t, .001, .35, .09); o.connect(g); g.connect(master); o.start(t); o.stop(t + .15); }
function tick(t){ const o = AC.createOscillator(), g = AC.createGain(); o.frequency.value = 2360; env(g, t, .001, .18, .05); o.connect(g); g.connect(master); o.start(t); o.stop(t + .08); }
function stab(t, chord){
  const f = AC.createBiquadFilter(), g = AC.createGain(); f.type = "lowpass"; f.Q.value = 6;
  f.frequency.setValueAtTime(2600, t); f.frequency.exponentialRampToValueAtTime(380, t + .18); env(g, t, .004, .22, .2);
  chord.forEach((hz, i) => { const o = AC.createOscillator(); o.type = "sawtooth"; o.frequency.value = hz; o.detune.value = (i - 1) * 9; o.connect(f); o.start(t); o.stop(t + .3); });
  f.connect(g); g.connect(master);
}
function schedule(){
  while (nextTime < AC.currentTime + .12){
    const s = step16, t = nextTime, bar = Math.floor(beatCount / 2) % CHORDS.length;
    if (PAT.kick.includes(s)) kick(t);
    if (PAT.snare.includes(s)) snare(t);
    if (s % 2 === 1) noise(t, "highpass", 7500, .7, .12, .03);
    if (PAT.tick.includes(s)) tick(t);
    if (PAT.stab.includes(s)) stab(t, CHORDS[bar]);
    if (s % 4 === 0) setTimeout(() => onBeat(s), Math.max(0, (t - AC.currentTime) * 1000));
    step16 = (s + 1) % 16; nextTime += STEP;
  }
}
function blip(){
  if (!playing) return;
  const t = AC.currentTime, o = AC.createOscillator(), g = AC.createGain(); o.type = "square";
  o.frequency.setValueAtTime(1400 + Math.random() * 900, t); o.frequency.exponentialRampToValueAtTime(90, t + .07); env(g, t, .001, .12, .07);
  o.connect(g); g.connect(master); o.start(t); o.stop(t + .1);
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
    await AC.resume(); playing = true; clearInterval(silentTimer); nextTime = AC.currentTime + .05; step16 = 0;
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
