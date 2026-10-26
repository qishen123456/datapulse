<template>
  <div class="cmp" :class="{ 'is-running': isRunning }">
    <div class="cmp-dock">
      <span v-if="isRunning" class="cmp-activity-ribbon" aria-hidden="true"></span>
      <div v-if="isRunning && !disabled" class="cmp-draft-hint"><span class="cmp-draft-spark" aria-hidden="true">✦</span> 分析继续，你可以先写下一问<span>Enter 排队 · Shift + Enter 换行</span></div>
      <!-- 输入区：通栏第一行，占满全宽，无内框 -->
      <div class="cmp-input-zone">
        <div v-if="disabled" class="cmp-running-mask" aria-hidden="true">
          <span class="cmp-running-line"></span>
          <span class="cmp-running-text">正在查看历史任务，请先返回当前对话</span>
        </div>
        <textarea
          ref="inputRef"
          v-model="modelQuery"
          class="cmp-textarea"
          :placeholder="flow==='advanced'?'描述你要深入分析的问题，例如：本季度利润变化由哪些因素推动？':'输入业务问题，例如：2026年9月各分公司销气量排名'"
          rows="1"
          :disabled="disabled"
          @input="autoGrow"
          @keydown="handleKeydown"
        ></textarea>
      </div>

      <!-- 指挥条：左=数据集/路由状态，右=模型/语音/发送（与旧版顶部pill+右下圆钮完全不同的排布） -->
      <div class="cmp-commandbar">
        <div class="cmp-command-left">
          <el-select
            v-if="allowDatasetSelect"
            v-model="datasetSelectValue"
            placeholder="智能选择数据集"
            size="small"
            class="cmp-dataset-select"
            :class="{ 'is-locked': !!selectedDatasetMeta }"
            popper-class="ax-ds-popper ax-dataset-popper"
            placement="top-start"
            :fallback-placements="['top-start']"
            @change="$emit('datasetChange', $event || null)"
          >
            <template #prefix>
              <span class="cmp-ds-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" focusable="false">
                  <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
                  <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
                  <path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"></path>
                </svg>
              </span>
            </template>
            <el-option label="智能选择数据集" value="">
              <div class="ax-ds-option ax-ds-option-auto">
                <div class="ax-ds-option-main">
                  <div class="ax-ds-option-title">智能选择数据集（自动路由）</div>
                </div>
              </div>
            </el-option>
            <el-option
              v-for="d in datasets"
              :key="d.id"
              :label="d.dataset_name"
              :value="d.id"
            >
              <div class="ax-ds-option">
                <div class="ax-ds-option-main">
                  <div class="ax-ds-option-title">{{ d.dataset_name }}</div>
                </div>
              </div>
            </el-option>
          </el-select>

          <div v-if="statusText" class="cmp-status" :class="statusTone">
            <span class="cmp-status-dot"></span>
            <span class="cmp-status-text">{{ statusText }}</span>
            <span v-if="statusElapsed" class="cmp-status-time">{{ statusElapsed }}</span>
          </div>
          <span v-else-if="allowDatasetSelect" class="cmp-route-hint">
            <span class="cmp-route-dot" :class="{ 'is-locked': !!selectedDatasetMeta }"></span>
            {{ selectedDatasetMeta ? '已锁定该数据集' : '将按问题自动路由' }}
          </span>
        </div>

        <div class="cmp-command-right">
          <el-select
            v-if="allowModelSelect"
            v-model="modelSelectValue"
            placeholder="Auto"
            size="small"
            class="cmp-model-select"
            popper-class="ax-ds-popper ax-model-popper"
            placement="top-end"
            :fallback-placements="['top-end']"
          >
            <template #prefix>
              <span class="cmp-model-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" focusable="false">
                  <path d="M13.4 2.4 5.9 13.1h5.2l-.6 8.5 7.6-11h-5.3l.6-8.2Z" fill="currentColor" />
                </svg>
              </span>
            </template>
            <el-option label="Auto" value="">
              <div class="ax-ds-option ax-model-option ax-ds-option-auto">
                <div class="ax-ds-option-main">
                  <div class="ax-ds-option-title">Auto</div>
                </div>
              </div>
            </el-option>
            <el-option
              v-for="m in aiModels"
              :key="m.id"
              :label="m.name"
              :value="m.id"
            >
              <div
                class="ax-ds-option ax-model-option"
                :class="{ 'is-default-model': m.is_default }"
              >
                <div class="ax-ds-option-main">
                  <div class="ax-ds-option-title ax-model-option-title">
                    <div class="ax-model-option-left">
                      <span class="ax-model-icon-mini" aria-hidden="true">
                        <svg viewBox="0 0 24 24" focusable="false"><path d="M13.4 2.4 5.9 13.1h5.2l-.6 8.5 7.6-11h-5.3l.6-8.2Z" fill="currentColor"/></svg>
                      </span>
                      <span class="ax-model-option-name">{{ m.name }}</span>
                      <span v-if="m.is_default" class="ax-model-default-badge">默认</span>
                    </div>
                    <div class="ax-model-option-right">
                      <span v-if="m.channel_display_name" class="ax-model-option-channel">
                        {{ m.channel_display_name }}
                      </span>
                      <span v-if="m.is_default" class="ax-model-check" aria-hidden="true">✓</span>
                    </div>
                  </div>
                </div>
              </div>
            </el-option>
          </el-select>

          <!-- 语音输入：点击开始/结束，移动端按住说话 -->
          <button
            v-if="canRecord && recorderState === 'idle' && !isRunning && !disabled"
            class="cmp-icon-btn"
            aria-label="语音输入"
            title="语音输入"
            @click="handleMicClick"
            @touchstart.prevent="handleMicTouchStart"
            @touchend.prevent="handleMicTouchEnd"
            @touchmove="handleMicTouchMove"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" focusable="false">
              <rect x="9" y="2" width="6" height="12" rx="2"></rect>
              <path d="M5 10a7 7 0 0 0 14 0"></path>
              <line x1="12" y1="17" x2="12" y2="22"></line>
            </svg>
          </button>

          <div
            v-else-if="recorderState !== 'idle'"
            class="cmp-recorder-pill"
            :class="{ 'is-cancel-pending': touchCancelPending, 'is-clickable': recorderState === 'recording' && !isTouchDevice, 'is-recording': recorderState === 'recording' }"
            :title="recorderState === 'recording' && !isTouchDevice ? '点击结束并识别，Esc 取消' : ''"
            @click="handlePillClick"
          >
            <span class="cmp-recorder-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" focusable="false">
                <rect x="9" y="2" width="6" height="12" rx="2"></rect>
                <path d="M5 10a7 7 0 0 0 14 0"></path>
                <line x1="12" y1="17" x2="12" y2="22"></line>
              </svg>
            </span>
            <span class="cmp-recorder-timer">{{ recordTimerText }}</span>
            <span v-if="recorderState === 'recording' && isTouchDevice" class="cmp-recorder-hint">
              {{ touchCancelPending ? '松手取消' : '松手结束，上滑取消' }}
            </span>
            <span v-else-if="recorderState === 'transcribing'" class="cmp-recorder-hint">识别中…</span>
          </div>

          <button
            v-if="allowSend"
            class="cmp-send-btn"
            :class="{ 'is-disabled': recorderState !== 'idle' || !hasQuery || disabled, 'is-queue-send': queueMode }"
            :disabled="recorderState !== 'idle' || !hasQuery || disabled"
            :aria-label="queueMode ? '加入问数队列' : '发送问题'"
            @click="recorderState === 'idle' && $emit('send')"
          >
            <svg class="cmp-send-plane" viewBox="0 0 24 24" fill="currentColor" focusable="false">
              <path d="M9.78 18.65l.28-4.28 7.68-6.95c.33-.29-.07-.45-.51-.16l-9.5 5.98-4.15-1.3c-.9-.28-.92-.9.19-1.33L20.2 3.44c.73-.27 1.37.17 1.13 1.2l-2.8 13.23c-.2 1-.8 1.25-1.63.78l-4.25-3.13-2.05 1.98-1.02 1.15z" />
            </svg>
            <span class="cmp-send-text">{{ queueMode ? '排队' : '发送' }}</span>
            <kbd class="cmp-send-kbd">↵</kbd>
          </button>

          <button
            v-if="isRunning && allowStop"
            class="cmp-stop-btn"
            aria-label="停止执行"
            @click="$emit('stop')"
          >
            <span class="cmp-stop-icon" aria-hidden="true"></span>
            <span class="cmp-send-text">停止</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { getAsrConfig, transcribeAudio } from '../../api/index'

