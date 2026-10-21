<template>
  <div class="ax-header">
    <div class="ax-header-left">
      <div class="ax-header-copy">
        <div class="ax-title-row">
          <div class="ax-title">当前会话</div>
          <span class="ax-workspace-badge">经营助手</span>
        </div>
      </div>
    </div>

    <div class="ax-header-right">
      <button v-if="allowNewChat" class="ax-solid-btn" type="button" @click="$emit('newChat')">新会话</button>
      <button v-if="allowTogglePanel" class="ax-text-btn" type="button" @click="$emit('togglePanel')">
        {{ showPanel ? '隐藏详情' : '显示详情' }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  showPanel: {
    type: Boolean,
    default: true
  },
  allowTogglePanel: {
    type: Boolean,
    default: true
  },
  allowNewChat: {
    type: Boolean,
    default: true
  }
})

defineEmits(['togglePanel', 'newChat', 'showHistory'])
</script>

<style scoped>
.ax-header {
  min-height: 56px;
  padding: 12px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  container-type: inline-size;
  border-bottom: 1px solid rgba(17, 24, 39, 0.06);
  background: rgba(255, 255, 255, 0.96);
  box-shadow: none;
  flex-shrink: 0;
}

.ax-header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
  flex: 1 1 320px;
}

.ax-header-copy {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.ax-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.ax-title {
  font-size: 16px;
  line-height: 1.25;
  font-weight: 800;
  color: #111827;
}

.ax-workspace-badge {
  display: inline-flex;
  align-items: center;
  height: 20px;
  padding: 0;
  border-radius: 999px;
  background: transparent;
  color: #0D9488;
  font-size: 12px;
  font-weight: 800;
  box-shadow: none;
}

.ax-header-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 0 1 auto;
  justify-content: flex-end;
  margin-left: auto;
  min-width: 0;
}

.ax-solid-btn,
.ax-text-btn {
  height: 38px;
  padding: 0 18px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 800;
  white-space: nowrap;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
}

.ax-text-btn {
  border: 1px solid rgba(17, 24, 39, 0.08);
  background: rgba(255, 255, 255, 0.88);
  color: #6B7280;
  box-shadow:
    0 8px 16px rgba(15, 23, 42, 0.03),
    inset 0 1px 0 rgba(255, 255, 255, 0.7);
}

.ax-text-btn:hover {
  color: #1A1A1A;
  border-color: rgba(17, 24, 39, 0.16);
  background: #FFFFFF;
  transform: translateY(-1px);
}

.ax-solid-btn {
  border: 1px solid rgba(13, 148, 136, 0.42);
  background: #FFFFFF;
  color: #0D9488;
  box-shadow:
    0 10px 20px rgba(13, 148, 136, 0.06),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.ax-solid-btn:hover {
  border-color: rgba(13, 148, 136, 0.58);
  background: rgba(13, 148, 136, 0.04);
  color: #0D9488;
  transform: translateY(-1px);
}

.ax-solid-btn:active,
.ax-text-btn:active {
  transform: scale(0.96);
}

@container (max-width: 760px) {
  .ax-header {
    padding: 10px 12px;
  }
}

@container (max-width: 620px) {
  .ax-workspace-badge {
    display: none;
  }

  .ax-header-right {
    width: 100%;
    justify-content: flex-start;
    margin-left: 0;
  }

  .ax-solid-btn,
  .ax-text-btn {
    height: 32px;
    padding: 0 12px;
    font-size: 10px;
  }
}

@media (max-width: 900px) {
  .ax-header {
    align-items: flex-start;
  }

  .ax-header-right {
    width: 100%;
    justify-content: flex-start;
    margin-left: 0;
  }
}
</style>
