<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { X, Square, Target, Paperclip, Mic } from 'lucide-vue-next'
import { useWorkspace, STATUSES, type Status } from '../composables/useWorkspace'
import { md } from '../composables/md'

const { state, moveTask, replyTask, stopTask, toast } = useWorkspace()
const trail = ref<HTMLElement>()
const reply = ref('')

// ---- follow-up attachments: drop, paste, pick (same as the composer) ----
const pending = ref<{ name: string; path: string; url?: string }[]>([])
const uploading = ref(false)
const filePick = ref<HTMLInputElement>()

async function uploadFiles(files: FileList | File[]) {
  uploading.value = true
  for (const f of Array.from(files)) {
    const form = new FormData()
    form.append('file', f)
    try {
      const res = await fetch(`/api/rooms/${t.value.room_id}/assets`, { method: 'POST', body: form })
      const a = await res.json()
      if (!res.ok) throw new Error(a.error || 'upload failed')
      pending.value.push({
        name: a.filename, path: a.path,
        url: f.type.startsWith('image/') ? URL.createObjectURL(f) : undefined
      })
    } catch (e: any) { toast(e.message, true) }
  }
  uploading.value = false
}

function onPaste(e: ClipboardEvent) {
  const files = Array.from(e.clipboardData?.files || [])
  if (files.length) { e.preventDefault(); uploadFiles(files) }
}

// ---- voice: dictate into the reply (or record a voice note) ----
const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
const recording = ref(false)
const elapsed = ref(0)
const levels = ref<number[]>(Array(24).fill(2))
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
      levels.value = [...levels.value.slice(1), Math.max(2, Math.min(18, Math.sqrt(sum / buf.length) * 1.4))]
      meterRaf = requestAnimationFrame(tick)
    }
    tick()
  } catch { /* no meter — the dot + timer still show it's live */ }
}

function stopMeter() {
  if (clockTimer) { clearInterval(clockTimer); clockTimer = null }
  cancelAnimationFrame(meterRaf)
  meterStream?.getTracks().forEach(x => x.stop())
  meterStream = null
  meterCtx?.close().catch(() => {})
  meterCtx = null
  levels.value = Array(24).fill(2)
}

let recog: any = null
let mediaRec: MediaRecorder | null = null
let baseReply = ''
let finalAcc = ''