const modelQuery = defineModel('query', { type: String, default: '' })
const modelDatasetId = defineModel('datasetId', { default: null })
const modelModelId = defineModel('modelId', { default: null })

const props = defineProps({
  flow:{type:String,default:'basic'},
  queueMode:Boolean,
  datasets: {
    type: Array,
    default: () => []
  },
  aiModels: {
    type: Array,
    default: () => []
  },
  isRunning: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  allowSend: {
    type: Boolean,
    default: true
  },
  allowStop: {
    type: Boolean,
    default: true
  },
  allowDatasetSelect: {
    type: Boolean,
    default: true
  },
  allowModelSelect: {
    type: Boolean,
    default: true
  },
  statusText: {
    type: String,
    default: ''
  },
  statusElapsed: {
    type: String,
    default: ''
  },
  statusTone: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['send', 'stop', 'datasetChange'])

const inputRef = ref(null)

const datasetSelectValue = computed({
  get: () => modelDatasetId.value ?? '',
  set: value => { modelDatasetId.value = value === '' ? null : value }
})

const modelSelectValue = computed({
  get: () => {
    // bug 2026-08-26：aiModels 异步加载未到位时，modelModelId 已是有效 ID（如 13），
    // el-select 找不到匹配 option 会把原始 ID 当文字渲染（"神马13" 闪烁）。
    // 守卫：列表未就绪 或 当前 ID 不在列表中 → 返回 '' 显示 placeholder "Auto"
    // 注意：props 必须用 props.aiModels 访问（defineProps 对象方式下裸写 aiModels 是未定义变量，
    // 上一版因此 ReferenceError → 点击模型选项无反应，2026-08-26 二次修复）
    if (!modelModelId.value) return ''
    const models = props.aiModels || []
    if (models.length === 0) return ''
    if (!models.some(m => String(m.id) === String(modelModelId.value))) return ''
    return modelModelId.value
  },
  set: value => { modelModelId.value = value === '' ? null : value }
})

const selectedDatasetMeta = computed(() => (
  (props.datasets || []).find(item => Number(item?.id) === Number(modelDatasetId.value)) || null
))

const hasQuery = computed(() => String(modelQuery.value || '').trim().length > 0)

const resizeTextarea = () => {
  const textarea = inputRef.value
  if (!textarea) return
  // 先收再撑：随内容自适应增高，最高 160px 后内部滚动
  textarea.style.height = '24px'
  const next = Math.min(Math.max(textarea.scrollHeight, 24), 160)
  textarea.style.height = `${next}px`
  textarea.style.overflowY = textarea.scrollHeight > 160 ? 'auto' : 'hidden'
}

const autoGrow = () => {
  resizeTextarea()
}

const handleKeydown = (event) => {
  if (event.key !== 'Enter') return
  if (event.shiftKey) return
  if (event.isComposing || event.keyCode===229 || props.disabled || !props.allowSend) return
  if (recorderState.value !== 'idle') return // 录音/识别中不触发发送
  event.preventDefault()
  emit('send')
}

// ===================== 语音输入（ASR，方案见 docs/voice-input-design-2026-08-26.md） =====================
// 飞书 file_recognize 只收 16k PCM：用 AudioWorklet 直接采 PCM，不走 MediaRecorder（webm 不被接受）
const recorderState = ref('idle') // idle | recording | transcribing
const asrEnabled = ref(false)
const asrMaxDurationSec = ref(60)
const recordSeconds = ref(0)
const touchCancelPending = ref(false)
// 只用主指针判定触屏：带触屏的 Windows 笔记本 'ontouchstart' 也为 true，
// 会被误判成移动端导致桌面点击失效（2026-08-27 实测 bug）
const isTouchDevice = !!(window.matchMedia && window.matchMedia('(pointer: coarse)').matches)

const canRecord = computed(() => (
  asrEnabled.value
  && !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
  && typeof (window.AudioContext || window.webkitAudioContext) !== 'undefined'
))

const recordTimerText = computed(() => {
  const s = recordSeconds.value
  return `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`
})

let audioCtx = null
let mediaStream = null
let workletNode = null
let pcmChunks = []
let recordTimer = null
let recordMaxTimer = null
let recordStartedAt = 0
let touchStartY = 0

const WORKLET_CODE = `
class PCMCollector extends AudioWorkletProcessor {
  process(inputs) {
    const input = inputs[0]
    if (input && input[0] && input[0].length) this.port.postMessage(input[0].slice(0))
    return true
  }
}
registerProcessor('pcm-collector', PCMCollector)
`

const startRecording = async () => {
  if (recorderState.value !== 'idle') return
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true })
  } catch (e) {
    ElMessage.warning('请允许浏览器使用麦克风')
    return
  }
  try {
    const Ctx = window.AudioContext || window.webkitAudioContext
    audioCtx = new Ctx()
    const source = audioCtx.createMediaStreamSource(mediaStream)
    const workletUrl = URL.createObjectURL(new Blob([WORKLET_CODE], { type: 'application/javascript' }))
    await audioCtx.audioWorklet.addModule(workletUrl)
    URL.revokeObjectURL(workletUrl)
    workletNode = new AudioWorkletNode(audioCtx, 'pcm-collector')
    pcmChunks = []
    workletNode.port.onmessage = (e) => { pcmChunks.push(e.data) }
    // 不接 destination 时 Chrome 不驱动 process()；接零增益节点避免外放回录
    const mute = audioCtx.createGain()
    mute.gain.value = 0
    source.connect(workletNode)
    workletNode.connect(mute)
    mute.connect(audioCtx.destination)
  } catch (e) {
    cleanupAudio()
    ElMessage.error('当前浏览器不支持录音')
    return
  }
  recordStartedAt = Date.now()
  recordSeconds.value = 0
  touchCancelPending.value = false
  recorderState.value = 'recording'
  recordTimer = setInterval(() => {
    recordSeconds.value = Math.floor((Date.now() - recordStartedAt) / 1000)
  }, 500)
  recordMaxTimer = setTimeout(() => finishRecording(), asrMaxDurationSec.value * 1000)
}

