<template>
  <main class="auth-login-page">
    <header class="auth-brand"><span class="brand-symbol" aria-hidden="true"><i></i><i></i><i></i><i></i></span><span>DataPulse</span><span class="brand-name">脉策智能</span></header>
    <section class="login-workspace" aria-labelledby="login-title">
      <div class="login-intro"><span class="section-index">工作空间 / 登录</span><h1 id="login-title">回到你的<br />数据工作现场。</h1><p>使用工作账号，继续探索与决策。</p></div>
      <form class="login-form" @submit.prevent="submitAdmin">
        <label for="login-account">工作账号</label>
        <input id="login-account" v-model.trim="form.username" type="text" autocomplete="username" placeholder="请输入账号或手机号" required />
        <label for="login-password">密码</label>
        <div class="password-control"><input id="login-password" v-model="form.password" :type="showPassword ? 'text' : 'password'" autocomplete="current-password" placeholder="请输入密码" required /><button class="password-eye" type="button" :aria-label="showPassword ? '隐藏密码' : '显示密码'" :aria-pressed="showPassword" @click="showPassword = !showPassword"><el-icon><component :is="showPassword ? Hide : View" /></el-icon></button></div>
        <button class="primary-login" type="submit" :disabled="adminLoading" :aria-busy="adminLoading"><span>{{ adminLoading ? '正在登录…' : '进入工作空间' }}</span><span aria-hidden="true">→</span></button>
      </form>
      <div class="login-divider"><span>使用组织身份</span></div>
      <button class="feishu-login" type="button" :disabled="feishuLoading" @click="startFeishu"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m4 6 6 3 10-4-5 9-5 4-6-3 6-6" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>{{ feishuLoading ? '正在连接飞书…' : '飞书登录' }}</button>
      <p class="login-tip">还没有账号或无法登录？请联系组织管理员。</p>
    </section>
    <aside class="auth-story" aria-label="产品介绍">
      <div class="story-caption"><span>DATAPULSE</span><span>让业务与数据相遇</span></div>
      <div class="signal-art" aria-hidden="true"><svg viewBox="0 0 640 480" fill="none"><g stroke="currentColor" stroke-width="1"><ellipse cx="320" cy="240" rx="260" ry="100" transform="rotate(-30 320 240)"/><ellipse cx="320" cy="240" rx="260" ry="100" transform="rotate(30 320 240)"/><ellipse cx="320" cy="240" rx="260" ry="100" transform="rotate(90 320 240)"/><circle cx="320" cy="240" r="58"/><circle cx="320" cy="240" r="104" stroke-dasharray="2 8"/></g><circle cx="320" cy="240" r="8" fill="#425f83"/><circle cx="97" cy="369" r="5" fill="#425f83"/><circle cx="543" cy="369" r="5" fill="#425f83"/><circle cx="320" cy="-20" r="5" fill="#425f83"/></svg><span class="art-label label-question">一个业务问题</span><span class="art-label label-answer">连接可验证的答案</span></div>
      <div class="story-copy"><span class="story-rule"></span><h2>每一个好决策，<br />都有数据作答。</h2><p>把分散的数据连成依据，<br />把值得追问的问题留在眼前。</p></div>
      <div class="story-footer"><span>企业智能分析与数据治理</span><span>脉策 · DataPulse</span></div>
    </aside>
    <footer class="auth-footer">DataPulse 工作空间</footer>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Hide, View } from '@element-plus/icons-vue'
import { getFeishuLoginUrl, passwordLogin, setAuthToken } from '../api/index.js'

const emit = defineEmits(['authenticated'])

const form = ref({
  username: '',
  password: ''
})
const adminLoading = ref(false)
const feishuLoading = ref(false)
const showPassword = ref(false)

const submitAdmin = async () => {
  if (adminLoading.value) return
  adminLoading.value = true
  try {
    const data = await passwordLogin(form.value)
    if (data?.success && data?.token) {
      setAuthToken(data.token)
      form.value.password = ''
      ElMessage({
        message: '登录成功',
        type: 'success',
        duration: 1800,
        customClass: 'app-toast-modern',
      })
      emit('authenticated', data.user || null)
    }
  } catch {
    // interceptor already displays backend error
  } finally {
    adminLoading.value = false
  }
}

const startFeishu = async () => {
  if (feishuLoading.value) return
  feishuLoading.value = true
  try {
    const data = await getFeishuLoginUrl()
    if (data?.url) {
      window.location.href = data.url
      return
    }
    ElMessage.warning('飞书登录地址暂未生成，请检查后端飞书配置')
  } catch (error) {
    ElMessage.error(error?.response?.data?.error || '飞书登录入口不可用')
  } finally {
    feishuLoading.value = false
  }
}
</script>

