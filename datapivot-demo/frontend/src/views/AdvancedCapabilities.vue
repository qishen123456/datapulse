<template>
  <div class="module-layout-v4 advanced-page">
    <section class="advanced-hero">
      <div>
        <p class="eyebrow">问数编排</p>
        <h1>技能与工具</h1>
        <p>
          管理执行能力、专家绑定与外部工具，所有变更用于后续新任务。
        </p>
      </div>
      <div class="hero-actions">
        <el-button :loading="loading" @click="loadConfig">刷新</el-button>
        <el-button plain :loading="askFlowLoading" @click="goAskFlowControl">流程控制</el-button>
        <el-button v-if="featureAccess.advanced_capability_reset" plain type="warning" :loading="resetting" @click="handleReset">恢复默认</el-button>
        <el-button v-if="featureAccess.advanced_capability_save" type="primary" :loading="saving" @click="handleSave">保存配置</el-button>
      </div>
    </section>

    <div class="capability-status-strip"><span><i class="status-dot"></i>技能目录 <strong>{{ enabledSkillCount }} / {{ sortedSkills.length }}</strong></span><span>高阶研究 <strong>{{ askFlowStatus.label }}</strong></span><span>外部工具 <strong>{{ externalToolSummary }}</strong></span></div>

    <section class="advanced-workbench">
      <el-tabs v-model="activeTab" class="advanced-tabs" tab-position="left">
        <el-tab-pane label="运行概览" name="overview">    <section class="capability-flow-map" aria-label="两条问数路径的能力绑定">
      <article><span class="flow-map-label">普通问数</span><strong>口径确认 · 生成查询 · 核验执行 · 解读答案</strong><p>组织权限、字段剪枝、只读审核与数据断言始终执行，配置共享技能可影响后续新任务。</p></article>
      <article><span class="flow-map-label">高阶研究 · {{ askFlowStatus.label }}</span><strong>研究计划 · 并行取证 · 证据核验 · 研究报告</strong><p>{{ askFlowStatus.hint }}。共享查询护栏沿用同一套授权与执行服务。</p></article>
    </section>
    <nav class="capability-related" aria-label="关联配置"><el-button link @click="router.push('/agents')">专家协作</el-button><el-button link @click="router.push('/datasets')">数据集与业务口径</el-button><el-button link @click="router.push('/ai-models')">模型服务</el-button><el-button link @click="router.push('/report-config')">报告模板</el-button></nav>


          <div class="overview-grid">
            <section class="plain-panel">
              <h2>执行边界</h2>
              <ul>
                <li>普通问数与高阶研究分别执行，入口由控制台角色授权与流程策略决定，用户无需选择路径。</li>
                <li>共享技能作用于两条路径；研究规划与结果诊断只作用于高阶研究。</li>
                <li>最终报告结果保持现有结构，继续复用报告模板、图表和下载能力。</li>
                <li>数据集字段、指标口径、金标 SQL、组织树与报告模板共同提供上下文；专家职责在“专家协作”维护。</li>
              </ul>
            </section>
            <section class="plain-panel">
              <h2>当前摘要</h2>
              <div class="summary-list">
                <div><span>能力中心</span><strong>{{ config.enabled ? '开启' : '关闭' }}</strong></div>
                <div><span>流程入口</span><strong>{{ askFlowStatus.label }}</strong></div>
                <div><span>Skill Trace</span><strong>{{ config.execution.emitSkillTrace ? '显示' : '隐藏' }}</strong></div>
                <div><span>资产预览数</span><strong>{{ config.execution.assetPreviewLimit }}</strong></div>
                <div><span>MCP</span><strong>{{ config.mcp.enabled ? '开启' : '关闭' }}</strong></div>
                <div><span>SQL Server</span><strong>{{ config.sqlServer.enabled ? '开启' : '关闭' }}</strong></div>
              </div>
              <div v-if="!askFlowReady" class="flow-warning">
                高阶研究尚未开放。请检查流程控制中的开放状态、角色和数据集策略；普通问数继续执行共享安全护栏。
              </div>
            </section>
          </div>
        </el-tab-pane>

        <el-tab-pane label="技能配置" name="skills">
          <section class="plain-panel">
            <div class="panel-head">
              <div>
                <h2>问数技能</h2>
                <p>维护已接入执行链路的指令与参数。固定安全护栏始终生效。</p>
              </div>
              <div class="panel-actions">
                <el-button v-if="featureAccess.advanced_skill_import" plain type="primary" @click="openImportDialog">导入技能</el-button>
                <el-switch v-model="config.enabled" active-text="高阶研究开启" inactive-text="高阶研究关闭" />
              </div>
            </div>
            <div class="skill-library-toolbar"><el-input v-model="skillSearch" clearable placeholder="搜索技能名称、说明或标识" aria-label="搜索技能" /><div class="skill-scope-filter" aria-label="筛选技能路径"><button v-for="item in [{key:'all',label:'全部'},{key:'shared',label:'共享技能'},{key:'advanced',label:'研究专用'}]" :key="item.key" type="button" :aria-pressed="skillScope===item.key" @click="skillScope=item.key">{{ item.label }}</button></div></div>
            <div class="skill-list-caption"><span>{{ visibleSkills.length }} 项技能</span><span>执行绑定 / 启用状态</span></div>
            <div class="skill-library" aria-label="技能目录">
              <article v-for="row in visibleSkills" :key="row.key" class="skill-library-row">
                <div class="skill-emblem" :class="{fixed:requiredSkills.includes(row.key)}"><svg v-if="requiredSkills.includes(row.key)" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m12 3 7 3v5c0 5-7 10-7 10S5 16 5 11V6l7-3Z" stroke="currentColor" stroke-width="1.4"/><path d="m8.5 11.5 2.3 2.3 4.7-5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg><svg v-else viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m12 3 3 6 6 3-6 3-3 6-3-6-6-3 6-3 3-6Z" stroke="currentColor" stroke-width="1.4"/></svg></div>
                <button class="skill-identity" type="button" @click="editSkill(row)"><span><strong>{{ row.label }}</strong><small>{{ flowLabel(row) }}</small></span><p>{{ row.description }}</p><code>{{ row.key }}</code></button>
                <div class="skill-runtime"><span>{{ bindingLabel(row) }}</span><small>{{ toolTypeLabel(row.toolType) }}</small></div>
                <div class="skill-row-actions"><el-switch v-model="row.enabled" :disabled="requiredSkills.includes(row.key) || !featureAccess.advanced_capability_save" :aria-label="`${row.label}启用状态`" /><el-button @click="editSkill(row)" size="small">{{ featureAccess.advanced_capability_save ? '配置' : '查看' }}</el-button></div>
              </article>
              <el-empty v-if="!visibleSkills.length" description="没有匹配的技能" :image-size="72" />
            </div>
          </section>
        </el-tab-pane>

        <el-tab-pane label="MCP 工具" name="mcp">
          <section class="plain-panel">
            <div class="panel-head">
              <div>
                <h2>MCP 工具配置</h2>
                <p>第一阶段先作为外部工具插座管理，稳定后再接文件、知识库、飞书发送等真实调用。</p>
              </div>
              <el-switch v-model="config.mcp.enabled" active-text="开启 MCP" inactive-text="关闭 MCP" />
            </div>
            <el-form label-position="top">
              <el-form-item label="服务列表 JSON">
                <el-input
                  v-model="mcpServersText"
                  type="textarea"
                  :rows="9"
                  placeholder='例如：[{"name":"knowledge","url":"http://mcp-server:9000"}]'
                />
              </el-form-item>
              <el-form-item label="备注">
                <el-input v-model="config.mcp.notes" type="textarea" :rows="3" />
              </el-form-item>
            </el-form>
          </section>
        </el-tab-pane>

        <el-tab-pane label="SQL Server" name="sqlserver">
          <section class="plain-panel">
            <div class="panel-head">
              <div>
                <h2>SQL Server 工具</h2>
                <p>优先复用数据源管理中的 SQL Server 数据源，驱动和镜像依赖后续做容器级检测。</p>
              </div>
              <el-switch v-model="config.sqlServer.enabled" active-text="开启 SQL Server 工具" inactive-text="关闭" />
            </div>
            <el-form label-position="top" class="form-grid">
              <el-form-item label="ODBC Driver">
                <el-input v-model="config.sqlServer.driver" />
              </el-form-item>
              <el-form-item label="复用数据源管理">
                <el-switch v-model="config.sqlServer.reuseDataSources" />
              </el-form-item>
              <el-form-item label="备注" class="form-wide">
                <el-input v-model="config.sqlServer.notes" type="textarea" :rows="4" />
              </el-form-item>
            </el-form>
          </section>
        </el-tab-pane>

        <el-tab-pane label="流程保护" name="execution">
          <section class="plain-panel">
            <h2>执行与展示策略</h2>
            <div class="switch-list">
              <label>
                <span>
                  <strong>显示 Skill Trace</strong>
                  <small>高阶研究开启后，工作区展示真实业务过程；技术详情仍受功能权限控制。</small>
                </span>
                <el-switch v-model="config.execution.emitSkillTrace" />
              </label>
              <label>
                <span>
                  <strong>保持最终报告契约</strong>
                  <small>固定开启：最终仍输出现有报告组件需要的 dataset_results 和 report_spec。</small>
                </span>
                <el-switch v-model="config.execution.preserveFinalReportContract" disabled />
              </label>
              <label>
                <span>
                  <strong>高阶异常保留现场</strong>
                  <small>高阶异常保留可用证据与未完成方向，禁止自动切换为普通流程。</small>
                </span>
                <el-tag type="success">独立执行</el-tag>
              </label>
            </div>
            <div class="slider-row">
              <span>单次研究数据域上限</span>
              <el-slider v-model="config.execution.assetPreviewLimit" :min="1" :max="4" show-input />
            </div>
          </section>
        </el-tab-pane>

        <el-tab-pane label="诊断" name="diagnostics">
          <section class="plain-panel">
            <div class="panel-head">
              <div>
                <h2>配置诊断</h2>
                <p>用于发版前核对迁移包中的技能与工具配置。</p>
              </div>
              <el-tag type="success" effect="light">运行态迁移已纳入</el-tag>
            </div>
            <pre class="json-preview">{{ prettyConfig }}</pre>
          </section>
        </el-tab-pane>
      </el-tabs>
    </section>

    <el-drawer v-model="skillEditorVisible" title="技能配置" size="min(560px, 100vw)" append-to-body class="skill-editor-drawer">
      <template v-if="skillDraft">
        <div class="skill-binding-summary"><strong>{{ flowLabel(skillDraft) }}</strong><span>{{ bindingLabel(skillDraft) }}</span><code>{{ skillDraft.key }}</code><el-button v-if="runtime(skillDraft).roles?.length" link type="primary" @click="router.push('/agents?role='+runtime(skillDraft).roles[0]);skillEditorVisible=false">查看绑定专家</el-button></div>
        <el-form label-position="top" :disabled="!featureAccess.advanced_capability_save">
          <el-form-item label="技能名称"><el-input v-model="skillDraft.label" maxlength="100" /></el-form-item>
          <el-form-item label="能力说明"><el-input v-model="skillDraft.description" type="textarea" :rows="3" /></el-form-item>
          <el-form-item v-if="runtime(skillDraft).promptEditable" label="执行指令"><el-input v-model="skillDraft.prompt" type="textarea" :rows="10" maxlength="6000" show-word-limit /><p class="skill-editor-hint">保存后注入绑定专家的模型提示词，对后续新任务生效；不会覆盖已有任务或绕过 SQL、组织与数据护栏。</p></el-form-item>
          <el-form-item v-if="runtime(skillDraft).parameterEditable" label="字段检索数量"><el-input-number v-model="skillDraft.config.fieldLimit" :min="8" :max="160" /><p class="skill-editor-hint">控制模型上下文字段剪枝数量。组织、时间和关联键仍强制保留；完整字段继续参与审核。</p></el-form-item>
          <el-alert v-if="!runtime(skillDraft).promptEditable && !runtime(skillDraft).parameterEditable" :closable="false" type="info" :title="skillDraft.custom ? '此扩展尚未接入执行器。编辑仅保存技能资料，不会执行代码或调用外部工具。' : '此技能由固定执行器完成，可编辑资料说明；安全检查和执行顺序不能通过文字配置关闭。'" />
        </el-form>
      </template>
      <template #footer><el-button @click="skillEditorVisible=false">取消</el-button><el-button v-if="featureAccess.advanced_capability_save" type="primary" :loading="saving" @click="saveSkill">保存配置</el-button></template>
    </el-drawer>

    <el-dialog v-model="importDialogVisible" title="导入 Skill Manifest" width="760px" destroy-on-close>
      <div class="import-panel">
        <p>
          支持粘贴网上找到的 Skill Manifest JSON。当前只导入能力定义、提示词和工具声明，
          不执行第三方代码；内置 Skill 也不会被覆盖。
        </p>
        <el-input
          v-model="skillImportText"
          type="textarea"
          :rows="14"
          placeholder='{"skills":[{"key":"cohort_analysis","label":"客群分层分析 Skill","toolType":"python","description":"按客户/组织/指标做分层分析","prompt":"..."}]}'
        />
        <div v-if="importReport" class="import-report">
          <el-tag type="success">导入 {{ importReport.imported?.length || 0 }} 个</el-tag>
          <el-tag v-if="importReport.skipped?.length" type="warning">跳过 {{ importReport.skipped.length }} 个</el-tag>
          <ul v-if="importReport.skipped?.length">
            <li v-for="item in importReport.skipped" :key="`${item.key || item.label}-${item.reason}`">
              {{ item.key || item.label || '未命名' }}：{{ item.reason }}
            </li>
          </ul>
        </div>
      </div>
      <template #footer>
        <el-button @click="importDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="importing" @click="handleImportSkills">导入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import "../styles/module-interiors.css"
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getAdvancedCapabilitiesConfig,
  getAskFlowConfig,
  importAdvancedSkills,
  resetAdvancedCapabilitiesConfig,
  saveAdvancedCapabilitiesConfig,
} from '../api/index.js'
import { useFeatureFlags } from '../state/featureFlags.js'

