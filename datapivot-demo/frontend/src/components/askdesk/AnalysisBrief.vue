<template>
  <section class="analysis-brief" :class="{compact}" aria-label="分析过程摘要">
    <header class="brief-header"><div><span class="brief-eyebrow">本次分析</span><h3>{{ busy ? '正在把问题变成可验证的答案' : '这次分析的依据' }}</h3></div><span class="brief-count">{{ steps.length }} 项已记录依据</span></header>

    <div v-if="busy" class="analysis-live" role="status" aria-live="polite">
      <span class="live-orbit" aria-hidden="true"></span><div><strong>{{ currentTitle }}</strong><p>{{ latest || '收到查询方案或核验结果后，会在这里继续更新。' }}</p><small>依据真实执行记录更新</small></div>
    </div>

    <ol v-if="steps.length" class="analysis-story" aria-label="已记录的分析依据">
      <li v-for="step in steps" :key="step.id" :class="{warning:step.status==='warning'}" :data-fact="step.id">
        <span class="story-marker" aria-hidden="true">{{ String(step.number).padStart(2,'0') }}</span>
        <div class="story-body"><div class="story-heading"><h4><span class="story-phase">{{ phaseTitles[step.number] }}</span>{{ step.title }}</h4><span v-if="step.status==='warning'" class="story-warning">需关注</span></div><p class="story-answer">{{ step.value }}</p>
          <dl v-if="step.details.length" class="story-evidence"><div v-for="(line,i) in step.details" :key="i"><dt v-if="line.label">{{ line.label }}</dt><dd>{{ line.value }}</dd></div></dl>
        </div>
      </li>
    </ol>
    <p v-else class="brief-empty">{{ busy ? '正在确认本次问题与可用的数据范围，尚未收到查询依据。' : '本次记录没有提供分析依据。' }}</p>

    <details class="brief-parameters"><summary>按流程查看查询依据 <span>与上方四个阶段对应</span></summary>
      <section v-for="phase in phaseGroups" :key="phase.number" class="phase-evidence"><h4>{{ String(phase.number).padStart(2,'0') }} · {{ phase.title }}</h4><dl><div v-for="fact in phase.facts" :key="fact.id" :class="fact.status"><dt>{{ fact.label }}</dt><dd>{{ fact.status==='pending' ? (busy ? '尚未收到该项记录' : '本次未记录') : fact.value }}<ul v-if="fact.details.some(line=>line.value!==fact.value)"><li v-for="(line,i) in fact.details.filter(line=>line.value!==fact.value)" :key="i">{{ line.label ? line.label+'：' : '' }}{{ line.value }}</li></ul></dd></div></dl><p v-if="phase.number===4">业务解读与结论在下方结果区呈现。</p></section>
    </details>
  </section>