<style scoped>
.auth-login-page{--ink:#142238;--sub:#526176;--accent:#425f83;box-sizing:border-box;min-height:100svh;display:grid;grid-template-columns:minmax(440px, .9fr) minmax(0,1.1fr);grid-template-rows:auto 1fr auto;background:#fff;color:var(--ink);font-family:inherit;padding:0 24px 0 0}
.auth-login-page *{box-sizing:border-box}.auth-brand{grid-column:1;display:flex;align-items:center;gap:12px;padding:38px 0 0 54px;font-size:21px;letter-spacing:-.6px;font-weight:650}.brand-symbol{height:31px;width:31px;background:#182b45;display:flex;align-items:center;justify-content:center;gap:3px;border-radius:9px}.brand-symbol i{height:10px;width:2px;background:#fff;border-radius:3px}.brand-symbol i:nth-child(2){height:19px}.brand-symbol i:nth-child(3){height:14px}.brand-symbol i:nth-child(4){height:7px}.brand-name{font-size:12px;color:var(--sub);border-left:1px solid #dce2eb;padding-left:12px;letter-spacing:1px;font-weight:500}
.login-workspace{width:min(360px,calc(100% - 80px));margin:56px auto;align-self:center}.section-index{font-size:11px;color:var(--sub);letter-spacing:1.5px}.login-intro h1{font-size:38px;line-height:1.35;letter-spacing:-1.5px;font-weight:600;margin:20px 0 12px}.login-intro p{font-size:14px;color:var(--sub);margin:0 0 34px}.login-form{display:flex;flex-direction:column}.login-form label{font-size:13px;font-weight:550;margin:0 0 9px}.login-form input{width:100%;height:48px;padding:0 14px;border:1px solid #d8e0ea;background:#fff;border-radius:8px;color:var(--ink);font:14px inherit;outline:none;transition:border-color 150ms,box-shadow 150ms}.login-form>input{margin-bottom:22px}.login-form input::placeholder{color:#617085}.login-form input:focus{border-color:var(--accent);box-shadow:0 0 0 3px #425f8314}.password-control{position:relative}.password-control input{padding-right:48px}.password-eye{position:absolute;right:7px;top:7px;width:34px;height:34px;display:grid;place-items:center;border:0;background:transparent;color:var(--sub);border-radius:6px;cursor:pointer}.password-eye:hover{background:#edf2f8}.primary-login,.feishu-login{height:48px;border-radius:8px;font:inherit;font-size:14px;font-weight:550;cursor:pointer;transition:background 150ms,transform 150ms}.primary-login{display:flex;align-items:center;justify-content:space-between;padding:0 17px;margin-top:26px;border:0;background:#425f83;color:white}.primary-login:hover:not(:disabled){background:#344c69;transform:translateY(-1px)}.primary-login span:last-child{font-size:21px;font-weight:400}.login-divider{display:flex;gap:16px;align-items:center;font-size:11px;color:var(--sub);margin:26px 0 18px}.login-divider:before,.login-divider:after{content:'';height:1px;background:#e5eaf0;flex:1}.feishu-login{width:100%;border:1px solid #d8e0ea;background:white;color:var(--ink);display:flex;justify-content:center;align-items:center;gap:9px}.feishu-login svg{width:21px;height:21px;color:#425f83}.feishu-login:hover:not(:disabled){background:#f5f7fa}.login-tip{font-size:12px;color:var(--sub);line-height:1.8;margin:22px 0 0}.primary-login:disabled,.feishu-login:disabled{opacity:.6;cursor:wait}.auth-login-page button:focus-visible{outline:3px solid #425f8355;outline-offset:3px}
.auth-story{position:relative;grid-column:2;grid-row:1/4;min-height:700px;margin:24px 0;border-radius:18px;background:#edf2f8;overflow:hidden;display:flex;flex-direction:column;padding:34px 40px}.story-caption,.story-footer{display:flex;justify-content:space-between;gap:16px;color:#526176;font-size:11px}.story-caption>span:first-child{letter-spacing:2px;font:11px ui-monospace,monospace}.signal-art{position:relative;flex:1;min-height:280px;display:grid;place-items:center;margin:0 -40px;color:#a5b6d0}.signal-art svg{width:min(100%,640px);max-height:440px;overflow:visible}.art-label{position:absolute;font-size:11px;letter-spacing:1px;color:#475569;background:#edf2f8;padding:6px 10px}.label-question{top:22%;left:14%}.label-answer{right:10%;bottom:23%}.story-copy{position:relative;padding:12px 0 40px 12px;display:grid;grid-template-columns:1fr auto;gap:18px}.story-rule{grid-column:1/-1;width:32px;height:2px;background:#425f83;margin-bottom:10px}.story-copy h2{font-size:clamp(25px,2.7vw,40px);font-weight:500;letter-spacing:-1px;line-height:1.45;margin:0}.story-copy p{font-size:12px;line-height:2;color:#526176;align-self:end;margin:0 0 5px}.story-footer{padding-top:20px;border-top:1px solid #d4ddea}.auth-footer{grid-column:1;padding:0 54px 30px;color:#617085;font-size:11px}
@media(min-width:1700px){.login-workspace{width:400px}.login-intro h1{font-size:44px}.auth-story{padding:44px 56px}.story-copy{padding-bottom:60px}}
@media(max-width:1050px){.auth-login-page{grid-template-columns:minmax(400px,1fr) minmax(0,.85fr)}.auth-brand{padding-left:32px}.auth-story{padding:28px}.story-copy{display:block;padding-left:0}.story-rule{display:block;margin-bottom:22px}.story-copy p{margin-top:16px}.story-caption span:last-child{display:none}.art-label{display:none}.auth-footer{padding-left:32px}}
@media(max-width:760px){.auth-login-page{display:flex;flex-direction:column;padding:0;min-height:100svh}.auth-brand{padding:28px 28px 0}.login-workspace{margin:50px auto 40px;width:min(360px,calc(100% - 48px));flex:1}.login-intro h1{font-size:34px}.auth-story{display:none}.auth-footer{padding:14px 24px 24px;text-align:center}.login-intro p{margin-bottom:30px}}
@media(prefers-reduced-motion:reduce){.auth-login-page *{transition:none!important}}
</style>