const cleanupAudio = () => {
  if (recordTimer) { clearInterval(recordTimer); recordTimer = null }
  if (recordMaxTimer) { clearTimeout(recordMaxTimer); recordMaxTimer = null }
  if (workletNode) { try { workletNode.disconnect() } catch (e) {} workletNode = null }
  if (mediaStream) { mediaStream.getTracks().forEach(t => t.stop()); mediaStream = null }
  if (audioCtx) { audioCtx.close().catch(() => {}); audioCtx = null }
}

const cancelRecording = () => {
  cleanupAudio()
  pcmChunks = []
  recorderState.value = 'idle'
}

const mergeChunks = (chunks) => {
  const total = chunks.reduce((n, c) => n + c.length, 0)
  const merged = new Float32Array(total)
  let offset = 0
  for (const c of chunks) { merged.set(c, offset); offset += c.length }
  return merged
}

const downsampleTo16k = (samples, srcRate) => {
  if (srcRate === 16000) return samples
  const ratio = srcRate / 16000
  const out = new Float32Array(Math.floor(samples.length / ratio))
  for (let i = 0; i < out.length; i++) {
    out[i] = samples[Math.min(samples.length - 1, Math.floor(i * ratio))]
  }
  return out
}

const floatTo16BitPcmBase64 = (samples) => {
  const buf = new ArrayBuffer(samples.length * 2)
  const view = new DataView(buf)
  for (let i = 0; i < samples.length; i++) {
    const s = Math.max(-1, Math.min(1, samples[i]))
    view.setInt16(i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true)
  }
  const bytes = new Uint8Array(buf)
  let binary = ''
  const step = 0x8000
  for (let i = 0; i < bytes.length; i += step) {
    binary += String.fromCharCode.apply(null, bytes.subarray(i, i + step))
  }
  return btoa(binary)
}