async function toggleMic() {
  if (recording.value) { stopMic(); return }
  if (SR) {
    baseReply = reply.value.trim()
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
      reply.value = [baseReply, finalAcc.trim(), interim.trim()].filter(Boolean).join(' ')
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
        stream.getTracks().forEach(x => x.stop())
        const blob = new Blob(chunks, { type: mediaRec?.mimeType || 'audio/webm' })
        await uploadFiles([new File([blob], `voice-${Date.now()}.webm`, { type: blob.type })])
        if (!reply.value.trim()) reply.value = 'Transcribe the attached voice note and treat it as my reply.'
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

async function sendReply() {
  let t2 = reply.value.trim()
  if (recording.value) stopMic()
  if (!t2 && !pending.value.length) return
  if (pending.value.length) {
    t2 += '\n\n[Attached files — read them as part of this reply]:\n'
      + pending.value.map(f => `- ${f.path}`).join('\n')
    pending.value = []
  }
  reply.value = ''
  await replyTask(t.value.id, t2)
}

const LABELS: Record<string, string> = {
  todo: 'To do', in_progress: 'In progress', review: 'Review', done: 'Done'
}
const COLORS: Record<string, string> = {
  todo: 'var(--slate)', in_progress: 'var(--brass)', review: 'var(--lilac)', done: 'var(--sage)'
}

const t = computed(() => state.modal!.task)

function nextOf(s: Status): Status | null {
  const i = STATUSES.indexOf(s)
  return i < STATUSES.length - 1 ? STATUSES[i + 1] : null
}

function fmtTime(ts: number) {
  return new Date(ts * 1000).toLocaleTimeString()
}

watch(() => state.modal?.log.length, async () => {
  await nextTick()
  trail.value?.scrollTo({ top: trail.value.scrollHeight })
}, { immediate: true })
</script>

<template>
  <div class="sheet-backdrop" @click.self="state.modal = null">
    <div class="task-modal" role="dialog" :aria-label="`Card #${t.id}`">
      <div class="tm-head">
        <span class="status-pill" :style="{ '--c': COLORS[t.status] }">{{ LABELS[t.status] }}</span>
        <span v-if="t.kind === 'goal'" class="room-tag"><Target :size="11" :stroke-width="1.75" /> goal · iteration {{ t.iterations || 0 }}</span>
        <span v-if="state.modal!.room" class="room-tag">{{ state.modal!.room.name }}</span>
        <span class="tm-id">#{{ t.id }}</span>
        <button class="row-x" title="Close" aria-label="Close" @click="state.modal = null"><X :size="15" :stroke-width="1.75" /></button>
      </div>

      <h2 class="tm-title">{{ t.title }}</h2>
      <p v-if="t.body && t.body !== t.title" class="tm-body" v-html="md(t.body)"></p>

      <div class="tm-cols">
        <div class="tm-left">
          <template v-if="t.result">
            <div class="tm-section">Result</div>
            <div class="tm-result" v-html="md(t.result)"></div>
          </template>

          <template v-if="state.modal!.thread.length">
            <div class="tm-section">Follow-ups</div>
            <div class="tm-thread">
              <div v-for="m in state.modal!.thread" :key="m.id" class="tm-thread-msg" :class="m.role">
                <span class="who">{{ m.role === 'user' ? 'You' : 'Agent' }}</span><span v-html="md(m.text)"></span>
              </div>
            </div>
          </template>

          <div v-if="pending.length || uploading" class="attach-row">
            <span v-for="(f, i) in pending" :key="f.path"
              class="attach-item" :class="{ thumb: f.url }">
              <img v-if="f.url" :src="f.url" :alt="f.name" class="attach-img" />
              <span v-else class="attach-chip"><Paperclip :size="11" :stroke-width="1.75" /> {{ f.name }}</span>
              <button type="button" class="attach-del" :aria-label="`Remove ${f.name}`" :title="`Remove ${f.name}`"
                @click="pending.splice(i, 1)">✕</button>
            </span>
            <span v-if="uploading" class="attach-chip dim">uploading…</span>
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
          <form class="tm-reply" @submit.prevent="sendReply"
            @dragover.prevent @drop.prevent="($event.dataTransfer?.files.length && t.status !== 'in_progress') && uploadFiles($event.dataTransfer.files)">
            <input ref="filePick" type="file" multiple hidden aria-label="Attach files to reply"
              @change="filePick?.files?.length && uploadFiles(filePick.files); filePick && (filePick.value = '')" />
            <button type="button" class="lane icon-lane" title="Attach files or images" aria-label="Attach files"
              :disabled="t.status === 'in_progress'" @click="filePick?.click()"><Paperclip :size="14" :stroke-width="1.75" /></button>
            <button type="button" class="lane icon-lane" :class="{ 'rec-on': recording }"
              :title="recording ? 'Stop recording' : 'Dictate (or record a voice note)'"
              :disabled="t.status === 'in_progress'"
              aria-label="Voice reply" @click="toggleMic">
              <Square v-if="recording" :size="13" :stroke-width="1.75" />
              <Mic v-else :size="14" :stroke-width="1.75" />
            </button>
            <textarea
              v-model="reply" rows="3"
              :placeholder="t.status === 'in_progress' ? 'Working — wait for it to finish…' : recording ? 'Listening — speak, words appear here…' : 'Reply on this card — text, files, images, voice'"
              :disabled="t.status === 'in_progress'"
              aria-label="Reply on card"
              @paste="onPaste"
              @keydown.enter.exact.prevent="sendReply"></textarea>
            <button class="btn" :disabled="(!reply.trim() && !pending.length) || uploading || t.status === 'in_progress'">Send</button>
          </form>

          <div class="tm-actions">
            <button v-if="t.status === 'in_progress'" class="btn ghost stop-btn" @click="stopTask(t.id)">
              <Square :size="12" :stroke-width="2" /> Stop
            </button>
            <button v-if="nextOf(t.status)" class="btn ghost" @click="moveTask(t.id, nextOf(t.status)!)">
              → {{ LABELS[nextOf(t.status)!] }}
            </button>
            <button v-if="t.status !== 'done'" class="btn" @click="moveTask(t.id, 'done'); state.modal = null">
              Close card
            </button>
          </div>
        </div>

        <div class="tm-right">
          <div class="tm-section" style="margin-top: 0">The work</div>
          <div ref="trail" class="tm-trail">
            <div v-for="l in state.modal!.log" :key="l.id" class="tm-step"
              :class="{ marker: l.text.startsWith('—') }">
              <span class="tm-time">{{ fmtTime(l.created_at) }}</span>{{ l.text }}
            </div>
            <div v-if="!state.modal!.log.length" class="tm-step dim">
              {{ t.status === 'todo' ? 'Waiting for the worker to pick this up…' : 'No steps recorded.' }}
            </div>
            <div v-if="t.status === 'in_progress'" class="tm-step working">⚡ working…</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
