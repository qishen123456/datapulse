<template>
  <div class="module-layout-v4 db-page admin-workspace">
    <div class="admin-page-head">
      <div>
        <div class="admin-kicker">DATA SOURCES</div>
        <h2>数据源管理</h2>
        <p>维护问数系统可访问的数据连接、默认库与连通性状态。</p>
      </div>
      <el-button v-if="isFeatureEnabled('datasource_create')" type="primary" :icon="Plus" @click="openAdd">添加数据源</el-button>
    </div>
    <div class="db-summary-strip" aria-label="连接概览">
      <span><strong>{{ connections.length }}</strong> 个数据源</span>
      <span><i class="db-status-dot"></i><strong>{{ connections.filter(c=>c.is_active).length }}</strong> 已启用</span>
      <span><strong>{{ new Set(connections.map(c=>c.type)).size }}</strong> 种数据库类型</span>
      <small>启用状态不代表已通过连通性测试</small>
    </div>
    <div class="db-workbench">
    <aside class="db-detail" v-if="selectedConnection">
      <div class="db-detail-mark"><el-icon><Coin /></el-icon></div>
      <span class="db-detail-eyebrow">连接详情</span>
      <h3>{{ selectedConnection.name }}</h3>
      <span class="db-engine">{{ selectedConnection.type.toUpperCase() }}</span>
      <dl>
        <div><dt>主机 / 路径</dt><dd>{{ selectedConnection.type==='sqlite' ? selectedConnection.sqlite_path : `${selectedConnection.host}:${selectedConnection.port}` }}</dd></div>
        <div><dt>数据库</dt><dd>{{ selectedConnection.database_name || '—' }}</dd></div>
        <div><dt>访问账号</dt><dd>{{ selectedConnection.username || '—' }}</dd></div>
        <div><dt>使用状态</dt><dd><i class="db-status-dot" :class="{inactive:!selectedConnection.is_active}"></i>{{ selectedConnection.is_active?'已启用':'已禁用' }}<span v-if="selectedConnection.is_default"> · 默认连接</span></dd></div>
      </dl>
      <div class="db-detail-actions">
        <el-button v-if="isFeatureEnabled('datasource_edit')" :icon="Edit" @click="openEdit(selectedConnection)">编辑连接</el-button>
        <el-button v-if="isFeatureEnabled('datasource_test')" :loading="testingId===selectedConnection.id" @click="testConn(selectedConnection)">测试</el-button>
      </div>
    </aside>
    <section class="db-inventory">
      <div class="db-inventory-toolbar">
        <div><h3>连接目录</h3><span>{{ filteredConnections.length }} 个结果</span></div>
        <el-input v-model="connectionSearch" clearable placeholder="搜索连接、主机或数据库" :prefix-icon="Search" />
      </div>
    <el-card class="admin-table-card">
      <template #header>
        <div class="card-header">
          <span class="db-table-caption">选择连接查看配置</span>
          <el-button v-if="isFeatureEnabled('datasource_test')" plain :icon="Connection" :disabled="!connections.length" @click="testActiveConnections">批量测试活跃连接</el-button>
        </div>
      </template>

      <el-table :data="filteredConnections" v-loading="loading" highlight-current-row @row-click="selectedConnectionId=$event.id">
        <el-table-column prop="name" label="名称" min-width="180">
          <template #default="{ row }">
            <el-text strong>{{ row.name }}</el-text>
            <el-tag v-if="row.is_default" type="warning" size="small" style="margin-left:6px">默认</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="110">
          <template #default="{ row }">
            <el-tag :type="typeTag(row.type)">{{ row.type.toUpperCase() }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="主机/路径" min-width="160">
          <template #default="{ row }">
            <el-text type="info" size="small">{{ row.type === 'sqlite' ? row.sqlite_path : `${row.host}:${row.port}` }}</el-text>
          </template>
        </el-table-column>
        <el-table-column prop="database_name" label="数据库" width="130" show-overflow-tooltip />
        <el-table-column prop="is_active" label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'">{{ row.is_active ? '已启用' : '已禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240">
          <template #default="{ row }">
            <div style="white-space: nowrap">
              <el-button v-if="isFeatureEnabled('datasource_test')" link :icon="Connection" :loading="testingId === row.id" @click="testConn(row)">测试</el-button>
              <el-button v-if="isFeatureEnabled('datasource_edit')" link :icon="Edit" @click="openEdit(row)">编辑</el-button>
              <el-popconfirm v-if="isFeatureEnabled('datasource_delete')" title="确认删除此数据源？" @confirm="deleteConn(row.id)">
                <template #reference>
                  <el-button link type="danger" :icon="Delete">删除</el-button>
                </template>
              </el-popconfirm>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    </section>

    </div>

    <!-- 添加/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑数据源' : '添加数据源'" width="600px" @close="resetForm">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="连接名称" prop="name">
          <el-input v-model="form.name" placeholder="例如：生产CRM库" />
        </el-form-item>
        <el-form-item label="数据库类型" prop="type">
          <el-select v-model="form.type" style="width:100%" @change="onTypeChange">
            <el-option label="SQLite（本地文件，无需驱动）" value="sqlite" />
            <el-option label="MySQL" value="mysql" />
            <el-option label="PostgreSQL (PGSQL)" value="postgresql" />
            <el-option label="SQL Server (MSSQL)" value="sqlserver" />
          </el-select>
        </el-form-item>

        <!-- SQLite -->
        <template v-if="form.type === 'sqlite'">
          <el-form-item label="文件路径" prop="sqlite_path">
            <el-input v-model="form.sqlite_path" placeholder="例如：./test.db 或 D:/data/mydb.db" />
          </el-form-item>
        </template>

        <!-- MySQL / PostgreSQL / MSSQL -->
        <template v-else>
          <el-row :gutter="12">
            <el-col :span="16">
              <el-form-item label="主机地址" prop="host">
                <el-input v-model="form.host" placeholder="localhost 或 IP" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="端口" prop="port">
                <el-input v-model.number="form.port" :placeholder="getDefaultPort()" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label="数据库名" prop="database_name">
            <el-input v-model="form.database_name" placeholder="数据库名称" />
          </el-form-item>
          <el-row :gutter="12">
            <el-col :span="12">
              <el-form-item label="用户名" prop="username">
                <el-input v-model="form.username" placeholder="用户名" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="密码" prop="password">
                <el-input v-model="form.password" type="password" placeholder="密码（留空则不修改）" show-password />
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item v-if="form.type === 'sqlserver'" label="ODBC驱动">
            <el-input v-model="form.driver" placeholder="ODBC Driver 17 for SQL Server" />
          </el-form-item>
          <el-form-item v-if="form.type === 'postgresql'" label="驱动类型">
            <el-input v-model="form.driver" placeholder="psycopg2" />
          </el-form-item>
        </template>

        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="启用">
              <el-switch v-model="form.is_active" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="设为默认">
              <el-switch v-model="form.is_default" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button v-if="!isEdit || isFeatureEnabled('datasource_edit')" type="primary" :loading="saving" @click="submitForm">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import "../styles/module-interiors.css"
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Edit, Delete, Connection, Search, Coin } from '@element-plus/icons-vue'
import { getDataSources, createDataSource, updateDataSource, deleteDataSource, testDataSource } from '../api/index.js'
import { useFeatureFlags } from '../state/featureFlags.js'