const defaultConfig = () => ({
  version: 1,
  enabled: true,
  description: '',
  execution: {
    emitSkillTrace: true,
    preserveFinalReportContract: true,
    assetPreviewLimit: 3,
    fallbackToBasicEngine: false,
  },
  skills: [],
  mcp: { enabled: false, servers: [], notes: '' },
  sqlServer: { enabled: false, reuseDataSources: true, driver: 'ODBC Driver 18 for SQL Server', notes: '' },
})

const pageRoute=useRoute()
const activeTab = ref(['overview','skills','mcp','sqlserver','execution','diagnostics'].includes(pageRoute.query.tab)?pageRoute.query.tab:'skills')
watch(()=>pageRoute.query.tab,value=>{if(value==='skills')activeTab.value='skills'})
const loading = ref(false)
const saving = ref(false)
const resetting = ref(false)
const importing = ref(false)
const askFlowLoading = ref(false)
const config = ref(defaultConfig())
const askFlowConfig = ref({
  defaultFlow: 'basic',
  advancedEnabled: false,
  advancedRoles: ['super_admin'],
  datasetPolicies: {},
})
const mcpServersText = ref('[]')
const importDialogVisible = ref(false)
const skillImportText = ref('')
const importReport = ref(null)
const router = useRouter()
const { isFeatureEnabled, loadFeatureFlags } = useFeatureFlags()
const advancedFeatureKeys = [
  'advanced_capability_save',
  'advanced_skill_import',
  'advanced_capability_reset',
]
const featureAccess = computed(() => advancedFeatureKeys.reduce((map, key) => {
  map[key] = isFeatureEnabled(key)
  return map
}, {}))

