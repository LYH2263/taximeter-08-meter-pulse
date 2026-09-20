<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getJSON, postJSON } from '../api'
const route = useRoute()
const trip = ref(null)
const fare = ref(null)
const load = async () => {
  trip.value = await getJSON(`/api/trips/${route.params.id}`)
  // 只读试算：persist=false 不写记录；展示的是按当前规则重算的结果
  fare.value = await postJSON('/api/fare', { distance_km: trip.value.distance_km, slow_min: trip.value.slow_min, night: !!trip.value.night, trip_id: trip.value.id, persist: false })
}
onMounted(load); watch(() => route.params.id, load)
</script>
<template>
  <div class="page" v-if="trip"><h1>{{ trip.label }}</h1>
    <p class="hero-num" v-if="fare">¥{{ fare.total }}</p>
    <p v-if="fare">起步 {{ fare.start }} · 里程 {{ fare.mileage }} · 低速 {{ fare.slow_fee }}</p>
    <div v-if="fare?.pulse_enabled" class="panel">
      <p>只读试算（不落记录）：里程跳 {{ fare.mileage_hops }} 跳 × {{ fare.hop_distance_km }} 公里（每跳 ¥{{ fare.per_mileage_hop }}）；低速跳 {{ fare.slow_hops }} 跳 × {{ fare.hop_slow_min }} 分钟（每跳 ¥{{ fare.per_slow_hop }}）。</p>
    </div>
    <p v-else-if="fare" class="muted">连续计价（脉冲停用，跳数 0）</p>
  </div>
</template>