const connections = ref([])
const connectionSearch = ref('')
const selectedConnectionId = ref(null)
const filteredConnections = computed(()=>connections.value.filter(item=>[item.name,item.host,item.database_name,item.type].join(' ').toLowerCase().includes(connectionSearch.value.toLowerCase())))
const selectedConnection = computed(()=>filteredConnections.value.find(item=>item.id===selectedConnectionId.value) || filteredConnections.value[0] || null)
const loading = ref(false)
const saving = ref(false)
const testingId = ref(null)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()
const { isFeatureEnabled, loadFeatureFlags } = useFeatureFlags()

const defaultForm = () => ({ name:'', type:'sqlite', sqlite_path:'./test.db', host:'', port:3306, database_name:'', username:'', password:'', driver:'psycopg2', is_active:true, is_default:false })
const form = ref(defaultForm())

const rules = {
  name: [{ required: true, message: '请输入连接名称' }],
  type: [{ required: true, message: '请选择类型' }],
}

const typeTag = (type) => ({ sqlite:'info', mysql:'success', postgresql:'primary', sqlserver:'warning' }[type] || 'primary')

const loadData = async () => {
  loading.value = true
  try { const data = await getDataSources(); connections.value = data.databases || [] }
  finally { loading.value = false }
}

const getDefaultPort = () => {
  switch (form.value.type) {
    case 'mysql': return 3306
    case 'postgresql': return 5432
    case 'sqlserver': return 1433
    default: return 3306
  }
}

const onTypeChange = (t) => { 
  form.value.port = getDefaultPort()
  form.value.driver = t === 'sqlserver' ? 'ODBC Driver 17 for SQL Server' : t === 'postgresql' ? 'psycopg2' : ''
}

const openAdd = () => { isEdit.value = false; form.value = defaultForm(); dialogVisible.value = true }
const openEdit = (row) => {
  isEdit.value = true
  form.value = { ...defaultForm(), ...row, password: '' }
  dialogVisible.value = true
}
const resetForm = () => { formRef.value?.resetFields() }

const submitForm = async () => {
  await formRef.value.validate()
  saving.value = true
  try {
    if (isEdit.value) {
      await updateDataSource(form.value.id, form.value)
      ElMessage.success('数据源已更新')
    } else {
      await createDataSource(form.value)
      ElMessage.success('数据源已添加')
    }
    dialogVisible.value = false
    loadData()
  } finally { saving.value = false }
}

