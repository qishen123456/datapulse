<template>
  <span
    class="task-status-indicator"
    :class="`task-status--${variant}`"
    role="status"
    :aria-label="ariaLabel"
  >
    <!-- running: 环形旋转动画 + 文字 -->
    <span v-if="variant === 'running'" class="ax-status-content">
      <span class="ax-spin-ring" aria-hidden="true">
        <span class="ax-spin-ring-track"></span>
        <span class="ax-spin-ring-bar"></span>
      </span>
      <span v-if="showTextLabel" class="ax-text">{{ runningLabel }}</span>
    </span>

    <!-- completed: 绿点 + 文字 -->
    <span v-else-if="variant === 'completed'" class="ax-status-content">
      <span class="ax-dot ax-dot--success" aria-hidden="true"></span>
      <span v-if="showTextLabel" class="ax-text">{{ completedLabel }}</span>
    </span>

    <!-- pending_confirmation: 橙黄胶囊 + 文字 -->
    <span v-else-if="variant === 'pending_confirmation'" class="ax-status-content">
      <span class="ax-tag ax-tag--pending">{{ pendingLabel }}</span>
    </span>

    <!-- failed: 红点 + 文字 -->
    <span v-else-if="variant === 'failed'" class="ax-status-content">
      <span class="ax-dot ax-dot--danger" aria-hidden="true"></span>
      <span v-if="showTextLabel" class="ax-text">{{ failedLabel }}</span>
    </span>

    <!-- 耗时（仅 running） -->
    <span v-if="variant === 'running' && showTextLabel && elapsedMs > 0" class="ax-elapsed">
      {{ formattedElapsed }}
    </span>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'completed',
    validator: (v) => ['running', 'completed', 'pending_confirmation', 'failed', 'idle'].includes(v),
  },
  showTextLabel: {
    type: Boolean,
    default: false,
  },
  elapsedMs: {
    type: Number,
    default: 0,
  },
  size: {
    type: Number,
    default: 14,
  },
  // 文字标签（预留 i18n 接入点，硬编码中文 + 注释占位）
  // i18n: task.status.running
  runningLabel: {
    type: String,
    default: '执行中',
  },
  // i18n: task.status.completed
  completedLabel: {
    type: String,
    default: '已完成',
  },
  // i18n: task.status.pending_confirmation
  pendingLabel: {
    type: String,
    default: '待确认',
  },
  // i18n: task.status.failed
  failedLabel: {
    type: String,
    default: '失败',
  },
})

const formattedElapsed = computed(() => {
  const total = Math.max(0, Math.floor((props.elapsedMs || 0) / 1000))
  const m = String(Math.floor(total / 60)).padStart(2, '0')
  const s = String(total % 60).padStart(2, '0')
  return `${m}:${s}`
})

const ariaLabel = computed(() => {
  switch (props.variant) {
    case 'running':
      return '任务执行中'
    case 'pending_confirmation':
      return '任务待确认，请前往任务对话框确认结果'
    case 'failed':
      return '任务执行失败'
    case 'idle':
      return '任务空闲'
    case 'completed':
    default:
      return '任务已完成'
  }
})
</script>

<style scoped>
.task-status-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  line-height: 1;
  flex-shrink: 0;
}

.task-status-indicator.task-status--running {
  color: var(--el-color-primary, #425f83);
}

.task-status-indicator.task-status--completed {
  color: var(--el-color-success, #526b7a);
}

.task-status-indicator.task-status--pending_confirmation {
  color: var(--el-color-warning, #806b47);
}

.task-status-indicator.task-status--failed {
  color: var(--el-color-danger, #b29396);
}

.ax-status-content {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

/* 环形旋转加载 */
.ax-spin-ring {
  position: relative;
  width: 14px;
  height: 14px;
  display: inline-block;
}
.ax-spin-ring-track {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid currentColor;
  opacity: 0.2;
}
.ax-spin-ring-bar {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid transparent;
  border-top-color: currentColor;
  animation: ax-ring-spin 0.8s linear infinite;
}

@keyframes ax-ring-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 完成绿点 */
.ax-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  vertical-align: baseline;
  flex-shrink: 0;
}
.ax-dot--success {
  background: var(--el-color-success, #526b7a);
}
.ax-dot--danger {
  background: var(--el-color-danger, #b29396);
}

/* 辅助文字 */
.ax-text {
  font-size: 12px;
  color: var(--el-text-color-secondary, #909399);
  white-space: nowrap;
}

/* 待确认胶囊 */
.ax-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  line-height: 1.4;
  color: #fff;
  background: var(--el-color-warning, #806b47);
  animation: ax-breathe 2s ease-in-out infinite;
  white-space: nowrap;
}

@keyframes ax-breathe {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.85; }
}

/* 耗时 */
.ax-elapsed {
  font-size: 12px;
  color: var(--el-text-color-secondary, #909399);
  margin-left: 2px;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

/* 减少动画偏好降级 */
@media (prefers-reduced-motion: reduce) {
  .ax-spin-ring-bar {
    animation: none;
    opacity: 0.6;
  }
  .ax-tag {
    animation: none;
  }
}
</style>
