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
  try {
    out.value = await postJSON('/api/fare', { distance_km: distance_km.value, slow_min: slow_min.value, night: night.value, persist: true })
  } catch (e) {
    out.value = null
    err.value = '公里或低速为负，已拒绝且未写入记录'
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
    <p v-if="err" class="error">{{ err }}</p>
    <template v-if="out">
      <p class="hero-num">¥{{ out.total }}</p>
      <p>起步 {{ out.start }} · 应付 ¥{{ out.total }}</p>
      <div v-if="out.pulse_enabled" class="panel">
        <p>脉冲计价：里程跳数 {{ out.distance_hops }} 跳（每跳 ¥{{ out.per_hop_mileage }}）·
           低速跳数 {{ out.slow_hops }} 跳（每跳 ¥{{ out.per_hop_slow }}）</p>
        <p>里程费 {{ out.mileage }} · 低速费 {{ out.slow_fee }}<template v-if="out.night"> · 夜间 {{ out.night_factor }}×（作用于跳后金额）</template></p>
      </div>
    </template>
  </div>
</template>