</template>
<script setup>
import { computed } from 'vue'
import { analysisFacts, analysisNarrative, latestAnalysisSummary } from '../../utils/analysisActivity'
const props=defineProps({workflow:{type:Object,default:()=>({})},result:Object,busy:Boolean,compact:Boolean})
const facts=computed(()=>analysisFacts(props.workflow,props.result))
const phaseFor={scope:1,sources:2,plan:2,aggregation:2,review:3,results:3}
const phaseTitles={1:'理解问题',2:'准备查询',3:'查询与核验',4:'形成回答'}
const phaseGroups=computed(()=>[1,2,3,4].map(number=>({number,title:phaseTitles[number],facts:facts.value.filter(fact=>phaseFor[fact.id]===number)})))
const steps=computed(()=>{
  const recorded=analysisNarrative(props.workflow,props.result).map((step,index)=>({...step,number:phaseFor[step.id]}))
  return props.busy ? recorded.reverse() : recorded
})
const latest=computed(()=>latestAnalysisSummary(props.workflow))
const currentTitle=computed(()=>{
  const events=props.workflow?.events || []
  const event=[...events].reverse().find(e=>e.node_id && e.title)
  return event?.title || '正在准备本次分析'
})
</script>
<style scoped>
.analysis-brief{color:#142238;padding-top:18px;min-width:0}.brief-header{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:20px}.brief-eyebrow{font-size:10px;letter-spacing:1px;color:#617085}.brief-header h3{font-size:17px;font-weight:550;margin:7px 0 0;line-height:1.6}.brief-count{font-size:11px;color:#617085;white-space:nowrap}
.analysis-live{display:flex;align-items:flex-start;gap:14px;padding:18px 20px;background:#edf2f8;border-radius:10px;margin-bottom:24px;border-left:2px solid #425f83}.analysis-live strong{font-size:13px;font-weight:550;color:#425f83}.analysis-live p{font-size:13px;line-height:1.9;color:#475569;margin:6px 0}.analysis-live small{font-size:11px;color:#617085}.live-orbit{width:15px;height:15px;border:1.5px solid #dce5ef;border-top-color:#425f83;border-radius:50%;flex-shrink:0;margin-top:3px;animation:live-spin 1.5s linear infinite}@keyframes live-spin{to{transform:rotate(360deg)}}
.analysis-story{list-style:none;margin:0;padding:0}.analysis-story>li{position:relative;display:grid;grid-template-columns:30px minmax(0,1fr);gap:16px;padding:0 0 26px}.analysis-story>li:not(:last-child):before{content:'';position:absolute;left:14px;top:30px;bottom:0;width:1px;background:#e2e8f0}.story-marker{display:grid;place-items:center;width:29px;height:29px;border-radius:50%;background:#edf2f8;color:#526b90;font:10px ui-monospace,monospace;border:1px solid #e2e8f0}.story-heading{display:flex;align-items:center;gap:10px;min-height:29px}.story-heading h4{margin:0;font-size:12px;font-weight:500;color:#617085}.story-answer{font-size:14px;line-height:1.9;color:#1e293b;margin:6px 0 0;white-space:pre-wrap;overflow-wrap:anywhere}.story-evidence{display:grid;gap:9px;margin:12px 0 0;padding:12px 16px;background:#f5f7fa;border-radius:8px}.story-evidence>div{display:flex;gap:14px;align-items:baseline;min-width:0}.story-evidence dt{font-size:11px;color:#617085;flex-shrink:0;max-width:40%;overflow-wrap:anywhere}.story-evidence dd{font-size:12px;line-height:1.85;color:#475569;margin:0;overflow-wrap:anywhere;white-space:pre-wrap}.story-warning{font-size:10px;color:#806b47;background:#f5f2ec;padding:2px 7px;border-radius:5px}.warning .story-marker{background:#f5f2ec;border-color:#d4c9b5;color:#806b47}
.brief-parameters,.brief-records{border-top:1px solid #e8edf4;font-size:12px}.brief-parameters summary,.brief-records summary{padding:14px 0;cursor:pointer;color:#475569;list-style-position:inside}.brief-parameters summary span,.brief-records summary span{font-size:11px;color:#617085;margin-left:10px}.brief-parameters dl{margin:0 0 16px}.brief-parameters dl>div{display:grid;grid-template-columns:130px minmax(0,1fr);gap:12px;padding:10px 0}.brief-parameters dt,.brief-records dt{font-size:11px;color:#617085}.brief-parameters dd,.brief-records dd{margin:0;color:#334155;line-height:1.85;overflow-wrap:anywhere}.brief-parameters .pending dd{color:#617085}.brief-parameters ul{padding-left:16px;margin:6px 0 0}.brief-records ol{padding-left:18px}.brief-records li{padding:8px 0 16px}.brief-records strong{font-weight:550}.brief-records dl>div{display:grid;grid-template-columns:100px minmax(0,1fr);gap:12px;margin-top:8px}.brief-empty{font-size:12px;line-height:1.8;color:#617085;margin:12px 0 24px}summary:focus-visible{outline:2px solid #7188a5;outline-offset:2px}
@media(max-width:600px){.brief-header{align-items:flex-start}.brief-count{display:none}.brief-header h3{font-size:15px}.analysis-live{padding:16px}.analysis-story>li{grid-template-columns:26px minmax(0,1fr);gap:10px}.story-marker{width:25px;height:25px}.analysis-story>li:not(:last-child):before{left:12px;top:26px}.story-evidence{padding:12px}.story-evidence>div{display:block}.story-evidence dt{max-width:none;margin-bottom:3px}.brief-parameters dl>div{grid-template-columns:1fr;gap:4px}.brief-records dl>div{grid-template-columns:1fr;gap:3px}.story-answer{font-size:13px}}
@media(prefers-reduced-motion:reduce){.live-orbit{animation:none}}
.story-phase{color:#425f83;padding-right:9px;margin-right:9px;border-right:1px solid #dce3ee}.phase-evidence{padding:12px 0;border-top:1px solid #edf1f6}.phase-evidence h4{margin:0 0 8px;font-size:12px;color:#425f83;font-weight:550}.phase-evidence p{font-size:12px;line-height:1.8;color:#617085;margin:6px 0}.phase-evidence dl{margin-bottom:0}
</style>
