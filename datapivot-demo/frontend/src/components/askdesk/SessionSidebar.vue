<template>
  <aside class="doubao-sidebar" :class="{ 'is-collapsed': isCollapsed }">
    <!-- 顶部操作区：收起按钮 + 新会话按钮 -->
    <div class="sidebar-top">
      <div class="sidebar-top-header">
        <button
          class="sidebar-toggle-btn"
          type="button"
          :title="isCollapsed ? '展开会话侧边栏' : '收起侧边栏'"
          @click="toggleCollapse"
        >
          <!-- 豆包式分栏折叠图标 -->
          <svg class="icon-toggle" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="3" ry="3"/>
            <line x1="9" y1="3" x2="9" y2="21"/>
          </svg>
        </button>
        <span v-if="!isCollapsed" class="sidebar-brand-title">历史会话</span>
      </div>

      <!-- 新建对话大按钮 -->
      <button
        class="new-chat-btn"
        type="button"
        :title="isCollapsed ? '发起新对话' : ''"
        @click="$emit('newChat')"
      >
        <svg class="new-chat-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        <span v-if="!isCollapsed" class="new-chat-text">新对话</span>
      </button>
    </div>

    <!-- 中间：历史会话列表 -->
    <div class="sidebar-body" v-if="!isCollapsed">
      <!-- 列表标题 -->
      <div class="session-group-header">
        <span class="session-group-title">最近记录</span>
        <span class="session-group-badge">{{ sessions.length }}</span>
      </div>

      <div v-if="sessions.length === 0" class="sidebar-empty">
        <svg class="empty-icon" viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#94a3b8" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
        <span>暂无历史会话</span>
      </div>

      <div v-else class="session-list">
        <div
          v-for="item in sessions"
          :key="item.id"
          class="session-item"
          :class="{ 'is-active': item.id === activeSessionId }"
          @click="$emit('selectSession', item)"
        >
          <!-- 消息气泡图标 -->
          <svg class="session-item-icon" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>

          <!-- 会话标题 -->
          <span class="session-item-title" :title="item.title">{{ item.title || '新对话' }}</span>

          <!-- 删除按钮 -->
          <button
            class="session-delete-btn"
            type="button"
            title="删除此会话"
            @click.stop="$emit('deleteSession', item, $event)"
          >
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- 折叠态极简显示 -->
    <div v-else class="collapsed-body">
      <div
        v-for="item in sessions.slice(0, 10)"
        :key="item.id"
        class="collapsed-item"
        :class="{ 'is-active': item.id === activeSessionId }"
        :title="item.title"
        @click="$emit('selectSession', item)"
      >
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
      </div>
    </div>

    <!-- 底部区域：清空历史或版本说明 -->
    <div class="sidebar-footer" v-if="!isCollapsed">
      <button
        v-if="sessions.length > 0 && allowClear"
        class="clear-all-btn"
        type="button"
        @click="$emit('clearAll')"
      >
        <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="3 6 5 6 21 6"/>
          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
        </svg>
        <span>清空全部记录</span>
      </button>
      <div v-else class="sidebar-tip">DataPulse 脉策问数</div>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  sessions: {
    type: Array,
    default: () => []
  },
  activeSessionId: {
    type: String,
    default: ''
  },
  allowClear: {
    type: Boolean,
    default: true
  }
})

defineEmits(['newChat', 'selectSession', 'deleteSession', 'clearAll'])

const isCollapsed = ref(false)

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}
</script>

<style scoped>
.doubao-sidebar {
  width: 250px;
  flex: 0 0 250px;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fbfcfd;
  border-right: 1px solid #eef2f6;
  transition: width 0.25s cubic-bezier(0.2, 0, 0, 1), flex-basis 0.25s cubic-bezier(0.2, 0, 0, 1);
  user-select: none;
  z-index: 10;
  box-sizing: border-box;
}

.doubao-sidebar.is-collapsed {
  width: 58px;
  flex: 0 0 58px;
  background: #f8fafc;
}

