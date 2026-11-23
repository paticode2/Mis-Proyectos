/* ===== sonido: loop original hecho en la página (sin archivos de audio), apagado hasta que la persona lo prende.
   Soñador y lento: dembow suave a 94 BPM, acordes con eco, arpegio brillante y bajo redondo. ===== */
const BPM = 94, STEP = 60 / BPM / 4;
let beatCount = 0;
function onBeat(s){ if (s % 16 === 0) beatCount++; document.body.classList.add("beat"); setTimeout(() => document.body.classList.remove("beat"), 110); }
let AC = null, master, bus, verbIn, delayIn, analyser, nextTime = 0, step16 = 0, bar = 0, timer = null, playing = false, noiseBuf;
const hz = m => 440 * Math.pow(2, (m - 69) / 12);
// four dreamy chords (MIDI notes), one per bar: Am9 · Fmaj7 · Cmaj7 · Gadd6
const CHORDS = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 69], [48, 55, 59, 64, 67], [55, 59, 62, 64, 71]];
const ROOTS = [33, 29, 36, 31];
const ARP = [0, 2, 4, 3, 1, 4, 2, 3];                       // which chord tone, high octave
const ARP_STEPS = [0, 3, 6, 8, 10, 11, 14];                  // sparse, so it breathes
const DEMBOW = { kick: [0, 4, 8, 12], snare: [3, 6, 11, 14], hat: [2, 6, 10, 14], shaker: [1, 5, 7, 9, 13, 15] };
function setupAudio(){
  AC = new (window.AudioContext || window.webkitAudioContext)();
  master = AC.createGain(); master.gain.value = .6;
  const comp = AC.createDynamicsCompressor(); comp.threshold.value = -16; comp.ratio.value = 3.5;
  const air = AC.createBiquadFilter(); air.type = "lowpass"; air.frequency.value = 9000;
  analyser = AC.createAnalyser(); analyser.fftSize = 64;
  master.connect(comp); comp.connect(air); air.connect(analyser); analyser.connect(AC.destination);
  bus = AC.createGain(); bus.connect(master);
  // soft room: convolver with a decaying noise tail
  const len = AC.sampleRate * 2.6, ir = AC.createBuffer(2, len, AC.sampleRate);
  for (let ch = 0; ch < 2; ch++){ const d = ir.getChannelData(ch); for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 2.4); }
  const verb = AC.createConvolver(); verb.buffer = ir; const vg = AC.createGain(); vg.gain.value = .42;
  verbIn = AC.createGain(); verbIn.connect(verb); verb.connect(vg); vg.connect(master);
  // dotted-eighth echo
  const dl = AC.createDelay(2); dl.delayTime.value = STEP * 3; const fb = AC.createGain(); fb.gain.value = .38;
  const dlf = AC.createBiquadFilter(); dlf.type = "lowpass"; dlf.frequency.value = 3200; const dg = AC.createGain(); dg.gain.value = .32;
  delayIn = AC.createGain(); delayIn.connect(dl); dl.connect(dlf); dlf.connect(fb); fb.connect(dl); dlf.connect(dg); dg.connect(master); dg.connect(verbIn);
  noiseBuf = AC.createBuffer(1, AC.sampleRate * .5, AC.sampleRate); const nd = noiseBuf.getChannelData(0); for (let i = 0; i < nd.length; i++) nd[i] = Math.random() * 2 - 1;
}
function env(g, t, a, peak, d){ g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(peak, t + a); g.gain.exponentialRampToValueAtTime(.0006, t + a + d); }
function send(node, dry, verb, echo){ const a = AC.createGain(); a.gain.value = dry; node.connect(a); a.connect(bus);
  if (verb){ const v = AC.createGain(); v.gain.value = verb; node.connect(v); v.connect(verbIn); }
  if (echo){ const e = AC.createGain(); e.gain.value = echo; node.connect(e); e.connect(delayIn); } }
function kick(t){ const o = AC.createOscillator(), g = AC.createGain(); o.frequency.setValueAtTime(120, t); o.frequency.exponentialRampToValueAtTime(44, t + .14); env(g, t, .003, .8, .26); o.connect(g); send(g, 1); o.start(t); o.stop(t + .32); }
function noise(t, type, f, q, peak, d, verb = .2){ const s = AC.createBufferSource(), b = AC.createBiquadFilter(), g = AC.createGain(); s.buffer = noiseBuf; b.type = type; b.frequency.value = f; b.Q.value = q; env(g, t, .001, peak, d); s.connect(b); b.connect(g); send(g, 1, verb); s.start(t); s.stop(t + d + .05); }
function snare(t){ noise(t, "bandpass", 2300, 1.2, .32, .11, .35); const o = AC.createOscillator(), g = AC.createGain(); o.type = "triangle"; o.frequency.value = 330; env(g, t, .001, .14, .06); o.connect(g); send(g, 1, .2); o.start(t); o.stop(t + .1); }
function pad(t, chord, len){
  const f = AC.createBiquadFilter(), g = AC.createGain(); f.type = "lowpass"; f.frequency.setValueAtTime(700, t); f.frequency.linearRampToValueAtTime(1800, t + len * .5); f.frequency.linearRampToValueAtTime(900, t + len);
  g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(.09, t + .6); g.gain.setValueAtTime(.09, t + len - .3); g.gain.linearRampToValueAtTime(0, t + len + .4);
  chord.forEach(m => [-7, 7].forEach(det => { const o = AC.createOscillator(); o.type = "triangle"; o.frequency.value = hz(m); o.detune.value = det; o.connect(f); o.start(t); o.stop(t + len + .5); }));
  f.connect(g); send(g, .8, .6);
}
function bell(t, m){ const o = AC.createOscillator(), o2 = AC.createOscillator(), g = AC.createGain(); o.type = "sine"; o2.type = "sine"; o.frequency.value = hz(m); o2.frequency.value = hz(m) * 3.01;
  const g2 = AC.createGain(); g2.gain.value = .25; o2.connect(g2); g2.connect(g); o.connect(g); env(g, t, .004, .11, .5); send(g, .7, .45, .55); o.start(t); o2.start(t); o.stop(t + .6); o2.stop(t + .6); }
function bass(t, m, d){ const o = AC.createOscillator(), g = AC.createGain(), f = AC.createBiquadFilter(); o.type = "sine"; o.frequency.value = hz(m); f.type = "lowpass"; f.frequency.value = 260;
  env(g, t, .01, .42, d); o.connect(f); f.connect(g); send(g, 1); o.start(t); o.stop(t + d + .1); }
function schedule(){
  while (nextTime < AC.currentTime + .15){
    const s = step16, t = nextTime + (s % 2 ? STEP * .12 : 0), c = bar % 4, chord = CHORDS[c];   // a little swing
    if (s === 0) pad(t, chord, STEP * 16);
    if (DEMBOW.kick.includes(s)) kick(t);
    if (DEMBOW.snare.includes(s)) snare(t);
    if (DEMBOW.hat.includes(s)) noise(t, "highpass", 8500, .7, .07, .04, .1);
    if (DEMBOW.shaker.includes(s)) noise(t, "highpass", 6000, .5, .035, .03, .05);
    if (s === 0 || s === 3 || s === 8 || s === 11) bass(t, ROOTS[c], s === 0 || s === 8 ? STEP * 2.6 : STEP * 1.4);
    const k = ARP_STEPS.indexOf(s); if (k >= 0 && bar % 8 !== 7) bell(t, chord[ARP[(k + bar) % ARP.length] % chord.length] + 12);
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