const deleteConn = async (id) => {
  await deleteDataSource(id)
  ElMessage.success('已删除')
  loadData()
}

const testConn = async (row) => {
  testingId.value = row.id
  try {
    const res = await testDataSource(row.id)
    ElMessage.success(res.message || '连接成功')
  } catch (e) {
    // 错误已由拦截器处理
  } finally { testingId.value = null }
}

const testActiveConnections = async () => {
  const activeConnections = connections.value.filter(connection => connection.is_active)
  if (!activeConnections.length) {
    ElMessage.info('暂无活跃数据源可测试')
    return
  }
  for (const connection of activeConnections) {
    await testConn(connection)
  }
}

onMounted(() => {
  loadFeatureFlags()
  loadData()
})
</script>

<style scoped>
.db-page{padding:0;max-width:1800px;margin:0 auto;color:#18222f}
.db-page .admin-page-head{padding:0 0 24px;margin:0;border:0;border-radius:0;background:transparent;box-shadow:none;display:flex;align-items:center;justify-content:space-between;gap:20px}
.db-page .admin-kicker{font-size:11px;letter-spacing:.1em;color:#7b8697;margin-bottom:8px}.db-page h2{font-size:25px;letter-spacing:-.6px;font-weight:600}.db-page .admin-page-head p{font-size:13px;color:#6d7888;margin-top:8px}
.db-summary-strip{display:flex;align-items:center;gap:26px;padding:14px 0 22px;border-top:1px solid #e6e9ee;font-size:12px;color:#677485;flex-wrap:wrap}.db-summary-strip strong{font-size:17px;color:#26364b;font-weight:550;margin-right:5px}.db-summary-strip small{margin-left:auto;color:#84909d;font-size:11px}.db-status-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#2b987b;margin-right:6px}.db-status-dot.inactive{background:#9ba5b1}
.db-workbench{display:grid;grid-template-columns:minmax(0,1fr) 260px;border:1px solid #e1e5eb;border-radius:12px;background:#fff;overflow:hidden;min-height:420px}.db-inventory{min-width:0}.db-inventory-toolbar{padding:22px 22px 14px;display:flex;align-items:center;justify-content:space-between;gap:20px}.db-inventory-toolbar>div:first-child{display:flex;align-items:baseline;gap:10px}.db-inventory-toolbar h3{font-size:14px;font-weight:600;white-space:nowrap}.db-inventory-toolbar span{font-size:11px;color:#7e8998;white-space:nowrap}.db-inventory-toolbar>.el-input{width:270px}.db-page .admin-table-card{border:0!important;box-shadow:none!important;border-radius:0!important}.db-page .admin-table-card :deep(.el-card__header){padding:0 22px 15px;border:0}.db-table-caption{font-size:11px;color:#8b95a3}.card-header{display:flex;align-items:center;justify-content:space-between;gap:12px}.admin-table-card :deep(.el-card__body){padding:0}.admin-table-card :deep(.el-table){border-radius:0!important;font-size:12px}.admin-table-card :deep(.el-table__row){cursor:pointer}.admin-table-card :deep(.el-table th.el-table__cell){background:#f8f9fb;color:#7c8796;font-weight:500;height:40px}.admin-table-card :deep(.el-table td.el-table__cell){height:58px}.admin-table-card :deep(.el-table .cell){padding-left:20px;padding-right:16px}
.db-detail{padding:25px 22px;background:#fafbfc;border-left:1px solid #e8ebef;min-width:0}.db-detail-mark{width:38px;height:38px;display:grid;place-items:center;border:1px solid #dfe6ef;border-radius:10px;background:#f1f5f9;color:#426183;font-size:20px;margin-bottom:18px}.db-detail-eyebrow{font-size:11px;color:#8994a3}.db-detail h3{font-size:16px;font-weight:600;margin:8px 0;overflow-wrap:anywhere}.db-engine{font:10px/1.4 ui-monospace,SFMono-Regular,monospace;color:#6d7e92}.db-detail dl{margin:24px 0}.db-detail dl>div{padding:13px 0;border-top:1px solid #e9edf2}.db-detail dt{font-size:11px;color:#8490a1;margin-bottom:6px}.db-detail dd{margin:0;font-size:12px;color:#40516a;overflow-wrap:anywhere}.db-detail-actions{display:flex;gap:8px}.db-detail-actions :deep(.el-button + .el-button){margin-left:0}
@media(max-width:1200px){.db-workbench{grid-template-columns:minmax(0,1fr)}.db-detail{display:block;border-left:0;border-top:1px solid #e8ebef}.db-detail dl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 24px;margin:16px 0}.db-detail-mark{display:none}}@media(max-width:700px){.db-page{padding:0}.db-page .admin-page-head{align-items:flex-start;flex-direction:column}.db-inventory-toolbar{align-items:flex-start;flex-direction:column}.db-inventory-toolbar>.el-input{width:100%}.db-summary-strip{gap:14px}.db-summary-strip small{margin-left:0}}
</style>