const finishRecording = async () => {
  if (recorderState.value !== 'recording') return
  const srcRate = audioCtx ? audioCtx.sampleRate : 48000
  const chunks = pcmChunks
  cleanupAudio()
  pcmChunks = []
  const samples = downsampleTo16k(mergeChunks(chunks), srcRate)
  // 少于 0.3 秒视为误触
  if (!samples || samples.length < 16000 * 0.3) {
    recorderState.value = 'idle'
    return
  }
  recorderState.value = 'transcribing'
  try {
    const res = await transcribeAudio(floatTo16BitPcmBase64(samples))
    const text = String(res?.text || '').trim()
    if (text) {
      const cur = String(modelQuery.value || '').trimEnd()
      modelQuery.value = cur ? `${cur} ${text}` : text
      nextTick(() => { resizeTextarea(); inputRef.value && inputRef.value.focus() })
    } else {
      ElMessage.info('未检测到语音内容，请重试。')
    }
  } catch (e) {
    ElMessage.error(e?.response?.data?.error || '语音识别失败，请稍后重试')
  } finally {
    recorderState.value = 'idle'
  }
}

// 桌面端：点击开始；录音条点击=结束识别，Esc=取消（谷歌式极简）
const handleMicClick = () => {
  if (isTouchDevice) return // 触屏走 press-hold，避免 touch 合成 click 冲突
  startRecording()
}
const handlePillClick = () => {
  if (isTouchDevice) return
  if (recorderState.value === 'recording') finishRecording()
}
const handleEscKey = (e) => {
  if (e.key === 'Escape' && recorderState.value === 'recording') cancelRecording()
}
// 移动端：按住说话，上滑取消
const handleMicTouchStart = (e) => {
  touchStartY = e.touches && e.touches[0] ? e.touches[0].clientY : 0
  startRecording()
}
const handleMicTouchMove = (e) => {
  if (recorderState.value !== 'recording') return
  const y = e.touches && e.touches[0] ? e.touches[0].clientY : touchStartY
  touchCancelPending.value = (touchStartY - y) > 60
}
const handleMicTouchEnd = () => {
  if (recorderState.value !== 'recording') return
  if (touchCancelPending.value) cancelRecording()
  else finishRecording()
}

watch(modelQuery, () => nextTick(resizeTextarea))

onMounted(() => {
  nextTick(() => {
    resizeTextarea()
    inputRef.value?.focus()
  })
  getAsrConfig()
    .then((res) => {
      asrEnabled.value = !!(res && res.enabled)
      if (res && res.max_duration_sec) asrMaxDurationSec.value = res.max_duration_sec
    })
    .catch(() => { asrEnabled.value = false })
  window.addEventListener('keydown', handleEscKey)
})

onUnmounted(() => {
  // 组件销毁时释放麦克风，避免录音中路由跳走导致设备占用
  window.removeEventListener('keydown', handleEscKey)
  cleanupAudio()
})
</script>

<style scoped>
/* ============ 贴底指挥台输入区（2026-10 二次重设计：通栏/锐角/方钮） ============ */
.cmp {
  width: 100%;
  margin: 0;
  box-sizing: border-box;
  container-type: inline-size;
}

/* 通栏贴底：零圆角、零浮起，仅靠顶部双线与内容区分隔 */
.cmp-dock {
  position: relative;
  background: #FFFFFF;
  border-top: 2px solid #dbe3ed;
  padding: 12px 18px 10px;
  transition: border-color 0.18s ease, background 0.18s ease;
}

