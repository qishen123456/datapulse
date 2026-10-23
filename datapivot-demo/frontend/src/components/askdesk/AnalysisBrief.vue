<template>
  <section class="analysis-brief" :class="{compact}" aria-label="分析思路与依据">
    <header><div><span class="brief-eyebrow">本次执行</span><h3>{{ compact ? '查询参数与依据' : '从问题到结果，有据可查' }}</h3></div><span class="brief-update"><i :class="{live:busy}"></i>{{ busy?'随执行更新':'执行记录' }}</span></header>
    <div class="brief-facts" aria-label="查询事实摘要">
      <article v-for="(fact,index) in facts" :key="fact.id" class="brief-fact" :class="fact.status" :data-fact="fact.id">
        <div class="fact-label"><span>{{ String(index+1).padStart(2,'0') }}</span><h4>{{ fact.label }}</h4><small v-if="fact.status==='pending'">{{ busy?'待返回':'未记录' }}</small><small v-else-if="fact.status==='warning'">需关注</small></div>
        <p class="fact-value">{{ fact.value }}</p>
        <dl v-if="previewLines(fact).length" class="fact-preview"><div v-for="(line,i) in previewLines(fact).slice(0,2)" :key="i"><dt>{{ line.label }}</dt><dd>{{ line.value }}</dd></div></dl>
        <details v-if="previewLines(fact).length>2" class="fact-detail">
          <summary>查看{{ fact.id==='results'?'字段与规模':fact.id==='sources'?'数据依据':'具体说明' }}<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m6 3 5 5-5 5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/></svg></summary>
          <dl><div v-for="(line,i) in previewLines(fact).slice(2)" :key="i"><dt>{{ line.label }}</dt><dd>{{ line.value }}</dd></div></dl>
        </details>
      </article>
    </div>
    <details v-if="entries.length" class="brief-records">
      <summary><span>执行记录与依据</span><small>{{ entries.length }} 项记录</small><svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m6 3 5 5-5 5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/></svg></summary>
      <ol><li v-for="entry in entries" :key="entry.id"><span class="brief-marker" :class="entry.status"></span><div><strong>{{ entry.heading }}</strong><dl><div v-for="(line,index) in entry.lines" :key="index"><dt>{{ line.label }}</dt><dd>{{ line.value }}</dd></div></dl></div></li></ol>
    </details>
    <div v-if="busy && latest" class="brief-current" role="status"><span aria-hidden="true"></span><p>{{ latest }}</p></div>
  </section>
