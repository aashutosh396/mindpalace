<script setup lang="ts">
import { ref } from 'vue'
import { Paperclip, Mic, Square, ArrowUp, Landmark, Sparkles, MessageCircle, Ticket, Target } from 'lucide-vue-next'
import { useWorkspace } from '../composables/useWorkspace'

const { state, sendChat, sendHomeChat, toast, uploadFiles } = useWorkspace()
const text = ref('')
const filePick = ref<HTMLInputElement>()
const LANES = [
  { key: 'auto', label: 'Auto', icon: Sparkles, hint: 'I decide: work becomes a card, talk gets an answer' },
  { key: 'chat', label: 'Chat', icon: MessageCircle, hint: 'Just talk — never makes a card' },
  { key: 'task', label: 'Ticket', icon: Ticket, hint: 'Always make a card on the board' },
  { key: 'goal', label: 'Goal', icon: Target, hint: 'A card that iterates until the goal is truly done' }
] as const
const lane = ref<'auto' | 'chat' | 'task' | 'goal'>('auto')

// attachments live in shared state (useWorkspace.uploadFiles) so the whole
// chat area is a drop zone, not just this box

function onDrop(e: DragEvent) {
  if (e.dataTransfer?.files.length) uploadFiles(e.dataTransfer.files)
}

function onPaste(e: ClipboardEvent) {
  const files = Array.from(e.clipboardData?.files || [])
  if (files.length) { e.preventDefault(); uploadFiles(files) }
}

function onPick() {
  if (filePick.value?.files?.length) uploadFiles(filePick.value.files)
  if (filePick.value) filePick.value.value = ''
}

// ---- voice ----
// Dictation = the browser's Web Speech API (SpeechRecognition) — live interim
// words land in the box as you speak. No SR support → record a voice note the
// agent transcribes. The strip (dot + timer + level bars) runs off a parallel
// mic stream so you SEE it listening either way.
const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
const recording = ref(false)
const elapsed = ref(0)
const levels = ref<number[]>(Array(24).fill(2))
let recog: any = null
let mediaRec: MediaRecorder | null = null
let baseText = ''
let finalAcc = ''
let clockTimer: ReturnType<typeof setInterval> | null = null
let meterStream: MediaStream | null = null
let meterCtx: AudioContext | null = null
let meterRaf = 0

const clock = () => `${String(Math.floor(elapsed.value / 60)).padStart(2, '0')}:${String(elapsed.value % 60).padStart(2, '0')}`

async function startMeter() {
  elapsed.value = 0
  clockTimer = setInterval(() => { elapsed.value++ }, 1000)
  try {
    meterStream = await navigator.mediaDevices.getUserMedia({ audio: true })
    meterCtx = new AudioContext()
    const src = meterCtx.createMediaStreamSource(meterStream)
    const an = meterCtx.createAnalyser()
    an.fftSize = 256
    src.connect(an)
    const buf = new Uint8Array(an.frequencyBinCount)
    const tick = () => {
      an.getByteTimeDomainData(buf)
      let sum = 0
      for (const v of buf) sum += (v - 128) * (v - 128)
      const rms = Math.sqrt(sum / buf.length)                    // 0..~40 speaking
      levels.value = [...levels.value.slice(1), Math.max(2, Math.min(18, rms * 1.4))]
      meterRaf = requestAnimationFrame(tick)
    }
    tick()
  } catch { /* no meter — the dot + timer still show it's live */ }
}

function stopMeter() {
  if (clockTimer) { clearInterval(clockTimer); clockTimer = null }
  cancelAnimationFrame(meterRaf)
  meterStream?.getTracks().forEach(t => t.stop())
  meterStream = null
  meterCtx?.close().catch(() => {})
  meterCtx = null
  levels.value = Array(24).fill(2)
}

async function toggleMic() {
  if (recording.value) { stopMic(); return }
  if (SR) {
    baseText = text.value.trim()
    finalAcc = ''
    recog = new SR()
    recog.continuous = true
    recog.interimResults = true
    recog.onresult = (ev: any) => {
      // ACCUMULATE finals — the browser resets its result list when it
      // restarts after a silence, so rebuilding from ev.results loses text
      let interim = ''
      for (let i = ev.resultIndex; i < ev.results.length; i++) {
        const r = ev.results[i]
        if (r.isFinal) finalAcc += r[0].transcript + ' '
        else interim += r[0].transcript
      }
      text.value = [baseText, finalAcc.trim(), interim.trim()].filter(Boolean).join(' ')
    }
    recog.onend = () => {                            // silence timeout — keep listening
      if (recording.value && recog) { try { recog.start() } catch { /* stopping */ } }
    }
    recog.onerror = () => stopMic()
    recog.start()
    recording.value = true
    startMeter()
  } else {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const chunks: Blob[] = []
      mediaRec = new MediaRecorder(stream)
      mediaRec.ondataavailable = (e) => chunks.push(e.data)
      mediaRec.onstop = async () => {
        stream.getTracks().forEach(t => t.stop())
        const blob = new Blob(chunks, { type: mediaRec?.mimeType || 'audio/webm' })
        const f = new File([blob], `voice-${Date.now()}.webm`, { type: blob.type })
        await uploadFiles([f])
        if (!text.value.trim()) text.value = 'Transcribe the attached voice note and treat it as my message.'
      }
      mediaRec.start()
      recording.value = true
      startMeter()
    } catch { toast('microphone unavailable', true) }
  }
}

