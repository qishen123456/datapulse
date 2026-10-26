<template>
  <div class="ax-welcome">
    <div class="ax-welcome-head">
      <div class="ax-welcome-avatar">
        <svg class="ax-welcome-avatar-svg" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
          <defs>
            <linearGradient id="aiRingWelcome" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#526b7a" />
              <stop offset="100%" stop-color="#3c536e" />
            </linearGradient>
            <linearGradient id="aiDiscWelcome" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#FFFFFF" />
              <stop offset="100%" stop-color="#edf2f5" />
            </linearGradient>
          </defs>
          <circle cx="50" cy="50" r="48" fill="url(#aiDiscWelcome)" />
          <circle cx="50" cy="50" r="46" fill="none" stroke="url(#aiRingWelcome)" stroke-width="3.5" />
          <path d="M28 62 L42 40 L52 52 L62 36 L72 44" fill="none" stroke="#526b7a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" />
          <circle cx="72" cy="44" r="4.5" fill="#526b7a" />
        </svg>
      </div>
      <div class="ax-welcome-copy">
        <div class="ax-welcome-label">DataPulse AI 经营分析顾问</div>
        <div class="ax-welcome-text" :class="{ 'is-typing': isTyping }">{{ displayText }}</div>
      </div>
    </div>

    <div class="ax-quick-questions">
      <div class="ax-quick-head">
        <div>
          <div class="ax-quick-title">常用问题</div>
          <div class="ax-quick-tip">点击问题将带入所属数据集口径，你可以修改后再发送。</div>
        </div>
        <button v-if="allowRefreshQuestions" class="ax-quick-refresh" :disabled="commonQuestionsLoading" @click="$emit('refresh-questions')">
          <el-icon class="ax-quick-refresh-icon" :class="{ 'is-loading': commonQuestionsLoading }">
            <RefreshRight />
          </el-icon>
          <span>{{ commonQuestionsLoading ? '刷新中' : '换一批' }}</span>
        </button>
      </div>
      <div v-if="commonQuestions.length" class="ax-quick-list">
        <button 
          v-for="(q, i) in commonQuestions" 
          :key="q.id || `${q.dataset_id || 'auto'}-${q.question_text || q}-${i}`" 
          class="ax-quick-btn"
          :disabled="!allowQuickAsk"
          @click="$emit('quick-ask', q)"
        >
          <span class="ax-quick-dataset">{{ q.dataset_tag || q.dataset_name || '自动' }}</span>
          <span class="ax-quick-question">{{ q.question_text || q }}</span>
        </button>
      </div>
      <div v-else class="ax-quick-empty">
        {{ commonQuestionsLoading ? '正在加载推荐问题...' : '暂无可用常用问题，请先在数据集管理中为数据集维护问题池。' }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RefreshRight } from '@element-plus/icons-vue'

const props = defineProps({
  welcomeText: {
    type: String,
    default: '你好，我是你的经营分析顾问，今天有什么我可以帮助你的吗？'
  },
  commonQuestions: {
    type: Array,
    default: () => []
  },
  commonQuestionsLoading: {
    type: Boolean,
    default: false
  },
  allowQuickAsk: {
    type: Boolean,
    default: true
  },
  allowRefreshQuestions: {
    type: Boolean,
    default: true
  }
})

defineEmits(['quick-ask', 'refresh-questions'])

const displayText = ref('')
const currentIndex = ref(0)
const isTyping = ref(false)

const typeWriter = () => {
  isTyping.value = true
  const run = () => {
    if (currentIndex.value < props.welcomeText.length) {
      displayText.value += props.welcomeText[currentIndex.value]
      currentIndex.value++
      setTimeout(run, 30) // 火山引擎规格：每字30ms
    } else {
      isTyping.value = false
    }
  }
  run()
}

onMounted(() => {
  typeWriter()
})
</script>

<style scoped>
/* 新版首屏：居中 Hero + 单列推荐问题（替代原「左对齐 + 两列卡片」） */
.ax-welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 22px;
  padding: 24px 0 48px;
  max-width: 720px;
  margin: auto 0;
  width: 100%;
}

.ax-welcome-head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 0;
  border: 0;
  border-radius: 0;
  background: transparent;
  box-shadow: none;
}

.ax-welcome-avatar {
  position: relative;
  width: 44px;
  height: 44px;
  margin-top: 0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  overflow: visible;
  padding: 0;
  background: transparent;
  border: 0;
  box-shadow: 0 4px 12px rgba(66, 95, 131, 0.18);
}

.ax-welcome-avatar::before {
  content: none;
}

.ax-welcome-avatar::after {
  content: '';
  position: absolute;
  right: 1px;
  bottom: 1px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #526b7a;
  box-shadow:
    0 0 0 3px #FFFFFF,
    0 4px 9px rgba(82, 107, 122, 0.2);
}