const syncMcpText = () => {
  mcpServersText.value = JSON.stringify(config.value.mcp?.servers || [], null, 2)
}

const applyConfig = (payload = {}) => {
  config.value = {
    ...defaultConfig(),
    ...payload,
    execution: { ...defaultConfig().execution, ...(payload.execution || {}) },
    skills: Array.isArray(payload.skills) ? payload.skills : [],
    mcp: { ...defaultConfig().mcp, ...(payload.mcp || {}) },
    sqlServer: { ...defaultConfig().sqlServer, ...(payload.sqlServer || {}) },
  }
  config.value.execution.preserveFinalReportContract = true
  config.value.execution.fallbackToBasicEngine = false
  syncMcpText()
}

const requiredSkills = ['organization_scope','schema_link','semantic_align','explain_guard','result_assertions','dataset_route','asset_pack','route_guard','planner','sql_generate','sql_review','sql_execute','self_check','report_compose']
const sortedSkills = computed(() => [...(config.value.skills || [])].sort((a, b) => Number(a.order || 999) - Number(b.order || 999)))
const enabledSkillCount = computed(() => sortedSkills.value.filter(item => item.enabled !== false).length)
const externalToolSummary = computed(() => {
  const items = []
  if (config.value.mcp?.enabled) items.push('MCP')
  if (config.value.sqlServer?.enabled) items.push('SQL Server')
  return items.length ? items.join(' / ') : '未开启'
})
const hasAdvancedDatasetPolicy = computed(() => Object.values(askFlowConfig.value.datasetPolicies || {}).some(flow => flow === 'advanced'))
const askFlowReady = computed(() => config.value.enabled && askFlowConfig.value.advancedEnabled)
const askFlowStatus = computed(() => {
  if (!config.value.enabled) return {label:'已关闭',hint:'高阶能力已关闭，普通问数共享护栏继续执行'}
  if (!askFlowConfig.value.advancedEnabled) return {label:'入口未开放',hint:'请在流程控制中开放高阶研究，再核对角色与数据集策略'}
  return {label:'已开放',hint:askFlowConfig.value.defaultFlow==='advanced'?'默认进入高阶研究，仍需满足角色与数据集策略':'按角色与数据集策略进入高阶研究；默认普通问数不代表高阶未生效'}
})
const skillScope=ref('all')
const skillSearch=ref('')
const visibleSkills=computed(()=>sortedSkills.value.filter(row=>{
  const scope=skillScope.value==='all'||(skillScope.value==='shared'?runtime(row).flows.length===2:runtime(row).flows.length===1)
  const query=skillSearch.value.trim().toLowerCase()
  return scope && (!query || [row.label,row.key,row.description].join(' ').toLowerCase().includes(query))
}))
const skillEditorVisible=ref(false)
const skillDraft=ref(null)
const promptKeys=['dataset_route','asset_pack','route_guard','semantic_align','planner','golden_sql','sql_generate','sql_review','report_compose']
const sharedKeys=['organization_scope','schema_link','semantic_align','explain_guard','result_assertions','dataset_route','asset_pack','route_guard','golden_sql','sql_generate','sql_review','sql_execute','report_compose']
const runtime=row=>row.runtime || {flows:sharedKeys.includes(row.key)?['basic','advanced']:['advanced'],promptEditable:promptKeys.includes(row.key)&&!row.custom,parameterEditable:row.key==='schema_link',executor:row.custom?'archive':promptKeys.includes(row.key)?'prompt':'deterministic'}
const flowLabel=row=>runtime(row).flows.length===2?'普通 / 高阶':runtime(row).flows.includes('advanced')?'高阶研究':'普通问数'
const bindingLabel=row=>row.custom?'仅存档 · 未接执行器':runtime(row).promptEditable?'指令已绑定专家':runtime(row).parameterEditable?'参数已接入剪枝':requiredSkills.includes(row.key)?'固定护栏 · 始终执行':'高阶结果诊断'
const editSkill=row=>{skillDraft.value=JSON.parse(JSON.stringify(row));skillDraft.value.config ||= {};skillEditorVisible.value=true}
const saveSkill=async()=>{
  if(!skillDraft.value?.label?.trim()){ElMessage.warning('请填写技能名称');return}
  const index=config.value.skills.findIndex(item=>item.key===skillDraft.value.key)
  const previous=config.value.skills[index]
  config.value.skills[index]=JSON.parse(JSON.stringify(skillDraft.value))
  if(await handleSave())skillEditorVisible.value=false
  else config.value.skills[index]=previous
}
const prettyConfig = computed(() => JSON.stringify(config.value, null, 2))