.cmp-dock:focus-within {
  border-top-color: #425f83;
  background: #FFFFFF;
}

.cmp.is-running .cmp-dock {
  border-top-color: #8297a4;
  background: #f5f7f9;
}

/* ---------- 输入区（第一行，占满全宽） ---------- */
.cmp-input-zone {
  position: relative;
  padding: 0 2px;
}

.cmp-textarea {
  display: block;
  width: 100%;
  min-height: 26px;
  max-height: 160px;
  padding: 2px 0;
  margin: 0;
  border: none;
  outline: none !important;
  appearance: none;
  -webkit-appearance: none;
  box-shadow: none !important;
  background: transparent;
  resize: none;
  font-size: 15px;
  line-height: 1.6;
  color: #344652;
  caret-color: var(--brand-primary, #425f83);
  font-family: inherit;
}

.cmp-textarea::placeholder {
  color: #93A3A0;
  font-weight: 450;
}

.cmp-textarea:disabled {
  color: rgba(148, 163, 160, 0.4);
  cursor: not-allowed;
  caret-color: transparent;
  -webkit-text-fill-color: rgba(148, 163, 160, 0.4);
}

/* 运行中遮罩：不透明盖底，避免与 textarea 原文叠字 */
.cmp-running-mask {
  position: absolute;
  inset: 0;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 2px;
  background: #f5f7f9;
  pointer-events: none;
}

.cmp-running-line {
  width: 18px;
  height: 2px;
  border-radius: 1px;
  background: linear-gradient(90deg, rgba(148, 163, 160, 0.2) 0%, rgba(66, 95, 131, 0.75) 50%, rgba(148, 163, 160, 0.2) 100%);
  animation: cmp-line-pulse 1.4s ease-in-out infinite;
  flex: 0 0 auto;
}

.cmp-running-text {
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
  background: linear-gradient(110deg, rgba(100, 116, 139, 0.8) 0%, rgba(66, 95, 131, 1) 48%, rgba(100, 116, 139, 0.8) 100%);
  background-size: 220px 100%;
  background-repeat: no-repeat;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: cmp-shimmer 2.2s ease-in-out infinite;
}

@keyframes cmp-shimmer {
  0% { background-position: -240px 0; }
  100% { background-position: calc(100% + 240px) 0; }
}

@keyframes cmp-line-pulse {
  0%, 100% { opacity: 0.45; transform: scaleX(0.88); }
  50% { opacity: 1; transform: scaleX(1); }
}

/* ---------- 底部指挥条（第二行） ---------- */
.cmp-commandbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 8px 2px 0;
  min-height: 38px;
}

.cmp-command-left {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.cmp-command-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 0 0 auto;
}

/* 数据集：指挥条内的紧凑直角控件（非顶部大 pill） */
.cmp-dataset-select {
  width: auto;
  min-width: 158px;
  max-width: 260px;
  flex: 0 1 auto;
}

.cmp-dataset-select :deep(.el-select__wrapper) {
  min-height: 30px;
  padding-left: 28px;
  padding-right: 10px;
  border-radius: 4px;
  background: #edf2f5;
  box-shadow: none !important;
  cursor: pointer;
  transition: background 0.15s ease;
}

.cmp-dataset-select :deep(.el-select__wrapper:hover) {
  background: #dce5eb;
}

.cmp-dataset-select.is-locked :deep(.el-select__wrapper) {
  background: #edf2f5;
  box-shadow: inset 0 0 0 1px rgba(66, 95, 131, 0.35) !important;
}

.cmp-dataset-select.is-locked :deep(.el-select__wrapper:hover) {
  background: #dce5eb;
}

.cmp-dataset-select :deep(.el-select__selected-item),
.cmp-dataset-select :deep(.el-select__placeholder) {
  font-size: 12.5px;
  line-height: 1.2;
  font-weight: 650;
  white-space: nowrap;
  color: #344652;
}

.cmp-dataset-select.is-locked :deep(.el-select__selected-item) {
  color: #344652;
}

.cmp-dataset-select :deep(.el-select__placeholder) {
  color: #66766F;
}

.cmp-dataset-select :deep(.el-select__caret) {
  color: #66766F;
}

.cmp-ds-icon {
  position: absolute;
  left: 9px;
  top: 50%;
  width: 15px;
  height: 15px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transform: translateY(-50%);
  pointer-events: none;
  color: #66766F;
}

.cmp-dataset-select.is-locked .cmp-ds-icon {
  color: #425f83;
}

.cmp-ds-icon svg {
  width: 15px;
  height: 15px;
  display: block;
}

/* 路由提示：指挥条内的小字状态 */
.cmp-route-hint {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  font-weight: 600;
  color: #8A9995;
  white-space: nowrap;
  user-select: none;
}

.cmp-route-dot {
  width: 6px;
  height: 6px;
  border-radius: 1px;
  background: #94a3b8;
  flex: 0 0 auto;
}

