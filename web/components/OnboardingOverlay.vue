<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, checkHealth, goHome, toast } = useWorkspace()

const step = ref<'gate' | 'name' | 'seed'>('gate')
const name = ref('')
const agentName = ref('')
const seedPath = ref('')
const seeding = ref(false)

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
  const body: any = {}
  if (name.value.trim()) body.name = name.value
  if (agentName.value.trim()) body.agent_name = agentName.value
  if (Object.keys(body).length) {
    await api('/onboarding', body)
    if (body.agent_name) state.agentName = body.agent_name.trim()
  }
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
  await finish()
}

async function finish() {
  await api('/onboarding', { onboarded: true })
  state.showOnboarding = false
  await goHome()                     // land in Home — the default chatroom
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
          <p class="onboard-sub" style="margin: 12px 0 6px">What do you want to name your personal assistant?</p>
          <input v-model="agentName" class="onboard-input" placeholder="Assistant name — e.g. Jarvis, Ginji" aria-label="Assistant name" />
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
              <button class="btn" @click="finish">Continue →</button>
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
              <button class="btn" @click="saveWorkspace(); finish()">Use this</button>
            </div>
            <div class="onboard-actions">
              <button class="btn ghost" @click="finish">Continue with default →</button>
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

    </div>
  </div>
</template>