const toolTypeLabel = (type) => ({
  dataset: '数据资产',
  sql: 'SQL',
  python: 'Python',
  report: '报告',
  fact: '规划',
  confirm: '确认',
}[type] || '通用')

const loadConfig = async () => {
  loading.value = true
  try {
    const res = await getAdvancedCapabilitiesConfig()
    applyConfig(res?.data?.config || {})
    if (res?.data?.entryPolicy) Object.assign(askFlowConfig.value, res.data.entryPolicy)
  } finally {
    loading.value = false
  }
}

const loadAskFlowState = async () => {
  askFlowLoading.value = true
  try {
    const res = await getAskFlowConfig({ silent: true })
    askFlowConfig.value = {
      ...askFlowConfig.value,
      ...(res?.data?.config || {}),
      datasetPolicies: res?.data?.config?.datasetPolicies || {},
    }
  } catch {
    // Ask-flow control is super-admin only. Keep the page usable for admins.
  } finally {
    askFlowLoading.value = false
  }
}

const goAskFlowControl = () => {
  router.push('/admin-console?tab=ask-flow')
}

const buildPayload = () => {
  let servers = []
  try {
    const parsed = JSON.parse(mcpServersText.value || '[]')
    servers = Array.isArray(parsed) ? parsed : []
  } catch {
    throw new Error('MCP 服务列表必须是 JSON 数组')
  }
  return {
    ...config.value,
    mcp: {
      ...config.value.mcp,
      servers,
    },
    execution: {
      ...config.value.execution,
      preserveFinalReportContract: true,
      fallbackToBasicEngine: false,
    },
  }
}

