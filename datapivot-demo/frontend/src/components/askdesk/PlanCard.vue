<template>
  <div v-if="steps.length" class="ax-plan-card">
    <div class="ax-plan-badge">执行计划</div>
    <p class="ax-plan-intro">{{ introText }}</p>

    <div class="ax-steps">
      <div v-for="step in steps" :key="step.index" class="ax-step">
        <div class="ax-step-number">{{ String(step.index).padStart(2, '0') }}</div>
        <div class="ax-step-main">
          <div class="ax-step-content">{{ step.title }}</div>
          <div v-for="(substep, subIndex) in step.substeps" :key="subIndex" class="ax-step-sub">
            {{ substep }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  route: {
    type: [String, Object],
    default: null
  }
})

const planText = computed(() => {
  const route = props.route
  if (!route) return ''

  const text = typeof route === 'string' ? route : (route.route_desc || JSON.stringify(route))
  return text
})

const introText = computed(() => {
  const lines = planText.value.split('\n').map(line => line.trim()).filter(Boolean)
  const intro = lines.find(line => !/^(步骤\s*\d+|[0-9]+[\.、]|\d+\.\d+)/.test(line))
  return intro || '好的，根据你的问题，我制定了以下执行计划：'
})

const steps = computed(() => {
  const lines = planText.value.split('\n').map(line => line.trim()).filter(Boolean)
  const list = []
  let current = null

  lines.forEach((line) => {
    if (/^(步骤\s*\d+|[0-9]+[\.、])/.test(line)) {
      const cleaned = line.replace(/^(步骤\s*\d+[:：]?|[0-9]+[\.、]\s*)/, '').trim()
      current = {
        index: list.length + 1,
        title: cleaned || `步骤 ${list.length + 1}`,
        substeps: [],
      }
      list.push(current)
      return
    }

    if (/^\d+\.\d+/.test(line) && current) {
      current.substeps.push(line.replace(/^\d+\.\d+\s*/, '').trim())
    }
  })

  return list
})
</script>

<style scoped>
.ax-plan-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  padding: 2px 0 3px;
}

.ax-plan-badge {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  height: 24px;
  padding: 0 10px;
  border-radius: 4px;
  background: #edf2f8;
  color: #425f83;
  font-size: 11px;
  font-weight: 700;
}

.ax-plan-intro {
  margin: 0;
  font-size: 14px;
  color: #111827;
  line-height: 1.72;
  font-weight: 500;
}

.ax-steps {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ax-step {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.ax-step-number {
  width: 30px;
  height: 30px;
  border-radius: 4px;
  background: linear-gradient(180deg, #edf2f8 0%, #edf2f8 100%);
  color: #425f83;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ax-step-main {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding-top: 2px;
}

.ax-step-content {
  font-size: 13px;
  color: #111827;
  line-height: 1.65;
}

.ax-step-sub {
  font-size: 12px;
  color: #9CA3AF;
  line-height: 1.62;
}
</style>