.ax-welcome-avatar-img {
  display: none;
}

.ax-welcome-avatar-svg {
  width: 44px;
  height: 44px;
  display: block;
}

.ax-welcome-copy {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 7px;
  min-width: 0;
}

.ax-welcome-label {
  display: inline-flex;
  align-self: center;
  padding: 0;
  border-radius: 0;
  background: transparent;
  color: #425f83;
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 0;
}

.ax-welcome-text {
  max-width: 100%;
  font-size: 22px;
  font-weight: 760;
  color: #1F2937;
  line-height: 1.32;
  white-space: normal;
  text-wrap: balance;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ax-welcome-text.is-typing::after {
  content: '|';
  margin-left: 5px;
  color: rgba(66, 95, 131, 0.72);
  animation: ax-welcome-cursor-blink 1s step-end infinite;
}

.ax-quick-questions {
  margin-left: 0;
  padding-top: 0;
  width: 100%;
}

.ax-quick-head {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 16px;
}

.ax-quick-title {
  font-size: 14px;
  font-weight: 800;
  color: rgba(17, 24, 39, 0.7);
  margin-bottom: 5px;
}

.ax-quick-tip {
  margin-bottom: 0;
  font-size: 12px;
  color: #8B95A1;
  line-height: 1.45;
}

.ax-quick-refresh {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 32px;
  min-width: 84px;
  padding: 0 12px;
  border: 1px solid #bdcbd3;
  border-radius: 4px;
  background: #FFFFFF;
  color: #344652;
  font-size: 12px;
  font-weight: 700;
  line-height: 1;
  cursor: pointer;
  box-shadow: none;
  transition: border-color 0.16s ease, color 0.16s ease, background 0.16s ease, box-shadow 0.16s ease;
  white-space: nowrap;
}

.ax-quick-refresh:hover:not(:disabled) {
  border-color: #425f83;
  background: #edf2f8;
  color: #425f83;
  box-shadow: none;
}

.ax-quick-refresh:disabled {
  cursor: default;
  opacity: 0.72;
}

.ax-quick-refresh-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 13px;
  height: 13px;
  font-size: 13px;
  line-height: 1;
  transform-origin: center;
}

.ax-quick-refresh-icon.is-loading {
  animation: ax-quick-spin 0.8s linear infinite;
}

/* 单列推荐行：替代原来的两列卡片网格 */
.ax-quick-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
}

.ax-quick-btn {
  position: relative;
  text-align: left;
  min-height: 0;
  width: 100%;
  padding: 12px 40px 12px 14px;
  background: #FFFFFF;
  border: 1px solid #dce5eb;
  border-radius: 6px;
  font-size: 11px;
  color: #6B7280;
  cursor: pointer;
  transition: border-color 0.18s ease, background 0.18s ease;
  box-shadow: none;
  line-height: 1.35;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
}

.ax-quick-btn::after {
  content: '›';
  position: absolute;
  right: 18px;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(17, 24, 39, 0.38);
  font-size: 26px;
  font-weight: 300;
  line-height: 1;
}

.ax-quick-btn:hover {
  background: #f5f7f9;
  border-color: #425f83;
  color: #1A1A1A;
}

.ax-quick-btn:disabled {
  cursor: not-allowed;
  opacity: 0.58;
}

.ax-quick-dataset {
  display: inline-flex;
  flex: 0 0 auto;
  align-self: center;
  max-width: 200px;
  padding: 3px 8px;
  border-radius: 3px;
  border: 1px solid rgba(66, 95, 131, 0.32);
  background: #edf2f8;
  color: #425f83;
  font-size: 11px;
  font-weight: 700;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ax-quick-question {
  display: block;
  flex: 1 1 auto;
  min-width: 0;
  color: #111827;
  font-size: 14px;
  font-weight: 760;
  line-height: 1.35;
}

.ax-quick-empty {
  padding: 14px 16px;
  border: 1px dashed rgba(17, 24, 39, 0.12);
  border-radius: 6px;
  background: rgba(247, 248, 250, 0.82);
  color: #6B7280;
  font-size: 11px;
  line-height: 1.5;
  text-align: center;
}

@keyframes ax-quick-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes ax-welcome-cursor-blink {
  0%, 45% {
    opacity: 1;
  }
  46%, 100% {
    opacity: 0;
  }
}

@media (max-width: 900px) {
  .ax-welcome {
    padding: 28px 16px 8px;
    max-width: 100%;
  }

  .ax-quick-questions {
    margin-left: 0;
  }

  .ax-welcome-text {
    font-size: 18px;
  }

  .ax-quick-btn {
    align-items: flex-start;
    flex-direction: column;
    gap: 7px;
  }

  .ax-quick-dataset {
    align-self: flex-start;
  }
}
</style>
