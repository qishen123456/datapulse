<template>
  <div class="ax-user-message">
    <div class="ax-user-main">
      <div class="ax-user-bubble">
        <template v-if="segments">
          <template v-for="(seg, i) in segments" :key="i">
            <span
              v-if="seg.slot"
              class="ax-user-span"
              :title="`${seg.slot === 'node' ? '对象' : '指标'}：${seg.resolved}`"
            >{{ seg.text }}</span>
            <template v-else>{{ seg.text }}</template>
          </template>
        </template>
        <template v-else>{{ content }}</template>
      </div>
      <div v-if="allowCopy || allowEdit || allowRerun" class="ax-user-actions" aria-label="问题操作">
        <el-tooltip v-if="allowCopy" content="复制" placement="bottom" :show-after="180">
          <button class="ax-user-action" type="button" aria-label="复制问题" @click="$emit('copy')">
            <el-icon><DocumentCopy /></el-icon>
          </button>
        </el-tooltip>
        <el-tooltip v-if="allowEdit" content="修改" placement="bottom" :show-after="180">
          <button
            class="ax-user-action"
            type="button"
            aria-label="修改问题"
            :disabled="disabled"
            @click="$emit('edit')"
          >
            <el-icon><Edit /></el-icon>
          </button>
        </el-tooltip>
        <el-tooltip v-if="allowRerun" content="重新问" placement="bottom" :show-after="180">
          <button
            class="ax-user-action"
            type="button"
            aria-label="重新问"
            :disabled="disabled"
            @click="$emit('rerun')"
          >
            <el-icon><RefreshRight /></el-icon>
          </button>
        </el-tooltip>
      </div>
    </div>
    <div class="ax-user-avatar" aria-label="用户头像">
      <svg class="ax-user-avatar-svg" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
        <defs>
          <linearGradient id="userAvatarFillChat" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#14B8A6" />
            <stop offset="100%" stop-color="#0F766E" />
          </linearGradient>
        </defs>
        <circle cx="50" cy="50" r="50" fill="url(#userAvatarFillChat)" />
        <circle cx="50" cy="39" r="15" fill="#FFFFFF" fill-opacity="0.96" />
        <path d="M21 80c3.2-16.8 14.2-25 29-25s25.8 8.2 29 25" fill="none" stroke="#FFFFFF" stroke-opacity="0.96" stroke-width="10" stroke-linecap="round" />
      </svg>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { DocumentCopy, Edit, RefreshRight } from '@element-plus/icons-vue'

const props = defineProps({
  content: {
    type: String,
    default: ''
  },
  userName: {
    type: String,
    default: '用户'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  allowCopy: {
    type: Boolean,
    default: true
  },
  allowEdit: {
    type: Boolean,
    default: true
  },
  allowRerun: {
    type: Boolean,
    default: true
  },
  // 解析条 span 框出（parse-bar-design.md v1）：[{start, end, slot, resolved_value}]
  spans: {
    type: Array,
    default: null
  }
})

defineEmits(['copy', 'edit', 'rerun'])

// 按 spans 的 start/end 把问句切成 普通文本/高亮片段 段；区间无效或重叠时回退纯文本
const segments = computed(() => {
  const spans = (props.spans || [])
    .filter(s => Number.isInteger(s.start) && Number.isInteger(s.end) && s.end > s.start)
    .sort((a, b) => a.start - b.start)
  if (!spans.length || !props.content) return null
  const segs = []
  let cursor = 0
  for (const s of spans) {
    if (s.start < cursor || s.end > props.content.length) return null // 重叠/越界 → 回退纯文本
    if (s.start > cursor) segs.push({ text: props.content.slice(cursor, s.start) })
    segs.push({ text: props.content.slice(s.start, s.end), slot: s.slot, resolved: s.resolved_value })
    cursor = s.end
  }
  if (cursor < props.content.length) segs.push({ text: props.content.slice(cursor) })
  return segs
})
</script>

<style scoped>
.ax-user-message {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  justify-content: flex-end;
  margin: 10px 0;
}

.ax-user-main {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  max-width: 70%;
}

.ax-user-avatar {
  width: 40px;
  height: 40px;
  position: relative;
  overflow: visible;
  background: transparent;
  color: #475569;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 0;
  box-shadow: 0 4px 12px rgba(15, 118, 110, 0.22);
}

.ax-user-avatar::before {
  content: none;
}

.ax-user-avatar::after {
  content: '';
  position: absolute;
  right: 0;
  bottom: 0;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #10B981;
  box-shadow:
    0 0 0 2.5px #FFFFFF,
    0 2px 6px rgba(16, 185, 129, 0.25);
}

.ax-user-avatar-svg {
  width: 40px;
  height: 40px;
  display: block;
}

.ax-user-bubble {
  padding: 12px 18px;
  background: linear-gradient(135deg, #386553 0%, #294e3e 100%);
  color: #ffffff;
  border: none;
  border-radius: 8px 8px 6px 8px;
  font-size: 15px;
  line-height: 1.7;
  word-break: break-word;
  box-shadow:
    0 6px 16px rgba(15, 118, 110, 0.18),
    0 2px 5px rgba(15, 118, 110, 0.08);
}

/* 解析片段框出（解析条 v1）：红底气泡上的白边半透框 */
.ax-user-span {
  display: inline-block;
  padding: 0 4px;
  margin: 0 1px;
  border: 1px solid rgba(255, 255, 255, 0.85);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.16);
  cursor: default;
}

.ax-user-actions {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  min-height: 28px;
  margin-top: 6px;
  padding: 2px;
  opacity: 0;
  pointer-events: none;
  transform: translateY(-3px);
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.ax-user-message:hover .ax-user-actions,
.ax-user-actions:focus-within {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0);
}

.ax-user-action {
  width: 28px;
  height: 28px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.98);
  color: #64748B;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.2s ease;
}

.ax-user-action:hover:not(:disabled) {
  color: #294e3e;
  border-color: rgba(29, 78, 216, 0.22);
  background: #ffffff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(15, 118, 110, 0.12);
}

.ax-user-action:disabled {
  cursor: not-allowed;
  opacity: 0.42;
  box-shadow: none;
}

.ax-user-action :deep(.el-icon) {
  font-size: 14px;
}

@media (max-width: 720px) {
  .ax-user-main {
    max-width: 82%;
  }
}
</style>