const handleSave = async () => {
  saving.value = true
  try {
    const payload = buildPayload()
    const res = await saveAdvancedCapabilitiesConfig(payload)
    applyConfig(res?.data?.config || payload)
    ElMessage.success('技能配置已保存，对后续新任务生效')
    return true
  } catch (error) {
    ElMessage.error(error?.response?.data?.error || error?.message || '保存失败')
    return false
  } finally {
    saving.value = false
  }
}

const openImportDialog = () => {
  importReport.value = null
  if (!skillImportText.value.trim()) {
    skillImportText.value = JSON.stringify({
      skills: [
        {
          key: 'cohort_analysis',
          label: '客群分层分析 Skill',
          toolType: 'python',
          description: '按客户、组织、指标或时间窗口做分层对比和贡献度分析。',
          prompt: '根据用户问题识别分层维度，输出分组、指标、排序和异常节点。',
          safety: { executeCode: false, requiresReview: true },
        },
      ],
    }, null, 2)
  }
  importDialogVisible.value = true
}

const handleImportSkills = async () => {
  importing.value = true
  try {
    const manifest = JSON.parse(skillImportText.value || '{}')
    const res = await importAdvancedSkills(manifest)
    applyConfig(res?.data?.config || {})
    importReport.value = {
      imported: res?.data?.imported || [],
      skipped: res?.data?.skipped || [],
    }
    ElMessage.success(`Skill 导入完成：${importReport.value.imported.length} 个`)
  } catch (error) {
    ElMessage.error(error?.response?.data?.error || error?.message || 'Skill Manifest 格式不正确')
  } finally {
    importing.value = false
  }
}

