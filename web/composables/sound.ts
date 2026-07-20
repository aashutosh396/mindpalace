// Tiny synthesized sounds — no audio assets, just Web Audio oscillators.
// Browsers unlock audio after the first user gesture; we resume() on play.

let ctx: AudioContext | null = null

function ac(): AudioContext | null {
  try {
    ctx ||= new AudioContext()
    if (ctx.state === 'suspended') ctx.resume().catch(() => {})
    return ctx
  } catch { return null }
}

function tone(freq: number, delay: number, dur: number, gain: number) {
  const c = ac()
  if (!c) return
  const o = c.createOscillator()
  const g = c.createGain()
  o.type = 'sine'
  o.frequency.value = freq
  o.connect(g)
  g.connect(c.destination)
  const t = c.currentTime + delay
  g.gain.setValueAtTime(0, t)
  g.gain.linearRampToValueAtTime(gain, t + 0.02)
  g.gain.exponentialRampToValueAtTime(0.0001, t + dur)
  o.start(t)
  o.stop(t + dur + 0.05)
}

// reminder: a two-tone bell that asks for attention
export function chime() {
  tone(659.25, 0, 0.55, 0.16)      // E5
  tone(880, 0.14, 0.7, 0.14)       // A5
  tone(1318.5, 0.14, 0.5, 0.05)    // E6 shimmer
}

// alarm: LOUD double ring, repeating until stopRing() — for reminders
let ringTimer: ReturnType<typeof setInterval> | null = null

function bellStrike(delay: number) {
  tone(880, delay, 0.6, 0.5)         // A5 — the body, loud
  tone(1108.73, delay, 0.55, 0.32)   // C#6
  tone(659.25, delay, 0.5, 0.28)     // E5 under
  tone(1760, delay, 0.35, 0.12)      // ring edge
}

export function startRing() {
  if (ringTimer) return
  const pattern = () => { bellStrike(0); bellStrike(0.3) }   // classic ring-ring
  pattern()
  ringTimer = setInterval(pattern, 1600)
}

export function stopRing() {
  if (ringTimer) { clearInterval(ringTimer); ringTimer = null }
}

// card finished: one soft ding
export function ding() {
  tone(783.99, 0, 0.4, 0.1)        // G5
  tone(1567.98, 0.02, 0.3, 0.035)  // overtone
}
