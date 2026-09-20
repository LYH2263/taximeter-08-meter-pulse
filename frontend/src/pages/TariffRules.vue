<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const t = ref(null)
const pulse = ref(null)
const saving = ref(false)
onMounted(load)
async function load() {
  t.value = await getJSON('/api/tariff')
  pulse.value = await getJSON('/api/pulse')
}
async function toggle(v) {
  saving.value = true
  try {
    pulse.value = await postJSON('/api/pulse', { enabled: v })
  } finally {
    saving.value = false
    await load()
  }
}
</script>
<template>
  <div class="page"><h1>运价表</h1>
    <pre v-if="t">{{ t }}</pre>
    <div v-if="pulse" class="panel">
      <h2>计价脉冲</h2>
      <p>启用后：超出含公里的里程每 0.5 公里一跳，低速每整分钟一跳，不足一跳的尾数不计。全局仅允许一条规则启用。</p>
      <ul v-if="pulse.rules?.length">
        <li v-for="r in pulse.rules" :key="r.id">
          规则 #{{ r.id }}：{{ r.distance_step_km }} 公里/跳 · {{ r.slow_step_min }} 分钟/跳 ·
          {{ r.enabled ? '启用中' : '停用' }}
        </li>
      </ul>
      <label>
        <input type="checkbox" :checked="pulse.enabled" :disabled="saving"
               @change="toggle($event.target.checked)" />
        启用脉冲计价
      </label>
    </div>
  </div>
</template>
