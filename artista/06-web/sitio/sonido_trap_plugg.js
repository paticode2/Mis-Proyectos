/* ===== sonido: loop original hecho en la página (sin archivos de audio), apagado hasta que la persona lo prende.
   Trap suave tipo plugg a 146 BPM: 808 que se desliza, hi-hats con redobles, campanitas cuadradas y acordes de fondo. ===== */
const BPM = 146, STEP = 60 / BPM / 4;
let beatCount = 0;
function onBeat(s){ if (s % 16 === 0) beatCount++; document.body.classList.add("beat"); setTimeout(() => document.body.classList.remove("beat"), 100); }
let AC = null, master, bus, verbIn, delayIn, analyser, nextTime = 0, step16 = 0, bar = 0, timer = null, playing = false, noiseBuf, sat;
const hz = m => 440 * Math.pow(2, (m - 69) / 12);
// one chord per bar, falling: Fmaj7 · Em7 · Dm9 · Cmaj7
const CHORDS = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60, 64], [48, 52, 55, 59]];
const ROOTS = [29, 28, 26, 24];
// 808: [step, semitones above the root, length in steps]; the second note slides from the first
const B808 = [[0, 0, 5], [6, 0, 3], [10, 7, 2], [12, 12, 4]];
// bell melody over two bars: [step, scale degree], C major pentatonic, high
const PENTA = [72, 74, 76, 79, 81, 84, 86];
const MEL = [[[0, 4], [3, 3], [6, 2], [8, 4], [11, 5], [14, 3]], [[0, 2], [2, 1], [4, 2], [8, 0], [10, 1], [12, 3]]];
const KICK = [0, 6, 10], CLAP = [8], HAT = [0, 2, 4, 6, 8, 10, 12, 14];
function setupAudio(){
  AC = new (window.AudioContext || window.webkitAudioContext)();
  master = AC.createGain(); master.gain.value = .55;
  const comp = AC.createDynamicsCompressor(); comp.threshold.value = -14; comp.ratio.value = 4;
  analyser = AC.createAnalyser(); analyser.fftSize = 64;
  master.connect(comp); comp.connect(analyser); analyser.connect(AC.destination);
  bus = AC.createGain(); bus.connect(master);
  const len = AC.sampleRate * 2.2, ir = AC.createBuffer(2, len, AC.sampleRate);
  for (let ch = 0; ch < 2; ch++){ const d = ir.getChannelData(ch); for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 2.6); }
  const verb = AC.createConvolver(); verb.buffer = ir; const vg = AC.createGain(); vg.gain.value = .38;
  verbIn = AC.createGain(); verbIn.connect(verb); verb.connect(vg); vg.connect(master);
  const dl = AC.createDelay(2); dl.delayTime.value = STEP * 3; const fb = AC.createGain(); fb.gain.value = .33;
  const dlf = AC.createBiquadFilter(); dlf.type = "lowpass"; dlf.frequency.value = 3600; const dg = AC.createGain(); dg.gain.value = .28;
  delayIn = AC.createGain(); delayIn.connect(dl); dl.connect(dlf); dlf.connect(fb); fb.connect(dl); dlf.connect(dg); dg.connect(master);
  // warm saturation for the 808
  sat = AC.createWaveShaper(); const c = new Float32Array(1024); for (let i = 0; i < 1024; i++){ const x = i / 512 - 1; c[i] = Math.tanh(x * 2.6); } sat.curve = c;
  const sg = AC.createGain(); sg.gain.value = .55; sat.connect(sg); sg.connect(bus);
  noiseBuf = AC.createBuffer(1, AC.sampleRate * .5, AC.sampleRate); const nd = noiseBuf.getChannelData(0); for (let i = 0; i < nd.length; i++) nd[i] = Math.random() * 2 - 1;
}
function env(g, t, a, peak, d){ g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(peak, t + a); g.gain.exponentialRampToValueAtTime(.0006, t + a + d); }
function send(node, dry, verb, echo){ const a = AC.createGain(); a.gain.value = dry; node.connect(a); a.connect(bus);
  if (verb){ const v = AC.createGain(); v.gain.value = verb; node.connect(v); v.connect(verbIn); }
  if (echo){ const e = AC.createGain(); e.gain.value = echo; node.connect(e); e.connect(delayIn); } }
