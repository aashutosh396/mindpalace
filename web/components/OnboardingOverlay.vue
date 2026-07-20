<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, checkHealth, createRoom, goHome, loadProjects, projectsApi, sendHomeChat, toast } = useWorkspace()

const step = ref<'gate' | 'name' | 'seed' | 'room' | 'spark' | 'tips'>('gate')
const name = ref('')
const seedPath = ref('')
const seeding = ref(false)
const roomName = ref('')
const madeRoom = ref(false)
const lastRoom = ref('')

async function api(path: string, body?: any) {
  const res = await fetch(`/api${path}`, body === undefined ? {} : {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body)
  })
  return res.json()
}

const providerOk = computed(() => !!state.health?.provider_ok)
const vaultPresent = ref(false)
const workspace = ref('')

async function loadInfo() {
  const info = await api('/onboarding')
  vaultPresent.value = !!info.vault_present
  workspace.value = info.workspace || ''
}

let gateTimer: ReturnType<typeof setInterval> | null = null
onMounted(() => {
  loadInfo()
  if (providerOk.value) step.value = 'name'
  else gateTimer = setInterval(async () => {
    await checkHealth()
    if (providerOk.value && step.value === 'gate') {
      step.value = 'name'
      if (gateTimer) clearInterval(gateTimer)
    }
  }, 4000)
})
onUnmounted(() => { if (gateTimer) clearInterval(gateTimer) })

async function saveName() {
  if (name.value.trim()) await api('/onboarding', { name: name.value })
  if (vaultPresent.value) {
    await api('/onboarding/seed', { mode: 'vault' })   // no question — the vault IS the answer
  }
  step.value = 'seed'
}

async function saveWorkspace() {
  if (workspace.value.trim()) await api('/onboarding', { workspace: workspace.value })
  // stay on the seed card — the owner may also scan a folder, or continue
}

async function seed(mode: 'folder' | 'vault') {
  seeding.value = true
  const body: any = { mode }
  if (mode === 'folder') body.path = seedPath.value.trim()
  const r = await api('/onboarding/seed', body)
  seeding.value = false
  if (r.error) { toast(r.error, true); return }
  toast('The keeper is scanning — projects will appear as they load')
  startRoomStep()
}

// suggestion chips fill in live as the keeper loads the inventory
let projTimer: ReturnType<typeof setInterval> | null = null
function startRoomStep() {
  step.value = 'room'
  loadProjects()
  projTimer = setInterval(loadProjects, 4000)
}
onUnmounted(() => { if (projTimer) clearInterval(projTimer) })

async function makeRoom(n?: string) {
  const nm = (n || roomName.value).trim()
  if (!nm) return
  await createRoom(nm)
  // if a project matches the chatroom name, connect it right away
  const match = state.projects.find((p: any) =>
    p.name.toLowerCase() === nm.toLowerCase() || p.slug === nm.toLowerCase())
  if (match && state.current) await projectsApi.connect(state.current.id, match.id)
  madeRoom.value = true
  lastRoom.value = nm
  await goHome()                     // Home is the default room — you start there
  step.value = 'spark'
}

async function spark(text: string) {
  await sendHomeChat(text)           // the hall routes it — that's the lesson
  step.value = 'tips'
}

async function finish() {
  await api('/onboarding', { onboarded: true })
  state.showOnboarding = false
}
</script>

