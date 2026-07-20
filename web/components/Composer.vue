<script setup lang="ts">
import { ref } from 'vue'
import { Paperclip, Mic, Square, ArrowUp, Landmark, Sparkles, MessageCircle, Ticket, Target } from 'lucide-vue-next'
import { useWorkspace } from '../composables/useWorkspace'

const { state, sendChat, sendHomeChat, toast } = useWorkspace()
const text = ref('')
const filePick = ref<HTMLInputElement>()
const LANES = [
  { key: 'auto', label: 'Auto', icon: Sparkles, hint: 'I decide: work becomes a card, talk gets an answer' },
  { key: 'chat', label: 'Chat', icon: MessageCircle, hint: 'Just talk — never makes a card' },
  { key: 'task', label: 'Ticket', icon: Ticket, hint: 'Always make a card on the board' },
  { key: 'goal', label: 'Goal', icon: Target, hint: 'A card that iterates until the goal is truly done' }
] as const
const lane = ref<'auto' | 'chat' | 'task' | 'goal'>('auto')

// ---- attachments: drop, paste, pick ----
const pending = ref<{ name: string; path: string }[]>([])
const uploading = ref(false)

async function uploadFiles(files: FileList | File[]) {
  uploading.value = true
  const url = state.current ? `/api/rooms/${state.current.id}/assets` : '/api/home/upload'
  for (const f of Array.from(files)) {
    const form = new FormData()
    form.append('file', f)
    try {
      const res = await fetch(url, { method: 'POST', body: form })
      const a = await res.json()
      if (!res.ok) throw new Error(a.error || 'upload failed')
      pending.value.push({ name: a.filename, path: a.path })
    } catch (e: any) { toast(e.message, true) }
  }
  uploading.value = false
}

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
const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
const recording = ref(false)
let recog: any = null
let mediaRec: MediaRecorder | null = null

async function toggleMic() {
  if (recording.value) { stopMic(); return }
  if (SR) {
    recog = new SR()
    recog.continuous = true
    recog.interimResults = false
    recog.onresult = (ev: any) => {
      for (let i = ev.resultIndex; i < ev.results.length; i++) {
        if (ev.results[i].isFinal) {
          text.value = (text.value + ' ' + ev.results[i][0].transcript).trimStart()
        }
      }
    }
    recog.onerror = () => stopMic()
    recog.start()
    recording.value = true
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
    } catch { toast('microphone unavailable', true) }
  }
}

function stopMic() {
  recording.value = false
  try { recog?.stop() } catch { /* already stopped */ }
  try { mediaRec?.state !== 'inactive' && mediaRec?.stop() } catch { /* already stopped */ }
  recog = null
}

async function send() {
  let t = text.value.trim()
  if (recording.value) stopMic()
  if (!t && !pending.value.length) return
  if (pending.value.length) {
    t += '\n\n[Attached files — read them as part of this message]:\n'
      + pending.value.map(f => `- ${f.path}`).join('\n')
    pending.value = []
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
    <div v-if="pending.length || uploading" class="attach-row">
      <span v-for="(f, i) in pending" :key="f.path" class="attach-chip">
        <Paperclip :size="11" :stroke-width="1.75" /> {{ f.name }}
        <button type="button" class="attach-x" :aria-label="`Remove ${f.name}`"
          @click="pending.splice(i, 1)">✕</button>
      </span>
      <span v-if="uploading" class="attach-chip dim">uploading…</span>
    </div>
    <textarea
      v-model="text"
      :placeholder="state.current ? 'How can I help in this room? (drop files here)' : 'Tell me anything — I\'ll route it to the right room'"
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
      <button class="send" :disabled="(!text.trim() && !pending.length) || uploading" title="Send" aria-label="Send"><ArrowUp :size="17" :stroke-width="2" /></button>
    </div>
  </form>
</template>
