<template><div v-if="configuredChart?.chartType === 'metric'" class="evidence-kpi"><strong>{{ formatMetric(configuredChart.value,configuredChart.label,dataset) }}</strong><span>{{ configuredChart.label }}</span></div><div v-else-if="configuredChart || (allowAuto && chartData.length)" ref="container" class="evidence-chart" role="img" :aria-label="`${metric}，展示${chartData.length}项查询结果`"></div></template>
<script setup>
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { numericColumns,dimensionColumn,chartLabel,formatMetric,percentageScale } from '../../utils/answerPresentation'
const props = defineProps({ dataset: { type: Object, default: () => ({}) }, renderer: Function, allowAuto: Boolean,metricKey:String,chartType:{type:String,default:'auto'}, selectedIndices:{type:Array,default:()=>[]} })
const emit = defineEmits(['select-row'])
const container = ref(null)
const configuredChart = computed(() => props.dataset.report_spec?.charts?.[0] || null)
const rows = computed(() => configuredChart.value?.rows || props.dataset.rows || [])
const columns = computed(() => configuredChart.value?.columns || props.dataset.columns || Object.keys(rows.value[0] || {}))
const metric = computed(() => props.metricKey || numericColumns({columns:columns.value,rows:rows.value})[0] || '')
const label = computed(() => dimensionColumn({columns:columns.value,rows:rows.value},metric.value))
const isTime = computed(()=>rows.value.length>1 && rows.value.every(row=>/^\d{4}[-/]\d{2}([-/]\d{2})?/.test(String(row[label.value]))))
const line = computed(()=>props.chartType==='line' || (props.chartType==='auto' && isTime.value))
const chartData = computed(() => {
  if(!metric.value || !label.value)return []
  const data=rows.value.map((r,index)=>({rowIndex:index,name:String(r[label.value] ?? '未命名'),value:typeof r[metric.value]==='number' && Number.isFinite(r[metric.value])?r[metric.value]:null}))
  return isTime.value?data.sort((a,b)=>a.name.localeCompare(b.name)):data
})
let chart, observer
const draw = async () => {
  await nextTick()
  if (!container.value || (!configuredChart.value && (!props.allowAuto || !chartData.value.length))) { chart?.dispose(); chart = null; return }
  if (!chart) {
    chart = echarts.init(container.value)
    chart.on('click', event => {
      // Configured charts may transform rows; never guess their source record.
      if (!configuredChart.value && Number.isInteger(event.dataIndex)) {
        const item = chartData.value[event.dataIndex]
        if (item) emit('select-row', item.rowIndex)
      }
    })
    observer?.disconnect()
    observer = new ResizeObserver(() => chart?.resize())
    observer.observe(container.value)
  }
  if (configuredChart.value && props.renderer) {
    props.renderer(chart, { ...configuredChart.value, dataset: props.dataset })
    const option=chart.getOption(),horizontal=option.xAxis?.[0]?.type==='value'
    chart.setOption({series:(option.series || []).map(series=>({label:{...series.label,show:true,position:series.type==='pie'?'outside':series.type==='bar'&&horizontal?'right':'top',formatter:percentageScale(series.name || metric.value,props.dataset)!==null ? (p=>formatMetric(p.value,series.name || metric.value,props.dataset)) : series.label?.formatter || (p=>chartLabel(p.value))},labelLayout:{hideOverlap:true}}))})
    return
  }
  const category={type:'category',data:chartData.value.map(d=>d.name),axisLabel:{width:140,overflow:'truncate',color:'#526177',fontSize:12},axisLine:{show:false},axisTick:{show:false}}
  const value={type:'value',splitLine:{lineStyle:{color:'#edf0f6',type:'dashed'}},axisLabel:{color:'#526177',fontSize:12,formatter:value=>formatMetric(value,metric.value,props.dataset)},name:line.value?metric.value:'',nameTruncate:{maxWidth:160},nameTextStyle:{color:'#526177',fontSize:12}}
  chart.setOption({animation:!window.matchMedia('(prefers-reduced-motion: reduce)').matches,grid:{left:12,right:100,top:36,bottom:36,containLabel:true},tooltip:{trigger:'axis',valueFormatter:value=>formatMetric(value,metric.value,props.dataset),renderMode:'richText',backgroundColor:'#20283d',borderWidth:0,textStyle:{color:'#fff',fontSize:12}},xAxis:line.value?category:value,yAxis:line.value?value:{...category,inverse:true},dataZoom:chartData.value.length>18?[{type:'slider',yAxisIndex:line.value?undefined:0,xAxisIndex:line.value?0:undefined,start:0,end:18/chartData.value.length*100,width:line.value?undefined:12}]:[],series:[{type:line.value?'line':'bar',data:chartData.value.map(d=>({value:d.value,itemStyle:{color:props.selectedIndices.length?(props.selectedIndices.includes(d.rowIndex)?'#425f83':'#dce5ef'):'#425f83'}})),barMaxWidth:22,symbolSize:6,connectNulls:false,lineStyle:{width:2.5},itemStyle:{color:'#425f83',borderRadius:[0,4,4,0]},label:{show:true,position:line.value?'top':'right',fontSize:12,color:'#526177',formatter:p=>(percentageScale(metric.value,props.dataset)!==null ? formatMetric(p.value,metric.value,props.dataset) : chartLabel(p.value))},labelLayout:{hideOverlap:true}}]},true)
}
watch(() => props.dataset, draw, { immediate: true, deep: true })
watch(()=>[props.metricKey,props.chartType,props.allowAuto,props.selectedIndices],draw)
onBeforeUnmount(() => { observer?.disconnect(); chart?.dispose() })
</script>
<style scoped>.evidence-kpi{display:flex;flex-direction:column;padding:22px 0}.evidence-kpi strong{font-size:36px;font-weight:500;color:#26334b}.evidence-kpi span{font-size:12px;color:#526177}.evidence-chart{height:330px;width:100%;min-width:0}</style>
