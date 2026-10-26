<template>
  <el-drawer v-model="visible" title="最近分析" direction="ltr" size="min(420px, 100vw)" append-to-body class="analysis-history-drawer" @closed="search = ''">
    <template #header>
      <div class="history-heading"><span class="history-kicker">你的分析空间</span><h2>最近分析 <span>{{ sessions.length }}</span></h2></div>
    </template>
    <div class="history-tools">
      <el-input v-model="search" placeholder="搜索问题或数据集" :prefix-icon="Search" clearable aria-label="搜索历史分析" />
      <button v-if="allowNewChat" class="history-new" type="button" @click="newChat"><el-icon><Plus /></el-icon>新分析</button>
    </div>
    <p v-if="busy" class="history-notice">当前任务正在运行，可以浏览记录，完成后再切换。</p>
    <div class="history-scroll">
      <section v-for="group in groups" :key="group.label" class="history-group">
        <h3>{{ group.label }}<span>{{ group.items.length }}</span></h3>
        <article v-for="item in group.items" :key="item.id" class="history-record" :class="{ 'is-selected': item.id === activeSessionId }">
          <button class="history-select" type="button" :aria-current="item.id === activeSessionId ? 'true' : undefined" :disabled="busy" @click="select(item)">
            <span class="history-record-title">{{ question(item) }}</span>
            <span class="history-record-meta"><span>{{ item.datasetName || item.reportSnapshot?.datasetName || '分析记录' }}</span><time>{{ timeLabel(item) }}</time></span>
          </button>
          <button v-if="allowDelete" class="history-delete" type="button" :aria-label="`删除分析：${question(item)}`" @click="$emit('deleteSession', item, $event)"><el-icon><Delete /></el-icon></button>
        </article>
      </section>
      <div v-if="!groups.length" class="history-empty"><el-icon :size="26"><Search v-if="search" /><Clock v-else /></el-icon><strong>{{ search ? '没有找到相关分析' : '从第一个问题开始' }}</strong><span>{{ search ? '试试其他问题关键词或数据集名称' : '完成的分析将保存在这里，随时回来继续探索' }}</span></div>
    </div>
    <template #footer><div class="history-footer"><span>仅显示当前账号的分析记录</span><button v-if="sessions.length && allowClear" type="button" @click="$emit('clearAll')">清空记录</button></div></template>
  </el-drawer>
</template>