<template>
  <div class="sheet-backdrop onboard-backdrop">
    <div class="onboard" role="dialog" aria-label="Welcome to mindpalace">
      <button v-if="step !== 'gate'" class="onboard-skip" @click="finish">Skip setup</button>

      <!-- 0 · the gate -->
      <template v-if="step === 'gate'">
        <div class="onboard-hello"><span class="star">✳</span>Welcome to mindpalace</div>
        <p class="onboard-sub">Your projects, chatrooms, and an agent that works the tickets.</p>
        <div class="onboard-card">
          <p><strong>One thing to set up:</strong> the palace thinks with Claude.
          Install Claude Code and sign in to your Claude plan:</p>
          <code class="onboard-code">curl -fsSL https://claude.ai/install.sh | bash</code>
          <p class="dim-note" style="margin: 8px 0 0">
            {{ state.health ? state.health.provider_status : 'checking…' }} — I re-check automatically.
          </p>
          <div class="onboard-actions">
            <button class="btn" @click="checkHealth()">Check again</button>
          </div>
        </div>
      </template>

      <!-- 1 · name -->
      <template v-else-if="step === 'name'">
        <div class="onboard-hello"><span class="star">✳</span>Claude is connected.</div>
        <p class="onboard-sub">What should the palace call you?</p>
        <form class="onboard-card" @submit.prevent="saveName">
          <input v-model="name" class="onboard-input" placeholder="Your name" aria-label="Your name" autofocus />
          <div class="onboard-actions">
            <button class="btn" type="submit">Continue</button>
          </div>
        </form>
      </template>

      <!-- 2 · vault detected → say so; else workspace question + optional scan -->
      <template v-else-if="step === 'seed'">
        <template v-if="vaultPresent">
          <div class="onboard-hello"><span class="star">✳</span>.mindpalace detected</div>
          <p class="onboard-sub">Found your vault — importing its tracked projects into the inventory now.</p>
          <div class="onboard-card">
            <p class="dim-note" style="margin:0">
              The keeper is reading your vault's project pointers. Projects appear as they
              load — you can continue right away.
            </p>
            <div class="onboard-actions">
              <button class="btn" @click="startRoomStep">Continue →</button>
            </div>
          </div>
        </template>
        <template v-else>
          <div class="onboard-hello"><span class="star">✳</span>No .mindpalace vault found.</div>
          <p class="onboard-sub">Where should your workspace be? New projects are born there.</p>
          <div class="onboard-card">
            <p><strong>Create a workspace</strong> — pick a folder:</p>
            <div style="display:flex; gap:8px">
              <input v-model="workspace" class="onboard-input" aria-label="Workspace folder" />
              <button class="btn" @click="saveWorkspace(); startRoomStep()">Use this</button>
            </div>
            <div class="onboard-actions">
              <button class="btn ghost" @click="startRoomStep">Continue with default →</button>
            </div>
          </div>
          <div class="onboard-card">
            <p><strong>Already have projects?</strong> Point me at their folder and I'll load them in.</p>
            <div style="display:flex; gap:8px">
              <input v-model="seedPath" class="onboard-input" placeholder="/Users/you/code" aria-label="Folder to scan" />
              <button class="btn" :disabled="!seedPath.trim() || seeding" @click="seed('folder')">Scan</button>
            </div>
          </div>
        </template>
      </template>

      <!-- 3 · first chatroom -->
      <template v-else-if="step === 'room'">
        <div class="onboard-hello"><span class="star">✳</span>Make your first chatroom.</div>
        <p class="onboard-sub">
          Chatrooms are <em>yours</em> — like Discord channels. Each connects to projects,
          and its agent works inside their folders.
        </p>
        <div class="onboard-card">
          <form style="display:flex; gap:8px" @submit.prevent="makeRoom()">
            <input v-model="roomName" class="onboard-input" placeholder="Chatroom name" aria-label="Chatroom name" />
            <button class="btn" :disabled="!roomName.trim()">Create</button>
          </form>
          <div v-if="state.projects.length" class="onboard-chips">
            <span class="dim-note">from your inventory:</span>
            <button v-for="p in state.projects.slice(0, 6)" :key="p.id" class="lane"
              @click="makeRoom(p.name)">{{ p.name }}</button>
          </div>
          <p v-else class="dim-note" style="margin-top:8px">
            (inventory is still loading — chips appear as the keeper finds projects)
          </p>
        </div>
      </template>

      <!-- 4 · first spark — from Home, the default room -->
      <template v-else-if="step === 'spark'">
        <div class="onboard-hello"><span class="star">✳</span>You start in Home.</div>
        <p class="onboard-sub">Home is your default room — talk here and I route work into your chatrooms. Try one:</p>
        <div class="onboard-card onboard-sparks">
          <button class="btn ghost" @click="spark('what projects do we have?')">
            💬 “what projects do we have?”
          </button>
          <button v-if="lastRoom" class="btn ghost" @click="spark(`in ${lastRoom}: add a card to review the README`)">
            🎫 “in {{ lastRoom }}: add a card to review the README”
          </button>
          <button class="btn ghost" @click="step = 'tips'">I'll type my own →</button>
        </div>
      </template>

      <!-- 5 · tips & done -->
      <template v-else>
        <div class="onboard-hello"><span class="star">✳</span>You're in.</div>
        <div class="onboard-card">
          <ul class="onboard-tips">
            <li><strong>Home</strong> routes anything — talk there, it files work into your chatrooms.</li>
            <li><strong>Review is your inbox</strong> — the tab badge counts cards waiting on you.</li>
            <li><strong>⌘K</strong> searches rooms, projects, cards and chats.</li>
            <li><strong>Auto / 💬 / 🎫 / 🎯</strong> lanes control what Send does; click any card to watch its work.</li>
          </ul>
          <div class="onboard-actions">
            <button class="btn" @click="finish">Enter the palace</button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
