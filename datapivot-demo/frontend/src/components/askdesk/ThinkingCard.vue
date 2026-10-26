<template>
  <div class="ax-thinking-card">
    <div class="ax-thinking-header" @click="$emit('toggle')">
      <span class="ax-arrow" :class="{ open: isOpen }">▶</span>
      <span class="ax-title">{{ loading ? '思考中' : '思考完成' }}</span>
      <span class="ax-header-count">{{ normalizedSteps.length }} 个节点</span>
      <span class="ax-check" :class="{ loading }">{{ loading ? '...' : '✓' }}</span>
    </div>
    <transition name="ax-collapse">
      <div v-if="isOpen" class="ax-thinking-body">
        <div v-for="(step, idx) in normalizedSteps" :key="idx" class="ax-thinking-step">
          <span class="ax-dot" :class="step.status"></span>
          <div class="ax-step-copy">
            <span class="ax-step-text">{{ step.text }}</span>
            <span v-if="step.detail" class="ax-step-detail">{{ step.detail }}</span>
          </div>
          <span class="ax-step-status" :class="step.status">{{ step.statusText }}</span>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  steps: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggle'])

const statusMap = {
  success: 'completed',
  completed: 'completed',
  running: 'running',
  pending: 'pending',
  warning: 'warning',
  error: 'error',
}

const statusTextMap = {
  completed: '已完成',
  running: '执行中',
  pending: '等待中',
  warning: '待确认',
  error: '异常',
}

const normalizedSteps = computed(() => {
  return (props.steps || []).map((step) => {
    const status = statusMap[step?.status] || 'completed'
    return {
      text: step?.text || step?.title || step?.detail || '执行步骤',
      detail: step?.detail && step?.detail !== step?.text && step?.detail !== step?.title ? step.detail : '',
      status,
      statusText: step?.statusText || statusTextMap[status],
    }
  })
})
</script>

<style scoped>
.ax-thinking-card {
  width: 100%;
  background: linear-gradient(180deg, #FFFFFF 0%, #ffffff 100%);
  border: 1px solid rgba(26, 26, 26, 0.12);
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 7px 18px rgba(0, 0, 0, 0.035);
}

.ax-thinking-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 11px 13px;
  cursor: pointer;
  transition: background 0.15s;
}

.ax-thinking-header:hover {
  background: #edf2f5;
}

.ax-arrow {
  font-size: 12px;
  color: #9CA3AF;
  transition: transform 200ms;
}

.ax-arrow.open {
  transform: rotate(90deg);
}

.ax-title {
  flex: 1;
  font-size: 13px;
  font-weight: 600;
  color: #111827;
}

.ax-header-count {
  font-size: 11px;
  color: #9CA3AF;
}

.ax-check {
  min-width: 22px;
  height: 22px;
  padding: 0 7px;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #526b7a;
  background: #edf2f5;
}

.ax-check.loading {
  color: #1A1A1A;
  background: #edf2f8;
}

.ax-thinking-body {
  background: #edf2f5;
  border-top: 1px solid rgba(26, 26, 26, 0.08);
  padding: 11px 13px 13px;
}

.ax-thinking-step {
  display: flex;
  align-items: flex-start;
  gap: 9px;
  padding: 7px 0;
}

.ax-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 6px;
}

.ax-dot.running {
  background: #1A1A1A;
  animation: pulse 1.2s ease-in-out infinite;
}

.ax-dot.completed {
  background: #526b7a;
}

.ax-dot.pending {
  background: #9CA3AF;
}

.ax-dot.warning {
  background: #806b47;
}

.ax-dot.error {
  background: #1A1A1A;
}

.ax-step-copy {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.ax-step-text {
  font-size: 12px;
  color: #111827;
  line-height: 1.55;
}

.ax-step-detail {
  font-size: 11px;
  color: #9CA3AF;
  line-height: 1.52;
}

.ax-step-status {
  padding: 2px 7px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
  white-space: nowrap;
}

.ax-step-status.completed {
  background: #edf2f5;
  color: #526b7a;
}

.ax-step-status.running {
  background: #edf2f8;
  color: #1A1A1A;
}

.ax-step-status.pending {
  background: #F3F4F6;
  color: #9CA3AF;
}

.ax-step-status.warning {
  background: #f5f2ec;
  color: #806b47;
}

.ax-step-status.error {
  background: #edf2f8;
  color: #1A1A1A;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.4;
  }
  50% {
    opacity: 1;
  }
}

.ax-collapse-enter-active,
.ax-collapse-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.ax-collapse-enter-to,
.ax-collapse-leave-from {
  opacity: 1;
  max-height: 500px;
}

.ax-collapse-enter-from,
.ax-collapse-leave-to {
  opacity: 0;
  max-height: 0;
}
</style>
