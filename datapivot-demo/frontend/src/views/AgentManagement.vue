<template>
  <div class="agent-page">
    <header class="expert-page-head"><div><span class="page-overline">协作配置</span><h1>专家协作</h1><p>定义每个角色的职责、执行指令与业务知识。</p></div><div class="expert-head-actions"><el-button @click="router.push('/advanced-capabilities?tab=skills')">技能与工具</el-button><el-button @click="router.push('/admin-console?tab=ask-flow')">流程策略</el-button></div></header>
    <div class="agent-workbench document-workbench">
      <aside class="agent-rail" aria-label="协作角色">
        <div class="agent-rail-head"><span>协作角色</span><small>{{ agents.length }}</small></div>
        <button v-for="item in agents" :key="item.agent_no" class="agent-card" :class="{active:selectedAgentNo===item.agent_no}" :aria-pressed="selectedAgentNo===item.agent_no" @click="selectAgent(item)">
          <span class="agent-card-no">{{ String(item.agent_no).padStart(2,'0') }}</span><span class="agent-card-copy"><strong>{{ roleNames[item.agent_no] || item.name }}</strong><small>{{ roleShort[item.agent_no] }}</small></span><span v-if="selectedAgentNo===item.agent_no" class="role-selected-dot"></span>
        </button>

      </aside>
      <section class="agent-editor">
        <header class="agent-editor-head"><div><span class="editor-overline">角色工作区</span><h2>{{ roleNames[selectedAgentNo] || '角色详情' }}</h2></div><el-button v-if="isFeatureEnabled('agent_config_edit')" type="primary" @click="saveAgent">保存配置</el-button></header>
        <GovernanceEmpty v-if="!selectedAgentNo" description="请选择一个协作角色" />
        <template v-else>
          <div class="role-execution-note"><span class="execution-indicator"></span><p>{{ roleBindings[selectedAgentNo] }}</p></div>
          <nav class="editor-section-tabs" aria-label="角色配置分区"><button v-for="item in editorSections" :key="item.key" :aria-pressed="editorTab===item.key" @click="editorTab=item.key">{{ item.label }}<span v-if="item.key==='knowledge'">{{ form.knowledge_base.length }}</span></button></nav>
          <div class="editor-content" :class="{ 'has-instruction-context': editorTab==='instructions' }"><aside class="instruction-context" v-if="editorTab==='instructions'"><span>执行边界</span><h3>配置如何生效</h3><dl><div><dt>调用角色</dt><dd>{{ roleNames[selectedAgentNo] }}</dd></div><div><dt>应用范围</dt><dd>保存后用于后续新任务</dd></div><div><dt>安全约束</dt><dd>组织权限与查询安全由固定护栏校验，不能被指令覆盖。</dd></div><div><dt>检查方式</dt><dd>本地检查确认指令非空；不执行 SQL，也不调用模型。</dd></div></dl></aside>
            <section v-if="editorTab==='instructions'" class="instruction-section" :class="{ 'editor-expanded': editorExpanded }" @keydown.esc="editorExpanded = false"><div class="section-heading"><div><h3>执行指令</h3><p>此指令随该角色的模型调用读取，保存后用于后续新任务。</p></div><span class="text-count">{{ form.system_prompt.length.toLocaleString() }} 字符</span></div><div class="instruction-toolbar"><span>instruction.md</span><span>{{ promptLines }} 行 · ≈ {{ estimatedTokens }} tokens（估算）</span><div><el-button size="small" :disabled="!isFeatureEnabled('agent_config_edit')" @click="insertOutline">插入结构</el-button><el-button size="small" @click="validateInstruction">检查指令</el-button><el-button size="small" @click="editorExpanded = !editorExpanded">{{ editorExpanded ? '退出全屏' : '全屏编辑' }}</el-button></div></div><el-input :disabled="!isFeatureEnabled('agent_config_edit')" v-model="form.system_prompt" type="textarea" :rows="17" class="prompt-input" aria-label="系统提示词" /><div class="editor-footnote"><span>指令负责业务行为与输出要求。</span><span>权限与查询安全由固定护栏执行</span></div></section>
            <section v-else-if="editorTab==='knowledge'" class="knowledge-section"><div class="section-heading"><div><h3>业务知识</h3><p>补充该角色需要遵循的术语、口径和业务约束。</p></div><el-button v-if="isFeatureEnabled('agent_config_edit')" size="small" @click="addKnowledge">新增知识片段</el-button></div><div v-for="(item,index) in form.knowledge_base" :key="index" class="knowledge-item"><span class="knowledge-index">{{ String(index+1).padStart(2,'0') }}</span><el-input :disabled="!isFeatureEnabled('agent_config_edit')" v-model="form.knowledge_base[index]" type="textarea" :rows="3" :aria-label="`知识片段 ${index+1}`" /><el-button v-if="isFeatureEnabled('agent_config_edit')" link type="danger" @click="form.knowledge_base.splice(index,1)">删除</el-button></div><GovernanceEmpty v-if="!form.knowledge_base.length" description="暂无知识片段" :image-size="72" /></section>
            <section v-else class="profile-section"><div class="section-heading"><div><h3>角色资料</h3><p>维护展示名称与职责说明，角色的执行绑定保持一致。</p></div></div><label class="agent-field"><span>显示名称</span><el-input :disabled="!isFeatureEnabled('agent_config_edit')" v-model="form.name" /></label><label class="agent-field"><span>职责说明</span><el-input :disabled="!isFeatureEnabled('agent_config_edit')" v-model="form.role_summary" type="textarea" :rows="5" /></label></section>
          </div>
        <div class="role-rail-note"><span class="rail-note-label">协作方式</span><p>主理人统筹任务<br>专家完成查询、核验与解读</p><details class="collaboration-map"><summary>查看两条执行路径</summary><div><span>普通问数</span><ol><li>识别范围与口径</li><li>生成查询并核验</li><li>解读结果与交付</li></ol></div><div><span>高阶研究</span><ol><li>规划取证方向</li><li>多分支并行验证</li><li>汇合证据与签收</li></ol></div></details></div>
        </template>
      </section>
    </div>
  </div>