.cmp-route-dot.is-locked {
  background: #425f83;
}

/* 运行状态：直角小块（非胶囊） */
.cmp-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  max-width: 340px;
  padding: 4px 9px;
  border-radius: 3px;
  border: 1px solid #dce5eb;
  background: #edf2f5;
  white-space: nowrap;
}

.cmp-status-dot {
  width: 6px;
  height: 6px;
  border-radius: 1px;
  background: #425f83;
  flex: 0 0 auto;
  animation: cmp-dot-pulse 1.2s ease-in-out infinite;
}

.cmp-status.completed .cmp-status-dot {
  background: #526b7a;
  animation: none;
}

.cmp-status.completed {
  background: #edf2f5;
  border-color: #bdcbd3;
}

.cmp-status.error .cmp-status-dot {
  background: #8b6064;
  animation: none;
}

.cmp-status.error {
  background: #faf7f7;
  border-color: #eadfe1;
}

@keyframes cmp-dot-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.35; }
}

.cmp-status-text {
  min-width: 0;
  color: #526b7a;
  font-size: 11px;
  font-weight: 600;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cmp-status.completed .cmp-status-text { color: #526b7a; }
.cmp-status.error .cmp-status-text { color: #8b6064; }

.cmp-status-time {
  color: #8A9995;
  font-size: 10.5px;
  font-weight: 600;
  flex: 0 0 auto;
}

/* ---------- 模型选择：文字式无边框下拉 ---------- */
.cmp-model-select {
  width: 132px;
  flex: 0 0 auto;
}

.cmp-model-select :deep(.el-select__wrapper) {
  min-height: 30px;
  padding-left: 24px;
  padding-right: 6px;
  border-radius: 4px;
  background: transparent;
  box-shadow: none !important;
  cursor: pointer;
  transition: background 0.15s ease;
}

.cmp-model-select :deep(.el-select__wrapper:hover) {
  background: #edf2f5;
  box-shadow: inset 0 0 0 1px #dbe3ed !important;
}

.cmp-model-select :deep(.el-select__selected-item),
.cmp-model-select :deep(.el-select__placeholder) {
  font-size: 12px;
  font-weight: 650;
  line-height: 1.2;
  color: #344652;
}

.cmp-model-select :deep(.el-select__placeholder) {
  color: #344652;
}

.cmp-model-icon {
  position: absolute;
  left: 7px;
  top: 50%;
  transform: translateY(-50%);
  width: 13px;
  height: 13px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #425f83;
  pointer-events: none;
}

.cmp-model-icon svg {
  width: 11px;
  height: 11px;
  display: block;
}

/* 麦克风：方形直角幽灵钮 */
.cmp-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: 1px solid transparent;
  border-radius: 4px;
  background: transparent;
  color: #5C6D68;
  cursor: pointer;
  flex: 0 0 auto;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
}

.cmp-icon-btn:hover {
  background: #edf2f5;
  border-color: #dbe3ed;
  color: #344652;
}

.cmp-icon-btn svg {
  width: 17px;
  height: 17px;
}

/* ---------- 发送 / 停止：方形实色按钮（区别于旧版圆形渐变钮） ---------- */
.cmp-send-btn,
.cmp-stop-btn {
  height: 32px;
  min-width: 32px;
  padding: 0 12px;
  gap: 6px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  flex: 0 0 auto;
  font-size: 12.5px;
  font-weight: 700;
  transition: background 0.15s ease, opacity 0.15s ease, box-shadow 0.15s ease;
}

.cmp-send-btn {
  background: #344652;
  box-shadow: inset 0 -2px 0 rgba(52, 70, 82, 0.22);
}

.cmp-send-btn:hover {
  background: #344652;
}

.cmp-send-btn:active {
  box-shadow: none;
}

.cmp-send-btn.is-disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.cmp-send-plane {
  width: 14px;
  height: 14px;
}

.cmp-send-text {
  line-height: 1;
}

.cmp-send-kbd {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 15px;
  height: 15px;
  padding: 0 3px;
  margin-left: 1px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.18);
  font-family: inherit;
  font-size: 11px;
  font-weight: 700;
  line-height: 1;
}

.cmp-stop-btn {
  background: #344652;
}

.cmp-stop-btn:hover {
  background: #344652;
}

.cmp-stop-icon {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  background: currentColor;
}

/* 录音条：直角线框 */
.cmp-recorder-pill {
  display: flex;
  align-items: center;
  gap: 9px;
  height: 32px;
  padding: 0 12px;
  border-radius: 4px;
  background: #FFFFFF;
  border: 1px solid #dbe3ed;
  flex: 0 0 auto;
}

.cmp-recorder-pill.is-recording {
  animation: cmp-recorder-glow 1.2s ease-in-out infinite;
}

.cmp-recorder-pill.is-cancel-pending {
  border-color: #d7c6c8;
  background: #faf7f7;
}

.cmp-recorder-icon {
  display: flex;
  color: #425f83;
}

.cmp-recorder-pill.is-recording .cmp-recorder-icon {
  animation: cmp-recorder-pulse 1.2s ease-in-out infinite;
}

.cmp-recorder-icon svg {
  width: 16px;
  height: 16px;
}

@keyframes cmp-recorder-pulse {
  0%, 100% { color: #425f83; transform: scale(1); }
  50% { color: #806b47; transform: scale(1.22); }
}

@keyframes cmp-recorder-glow {
  0%, 100% {
    border-color: #dbe3ed;
    box-shadow: none;
  }
  50% {
    border-color: #425f83;
    box-shadow: 0 0 0 3px rgba(66, 95, 131, 0.14);
  }
}

.cmp-recorder-timer {
  font-size: 13px;
  font-variant-numeric: tabular-nums;
  color: #344652;
  min-width: 38px;
}

.cmp-recorder-pill.is-clickable {
  cursor: pointer;
}

.cmp-recorder-pill.is-clickable:hover {
  border-color: #94a3b8;
}

.cmp-recorder-hint {
  font-size: 12px;
  color: #5C6D68;
  white-space: nowrap;
}

/* ---------- 下拉弹层通用项（保留旧类名，供 teleport popper 使用） ---------- */
.ax-ds-option {
  display: flex;
  align-items: center;
  min-width: 0;
  position: relative;
  padding-left: 11px;
}

.ax-ds-option::before {
  content: '';
  position: absolute;
  left: 0;
  top: 6px;
  bottom: 6px;
  width: 3px;
  border-radius: 1px;
  background: #bdcbd3;
  opacity: 0.7;
}

.ax-model-option.is-default-model::before {
  width: 4px;
  background: #425f83;
  opacity: 1;
}

.ax-ds-option-main {
  min-width: 0;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.ax-ds-option-title {
  font-size: 12px;
  font-weight: 600;
  color: #344652;
  line-height: 1.4;
}

.ax-ds-option-auto .ax-ds-option-title {
  color: #344652;
}

.ax-model-option-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  min-width: 0;
}

.ax-model-option-left {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
  flex: 1 1 auto;
}

.ax-model-option-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ax-model-option-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 0 0 auto;
}

.ax-model-option-channel {
  flex: 0 0 auto;
  max-width: 110px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 2px 8px;
  border-radius: 3px;
  background: #edf2f5;
  font-size: 10px;
  font-weight: 600;
  color: #5C6D68;
  line-height: 1.3;
}

.ax-model-default-badge {
  display: inline-flex;
  align-items: center;
  flex: 0 0 auto;
  height: 18px;
  padding: 0 7px;
  border-radius: 3px;
  background: rgba(66, 95, 131, 0.1);
  color: #344652;
  font-size: 10px;
  font-weight: 700;
}

:deep(.ax-ds-popper.el-popper) {
  border-radius: 6px;
  border: 1px solid #dbe3ed;
  box-shadow: 0 8px 24px rgba(52, 70, 82, 0.12);
  padding: 4px;
}

:deep(.ax-ds-popper .el-select-dropdown__item) {
  min-height: 34px;
  border-radius: 4px;
  padding-top: 6px;
  padding-bottom: 6px;
  color: #344652;
}

:deep(.ax-dataset-popper .el-select-dropdown__item.is-hovering),
:deep(.ax-dataset-popper .el-select-dropdown__item:hover),
:deep(.ax-model-popper .el-select-dropdown__item.is-hovering),
:deep(.ax-model-popper .el-select-dropdown__item:hover) {
  background: #edf2f5;
}

/* ---------- 响应式 ---------- */
@media (max-width: 900px) {
  .cmp-dock {
    padding: 10px 12px 8px;
  }

  .cmp-dataset-select {
    min-width: 132px;
    max-width: 46vw;
  }

  .cmp-route-hint {
    display: none;
  }

  .cmp-model-select {
    width: 112px;
  }

  .cmp-status {
    max-width: 40vw;
  }

  .cmp-send-kbd {
    display: none;
  }
}
</style>

<style>
/* ============================================================
   模型下拉弹层 — 浅色高端版（参考用户截图的版式 / 配色与整体协调）
   触发器保持原色；弹层浅色面板 + 精致边框 + 柔和投影
   布局参考截图：左=闪电+名称+默认徽章 / 右=通道+对勾
   ============================================================ */
.ax-model-popper.el-popper {
  min-width: 280px;
  background: #FFFFFF;
  border: 1px solid #dbe3ed;
  border-radius: 6px;
  box-shadow: 0 8px 24px rgba(52, 70, 82, 0.12);
  max-height: 380px;
  overflow: hidden;
}
.ax-model-popper .el-select-dropdown__list {
  max-height: 368px;
  overflow-y: auto;
  padding: 6px;
}
/* 滚动条：白底弹层配黑灰半透明（bug 2026-08-25 反馈"太白"） */
.ax-model-popper .el-select-dropdown__list::-webkit-scrollbar {
  width: 5px;
}
.ax-model-popper .el-select-dropdown__list::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.22);
  border-radius: 3px;
}
.ax-model-popper .el-select-dropdown__list::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.34);
}
.ax-model-popper .el-select-dropdown__list::-webkit-scrollbar-track {
  background: transparent;
}
.ax-model-popper .el-select-dropdown__item {
  background: transparent;
  border-radius: 4px;
  margin: 2px 0;
  padding: 9px 12px;
  border: 1px solid transparent;
}
.ax-model-popper .el-select-dropdown__item:hover,
.ax-model-popper .el-select-dropdown__item.is-hovering {
  background: #edf2f5;
  border-color: #dbe3ed;
}
.ax-model-popper .el-select-dropdown__item.is-selected {
  background: #edf2f5;
  border-color: #cbd5e1;
}
.ax-model-option-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  min-width: 0;
}
.ax-model-option-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  flex: 1 1 auto;
}
.ax-model-option-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 0 0 auto;
}
.ax-model-icon-mini {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  flex: 0 0 auto;
  color: #425f83;
}
.ax-model-icon-mini svg {
  width: 14px;
  height: 14px;
}
.ax-model-option-name {
  color: #111827;
  font-size: 13px;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.ax-model-default-badge {
  flex: 0 0 auto;
  padding: 1px 6px;
  border-radius: 4px;
  background: rgba(66, 95, 131, 0.1);
  color: #344652;
  font-size: 10px;
  font-weight: 600;
  line-height: 1.3;
}
.ax-model-option-channel {
  flex: 0 0 auto;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 1px 6px;
  border-radius: 4px;
  background: #F3F4F6;
  color: #4B5563;
  font-size: 10px;
  font-weight: 500;
  line-height: 1.3;
}
.ax-model-check {
  color: #344652;
  font-size: 13px;
  font-weight: 700;
  line-height: 1;
}
</style>

<style scoped>
.cmp-dock{position:relative;isolation:isolate;transition:border-color .2s,box-shadow .2s;overflow:hidden}.cmp-dock:focus-within{border-color:#7188a5!important;box-shadow:0 0 0 3px #dce5ef80,0 8px 28px #425f8308!important}.cmp-activity-ribbon{position:absolute;inset:0 0 auto;height:2px;pointer-events:none;background:linear-gradient(90deg,transparent 5%,#7188a5 30%,#425f83 48%,#425f83 58%,transparent 80%);background-size:230% 100%;animation:composer-marquee 3.2s linear infinite;opacity:.85}.cmp-draft-hint{display:flex;align-items:center;gap:7px;color:#475569;font-size:12px;margin-bottom:10px;line-height:1.6}.cmp-draft-hint>span:last-child{margin-left:auto;font-size:11px;color:#617085}.cmp-draft-spark{color:#425f83;font-size:13px}.cmp.is-running .cmp-dock{background:#fff}.cmp-send-btn.is-queue-send{background:#425f83}.cmp-send-btn:disabled{opacity:.45;cursor:not-allowed;transform:none}.cmp-stop-btn{background:#f4f7fa!important;color:#475569!important;border:1px solid #dce5eb!important;box-shadow:none!important;border-radius:7px!important}.cmp-stop-btn:hover{background:#faf7f7!important;color:#8b6064!important;border-color:#eadfe1!important}.cmp-stop-icon{background:currentColor}.cmp-send-btn:active:not(:disabled){transform:translateY(1px)}@keyframes composer-marquee{from{background-position:160% 0}to{background-position:-60% 0}}@media(max-width:600px){.cmp-draft-hint>span:last-child{display:none}.cmp-command-right{gap:6px}.cmp-stop-btn{padding-inline:8px}.cmp-send-btn.is-queue-send{padding-inline:10px}}@media(prefers-reduced-motion:reduce){.cmp-activity-ribbon{animation:none;background-position:50% 0;opacity:.5}.cmp-dock,.cmp-send-btn{transition:none}}
</style>

<style scoped>
@property --composer-orbit-angle{syntax:'<angle>';initial-value:0deg;inherits:false}
.cmp-activity-ribbon{inset:0!important;width:100%;height:100%!important;padding:0!important;background:none!important;mask:none!important;-webkit-mask:none!important;animation:none!important;opacity:0;pointer-events:none}
.cmp.is-running .cmp-dock{border:2px solid transparent!important;background:linear-gradient(#fff,#fff) padding-box,conic-gradient(from var(--composer-orbit-angle),#e2e8f0 0deg,#e2e8f0 250deg,#7188a5 285deg,#425f83 320deg,#425f83 342deg,#e2e8f0 360deg) border-box!important;animation:composer-orbit 3.2s linear infinite!important}
@keyframes composer-orbit{to{--composer-orbit-angle:360deg}}
@media(prefers-reduced-motion:reduce){.cmp.is-running .cmp-dock{animation:none!important;background:linear-gradient(#fff,#fff) padding-box,linear-gradient(110deg,#7188a5,#425f83,#425f83) border-box!important}}
</style>
