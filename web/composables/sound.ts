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

// card finished: one soft ding
export function ding() {
  tone(783.99, 0, 0.4, 0.1)        // G5
  tone(1567.98, 0.02, 0.3, 0.035)  // overtone
}