</template>

<script setup>
import GovernanceEmpty from "../components/GovernanceEmpty.vue"
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter, useRoute } from 'vue-router'
import { getAgents, updateAgent } from '../api/index.js'
import { useFeatureFlags } from '../state/featureFlags.js'

const router = useRouter()
const pageRoute = useRoute()
const roleNames = {1:'主理人 · 路由与研究规划',2:'查询专家',3:'核验专家',4:'分析与报告专家'}
const roleBindings = {1:'普通：识别范围、路由与口径确认；高阶：形成研究计划并拆分取证方向。',2:'两条路径：依据字段、关联与金标样例生成查询，参与有界修复。',3:'两条路径：复核查询、字段与业务口径；执行前仍经过固定安全护栏。',4:'普通：解读核验结果；高阶：根据分支证据形成研究报告并接受复核。'}
const agents = ref([])
const selectedAgentNo = ref(null)
const editorTab = ref('instructions')
const editorSections = [{key:'instructions',label:'执行指令'},{key:'knowledge',label:'业务知识'},{key:'profile',label:'角色资料'}]
const roleShort = {1:'路由 · 规划 · 签收',2:'字段映射 · 查询生成',3:'口径复核 · 结果核验',4:'证据解读 · 报告交付'}
const { isFeatureEnabled, loadFeatureFlags } = useFeatureFlags()
const form = reactive({
  name: '',
  role_summary: '',
  system_prompt: '',
  knowledge_base: []
})

const editorExpanded = ref(false)
const promptLines = computed(() => form.system_prompt.split('\n').length)
const estimatedTokens = computed(() => Math.ceil([...form.system_prompt].reduce((n,c) => n + (/[^\x00-\x7F]/.test(c) ? 1 : 0.25), 0)))
const insertOutline = () => {
  form.system_prompt += '\n\n## 任务目标\n\n## 业务约束\n\n## 输出格式\n'
  ElMessage.info('已追加结构草稿，保存后才生效')
}
const validateInstruction = () => {
  if (!form.system_prompt.trim()) return ElMessage.warning('指令不能为空')
  ElMessage.success('本地检查通过：指令非空。此检查不会调用模型或执行查询。')
}
const applyAgent = (agent) => {
  selectedAgentNo.value = agent.agent_no
  form.name = /^Agent[1-4]\b/.test(agent.name || '') ? roleNames[agent.agent_no] : agent.name || roleNames[agent.agent_no] || ''
  form.role_summary = agent.role_summary || ''
  form.system_prompt = agent.system_prompt || ''
  form.knowledge_base = Array.isArray(agent.knowledge_base) ? [...agent.knowledge_base] : []
}

