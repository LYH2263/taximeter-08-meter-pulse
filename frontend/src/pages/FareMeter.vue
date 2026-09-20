<script setup>
import { ref } from 'vue'
import { postJSON } from '../api'
const distance_km = ref(8)
const slow_min = ref(3)
const night = ref(false)
const out = ref(null)
const err = ref('')
const run = async () => {
  err.value = ''
  out.value = null
  try {
    out.value = await postJSON('/api/fare', { distance_km: distance_km.value, slow_min: slow_min.value, night: night.value, persist: true })
  } catch (e) {
    err.value = '计价被拒绝：公里与低速分钟不得为负，且本次未写记录'
  }
}
</script>
<template>
  <div class="page"><h1>打表试算</h1>
    <div class="panel">
      <label>公里 <input type="number" v-model.number="distance_km" /></label>
      <label>低速分钟 <input type="number" v-model.number="slow_min" /></label>
      <label><input type="checkbox" v-model="night" /> 夜间</label>
      <button @click="run">计算</button>
    </div>
    <p v-if="err" class="err">{{ err }}</p>
    <template v-else-if="out">
      <p class="hero-num">应付 ¥{{ out.total }}</p>
      <p>起步 {{ out.start }} · 里程 {{ out.mileage }} · 低速 {{ out.slow_fee }}</p>
      <div v-if="out.pulse_enabled" class="panel">
        <p>脉冲计价：里程跳 <strong>{{ out.mileage_hops }}</strong> 跳 × {{ out.hop_distance_km }} 公里（每跳 ¥{{ out.per_mileage_hop }}）；低速跳 <strong>{{ out.slow_hops }}</strong> 跳 × {{ out.hop_slow_min }} 分钟（每跳 ¥{{ out.per_slow_hop }}），不足一跳的尾数不计。</p>
      </div>
      <p v-else class="muted">连续计价（脉冲停用，跳数 0）</p>
    </template>
  </div>
</template>