function stopMic() {
  recording.value = false
  stopMeter()
  try { recog?.stop() } catch { /* already stopped */ }
  try { mediaRec?.state !== 'inactive' && mediaRec?.stop() } catch { /* already stopped */ }
  recog = null
}

async function send() {
  let t = text.value.trim()
  if (recording.value) stopMic()
  if (!t && !state.pendingFiles.length) return
  if (state.pendingFiles.length) {
    t += '\n\n[Attached files — read them as part of this message]:\n'
      + state.pendingFiles.map(f => `- ${f.path}`).join('\n')
    state.pendingFiles = []
  }
  text.value = ''
  if (state.current) await sendChat(t, lane.value)
  else await sendHomeChat(t)
}

function onKey(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }
}
</script>

<template>
  <form class="composer" @submit.prevent="send"
    @dragover.prevent @drop.prevent="onDrop">
    <div v-if="state.pendingFiles.length || state.uploadingFiles" class="attach-row">
      <span v-for="(f, i) in state.pendingFiles" :key="f.path"
        class="attach-item" :class="{ thumb: f.url }">
        <img v-if="f.url" :src="f.url" :alt="f.name" class="attach-img" />
        <span v-else class="attach-chip"><Paperclip :size="11" :stroke-width="1.75" /> {{ f.name }}</span>
        <button type="button" class="attach-del" :aria-label="`Remove ${f.name}`" :title="`Remove ${f.name}`"
          @click="state.pendingFiles.splice(i, 1)">✕</button>
      </span>
      <span v-if="state.uploadingFiles" class="attach-chip dim">uploading…</span>
    </div>
    <div v-if="recording" class="rec-strip" role="status" aria-label="Recording">
      <span class="rec-dot"></span>
      <span class="rec-label">Listening</span>
      <span class="rec-clock">{{ clock() }}</span>
      <span class="rec-bars" aria-hidden="true">
        <span v-for="(h, i) in levels" :key="i" class="rec-bar" :style="{ height: h + 'px' }"></span>
      </span>
      <span class="rec-hint">{{ SR ? 'your words land in the box' : 'voice note — sent for transcription' }}</span>
    </div>
    <textarea
      v-model="text"
      :placeholder="recording ? 'Listening — speak, words appear here…' : state.current ? 'How can I help in this room? (drop files here)' : 'Tell me anything — I\'ll route it to the right room'"
      aria-label="Instruction"
      @keydown="onKey"
      @paste="onPaste"></textarea>
    <div class="composer-controls" role="radiogroup" aria-label="Message lane">
      <input ref="filePick" type="file" multiple hidden aria-label="Attach files" @change="onPick" />
      <button type="button" class="lane icon-lane" title="Attach files or images" aria-label="Attach files"
        @click="filePick?.click()"><Paperclip :size="14" :stroke-width="1.75" /></button>
      <button type="button" class="lane icon-lane" :class="{ 'rec-on': recording }"
        :title="recording ? 'Stop recording' : 'Dictate (or record a voice note)'"
        aria-label="Voice input" @click="toggleMic">
        <Square v-if="recording" :size="13" :stroke-width="1.75" />
        <Mic v-else :size="14" :stroke-width="1.75" />
      </button>
      <template v-if="state.current">
        <button
          v-for="l in LANES" :key="l.key" type="button"
          class="lane" :class="{ active: lane === l.key }"
          :title="l.hint" :aria-checked="lane === l.key" role="radio"
          @click="lane = l.key"><component :is="l.icon" :size="13" :stroke-width="1.75" /> {{ l.label }}</button>
      </template>
      <span v-else class="lane active" style="cursor: default" title="The concierge decides: answer, file into one of your rooms, or hand palace chores to the keeper"><Landmark :size="13" :stroke-width="1.75" /> Concierge</span>
      <button class="send" :disabled="(!text.trim() && !state.pendingFiles.length) || state.uploadingFiles" title="Send" aria-label="Send"><ArrowUp :size="17" :stroke-width="2" /></button>
    </div>
  </form>
</template>