const loadAgents = async () => {
  const result = await getAgents()
  agents.value = result.agents || []
  if (!selectedAgentNo.value && agents.value.length > 0) {
    applyAgent(agents.value.find(item=>item.agent_no===Number(pageRoute.query.role)) || agents.value[0])
  }
}

const selectAgent = (agent) => {
  applyAgent(agent)
}

const addKnowledge = () => {
  form.knowledge_base.push('')
}

const saveAgent = async () => {
  if (!selectedAgentNo.value) return
  await updateAgent(selectedAgentNo.value, {
    name: form.name,
    role_summary: form.role_summary,
    system_prompt: form.system_prompt,
    knowledge_base: form.knowledge_base
  })
  ElMessage.success('角色配置已保存，对后续新任务生效')
  await loadAgents()
}

watch(()=>pageRoute.query.role, value=>{const role=agents.value.find(item=>item.agent_no===Number(value));if(role)applyAgent(role)})

onMounted(() => {
  loadFeatureFlags()
  loadAgents()
})
</script>
<style scoped>
.agent-page{color:#18222f;max-width:1600px;margin:0 auto;padding:4px 0 28px}.expert-page-head{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:8px 0 26px}.page-overline,.editor-overline{display:block;color:#637184;font-size:11px;letter-spacing:.06em;margin-bottom:7px}.expert-page-head h1{font-size:25px;font-weight:600;letter-spacing:-.6px;margin:0}.expert-page-head p{font-size:13px;color:#687586;margin:8px 0 0}.expert-head-actions{display:flex;gap:8px}.expert-head-actions :deep(.el-button+.el-button){margin-left:0}.agent-workbench{display:grid;grid-template-columns:264px minmax(0,1fr);border:1px solid #e2e6eb;border-radius:12px;background:#fff;min-height:650px;overflow:hidden}.agent-rail{padding:22px 14px;background:#f9fafb;border-right:1px solid #e8ebef}.agent-rail-head{display:flex;justify-content:space-between;align-items:center;padding:0 12px 18px;color:#778292;font-size:12px}.agent-rail-head small{font-size:11px;border:1px solid #e2e6eb;border-radius:5px;padding:1px 6px}.agent-card{display:flex;gap:11px;align-items:center;width:100%;text-align:left;padding:15px 12px;border:1px solid #edf0f5;border-radius:10px;margin-bottom:14px;color:#465365;background:#ffffff;position:relative;transition:all .18s cubic-bezier(0.4, 0, 0.2, 1);box-shadow:0 1px 3px rgba(15,23,42,0.03)}.agent-card:hover{background:#f5f7fa;border-color:#cbd5e1;transform:translateY(-1px)}.agent-card.active{background:#ffffff;border-color:#425f83;box-shadow:0 4px 14px rgba(66, 95, 131,0.09);outline:1px solid #425f83}.agent-card:not(:last-of-type)::after{content:'→';position:absolute;top:50%;right:-10px;transform:translateY(-50%);font-size:11px;color:#617085;font-weight:700;line-height:1;pointer-events:none;z-index:5;background:#ffffff;border:1px solid #cbd5e1;border-radius:50%;width:18px;height:18px;display:flex;align-items:center;justify-content:center;box-shadow:0 1px 3px rgba(15,23,42,0.06)}.agent-card-no{font-size:11px;line-height:28px;text-align:center;border-radius:8px;width:30px;height:30px;flex-shrink:0;font-weight:700;font-variant-numeric:tabular-nums;transition:all .18s}.agent-card:nth-of-type(1) .agent-card-no{color:#425f83;background:#edf2f8;border:1px solid #dce5ef}.agent-card:nth-of-type(2) .agent-card-no{color:#696780;background:#f8f8fa;border:1px solid #f1f0f6}.agent-card:nth-of-type(3) .agent-card-no{color:#806b47;background:#f5f2ec;border:1px solid #e8e2d7}.agent-card:nth-of-type(4) .agent-card-no{color:#526b7a;background:#edf2f5;border:1px solid #dce5eb}.active .agent-card-no{box-shadow:0 2px 6px rgba(0,0,0,0.08)}.agent-card-copy{display:flex;min-width:0;flex:1;flex-direction:column;gap:5px}.agent-card-copy strong{font-size:13px;font-weight:600;color:#1e293b;line-height:1.4}.agent-card-copy small{font-size:11px;color:#617085}.role-selected-dot{width:6px;height:6px;border-radius:50%;background:#425f83;box-shadow:0 0 6px rgba(66, 95, 131,0.5)}.role-rail-note{margin:28px 8px 0;padding-top:18px;border-top:1px solid #e2e8f0}.rail-note-label{font-size:11px;font-weight:600;color:#617085;letter-spacing:0.04em;text-transform:uppercase}.role-rail-note>p{font-size:12px;line-height:1.8;color:#475569;margin:8px 0 16px}.collaboration-map summary{font-size:12px;color:#425f83;cursor:pointer;font-weight:500}.collaboration-map>div{padding-top:14px}.collaboration-map>div>span{font-size:11px;font-weight:600;color:#475569}.collaboration-map ol{margin:8px 0 0;padding-left:14px;list-style:decimal;font-size:11px;line-height:1.8;color:#617085}.agent-editor{min-width:0}.agent-editor-head{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:25px 30px 18px}.agent-editor-head h2{font-size:19px;font-weight:550;margin:0;letter-spacing:-.3px}.role-execution-note{display:flex;align-items:flex-start;gap:8px;padding:0 30px 23px}.execution-indicator{width:5px;height:5px;background:#526b7a;flex-shrink:0;border-radius:50%;margin-top:7px}.role-execution-note p{font-size:12px;line-height:1.8;color:#637184;margin:0}.editor-section-tabs{display:flex;gap:26px;padding:0 30px;border-bottom:1px solid #e7ebf0}.editor-section-tabs button{display:flex;align-items:center;gap:7px;color:#6b798b;font-size:12px;padding:0 0 13px;border-bottom:2px solid transparent}.editor-section-tabs button[aria-pressed=true]{color:#3c536e;border-color:#3c536e}.editor-section-tabs span{padding:1px 5px;border-radius:4px;background:#f0f3f6;font-size:10px}.editor-content{padding:27px 30px 30px}.section-heading{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:20px}.section-heading h3{font-size:14px;font-weight:550;margin:0 0 7px}.section-heading p{color:#637184;font-size:12px;line-height:1.8;margin:0}.text-count{font-size:11px;color:#9aa3af;white-space:nowrap}.prompt-input :deep(textarea){background:#fbfcfd;font-family:'SFMono-Regular',Consolas,'PingFang SC',monospace;font-size:13px;line-height:1.9;padding:20px;box-shadow:0 0 0 1px #e5e9ee inset;color:#425169;border-radius:8px;resize:vertical}.editor-footnote{display:flex;justify-content:space-between;gap:12px;margin-top:12px;color:#8b96a4;font-size:11px;line-height:1.7}.knowledge-item{display:flex;gap:14px;align-items:flex-start;padding:18px 0;border-bottom:1px solid #edf0f3}.knowledge-index{font-size:11px;color:#96a0ac;padding-top:9px}.knowledge-item :deep(textarea){padding:12px;line-height:1.8}.agent-field{display:flex;flex-direction:column;gap:10px;font-size:12px;color:#566578;margin-bottom:24px;max-width:760px}.profile-section{min-height:420px}@media(max-width:1000px){.agent-workbench{grid-template-columns:220px minmax(0,1fr)}.expert-page-head{align-items:flex-start}.expert-head-actions{flex-wrap:wrap;justify-content:flex-end}.agent-editor-head,.editor-content{padding-left:22px;padding-right:22px}.role-execution-note,.editor-section-tabs{padding-left:22px;padding-right:22px}}@media(max-width:720px){.expert-page-head{flex-direction:column}.agent-workbench{grid-template-columns:1fr}.agent-rail{border-right:0;border-bottom:1px solid #e8ebef;display:grid;grid-template-columns:1fr 1fr;gap:4px;padding:12px}.agent-rail-head,.role-rail-note{display:none}.agent-card{margin:0}.agent-card-no{display:none}.agent-card-copy strong{font-size:11px}.agent-card-copy small{font-size:10px}.agent-editor-head h2{font-size:17px}.editor-footnote{flex-direction:column}.text-count{display:none}}
</style>