<script setup>
import { computed, ref } from 'vue'
import { Search, Plus, Clock, Delete } from '@element-plus/icons-vue'
const props = defineProps({ sessions:{type:Array,default:()=>[]},activeSessionId:{type:String,default:''},allowClear:{type:Boolean,default:true},allowDelete:{type:Boolean,default:true},allowNewChat:{type:Boolean,default:true},busy:{type:Boolean,default:false} })
const emit = defineEmits(['newChat','selectSession','deleteSession','clearAll'])
const visible=ref(false), search=ref('')
const question=item=>String(item.question || item.reportSnapshot?.question || item.title || '未命名分析')
const dateOf=item=>{const date=new Date(item.serverUpdatedAt || item.updatedAt || item.reportSnapshot?.updatedAt || '');return Number.isNaN(date.getTime())?null:date}
const timeLabel=item=>{const date=dateOf(item);return date?new Intl.DateTimeFormat('zh-CN',{month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit',hour12:false}).format(date):'时间未记录'}
const groups=computed(()=>{
  const now=new Date(),today=new Date(now.getFullYear(),now.getMonth(),now.getDate()).getTime()
  const yesterday=new Date(now.getFullYear(),now.getMonth(),now.getDate()-1).getTime()
  const week=new Date(now.getFullYear(),now.getMonth(),now.getDate()-6).getTime()
  const buckets=new Map(['今天','昨天','近七天','更早','时间未记录'].map(label=>[label,[]]))
  const keyword=search.value.trim().toLocaleLowerCase()
  const items=props.sessions.filter(item=>`${question(item)} ${item.datasetName || item.reportSnapshot?.datasetName || ''}`.toLocaleLowerCase().includes(keyword)).slice().sort((a,b)=>(dateOf(b)?.getTime()||0)-(dateOf(a)?.getTime()||0))
  for(const item of items){const time=dateOf(item)?.getTime();const label=time===undefined?'时间未记录':time>=today?'今天':time>=yesterday?'昨天':time>=week?'近七天':'更早';buckets.get(label).push(item)}
  return [...buckets].filter(([,items])=>items.length).map(([label,items])=>({label,items}))
})
const select=item=>{if(props.busy)return;emit('selectSession',item);visible.value=false}
const newChat=()=>{emit('newChat');visible.value=false}
defineExpose({open:()=>{visible.value=true}})
</script>

<style>
.analysis-history-drawer{--el-drawer-padding-primary:24px;background:#fff;color:#26364b;box-shadow:12px 0 50px #172c4d14!important}
.analysis-history-drawer .el-drawer__header{margin:0;padding:28px 24px 20px;border-bottom:1px solid #edf0f5;align-items:center}
.analysis-history-drawer .el-drawer__body{display:flex;flex-direction:column;min-height:0;padding:20px 16px 0;overflow:hidden}
.analysis-history-drawer .el-drawer__footer{padding:16px 24px;border-top:1px solid #edf0f5}
.history-kicker{font-size:11px;color:#617085;letter-spacing:1px}.history-heading h2{font-size:21px;font-weight:600;letter-spacing:-.5px;color:#20324b;margin:6px 0 0}.history-heading h2 span{font-size:12px;font-weight:400;color:#687b92;margin-left:7px;letter-spacing:0}
.history-tools{display:flex;gap:10px;align-items:center;padding:0 8px 16px}.history-tools .el-input{min-width:0}.history-tools .el-input__wrapper{background:#f6f8fb;box-shadow:0 0 0 1px #e5eaf2 inset;border-radius:8px;min-height:36px}
.history-new{display:flex;align-items:center;gap:6px;white-space:nowrap;border:1px solid #dce5ef;background:#edf2f8;color:#425f83;border-radius:8px;padding:9px 10px;font-size:12px;cursor:pointer}
.history-scroll{min-height:0;overflow:auto;flex:1;padding:0 6px 18px;scrollbar-width:thin;scrollbar-color:#d4ddea transparent}.history-group{margin:0 0 18px}.history-group h3{display:flex;align-items:center;gap:8px;font-size:11px;font-weight:500;letter-spacing:.5px;color:#617085;margin:9px 10px}.history-group h3 span{color:#7a8ba1;font-size:11px}
.history-record{display:flex;align-items:center;gap:4px;border:1px solid transparent;border-radius:9px;margin:3px 0;padding-right:7px;transition:background .15s,border-color .15s}.history-record:hover{background:#f6f8fb}.history-record.is-selected{background:#edf2f8;border-color:#edf2f8}.history-select{display:flex;flex-direction:column;gap:10px;flex:1;min-width:0;align-items:stretch;text-align:left;border:0;background:none;padding:13px 10px;color:#26364b;cursor:pointer}.history-select:disabled{cursor:default;opacity:1}.history-record-title{font-size:13px;line-height:1.65;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;overflow-wrap:anywhere}.history-record-meta{display:flex;justify-content:space-between;align-items:center;gap:10px;color:#687b92;font-size:11px;line-height:1.5}.history-record-meta>span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0}.history-record-meta time{white-space:nowrap;font-variant-numeric:tabular-nums;flex-shrink:0}
.history-delete{display:grid;place-items:center;flex-shrink:0;width:30px;height:32px;border:0;background:none;color:#8190a5;border-radius:6px;cursor:pointer}.history-delete:hover{background:#faf7f7;color:#8b6064}.history-delete:focus-visible,.history-select:focus-visible,.history-new:focus-visible{outline:2px solid #425f83;outline-offset:2px}
.history-empty{display:flex;align-items:center;flex-direction:column;gap:12px;text-align:center;padding:64px 18px;color:#718299}.history-empty strong{font-size:14px;font-weight:500;color:#40536d}.history-empty span{font-size:12px;line-height:1.8}.history-footer{display:flex;align-items:center;justify-content:space-between;gap:12px;color:#687b92;font-size:11px}.history-footer button{padding:5px 0;color:#6b7c93;background:none;border:0;font:inherit;cursor:pointer}.history-footer button:hover{color:#8b6064}.history-notice{font-size:12px;line-height:1.7;background:#f5f7fa;color:#556985;margin:0 8px 12px;padding:10px;border-radius:8px}
@media(pointer:coarse){.history-delete{min-width:44px;min-height:44px}}@media(prefers-reduced-motion:reduce){.history-record{transition:none}}
</style>