/* 顶部操作区 */
.sidebar-top {
  padding: 12px 14px 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.doubao-sidebar.is-collapsed .sidebar-top {
  padding: 12px 8px;
  align-items: center;
}

.sidebar-top-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 32px;
}

.sidebar-brand-title {
  font-size: 13px;
  font-weight: 700;
  color: #334155;
  letter-spacing: -0.01em;
}

.sidebar-toggle-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 1px solid transparent;
  background: transparent;
  color: #64748b;
  cursor: pointer;
  transition: all 0.15s ease;
}

.sidebar-toggle-btn:hover {
  background: #f1f5f9;
  color: #0d9488;
}

/* 新对话按钮 */
.new-chat-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 38px;
  padding: 0 14px;
  border: 1px solid rgba(13, 148, 136, 0.3);
  border-radius: 8px;
  background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);
  color: #ffffff;
  font-size: 13.5px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(13, 148, 136, 0.22);
  transition: all 0.2s ease;
}

.new-chat-btn:hover {
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.35);
  transform: translateY(-1px);
}

.new-chat-btn:active {
  transform: scale(0.98);
}

.doubao-sidebar.is-collapsed .new-chat-btn {
  width: 38px;
  height: 38px;
  padding: 0;
  border-radius: 8px;
}

/* 中间滚动区 */
.sidebar-body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 10px 10px 14px;
  display: flex;
  flex-direction: column;
}

.sidebar-body::-webkit-scrollbar {
  width: 4px;
}

.sidebar-body::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.session-group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 8px 8px;
}

.session-group-title {
  font-size: 11.5px;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.session-group-badge {
  font-size: 11px;
  color: #0d9488;
  background: rgba(13, 148, 136, 0.1);
  padding: 1px 6px;
  border-radius: 10px;
  font-weight: 600;
}

.session-list {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

/* 会话条目 */
.session-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 9px;
  height: 38px;
  padding: 0 10px;
  border-radius: 7px;
  border: 1px solid transparent;
  color: #475569;
  cursor: pointer;
  transition: all 0.15s ease;
}

.session-item:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.session-item-icon {
  flex-shrink: 0;
  color: #94a3b8;
  transition: color 0.15s ease;
}

.session-item:hover .session-item-icon {
  color: #0d9488;
}

.session-item-title {
  flex: 1;
  min-width: 0;
  font-size: 13px;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
}

/* 激活态：绿色色块 + 醒目文字 */
.session-item.is-active {
  background: #f0fdfa;
  border-color: rgba(13, 148, 136, 0.25);
  color: #0f766e;
  font-weight: 700;
}

.session-item.is-active .session-item-icon {
  color: #0d9488;
}

.session-item.is-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  bottom: 8px;
  width: 3px;
  border-radius: 0 3px 3px 0;
  background: #0d9488;
}

/* 删除按钮 */
.session-delete-btn {
  display: none;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 4px;
  border: 0;
  background: transparent;
  color: #94a3b8;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.15s ease;
}

.session-item:hover .session-delete-btn {
  display: inline-flex;
}

.session-delete-btn:hover {
  background: #fee2e2;
  color: #dc2626;
}

/* 空状态 */
.sidebar-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 10px;
  gap: 10px;
  color: #94a3b8;
  font-size: 12.5px;
}

/* 折叠态会话图标列表 */
.collapsed-body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 10px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.collapsed-item {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  cursor: pointer;
  transition: all 0.15s ease;
}

.collapsed-item:hover {
  background: #f1f5f9;
  color: #0d9488;
}

.collapsed-item.is-active {
  background: #f0fdfa;
  color: #0d9488;
  border: 1px solid rgba(13, 148, 136, 0.3);
}

/* 底部区域 */
.sidebar-footer {
  padding: 10px 14px;
  border-top: 1px solid rgba(0, 0, 0, 0.04);
  display: flex;
  align-items: center;
  justify-content: center;
}

.clear-all-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: #ffffff;
  color: #64748b;
  font-size: 11.5px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.clear-all-btn:hover {
  border-color: #fca5a5;
  background: #fef2f2;
  color: #dc2626;
}

.sidebar-tip {
  font-size: 11px;
  color: #94a3b8;
}
</style>