function kick(t){ const o = AC.createOscillator(), g = AC.createGain(); o.frequency.setValueAtTime(150, t); o.frequency.exponentialRampToValueAtTime(50, t + .08); env(g, t, .002, .55, .12); o.connect(g); send(g, 1); o.start(t); o.stop(t + .2); }
function noise(t, type, f, q, peak, d, verb = 0){ const s = AC.createBufferSource(), b = AC.createBiquadFilter(), g = AC.createGain(); s.buffer = noiseBuf; b.type = type; b.frequency.value = f; b.Q.value = q; env(g, t, .001, peak, d); s.connect(b); b.connect(g); send(g, 1, verb); s.start(t); s.stop(t + d + .05); }
function clap(t){ [0, .012, .024].forEach(dt => noise(t + dt, "bandpass", 1500, .9, .3, .09, .35)); noise(t + .03, "bandpass", 1200, .7, .18, .22, .5); }
function hat(t, v = .09){ noise(t, "highpass", 9000, .8, v, .03); }
function b808(t, m, len, from){
  const o = AC.createOscillator(), g = AC.createGain(); o.type = "sine";
  if (from){ o.frequency.setValueAtTime(hz(from), t); o.frequency.exponentialRampToValueAtTime(hz(m), t + .09); } else o.frequency.setValueAtTime(hz(m), t);
  g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(.7, t + .006); g.gain.setValueAtTime(.7, t + len * .7); g.gain.exponentialRampToValueAtTime(.001, t + len);
  o.connect(g); g.connect(sat); o.start(t); o.stop(t + len + .05);
}
function bell(t, m){ const o = AC.createOscillator(), f = AC.createBiquadFilter(), g = AC.createGain(); o.type = "square"; o.frequency.value = hz(m);
  const lfo = AC.createOscillator(), lg = AC.createGain(); lfo.frequency.value = 5.5; lg.gain.value = 6; lfo.connect(lg); lg.connect(o.detune);
  f.type = "lowpass"; f.frequency.setValueAtTime(3800, t); f.frequency.exponentialRampToValueAtTime(900, t + .3);
  env(g, t, .005, .07, .42); o.connect(f); f.connect(g); send(g, .8, .35, .5); o.start(t); lfo.start(t); o.stop(t + .5); lfo.stop(t + .5); }
function pad(t, chord, len){
  const f = AC.createBiquadFilter(), g = AC.createGain(); f.type = "lowpass"; f.frequency.value = 1100;
  g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(.06, t + .3); g.gain.setValueAtTime(.06, t + len - .2); g.gain.linearRampToValueAtTime(0, t + len + .3);
  chord.forEach(m => [-9, 9].forEach(det => { const o = AC.createOscillator(); o.type = "sawtooth"; o.frequency.value = hz(m + 12); o.detune.value = det; o.connect(f); o.start(t); o.stop(t + len + .4); }));
  f.connect(g); send(g, .6, .7);
}
function schedule(){
  while (nextTime < AC.currentTime + .15){
    const s = step16, t = nextTime, c = bar % 4, chord = CHORDS[c];
    if (s === 0) pad(t, chord, STEP * 16);
    if (KICK.includes(s)) kick(t);
    if (CLAP.includes(s)) clap(t);
    if (HAT.includes(s)) hat(t, s % 4 ? .06 : .09);
    // hi-hat rolls at the end of every other bar: triplets, then 32nds
    if (bar % 2 === 1 && s === 13) for (let k = 0; k < 3; k++) hat(t + k * STEP * 2 / 3, .05);
    if (bar % 4 === 3 && s === 15) for (let k = 0; k < 4; k++) hat(t + k * STEP / 4, .04 + k * .01);
    const n = B808.find(x => x[0] === s); if (n){ const prev = B808[B808.indexOf(n) - 1]; b808(t, ROOTS[c] + n[1], STEP * n[2], n[1] !== (prev ? prev[1] : n[1]) ? ROOTS[c] + prev[1] : 0); }
    const mel = MEL[bar % 2].find(x => x[0] === s); if (mel && bar % 8 < 6) bell(t, PENTA[mel[1]]);
    if (s % 4 === 0) setTimeout(() => onBeat(s), Math.max(0, (t - AC.currentTime) * 1000));
    step16 = (s + 1) % 16; if (step16 === 0) bar++; nextTime += STEP;
  }
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
    await AC.resume(); playing = true; nextTime = AC.currentTime + .08; step16 = 0; bar = 0;
    timer = setInterval(schedule, 25); btn.setAttribute("aria-pressed", "true"); document.getElementById("soundlabel").textContent = "Silencio"; drawMeter();
  } else {
    playing = false; clearInterval(timer); await AC.suspend(); btn.setAttribute("aria-pressed", "false"); document.getElementById("soundlabel").textContent = "Sonido"; drawMeter();
  }
});