</template>
<script setup>
import {computed} from 'vue'
import {analysisActivity,analysisFacts,latestAnalysisSummary} from '../../utils/analysisActivity'
const props=defineProps({workflow:{type:Object,default:()=>({})},result:Object,busy:Boolean,compact:Boolean})
const entries=computed(()=>analysisActivity(props.workflow,props.result))
const facts=computed(()=>analysisFacts(props.workflow,props.result))
const latest=computed(()=>latestAnalysisSummary(props.workflow))
const previewLines=fact=>(fact.details || []).filter(line=>line.value!==fact.value)
</script>
<style scoped>
.analysis-brief{--fact-ink:var(--studio-ink,#24292e);--fact-muted:var(--studio-muted,#66716b);--fact-line:var(--studio-line,#e3e6e1);color:var(--fact-ink);padding:22px 0 0;border-top:1px solid var(--fact-line)}
.analysis-brief>header{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:20px}.brief-eyebrow{font-size:10px;letter-spacing:1.2px;color:var(--fact-muted)}.analysis-brief h3{font-size:16px;letter-spacing:-.3px;font-weight:600;margin:7px 0 0;color:var(--fact-ink)}.brief-update{display:flex;align-items:center;gap:6px;font-size:11px;color:var(--fact-muted);white-space:nowrap}.brief-update i{width:5px;height:5px;border-radius:50%;background:#8d9991}.brief-update i.live{background:#386553;box-shadow:0 0 0 3px #edf3ef}
.brief-facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border:1px solid var(--fact-line);border-radius:10px;overflow:hidden;background:#fff}.brief-fact{min-width:0;padding:18px 20px;border-bottom:1px solid var(--fact-line)}.brief-fact:nth-child(odd){border-right:1px solid var(--fact-line)}.brief-fact:nth-last-child(-n+2){border-bottom:0}.fact-label{display:flex;align-items:center;gap:9px}.fact-label>span{font:10px ui-monospace,SFMono-Regular,monospace;color:#7d8881}.fact-label h4{font-size:12px;font-weight:500;color:var(--fact-muted);margin:0}.fact-label small{margin-left:auto;font-size:10px;color:#6d7871;background:#f2f3f0;padding:2px 6px;border-radius:4px}.warning .fact-label small{color:#946025;background:#fbf4e6}.fact-value{margin:11px 0 0;font-size:13px!important;line-height:1.85;color:var(--fact-ink);overflow-wrap:anywhere;white-space:pre-line}.pending .fact-value{color:var(--fact-muted);font-size:12px!important}.fact-detail{margin-top:10px}.fact-detail summary{display:flex;align-items:center;gap:5px;cursor:pointer;list-style:none;font-size:11px;color:#386553}.fact-detail svg,.brief-records svg{width:12px;height:12px;transition:transform .15s}.fact-detail[open] summary svg,.brief-records[open]>summary svg{transform:rotate(90deg)}
.analysis-brief .fact-preview{margin-top:10px}.fact-preview dt{font-size:10px}.analysis-brief dl{display:grid;gap:8px;margin:12px 0 0}.analysis-brief dl>div{font-size:12px;line-height:1.8;min-width:0}.analysis-brief dt{color:var(--fact-muted);font-size:11px}.analysis-brief dd{margin:2px 0 0;color:#48534d;overflow-wrap:anywhere;white-space:pre-line}.brief-records{margin-top:14px}.brief-records>summary{display:flex;align-items:center;gap:10px;list-style:none;cursor:pointer;font-size:12px;color:#66716b;padding:4px 0}.brief-records summary small{font-size:11px;color:#737e77}.analysis-brief ol{list-style:none;padding:18px 0 4px;margin:0;display:grid;gap:22px}.analysis-brief li{display:flex;gap:12px;align-items:flex-start;min-width:0}.brief-marker{width:6px;height:6px;flex-shrink:0;margin-top:9px;border:1px solid #87988b;border-radius:50%;background:#f4f6f3}.brief-marker.completed{background:#386553;border-color:#386553}.brief-marker.warning,.brief-marker.failed{background:#af7d35;border-color:#af7d35}.analysis-brief li>div{min-width:0;flex:1}.analysis-brief strong{font-size:13px;font-weight:500;line-height:1.8;color:var(--fact-ink)}.brief-current{display:flex;gap:9px;align-items:flex-start;margin-top:16px;padding:12px 14px;border-radius:7px;background:#f2f5f1}.brief-current>span{flex-shrink:0;width:5px;height:5px;background:#386553;border-radius:50%;margin-top:8px}.brief-current p{font-size:12px;line-height:1.8;color:#48534d;margin:0;overflow-wrap:anywhere}.analysis-brief summary:focus-visible{outline:2px solid #386553;outline-offset:4px}
.compact{border-top:0;padding-top:0}.compact>header{margin-bottom:16px}.compact h3{font-size:14px}.compact .brief-eyebrow{display:none}.compact .brief-facts{display:block;border:0;border-radius:0}.compact .brief-fact{padding:16px 0;border:0;border-bottom:1px solid var(--fact-line)}.compact .brief-fact:first-child{padding-top:0}.compact .brief-fact:last-child{border-bottom:0}.compact .fact-value{font-size:13px!important}.compact .fact-label>span{color:#7b8880}.compact .brief-records{margin:8px 0 24px;padding-bottom:16px;border-bottom:1px solid var(--fact-line)}
@media(max-width:600px){.brief-facts{grid-template-columns:1fr}.brief-fact:nth-child(odd){border-right:0}.brief-fact:nth-last-child(2){border-bottom:1px solid var(--fact-line)}.brief-fact{padding:16px}.analysis-brief h3{font-size:15px}.analysis-brief>header{gap:10px}.brief-update{font-size:10px}}
</style>