const handleReset = async () => {
  try {
    await ElMessageBox.confirm('将恢复技能与工具默认配置，确认继续吗？', '恢复默认', {
      type: 'warning',
      confirmButtonText: '恢复默认',
      cancelButtonText: '取消',
    })
  } catch {
    return
  }
  resetting.value = true
  try {
    const res = await resetAdvancedCapabilitiesConfig()
    applyConfig(res?.data?.config || {})
    ElMessage.success('技能与工具配置已恢复默认')
  } finally {
    resetting.value = false
  }
}

watch(() => config.value.mcp?.enabled, () => {
  if (!mcpServersText.value) syncMcpText()
})

onMounted(() => {
  loadFeatureFlags()
  loadConfig()
  loadAskFlowState()
})
</script>

<style scoped>
.advanced-page{min-height:100%;max-width:1600px;margin:0 auto;padding:4px 0 28px;color:#18222f}.advanced-hero{display:flex;justify-content:space-between;align-items:center;gap:24px;padding:8px 0 26px;background:transparent;border:0;box-shadow:none}.eyebrow{font-size:11px;letter-spacing:.06em;color:#637184;margin:0 0 7px}.advanced-hero h1{font-size:25px;font-weight:600;letter-spacing:-.6px;margin:0}.advanced-hero p:last-child{margin:8px 0 0;color:#687586;font-size:13px;line-height:1.7}.hero-actions{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}.hero-actions :deep(.el-button+.el-button){margin-left:0}.capability-status-strip{display:flex;flex-wrap:wrap;gap:28px;align-items:center;padding:16px 20px;border:1px solid #e3e7ec;background:#fff;border-radius:10px;margin-bottom:20px;font-size:12px;color:#87919f}.capability-status-strip>span{display:flex;align-items:center;gap:9px}.capability-status-strip strong{color:#45566d;font-size:12px;font-weight:500}.status-dot{width:6px;height:6px;border-radius:50%;background:#526b7a}.advanced-workbench{background:#fff;border:1px solid #e2e6eb;border-radius:12px;padding:0;overflow:hidden}.advanced-tabs{min-height:600px}.advanced-tabs :deep(.el-tabs__header.is-left){width:180px;margin:0;padding:20px 14px;background:#f9fafb;border-right:1px solid #e8ebef;float:left}.advanced-tabs :deep(.el-tabs__nav-wrap::after){display:none}.advanced-tabs :deep(.el-tabs__active-bar){display:none}.advanced-tabs :deep(.el-tabs__item.is-left){justify-content:flex-start;text-align:left;padding:0 14px;height:42px;font-size:12px;font-weight:400;border-radius:7px;margin-bottom:4px;color:#738092}.advanced-tabs :deep(.el-tabs__item.is-active){background:#edf2f8;color:#3c536e;font-weight:500}.advanced-tabs :deep(.el-tabs__content){padding:27px 30px;min-width:0;overflow:hidden}.plain-panel{border:0;background:transparent;padding:0;min-width:0}.plain-panel h2{font-size:18px;font-weight:550;margin:0 0 8px;letter-spacing:-.3px}.plain-panel p,.plain-panel li,.switch-list small{color:#637184;font-size:12px;line-height:1.8}.plain-panel ul{padding-left:17px;list-style:disc}.plain-panel li{margin:10px 0}.panel-head{display:flex;align-items:flex-start;justify-content:space-between;gap:18px;margin-bottom:24px}.panel-head p{max-width:650px;margin:0}.panel-actions{display:flex;gap:12px;align-items:center;flex-wrap:wrap;justify-content:flex-end}.panel-actions :deep(.el-switch__label){font-size:11px}.skill-library-toolbar{display:flex;align-items:center;justify-content:space-between;gap:18px;padding-bottom:20px}.skill-library-toolbar>.el-input{max-width:330px}.skill-scope-filter{display:flex;gap:3px;flex-wrap:wrap;background:#f2f4f7;border-radius:7px;padding:3px}.skill-scope-filter button{padding:6px 12px;border:0;border-radius:5px;font-size:11px;color:#738095;white-space:nowrap}.skill-scope-filter button[aria-pressed=true]{background:#fff;color:#3c536e;box-shadow:0 1px 3px #1423370c}.skill-list-caption{display:flex;justify-content:space-between;font-size:11px;color:#98a1ac;padding:13px 0;border-block:1px solid #e9edf1}.skill-library-row{display:flex;align-items:center;gap:16px;padding:19px 0;border-bottom:1px solid #edf0f3}.skill-library-row:last-child{border-bottom:0}.skill-emblem{height:33px;width:33px;flex-shrink:0;display:flex;align-items:center;justify-content:center;color:#8797aa;border:1px solid #e5e9ef;border-radius:8px;background:#f5f7fa}.skill-emblem.fixed{color:#688291;background:#f5f8fa}.skill-emblem svg{width:18px;height:18px}.skill-identity{display:block;text-align:left;flex:1;min-width:0}.skill-identity>span{display:flex;align-items:center;gap:10px;flex-wrap:wrap}.skill-identity strong{font-size:13px;font-weight:550;color:#314156}.skill-identity small{font-size:10px;color:#7f91a5;background:#f1f5f8;padding:2px 6px;border-radius:4px}.skill-identity p{font-size:12px;line-height:1.7;color:#637184;margin:7px 0 4px}.skill-identity code{font-size:10px;color:#a0aab6}.skill-runtime{width:145px;flex-shrink:0;display:flex;flex-direction:column;gap:8px;font-size:11px;color:#687e96}.skill-runtime small{font-size:10px;color:#9aa4b1}.skill-row-actions{display:flex;align-items:center;gap:18px}.skill-row-actions :deep(.el-button){color:#526b87;background:#fff;border-color:#e0e7ef}.skill-identity:hover strong{color:#3c536e}.capability-flow-map{display:grid;grid-template-columns:1fr 1fr;gap:25px;margin-bottom:18px;border-bottom:1px solid #e8ecf1;padding-bottom:22px}.flow-map-label{display:block;font-size:11px;color:#8290a0;margin-bottom:10px}.capability-flow-map strong{font-size:13px;color:#405772;font-weight:500;line-height:1.9}.capability-flow-map p{font-size:12px;color:#637184;line-height:1.8;margin:8px 0 0}.capability-related{display:flex;flex-wrap:wrap;gap:20px;margin:18px 0 32px}.capability-related :deep(.el-button){font-size:12px;color:#557391}.overview-grid{display:grid;grid-template-columns:1.1fr 1fr;gap:36px}.summary-list{display:grid;gap:0}.summary-list>div{display:flex;justify-content:space-between;gap:14px;padding:12px 0;border-bottom:1px solid #edf0f4;font-size:12px}.summary-list span{color:#8490a0}.summary-list strong{font-weight:500;color:#546980}.flow-warning{font-size:12px;line-height:1.8;color:#806b47;background:#f5f2ec;padding:14px;border-radius:6px;margin-top:18px}.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px 24px}.form-wide{grid-column:1/-1}.switch-list{display:grid;gap:0;margin-top:24px}.switch-list label{display:flex;justify-content:space-between;gap:24px;align-items:center;padding:22px 0;border-bottom:1px solid #e9edf1}.switch-list strong{display:block;font-size:13px;font-weight:500;color:#485d75;margin-bottom:6px}.switch-list small{display:block}.slider-row{margin-top:28px;display:grid;grid-template-columns:150px minmax(0,1fr);align-items:center;gap:20px;font-size:12px;color:#687b92}.json-preview{max-height:550px;overflow:auto;background:#f5f7fa;border:1px solid #e6ebf1;border-radius:8px;color:#51657e;font-size:12px;line-height:1.8;padding:20px}.skill-binding-summary{display:flex;gap:12px;flex-wrap:wrap;align-items:center;padding:0 0 20px;margin-bottom:20px;border-bottom:1px solid #e2e8f0;font-size:12px;color:#61748d}.skill-binding-summary strong{font-weight:500;color:#344b68}.skill-binding-summary code{font-size:11px}.skill-editor-hint{font-size:12px;line-height:1.8;color:#657892;margin:12px 0 0}.import-panel p{font-size:12px;color:#718198;line-height:1.8;margin-bottom:16px}.import-report{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}.import-report ul{width:100%;font-size:12px;color:#806b47;line-height:1.8}@media(max-width:1200px){.advanced-tabs :deep(.el-tabs__header.is-left){width:150px;padding:16px 10px}.advanced-tabs :deep(.el-tabs__content){padding:24px}.skill-runtime{display:none}.panel-head{flex-direction:column}.panel-actions{justify-content:flex-start}.advanced-hero{align-items:flex-start}.hero-actions{max-width:360px}.skill-library-toolbar{flex-wrap:wrap}}@media(max-width:750px){.advanced-hero{flex-direction:column}.hero-actions{justify-content:flex-start;max-width:none}.capability-status-strip{gap:16px}.advanced-tabs :deep(.el-tabs__header.is-left){float:none;width:100%;padding:10px;border-right:0;border-bottom:1px solid #e6ebf1}.advanced-tabs :deep(.el-tabs__nav){display:flex;flex-direction:row;flex-wrap:wrap;gap:3px}.advanced-tabs :deep(.el-tabs__item.is-left){height:34px;padding:0 10px;margin:0;font-size:11px}.advanced-tabs :deep(.el-tabs__content){padding:20px 16px}.skill-list-caption span:last-child{display:none}.skill-emblem{display:none}.skill-row-actions{gap:8px;flex-direction:column}.skill-identity strong{font-size:12px}.skill-identity p{font-size:11px}.skill-library-row{gap:12px}.capability-flow-map,.overview-grid,.form-grid{grid-template-columns:1fr}.slider-row{grid-template-columns:1fr}.skill-library-toolbar>.el-input{max-width:none}}
</style>
