<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const t = ref(null)
const rules = ref([])
const busy = ref(false)
const err = ref('')
const load = async () => {
  t.value = await getJSON('/api/tariff')
  rules.value = (await getJSON('/api/pulse')).items
}
const toggle = async (r) => {
  busy.value = true
  err.value = ''
  try {
    await postJSON(`/api/pulse/${r.id}/enabled`, { enabled: !r.enabled_flag })
    await load()
  } catch (e) {
    err.value = String(e.message || e)
  } finally {
    busy.value = false
  }
}
onMounted(load)
</script>
<template>
  <div class="page">
    <h1>运价表</h1>
    <pre v-if="t">{{ t }}</pre>
    <h2>计价脉冲</h2>
    <p class="muted">启用后超出含公里按每 0.5 公里一跳、低速按每整分钟一跳计价，不足一跳不计；同一时间只允许一条规则启用，停用后回到连续计价。</p>
    <p v-if="err" class="err">{{ err }}</p>
    <table>
      <tr><th>#</th><th>规则</th><th>状态</th><th></th></tr>
      <tr v-for="r in rules" :key="r.id">
        <td>{{ r.id }}</td>
        <td>{{ r.name }}</td>
        <td>{{ r.enabled_flag ? '启用中' : '停用' }}</td>
        <td>
          <button :disabled="busy" @click="toggle(r)">{{ r.enabled_flag ? '停用' : '启用' }}</button>
        </td>
      </tr>
    </table>
  </div>
</template>
