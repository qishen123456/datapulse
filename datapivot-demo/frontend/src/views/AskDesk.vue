<template>
  <div class="ax-page">
    <div class="ax-shell">
      <section class="ax-workspace" :class="{ 'is-detail-hidden': !detailPanelVisible }">
        <!-- 历史按需打开，不占用分析画布 -->
        <SessionSidebar
          ref="historyPanelRef"
          :busy="isRunning"
          :allow-new-chat="featureAccess.ask_new_chat"
          :sessions="historySessions"
          :active-session-id="activeHistoryId"
          :allow-clear="canUseFeature('app_history_clear')"
          :allow-delete="canUseFeature('app_history_delete')"
          @new-chat="handleNewChat"
          @select-session="handleSelectHistorySession"
          @delete-session="handleDeleteHistorySession"
          @clear-all="handleClearAllSessions"
        />

        <!-- 📌 左侧/中间 对话区-->
        <div class="ax-chat-panel" :class="{ 'is-detail-hidden': !detailPanelVisible }">
          <!-- 头部组件-->
          <div class="ax-content-track ax-header-track">
            <ChatHeader
              :flow="requestedFlow"
              :show-panel="detailPanelVisible"
              :allow-toggle-panel="featureAccess.debug_execution_trace && featureAccess.ask_field_execution_trace"
              :allow-new-chat="featureAccess.ask_new_chat"
              @toggle-panel="togglePanel"
              @new-chat="handleNewChat"
              @show-history="focusSidebarHistory"
            />
          </div>

          <!-- 只读视图提示：正在查看历史，后台有任务执行中/待确认/已完成/失败 -->
          <div v-if="isViewingReadonly && runningTaskStatus !== 'idle'" class="ax-readonly-banner" :class="`banner-${runningTaskStatus}`" @click="handleReturnToRunning">
            <span v-if="runningTaskStatus === 'running'" class="ax-readonly-banner-icon ax-spin-ring-small">
              <span class="ax-spin-ring-track-small"></span>
              <span class="ax-spin-ring-bar-small"></span>
            </span>
            <span v-else-if="runningTaskStatus === 'pending_confirmation'" class="ax-readonly-banner-icon">⚠️</span>
            <span v-else-if="runningTaskStatus === 'completed'" class="ax-readonly-banner-icon">✅</span>
            <span v-else class="ax-readonly-banner-icon">❌</span>
            <span class="ax-readonly-banner-text">
              <template v-if="runningTaskStatus === 'running'">正在查看历史任务，后台有任务正在执行中，点击此处跳回执行中的任务</template>
              <template v-else-if="runningTaskStatus === 'pending_confirmation'">后台任务需要确认口径，点击此处返回确认</template>
              <template v-else-if="runningTaskStatus === 'completed'">后台任务已执行完成，点击此处查看结果</template><template v-else-if="runningTaskStatus === 'partial'">后台任务仅形成部分结果，点击此处查看待完成项</template>
              <template v-else>后台任务执行失败，点击此处查看详情</template>
            </span>
            <!-- i18n: datapulse.task.readonlyBanner -->
          </div>

          <!-- 会话滚动区-->
          <div class="ax-chat-body" ref="chatBodyRef">
            <div class="ax-content-track ax-chat-content">
            <!-- 欢迎首屏 -->
            <WelcomeScreen
              v-if="messages.length === 0"
              :flow="requestedFlow"
              :welcome-text="requestedFlow === 'advanced' ? '从一个业务疑问开始，先制定计划，再用证据逐步验证。' : '把业务问题交给我，获取口径清晰、可以核对的答案。'"
              :common-questions="commonQuestions"
              :common-questions-loading="commonQuestionsLoading"
              :allow-quick-ask="featureAccess.ask_quick_ask"
              :allow-refresh-questions="featureAccess.ask_quick_refresh"
              @quick-ask="quickAsk"
              @refresh-questions="refreshCommonQuestions"
            />

            <!-- 消息列表 -->
            <div class="ax-msg-list">
              <div v-for="msg in displayMessages" :key="msg.id" class="ax-msg-wrap">
                <!-- 用户气泡 -->
                <UserBubble
                  v-if="msg.role === 'user'"
                  :content="msg.content"
                  :disabled="isRunning"
                  :allow-copy="featureAccess.ask_question_copy"
                  :allow-edit="featureAccess.ask_question_edit"
                  :allow-rerun="featureAccess.ask_question_rerun"
                  @copy="copyQuestion(msg)"
                  @edit="editQuestion(msg)"
                  @rerun="rerunQuestion(msg)"
                />

                <!-- AI 回复 -->
                <div v-else class="ax-ai-wrap">
                  <div class="ax-ai-meta">
                    <div class="ax-ai-avatar" aria-label="脉策经营分析助手头像">
                      <svg class="ax-ai-avatar-svg" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
                        <defs>
                          <linearGradient id="aiRingChat" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#526b7a" />
                            <stop offset="100%" stop-color="#3c536e" />
                          </linearGradient>
                          <linearGradient id="aiDiscChat" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stop-color="#FFFFFF" />
                            <stop offset="100%" stop-color="#edf2f5" />
                          </linearGradient>
                        </defs>
                        <circle cx="50" cy="50" r="48" fill="url(#aiDiscChat)" />
                        <circle cx="50" cy="50" r="46" fill="none" stroke="url(#aiRingChat)" stroke-width="3.5" />
                        <path d="M28 62 L42 40 L52 52 L62 36 L72 44" fill="none" stroke="#526b7a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" />
                        <circle cx="72" cy="44" r="4.5" fill="#526b7a" />
                      </svg>
                    </div>
                    <span class="ax-ai-name">DataPulse AI 经营分析顾问</span>
                  </div>
                  <div class="ax-ai-cards">
                    <!-- 加载中-->
                    <div v-if="msg.loading && !displayLogs.length" class="ax-thinking-loading">
                      <div class="ax-dots">
                        <span></span><span></span><span></span>
                      </div>
                      <span class="ax-thinking-text">正在分析问题意图并规划路径...</span>
                    </div>

                    <!-- 结构化解析条（响应层聚合，后端开关+角色门控；确认卡/纠正卡消息不出条）。置顶：先看到"系统怎么理解"，再看执行过程。运行中显示实时条（理解完成即推），终态以 result.parse_bar 为准 -->
                    <ParseBar
                      v-if="parseBarFor(msg)"
                      :bar="parseBarFor(msg)"
                      :dataset-id="getParseBarDatasetId(msg)"
                      :editable="!isRunning && !isViewingReadonly"
                      @ask="handleParseBarAsk(msg, $event)"
                    />

                    <AskProcessView
                      v-if="workflowFor(msg)?.run_id"
                      :workflow="workflowFor(msg)"
                      :result="msg.data"
                      :status="msg.loading ? 'running' : msg.data?.aborted ? 'canceled' : msg.data?.error ? 'error' : 'completed'"
                      :readonly="isViewingReadonly"
                      :allow-inspector="featureAccess.debug_execution_trace && featureAccess.ask_field_execution_trace"
                      :allow-retry="featureAccess.ask_quick_ask && featureAccess.ask_send_question && !isViewingReadonly && !isRunning"
                      @inspect="openActivityInspector(msg,$event)"
                      @retry="draftAnswerFollowUp(msg.data?.question || '')"
                      :busy="Boolean(msg.loading || confirmationSubmitting[msg.id])"
                      :allow-technical="featureAccess.debug_execution_trace && featureAccess.ask_field_generated_sql"
                      :render-chart="renderChartSpec"
                      :allow-auto-chart="featureAccess.ask_chart_auto_infer"
                      :allow-download="featureAccess.ask_report_download"
                      @download-report="downloadResearchReport(msg)"
                      @start-plan="doConfirm({ label: '确认研究计划', plan_branch_ids: $event }, msg)"
                    />
                    <PlanCard v-else :route="msg.data?.route" />

                    <!-- 错字短路纠正卡（第 0 层快检命中：只出此卡，不进流水线） -->
                    <div v-if="msg.data?.early_clarify" class="ax-early-clarify">
                      <div class="ax-early-clarify-head">
                        <span class="ax-clarify-icon">?</span>
                        <span class="ax-early-clarify-title">
                          {{ msg.data.clarify_suggestion?.reason || '这个问题里可能有错字' }}
                        </span>
                      </div>
                      <div class="ax-early-clarify-body">
                        <span class="ax-early-clarify-label">你是不是想问：</span>
                        <button
                          v-for="(cand, ci) in (msg.data.clarify_suggestion?.candidates || [])"
                          :key="ci"
                          class="ax-clarify-chip ax-early-clarify-chip"
                          :disabled="isRunning"
                          @click.stop.prevent="applyClarifySuggestion(cand)"
                        >{{ cand }}</button>
                      </div>
                      <button
                        class="ax-early-clarify-continue"
                        :disabled="isRunning"
                        @click.stop.prevent="resendOriginalQuestion(msg)"
                      >没问题，按原问题继续查</button>
                      <div class="ax-clarify-freeform">
                        <input
                          v-model="clarifyDrafts[msg.id]"
                          class="ax-clarify-input"
                          :disabled="isRunning"
                          placeholder="都不是？输入你想问的"
                          @keydown.enter.exact.prevent="handleClarifyDraftEnter($event, msg)"
                          @click.stop
                        />
                        <button
                          class="ax-clarify-send"
                          :disabled="isRunning || !String(clarifyDrafts[msg.id] || '').trim()"
                          @click.stop.prevent="submitClarifyDraft(msg)"
                        >发送</button>
                      </div>
                    </div>

                    <!-- 纠正条（守门员预览，后端按角色门控，默认仅超管可见） -->
                    <div v-if="msg.data?.clarify_suggestion && !msg.data?.early_clarify" class="ax-clarify-strip">
                      <span class="ax-clarify-icon">?</span>
                      <span class="ax-clarify-text">
                        已按「{{ msg.data.clarify_suggestion.interpretation }}」理解
                        <span v-if="msg.data.clarify_suggestion.reason" class="ax-clarify-reason">
                          {{ msg.data.clarify_suggestion.reason }}
                        </span>
                      </span>
                      <span class="ax-clarify-chips">
                        <button
                          v-for="(cand, ci) in msg.data.clarify_suggestion.candidates"
                          :key="ci"
                          class="ax-clarify-chip"
                          :disabled="isRunning"
                          @click.stop.prevent="applyClarifySuggestion(cand)"
                        >{{ cand }}</button>
                      </span>
                      <span class="ax-clarify-freeform ax-clarify-freeform-inline">
                        <input
                          v-model="clarifyDrafts[msg.id]"
                          class="ax-clarify-input"
                          :disabled="isRunning"
                          placeholder="都不是？输入你想问的"
                          @keydown.enter.exact.prevent="handleClarifyDraftEnter($event, msg)"
                          @click.stop
                        />
                        <button
                          class="ax-clarify-send"
                          :disabled="isRunning || !String(clarifyDrafts[msg.id] || '').trim()"
                          @click.stop.prevent="submitClarifyDraft(msg)"
                        >发送</button>
                      </span>
                    </div>

                    <!-- 思考过程卡（可折叠）-->
                    <ThinkingCard
                      v-if="shouldShowThinkingCard(msg)"
                      :steps="getThinkingSteps(msg)"
                      :loading="msg.loading"
                      :is-open="thinkingOpen[msg.id]"
                      @toggle="toggleThinking(msg.id)"
                    />

                    <!-- 确认口径卡-->
                    <div v-if="!msg.data?.workflow && shouldShowResultHandoff(msg)" class="ax-flow-handoff">
                      <div class="ax-flow-handoff-top">
                        <div class="ax-flow-handoff-kicker">执行已完成</div>
                        <span v-if="getAskFlowLabel(msg)" class="ax-flow-badge" :class="getAskFlowClass(msg)">
                          {{ getAskFlowLabel(msg) }}
                        </span>
                      </div>
                      <div class="ax-flow-handoff-title">正在整理结果摘要与报告内容</div>
                      <div class="ax-flow-handoff-desc">
                        执行轨迹已经沉淀完成，下面将继续承接结果摘要、报告内容和附件产物。                      </div>
                    </div>

                    <div v-if="shouldShowConfirmationCard(msg)" class="ax-card ax-confirm-card">
                      <div class="ax-confirm-header">
                        <span class="ax-confirm-badge">需要确认</span>
                        <span class="ax-confirm-q">{{ msg.data.confirmation_question }}</span>
                      </div>
                      <div class="ax-confirm-opts">
                        <div class="ax-confirm-list">
                          <button
                            v-for="(opt, idx) in visibleConfirmationOptions(msg)"
                            :key="getConfirmOptionKey(opt)"
                            class="ax-confirm-row"
                            :class="{ 'ax-confirm-row-top': idx === 0 }"
                            :disabled="isRunning || confirmationSubmitting[msg.id]"
                            @click.stop.prevent="doConfirm(opt, msg)"
                          >
                            <span class="ax-confirm-rank">{{ idx + 1 }}</span>
                            <span class="ax-confirm-info">
                              <span class="ax-confirm-row-label">
                                {{ getConfirmOptionLabel(opt) }}
                                <span v-if="opt.recommended" class="ax-confirm-recommended">推荐</span>
                              </span>
                              <span v-if="getConfirmOptionDescription(opt)" class="ax-confirm-row-desc">
                                {{ getConfirmOptionDescription(opt) }}
                              </span>
                            </span>
                            <span class="ax-confirm-spacer"></span>
                            <span v-if="shouldShowConfirmOptionScore(msg, opt)" class="ax-confirm-score">
                              {{ getConfirmOptionScore(opt) }}分
                            </span>
                          </button>
                        </div>
                        <button
                          v-if="(msg.data.confirmation_options || []).length > 4"
                          class="ax-confirm-toggle"
                          :disabled="isRunning || confirmationSubmitting[msg.id]"
                          @click.stop.prevent="toggleConfirmOptions(msg.id)"
                        >
                          {{ confirmExpanded[msg.id] ? '收起' : `展开更多 (${msg.data.confirmation_options.length - 4})` }}
                        </button>
                      </div>
                      <div class="ax-confirm-freeform">
                        <textarea
                          v-model="confirmationDrafts[msg.id]"
                          class="ax-confirm-textarea"
                          :disabled="isRunning || confirmationSubmitting[msg.id]"
                          placeholder="都不合适？补充说明继续分析，例如：按华东区域战区口径。"
                          @keydown.enter.exact.prevent="handleConfirmationDraftEnter($event, msg)"
                          @click.stop
                        ></textarea>
                        <button
                          class="ax-confirm-send"
                          :disabled="isRunning || confirmationSubmitting[msg.id] || !String(confirmationDrafts[msg.id] || '').trim()"
                          @click.stop.prevent="submitConfirmationDraft(msg)"
                        >
                          发送补充说明
                        </button>
                      </div>
                    </div>

                    <div v-else-if="shouldShowConfirmationSubmitted(msg)" class="ax-card ax-confirm-submitted">
                      <div class="ax-confirm-submitted-head">
                        <span class="ax-confirm-submitted-dot"></span>
                        <span class="ax-confirm-submitted-title">已提交确认，正在继续执行</span>
                      </div>
                      <div class="ax-confirm-submitted-desc">
                        系统已收到老板确认口径，正在继续生成 SQL 与后续分析结果。                      </div>
                    </div>

                    <div
                      v-if="!msg.data?.research && shouldShowResultChain(msg)"
                      class="ax-result-chain"
                      :ref="el => setResultChainRef(msg.id, el)"
                    >
                    <ResultDigestCard
                      v-if="!(msg.data?.research || msg.data?.research_plan) && (getReport(msg) || getPrimaryDataset(msg))"
                      :title="getResultTitle(msg)"
                      :display-title="msg.data?.display_title || ''"
                      :question="msg.data?.question || session.state.question"
                      :report="getReport(msg)"
                      :dataset="getPrimaryDataset(msg)"
                      :datasets="getDatasets(msg)"
                      :route="msg.data?.route || null"
                      :flow-label="getAskFlowLabel(msg)"
                      :flow-class="getAskFlowClass(msg)"
                      :flow-hint="getAskFlowHint(msg)"
                      :show-details-button="featureAccess.ask_report_details"
                      :allow-download="featureAccess.ask_report_download"
                      :allow-technical="featureAccess.debug_execution_trace && featureAccess.ask_field_generated_sql"
                      :allow-auto-chart="featureAccess.ask_chart_auto_infer"
                      :render-chart="renderChartSpec"
                      :allow-follow-up="featureAccess.ask_quick_ask && featureAccess.ask_send_question && !isRunning && !isViewingReadonly"
                      @follow-up="draftAnswerFollowUp"
                      @view-details="openDetailPanel(msg)"
                      @view-report="openMessageReport(msg.data)"
                    />

                    <div
                      v-else-if="shouldShowResultChain(msg)"
                      class="ax-result-empty"
                    >
                      <div class="ax-result-empty-icon">📭</div>
                      <div class="ax-result-empty-title">未查询到可用数据</div>
                      <div class="ax-result-empty-desc">
                        执行链路已完成，但当前结果中没有可展示的数据。可能原因：当前账号权限范围未覆盖该对象、问题条件未命中任何记录，或数据集配置已变更。可尝试切换账号、调整问题范围，或联系管理员检查数据权限。
                      </div>
                    </div>

                    <!-- 状态提示卡-->
                    </div>
                    <div v-if="msg.data?.aborted" class="ax-card ax-cancel-card">
                      <span class="ax-cancel-icon" aria-hidden="true">
                        <span class="ax-cancel-icon-core"></span>
                      </span>
                      <div class="ax-cancel-copy">
                        <div class="ax-cancel-kicker">FLOW INTERRUPTED</div>
                        <div class="ax-cancel-title">本轮问数已取消</div>
                        <div class="ax-cancel-desc">已请求停止。正在执行的操作将在返回或超时后退出，后续步骤不再启动。</div>
                      </div>
                    </div>
                    <div v-if="msg.data?.error" class="ax-card ax-error-card" role="alert">
                      <span>❌</span>
                      <span>{{ msg.data.error }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            </div>
          </div>

          <!-- 底部输入区-->
          <div class="ax-content-track ax-composer-track">
            <QuestionQueue :items="questionQueue" :paused="queuePaused" :reason="queueReason" :busy="isRunning" :disabled="isViewingReadonly || !featureAccess.ask_send_question" @resume="resumeQuestionQueue" @pause="pauseQuestionQueue('已手动暂停，当前问题继续执行')" @remove="removeQueuedQuestion" @edit="editQueuedQuestion" @move-up="questionQueue=moveQuestionUp(questionQueue,$event)" @clear="clearQuestionQueue" />
            <div v-if="queueDraftFlow" class="queue-draft-context">正在编辑队列问题 · {{ queueDraftFlow==='advanced'?'高阶研究':'普通问数' }}<button @click="queueDraftFlow=''">改用当前模式</button></div>
            <ComposerArea
              :queue-mode="isRunning || questionQueue.length>0 || session.state.status==='waiting_confirmation'"
              :flow="queueDraftFlow || requestedFlow"
              :class="{ 'ax-composer-narrow': !detailPanelVisible }"
              v-model:query="query"
              v-model:dataset-id="datasetId"
              v-model:model-id="modelId"
              :datasets="datasets"
              :ai-models="aiModels"
              :is-running="isRunning"
              :disabled="isViewingReadonly"
              :allow-send="featureAccess.ask_send_question"
              :allow-stop="featureAccess.ask_stop_run"
              :allow-dataset-select="featureAccess.ask_dataset_select"
              :allow-model-select="featureAccess.ask_model_select"
              :status-text="isRunning || session.state.status === 'completed' ? statusBarText : ''"
              :status-elapsed="isRunning ? `${elapsed}s` : ''"
              :status-tone="taskOutcome(session.state.result,{status:session.state.status,busy:isRunning,workflow:session.state.workflow}).status"
              :status-flow-label="activeAskFlowLabel"
              :status-flow-class="activeAskFlowClass"
              :status-flow-hint="activeAskFlowLabel ? activeAskFlowHint : ''"
              @send="handleSend"
              @stop="handleStop"
              @dataset-change="handleDatasetChange"
            />
          </div>
        </div>

        <!-- ██ 右侧 决策推导透视面板（全新设计） -->
        <transition name="ax-panel-slide">
          <div v-if="detailPanelVisible" class="ax-detail-panel-container">
            <ReasoningPanel
              :logs="inspectionBusy || inspectionResult === session.state.result ? displayLogs : []"
              :status="inspectionBusy ? 'running' : ''"
              :workflow="inspectionWorkflow"
              :result="inspectionResult"
              :busy="inspectionBusy"
              :allow-technical="featureAccess.ask_field_generated_sql"
              :allow-retry="featureAccess.ask_quick_ask && featureAccess.ask_send_question && !isViewingReadonly && !isRunning"
              :focus-phase="inspectorFocusPhase"
              :allow-report="featureAccess.ask_report_details"
              @view-report="openMessageReport(inspectionResult)"
              @retry="draftAnswerFollowUp(inspectionResult?.question || session.state.question)"
              @close="togglePanel"
            >
              <template #content="{ log, index }">
                <div v-if="log.sql && featureAccess.ask_field_generated_sql" class="ax-log-section">
                  <div class="ax-log-section-title">{{ log.sqlTitle || '生成 SQL' }}</div>
                  <SqlBlock :sql="log.sql" :allow-copy="featureAccess.ask_sql_copy" />
                </div>

                <div v-if="log.chartData" class="ax-log-section">
                  <div class="ax-log-section-title">{{ log.chartTitle || '图表预览' }}</div>
                  <button v-if="featureAccess.chart_viewer" class="ax-ghost-btn ax-log-inline-action" @click="openChartViewer(log.chartData, log.chartTitle || '图表预览')">放大查看</button>
                  <div class="ax-chart-embed" :ref="el => initLogChart(el, log.chartData, index)"></div>
                </div>

                <div v-if="log.tableRows?.length" class="ax-log-section">
                  <div class="ax-log-section-title">{{ log.tableTitle || '结果预览' }}</div>
                  <div class="ax-mini-table-wrap">
                    <el-table :data="log.tableRows.slice(0, 5)" size="small" border class="ax-mini-table">
                      <el-table-column v-for="c in log.tableColumns" :key="c" :prop="c" :label="c" min-width="100" show-overflow-tooltip />
                    </el-table>
                    <div v-if="log.tableRows.length > 5" class="ax-table-more">共 {{ log.tableRows.length }} 行</div>
                  </div>
                </div>

              </template>
            </ReasoningPanel>

            </div>
          </transition>
      </section>
    </div>

    <el-dialog
      v-model="reportViewerVisible"
      title=""
      :fullscreen="reportDialogFullscreen"
      :width="reportDialogFullscreen ? undefined : 'min(1280px, 94vw)'"
      top="4vh"
      class="ax-report-dialog"
      destroy-on-close
    >
      <div class="ax-report-dialog-body">
        <div class="ax-report-dialog-head">
              <div class="ax-report-dialog-title-block">
            <h3 class="ax-report-dialog-title">数据分析报告</h3>
            <p v-if="reportViewerTitle" class="ax-report-dialog-subtitle">{{ reportViewerTitle }}</p>
          </div>
          <div class="ax-report-dialog-actions">
            <button class="ax-secondary-btn" @click="reportDialogFullscreen = !reportDialogFullscreen">
              <span class="ax-btn-label">{{ reportDialogFullscreen ? '退出全屏' : '全屏查看' }}</span>
            </button>
            <button class="ax-secondary-btn" @click="reportViewerVisible = false">
              <span class="ax-btn-label">关闭</span>
            </button>
          </div>
        </div>
        <iframe class="html-report-reader" title="完整 HTML 分析报告" sandbox="" :srcdoc="reportViewerResearch ? buildResearchReportHtml(reportViewerResearch,{allowAutoChart:featureAccess.ask_chart_auto_infer}) : answerHtml(reportViewerTitle,reportViewerDatasets,reportViewerReport)"></iframe>
      </div>
    </el-dialog>

    <el-dialog
      v-model="chartViewerVisible"
      :title="chartViewerTitle"
      width="min(980px, 92vw)"
      top="8vh"
      class="ax-chart-dialog"
      destroy-on-close
    >
      <div class="ax-chart-dialog-body">
        <div v-if="chartViewerHasTable" class="ax-chart-dialog-head">
          <div class="ax-chart-dialog-kicker">DETAIL VIEW</div>
          <div class="ax-chart-dialog-switch">
            <button
              type="button"
              class="ax-chart-switch-btn"
              :class="{ 'is-active': chartViewerMode === 'chart' }"
              @click="chartViewerMode = 'chart'"
            >
              图表
            </button>
            <button
              type="button"
              class="ax-chart-switch-btn"
              :class="{ 'is-active': chartViewerMode === 'table' }"
              @click="chartViewerMode = 'table'"
            >
              数据表
            </button>
          </div>
        </div>
        <div v-if="chartViewerMode === 'chart' && chartViewerSpec?.chartType === 'metric'" class="ax-insight-metric ax-insight-metric-large">
          <div class="ax-insight-metric-value">{{ chartViewerSpec.value }}</div>
          <div class="ax-insight-metric-label">{{ chartViewerSpec.label }}</div>
        </div>
        <div v-else-if="chartViewerMode === 'chart'" ref="chartDialogRef" class="ax-chart-dialog-canvas"></div>
        <div v-else class="ax-chart-dialog-table">
          <div class="ax-chart-dialog-table-meta">
            <span>{{ chartViewerTableColumns.length }} 列</span>
            <span>{{ chartViewerTableRows.length }} 行</span>
          </div>
          <el-table :data="chartViewerTableRows" size="small" border height="68vh" style="width: 100%">
            <el-table-column
              v-for="column in chartViewerTableColumns"
              :key="column"
              :prop="column"
              :label="column"
              min-width="140"
              show-overflow-tooltip
            />
          </el-table>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, nextTick, onActivated, onDeactivated, onMounted, onUnmounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { marked } from 'marked'
import { buildResearchReportHtml } from '../utils/researchReport'
import * as echarts from 'echarts'
import { getBookshelfDatasets, getCommonQuestions, getActiveAIModels, recordParseBarFeedback, getAskCapabilities } from '../api/index'
import { useDataPulseSession } from '../state/askDeskSession'
import { getSessionCache, setSessionCache } from '../state/sessionCache'
import { useFeatureFlags } from '../state/featureFlags'

import SessionSidebar from '../components/askdesk/SessionSidebar.vue'
import ChatHeader from '../components/askdesk/ChatHeader.vue'
import WelcomeScreen from '../components/askdesk/ExploreWelcome.vue'
import UserBubble from '../components/askdesk/UserBubble.vue'
import PlanCard from '../components/askdesk/PlanCard.vue'
import ParseBar from '../components/askdesk/ParseBar.vue'
import ThinkingCard from '../components/askdesk/ThinkingCard.vue'
import {taskOutcome} from '../state/askWorkflow'
import QuestionQueue from '../components/askdesk/QuestionQueue.vue'
import {queuedQuestion,appendQuestion,moveQuestionUp,queuePauseReason} from '../state/questionQueue'
import AskProcessView from '../components/askdesk/AskProcessView.vue'
import ResultDigestCard from '../components/askdesk/AnswerCanvas.vue'
import ComposerArea from '../components/askdesk/ComposerArea.vue'
import {answerHtml,formatMetric,percentageScale} from '../utils/answerPresentation'
import ReasoningPanel from '../components/askdesk/ReasoningPanel.vue'
import SqlBlock from '../components/askdesk/SqlBlock.vue'

defineOptions({ name: 'DataPulse' })
import { useDataPulseHistory } from '../state/askDeskHistory'
import { useDataPulseTaskView } from '../state/askDeskTaskView'
import { useDataPulseReportHistory } from '../composables/useAskDeskReportHistory'
import { buildOrgTree, getDefaultConfig as getDefaultReportTreeConfig } from '../composables/useOrgTree'

const session = useDataPulseSession()
const { isFeatureEnabled, loadFeatureFlags } = useFeatureFlags()
const smartFeatureKeys = [
  'debug_execution_trace',
  'ask_field_execution_trace',
  'ask_field_generated_sql',
  'ask_field_dataset_hit',
  'ask_field_error_detail',
  'ask_field_confidence',
  'ask_field_token_usage',
  'ask_new_chat',
  'ask_quick_ask',
  'ask_quick_refresh',
  'ask_question_copy',
  'ask_question_edit',
  'ask_question_rerun',
  'ask_confirm_scope',
  'ask_submit_note',
  'chart_viewer',
  'ask_report_details',
  'ask_send_question',
  'ask_stop_run',
  'ask_dataset_select',
  'ask_model_select',
  'ask_sql_copy',
  'report_fullscreen',
  'ask_report_download',
  'ask_chart_auto_infer',
]
const featureAccess = computed(() => smartFeatureKeys.reduce((map, key) => {
  map[key] = isFeatureEnabled(key)
  return map
}, {}))
const canUseFeature = (key) => Boolean(featureAccess.value[key])
const {
  historySessions,
  activeHistoryId,
  pendingRestoreId,
  loadHistory,
  upsertHistory,
  removeHistory,
  clearHistory,
  findHistoryById,
  clearRestoreRequest,
  setActiveHistory,
  takePendingRestoreOptions,
} = useDataPulseHistory()
const {
  runningSessionId,
  viewingTaskId,
  isViewingReadonly,
  readonlySnapshot,
  runningTaskStatus,
  completedTaskId,
  pendingTaskId,
  setRunningSessionId,
  clearRunningSessionId,
  markRunningTaskPending,
  markRunningTaskCompleted,
  markRunningTaskFailed,
  switchViewToRunning,
  switchViewToDefault,
} = useDataPulseTaskView()
const askCapabilities = ref({ advancedAvailable: false })
const requestedFlow = ref('basic')
let capabilityRequest = 0
const refreshAskCapabilities = async () => {
  const seq = ++capabilityRequest
  try {
    const response = await getAskCapabilities(datasetId.value)
    if (seq !== capabilityRequest) return
    askCapabilities.value = response.data || {}
    showAskFlowBadge.value = false
    requestedFlow.value = askCapabilities.value.defaultFlow || 'basic'
  } catch { askCapabilities.value = { advancedAvailable: false } }
}
const downloadResearchReport = async msg => {
  if (!canUseFeature('ask_report_download')) return
  try {
    const { data } = await getAskCapabilities()
    if (!data?.reportDownloadAvailable || data.authorizationScope !== msg.data?.authorization_scope) {
      ElMessage.warning('当前权限已变化，请重新查询后再下载研究报告。')
      return
    }
    const url = URL.createObjectURL(new Blob([buildResearchReportHtml(msg.data, { allowAutoChart: featureAccess.value.ask_chart_auto_infer })], { type:'text/html;charset=utf-8' }))
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = `DataPulse研究报告-${new Date().toISOString().slice(0,10)}.html`
    anchor.click()
    setTimeout(() => URL.revokeObjectURL(url),1000)
  } catch { ElMessage.error('未能验证当前下载权限，请稍后再试。') }
}
const workflowFor = msg => msg.loading || (isCurrentSessionMessage(msg) && session.state.status === 'running') ? session.state.workflow : msg.data?.workflow
const query = ref('')
const datasetId = ref(null)
const modelId = ref(null)
const datasets = ref([])
const aiModels = ref([])
// 数据集就绪信号：登录后 getBookshelfDatasets 为异步，历史恢复的权限过滤必须等它就绪，
// 否则 datasets.value 仍为空会被 isDatasetVisible 全部误判为无权限（首次点历史误报）。
const datasetsLoaded = ref(false)
let datasetsLoadedResolve = null
const ensureDatasetsReady = () => {
  if (datasetsLoaded.value) return Promise.resolve()
  return new Promise((resolve) => {
    datasetsLoadedResolve = resolve
    // 兜底超时放行：后端 GET 已做权限过滤，前端仅为二次校验，超时不再阻塞恢复。
    setTimeout(() => {
      if (datasetsLoadedResolve) { datasetsLoadedResolve(); datasetsLoadedResolve = null }
    }, 2500)
  })
}
const markDatasetsLoaded = () => {
  datasetsLoaded.value = true
  if (datasetsLoadedResolve) { datasetsLoadedResolve(); datasetsLoadedResolve = null }
}
const commonQuestions = ref([])
const commonQuestionsLoading = ref(false)
const messages = reactive([])
const confirmationDrafts = reactive({})
const clarifyDrafts = reactive({})
const confirmationSubmitting = reactive({})
const confirmExpanded = reactive({})

// keep-alive 切回 / 刷新都会调：先看是否有残留 stale，再清掉 session.result + 全部 UI 卡片状态
// hasActiveAsk 守卫：本页正在执行的问数不清（误杀会导致 result 帧被忽略、显示已取消）
const clearStaleSessionState = () => {
  const hasStaleRecovered = session.state.result || session.state.question || session.state.logs?.length
  if (!hasStaleRecovered || session.hasActiveAsk?.()) return
  session.clearRecoveredSessionResult()
  clearChatUiState()
}
const showPanel = ref(false)
const chatBodyRef = ref(null)
const panelRef = ref(null)
const sideReportRef = ref(null)
const sideReportHeadRef = ref(null)
const chartDialogRef = ref(null)
const resultChainRefs = new Map()
const thinkingOpen = reactive({})
const logOpen = reactive({})
const timelineVersion = ref(0)
const reportViewerVisible = ref(false)
const reportViewerResearch = ref(null)
const reportViewerTitle = ref('')
const reportViewerReport = ref('')
const reportViewerDatasets = ref([])
const reportDialogFullscreen = ref(false)
const chartViewerVisible = ref(false)
const chartViewerTitle = ref('图表预览')
const chartViewerSpec = ref(null)
const chartViewerMode = ref('chart')
const detailReportResult = ref(null)
const officeDrillOpen = reactive({})
const messageDerivedCache = new WeakMap()
const datasetChartSpecCache = new WeakMap()
const chartElementCache = new WeakMap()
let activePrintFrame = null
let msgCounter = 0
let elapsed = ref(0)
let timerInst = null
let chatScrollTimer = null
let panelScrollTimer = null
let reportTopScrollTimers = []
const activeRequestAiMessageId = ref(null)
const pendingQuickDataset = ref(null)
const isDatasetManuallySelected = ref(false)

const isRunning = computed(() => session.state.status === 'running')

const displayMessages = computed(() => {
  if (isViewingReadonly.value && readonlySnapshot.value?.messages) {
    return readonlySnapshot.value.messages
  }
  return messages
})

const displayLogs = computed(() => {
  if (isViewingReadonly.value && readonlySnapshot.value?.logs) {
    return readonlySnapshot.value.logs
  }
  return session.state.logs
})

// 解析条编辑（重设计）：点候选 = 本地暂存（可连改多个槽位），确认后把修正问句
// 作为一条新提问发进当前会话（新用户气泡 + 新 AI 回复），替代旧的"点选即就地重跑"
const getParseBarDatasetId = (msg) => {
  const dsr = msg?.data?.dataset_results
  const first = Array.isArray(dsr) && dsr.length ? dsr[0] : null
  const id = first?.dataset_id ?? msg?.data?.route?.dataset_ids?.[0]
  const n = Number(id)
  return Number.isFinite(n) && n > 0 ? n : null
}

// 按 span offset 倒序替换，把暂存修改编译成新问句（dataset 槽无 span，走显式锚定）
const compileParseBarQuestion = (question, overrides) => {
  const repls = (overrides || [])
    .filter(o => (o.slot === 'node' || o.slot === 'metric') && Number.isInteger(o.start) && Number.isInteger(o.end))
    .map(o => ({ start: o.start, end: o.end, text: String(o.new_label || o.new_value || '') }))
    .filter(r => r.text)
    .sort((a, b) => b.start - a.start)
  let q = String(question || '')
  for (const r of repls) q = q.slice(0, r.start) + r.text + q.slice(r.end)
  return q.trim()
}

// 运行中实时解析条（理解阶段完成即出条）：终态优先用 result.parse_bar；
// 实时条只挂在当前正在执行的那条 AI 消息上（loading 结束即收回，确认卡不残留）
const liveParseBar = computed(() => session.state.liveParseBar)
const parseBarFor = (msg) => msg.data?.parse_bar
  || (msg.loading && msg.id === activeRequestAiMessageId.value ? liveParseBar.value : null)

const handleParseBarAsk = async (msg, payload) => {
  const bar = msg?.data?.parse_bar
  const overrides = Array.isArray(payload?.overrides) ? payload.overrides : []
  if (!bar || !overrides.length) return
  if (isRunning.value) {
    ElMessage.info('正在查询中，请稍后再试')
    return
  }
  const list = displayMessages.value || []
  const idx = list.findIndex(m => m.id === msg.id)
  const userMsg = idx > 0 ? list[idx - 1] : null
  const question = String(userMsg && userMsg.role === 'user' ? userMsg.content : '').trim()
  if (!question) return
  const compiled = compileParseBarQuestion(question, overrides)
  const dsOverride = overrides.find(o => o.slot === 'dataset')
  const dsId = Number(dsOverride?.dataset_id ?? payload?.dataset_id)
  const pinnedDatasetId = Number.isFinite(dsId) && dsId > 0 ? dsId : null
  // 仅改数据集（问句无字面变化）时沿用原问句 + 显式锚定新数据集
  const finalQuestion = compiled && compiled !== question ? compiled : question
  if (finalQuestion === question && !pinnedDatasetId) {
    ElMessage.info('未改动解析内容')
    return
  }
  // 修正学习落库 fail-open：不等待、不阻塞提问链路
  recordParseBarFeedback({
    question,
    parse_bar: bar,
    overrides,
    dataset_id: pinnedDatasetId,
    session_id: session.state.conversationSessionId || ''
  }).catch(() => {})
  // 复用主发送链路（同 applyClarifySuggestion 范式）；改数据集时显式锚定，
  // 绕过 datasetInput 的自动释放启发式（用户已明确指定口径）
  query.value = finalQuestion
  await handleSend(pinnedDatasetId ? { datasetId: pinnedDatasetId } : undefined)
}

const displayResult = computed(() => {
  if (isViewingReadonly.value && readonlySnapshot.value?.result) {
    return readonlySnapshot.value.result
  }
  return session.state.result
})

const timelineKey = computed(() => `${session.state.conversationSessionId || 'fresh'}-${timelineVersion.value}`)
const detailPanelVisible = computed(() => showPanel.value && canUseFeature('debug_execution_trace') && canUseFeature('ask_field_execution_trace'))
const canViewCharts = computed(() => canUseFeature('chart_viewer'))
const canViewFullscreenReport = computed(() => canUseFeature('report_fullscreen'))

const statusBarText = computed(() => {
  if(session.state.status==='idle')return ''
  return taskOutcome(session.state.result,{status:session.state.status,busy:isRunning.value,workflow:session.state.workflow}).label
})

const activeReportResult = computed(() => {
  if (isViewingReadonly.value && displayResult.value) {
    return displayResult.value
  }
  return detailReportResult.value || session.state.result || null
})
const inspectorFocusPhase=ref(-1)
const inspectionBusy=computed(()=>isRunning.value && !isViewingReadonly.value)
const inspectionResult=computed(()=>inspectionBusy.value?null:activeReportResult.value)
const inspectionWorkflow=computed(()=>inspectionBusy.value?session.state.workflow:inspectionResult.value?.workflow || {})
const openActivityInspector=async(msg,phase=0)=>{
  if(!canUseFeature('debug_execution_trace') || !canUseFeature('ask_field_execution_trace'))return
  detailReportResult.value=msg?.loading?null:msg?.data || null
  inspectorFocusPhase.value=-1
  showPanel.value=true
  await nextTick()
  inspectorFocusPhase.value=phase
  resizeRenderedCharts()
}
const latestSessionError = computed(() => {
  const msg = activeRequestAiMessage.value || currentSessionAiMessage.value
  return String(msg?.data?.error || session.state.result?.error || '').trim()
})
const showAskFlowBadge = ref(false)

const activeAskFlowMeta = computed(() => {
  if (!showAskFlowBadge.value) return null
  const meta = activeReportResult.value?.ask_flow || activeReportResult.value?.diagnostics?.ask_flow || null
  return meta && typeof meta === 'object' ? meta : null
})

const activeAskFlowLabel = computed(() => {
  const flow = String(activeAskFlowMeta.value?.flow || '').toLowerCase()
  if (flow === 'advanced') return '进阶流程'
  if (flow === 'basic') return '基础流程'
  return ''
})

const activeAskFlowClass = computed(() => String(activeAskFlowMeta.value?.flow || '').toLowerCase() === 'advanced' ? 'is-advanced' : 'is-basic')

const activeAskFlowHint = computed(() => {
  const reason = String(activeAskFlowMeta.value?.reason || '')
  const map = {
    basic_selected: '当前问数由基础流程执行',
    advanced_selected: '当前问数由进阶流程执行',
    advanced_disabled: '进阶未启用，已回落基础流程',
    advanced_role_denied: '当前角色未进入进阶灰度',
    advanced_error_fallback: '进阶异常，已回退基础流程',
  }
  return map[reason] || '当前问数流程'
})

const latestDatasets = computed(() => (
  Array.isArray(activeReportResult.value?.dataset_results) ? activeReportResult.value.dataset_results : []
))

const mergeDatasetReports = (datasetResults) => (
  (datasetResults || [])
    .map((dataset, index) => {
      const analysis = String(dataset?.analysis || '').trim()
      if (!analysis) return ''
      const datasetName = dataset?.dataset_name || `数据集 ${dataset?.dataset_id || index + 1}`
      return datasetResults.length > 1 ? `## ${datasetName}\n\n${analysis}` : analysis
    })
    .filter(Boolean)
    .join('\n\n---\n\n')
)

const parseMetricNumber = (value) => {
  if (value === null || value === undefined || value === '') return null
  if (typeof value === 'number') return Number.isFinite(value) ? value : null
  const text = String(value || '').trim()
  const numeric = Number(text.replace(/[^0-9.-]/g, ''))
  if (!Number.isFinite(numeric)) return null
  if (text.includes('亿')) return numeric * 100000000
  if (text.includes('万')) return numeric * 10000
  return numeric
}

const findDatasetKpiNumber = (dataset, matcher) => {
  const kpis = Array.isArray(dataset?.report_spec?.kpis) ? dataset.report_spec.kpis : []
  const item = kpis.find(kpi => matcher.test(`${kpi?.key || ''}${kpi?.label || ''}`))
  if (!item) return null
  return parseMetricNumber(item.value ?? item.displayValue)
}

const findDatasetRowNumber = (dataset, matcher) => {
  const rows = Array.isArray(dataset?.rows) ? dataset.rows : []
  const row = rows.find(item => item && typeof item === 'object') || {}
  const key = Object.keys(row).find(name => matcher.test(name))
  return key ? parseMetricNumber(row[key]) : null
}

const inferSubjectLevel = (name) => {
  const text = String(name || '')
  if (text.includes('事业群')) return '事业群'
  if (text.includes('战区')) return '战区'
  if (text.includes('行业部')) return '行业部'
  if (text.includes('片区')) return '片区'
  return '对象'
}

const buildDatasetComparisonRow = (dataset) => {
  const subjectName = dataset?.comparison_subject_name || dataset?.dataset_name || `数据集 ${dataset?.dataset_id || ''}`.trim()
  const overview = dataset?.cross_dataset_subject_overview || {}
  const task = parseMetricNumber(overview?.task)
    ?? findDatasetKpiNumber(dataset, /总任务|任务金额|目标|task/i)
    ?? findDatasetRowNumber(dataset, /总任务|任务金额|目标/i)
  const actual = parseMetricNumber(overview?.actual)
    ?? findDatasetKpiNumber(dataset, /年度开单|开单金额|开单|完成|实际|actual/i)
    ?? findDatasetRowNumber(dataset, /年度开单|开单金额|开单|完成|实际/i)
  const rate = parseMetricNumber(overview?.rate)
    ?? findDatasetKpiNumber(dataset, /达成率|完成率|rate|percent/i)
    ?? findDatasetRowNumber(dataset, /达成率|完成率/i)
    ?? (task ? (Number(actual || 0) / task) * 100 : null)
  const remain = parseMetricNumber(overview?.remain)
    ?? findDatasetKpiNumber(dataset, /剩余|缺口|差额|remain|gap/i)
    ?? findDatasetRowNumber(dataset, /剩余|缺口|差额/i)
    ?? (task !== null && actual !== null ? task - actual : null)
  return {
    节点名称: subjectName,
    层级: overview?.level || dataset?.comparison_subject_level || inferSubjectLevel(subjectName),
    总任务金额: task,
    年度开单金额: actual,
    达成率: rate,
    剩余任务金额: remain,
  }
}

const collectResolvedNamesFromDatasets = (datasetResults) => {
  const names = []
  const add = (value) => {
    const text = String(value || '').trim()
    if (text && !names.includes(text)) names.push(text)
  }
  ;(datasetResults || []).forEach((dataset) => {
    const resolved = dataset?.resolved_entities || {}
    ;(resolved.all_members || []).forEach(add)
    ;(resolved.entities || []).forEach((entity) => {
      ;(entity?.members || []).forEach(add)
    })
  })
  return names
}

const datasetRowsContainAnyName = (dataset, names = []) => {
  if (!names.length) return false
  return (dataset?.rows || []).some((row) => {
    const text = Object.values(row || {}).map(value => String(value ?? '')).join(' ')
    return names.some(name => text.includes(name))
  })
}

const buildAggregateDataset = (datasetResults) => {
  if (!Array.isArray(datasetResults) || datasetResults.length === 0) return null
  if (datasetResults.length === 1) return datasetResults[0]

  const resolvedNames = collectResolvedNamesFromDatasets(datasetResults)
  if (resolvedNames.length === 1) {
    const matching = datasetResults.filter(dataset => datasetRowsContainAnyName(dataset, resolvedNames))
    if (matching.length === 1) return matching[0]
  }

  const totalRows = datasetResults.reduce((sum, item) => sum + Number(item?.row_count || item?.rows?.length || 0), 0)
  const allColumns = Array.from(new Set(datasetResults.flatMap(item => item?.columns || [])))
  const comparisonRows = datasetResults.map(buildDatasetComparisonRow).filter(item => item.节点名称)

  return {
    dataset_name: `共 ${datasetResults.length} 个数据集`,
    dataset_id: 'multi',
    row_count: totalRows,
    rows: comparisonRows,
    columns: Array.from(new Set([...allColumns, '节点名称', '层级', '总任务金额', '年度开单金额', '达成率', '剩余任务金额'])),
  }
}

const latestDataset = computed(() => buildAggregateDataset(latestDatasets.value))

const latestReport = computed(() => mergeDatasetReports(latestDatasets.value))

const isDatasetVisible = (id) => {
  const value = Number(id)
  if (!Number.isFinite(value)) return false
  return datasets.value.some(item => Number(item?.id) === value)
}

const sanitizeDatasetSelection = () => {
  if (datasetId.value && !isDatasetVisible(datasetId.value)) {
    datasetId.value = null
    isDatasetManuallySelected.value = false
  }
  if (session.state.selectedDatasetId && !isDatasetVisible(session.state.selectedDatasetId)) {
    session.state.selectedDatasetId = null
  }
  if (pendingQuickDataset.value?.datasetId && !isDatasetVisible(pendingQuickDataset.value.datasetId)) {
    pendingQuickDataset.value = null
  }
}

const datasetResults = computed(() => latestDatasets.value)
const hasSideReport = computed(() => {
  if (activeReportResult.value?.research) return false
  if (latestSessionError.value) return false
  return resultPreviews.value.length > 0 || !!latestReport.value
})
const sideReportHeading = computed(() => '业绩分析报告')

const reportSceneTemplate = computed(() => {
  const sourceDatasets = reportViewerVisible.value ? reportViewerDatasets.value : latestDatasets.value
  const specTemplate = sourceDatasets.find(item => item?.report_spec?.layoutTemplate)?.report_spec?.layoutTemplate
  if (specTemplate) return specTemplate
  const answerMode = String(sourceDatasets.find(item => item?.report_spec?.answerMode)?.report_spec?.answerMode || '').trim()
  if (answerMode === 'comparison') return 'comparison'
  if (answerMode === 'ranking') return 'ranking'
  if (answerMode === 'drilldown' || answerMode === 'filter') return 'detail'
  const questionText = String(activeReportResult.value?.question || session.state.question || query.value || '')
  if (/对比|比较|哪个|谁更|差异|和.+比|跟.+比|与.+比|\bvs\b/i.test(questionText)) return 'comparison'
  if (/排名|排行|前\s*(?:\d+|[一二两三四五六七八九十]+)|Top\s*\d+|TOP\s*\d+|最好|最差|最高|最低/.test(questionText)) return 'ranking'
  return 'detail'
})

const reportSceneTemplateLabel = computed(() => ({
  comparison: '对比模板',
  ranking: '排名模板',
  detail: '详情模板',
}[reportSceneTemplate.value] || '详情模板'))

const normalizeConfidenceScore = (value, fallback = 0) => {
  const numeric = Number(value)
  if (!Number.isFinite(numeric)) return fallback
  return Math.max(0, Math.min(100, Math.round(numeric)))
}

const buildRouteConfidenceMeta = (route = {}) => {
  const candidateCount = Array.isArray(route?.candidate_dataset_ids)
    ? route.candidate_dataset_ids.length
    : Array.isArray(route?.dataset_ids)
      ? route.dataset_ids.length
      : 0

  let score = normalizeConfidenceScore(route?.match_score, candidateCount <= 1 ? 78 : 64)
  if (candidateCount > 1) score -= Math.min(12, (candidateCount - 1) * 6)
  if (route?.requires_confirmation) score = Math.min(score, 60)
  if (route?.preferred_dataset_override) score = Math.max(score, 72)

  return {
    score,
    tone: score >= 82 ? 'success' : score >= 65 ? 'info' : 'warning',
    label: score >= 82 ? '路由把握' : score >= 65 ? '路由可用' : '路由待确认',
    value: `${score}`,
    candidateCount,
  }
}

const buildResultConfidenceMeta = (route = {}, datasets = []) => {
  const reviews = (datasets || []).map(item => item?.agent3_review).filter(Boolean)
  const approvedCount = reviews.filter(item => item?.approved !== false).length
  const riskCount = reviews.reduce((sum, item) => sum + (Array.isArray(item?.risks) ? item.risks.length : 0), 0)
  const datasetTotal = (datasets || []).length
  const rowsReady = (datasets || []).filter(item => Array.isArray(item?.rows) && item.rows.length > 0).length
  const analysesReady = (datasets || []).filter(item => String(item?.analysis || '').trim()).length

  let score = 55
  if (datasetTotal > 0) score += 8
  if (rowsReady === datasetTotal && datasetTotal > 0) score += 16
  else if (rowsReady > 0) score += 8
  if (reviews.length === datasetTotal && approvedCount === datasetTotal && datasetTotal > 0) score += 12
  else if (approvedCount > 0) score += 6
  if (analysesReady === datasetTotal && datasetTotal > 0) score += 8
  score -= Math.min(18, riskCount * 4)
  if (buildRouteConfidenceMeta(route).candidateCount > 1) score -= 5
  score = normalizeConfidenceScore(score, 60)

  return {
    score,
    tone: score >= 80 ? 'success' : score >= 62 ? 'info' : 'warning',
    label: score >= 80 ? '结果稳定' : score >= 62 ? '结果可用' : '结果谨慎',
    value: riskCount > 0 ? `${score} / ${riskCount} 风险` : `${score}`,
  }
}

const sideConfidenceBadges = computed(() => {
  if (activeReportResult.value?.workflow) return []
  const advanced = activeReportResult.value?.diagnostics?.advanced || {}
  const evidenceVote = advanced?.evidence_vote || {}
  const templatePolicy = advanced?.template_policy || {}
  const routeGuard = advanced?.route_guard || {}
  const backendConfidence = activeReportResult.value?.confidence || {}
  const routeMeta = backendConfidence?.route
    ? {
        score: Number(backendConfidence.route.score || 0),
        tone: backendConfidence.route.level === 'high' ? 'success' : backendConfidence.route.level === 'medium' ? 'info' : 'warning',
        label: '路由把握',
        value: `${backendConfidence.route.label || ''} ${backendConfidence.route.score || 0}`.trim(),
      }
    : buildRouteConfidenceMeta(activeReportResult.value?.route || {})
  const resultMeta = backendConfidence?.result
    ? {
        score: Number(backendConfidence.result.score || 0),
        tone: backendConfidence.result.level === 'high' ? 'success' : backendConfidence.result.level === 'medium' ? 'info' : 'warning',
        label: '结果可信',
        value: `${backendConfidence.result.label || ''} ${backendConfidence.result.score || 0}`.trim(),
      }
    : buildResultConfidenceMeta(activeReportResult.value?.route || {}, latestDatasets.value)
  const advancedVoteMeta = evidenceVote?.decision
    ? {
        score: Number(evidenceVote.confidence_score || 0),
        tone: evidenceVote.decision === 'accept' ? 'success' : evidenceVote.decision === 'accept_with_caution' ? 'info' : 'warning',
        label: '进阶择优',
        value: `${({
          accept: '可采信',
          accept_with_caution: '谨慎采信',
          review_required: '需复核',
        }[evidenceVote.decision] || evidenceVote.decision)} ${evidenceVote.confidence_score || 0}`.trim(),
      }
    : null
  const templateMeta = templatePolicy?.expected_top_n
    ? {
        score: Number(templatePolicy.expected_top_n || 0),
        tone: Number(templatePolicy.warning_count || 0) > 0 ? 'warning' : 'success',
        label: '模板策略',
        value: `Top${templatePolicy.expected_top_n}`,
      }
    : null
  const routeGuardLabel = {
    auto_lock: '自动锁定',
    cross_dataset_compare: '跨集对比',
    manual_respected: '手动优先',
    manual_mismatch: '手动错配',
    needs_confirmation: '待确认',
    no_candidate: '无候选',
    observe: '观察',
  }[routeGuard.action] || routeGuard.action
  const guardMeta = routeGuard?.action
    ? {
        score: Number(routeGuard.confidence || 0),
        tone: routeGuard.action === 'auto_lock' || routeGuard.action === 'manual_respected' ? 'success' : 'warning',
        label: '路由守门',
        value: routeGuardLabel,
      }
    : null
  return [routeMeta, resultMeta, advancedVoteMeta, templateMeta, guardMeta].filter(item => item?.score > 0)
})

const routeDecisionDetail = computed(() => {
  const result = activeReportResult.value || {}
  const advanced = result?.diagnostics?.advanced || {}
  const route = result.route || {}
  const summary = String(result.confidence?.route?.summary || '').trim()
  const reason = String(result.confidence?.route?.reason || route.arbiter_reason || '').trim()
  const reasonLabel = {
    profile_scope_resolved: '组织画像命中',
    explicit_dataset_alias: '同义词命中',
    organization_tree_name_resolved: '组织树命中',
    top_candidate_score_clear: '候选分数领先',
    high_confidence: '高置信语义匹配',
    low_similarity_requires_boss_confirm: '相似命中待确认',
  }[reason] || ''
  const ids = Array.isArray(route.dataset_ids) ? route.dataset_ids : []
  const names = ids.map(id => datasetNameMap.value.get(Number(id)) || `数据集 ${id}`).filter(Boolean)
  const routeGuard = advanced?.route_guard || {}
  const evidenceVote = advanced?.evidence_vote || {}
  const advancedLines = [
    routeGuard?.reason ? `进阶守门：${routeGuard.reason}` : '',
    evidenceVote?.recommended_action ? `采信建议：${evidenceVote.recommended_action}` : '',
  ].filter(Boolean)
  if (!summary && !reasonLabel && !names.length && !advancedLines.length) return ''
  return [
    names.length ? `自动路由：${names.join('、')}` : '',
    reasonLabel ? `依据：${reasonLabel}` : '',
    summary,
    ...advancedLines,
  ].filter(Boolean).join('；')
})

const detailPanelState = computed(() => {
  const m = {
    idle: '待命',
    running: '执行中',
    completed: '已完成',
    canceled: '已取消',
    error: '异常',
    waiting_confirmation: '待确认',
  }
  return m[session.state.status] || '待命'
})

const detailPanelDesc = computed(() => {
  if (session.state.status === 'running') {
    return session.latestLog?.value?.summary || session.latestLog?.value?.title || session.state.logs.slice(-1)[0]?.detail || '正在持续更新本轮问数任务的执行进度。'
  }
  if (session.state.status === 'completed') {
    return '本轮问数已经完成，可以继续查看执行细节、结果数据和完整报告。'
  }
  if (session.state.status === 'canceled') {
    return '你已手动取消本轮问数，执行链路已停止。'
  }
  if (session.state.status === 'waiting_confirmation') {
    return '当前任务等待确认统计口径，确认后会继续后续执行步骤。'
  }
  if (session.state.status === 'error') {
    return session.state.error || '当前任务执行异常，请查看节点详情后重新发起问数。'
  }
  return '发起问题后，这里会持续展示本轮任务的完整执行轨迹。'
})

const amountColumnPattern = /金额|开单|任务|销售|收入|成本|利润|缺口|剩余|回款|费用|价格|单价|amount|sales|revenue|cost|profit|remain/i
const rateColumnPattern = /率|percent|rate/i

const formatAmount = (value, metric = {}) => {
  const numeric = typeof value === 'number'
    ? value
    : Number(String(value ?? '').replace(/[^0-9.-]/g, ''))
  if (!Number.isFinite(numeric)) return '-'

  const unit = String(metric.unit || '').trim()
  const scale = Number(metric.scale) || 1
  const display = numeric / scale
  const absDisplay = Math.abs(display)

  const fmt = (num, digits = 2) => {
    if (Number.isInteger(num)) return String(num)
    return Number(num).toFixed(digits).replace(/\.?0+$/, '')
  }

  if (unit === '万元') {
    if (absDisplay < 10000) return `${fmt(display)}万`
    return `${fmt(display / 10000)}亿`
  }

  // 默认按 "元" 口径展示
  if (absDisplay < 10000) return fmt(display)
  if (absDisplay < 1000000) return `${(display / 10000).toFixed(1).replace(/\.?0+$/, '')}万`
  if (absDisplay < 100000000) return `${Math.round(display / 10000)}万`
  return `${(display / 100000000).toFixed(2).replace(/\.?0+$/, '')}亿`
}

const resolveAmountMetric = (metric = {}, dataset = null, column = '') => {
  const nextMetric = { ...(metric || {}) }
  if (String(nextMetric.unit || '').trim()) return nextMetric

  const reportSpec = dataset?.report_spec || {}
  const reportUnit = String(reportSpec.amountUnit || '').trim()
  const metricColumn = String(nextMetric.column || column || '').trim()

  if (reportUnit && isAmountColumn(metricColumn || nextMetric.label || nextMetric.key || '')) {
    nextMetric.unit = reportUnit
    nextMetric.scale = Number(nextMetric.scale) || 1
    return nextMetric
  }

  return nextMetric
}

const formatChartAmount = (value, dataset = null, column = '') => (
  formatAmount(value, resolveAmountMetric({ format: 'amount', column }, dataset, column))
)

const isAmountColumn = (column = '') => amountColumnPattern.test(String(column || ''))
const isRateColumn = (column = '') => rateColumnPattern.test(String(column || ''))

const formatDisplayValue = (value) => {
  if (typeof value === 'number') {
    if (Number.isInteger(value)) return value.toLocaleString()
    return value.toLocaleString('zh-CN', { maximumFractionDigits: 2 })
  }
  return String(value ?? '-')
}

const formatValueByColumn = (value, column = '', dataset = null) => {
  if (percentageScale(column,dataset || {}) !== null) return formatMetric(value,column,dataset || {})
  if (isAmountColumn(column)) {
    const metric = resolveAmountMetric({}, dataset, column)
    const col = String(column || '')
    if (/_万元$/.test(col) || /万元$/.test(col)) {
      metric.unit = '万元'
      metric.scale = 1
    }
    return formatAmount(value, metric)
  }
  return formatDisplayValue(value)
}

const formatBusinessValueByColumn = (value, column = '', dataset = null) => {
  const rawText = String(value ?? '').trim()
  if (rawText && /[万亿%]/.test(rawText)) return rawText
  return formatValueByColumn(value, column, dataset)
}

const getLabelColumn = (dataset) => {
  const columns = dataset?.columns || []
  const firstRow = dataset?.rows?.[0] || {}
  return (
    columns.find(col => /组织路径|归属组织|组织归属|管理链路|路径/i.test(col)) ||
    columns.find(col => /日期|时间|城市|战区|片区|行业部|名称|水平|类型|标识/i.test(col)) ||
    columns.find(col => typeof firstRow[col] === 'string') ||
    columns[0]
  )
}

const getNumericColumns = (dataset) => {
  const columns = dataset?.columns || []
  const firstRow = dataset?.rows?.[0] || {}
  return columns.filter(col => typeof firstRow[col] === 'number')
}

const getMetricCards = (dataset) => {
  const rows = dataset?.rows || []
  if (!rows.length) return []

  const businessCards = getBusinessMetricCards(dataset)
  if (businessCards.length) return businessCards

  const firstRow = rows[0]
  const numericColumns = getNumericColumns(dataset)
  const cards = []

  numericColumns.slice(0, 3).forEach((column) => {
    const values = rows.map(row => row[column]).filter(value => typeof value === 'number')
    if (!values.length) return
    const displayValue = rows.length === 1 ? firstRow[column] : Math.max(...values)
    cards.push({ label: rows.length === 1 ? column : `最高${column}`, value: formatValueByColumn(displayValue, column, dataset) })
  })

  if (rows.length === 1 && cards.length === 0) {
    const labelColumn = getLabelColumn(dataset)
    if (labelColumn) cards.push({ label: labelColumn, value: formatDisplayValue(firstRow[labelColumn]) })
  }

  if (rows.length > 1) cards.push({ label: '数据行数', value: formatDisplayValue(rows.length) })
  return cards.slice(0, 3)
}

const toNumber = (value) => {
  if (typeof value === 'number') return Number.isFinite(value) ? value : null
  const cleaned = String(value ?? '').replace(/[^0-9.-]/g, '')
  if (!cleaned) return null
  const numeric = Number(cleaned)
  return Number.isFinite(numeric) ? numeric : null
}

const pickColumn = (dataset, names) => {
  const columns = dataset?.columns || []
  return names.find(name => columns.includes(name)) || ''
}

const getDatasetReportConfig = (dataset) => (
  dataset?.report_config
  || activeReportResult.value?.report_configs?.[String(dataset?.dataset_id)]
  || activeReportResult.value?.report_config
  || getDefaultReportTreeConfig()
)

const getDatasetTreeModel = (dataset) => {
  const rows = Array.isArray(dataset?.rows) ? dataset.rows : []
  if (!rows.length) return null
  return buildOrgTree(rows, getDatasetReportConfig(dataset))
}

const sumBusinessColumn = (rows, column) => {
  if (!column) return null
  const values = rows.map(row => toNumber(row?.[column])).filter(value => value !== null)
  if (!values.length) return null
  return values.reduce((sum, value) => sum + value, 0)
}

const calcBusinessRate = (rows, taskCol, actualCol, rateCol) => {
  const task = sumBusinessColumn(rows, taskCol)
  const actual = sumBusinessColumn(rows, actualCol)
  if (task && actual !== null && task > 0) return Number((actual / task * 100).toFixed(2))
  const rates = rows.map(row => toNumber(row?.[rateCol])).filter(value => value !== null)
  if (!rates.length) return null
  return Number((rates.reduce((sum, value) => sum + value, 0) / rates.length).toFixed(2))
}

const formatBusinessAmount = (value) => {
  if (value === null || value === undefined) return '-'
  return formatAmount(value)
}

const formatMetricByDefinition = (value, metric = {}, dataset = null) => {
  if (value === null || value === undefined) return '-'
  if (metric.format === 'percent') return `${Number(value).toLocaleString('zh-CN', { maximumFractionDigits: 2 })}%`
  if (metric.format === 'amount' || metric.format === 'currency') return formatAmount(value, resolveAmountMetric(metric, dataset))
  return formatDisplayValue(value)
}

const getMetricDefinition = (config, key, matcher) => {
  const metrics = config?.metrics || []
  return metrics.find(item => item.key === key)
    || metrics.find(item => matcher?.(item))
    || null
}

const getNodeMetricValue = (node, metric) => {
  if (!node || !metric) return null
  const direct = toNumber(node.metrics?.[metric.key])
  if (direct !== null) return direct
  return toNumber(node.raw?.[metric.column])
}

const getRateTone = (rate, benchmark = 15, risk = 10) => {
  const value = toNumber(rate)
  if (value === null) return 'neutral'
  if (value >= benchmark) return 'good'
  if (value >= risk) return 'warn'
  return 'danger'
}

const getToneLabel = (tone) => ({ good: '区域标杆', warn: '中等达成', danger: '低达成风险' }[tone] || '待观察')

const getRateTag = (rate, benchmark = 15, risk = 10, goodLabel = '标杆') => {
  const tone = getRateTone(rate, benchmark, risk)
  if (tone === 'good') return `✅ ${goodLabel}`
  if (tone === 'warn') return '🟡 中等'
  if (tone === 'danger') return '⚠️ 风险'
  return '未分级'
}

const getOfficeThresholds = (config = {}) => {
  const risk = toNumber(config?.officeRiskThreshold ?? config?.riskThreshold) ?? 10
  const configuredBenchmark = toNumber(config?.officeBenchmarkThreshold ?? config?.benchmarkThreshold)
  return {
    risk,
    benchmark: configuredBenchmark ?? 15,
  }
}

const getOfficeRateTone = (rate, config = {}) => {
  const { benchmark, risk } = getOfficeThresholds(config)
  return getRateTone(rate, benchmark, risk)
}

const getOfficeToneLabel = (tone) => ({ good: '区域标杆', warn: '需推进', danger: '低达成风险' }[tone] || '待观察')

const getOfficeRateTag = (rate, config = {}, goodLabel = '区域标杆') => {
  const tone = getOfficeRateTone(rate, config)
  if (tone === 'good') return `✅ ${goodLabel}`
  if (tone === 'warn') return '🟠 需推进'
  if (tone === 'danger') return '⚠️ 风险'
  return '未分级'
}

const getToneFromDisplayTag = (label = '', fallback = 'neutral') => {
  const text = String(label || '')
  if (/风险|重点风险/.test(text)) return 'danger'
  if (/承压|第三梯队/.test(text)) return 'danger'
  if (/推进|第二梯队|稳定|中位/.test(text)) return 'warn'
  if (/标杆|领先|第一梯队/.test(text)) return 'good'
  return fallback
}

const requestedLevelTokens = ['城市战区', '城市站', '事业群', '行业部', '战区', '片区', '客户经理', '业务员', '部门', '线']

const canonicalRequestedLevel = (value) => {
  const text = String(value || '').trim()
  if (text === '城市战区') return '城市站'
  return text
}

const getQuestionText = () => String(session.state.question || query.value || '').trim()

const getRequestedLevelValues = (questionText = getQuestionText(), config = {}) => {
  const values = []
  const configuredValues = (config?.levels || [])
    .flatMap(level => level?.values || [])
    .map(value => String(value || '').trim())
    .filter(Boolean)
  ;[...configuredValues, ...requestedLevelTokens].forEach((value) => {
    const canonical = canonicalRequestedLevel(value)
    if (value && questionText.includes(value) && !values.includes(canonical)) values.push(canonical)
  })
  return values
}

const isNegativeRankingQuestion = (questionText = getQuestionText()) => (
  /完成.*不好|不好|差|最差|最低|落后|承压|风险|低于|倒数|垫底|未完成|缺口/.test(questionText || '')
)

const isRateRankingQuestion = (questionText = getQuestionText()) => (
  /达成率|完成率|完成|进度|不好|最低|最差|排名|排行|承压|风险/.test(questionText || '')
)

const isAmountRankingQuestion = (questionText = getQuestionText()) => (
  /排名|排行|Top\s*\d+|TOP\s*\d+|前\s*(?:\d+|[一二两三四五六七八九十]+)|最高|最低|最好|最差/.test(questionText || '')
  && /年度开单|开单金额|开单|实际|销售/.test(questionText || '')
)

const getQuestionRankingMetricLabel = (questionText = getQuestionText()) => {
  const text = String(questionText || '')
  if (!/排名|排行|Top\s*\d+|TOP\s*\d+|前\s*(?:\d+|[一二两三四五六七八九十]+)|最高|最低|最好|最差/.test(text)) return ''
  if (/年度开单|开单金额|开单|实际|销售/.test(text)) return '年度开单金额'
  if (/总任务|任务金额|目标/.test(text)) return '总任务金额'
  if (/剩余|缺口|差额|待完成/.test(text)) return '剩余任务金额'
  if (/达成率|完成率|进度|完成/.test(text)) return '达成率'
  return ''
}

const getRankingPolicy = (config = {}) => (
  config?.intentPolicies?.ranking && typeof config.intentPolicies.ranking === 'object'
    ? config.intentPolicies.ranking
    : {}
)

const getConfiguredTopN = (report = null) => {
  const config = report?.dataset ? getDatasetReportConfig(report.dataset) : getDefaultReportTreeConfig()
  const intentTopN = toNumber(report?.dataset?.report_spec?.debug?.query_intent?.top_n)
  const policy = getRankingPolicy(config)
  const defaultTopN = toNumber(policy.defaultTopN) ?? 3
  const maxTopN = toNumber(policy.maxTopN) ?? 20
  if (report?.answerMode === 'ranking' && intentTopN === null) {
    return Math.max(1, Array.isArray(report?.offices) && report.offices.length ? report.offices.length : defaultTopN)
  }
  const value = intentTopN ?? defaultTopN
  return Math.max(1, Math.min(maxTopN, value))
}

const sortNodesForQuestion = (nodes = [], rateMetric = null) => {
  const lowFirst = isNegativeRankingQuestion()
  return [...nodes].sort((left, right) => {
    const leftValue = getNodeMetricValue(left, rateMetric) || 0
    const rightValue = getNodeMetricValue(right, rateMetric) || 0
    return lowFirst ? leftValue - rightValue : rightValue - leftValue
  })
}

const normalizeOfficeCompareSpec = (chartSpec = {}, config = {}) => {
  if (!chartSpec || typeof chartSpec !== 'object') return chartSpec
  const rows = Array.isArray(chartSpec.rows) ? chartSpec.rows : []
  const columns = Array.isArray(chartSpec.columns) && chartSpec.columns.length
    ? [...chartSpec.columns]
    : Object.keys(rows[0] || {})
  const rateColumn = findColumn(columns, column => isRateColumn(column)) || '达成率'
  const nextColumns = columns.includes('标签') ? columns : [...columns, '标签']
  return {
    ...chartSpec,
    columns: nextColumns,
    sortColumn: chartSpec.sortColumn || '',
    rows: rows.map(row => ({
      ...row,
      标签: row?.标签 || getOfficeRateTag(row?.[rateColumn], config),
    })),
  }
}

const subjectAccentPalette = [
  { accent: '#1A1A1A', soft: 'rgba(26, 26, 26, 0.06)', border: 'rgba(26, 26, 26, 0.18)' },
  { accent: '#526b7a', soft: 'rgba(82, 107, 122, 0.08)', border: 'rgba(82, 107, 122, 0.22)' },
  { accent: '#806b47', soft: 'rgba(128, 107, 71, 0.09)', border: 'rgba(128, 107, 71, 0.24)' },
  { accent: '#6B7280', soft: 'rgba(107, 114, 128, 0.08)', border: 'rgba(107, 114, 128, 0.22)' },
]

const getSubjectAccent = (index = 0) => subjectAccentPalette[Math.abs(index) % subjectAccentPalette.length]

const getOfficeAccentStyle = (_office, index = 0) => {
  const color = getSubjectAccent(index)
  return {
    '--office-accent': color.accent,
    '--office-accent-soft': color.soft,
    '--office-accent-border': color.border,
  }
}

const decorateMetricCards = (kpis = [], offices = []) => (
  (kpis || []).map((item) => {
    const label = item.label || item.key || ''
    const officeIndex = offices.findIndex(office => label.startsWith(office.name))
    if (officeIndex < 0) {
      return {
        label,
        value: item.value ?? item.displayValue ?? formatDisplayValue(item.value),
      }
    }
    const office = offices[officeIndex]
    const color = getSubjectAccent(officeIndex)
    return {
      label: label.replace(office.name, ''),
      value: item.value ?? item.displayValue ?? formatDisplayValue(item.value),
      subject: office.name,
      accentStyle: {
        '--metric-accent': color.accent,
        '--metric-accent-soft': color.soft,
        '--metric-accent-border': color.border,
      },
    }
  }).filter(item => item.label)
)

const getOfficeKpiLabel = (office, type) => {
  const matchers = {
    task: /总任务|任务金额|目标/i,
    actual: /年度开单|开单|完成|实际|销售/i,
    remain: /剩余|缺口|差额|remain/i,
    rate: /达成率|percent|rate/i,
  }
  const matcher = matchers[type]
  const item = (office?.kpis || []).find(kpi => matcher?.test(kpi.label || ''))
  return item?.value || '-'
}

const getReportKpi = (report, type) => {
  const matchers = {
    task: /总任务|任务金额|目标/i,
    actual: /年度开单|开单|完成|实际|销售/i,
    remain: /剩余|缺口|差额|remain/i,
    rate: /达成率|percent|rate/i,
  }
  const matcher = matchers[type]
  return (report?.kpis || []).find(kpi => matcher?.test(kpi.label || '')) || null
}

const getReportKpiText = (report, type) => getReportKpi(report, type)?.value || '-'

const getSingleOrgCounts = (report) => {
  const offices = report?.offices || []
  const directCount = offices.length
  const detailCount = offices.reduce((sum, office) => (
    sum + Number(office.childCount || office.detailRows?.length || 0)
  ), 0)
  return {
    directCount,
    detailCount,
    directLabel: report?.compareLevelLabel || '下级节点',
    detailLabel: report?.detailLevelLabel || '明细节点',
  }
}

const getKnownChildLevelLabel = (levelLabel = '') => {
  const text = String(levelLabel || '').trim()
  if (/战区/.test(text) && !/城市/.test(text)) return '城市站'
  if (/片区|行业部/.test(text)) return '客户经理'
  return ''
}

const getOfficeSubtitle = (office, report) => {
  if (office?.isLeafLevel) {
    return `${office.leafLabel || '当前最细层'} · ${office.parentName || '当前口径'}`
  }
  return `${office?.childCount || 0} 个${report?.detailLevelLabel || office?.detailLevelLabel || '明细层级'} · ${office?.parentName || '当前口径'}`
}

const getOfficeToggleTitle = (office, report) => (
  office?.isLeafLevel
    ? `查看${office.name || '当前对象'}当前层指标`
    : `展开查看${office?.childCount || 0}个${report?.detailLevelLabel || office?.detailLevelLabel || '明细层级'}`
)

const getOfficeEmptyDrillText = (office, report) => (
  office?.isLeafLevel
    ? `${office.name || '当前对象'}已到当前最细层，暂无可继续下钻的下级明细。`
    : `当前 SQL 结果未返回 ${report?.detailLevelLabel || office?.detailLevelLabel || '明细层级'} 明细。请重新问“${office?.name || '当前对象'}下${report?.detailLevelLabel || office?.detailLevelLabel || '明细层级'}业绩明细”或检查 SQL 是否包含下级层级。`
)

const reportHasDrillableOffices = (report) => (
  Array.isArray(report?.offices) && report.offices.some(office => !office?.isLeafLevel)
)

const isLeafOnlyReport = (report) => (
  Array.isArray(report?.offices) && report.offices.length > 0 && report.offices.every(office => office?.isLeafLevel)
)

const canToggleOffice = (office) => !office?.isLeafLevel

const getReportRiskCount = (report) => {
  const offices = Array.isArray(report?.offices) ? report.offices : []
  if (!offices.length) return 0
  const threshold = report?.answerMode === 'ranking' || report?.answerMode === 'filter' ? 10 : 15
  return offices.filter(item => {
    const rate = toNumber(item?.rate)
    return rate !== null && rate < threshold
  }).length
}

const getMetricValueFromOffice = (office, label = '') => {
  const metricText = String(label || '')
  const kpis = Array.isArray(office?.kpis) ? office.kpis : []
  const direct = kpis.find(item => {
    const itemLabel = String(item?.label || '')
    return itemLabel && (itemLabel.includes(metricText) || metricText.includes(itemLabel))
  })
  const directValue = toNumber(direct?.value)
  if (directValue !== null) return directValue
  if (isRateMetricLabel(metricText)) return toNumber(office?.rate)
  if (/开单|完成|实际|销售/i.test(metricText)) return toNumber(getOfficeKpiLabel(office, 'actual'))
  if (/任务|目标/i.test(metricText)) return toNumber(getOfficeKpiLabel(office, 'task'))
  if (/剩余|缺口|差额|remain/i.test(metricText)) return toNumber(getOfficeKpiLabel(office, 'remain'))
  return toNumber(office?.rate)
}

const getReportSortSpec = (report = null) => {
  const datasetSortSpec = report?.dataset?.report_spec?.sortSpec
  const directSortSpec = report?.sortSpec
  const source = (datasetSortSpec && typeof datasetSortSpec === 'object' ? datasetSortSpec : directSortSpec) || {}
  const explicitMetricLabel = getQuestionRankingMetricLabel()
  if (!explicitMetricLabel || report?.answerMode !== 'ranking') return source
  return {
    ...source,
    metricLabel: explicitMetricLabel,
    direction: source.direction || (isNegativeRankingQuestion() ? 'asc' : 'desc'),
  }
}

const getSortMetricLabel = (report = null, fallback = '达成率') => (
  (report?.answerMode === 'ranking' ? getQuestionRankingMetricLabel() : '')
  || getReportSortSpec(report).metricLabel
  || report?.primaryAnswer?.metricLabel
  || report?.filterAnswer?.metricLabel
  || fallback
)

const normalizeRankingPrimaryAnswer = (report, offices = []) => {
  const answer = report?.primaryAnswer || {}
  if (report?.answerMode !== 'ranking') return answer
  const metricLabel = getQuestionRankingMetricLabel() || getReportSortSpec(report).metricLabel || answer?.metricLabel || '达成率'
  const levelLabel = report?.compareLevelLabel || answer?.targetLevel || '对象'
  const count = offices.length || Number(answer?.count || answer?.total || 0) || 0
  return {
    ...answer,
    title: answer?.title || '排名结果',
    text: `已按${metricLabel}输出${count ? ` ${count} 个` : ''}${levelLabel}的排序结果`,
    metricLabel,
    targetLevel: levelLabel,
    direction: getReportSortSpec(report).direction || answer?.direction || (isNegativeRankingQuestion() ? 'asc' : 'desc'),
  }
}

const sortOfficesByAnswerMetric = (offices = [], report = null) => {
  if (!Array.isArray(offices) || !offices.length) return []
  const sortSpec = getReportSortSpec(report)
  const metricLabel = getSortMetricLabel(report, '')
  if (!metricLabel) return [...offices]
  const lowFirst = (sortSpec.direction || report?.primaryAnswer?.direction || '').toLowerCase() === 'asc'
  return [...offices].sort((left, right) => {
    const leftValue = getMetricValueFromOffice(left, metricLabel)
    const rightValue = getMetricValueFromOffice(right, metricLabel)
    if (leftValue === null && rightValue === null) return 0
    if (leftValue === null) return 1
    if (rightValue === null) return -1
    return lowFirst ? leftValue - rightValue : rightValue - leftValue
  })
}

const getSingleOrgRateTone = (report) => {
  const rate = toNumber(getReportKpiText(report, 'rate'))
  if (rate === null) return 'neutral'
  return rate < 10 ? 'danger' : rate < 15 ? 'warn' : 'good'
}

const getSingleOrgConclusion = (report) => {
  if (!report) return ''
  const focusName = report.focusName || '当前组织'
  const task = getReportKpiText(report, 'task')
  const actual = getReportKpiText(report, 'actual')
  const rate = getReportKpiText(report, 'rate')
  const remain = getReportKpiText(report, 'remain')
  const remainText = remain && remain !== '-' ? `，剩余缺口 ${remain}` : ''
  const toneLabel = {
    good: '整体进度相对领先',
    warn: '整体进度偏滞后',
    danger: '整体进度明显滞后',
    neutral: '整体进度已形成初步判断',
  }[getSingleOrgRateTone(report)]
  return `${focusName}${toneLabel}，年度总任务 ${task}，当前开单 ${actual}，整体达成率 ${rate}${remainText}。`
}

const getSingleOrgRankContext = (report) => {
  const offices = report?.offices || []
  const ranked = [...offices].filter(item => item.rate !== null).sort((a, b) => (b.rate || 0) - (a.rate || 0))
  const best = ranked[0]
  const worst = ranked[ranked.length - 1]
  const diff = best && worst && best.rate !== null && worst.rate !== null
    ? Math.abs((best.rate || 0) - (worst.rate || 0)).toFixed(2).replace(/\.?0+$/, '')
    : ''
  return { best, worst, diff }
}

const getReportMetricContext = (report) => {
  const metricLabel = getSortMetricLabel(report, '达成率')
  const sortSpec = getReportSortSpec(report)
  const lowFirst = String(sortSpec.direction || report?.primaryAnswer?.direction || '').toLowerCase() === 'asc'
  const ranked = sortOfficesByAnswerMetric(
    (report?.offices || []).filter(item => getMetricValueFromOffice(item, metricLabel) !== null),
    report,
  )
  const best = ranked[0] || null
  const worst = ranked[ranked.length - 1] || null
  const bestValue = best ? getMetricValueFromOffice(best, metricLabel) : null
  const worstValue = worst ? getMetricValueFromOffice(worst, metricLabel) : null
  const diff = bestValue !== null && worstValue !== null && best?.name !== worst?.name
    ? (isRateMetricLabel(metricLabel)
      ? `${Math.abs(bestValue - worstValue).toFixed(2).replace(/\.?0+$/, '')}个百分点`
      : formatAmount(Math.abs(bestValue - worstValue)))
    : ''
  return { metricLabel, lowFirst, ranked, best, worst, diff }
}

const isCollectionAnswerMode = (report) => ['filter', 'ranking', 'drilldown'].includes(report?.answerMode || '')
const isRateMetricLabel = (label = '') => /达成率|完成率|rate|percent/i.test(String(label || ''))
const isAmountMetricLabel = (label = '') => /开单|金额|任务|销售|完成|实际/i.test(String(label || ''))
const findOfficeMetricValueByLabel = (office, label = '') => {
  const kpis = Array.isArray(office?.kpis) ? office.kpis : []
  const text = String(label || '')
  if (!text) return ''
  const direct = kpis.find(item => {
    const itemLabel = String(item?.label || '')
    return itemLabel && (itemLabel.includes(text) || text.includes(itemLabel))
  })
  if (direct?.value) return direct.value
  if (isRateMetricLabel(text)) return office?.rateLabel || ''
  if (/开单|完成|实际|销售/i.test(text)) return getOfficeKpiLabel(office, 'actual')
  if (/任务|目标/i.test(text)) return getOfficeKpiLabel(office, 'task')
  if (/剩余|缺口|差额|remain/i.test(text)) return getOfficeKpiLabel(office, 'remain')
  return ''
}

const buildCollectionMetricCards = (report) => {
  const offices = sortOfficesByAnswerMetric(report?.offices, report)
  if (!offices.length) return []
  const leader = offices[0] || null
  const tail = offices[offices.length - 1] || null
  const metricLabel = getSortMetricLabel(report, '指标')
  const metricValue = (office) => (
    findOfficeMetricValueByLabel(office, metricLabel)
    || (isAmountMetricLabel(metricLabel) ? getOfficeKpiLabel(office, 'actual') : '')
    || office?.rateLabel
    || '-'
  )
  const riskCount = getReportRiskCount(report)
  return [
    {
      label: report?.answerMode === 'filter' ? '命中数量' : '结果数量',
      value: `${offices.length} 个`,
      hint: `${report?.compareLevelLabel || '对象'}结果集合`,
      tone: 'neutral',
    },
    leader ? {
      label: report?.answerMode === 'ranking' ? '榜首结果' : '最高结果',
      value: leader.name,
      hint: `${metricLabel} ${metricValue(leader)}`,
      tone: 'good',
    } : null,
    tail ? {
      label: report?.answerMode === 'ranking' ? '末位结果' : '边界结果',
      value: tail.name,
      hint: `${metricLabel} ${metricValue(tail)}`,
      tone: report?.answerMode === 'ranking' ? 'warn' : 'neutral',
    } : null,
    {
      label: '风险节点',
      value: `${riskCount} 个`,
      hint: riskCount ? '存在明显滞后对象，建议继续下钻' : '当前结果内暂无明显风险节点',
      tone: riskCount ? 'danger' : 'good',
    },
  ].filter(Boolean)
}

const enrichSingleOrgMetricCards = (cards = [], report) => (
  (cards || []).map((card) => {
    const label = card.label || ''
    let hint = ''
    let tone = ''
    if (/总任务|任务金额|目标/i.test(label)) {
      hint = `${report?.focusName || '当前组织'}年度目标总量`
    } else if (/年度开单|开单|完成|实际|销售/i.test(label)) {
      hint = '当前已完成金额'
    } else if (/达成率|percent|rate/i.test(label)) {
      tone = getSingleOrgRateTone(report)
      hint = tone === 'good' ? '高于标杆线，保持节奏' : tone === 'danger' ? '低于风险线，需重点干预' : '低于预期进度，需持续跟进'
    } else if (/剩余|缺口|差额|remain/i.test(label)) {
      tone = 'warn'
      hint = '后续需推进缺口金额'
    }
    return { ...card, hint, tone }
  })
)

const getDrillBestText = (office) => {
  const rows = Array.isArray(office?.detailRows) ? office.detailRows : []
  const best = rows.filter(item => item.rate !== null && item.rate !== undefined)
    .sort((left, right) => (right.rate || 0) - (left.rate || 0))[0]
  if (!best) return office?.highlight || '暂无下级明细'
  return `${best.name} ${best.rateLabel || '-'}`
}

const getDrillWorstText = (office) => {
  const rows = Array.isArray(office?.detailRows) ? office.detailRows : []
  const worst = rows.filter(item => item.rate !== null && item.rate !== undefined)
    .sort((left, right) => (left.rate || 0) - (right.rate || 0))[0]
  if (!worst) return office?.riskSummary || '暂无风险明细'
  return `${worst.name} ${worst.rateLabel || '-'}`
}

const findColumn = (columns = [], matcher) => columns.find(column => matcher(String(column || ''))) || ''

const buildOfficeDetailRows = (chartSpec = {}, config = {}) => {
  const rows = Array.isArray(chartSpec.rows) ? chartSpec.rows : []
  const columns = Array.isArray(chartSpec.columns) && chartSpec.columns.length
    ? chartSpec.columns
    : Object.keys(rows[0] || {})
  const dataset = chartSpec?.dataset || null
  const nameColumn = columns[0] || '名称'
  const rateColumn = findColumn(columns, column => isRateColumn(column)) || '达成率'
  const taskColumn = findColumn(columns, column => /任务|目标/i.test(column) && !/剩余|缺口/i.test(column))
  const actualColumn = findColumn(columns, column => /开单|完成|实际|销售/i.test(column))
  const remainColumn = findColumn(columns, column => /剩余|缺口|差额|remain/i.test(column))

  return rows.map((row) => {
    const rate = toNumber(row?.[rateColumn]) || 0
    const remain = toNumber(row?.[remainColumn]) || 0
    const task = toNumber(row?.[taskColumn]) || 0
    const actual = toNumber(row?.[actualColumn]) || 0
    const label = row?.标签 || getOfficeRateTag(rate, config, '标杆')
    return {
      name: row?.[nameColumn] || row?.名称 || '-',
      rate,
      rateLabel: isRateColumn(rateColumn) ? `${rate.toLocaleString('zh-CN', { maximumFractionDigits: 2 })}%` : formatDisplayValue(rate),
      task,
      taskLabel: taskColumn ? formatAmount(task, resolveAmountMetric({ format: 'amount', column: taskColumn }, dataset, taskColumn)) : '-',
      actual,
      actualLabel: actualColumn ? formatAmount(actual, resolveAmountMetric({ format: 'amount', column: actualColumn }, dataset, actualColumn)) : '-',
      remain,
      remainLabel: remainColumn ? formatAmount(remain, resolveAmountMetric({ format: 'amount', column: remainColumn }, dataset, remainColumn)) : '-',
      label,
      tone: getToneFromDisplayTag(label, getOfficeRateTone(rate, config)),
      progress: Math.max(0, Math.min(100, rate)),
      gapProgress: 0,
    }
  }).map((row, _index, list) => {
    const maxRemain = Math.max(...list.map(item => item.remain || 0), 1)
    return {
      ...row,
      gapProgress: Math.max(0, Math.min(100, ((row.remain || 0) / maxRemain) * 100)),
    }
  })
}

const getDescendantNodes = (node) => {
  const output = []
  const walk = (current) => {
    ;(current?.children || []).forEach((child) => {
      output.push(child)
      walk(child)
    })
  }
  walk(node)
  return output
}

const isLeafNode = (node) => !Array.isArray(node?.children) || node.children.length === 0

const getLevelLabelFromNodes = (nodes = [], fallback = '层级') => {
  const values = Array.from(new Set(nodes.map(node => node?.levelValue || node?.levelName).filter(Boolean)))
  if (values.length === 1) return values[0]
  if (values.length > 1) return values.join(' / ')
  return fallback
}

const findQuestionFocusNode = (nodes = []) => {
  const questionText = String(session.state.question || query.value || '').trim()
  if (!questionText) return null
  return [...nodes]
    .filter(node => node?.name && questionText.includes(node.name) && Array.isArray(node.children) && node.children.length > 0)
    .sort((a, b) => String(b.name).length - String(a.name).length)[0] || null
}

const getComparisonNodes = (model) => {
  const focusNode = findQuestionFocusNode(model.flatNodes || [])
  const requestedLevels = getRequestedLevelValues(getQuestionText(), model.config || {})
  if (requestedLevels.length) {
    const scopedNodes = focusNode ? getDescendantNodes(focusNode) : (model.flatNodes || [])
    const levelNodes = scopedNodes.filter(node => (
      node?.name
      && (
        requestedLevels.includes(canonicalRequestedLevel(node.levelValue))
        || requestedLevels.includes(canonicalRequestedLevel(node.levelName))
        || requestedLevels.some(value => value && String(node.name || '').includes(value))
      )
    ))
    if (levelNodes.length) return levelNodes
  }
  if (focusNode?.children?.length) return focusNode.children
  const singleRoot = model.tree?.length === 1 ? model.tree[0] : null
  if (singleRoot?.children?.length) return singleRoot.children
  const parentNodes = (model.flatNodes || []).filter(node => Array.isArray(node.children) && node.children.length > 0)
  const maxParentDepth = Math.max(...parentNodes.map(node => Number(node.depth) || 0), 0)
  return parentNodes.filter(node => Number(node.depth) === maxParentDepth)
}

const getDetailNodes = (node) => {
  const directChildren = (node?.children || []).filter(item => item?.name)
  if (directChildren.length) return directChildren
  return getDescendantNodes(node).filter(item => item?.name)
}

const hasBusinessDrillDataset = (datasets) => (
  (datasets || []).some(dataset => Boolean(buildBusinessDrillReport(dataset)))
)

const buildBusinessDrillReportFromSpec = (dataset) => {
  const spec = dataset?.report_spec
  if (!spec || spec.version !== '2.0') return null
  const overviewChart = Array.isArray(spec.charts) ? spec.charts[0] : null
  const rawAccordions = Array.isArray(spec.accordions) ? spec.accordions : []
  const overviewRows = Array.isArray(overviewChart?.rows) ? overviewChart.rows : []
  if (!overviewChart && !rawAccordions.length) return null

  const config = getDatasetReportConfig(dataset)
  const requestedLevels = getRequestedLevelValues(getQuestionText(), config)
  const compareLevelLabel = requestedLevels[0] || spec.scope?.compareLevelLabel || '下一层级'
  const detailLevelLabel = spec.scope?.detailLevelLabel || '明细层级'
  const inferredDetailLevelLabel = getKnownChildLevelLabel(compareLevelLabel) || detailLevelLabel
  const accordions = rawAccordions.length
    ? rawAccordions
    : overviewRows.map((row, index) => {
        const name = row?.名称 || row?.name || row?.[overviewChart?.columns?.[0]] || `当前层对象 ${index + 1}`
        return {
          id: `overview-${index}-${name}`,
          title: name,
          parentName: spec.scope?.focusNode || '',
          levelLabel: compareLevelLabel,
          detailLevelLabel: inferredDetailLevelLabel,
          isLeafLevel: !getKnownChildLevelLabel(compareLevelLabel),
          leafLabel: getKnownChildLevelLabel(compareLevelLabel) ? '' : '当前最细层',
          childCount: 0,
          tag: row?.标签 || '',
          kpis: Object.entries(row || {})
            .filter(([key]) => !['名称', 'name', '标签'].includes(key))
            .map(([key, value]) => ({ label: key, value })),
          narrative: `${name}已是当前结果的最细层级。`,
          detailNarrative: `${name}已是当前结果的最细层级，右侧展示该节点当前指标。`,
          chart: {
            chartType: overviewChart?.chartType || 'horizontalDrill',
            title: `${name}当前层指标`,
            columns: overviewChart?.columns || Object.keys(row || {}),
            rows: [row],
            dataset,
          },
          drillGroups: [],
        }
      })
  const matchedAccordions = requestedLevels.length
    ? accordions.filter(item => (
        requestedLevels.includes(item?.levelLabel)
        || requestedLevels.some(value => value && String(item?.title || '').includes(value))
      ))
    : []
  const sourceAccordions = requestedLevels.length && matchedAccordions.length ? matchedAccordions : accordions
  const mappedOffices = sourceAccordions.map((item) => {
    const itemLevelLabel = item.levelLabel || compareLevelLabel
    const knownChildLevelLabel = getKnownChildLevelLabel(itemLevelLabel)
    const itemDetailLevelLabel = item.detailLevelLabel || knownChildLevelLabel || detailLevelLabel
    const rateKpi = (item.kpis || []).find(kpi => /率|percent|rate/i.test(kpi.label || ''))
    const rateValue = toNumber(rateKpi?.value)
    const chartRows = Array.isArray(item.chart?.rows) ? item.chart.rows : []
    const narrative = String(item.narrative || '').trim()
    const detailRows = buildOfficeDetailRows({ ...(item.chart || {}), dataset }, config)
    const drillGroups = (Array.isArray(item.drillGroups) ? item.drillGroups : [])
      .map((group) => {
        const groupRateKpi = (group.kpis || []).find(kpi => /率|percent|rate/i.test(kpi.label || ''))
        const groupRateValue = toNumber(groupRateKpi?.value)
        const groupRows = buildOfficeDetailRows({ ...(group.chart || {}), dataset }, config)
        const groupTag = group.tag || getOfficeRateTag(groupRateValue, config, '片区标杆')
        return {
          id: group.id || `${item.id || item.title}-${group.title}`,
          name: group.title || '未命名下级节点',
          parentName: group.parentName || item.title || '',
          tone: getToneFromDisplayTag(groupTag, getOfficeRateTone(groupRateValue, config)),
          tag: groupTag,
          rate: groupRateValue,
          rateLabel: groupRateKpi?.value || '-',
          progress: Math.max(0, Math.min(100, groupRateValue || 0)),
          childCount: groupRows.length,
          kpis: group.kpis || [],
          summary: String(group.narrative || '').trim(),
          chartText: group.detailNarrative || (groupRows.length ? `${group.title || '当前节点'}继续下钻到${group.detailLevelLabel || '业务员'}。` : ''),
          detailLevelLabel: group.detailLevelLabel || '业务员',
          detailRows: groupRows,
        }
      })
      .filter(group => group.detailRows.length > 0)
    const summaryText = narrative
      .split('\n')
      .map(line => line.trim())
      .filter(Boolean)
      .slice(0, 3)
      .join('；') || narrative
    const itemTag = item.tag || getOfficeRateTag(rateValue, config, '区域标杆')
    return {
      id: item.id || item.title,
      name: item.title || '未命名节点',
      parentName: item.parentName || item.levelLabel || '',
      tone: getToneFromDisplayTag(itemTag, getOfficeRateTone(rateValue, config)),
      tag: itemTag,
      highlight: item.highlight || '',
      rankLabel: item.rankLabel || '',
      rate: rateValue,
      rateLabel: rateKpi?.value || '-',
      progress: Math.max(0, Math.min(100, rateValue || 0)),
      childCount: Number.isFinite(Number(item.childCount)) ? Number(item.childCount) : chartRows.length,
      isLeafLevel: knownChildLevelLabel ? false : Boolean(item.isLeafLevel),
      leafLabel: knownChildLevelLabel ? '' : (item.leafLabel || ''),
      kpis: item.kpis || [],
      summary: summaryText,
      chartText: item.detailNarrative || '',
      chartSpec: item.chart,
      detailRows,
      drillGroups,
      detailLevelLabel: itemDetailLevelLabel,
    }
  })
  const answerMode = spec.answerMode || spec.analysisMode || 'detail'
  const answerSummary = spec.answerSummary || {}
  const reportContext = {
    dataset,
    sortSpec: spec.sortSpec || {},
    answerMode,
    primaryAnswer: ['ranking', 'drilldown'].includes(answerMode) ? answerSummary : null,
    filterAnswer: answerMode === 'filter' ? answerSummary : null,
  }
  const offices = sortOfficesByAnswerMetric(mappedOffices, reportContext).map((office, index) => {
    if (answerMode !== 'ranking') return office
    const childLevelLabel = getKnownChildLevelLabel(compareLevelLabel)
    const summary = childLevelLabel
      ? `${office.name}${office.tag ? ` ${office.tag}` : ''}；总任务金额 ${getOfficeKpiLabel(office, 'task')}，年度开单金额 ${getOfficeKpiLabel(office, 'actual')}，达成率 ${getOfficeKpiLabel(office, 'rate')}，剩余任务金额 ${getOfficeKpiLabel(office, 'remain')}。可继续下钻查看${childLevelLabel}明细。`
      : String(office.summary || '').replace(/（排序第\d+）/g, '')
    return {
      ...office,
      rankLabel: `排序第${index + 1}`,
      summary,
    }
  })
  const riskCount = getReportRiskCount({ ...reportContext, offices })
  const officeNames = new Set(offices.map(item => item.name))
  const filteredOverviewChart = overviewChart && officeNames.size
    ? {
        ...overviewChart,
        rows: (overviewChart.rows || []).filter(row => officeNames.has(row?.名称 || row?.name || row?.[overviewChart.columns?.[0]])),
      }
    : overviewChart
  const summary = Array.isArray(spec.narrative) && spec.narrative.length
    ? spec.narrative.join('；')
    : spec.sections?.find(section => section.key === 'overview')?.narrative || `本次结果覆盖 ${offices.length} 个${compareLevelLabel}。`
  const matchedNodes = Array.isArray(spec.matchedNodes) ? spec.matchedNodes : []
  const filterAnswer = spec.answerMode === 'filter'
    ? {
        ...spec.answerSummary,
        nodes: matchedNodes.map((node) => {
          const office = offices.find(item => item.name === node.name)
          const metric = node.metric || {}
          return {
            id: office?.id || node.id || node.name,
            name: node.name || '未命名对象',
            levelLabel: node.levelLabel || compareLevelLabel,
            tag: node.tag || office?.tag || '',
            tone: office?.tone || getOfficeRateTone(toNumber(metric.rawValue), config),
            metricLabel: metric.label || spec.answerSummary?.metricLabel || '指标',
            metricValue: metric.value ?? formatDisplayValue(metric.rawValue),
            kpis: Array.isArray(node.kpis) ? node.kpis : [],
          }
        }),
      }
    : null
  let primaryAnswer = ['ranking', 'drilldown'].includes(spec.answerMode)
    ? {
        ...spec.answerSummary,
      }
    : null

  const sortMetricLabel = getSortMetricLabel({ ...reportContext, primaryAnswer, filterAnswer }, '达成率')
  primaryAnswer = normalizeRankingPrimaryAnswer({ ...reportContext, primaryAnswer, filterAnswer, compareLevelLabel }, offices)

  return {
    dataset,
    sortSpec: spec.sortSpec || {},
    analysisMode: spec.analysisMode || 'detail',
    answerMode,
    primaryAnswer,
    filterAnswer,
    focusName: spec.scope?.focusNode || '',
    isSingleFocus: Boolean(spec.scope?.focusNode && spec.analysisMode !== 'comparative'),
    kpis: (spec.kpis || []).map(item => ({
      label: item.label || item.key,
      value: item.displayValue ?? formatDisplayValue(item.value),
    })).filter(item => item.label),
    offices,
    compareLevelLabel,
    detailLevelLabel: inferredDetailLevelLabel,
    officeCompareSpec: normalizeOfficeCompareSpec(filteredOverviewChart, config),
    officeCompareText: getKnownChildLevelLabel(compareLevelLabel)
      ? `当前结果按${compareLevelLabel}展示；${compareLevelLabel}下级为${inferredDetailLevelLabel}，可继续下钻查看${inferredDetailLevelLabel}明细。`
      : spec.sections?.find(section => section.key === 'drill')?.narrative || `一行一个同层级对象，按${sortMetricLabel}排序；对齐展示任务、开单、缺口、达成率和进度条，必要时继续下钻。`,
    summary,
    riskTone: riskCount ? 'danger' : 'good',
    riskLabel: riskCount ? `风险 ${riskCount} 个` : '整体可控',
  }
}

const buildBusinessDrillReport = (dataset) => {
  const specReport = buildBusinessDrillReportFromSpec(dataset)
  if (specReport) return specReport

  const model = getDatasetTreeModel(dataset)
  if (!model?.flatNodes?.length) return null
  const config = model.config || getDatasetReportConfig(dataset)
  const taskMetric = getMetricDefinition(config, 'task', item => /任务|目标/i.test(item.label || item.column || ''))
  const actualMetric = getMetricDefinition(config, 'actual', item => /开单|完成|实际/i.test(item.label || item.column || ''))
  const rateMetric = getMetricDefinition(config, 'rate', item => item.format === 'percent' || /率|rate/i.test(item.label || item.column || ''))
  const remainMetric = getMetricDefinition(config, 'remain', item => /剩余|缺口|差额/i.test(item.label || item.column || ''))
  if (!rateMetric) return null
  const rankingMetric = isAmountRankingQuestion() ? (actualMetric || rateMetric) : rateMetric
  const rankingMetricLabel = rankingMetric?.label || rankingMetric?.column || '达成率'
  const rankingChartType = isAmountRankingQuestion() ? 'bar' : 'horizontalRateBar'

  const focusNode = findQuestionFocusNode(model.flatNodes || [])
  const isSingleFocus = Boolean(focusNode && !/对比|比较|哪个|谁更|差异|分别|各自|和.+比|跟.+比|与.+比|\bvs\b/i.test(session.state.question || query.value || ''))
  const officeNodes = getComparisonNodes(model)
    .filter(node => node?.name)

  if (!officeNodes.length) return null
  const compareLevelLabel = getLevelLabelFromNodes(officeNodes, '下一层级')
  const detailLevelLabel = getLevelLabelFromNodes(officeNodes.flatMap(getDetailNodes), '明细层级')

  const offices = officeNodes.map((office) => {
    const people = getDetailNodes(office)
    const directChildren = people.length ? people : office.children || []
    const sortedPeople = [...directChildren]
      .filter(item => item?.name)
      .sort((a, b) => (getNodeMetricValue(a, rankingMetric) || 0) - (getNodeMetricValue(b, rankingMetric) || 0))
    const sortedPeopleDesc = [...sortedPeople].sort((a, b) => (getNodeMetricValue(b, rateMetric) || 0) - (getNodeMetricValue(a, rateMetric) || 0))
    const rate = getNodeMetricValue(office, rateMetric)
    const tone = getOfficeRateTone(rate, config)
    const riskPeople = sortedPeople.filter(item => getRateTone(getNodeMetricValue(item, rateMetric), 20, 10) === 'danger')
    const bestPerson = sortedPeopleDesc[0]
    const worstPerson = sortedPeople[0]
    const formatPersonMetric = (person, metric) => (
      metric ? formatMetricByDefinition(getNodeMetricValue(person, metric), metric, dataset) : '-'
    )
    const describePerson = (person) => {
      if (!person) return ''
      const actualText = formatPersonMetric(person, actualMetric)
      const taskText = formatPersonMetric(person, taskMetric)
      const remainText = formatPersonMetric(person, remainMetric)
      const rateText = formatPersonMetric(person, rateMetric)
      return `${person.name}开单${actualText} / 任务${taskText}，达成率${rateText}${remainMetric ? `，剩余缺口${remainText}` : ''}`
    }
    const chartPeople = isNegativeRankingQuestion() ? sortedPeople : [...directChildren]
      .filter(item => item?.name)
      .sort((a, b) => (getNodeMetricValue(b, rankingMetric) || 0) - (getNodeMetricValue(a, rankingMetric) || 0))
    const chartRows = chartPeople.map(person => {
      const personRate = getNodeMetricValue(person, rateMetric) || 0
      return {
      名称: person.name,
      [rateMetric.label || rateMetric.column || '达成率']: personRate,
      [actualMetric?.label || actualMetric?.column || '完成']: getNodeMetricValue(person, actualMetric) || 0,
      [taskMetric?.label || taskMetric?.column || '任务']: getNodeMetricValue(person, taskMetric) || 0,
      ...(remainMetric ? { [remainMetric.label || remainMetric.column || '剩余']: getNodeMetricValue(person, remainMetric) || 0 } : {}),
      标签: getOfficeRateTag(personRate, config, '标杆'),
    }
    })
    const officeKpis = [
      taskMetric ? { label: taskMetric.label || taskMetric.column, value: formatMetricByDefinition(getNodeMetricValue(office, taskMetric), taskMetric, dataset) } : null,
      actualMetric ? { label: actualMetric.label || actualMetric.column, value: formatMetricByDefinition(getNodeMetricValue(office, actualMetric), actualMetric, dataset) } : null,
      { label: rateMetric.label || rateMetric.column || '达成率', value: formatMetricByDefinition(rate, rateMetric, dataset) },
      remainMetric ? { label: remainMetric.label || remainMetric.column, value: formatMetricByDefinition(getNodeMetricValue(office, remainMetric), remainMetric, dataset) } : null,
    ].filter(Boolean)

    return {
      id: office.id || office.name,
      name: office.name,
      parentName: office.parentName,
      tone,
      rate,
      rateLabel: formatMetricByDefinition(rate, rateMetric, dataset),
      progress: Math.max(0, Math.min(100, rate || 0)),
      childCount: sortedPeople.length,
      isLeafLevel: sortedPeople.length === 0,
      leafLabel: sortedPeople.length === 0 ? '当前最细层' : '',
      kpis: officeKpis,
      tag: getOfficeRateTag(rate, config, '区域标杆'),
      highlight: bestPerson ? `亮点：${bestPerson.name}达成率${formatPersonMetric(bestPerson, rateMetric)}` : '',
      rankLabel: '',
      summary: `${office.name}达成率${formatMetricByDefinition(rate, rateMetric, dataset)}，${getOfficeToneLabel(tone)}；任务${taskMetric ? formatMetricByDefinition(getNodeMetricValue(office, taskMetric), taskMetric, dataset) : '-'} / 已完成${actualMetric ? formatMetricByDefinition(getNodeMetricValue(office, actualMetric), actualMetric, dataset) : '-'}${remainMetric ? ` / 缺口${formatMetricByDefinition(getNodeMetricValue(office, remainMetric), remainMetric, dataset)}` : ''}。${bestPerson ? `亮点：${bestPerson.name}达成率${formatPersonMetric(bestPerson, rateMetric)}` : `暂无${detailLevelLabel}明细`}；${riskPeople.length ? `${riskPeople.length} 个${detailLevelLabel}低于10%风险线` : `暂无低于10%的风险${detailLevelLabel}`}。`,
      chartText: `${office.name}下钻到${detailLevelLabel}层：${bestPerson ? `最高为${describePerson(bestPerson)}` : `暂无${detailLevelLabel}明细`}；${worstPerson ? `最低为${describePerson(worstPerson)}。` : ''}`,
      chartSpec: {
        chartType: 'horizontalDrill',
        title: `${office.name}${detailLevelLabel}达成率与缺口`,
        columns: ['名称', actualMetric?.label || actualMetric?.column || '完成', taskMetric?.label || taskMetric?.column || '任务', remainMetric?.label || remainMetric?.column || '剩余', rateMetric.label || rateMetric.column || '达成率'].filter(Boolean),
        rows: chartRows,
        dataset,
      },
      detailRows: buildOfficeDetailRows({
        columns: ['名称', actualMetric?.label || actualMetric?.column || '完成', taskMetric?.label || taskMetric?.column || '任务', remainMetric?.label || remainMetric?.column || '剩余', rateMetric.label || rateMetric.column || '达成率'].filter(Boolean),
        rows: chartRows,
      }, config),
    }
  }).sort((a, b) => {
    const left = getMetricValueFromOffice(a, rankingMetricLabel) || 0
    const right = getMetricValueFromOffice(b, rankingMetricLabel) || 0
    return isNegativeRankingQuestion() ? left - right : right - left
  })

  const kpis = (config.metrics || []).map(metric => ({
    label: metric.label || metric.column || metric.key,
    value: formatMetricByDefinition(model.rootMetrics?.[metric.key], metric, dataset),
  })).filter(item => item.value !== '-')
  const bestOffice = offices[0]
  const worstOffice = offices[offices.length - 1]
  const riskCount = offices.filter(item => item.tone === 'danger').length
  const officeCompareRows = offices.map(office => ({
    名称: office.name,
    [actualMetric?.label || actualMetric?.column || '完成']: getNodeMetricValue(officeNodes.find(node => node.name === office.name), actualMetric) || 0,
    [taskMetric?.label || taskMetric?.column || '任务']: getNodeMetricValue(officeNodes.find(node => node.name === office.name), taskMetric) || 0,
    ...(remainMetric ? { [remainMetric.label || remainMetric.column || '剩余']: getNodeMetricValue(officeNodes.find(node => node.name === office.name), remainMetric) || 0 } : {}),
    [rateMetric.label || rateMetric.column || '达成率']: office.rate || 0,
    标签: office.tag,
  })).sort((a, b) => {
    const key = rankingMetric.label || rankingMetric.column || '达成率'
    return isNegativeRankingQuestion()
      ? (a[key] || 0) - (b[key] || 0)
      : (b[key] || 0) - (a[key] || 0)
  })
  const officeCompareSpec = {
    chartType: rankingChartType,
    title: `各${compareLevelLabel}${rankingMetricLabel}排序`,
    columns: ['名称', actualMetric?.label || actualMetric?.column || '完成', taskMetric?.label || taskMetric?.column || '任务', remainMetric?.label || remainMetric?.column || '剩余', rateMetric.label || rateMetric.column || '达成率', '标签'].filter(Boolean),
    rows: officeCompareRows,
    sortColumn: rankingMetricLabel,
    lowFirst: isNegativeRankingQuestion(),
  }
  return {
    dataset,
    analysisMode: isSingleFocus ? 'detail' : 'comparative',
    focusName: focusNode?.name || '',
    isSingleFocus,
    kpis: kpis.slice(0, 6),
    offices,
    compareLevelLabel,
    detailLevelLabel,
    officeCompareSpec,
    officeCompareText: isNegativeRankingQuestion()
      ? `${worstOffice ? `${worstOffice.name}达成率最低，为${worstOffice.rateLabel}` : ''}${bestOffice ? `；最高为${bestOffice.name}，${bestOffice.rateLabel}` : ''}。按低达成率优先展示，便于定位承压节点。`
      : `${bestOffice ? `${bestOffice.name}${rankingMetricLabel}最高，为${findOfficeMetricValueByLabel(bestOffice, rankingMetricLabel) || '-'}` : ''}${worstOffice ? `；${worstOffice.name}${rankingMetricLabel}最低，为${findOfficeMetricValueByLabel(worstOffice, rankingMetricLabel) || '-'}` : ''}。一行一个同层级对象，对齐展示金额和进度条。`,
    summary: isNegativeRankingQuestion()
      ? `本次结果覆盖 ${offices.length} 个${compareLevelLabel}，已按低达成率优先排序。${worstOffice ? `${worstOffice.name}当前完成最弱，达成率${worstOffice.rateLabel}` : ''}${bestOffice ? `；最高为${bestOffice.name}，达成率${bestOffice.rateLabel}` : ''}。`
      : `本次结果覆盖 ${offices.length} 个${compareLevelLabel}。${bestOffice ? `${bestOffice.name}${rankingMetricLabel}最高，为${findOfficeMetricValueByLabel(bestOffice, rankingMetricLabel) || '-'}` : ''}${worstOffice ? `；${worstOffice.name}${rankingMetricLabel}最低，为${findOfficeMetricValueByLabel(worstOffice, rankingMetricLabel) || '-'}` : ''}。`,
    riskTone: riskCount ? 'danger' : 'good',
    riskLabel: riskCount ? `风险 ${riskCount} 个` : '整体可控',
  }
}

const getBusinessMetricCards = (dataset) => {
  const model = getDatasetTreeModel(dataset)
  if (!model?.levelSections?.length) return []
  const config = model.config || getDatasetReportConfig(dataset)
  const cards = []
  ;(config.metrics || []).forEach((metric) => {
    const value = model.rootMetrics?.[metric.key]
    if (value !== null && value !== undefined) {
      cards.push({ label: metric.label || metric.column || metric.key, value: formatMetricByDefinition(value, metric, dataset) })
    }
  })
  model.levelSections.slice(0, 2).forEach((section) => {
    cards.push({ label: `${section.levelName}数量`, value: formatDisplayValue(section.nodes.length) })
  })
  return cards.slice(0, 6)
}

const buildLayeredBusinessCharts = (dataset) => {
  const model = getDatasetTreeModel(dataset)
  if (!model?.levelSections?.length) return []
  const config = model.config || getDatasetReportConfig(dataset)
  const taskMetric = config.metrics?.find(item => item.key === 'task')
  const actualMetric = config.metrics?.find(item => item.key === 'actual')
  const rateMetric = config.metrics?.find(item => item.key === 'rate') || config.metrics?.find(item => item.format === 'percent')
  if (!rateMetric) return []
  const requestedLevels = getRequestedLevelValues(getQuestionText(), config)

  return model.levelSections
    .filter(section => (
      !requestedLevels.length
      || requestedLevels.some(value => section.levelValues?.includes(value) || section.levelName?.includes(value))
    ))
    .map((section) => {
      const rows = section.nodes
        .map(node => ({
          名称: node.name,
          [taskMetric?.label || taskMetric?.column || '目标']: toNumber(node.raw?.[taskMetric?.column]) ?? 0,
          [actualMetric?.label || actualMetric?.column || '完成']: toNumber(node.raw?.[actualMetric?.column]) ?? 0,
          [rateMetric?.label || rateMetric?.column || '达成率']: toNumber(node.raw?.[rateMetric?.column]) ?? 0,
          signalTone: section.riskNodes.some(item => item.id === node.id) ? 'danger' : section.topNodes.some(item => item.id === node.id) ? 'good' : 'neutral',
        }))
        .filter(row => row.名称)
        .sort((a, b) => {
          const key = rateMetric.label || rateMetric.column || '达成率'
          return isNegativeRankingQuestion()
            ? (a[key] || 0) - (b[key] || 0)
            : (b[key] || 0) - (a[key] || 0)
        })
        .slice(0, 12)
      if (!rows.length) return null
      const titlePrefix = section.trackNames.length ? `${section.trackNames.join(' / ')}：` : ''
      const rateFocused = requestedLevels.length || isRateRankingQuestion()
      const columns = rateFocused
        ? ['名称', rateMetric?.label || rateMetric?.column].filter(Boolean)
        : [
            '名称',
            taskMetric?.label || taskMetric?.column,
            actualMetric?.label || actualMetric?.column,
            rateMetric?.label || rateMetric?.column,
          ].filter(Boolean)
      return {
        chartType: rateFocused ? 'horizontalRateBar' : taskMetric && actualMetric ? 'combo' : 'bar',
        title: `${titlePrefix}${section.levelName}完成情况`,
        columns,
        rows,
        dataset,
        lowFirst: isNegativeRankingQuestion(),
      }
    })
    .filter(Boolean)
}

const inferChartSpec = (dataset) => {
  const rows = dataset?.rows || []
  if (!rows.length) return null

  const layeredCharts = buildLayeredBusinessCharts(dataset)
  if (layeredCharts.length) return layeredCharts[0]

  const labelColumn = getLabelColumn(dataset)
  const numericColumns = getNumericColumns(dataset)
  if (!labelColumn && !numericColumns.length) return null

  const firstRow = rows[0] || {}
  const nameText = `${dataset?.dataset_name || ''} ${(dataset?.analysis || '').slice(0, 80)}`

  if (rows.length === 1) {
    if (numericColumns.length > 0) {
      return {
        chartType: 'metric',
        title: dataset?.dataset_name || '关键指标',
        value: formatValueByColumn(firstRow[numericColumns[0]], numericColumns[0]),
        label: numericColumns[0],
      }
    }
    if (labelColumn) {
      return {
        chartType: 'metric',
        title: dataset?.dataset_name || '关键指标',
        value: formatDisplayValue(firstRow[labelColumn]),
        label: labelColumn,
      }
    }
  }

  if (/日期|时间/.test(labelColumn || '') && numericColumns.length > 0) {
    return {
      chartType: 'trend',
      title: '趋势组合图',
      columns: [labelColumn, ...numericColumns.slice(0, 2)],
      rows,
    }
  }

  if (/Top|TOP|股票|排名/i.test(nameText) || rows.length > 6) {
    return {
      chartType: 'bar',
      title: 'Top 结果分布',
      columns: [labelColumn, numericColumns[0]].filter(Boolean),
      rows,
    }
  }

  if (numericColumns.length > 0) {
    return {
      chartType: /城市|佣金|分布|占比/i.test(nameText) ? 'pie' : 'bar',
      title: /城市|佣金|分布|占比/i.test(nameText) ? '分类占比' : '分类对比',
      columns: [labelColumn, numericColumns[0]].filter(Boolean),
      rows,
    }
  }

  return null
}

const buildSingleRowMetricCharts = (dataset) => {
  const rows = dataset?.rows || []
  if (rows.length !== 1) return []

  const numericColumns = getNumericColumns(dataset)
  const firstRow = rows[0] || {}
  const datasetName = dataset?.dataset_name || '结果图表'
  const charts = []

  if (numericColumns.length >= 2) {
    charts.push({
      chartType: 'bar',
      title: '关键指标对比',
      columns: ['指标', '数值'],
      rows: numericColumns.slice(0, 6).map(column => ({
        指标: column,
        数值: Number(firstRow[column]) || 0,
      })),
    })
  }

  const completedKey = numericColumns.find(column => /开单|完成|达成|实际|已完成/i.test(column))
  const remainKey = numericColumns.find(column => /剩余|未完成|差额|缺口/i.test(column))
  if (completedKey && remainKey) {
    charts.push({
      chartType: 'pie',
      title: '完成与剩余结构',
      columns: ['分类', '数值'],
      rows: [
        { 分类: completedKey, 数值: Math.max(0, Number(firstRow[completedKey]) || 0) },
        { 分类: remainKey, 数值: Math.max(0, Number(firstRow[remainKey]) || 0) },
      ],
    })
  }

  return charts.map((chart, index) => ({
    key: `${dataset?.dataset_id || datasetName}-single-${index}`,
    caption: index === 0 ? '核心图表' : `衍生图表 ${index}`,
    dataset,
    metricCards: getMetricCards(dataset),
    chartSpec: chart,
  }))
}

const hasChartRows = (chartSpec) => Array.isArray(chartSpec?.rows) && chartSpec.rows.length > 0

const getReportSpecCharts = (dataset) => (
  Array.isArray(dataset?.report_spec?.charts)
    ? dataset.report_spec.charts.filter(Boolean)
    : []
)

const dedupeChartSpecs = (charts = []) => {
  const seen = new Set()
  const result = []
  charts.filter(Boolean).forEach((chart) => {
    const columns = Array.isArray(chart.columns) ? chart.columns.join('|') : ''
    const key = `${chart.chartType || ''}-${chart.title || ''}-${columns}`
    if (seen.has(key)) return
    seen.add(key)
    result.push(chart)
  })
  return result
}

const getDatasetChartSpecs = (dataset, { includeFallback = true } = {}) => {
  if (!dataset || typeof dataset !== 'object') return []
  if (dataset?.report_spec?.scope?.focusNodeIsLeaf) {
    const value = []
    datasetChartSpecCache.set(dataset, { key: [getQuestionText(), includeFallback ? 'fallback' : 'strict', 'leaf-focus-none'].join('|'), value })
    return value
  }
  const cacheKey = [
    getQuestionText(),
    includeFallback ? 'fallback' : 'strict',
    canUseFeature('ask_chart_auto_infer') ? 'infer-on' : 'infer-off',
  ].join('|')
  const cached = datasetChartSpecCache.get(dataset)
  if (cached?.key === cacheKey) return cached.value
  const specCharts = getReportSpecCharts(dataset)
  const value = specCharts.length
    ? dedupeChartSpecs(specCharts)
    : (!includeFallback || !canUseFeature('ask_chart_auto_infer')) ? []
    : dedupeChartSpecs([
    ...buildLayeredBusinessCharts(dataset),
    inferChartSpec(dataset),
    ...buildSingleRowMetricCharts(dataset).map(item => item.chartSpec),
  ])
  datasetChartSpecCache.set(dataset, { key: cacheKey, value })
  return value
}

const buildReportTableBlocks = (datasets = []) => {
  return (datasets || [])
    .filter(dataset => Array.isArray(dataset?.rows) && dataset.rows.length > 0 && Array.isArray(dataset?.columns) && dataset.columns.length > 0)
    .slice(0, 3)
    .map((dataset, index) => {
      const labelColumn = getLabelColumn(dataset)
      const numericColumns = getNumericColumns(dataset)
      const pathColumns = (dataset.columns || []).filter(column => /组织路径|归属组织|组织归属|管理链路|路径|上级名称|战区|片区|行业部/.test(column))
      const prioritizedColumns = [
        labelColumn,
        ...pathColumns,
        ...numericColumns,
        ...(dataset.columns || []),
      ].filter(Boolean)
      const columns = Array.from(new Set(prioritizedColumns)).slice(0, 6)
      const title = dataset.rows.length > 6
        ? `${dataset.dataset_name} 结果明细表`
        : `${dataset.dataset_name} 关键结果表`
      const description = dataset.rows.length > 6
        ? '补充展示图表对应的原始数据明细，方便继续核对与下钻。'
        : '提炼当前报告里的关键字段与结果值，便于快速核对。'

      return {
        key: `${dataset.dataset_id || index}-${dataset.dataset_name || 'table'}`,
        dataset,
        title,
        description,
        columns,
        rows: dataset.rows,
      }
    })
}

const resultPreviews = computed(() => (
  datasetResults.value.slice(0, 4).map((dataset, index) => {
    const chartSpecs = getDatasetChartSpecs(dataset)

    return {
      key: `${dataset.dataset_id || index}-${dataset.dataset_name || 'dataset'}`,
      caption: index === 0 ? '主结果视图' : '结果视图',
      dataset,
      metricCards: getMetricCards(dataset),
      chartSpec: chartSpecs[0] || null,
      extraCharts: chartSpecs.slice(1),
    }
  })
))

const sideReportCharts = computed(() => (
  latestDatasets.value
    .slice(0, 3)
    .flatMap((dataset, datasetIndex) => {
      const chartSpecs = getDatasetChartSpecs(dataset)
      return chartSpecs.slice(0, 3).map((chartSpec, chartIndex) => ({
        key: `side-report-chart-${dataset.dataset_id || datasetIndex}-${chartIndex}`,
        caption: chartSpec.title || `图表 ${chartIndex + 1}`,
        dataset,
        chartSpec,
      }))
    })
))

const reportDialogCharts = computed(() => {
  const sourceItems = reportViewerVisible.value
    ? reportViewerDatasets.value.slice(0, 4).flatMap((dataset, index) => {
        const chartSpecs = getDatasetChartSpecs(dataset)
        return chartSpecs.map((chartSpec, chartIndex) => ({
          key: `${dataset.dataset_id || index}-${dataset.dataset_name || 'dataset'}-${chartIndex}`,
          caption: chartSpec.title || (chartIndex === 0 ? '主结果视图' : `图表 ${chartIndex + 1}`),
          dataset,
          metricCards: getMetricCards(dataset),
          chartSpec,
        }))
      })
    : resultPreviews.value.flatMap(item => (
        item?.dataset ? [item, ...buildSingleRowMetricCharts(item.dataset)] : [item]
      ))

  const deduped = []
  const seen = new Set()
  sourceItems.forEach((item) => {
    if (!item?.chartSpec) return
    const key = `${item.key}-${item.chartSpec.chartType}-${item.chartSpec.title || ''}`
    if (seen.has(key)) return
    seen.add(key)
    deduped.push(item)
  })
  return deduped
})

const reportDialogMetricCards = computed(() => {
  const source = reportSourceDatasets.value
  const drillReport = activeBusinessDrillReport.value
  if (drillReport && isCollectionAnswerMode(drillReport)) {
    return buildCollectionMetricCards(drillReport)
  }
  if (drillReport?.kpis?.length) {
    const cards = drillReport.isSingleFocus
      ? drillReport.kpis.slice(0, 4).map(item => ({
          label: item.label || item.key || '',
          value: item.value ?? item.displayValue ?? formatDisplayValue(item.value),
        }))
      : decorateMetricCards(drillReport.kpis, drillReport.offices).slice(0, 8)
    return drillReport.isSingleFocus ? enrichSingleOrgMetricCards(cards, drillReport) : cards
  }
  return (
    (reportViewerVisible.value
      ? (reportViewerDatasets.value[0] ? getMetricCards(reportViewerDatasets.value[0]) : [])
      : resultPreviews.value[0]?.metricCards
    ) || []
  )
})

const reportTableBlocks = computed(() => (
  buildReportTableBlocks(reportSourceDatasets.value)
))

const reportSourceDatasets = computed(() => (
  reportViewerVisible.value ? reportViewerDatasets.value : latestDatasets.value
))

const findBusinessDrillReport = (datasets = []) => {
  const reports = (datasets || [])
    .map(buildBusinessDrillReport)
    .filter(Boolean)
  if (!reports.length) return null
  // 修 4（渲染侧优先级）：优先使用有明确 answerMode 的报告。
  // 用户问 ranking/TopN 问题时，ranking 报告的 offices 是客户经理层级；
  // 若无优先级，dataset_results[0] 若为 Overview 报告（行业部层级）会被误取，
  // 导致 offices 全是行业部/片区节点而不是客户经理。
  const INTENT_MODES = ['ranking', 'filter', 'drilldown', 'comparison']
  const intentful = reports.find(r => INTENT_MODES.includes(String(r.answerMode || '').trim()))
  if (intentful) return intentful
  const withOffices = reports.find(r => Array.isArray(r.offices) && r.offices.length > 0)
  if (withOffices) return withOffices
  return reports[0]
}

const businessDrillReport = computed(() => (
  findBusinessDrillReport(latestDatasets.value)
))

const activeBusinessDrillReport = computed(() => (
  reportViewerVisible.value
    ? findBusinessDrillReport(reportViewerDatasets.value)
    : businessDrillReport.value
))

const sideBusinessSummaryText = computed(() => (
  businessDrillReport.value?.primaryAnswer?.text
  || businessDrillReport.value?.filterAnswer?.text
  || businessDrillReport.value?.summary
  || ''
))

const sideBusinessMetricCards = computed(() => (
  businessDrillReport.value
    ? (
        isCollectionAnswerMode(businessDrillReport.value)
          ? buildCollectionMetricCards(businessDrillReport.value)
          : businessDrillReport.value.isSingleFocus
          ? enrichSingleOrgMetricCards(
              businessDrillReport.value.kpis.slice(0, 4).map(item => ({
                label: item.label || item.key || '',
                value: item.value ?? item.displayValue ?? formatDisplayValue(item.value),
              })),
              businessDrillReport.value,
            )
          : decorateMetricCards(businessDrillReport.value.kpis, businessDrillReport.value.offices).slice(0, 8)
      )
    : []
))

const dialogBusinessDrillReport = computed(() => activeBusinessDrillReport.value)

const dialogCoreConclusion = computed(() => {
  const report = dialogBusinessDrillReport.value
  if (report?.answerMode === 'ranking') {
    const metricContext = getReportMetricContext(report)
    const leader = metricContext.best
    const follower = metricContext.ranked[1] || null
    if (leader) {
      const leaderText = findOfficeMetricValueByLabel(leader, metricContext.metricLabel) || '-'
      const followerText = follower ? (findOfficeMetricValueByLabel(follower, metricContext.metricLabel) || '-') : ''
      const diffText = metricContext.diff ? `，较${follower?.name}${metricContext.lowFirst ? '更低' : '更高'}${metricContext.diff}` : ''
      return `${leader.name}当前位于首位，${metricContext.metricLabel}${leaderText}${follower ? `${diffText}` : ''}；建议继续下钻定位差距来自哪些下级单元。`
    }
  }
  if (report?.primaryAnswer?.text) return report.primaryAnswer.text
  if (report?.filterAnswer?.text) return report.filterAnswer.text
  const offices = report?.offices || []
  if (offices.length >= 2) {
    const metricLabel = getSortMetricLabel(report, '达成率')
    const lowFirst = (getReportSortSpec(report).direction || '').toLowerCase() === 'asc'
    const ranked = sortOfficesByAnswerMetric(
      offices.filter(item => getMetricValueFromOffice(item, metricLabel) !== null),
      report,
    )
    const leader = ranked[0]
    const follower = ranked[1]
    if (leader && follower) {
      const leaderValue = getMetricValueFromOffice(leader, metricLabel)
      const followerValue = getMetricValueFromOffice(follower, metricLabel)
      const diff = leaderValue !== null && followerValue !== null
        ? Math.abs(leaderValue - followerValue)
        : null
      const diffText = diff === null
        ? ''
        : isRateMetricLabel(metricLabel)
        ? `${diff.toFixed(2).replace(/\.?0+$/, '')} 个百分点`
        : formatAmount(diff)
      const relationText = lowFirst ? '更低' : '更高'
      return `${leader.name}当前位于首位，较${follower.name}${metricLabel}${relationText}${diffText ? ` ${diffText}` : ''}；建议继续下钻定位差距来自哪些下级单元。`
    }
  }
  const reportText = String(reportViewerReport.value || latestReport.value || '').trim()
  const match = reportText.match(/(?:核心结论|结论)[:：]?\s*([^。\n]{12,120}。?)/)
  if (match?.[1]) return match[1].trim()
  return report?.summary || ''
})

const dialogReportStageTitle = computed(() => {
  const report = dialogBusinessDrillReport.value
  if (!report) return '下钻分析'
  if (report.answerMode === 'ranking') return isLeafOnlyReport(report) ? `${report.compareLevelLabel}排名列表` : `${report.compareLevelLabel}排名结果`
  if (report.answerMode === 'filter') return isLeafOnlyReport(report) ? `${report.compareLevelLabel}命中列表` : `${report.compareLevelLabel}命中结果`
  if (report.answerMode === 'drilldown') return `${report.compareLevelLabel}下钻分析`
  return isLeafOnlyReport(report) ? `${report.compareLevelLabel}结果列表` : `${report.compareLevelLabel}下钻分析`
})

const getOfficeMetricText = (office, type) => getOfficeKpiLabel(office, type) || '-'

const buildComparisonMetricTable = (offices = []) => {
  if (!offices.length) return ''
  const displayOffices = offices.length <= 4
    ? offices
    : [offices[0], offices[1], offices[offices.length - 2], offices[offices.length - 1]]
        .filter((item, index, list) => item && list.findIndex(row => row.name === item.name) === index)
  const header = ['指标', ...displayOffices.map(item => item.name)]
  const rows = [
    ['总任务金额', ...displayOffices.map(item => getOfficeMetricText(item, 'task'))],
    ['已完成金额', ...displayOffices.map(item => getOfficeMetricText(item, 'actual'))],
    ['整体达成率', ...displayOffices.map(item => getOfficeMetricText(item, 'rate'))],
    ['剩余缺口金额', ...displayOffices.map(item => getOfficeMetricText(item, 'remain'))],
  ]
  const table = [
    `| ${header.join(' | ')} |`,
    `| ${header.map(() => '---').join(' | ')} |`,
    ...rows.map(row => `| ${row.join(' | ')} |`),
  ].join('\n')
  const levelLabel = dialogBusinessDrillReport.value?.compareLevelLabel || businessDrillReport.value?.compareLevelLabel || '对象'
  const note = offices.length > 4 ? `\n\n本次对象较多，表内展示最高/次高/次低/最低摘要，完整 ${offices.length} 个${levelLabel}见下方对比分析表。` : ''
  return `${table}${note}`
}

const buildRankMetricTable = (items = [], title = '对象') => {
  if (!items.length) return ''
  return [
    `| ${title} | 任务 | 完成 | 达成率 | 缺口 |`,
    '| --- | ---: | ---: | ---: | ---: |',
    ...items.map(item => (
      `| ${item.name} | ${getOfficeMetricText(item, 'task')} | ${getOfficeMetricText(item, 'actual')} | ${getOfficeMetricText(item, 'rate')} | ${getOfficeMetricText(item, 'remain')} |`
    )),
  ].join('\n')
}

const getQuestionTargetLevel = (questionText = getQuestionText()) => {
  const hit = requestedLevelTokens.find(token => token && questionText.includes(token))
  return hit || ''
}

const getDirectAnswerFromRows = (report) => {
  const dataset = report?.dataset
  const rows = Array.isArray(dataset?.rows) ? dataset.rows : []
  if (!rows.length) return null
  const questionText = getQuestionText()
  const targetLevel = getQuestionTargetLevel(questionText)
  if (!targetLevel) return null
  const columns = dataset?.columns || Object.keys(rows[0] || {})
  const levelColumn = findColumn(columns, column => /层级|级别|level/i.test(column))
  const nameColumn = findColumn(columns, column => /节点名称|名称|战区|城市站|组织/i.test(column)) || columns[0]
  const rateColumn = findColumn(columns, column => isRateColumn(column)) || '达成率'
  const taskColumn = findColumn(columns, column => /总任务|任务金额|目标/i.test(column) && !/剩余|缺口|差额/i.test(column))
  const actualColumn = findColumn(columns, column => /年度开单|开单|完成|实际|销售/i.test(column))
  const remainColumn = findColumn(columns, column => /剩余|缺口|差额|remain/i.test(column))
  const candidates = rows
    .filter(row => {
      const levelText = String(row?.[levelColumn] || '')
      const nameText = String(row?.[nameColumn] || '')
      return levelText.includes(targetLevel) || nameText.includes(targetLevel)
    })
    .map(row => ({
      name: row?.[nameColumn] || row?.节点名称 || row?.名称 || '-',
      level: targetLevel,
      rate: toNumber(row?.[rateColumn]),
      rateLabel: rateColumn ? formatBusinessValueByColumn(row?.[rateColumn], rateColumn, dataset) : '-',
      task: toNumber(row?.[taskColumn]),
      taskLabel: taskColumn ? formatBusinessValueByColumn(row?.[taskColumn], taskColumn, dataset) : '-',
      actual: toNumber(row?.[actualColumn]),
      actualLabel: actualColumn ? formatBusinessValueByColumn(row?.[actualColumn], actualColumn, dataset) : '-',
      remain: toNumber(row?.[remainColumn]),
      remainLabel: remainColumn ? formatBusinessValueByColumn(row?.[remainColumn], remainColumn, dataset) : '-',
    }))
    .filter(item => item.name && item.rate !== null)
  if (!candidates.length) return null
  const lowFirst = isNegativeRankingQuestion(questionText)
  const winner = [...candidates].sort((left, right) => (
    lowFirst ? (left.rate || 0) - (right.rate || 0) : (right.rate || 0) - (left.rate || 0)
  ))[0]
  const metricText = /线下/.test(questionText) ? '线下业务' : '当前口径'
  const directionText = lowFirst ? '完成最弱' : '完成最好'
  const riskText = winner.rate !== null && winner.rate < 60
    ? `但达成率低于60%红线，仍需关注任务缺口和后续转化。`
    : '当前未触发60%红线。'
  return {
    ...winner,
    targetLevel,
    sentence: `${metricText}${directionText}的${targetLevel}是${winner.name}，达成率${winner.rateLabel}，总任务${winner.taskLabel}，实际开单${winner.actualLabel}，任务缺口${winner.remainLabel}；${riskText}`,
  }
}

const getRateDistribution = (items = []) => {
  const source = items.filter(item => item?.rate !== null && item?.rate !== undefined)
  const total = source.length || 0
  const buckets = [
    { label: '20%以下', count: 0, matcher: rate => rate < 20 },
    { label: '20%-40%', count: 0, matcher: rate => rate >= 20 && rate < 40 },
    { label: '40%以上', count: 0, matcher: rate => rate >= 40 },
  ]
  source.forEach((item) => {
    const bucket = buckets.find(part => part.matcher(Number(item.rate)))
    if (bucket) bucket.count += 1
  })
  return buckets.map(item => ({
    ...item,
    pct: total ? `${Math.round(item.count / total * 100)}%` : '0%',
  }))
}

const buildRateDistributionText = (items = []) => (
  getRateDistribution(items).map(item => `${item.label}：${item.count}个（${item.pct}）`).join('；')
)

const getTrendProgressText = (report) => {
  const kpis = Array.isArray(report?.kpis) ? report.kpis : []
  const trendItems = kpis
    .filter(item => /同比|环比|较上期|较同期|增长|变化/i.test(`${item?.label || ''}${item?.key || ''}`))
    .map(item => `${item.label || item.key}：${item.value ?? item.displayValue ?? '-'}`)
  if (trendItems.length) return trendItems.join('；')
  return '本次 SQL 结果未返回同比/环比字段，当前以达成率、缺口和分布判断进度；建议后续在数据集中补充同期/上期指标列。'
}

const getPressureDiagnosis = (item, detailLabel = '下级节点') => {
  if (!item) return ''
  const task = toNumber(getOfficeMetricText(item, 'task'))
  const actual = toNumber(getOfficeMetricText(item, 'actual'))
  const remain = toNumber(getOfficeMetricText(item, 'remain'))
  const rate = toNumber(getOfficeMetricText(item, 'rate'))
  const detailCount = Number(item.childCount || item.detailRows?.length || 0)
  const signals = []
  if (task !== null && remain !== null && task > 0 && remain / task >= 0.5) {
    signals.push('任务体量或缺口压力偏大')
  }
  if (rate !== null && rate < 20) {
    signals.push('整体转化进度偏慢')
  }
  if (actual !== null && task !== null && task > 0 && actual / task < 0.25) {
    signals.push('客户转化或项目落单不足')
  }
  if (detailCount > 0) {
    signals.push(`需继续下钻${detailCount}个${detailLabel}确认项目阶段`)
  }
  return signals.length
    ? `${item.name}可能由${signals.join('、')}共同造成，优先用下级明细验证。`
    : `${item.name}需要补充项目阶段、客户转化和资源投入字段后再做归因。`
}

const buildBusinessNarrativeSections = (report) => {
  const offices = report?.offices || []
  if (!report || !offices.length) return []
  if (report.answerMode === 'ranking') {
    const metricContext = getReportMetricContext(report)
    const configuredTopN = getConfiguredTopN(report)
    const ranked = metricContext.ranked.length ? metricContext.ranked : offices
    const topItems = ranked.slice(0, configuredTopN)
    const bottomItems = [...ranked].reverse().slice(0, configuredTopN)
    const riskCount = offices.filter(item => item.tone === 'danger').length
    const metricTable = buildComparisonMetricTable(ranked)
    return [
      {
        title: '一、核心结论',
        body: [
          report.primaryAnswer?.text || report.summary,
          metricContext.best && metricContext.worst && metricContext.best.name !== metricContext.worst.name
            ? `${metricContext.best.name}${metricContext.metricLabel}${findOfficeMetricValueByLabel(metricContext.best, metricContext.metricLabel) || '-'}位于榜首；${metricContext.worst.name}${metricContext.metricLabel}${findOfficeMetricValueByLabel(metricContext.worst, metricContext.metricLabel) || '-'}位于末位${metricContext.diff ? `，首尾相差${metricContext.diff}` : ''}。`
            : '',
          riskCount
            ? `风险信号：当前结果中有${riskCount}个对象处于低达成风险，排名领先不代表进度无风险。`
            : '风险信号：当前结果内暂无明显低达成风险对象。',
        ].filter(Boolean).join('\n'),
      },
      {
        title: '二、关键指标与排序结果',
        body: [
          metricTable,
          `当前按${metricContext.metricLabel}${metricContext.lowFirst ? '由低到高' : '由高到低'}排序；右侧列表、图表与摘要已统一使用这一指标。`,
        ].filter(Boolean).join('\n\n'),
      },
      {
        title: `三、${report.compareLevelLabel}Top${configuredTopN}/末${configuredTopN}`,
        body: [
          `Top${configuredTopN}：`,
          buildRankMetricTable(topItems, report.compareLevelLabel || '对象'),
          '',
          `末${configuredTopN}：`,
          buildRankMetricTable(bottomItems, report.compareLevelLabel || '对象'),
        ].filter(Boolean).join('\n\n'),
      },
      {
        title: '四、后续动作',
        body: [
          metricContext.best ? `榜首复盘：优先复盘${metricContext.best.name}在${metricContext.metricLabel}上的领先做法，并核对其达成率与缺口是否同步健康。` : '',
          metricContext.worst ? `末位下钻：围绕${metricContext.worst.name}继续下钻${report.detailLevelLabel}，确认是任务体量、项目阶段还是客户转化拖累。` : '',
          '统一口径：排名按问题中的指标排序，风险继续看达成率与缺口，避免把“排位”和“健康度”混为一谈。',
        ].filter(Boolean).join('\n'),
      },
    ]
  }
  const ranked = [...offices].filter(item => item.rate !== null).sort((a, b) => (b.rate || 0) - (a.rate || 0))
  const best = ranked[0] || offices[0]
  const worst = ranked[ranked.length - 1] || offices[offices.length - 1]
  const configuredTopN = getConfiguredTopN(report)
  const topItems = ranked.slice(0, configuredTopN)
  const bottomItems = [...ranked].reverse().slice(0, configuredTopN)
  const directAnswer = getDirectAnswerFromRows(report)
  const diff = best?.rate !== null && worst?.rate !== null
    ? Math.abs((best.rate || 0) - (worst.rate || 0)).toFixed(2).replace(/\.?0+$/, '')
    : ''
  const visibleNames = offices.length <= 4
    ? offices.map(item => item.name).join('、')
    : `${offices.length} 个${report.compareLevelLabel}`
  const riskOffices = offices.filter(item => item.tone === 'danger')
  const riskText = riskOffices.length
    ? `${riskOffices.slice(0, 3).map(item => item.name).join('、')}处于低达成风险${riskOffices.length > 3 ? `等 ${riskOffices.length} 个对象` : ''}`
    : '当前同层级对象暂无低达成风险'
  const distributionText = buildRateDistributionText(offices)
  const trendText = getTrendProgressText(report)
  const topBottomTable = [
    `Top${configuredTopN}：`,
    buildRankMetricTable(topItems, report.compareLevelLabel || '对象'),
    '',
    `末${configuredTopN}：`,
    buildRankMetricTable(bottomItems, report.compareLevelLabel || '对象'),
  ].filter(Boolean).join('\n\n')

  if (report.isSingleFocus) {
    const focusName = report.focusName || '当前组织'
    const counts = getSingleOrgCounts(report)
    const rankContext = getSingleOrgRankContext(report)
    const overallRate = getReportKpiText(report, 'rate')
    const tableRows = offices.length <= 6
      ? offices
      : [
          ...ranked.slice(0, configuredTopN),
          ...ranked.slice(-Math.min(2, configuredTopN)),
        ].filter((item, index, list) => item && list.findIndex(row => row.name === item.name) === index)
    const comparisonRows = tableRows.map((office) => {
      const diffValue = office.rate !== null && toNumber(overallRate) !== null ? (office.rate - toNumber(overallRate)) : null
      const diffText = diffValue === null
        ? '-'
        : `${diffValue >= 0 ? '高于大盘' : '低于大盘'} ${Math.abs(diffValue).toFixed(2).replace(/\.?0+$/, '')}pct`
      return `| ${office.name} | ${office.rateLabel} | ${diffText} | ${office.tag || '-'} |`
    })
    const comparisonTable = [
      `数据为${focusName}下${counts.directCount}个${counts.directLabel}摘要，完整明细见下方附表。`,
      '',
      '| 对象 | 达成率 | 与大盘对比 | 标签 |',
      '| --- | --- | --- | --- |',
      ...comparisonRows,
    ].join('\n')
    return [
      {
        title: `一、${focusName}核心结论`,
        body: [
          directAnswer
            ? `1. ${directAnswer.sentence}`
            : `1. 当前进度：${getSingleOrgConclusion(report)}`,
          rankContext.diff
            ? `2. 头尾差异：${rankContext.best.name}达成率${rankContext.best.rateLabel}领跑，${rankContext.worst.name}达成率${rankContext.worst.rateLabel}承压，首尾差距${rankContext.diff}个百分点。`
            : report.summary,
          `3. 风险信号：${riskText}；${distributionText}。`,
        ].filter(Boolean).slice(0, 3).join('\n'),
      },
      {
        title: `二、${focusName}关键指标与二级拆解`,
        body: [
          `事业群/主体大盘：总任务金额 ${getReportKpiText(report, 'task')}，年度开单金额 ${getReportKpiText(report, 'actual')}，整体达成率 ${overallRate}，剩余任务金额 ${getReportKpiText(report, 'remain')}。`,
          `同比/环比进度：${trendText}`,
          `达成率分布：${distributionText}`,
          comparisonTable,
        ].filter(Boolean).join('\n\n'),
      },
      {
        title: `三、${counts.directLabel}Top${configuredTopN}/末${configuredTopN}对比`,
        body: topBottomTable,
      },
      {
        title: '四、结构看板与问题溯源',
        body: [
          `标杆分析：${rankContext.best ? `${rankContext.best.name}是当前标杆，任务 ${getOfficeMetricText(rankContext.best, 'task')}，完成 ${getOfficeMetricText(rankContext.best, 'actual')}，达成率 ${rankContext.best.rateLabel}；建议复盘其目标拆解、客户推进和项目转化节奏。` : '当前未识别稳定标杆。'}`,
          `压力节点：${rankContext.worst ? getPressureDiagnosis(rankContext.worst, counts.detailLabel) : '当前未识别明显压力节点。'}`,
          `分层归因：事业群层面关注头部贡献与尾部拖累是否过度分化；${counts.directLabel}层面重点比较标杆和末位在任务体量、项目阶段、客户转化和资源投入上的差异。`,
        ].join('\n\n'),
      },
      {
        title: '五、动作落地',
        body: [
          rankContext.best ? `标杆经验推广：由${rankContext.best.name}输出可复制动作清单，两周内同步给达成率低于20%的${counts.directLabel}。` : '',
          rankContext.worst ? `压力节点帮扶：围绕${rankContext.worst.name}建立下钻清单，责任方为业务负责人+经营分析；输出项目阶段、客户转化、缺口金额三张明细表。` : '',
          `整体优化：按${counts.directLabel}建立红黄绿看板，低于20%周度复盘，20%-40%专项推进，高于40%沉淀打法并横向复制。`,
        ].filter(Boolean).join('\n'),
      },
    ]
  }
  return [
    {
      title: '一、核心结论',
      body: [
        directAnswer
          ? `1. ${directAnswer.sentence}`
          : diff
          ? `1. 当前对比覆盖${visibleNames}，${best.name}达成率${best.rateLabel}领先，${worst.name}达成率${worst.rateLabel}承压，首尾差${diff}个百分点。`
          : `1. ${report.summary}`,
        `2. 头部/尾部差异：Top${configuredTopN}为${topItems.map(item => `${item.name}(${item.rateLabel})`).join('、') || '暂无'}；末${configuredTopN}为${bottomItems.map(item => `${item.name}(${item.rateLabel})`).join('、') || '暂无'}。`,
        `3. 核心风险信号：${riskText}；${distributionText}。`,
      ].join('\n'),
    },
    {
      title: '二、关键指标与分层拆解',
      body: [
        buildComparisonMetricTable(offices),
        `同比/环比进度：${trendText}`,
        `分布看板：${distributionText}`,
      ].join('\n\n'),
    },
    {
      title: `三、${report.compareLevelLabel}Top${configuredTopN}/末${configuredTopN}对比`,
      body: topBottomTable,
    },
    {
      title: '四、结构看板与问题溯源',
      body: [
        `标杆分析：${best.name}任务 ${getOfficeMetricText(best, 'task')}，完成 ${getOfficeMetricText(best, 'actual')}，达成率 ${best.rateLabel}；优先复盘其目标拆解、客户推进和项目转化动作。`,
        `压力节点：${getPressureDiagnosis(worst, report.detailLevelLabel)}`,
        `分层归因：事业群层面看头部贡献、尾部拖累和任务分配合理性；${report.compareLevelLabel}层面看任务体量、项目阶段、客户转化和资源投入差异。`,
      ].join('\n\n'),
    },
    {
      title: '五、动作落地',
      body: [
        `标杆经验推广：由${directAnswer?.name || best.name}沉淀关键动作，覆盖${bottomItems.map(item => item.name).join('、') || '低达成节点'}，两周内完成打法复盘和任务拆解。`,
        `压力节点帮扶：围绕${worst.name}下钻${report.detailLevelLabel}，责任方为业务负责人+经营分析；输出项目阶段、客户转化、缺口金额三类问题清单。`,
        `整体优化：按达成率分布配置资源，低于20%节点进入周度专项，20%-40%节点做过程纠偏，高于40%节点提炼可复制打法。`,
      ].join('\n'),
    },
  ]
}

const reportOverviewTitle = computed(() => {
  const drillReport = activeBusinessDrillReport.value
  return drillReport?.isSingleFocus
    ? `${drillReport.focusName || '当前组织'}业绩核心结论`
    : '分析摘要'
})

const reportSummaryBullets = computed(() => {
  const bullets = []
  const sourceDatasets = reportSourceDatasets.value
  const primary = sourceDatasets[0]
  const drillReport = activeBusinessDrillReport.value
  const names = sourceDatasets.map(item => item.dataset_name).filter(Boolean)
  if (drillReport?.isSingleFocus) {
    const counts = getSingleOrgCounts(drillReport)
    const rankContext = getSingleOrgRankContext(drillReport)
    bullets.push(getSingleOrgConclusion(drillReport))
    bullets.push(`覆盖范围：${counts.directCount}个${counts.directLabel}${counts.detailCount ? `，${counts.detailCount}个${counts.detailLabel}` : ''}。`)
    if (rankContext.best && rankContext.worst && rankContext.diff) {
      bullets.push(`${rankContext.best.name}达成率最高，为${rankContext.best.rateLabel}；${rankContext.worst.name}压力最大，为${rankContext.worst.rateLabel}，首尾差距${rankContext.diff}个百分点。`)
    }
    if (names.length) bullets.push(`命中数据集：${names.join('、')}`)
    return bullets.filter(Boolean)
  }
  if (drillReport?.offices?.length) {
    const metricContext = getReportMetricContext(drillReport)
    const best = metricContext.best || drillReport.offices[0]
    const worst = metricContext.worst || drillReport.offices[drillReport.offices.length - 1]
    const riskCount = drillReport.offices.filter(item => item.tone === 'danger').length
    bullets.push(`当前覆盖 ${drillReport.offices.length} 个${drillReport.compareLevelLabel}，先横向比较再下钻${drillReport.detailLevelLabel}。`)
    if (best && worst) {
      bullets.push(metricContext.diff
        ? `${best.name}${metricContext.metricLabel}${findOfficeMetricValueByLabel(best, metricContext.metricLabel) || '-'}领先，${worst.name}${metricContext.metricLabel}${findOfficeMetricValueByLabel(worst, metricContext.metricLabel) || '-'}位于末位，首尾差${metricContext.diff}。`
        : `${best.name}表现靠前，${worst.name}需要优先下钻复核。`)
    }
    bullets.push(riskCount
      ? `风险信号：${riskCount}个${drillReport.compareLevelLabel}处于低达成风险，需按缺口和项目阶段拆解责任。`
      : `风险信号：暂无明显低达成${drillReport.compareLevelLabel}，继续保持周度过程跟踪。`)
    return bullets.filter(Boolean).slice(0, 3)
  }
  if (session.state.question) bullets.push(`原始问题：${session.state.question}`)
  bullets.push(`报告模板：${reportSceneTemplateLabel.value}`)
  if (drillReport) {
    const nextLevelText = drillReport.offices?.some(item => item.drillGroups?.length)
      ? `，再从${drillReport.detailLevelLabel}继续下钻到业务员`
      : ''
    bullets.push(`分析口径：先横向比较 ${drillReport.offices.length} 个${drillReport.compareLevelLabel}，再纵向展开${drillReport.detailLevelLabel}${nextLevelText}。`)
  }
  if (names.length) bullets.push(`命中数据集：${names.join('、')}`)
  if (sourceDatasets.length) {
    const totalRows = sourceDatasets.reduce((sum, item) => sum + Number(item?.row_count || item?.rows?.length || 0), 0)
    bullets.push(`数据结果：共返回 ${sourceDatasets.length} 份结果，累计 ${totalRows} 行数据。`)
  }
  const reviewSummary = primary?.agent3_review?.review_summary
  if (reviewSummary) bullets.push(`SQL 复核结论：${reviewSummary}`)
  const sample = primary?.rows?.[0]
  const columns = primary?.columns || []
  if (!drillReport && sample && columns.length) {
    const snippet = columns.slice(0, 3).map(column => `${column}=${sample[column]}`).join('；')
    if (snippet) bullets.push(`样例结果：${snippet}`)
  }
  if (!bullets.length && (reportViewerReport.value || latestReport.value)) {
    bullets.push('本轮报告已生成，可继续查看下方图表分析与完整解读。')
  }
  return bullets
})

const reportNarrativeSections = computed(() => {
  const raw = String((reportViewerVisible.value ? reportViewerReport.value : latestReport.value) || '').trim()
  if (!raw) return []

  const sections = splitReportSections(raw)

  if (!sections.length) {
    return [{
      title: reportViewerTitle.value || sideReportHeading.value,
      body: normalizeReportMarkdown(raw),
    }]
  }

  return sections
})

const businessNarrativeSections = computed(() => {
  const generated = buildBusinessNarrativeSections(dialogBusinessDrillReport.value || businessDrillReport.value)
  if (generated.length) return generated
  return reportNarrativeSections.value
    .filter(section => !/^业绩分析报告$/.test(section.title))
    .slice(0, 4)
})

// 方法
const renderMd = (text) => marked.parse(text || '')
const renderReportMd = (text) => marked.parse(normalizeReportMarkdown(text))

const normalizeReportMarkdown = (text) => (
  String(text || '')
    .replace(/\r\n/g, '\n')
    .replace(/^#\s+/gm, '## ')
    .replace(/\n---\n/g, '\n\n')
    .replace(/[ \t]+•[ \t]*/g, '\n- ')
    .replace(/^•[ \t]*/gm, '- ')
    .replace(/([。！？；;])\s*(?=##|###)/g, '$1\n\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
)

const splitReportSections = (text) => {
  const normalized = normalizeReportMarkdown(text).replace(/^##\s*业绩分析报告\s*/i, '').trim()
  if (!normalized) return []

  const headingPattern = /^#{2,3}\s+(.+)$/gm
  const matches = Array.from(normalized.matchAll(headingPattern))
  if (!matches.length) {
    return [{ title: '核心结论', body: normalized }]
  }

  const sections = []
  const leading = normalized.slice(0, matches[0].index).trim()
  if (leading) sections.push({ title: '核心结论', body: leading })

  matches.forEach((match, index) => {
    const title = String(match[1] || '').trim()
    const start = Number(match.index || 0) + match[0].length
    const end = index + 1 < matches.length ? Number(matches[index + 1].index || normalized.length) : normalized.length
    const body = normalized.slice(start, end).trim()
    if (!title || /^业绩分析报告$/.test(title)) return
    if (body) sections.push({ title, body })
  })

  return sections
}

const togglePanel = () => {
  showPanel.value = !showPanel.value
  nextTick(resizeRenderedCharts)
}
const toggleThinking = (id) => { thinkingOpen[id] = !thinkingOpen[id] }
const toggleLog = (i) => { logOpen[i] = !logOpen[i] }
const setResultChainRef = (id, el) => {
  if (!id) return
  if (el) resultChainRefs.set(id, el)
  else resultChainRefs.delete(id)
}
const openDetailPanel = (msg = null) => {
  if (msg?.data && !msg.data.error && !msg.data.requires_confirmation) {
    detailReportResult.value = JSON.parse(JSON.stringify(msg.data))
  } else {
    detailReportResult.value = null
  }
  showPanel.value = true
  nextTick(resizeRenderedCharts)
  scrollPanelToReportTop()
}

const scrollPanelToReportTop = () => nextTick(() => {
  const panel = panelRef.value
  const report = sideReportRef.value
  const reportHead = sideReportHeadRef.value
  if (!panel) return
  if (!report) {
    panel.scrollTo({ top: 0, behavior: 'auto' })
    return
  }
  const target = reportHead || report
  const panelRect = panel.getBoundingClientRect()
  const targetRect = target.getBoundingClientRect()
  const top = panel.scrollTop + targetRect.top - panelRect.top - 12
  panel.scrollTo({ top: Math.max(0, top), behavior: 'auto' })
})

const clearExecutionPanelState = () => {
  detailReportResult.value = null
  Object.keys(logOpen).forEach(k => delete logOpen[k])
  // S1 信号重置：开始新一轮执行即脱离"历史快照恢复"状态
  if (session?.state) session.state.isHistoricalSnapshot = false
  timelineVersion.value += 1
  nextTick(() => {
    if (panelRef.value) panelRef.value.scrollTop = 0
  })
}

const clearChatUiState = () => {
  Object.keys(thinkingOpen).forEach(k => delete thinkingOpen[k])
  Object.keys(confirmationDrafts).forEach(k => delete confirmationDrafts[k])
  Object.keys(clarifyDrafts).forEach(k => delete clarifyDrafts[k])
  Object.keys(confirmationSubmitting).forEach(k => delete confirmationSubmitting[k])
  Object.keys(confirmExpanded).forEach(k => delete confirmExpanded[k])
  Object.keys(officeDrillOpen).forEach(k => delete officeDrillOpen[k])
  reportViewerVisible.value = false
  chartViewerVisible.value = false
  elapsed.value = 0
  stopTimer()
  clearExecutionPanelState()
}

const isUiEventLike = (value) => Boolean(
  value
  && typeof value === 'object'
  && (
    typeof value.preventDefault === 'function'
    || typeof value.stopPropagation === 'function'
    || value.type
  )
)

const openReportViewer = (report = latestReport.value, title = sideReportHeading.value, datasetsForReport = latestDatasets.value) => {
  if (isUiEventLike(report)) {
    report = latestReport.value
    title = sideReportHeading.value
    datasetsForReport = latestDatasets.value
  }
  if (!report && !datasetsForReport?.length) {
    ElMessage.warning('当前还没有可查看的完整报告')
    return
  }
  reportViewerResearch.value = null
  reportViewerReport.value = report
  reportViewerTitle.value = normalizeReportTitle(title)
  reportViewerDatasets.value = Array.isArray(datasetsForReport) ? datasetsForReport : []
  reportDialogFullscreen.value = false
  reportViewerVisible.value = true
}
const openMessageReport = result => {
  if(!canUseFeature('ask_report_details') || !result)return
  const datasets=result.research?(result.research.evidence || []).flatMap(e=>e.dataset_results || []):result.dataset_results || []
  const report=String(result.report || result.analysis || datasets.map(ds=>ds.analysis || '').join('\n\n'))
  openReportViewer(report,result.question || '数据分析报告',datasets)
  reportViewerResearch.value = result.research ? result : null
}
const openFullScreenReport = () => {
  openReportViewer(latestReport.value, sideReportHeading.value, latestDatasets.value)
  reportDialogFullscreen.value = true
}
const openChartViewer = (spec, title = '图表预览') => {
  if (!spec) return
  chartViewerSpec.value = spec
  chartViewerTitle.value = title
  chartViewerMode.value = 'chart'
  chartViewerVisible.value = true
}

const isOfficeExpanded = (id) => officeDrillOpen[String(id)] === true
const toggleOfficeDrill = (id) => {
  const key = String(id)
  officeDrillOpen[key] = !isOfficeExpanded(key)
  nextTick(resizeRenderedCharts)
}

const chartViewerTableRows = computed(() => (
  Array.isArray(chartViewerSpec.value?.rows) ? chartViewerSpec.value.rows : []
))

const chartViewerTableColumns = computed(() => (
  Array.isArray(chartViewerSpec.value?.columns) ? chartViewerSpec.value.columns : []
))

const chartViewerHasTable = computed(() => (
  chartViewerTableRows.value.length > 0 && chartViewerTableColumns.value.length > 0
))

const getPlanSteps = (msg) => {
  const route = msg.data?.route
  if (!route) return []
  const text = typeof route === 'string' ? route : (route.route_desc || JSON.stringify(route))
  return text.split('\n').filter(l => l.trim().match(/^步骤\d|^\d+[\.、]/)).map(s => s.replace(/^(步骤\d+[:：]?|\d+[\.、\s]*)/i, '').trim()).filter(Boolean)
}

const getThinkingSteps = (msg) => {
  const mapStatus = (status) => ({
    success: 'completed',
    completed: 'completed',
    running: 'running',
    pending: 'pending',
    warning: 'warning',
    error: 'error',
  }[status] || 'completed')

  const toStep = (step) => ({
    text: step?.text || step?.title || step?.detail || '执行步骤',
    detail: step?.detail && step?.detail !== step?.title ? step.detail : '',
    status: mapStatus(step?.status),
  })

  if (msg.loading) return session.state.logs.map(toStep)
  if (!msg.data) return []

  const isCurrentResult =
    msg.data?.question &&
    session.state.question &&
    msg.data.question === session.state.question &&
    session.state.logs.length > 0

  if (isCurrentResult) {
    return session.state.logs.map((step) => ({
      text: step?.title || step?.summary || '执行步骤',
      detail: step?.summary || step?.detailLines?.[0] || '',
      status: mapStatus(step?.status),
      statusText: step?.status === 'warning' ? '待确认' : undefined,
    }))
  }

  const steps = []
  if (msg.data.route) {
    steps.push({
      text: '已完成问题理解与执行规划',
      detail: '系统已经确定查询路径与分析重点。',
      status: 'completed',
    })
  }
  ;(msg.data.dataset_results || []).forEach((r) => {
    steps.push({
      text: `已完成数据检索 ${r.dataset_name || '目标数据集'}`,
      detail: r.rows?.length ? `已返回 ${r.rows.length} 行结果数据。` : '已拿到可分析的数据结果。',
      status: 'completed',
    })
  })
  if (msg.data.dataset_results?.[0]?.analysis) {
    steps.push({
      text: '已生成经营分析报告',
      detail: '报告摘要已经同步写入左侧回复区与右侧结果区。',
      status: 'completed',
    })
  }
  if (msg.data.requires_confirmation) {
    steps.push({
      text: '等待确认统计口径',
      detail: msg.data.confirmation_question || '需要先确认业务口径再继续执行。',
      status: 'warning',
    })
  }
  if (msg.data.error) {
    steps.push({
      text: '执行过程中发生异常',
      detail: msg.data.error,
      status: 'error',
    })
  }
  return steps
}

const isCurrentSessionMessage = (msg) => {
  return Boolean(
    !session.state.isHistoricalSnapshot &&
    msg?.data?.question &&
    session.state.question &&
    msg.data.question === session.state.question &&
    session.state.logs.length > 0
  )
}

const latestAiMessage = computed(() => (
  [...messages].reverse().find(item => item?.role === 'ai') || null
))

const isLatestAiMessage = (msg) => latestAiMessage.value?.id === msg?.id

const currentSessionAiMessage = computed(() => (
  [...messages].reverse().find(item => item?.role === 'ai' && isCurrentSessionMessage(item)) || latestAiMessage.value || null
))

const activeRequestAiMessage = computed(() => (
  messages.find(item => item?.id === activeRequestAiMessageId.value) || null
))

const syncPendingConfirmationMessage = () => {
  const result = session.state.result
  if (session.state.status !== 'waiting_confirmation' || !result?.requires_confirmation) return

  const msg = activeRequestAiMessage.value || currentSessionAiMessage.value
  if (!msg || msg.role !== 'ai') return
  if (msg.data?.requires_confirmation) return

  msg.loading = false
  msg.data = JSON.parse(JSON.stringify(result))
  thinkingOpen[msg.id] = false
  if (!(msg.id in confirmationDrafts)) confirmationDrafts[msg.id] = ''
  stopTimer()
  scheduleChatScroll(36, 'smooth')
}

const syncCompletedResultMessage = () => {
  const result = session.state.result
  if (session.state.status !== 'completed' || !result || result?.requires_confirmation || result?.error) return

  const msg = activeRequestAiMessage.value || currentSessionAiMessage.value
  if (!msg || msg.role !== 'ai') return

  const sameQuestion = !result.question || !session.state.question || result.question === session.state.question
  if (!sameQuestion) return

  const needsSync = msg.loading || !msg.data || !Array.isArray(msg.data?.dataset_results)
  if (!needsSync) return

  msg.loading = false
  msg.data = JSON.parse(JSON.stringify(result))
  thinkingOpen[msg.id] = false
  stopTimer()
  scheduleChatReportTop(48, 'smooth')
}

const shouldShowLiveFeed = (msg) => {
  if (msg?.loading) return true
  if (msg?.data?.early_clarify) return false
  if (!session.state.logs.length) return false
  if (msg?.data?.requires_confirmation) return false
  if (msg?.data?.aborted) return isLatestAiMessage(msg) || isCurrentSessionMessage(msg)
  return Boolean(
    isCurrentSessionMessage(msg) ||
    (isLatestAiMessage(msg) && ['completed', 'canceled', 'error'].includes(session.state.status))
  )
}

const getLiveFeedMode = (msg) => {
  if (msg?.data?.aborted || session.state.status === 'canceled') return 'canceled'
  if (!msg?.data?.aborted && session.state.status === 'completed' && (isCurrentSessionMessage(msg) || isLatestAiMessage(msg))) {
    return 'completed'
  }
  if (msg?.loading) return 'live'
  return 'completed'
}

const shouldShowThinkingCard = (msg) => {
  if (msg?.loading) return !session.state.logs.length
  return false
}

const shouldShowConfirmationCard = (msg) => Boolean(
  !isViewingReadonly.value && msg?.data?.confirmation_type !== 'research_plan' && msg?.data?.requires_confirmation && !confirmationSubmitting[msg.id] && !msg?.loading
)

const shouldShowConfirmationSubmitted = (msg) => Boolean(
  !isViewingReadonly.value && msg?.data?.confirmation_type !== 'research_plan' && msg?.data?.requires_confirmation && confirmationSubmitting[msg.id]
)

const isMessageExecutionComplete = (msg) => {
  if (!msg?.data || msg?.loading || msg?.data?.error || msg?.data?.requires_confirmation) return false
  if (isViewingReadonly.value) return true
  if (!isCurrentSessionMessage(msg)) return true
  return session.state.status === 'completed'
}

const shouldShowResultHandoff = (msg) => {
  return Boolean(
    isMessageExecutionComplete(msg) &&
    isCurrentSessionMessage(msg) &&
    (getReport(msg) || getPrimaryDataset(msg))
  )
}

const shouldShowResultChain = (msg) => Boolean(
  !msg?.data?.early_clarify &&
  isMessageExecutionComplete(msg) &&
  (getReport(msg) || getPrimaryDataset(msg) || (msg.data && !msg.data.error))
)

const getMessageDerived = (msg) => {
  if (!msg || typeof msg !== 'object') return null
  const data = msg.data || null
  const datasetResults = data?.dataset_results || null
  const questionKey = getQuestionText()
  const cached = messageDerivedCache.get(msg)
  if (cached?.data === data && cached?.datasetResults === datasetResults && cached?.questionKey === questionKey) {
    return cached
  }
  const entry = {
    data,
    datasetResults,
    questionKey,
    datasets: null,
    report: undefined,
    primaryDataset: undefined,
    visualPreviews: undefined,
  }
  messageDerivedCache.set(msg, entry)
  return entry
}

const getDatasets = (msg) => {
  const cache = getMessageDerived(msg)
  if (cache?.datasets) return cache.datasets
  const raw = Array.isArray(msg?.data?.dataset_results) ? msg.data.dataset_results : []
  if (!raw.length) {
    if (cache) cache.datasets = []
    return []
  }
  const subjectByDatasetId = new Map()
  const orgRoute = msg?.data?.diagnostics?.advanced?.route_guard?.organization_route || {}
  ;(orgRoute.organization_mentions || []).forEach((item) => {
    const subjectName = String(item?.node_name || '').trim()
    if (!subjectName) return
    ;(item?.dataset_ids || []).forEach((id) => {
      const numericId = Number(id)
      if (Number.isFinite(numericId)) {
        subjectByDatasetId.set(numericId, subjectName)
      }
    })
  })
  const enriched = raw.map((dataset) => {
    const subjectName = subjectByDatasetId.get(Number(dataset?.dataset_id))
    return subjectName
      ? { ...dataset, comparison_subject_name: subjectName, comparison_subject_level: inferSubjectLevel(subjectName) }
      : dataset
  })
  const visible = enriched.filter(dataset => isDatasetVisible(dataset?.dataset_id))
  const datasetsForMessage = visible.length ? visible : enriched
  if (cache) cache.datasets = datasetsForMessage
  return datasetsForMessage
}
const getReport = (msg) => {
  const cache = getMessageDerived(msg)
  if (cache && cache.report !== undefined) return cache.report
  const report = mergeDatasetReports(getDatasets(msg))
  if (cache) cache.report = report
  return report
}
const getPrimaryDataset = (msg) => {
  const cache = getMessageDerived(msg)
  if (cache && cache.primaryDataset !== undefined) return cache.primaryDataset
  const dataset = buildAggregateDataset(getDatasets(msg))
  if (cache) cache.primaryDataset = dataset
  return dataset
}
const getResultTitle = (msg) => {
  if (msg.data?.display_title) {
    return msg.data.display_title.length > 20 ? `${msg.data.display_title.slice(0, 20)}...` : msg.data.display_title
  }
  const raw = msg.data?.question || session.state.question || '本月公司经营表现分析'
  const normalized = normalizeReportTitle(raw)
  return normalized.length > 20 ? `${normalized.slice(0, 20)}...` : normalized
}

const formatElapsedLabel = (seconds) => {
  const totalSeconds = Math.max(0, Math.round(Number(seconds) || 0))
  const minutes = Math.floor(totalSeconds / 60)
  const remain = totalSeconds % 60
  if (minutes <= 0) return `${remain}s`
  return `${minutes}m ${remain}s`
}

const isAbortLikeInteractionError = (error) => {
  const text = `${error?.name || ''} ${error?.code || ''} ${error?.message || ''}`
  return Boolean(
    error?.isUserAbort ||
    /AbortError|CanceledError|ERR_CANCELED|aborted|cancelled|canceled|BodyStreamBuffer/i.test(text)
  )
}

const getMessageElapsedLabel = (msg) => {
  if (msg?.loading && isCurrentSessionMessage(msg)) {
    return formatElapsedLabel(elapsed.value)
  }
  return ''
}

const getAskFlowMeta = (msg) => {
  if (!showAskFlowBadge.value) return null
  const meta = msg?.data?.ask_flow || msg?.data?.diagnostics?.ask_flow || null
  return meta && typeof meta === 'object' ? meta : null
}

const getAskFlowLabel = (msg) => {
  const flow = String(getAskFlowMeta(msg)?.flow || '').toLowerCase()
  if (flow === 'advanced') return '进阶流程'
  if (flow === 'basic') return '基础流程'
  return ''
}

const getAskFlowClass = (msg) => {
  const flow = String(getAskFlowMeta(msg)?.flow || '').toLowerCase()
  return flow === 'advanced' ? 'is-advanced' : 'is-basic'
}

const getAskFlowHint = (msg) => {
  const reason = String(getAskFlowMeta(msg)?.reason || '')
  const map = {
    basic_selected: '由基础流程执行',
    advanced_selected: '由进阶流程执行',
    advanced_disabled: '进阶未启用，已回落基础流程',
    advanced_role_denied: '当前角色未进入进阶灰度',
    advanced_error_fallback: '进阶异常，已回退基础流程',
  }
  return map[reason] || ''
}

const getVisualPreviews = (msg) => {
  const cache = getMessageDerived(msg)
  if (cache && cache.visualPreviews !== undefined) return cache.visualPreviews
  const sourceDatasets = getDatasets(msg)
  const previews = hasBusinessDrillDataset(sourceDatasets) ? [] : sourceDatasets
    .slice(0, 2)
    .map((dataset, index) => ({
      key: `${dataset.dataset_id || index}-${dataset.dataset_name || 'dataset'}`,
      dataset,
      chartSpec: getDatasetChartSpecs(dataset)[0] || null,
    }))
    .filter(item => item.chartSpec && (item.chartSpec.chartType === 'metric' || hasChartRows(item.chartSpec)))
  if (cache) cache.visualPreviews = previews
  return previews
}

const focusComposer = (selectAll = false) => nextTick(() => {
  const textarea = document.querySelector('.cmp-textarea')
  if (!(textarea instanceof HTMLTextAreaElement)) return
  textarea.focus()
  const end = textarea.value.length
  textarea.setSelectionRange(selectAll ? 0 : end, end)
})

const writeClipboard = async (text) => {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text)
    return
  }
  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.setAttribute('readonly', 'readonly')
  textarea.style.position = 'fixed'
  textarea.style.left = '-9999px'
  document.body.appendChild(textarea)
  textarea.select()
  document.execCommand('copy')
  document.body.removeChild(textarea)
}

const copyQuestion = async (msg) => {
  if (!canUseFeature('ask_question_copy')) return
  const text = String(msg?.content || '').trim()
  if (!text) return
  try {
    await writeClipboard(text)
    ElMessage.success('问题已复制')
  } catch {
    ElMessage.warning('复制失败，请手动复制')
  }
}

const editQuestion = (msg) => {
  if (!canUseFeature('ask_question_edit')) return
  const text = String(msg?.content || '').trim()
  if (!text) return
  if (isRunning.value) {
    ElMessage.warning('当前正在执行，停止后再修改问题')
    return
  }
  query.value = text
  focusComposer(true)
  ElMessage.success('已放入输入框，修改后按 Enter 发送')
}

const clearMessageRuntimeState = (items = []) => {
  items.forEach((item) => {
    if (!item?.id) return
    delete thinkingOpen[item.id]
    delete confirmationDrafts[item.id]
    delete clarifyDrafts[item.id]
    delete confirmationSubmitting[item.id]
    delete confirmExpanded[item.id]
  })
}

const rerunQuestion = async (msg) => {
  if (!canUseFeature('ask_question_rerun')) return
  const text = String(msg?.content || '').trim()
  if (!text || isRunning.value) return

  // 重问创建新的任务条目
  const createShellId = () => {
    if (typeof window !== 'undefined' && window.crypto?.randomUUID) {
      return `history-report-${window.crypto.randomUUID()}`
    }
    return `history-report-${Date.now()}-${Math.random().toString(16).slice(2)}`
  }
  const shellId = createShellId()

  const runningShell = {
    id: shellId,
    title: String(text).slice(0, 24),
    question: text,
    datasetId: datasetId.value || null,
    datasetName: datasets.value.find(d => d.id === datasetId.value)?.name || '',
    updatedAt: new Date().toISOString(),
    status: 'running',
    reportSnapshot: null,
  }
  upsertHistory(runningShell)
  setActiveHistory(shellId)
  setRunningSessionId(shellId)
  switchViewToDefault()

  session.resetSession()
  clearChatUiState()
  messages.splice(0, messages.length)
  const uid = ++msgCounter
  messages.push({ id: uid, role: 'user', content: text })
  const aid = ++msgCounter
  const aiMsg = { id: aid, role: 'ai', loading: true, data: null }
  messages.push(aiMsg)
  activeRequestAiMessageId.value = aid
  thinkingOpen[aid] = true

  query.value = ''
  clearExecutionPanelState()
  scheduleChatScroll(24, 'smooth')
  startTimer()

  try {
    const datasetInput = getDatasetInputForQuestion(text)
    const res = await session.startAsk(text, datasetInput, getModelInputForQuestion(), {})
    clearPendingQuickDataset()
    if (res) {
      aiMsg.loading = false
      aiMsg.data = res
      if (res?.requires_confirmation) {
        markRunningTaskPending(shellId)
        upsertHistory({ ...runningShell, status: 'pending_confirmation' })
      } else if (!res?.error) {
        saveCurrentToHistory(res, { preferId: shellId })
        markRunningTaskCompleted(shellId, taskOutcome(res || aiMsg.data).status)
      } else {
        markRunningTaskFailed(shellId)
      }
    } else if (!aiMsg.data) {
      aiMsg.loading = false
      aiMsg.data = { aborted: true }
      markRunningTaskFailed(shellId)
    } else {
      aiMsg.loading = false
      markRunningTaskFailed(shellId)
    }
    thinkingOpen[aid] = false
    if (res && !res?.requires_confirmation && !res?.error) scheduleChatReportTop(48, 'smooth')
    else scheduleChatScroll(48, 'smooth')
  } catch (err) {
    if (isAbortLikeInteractionError(err)) {
      aiMsg.loading = false
      aiMsg.data = { aborted: true, question: text }
      thinkingOpen[aid] = false
      scheduleChatScroll(36, 'smooth')
      markRunningTaskFailed(shellId)
      return
    }
    if (aiMsg.data?.requires_confirmation && session.state.status === 'waiting_confirmation') {
      aiMsg.loading = false
      thinkingOpen[aid] = false
      scheduleChatScroll(36, 'smooth')
      return
    }
    aiMsg.loading = false
    aiMsg.data = { error: err.response?.data?.error || err.message || '系统繁忙' }
    query.value = text
    scheduleChatScroll(36, 'smooth')
  } finally {
    stopTimer()
    finishQuestionQueue(aiMsg.data)
  }
}

// 纠正条 chip 点击：把候选理解直接作为新问题发送（复用主发送链路）
const applyClarifySuggestion = (text) => {
  const t = String(text || '').trim()
  if (!t || isRunning.value) return
  query.value = t
  handleSend()
}

// 纠正条/错字卡自由输入：推荐候选都不是时，用户直接输入新问句走主链路
const submitClarifyDraft = (msg) => {
  const text = String(clarifyDrafts[msg?.id] || '').trim()
  if (!text || isRunning.value) return
  clarifyDrafts[msg.id] = ''
  applyClarifySuggestion(text)
}

const handleClarifyDraftEnter = (event, msg) => {
  if (event?.isComposing) return
  submitClarifyDraft(msg)
}

// 错字短路纠正卡：用户确认原问题没错字，带 skipTypoCheck 跳过第 0 层快检重新发送
const resendOriginalQuestion = (msg) => {
  const t = String(msg?.data?.question || msg?.question || '').trim()
  if (!t || isRunning.value) return
  query.value = t
  handleSend({ skipTypoCheck: true })
}

const questionQueue=ref([])
const queuePaused=ref(false)
const queueDraftFlow=ref('')
const queueReason=ref('')
const sendInFlight=ref(false)
let queueGeneration=0
const pauseQuestionQueue=reason=>{queuePaused.value=true;queueReason.value=reason}
const clearQuestionQueue=()=>{questionQueue.value=[];queuePaused.value=false;queueReason.value=''}
const removeQueuedQuestion=id=>{questionQueue.value=questionQueue.value.filter(item=>item.id!==id)}
const editQueuedQuestion=id=>{
  const item=questionQueue.value.find(item=>item.id===id)
  if(!item || isViewingReadonly.value)return
  if(query.value.trim()){ElMessage.info('先发送或整理当前草稿，再编辑队列问题');return}
  query.value=item.question;datasetId.value=item.datasetId;modelId.value=item.modelId;queueDraftFlow.value=item.flow
  isDatasetManuallySelected.value=Boolean(item.datasetId)
  removeQueuedQuestion(id);focusComposer()
}
const drainQuestionQueue=()=>{
  if(sendInFlight.value || isRunning.value || isViewingReadonly.value || queuePaused.value || !questionQueue.value.length)return
  if(!canUseFeature('ask_send_question')){pauseQuestionQueue('发送权限已变更，请确认后继续');return}
  if(session.state.status==='waiting_confirmation'){pauseQuestionQueue(queuePauseReason('waiting'));return}
  const upcoming=questionQueue.value[0]
  if(upcoming.datasetId && (!canUseFeature('ask_dataset_select') || !datasets.value.some(d=>Number(d.id)===Number(upcoming.datasetId)))){pauseQuestionQueue('排队问题的数据集或选择权限已变更，请检查后继续');return}
  if(upcoming.modelId && (!canUseFeature('ask_model_select') || !aiModels.value.some(m=>Number(m.id)===Number(upcoming.modelId)))){pauseQuestionQueue('排队问题的模型或选择权限已变更，请检查后继续');return}
  const [item,...rest]=questionQueue.value
  questionQueue.value=rest
  void handleSend({_queueItem:item})
}
const resumeQuestionQueue=()=>{
  if(session.state.status==='waiting_confirmation'){ElMessage.info('请先确认当前问题或研究计划');return}
  queuePaused.value=false;queueReason.value='';drainQuestionQueue()
}
const finishQuestionQueue=result=>{
  const reason=queuePauseReason(taskOutcome(result).status)
  if(reason){if(questionQueue.value.length)pauseQuestionQueue(reason);return}
  if(queueReason.value===queuePauseReason('waiting')){queuePaused.value=false;queueReason.value=''}
  window.setTimeout(drainQuestionQueue,0)
}
const handleSend = async (sendOptions) => {
  const opts = (sendOptions && typeof sendOptions === 'object' && !Array.isArray(sendOptions)) ? sendOptions : undefined
  if (!canUseFeature('ask_send_question')) return
  const queued=opts?._queueItem
  const text = String(queued?.question || query.value).trim()
  // 只读历史回看拦截必须给用户反馈（2026-10-25 云上用户反馈"发送没反应"：
  // 旧逻辑静默 return，且只读横幅在无运行任务时不显示，用户无任何提示）
  if (!text) return
  if (isViewingReadonly.value) {
    ElMessage.info('当前处于历史回看模式，点击右上角「新会话」后再提问')
    return
  }
  const submitted=queued || queuedQuestion(text,{datasetId:opts?.datasetId || getDatasetInputForQuestion(text),datasetName:datasets.value.find(d=>Number(d.id)===Number(opts?.datasetId || getDatasetInputForQuestion(text)))?.dataset_name,modelId:getModelInputForQuestion(),flow:queueDraftFlow.value || requestedFlow.value})
  if(!queued && (isRunning.value || sendInFlight.value || questionQueue.value.length || session.state.status==='waiting_confirmation')){
    try{questionQueue.value=appendQuestion(questionQueue.value,submitted)}catch(error){ElMessage.info(error.message);return}
    query.value='';queueDraftFlow.value='';clearPendingQuickDataset()
    if(session.state.status==='waiting_confirmation')pauseQuestionQueue(queuePauseReason('waiting'))
    drainQuestionQueue();focusComposer();return
  }
  const dispatchToken=++queueGeneration
  sendInFlight.value=true
  requestedFlow.value=submitted.flow
  if(!queued){query.value='';queueDraftFlow.value='';queuePaused.value=false;queueReason.value=''}
  const createShellId = () => {
    if (typeof window !== 'undefined' && window.crypto?.randomUUID) {
      return `history-report-${window.crypto.randomUUID()}`
    }
    return `history-report-${Date.now()}-${Math.random().toString(16).slice(2)}`
  }
  const shellId = createShellId()

  const runningShell = {
    id: shellId,
    title: String(text).slice(0, 24),
    question: text,
    datasetId: submitted.datasetId,
    datasetName: submitted.datasetName,
    updatedAt: new Date().toISOString(),
    status: 'running',
    reportSnapshot: null,
  }
  upsertHistory(runningShell)
  setActiveHistory(shellId)
  setRunningSessionId(shellId)
  switchViewToDefault()

  const uid = ++msgCounter
  messages.push({ id: uid, role: 'user', content: text })
  const aid = ++msgCounter
  const aiMsg = { id: aid, role: 'ai', loading: true, data: null }
  messages.push(aiMsg)
  activeRequestAiMessageId.value = aid
  thinkingOpen[aid] = true

  clearExecutionPanelState()
  scheduleChatScroll(24, 'smooth')
  startTimer()

  try {
    // 解析条确认链路可显式锚定数据集（opts.datasetId）：用户已明确指定口径，
    // 跳过 datasetInput 的自动释放启发式
    const res = await session.startAsk(text, submitted.datasetId, submitted.modelId, { ...opts, _queueItem:undefined, askFlow:undefined })
    clearPendingQuickDataset()
    if (res) {
      aiMsg.loading = false
      aiMsg.data = res
      if (res?.requires_confirmation) {
        markRunningTaskPending(shellId)
        upsertHistory({ ...runningShell, status: 'pending_confirmation' })
      } else if (!res?.error) {
        saveCurrentToHistory(res, { preferId: shellId })
        markRunningTaskCompleted(shellId, taskOutcome(res || aiMsg.data).status)
      } else {
        markRunningTaskFailed(shellId)
      }
    } else if (!aiMsg.data) {
      aiMsg.loading = false
      aiMsg.data = { aborted: true }
      markRunningTaskFailed(shellId)
    } else {
      aiMsg.loading = false
      markRunningTaskCompleted(shellId, taskOutcome(res || aiMsg.data).status)
    }
    thinkingOpen[aid] = false
    if (res && !res?.requires_confirmation && !res?.error) scheduleChatReportTop(48, 'smooth')
    else scheduleChatScroll(48, 'smooth')
  } catch (err) {
    if (isAbortLikeInteractionError(err)) {
      aiMsg.loading = false
      aiMsg.data = { aborted: true, question: text }
      thinkingOpen[aid] = false
      scheduleChatScroll(36, 'smooth')
      markRunningTaskFailed(shellId)
      return
    }
    if (aiMsg.data?.requires_confirmation && session.state.status === 'waiting_confirmation') {
      aiMsg.loading = false
      thinkingOpen[aid] = false
      scheduleChatScroll(36, 'smooth')
      return
    }
    aiMsg.loading = false
    aiMsg.data = { error: err.response?.data?.error || err.message || '系统繁忙' }
    if(!query.value.trim() && !queued)query.value = text
    scheduleChatScroll(36, 'smooth')
    markRunningTaskFailed(shellId)
  } finally {
    if(dispatchToken===queueGeneration){stopTimer();sendInFlight.value=false;finishQuestionQueue(aiMsg.data)}
  }
}

const handleStop = () => {
  if (!canUseFeature('ask_stop_run')) return
  if(questionQueue.value.length)pauseQuestionQueue(queuePauseReason('canceled'))
  session.stopAsk()
  const msg = latestAiMessage.value
  if (msg?.role === 'ai' && msg.loading) {
    msg.loading = false
    msg.data = {
      ...(msg.data || {}),
      aborted: true,
      requires_confirmation: false,
      workflow: { ...session.state.workflow, status: "canceled" },
      question: session.state.question || query.value.trim(),
    }
    thinkingOpen[msg.id] = false
  }
  stopTimer()
  if (runningSessionId.value) {
    markRunningTaskFailed(runningSessionId.value)
  }
  ElMessage({
    message: '已停止执行',
    type: 'warning',
    duration: 1500,
    showClose: false,
    customClass: 'ax-toast-modern ax-toast-stop',
  })
}

const resetForNewChat = () => {
  queueGeneration++;sendInFlight.value=false
  questionQueue.value=[];queuePaused.value=false;queueReason.value='';queueDraftFlow.value=''
  // 修 1（reset 保存 guard）：只有完整、正确的结果才保存，避免把 requires_confirmation 中间态
  // （行业部 Overview 层级）当成正式历史保存；也避免旧会话残留的脏 result 被保存。
  const cur = session.state.result || null
  const isCompleteResult = Boolean(
    cur &&
    typeof cur === 'object' &&
    !cur.requires_confirmation &&
    !cur.error &&
    Array.isArray(cur.dataset_results) &&
    cur.dataset_results.length > 0
  )
  if (isCompleteResult) saveCurrentToHistory(cur)
  messages.splice(0, messages.length)
  activeRequestAiMessageId.value = null
  query.value = ''
  clearRestoreRequest()
  setActiveHistory('')
  clearChatUiState()
  session.resetSession()
  showPanel.value = false
  nextTick(() => {
    scheduleChatScroll(20, 'auto')
    schedulePanelScroll(20, 'auto', true)
    focusComposer()
  })
}

const handleNewChat = async () => {
  if (messages.length === 0) {
    resetForNewChat()
    return
  }

  try {
    await ElMessageBox.confirm(
      questionQueue.value.length ? '开始新会话后，将清空待问队列与未发送草稿；当前记录归档到历史对话。' : '开始新会话后，当前执行记录会被清空，并自动归档到历史对话中。',
      '开始新会话',
      {
        type: 'info',
        confirmButtonText: '开始新会话',
        cancelButtonText: '暂不切换',
        distinguishCancelAndClose: true,
        customClass: 'ax-message-box',
      }
    )
    resetForNewChat()
  } catch {
    // user cancelled
  }
}

const historyPanelRef = ref(null)
const focusSidebarHistory = () => {
  historyPanelRef.value?.open()
}

const handleSelectHistorySession = async (item) => {
  if (isRunning.value) {
    ElMessage.warning('当前有任务正在执行，请稍候再切换')
    return
  }
  if (!item || item.id === activeHistoryId.value) return
  if(questionQueue.value.length)pauseQuestionQueue('正在查看历史会话，返回后可继续队列')
  await restoreHistory(item)
}

const handleDeleteHistorySession = async (item, event) => {
  event?.stopPropagation()
  if (!item?.id) return
  try {
    await removeHistory(item.id)
    ElMessage.success('已删除该会话记录')
    if (activeHistoryId.value === item.id) {
      resetForNewChat()
    }
  } catch (e) {
    ElMessage.error('删除会话失败')
  }
}

const handleClearAllSessions = async () => {
  try {
    await ElMessageBox.confirm('确定要清空全部历史会话记录吗？', '提示', {
      confirmButtonText: '确定清空',
      cancelButtonText: '取消',
      type: 'warning',
      customClass: 'ax-message-box',
    })
    await clearHistory()
    resetForNewChat()
    ElMessage.success('已清空全部会话')
  } catch (e) {
    // cancelled
  }
}

const datasetNameMap = computed(() => new Map(
  (datasets.value || []).map(item => [Number(item.id), item.dataset_name])
))

const normalizeReportTitle = (text) => {
  let s = String(text ?? '').trim()
  if (!s) return '业绩分析报告'
  s = s.replace(
    /^(?:我说的是|我说的是|我说|我的问题是|我想问|我想知道|请问|问一下|看一下|查一下|看下|查下|请|麻烦|帮我|给我|告诉我|咨询一下|了解一下|看看)(?:[，,：:\s]+)?/,
    ''
  )
  s = s.replace(/[？?！!。]+$/g, '').trim()
  if (s.endsWith('的')) {
    s = s.slice(0, -1).trim()
  }
  return s || '业绩分析报告'
}

const buildDownloadFilename = (title) => {
  const base = String(normalizeReportTitle(title))
    .replace(/[\\/:*?"<>|]+/g, '-')
    .replace(/\s+/g, ' ')
    .trim()
  return `${base || '业绩分析报告'}.pdf`
}

const buildReportHtml = (title, report) => `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${normalizeReportTitle(title)}</title>
  <style>
    @page { size: A4; margin: 16mm 14mm; }
    :root { --primary: #1A1A1A; --page-bg: #edf2f5; --card-bg: #ffffff; --text: #111827; }
    body { margin: 0; font-family: var(--font-sans, "Microsoft YaHei UI", "Microsoft YaHei", "PingFang SC", sans-serif); background: var(--page-bg); color: var(--text); }
    .page { max-width: 960px; margin: 0 auto; padding: 40px 24px 72px; }
    .card { background: var(--card-bg); border-radius: 4px; padding: 28px 32px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .eyebrow { font-size: 12px; color: var(--primary); font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
    h1 { margin: 12px 0 8px; font-size: 28px; line-height: 1.25; }
    h2 { margin: 28px 0 12px; font-size: 20px; }
    h3 { margin: 20px 0 10px; font-size: 16px; }
    p, li { font-size: 14px; line-height: 1.8; color: #6B7280; }
    hr { border: none; border-top: 1px solid #E5E7EB; margin: 24px 0; }
    code { background: #F3F4F6; padding: 2px 6px; border-radius: 6px; }
    table { width: 100%; border-collapse: collapse; margin: 16px 0; }
    th, td { border: 1px solid #E5E7EB; padding: 10px 12px; text-align: left; font-size: 13px; }
    th { background: #edf2f5; color: #111827; }
    .print-tip { margin-top: 20px; font-size: 12px; color: #9CA3AF; }
    @media print {
      body { background: #ffffff; }
      .page { max-width: none; padding: 0; }
      .card { border: none; border-radius: 0; padding: 0; box-shadow: none; }
      .print-tip { display: none; }
    }
  </style>
</head>
<body>
  <main class="page">
    <section class="card">
      <div class="eyebrow">Data Agent Report</div>
      <h1>${normalizeReportTitle(title)}</h1>
      <article>${renderMd(report)}</article>
      <div class="print-tip">请在打印对话框中选择“另存为 PDF”</div>
    </section>
  </main>
</body>
</html>`

const downloadLatestReport = (report = latestReport.value, title = sideReportHeading.value) => {
  if (!report) {
    ElMessage.warning('当前还没有可导出的报告内容')
    return
  }

  const exportTitle = normalizeReportTitle(title)
  if (activePrintFrame?.parentNode) {
    activePrintFrame.parentNode.removeChild(activePrintFrame)
    activePrintFrame = null
  }

  const frame = document.createElement('iframe')
  frame.style.position = 'fixed'
  frame.style.right = '0'
  frame.style.bottom = '0'
  frame.style.width = '0'
  frame.style.height = '0'
  frame.style.border = '0'
  frame.style.opacity = '0'
  frame.setAttribute('aria-hidden', 'true')
  document.body.appendChild(frame)
  activePrintFrame = frame

  const html = buildReportHtml(exportTitle, report)
  let printed = false
  const triggerPrint = () => {
    if (printed) return
    printed = true
    const frameWindow = frame.contentWindow
    if (!frameWindow) {
      ElMessage.warning('当前无法打开打印窗口，请稍后重试')
      return
    }

    try {
      frameWindow.document.open()
      frameWindow.document.write(html)
      frameWindow.document.close()
      frameWindow.document.title = buildDownloadFilename(exportTitle)
      frameWindow.focus()
      window.setTimeout(() => {
        frameWindow.print()
      }, 260)
      ElMessage.success('已准备好报告，请在打印对话框中选择“另存为 PDF”')
    } catch (error) {
      ElMessage.warning('当前无法导出 PDF，请稍后重试')
    }
  }

  frame.onload = triggerPrint
  window.setTimeout(triggerPrint, 40)
}
const draftAnswerFollowUp = (item) => {
  if (isRunning.value || isViewingReadonly.value || !canUseFeature('ask_send_question') || !canUseFeature('ask_quick_ask')) return
  // The same controlled dataset router rechecks scope when the user submits.
  quickAsk(item)
}
const quickAsk = (item) => {
  if (!canUseFeature('ask_quick_ask')) return
  const text = typeof item === 'string' ? item : String(item?.question_text || '').trim()
  if (!text) return
  const nextDatasetId = typeof item === 'string' ? null : Number(item?.dataset_id || 0)
  datasetId.value = null
  isDatasetManuallySelected.value = false
  pendingQuickDataset.value = nextDatasetId ? { datasetId: nextDatasetId, question: text } : null
  query.value = text
  nextTick(() => {
    const textarea = document.querySelector('.cmp-textarea')
    if (textarea instanceof HTMLTextAreaElement) {
      textarea.focus()
      textarea.setSelectionRange(textarea.value.length, textarea.value.length)
    }
  })
  const datasetName = typeof item === 'string' ? '' : String(item?.dataset_name || item?.dataset_tag || '').trim()
  ElMessage({
    message: datasetName ? `问题已填入 · ${datasetName}` : '问题已填入',
    type: 'success',
    duration: 1500,
    showClose: false,
    customClass: 'ax-toast-modern'
  })
}

const handleExternalFreshChat = () => {
  resetForNewChat()
}

const getConfirmOptionKey = (opt) => (typeof opt === 'string' ? opt : (opt?.id || opt?.label || JSON.stringify(opt)))
const getConfirmOptionLabel = (opt) => (typeof opt === 'string' ? opt : (opt?.label || opt?.name || '确认选项'))

const getConfirmOptionDescription = (opt) => (typeof opt === 'string' ? '' : String(opt?.description || '').trim())
const getConfirmOptionScore = (opt) => {
  if (typeof opt === 'string') return null
  const raw = opt?.score
  if (raw === null || raw === undefined || raw === '') return null
  const n = Number(raw)
  return Number.isFinite(n) ? Math.round(n) : null
}
const shouldShowConfirmOptionScore = () => false
const getConfirmOptionScorePct = (opt) => {
  const score = getConfirmOptionScore(opt)
  return score == null ? 0 : Math.min(100, Math.max(0, score))
}
const sortedConfirmationOptions = (msg) => {
  const opts = msg?.data?.confirmation_options || []
  const copy = opts.map((opt, idx) => ({ opt, idx }))
  copy.sort((a, b) => {
    const sa = getConfirmOptionScore(a.opt)
    const sb = getConfirmOptionScore(b.opt)
    if (sa != null && sb != null) return sb - sa
    if (sa != null) return -1
    if (sb != null) return 1
    return a.idx - b.idx
  })
  return copy.map(item => item.opt)
}
const visibleConfirmationOptions = (msg) => {
  const opts = sortedConfirmationOptions(msg)
  if (confirmExpanded[msg?.id]) return opts
  return opts.slice(0, 4)
}
const toggleConfirmOptions = (msgId) => {
  confirmExpanded[msgId] = !confirmExpanded[msgId]
}
const getConfirmOptionDatasetNames = (opt) => {
  if (typeof opt === 'string') return []
  const ids = Array.isArray(opt?.dataset_ids) ? opt.dataset_ids : []
  return ids.map(id => datasetNameMap.value.get(Number(id)) || `数据集 ${id}`)
}
const getConfirmOptionMemberNames = (opt) => {
  if (typeof opt === 'string') return []
  return (Array.isArray(opt?.resolved_members) ? opt.resolved_members : [])
    .map(item => String(item || '').trim())
    .filter(Boolean)
}
const getConfirmOptionImpact = (opt) => {
  if (typeof opt === 'string') return '确认后将继续执行当前问数任务。'
  const optionType = String(opt?.option_type || '')
  if (optionType === 'cross_dataset') return '确认后将以多数据集汇总方式继续生成结果和报告。'
  if (optionType === 'dataset_scope') return '确认后将采用该数据集口径，并继续生成 SQL 与分析报告。'
  if (optionType === 'dataset_disambiguation') return '确认后将采用具体数据集口径，并继续生成后续分析结果。'
  if (optionType === 'member_set_confirmation') {
    return String(opt?.scope_mode || '') === 'compare'
      ? '确认后将按成员逐个对比，再输出结论和报告。'
      : '确认后将先按该成员集合汇总，再继续生成分析结果。'
  }
  return '确认后将按照当前选定口径继续执行。'
}
const getConfirmationCandidateNames = (msg) => {
  const ids = msg?.data?.route?.candidate_dataset_ids || []
  return ids.map(id => datasetNameMap.value.get(Number(id)) || `数据集 ${id}`)
}
const getConfirmationScopeSummary = (msg) => {
  const route = msg?.data?.route || {}
  const confirmationType = String(route?.confirmation_type || '')
  const candidateCount = Array.isArray(route?.candidate_dataset_ids) ? route.candidate_dataset_ids.length : 0
  if (confirmationType === 'member_set_confirmation') {
    const memberCount = Array.isArray(route?.resolved_entities_preview) ? route.resolved_entities_preview.length : 0
    return memberCount > 0
      ? `当前需要确认集合口径，涉及 ${memberCount} 个成员，确认后会继续执行分析。`
      : '当前需要确认集合口径，确认后会继续执行分析。'
  }
  if (confirmationType === 'dataset_disambiguation') {
    return '当前命中了多个可能的数据集口径，确认后会采用对应执行范围。'
  }
  if (candidateCount > 1) return `当前存在 ${candidateCount} 个候选口径，确认后会采用对应执行范围。`
  return '当前需要先确认业务口径，确认后才会继续执行查询与报告生成。'
}

const doConfirm = async (opt, msg) => {
  // 第一时间设置提交状态，立即禁用按钮，防止重复点击或事件冒泡干扰
  if (msg?.id) confirmationSubmitting[msg.id] = true
  // 用户确认后，全局状态从待确认变回执行中，同步顶部banner和左侧任务状态
  if (runningTaskStatus.value === 'pending_confirmation' && runningSessionId.value) {
    runningTaskStatus.value = 'running'
    pendingTaskId.value = null
    const currentShell = historySessions.value.find(h => h.id === runningSessionId.value)
    if (currentShell) {
      upsertHistory({ ...currentShell, status: 'running' })
    }
  }
  startTimer()
  detailReportResult.value = null
  const originalData = msg?.data ? JSON.parse(JSON.stringify(msg.data)) : null
  // 预选联动：点确认选项立即把解析条更新为选中的数据集/节点（执行中也显示所选，不等执行完）。
  // 解决"我选了商用，但上面解析条没变"——ParseBar 用 slots 渲染，更新 slots 即联动（2026-09-01 用户实测反馈）。
  if (msg?.data?.parse_bar && opt && typeof opt === 'object') {
    const pb = msg.data.parse_bar
    const selNode = String(opt.resolved_subject_name || '').trim()
    const selDs = String(opt.dataset_name || '').trim()
    if (Array.isArray(pb.slots)) {
      pb.slots = pb.slots.map((s) => {
        if (s && s.slot === 'node' && selNode) return { ...s, resolved_value: selNode }
        if (s && s.slot === 'dataset' && selDs) return { ...s, resolved_value: selDs }
        return s
      })
    }
  }
  if (msg) {
    msg.loading = true
  }
  try {
    const res = await session.submitBossConfirmation(opt, {
      candidateDatasetIds: msg?.data?.route?.candidate_dataset_ids || msg?.data?.route?.dataset_ids || [],
      originalQuestion: msg?.data?.question || session.state.question,
      sessionId: msg?.data?.session_id,
    })
    const last = [...messages].reverse().find(m => m.role === 'ai')
    if (!res) {
      if (last) {
        last.loading = false
        last.data = { aborted: true, question: session.state.question }
      }
      if (msg?.id) confirmationSubmitting[msg.id] = false
      if (runningSessionId.value) markRunningTaskFailed(runningSessionId.value)
      scheduleChatScroll(36, 'smooth')
      return
    }
    if (last) {
      last.loading = false
      last.data = res
      activeRequestAiMessageId.value = last.id
    }
    if (!res?.requires_confirmation && !res?.error) {
      saveCurrentToHistory(res, { preferId: runningSessionId.value })
      markRunningTaskCompleted(runningSessionId.value,taskOutcome(res).status)
    } else if (res?.requires_confirmation) {
      markRunningTaskPending(runningSessionId.value)
      const currentShell = historySessions.value.find(h => h.id === runningSessionId.value)
      if (currentShell) {
        upsertHistory({ ...currentShell, status: 'pending_confirmation' })
      }
    } else {
      markRunningTaskFailed(runningSessionId.value)
    }
    if (msg?.id && typeof opt === 'string') confirmationDrafts[msg.id] = ''
    if (!res?.requires_confirmation && !res?.error) scheduleChatReportTop(36, 'smooth')
    else scheduleChatScroll(36, 'smooth')
  } catch (error) {
    if (isAbortLikeInteractionError(error)) {
      if (msg) {
        msg.loading = false
        msg.data = { aborted: true, question: session.state.question }
      }
      if (msg?.id) confirmationSubmitting[msg.id] = false
      scheduleChatScroll(36, 'smooth')
      return
    }
    if (msg) {
      msg.loading = false
      if (originalData?.requires_confirmation) {
        msg.data = {
          ...originalData,
          requires_confirmation: true,
          error: '',
        }
      }
    }
    if (msg?.id) confirmationSubmitting[msg.id] = false
    ElMessage.error(error?.response?.data?.error || error?.message || '提交失败')
    scheduleChatScroll(36, 'smooth')
  }
  finally { if (msg?.id) confirmationSubmitting[msg.id] = false; stopTimer(); finishQuestionQueue(msg?.data) }
}

const scrollChat = (behavior = 'smooth') => nextTick(() => {
  if (chatBodyRef.value) {
    chatBodyRef.value.scrollTo({ top: chatBodyRef.value.scrollHeight, behavior })
  }
})

const scrollChatToReportTop = (behavior = 'auto') => nextTick(() => {
  const container = chatBodyRef.value
  if (!container) return
  const latestId = latestAiMessage.value?.id
  const researchDesks = container.querySelectorAll('.research-desk.is-research')
  const researchDesk = researchDesks[researchDesks.length - 1]
  const researchTarget = researchDesk?.querySelector('.research-report') || researchDesk
  const allResultChains = Array.from(container.querySelectorAll('.ax-result-chain'))
  const target = researchTarget || (latestId && resultChainRefs.get(latestId))
    || allResultChains[allResultChains.length - 1]
  if (!target) {
    scrollChat(behavior)
    return
  }
  const containerRect = container.getBoundingClientRect()
  const targetRect = target.getBoundingClientRect()
  const top = container.scrollTop + targetRect.top - containerRect.top - 12
  container.scrollTo({ top: Math.max(0, top), behavior })
})

const isPanelNearBottom = () => {
  const el = panelRef.value
  if (!el) return true
  return el.scrollHeight - el.scrollTop - el.clientHeight < 120
}

const shouldFollowPanelBottom = () => ['running', 'waiting_confirmation'].includes(session.state.status)

const scrollPanel = (behavior = 'auto', force = false) => nextTick(() => {
  if (panelRef.value && (force || shouldFollowPanelBottom() || isPanelNearBottom())) {
    panelRef.value.scrollTo({ top: panelRef.value.scrollHeight, behavior })
  }
})

const {
  saveCurrentToHistory,
  restoreHistory,
} = useDataPulseReportHistory({
  session,
  messages,
  datasetId,
  datasets,
  isRunning,
  isDatasetVisible,
  ensureDatasetsReady,
  loadHistory,
  upsertHistory,
  setActiveHistory,
  detailReportResult,
  showPanel,
  thinkingOpen,
  logOpen,
  timelineVersion,
  scrollChat,
  scrollPanel,
  createMessageId: () => ++msgCounter,
})

const scheduleChatScroll = (delay = 40, behavior = 'smooth') => {
  if (isViewingReadonly.value) return
  if (chatScrollTimer) clearTimeout(chatScrollTimer)
  chatScrollTimer = window.setTimeout(() => {
    if (latestAiMessage.value?.data?.research_plan) scrollChatToReportTop(behavior)
    else scrollChat(behavior)
  }, delay)
}

const clearReportTopScrollTimers = () => {
  reportTopScrollTimers.forEach(timer => clearTimeout(timer))
  reportTopScrollTimers = []
}

const scheduleChatReportTop = (delay = 40, behavior = 'auto') => {
  if (isViewingReadonly.value) return
  if (chatScrollTimer) clearTimeout(chatScrollTimer)
  clearReportTopScrollTimers()
  ;[delay, delay + 90, delay + 240].forEach((timeout) => {
    reportTopScrollTimers.push(window.setTimeout(() => {
      scrollChatToReportTop(behavior)
    }, timeout))
  })
}

const schedulePanelScroll = (delay = 150, behavior = 'auto', force = false) => {
  if (panelScrollTimer) clearTimeout(panelScrollTimer)
  panelScrollTimer = window.setTimeout(() => {
    scrollPanel(behavior, force)
  }, delay)
}

const startTimer = () => {
  elapsed.value = 0
  clearInterval(timerInst)
  timerInst = setInterval(() => elapsed.value++, 1000)
}

const compactQuestionText = (value) => String(value || '').replace(/\s+/g, '').toLowerCase()

const isConsumerDatasetMeta = (dataset = {}) => {
  const text = compactQuestionText(`${dataset.dataset_code || ''}${dataset.dataset_name || ''}${dataset.business_domain || ''}${dataset.description || ''}`)
  return text.includes('consumer') || text.includes('消费者') || text.includes('消费事业群')
}

const datasetAliasScore = (text, dataset) => {
  const question = compactQuestionText(text)
  if (!question || !dataset) return 0
  const aliases = [
    dataset.dataset_name,
    dataset.business_domain,
    ...(Array.isArray(dataset.synonyms) ? dataset.synonyms : []),
  ].map(compactQuestionText).filter(Boolean)
  let score = 0
  const suffixes = ['事业群', '战区', '行业部', '片区', '数据集', '销售业绩分析', '业绩分析']
  aliases.forEach((alias) => {
    if (alias.length < 2 || ['业绩', '分析', '数据', '指标', '结果'].includes(alias)) return
    if (question.includes(alias)) score = Math.max(score, 95)
    suffixes.forEach((suffix) => {
      if (!alias.includes(suffix)) return
      const prefix = alias.split(suffix, 1)[0]
      if (prefix.length >= 2 && question.includes(prefix)) score = Math.max(score, 90)
    })
  })
  if (isConsumerDatasetMeta(dataset)) {
    const consumerBranchAliases = ['沧岩战区', '沧岩', '澔岳战区']
    if (consumerBranchAliases.some(alias => question.includes(compactQuestionText(alias)))) {
      score = Math.max(score, 94)
    }
  }
  return score
}

const shouldReleaseSelectedDatasetForQuestion = (text, selectedId) => {
  if (!selectedId) return false
  const selected = datasets.value.find(item => Number(item.id) === Number(selectedId))
  if (!selected) return false
  const selectedScore = datasetAliasScore(text, selected)
  const bestOther = datasets.value
    .filter(item => Number(item.id) !== Number(selectedId))
    .map(item => ({ dataset: item, score: datasetAliasScore(text, item) }))
    .sort((left, right) => right.score - left.score)[0]
  return Boolean(bestOther && bestOther.score >= 90 && bestOther.score >= selectedScore + 12)
}

const getDatasetInputForQuestion = (text) => {
  if (!canUseFeature('ask_dataset_select')) return null
  const pending = pendingQuickDataset.value
  if (pending?.datasetId && String(pending.question || '').trim() === String(text || '').trim()) {
    if (shouldReleaseSelectedDatasetForQuestion(text, pending.datasetId)) return null
    return pending.datasetId
  }
  if (datasetId.value && isDatasetManuallySelected.value) {
    return datasetId.value
  }
  return null
}

const getModelInputForQuestion = () => (
  canUseFeature('ask_model_select') ? modelId.value : null
)

const clearPendingQuickDataset = () => {
  pendingQuickDataset.value = null
}

const submitConfirmationDraft = (msg) => {
  if (!canUseFeature('ask_submit_note')) return
  const text = String(confirmationDrafts[msg?.id] || '').trim()
  if (!text || isRunning.value) return
  doConfirm(text, msg)
}

const handleConfirmationDraftEnter = (event, msg) => {
  if (event?.isComposing) return
  submitConfirmationDraft(msg)
}
const stopTimer = () => clearInterval(timerInst)

const loadQuestions = async () => {
  commonQuestionsLoading.value = true
  try {
    const res = await getCommonQuestions(null, { random: 1, limit: 4, t: Date.now() })
    commonQuestions.value = (res.questions || res.common_questions || []).slice(0, 4)
  } catch {
    commonQuestions.value = []
  } finally {
    commonQuestionsLoading.value = false
  }
}

const handleDatasetChange = async () => {
  if (!canUseFeature('ask_dataset_select')) {
    datasetId.value = null
    isDatasetManuallySelected.value = false
    clearPendingQuickDataset()
    return
  }
  isDatasetManuallySelected.value = Boolean(datasetId.value)
  clearPendingQuickDataset()
  await loadQuestions()
}

const refreshCommonQuestions = async () => {
  if (!canUseFeature('ask_quick_refresh')) return
  if (commonQuestionsLoading.value) return
  await loadQuestions()
}

const getStatusColor = (rate) => {
  const value = toNumber(rate)
  if (value === null) return '#526b7a'
  if (value >= 15) return '#526b7a'
  if (value >= 10) return '#806b47'
  return '#526b7a'
}

const getMetricColor = (column) => {
  const text = String(column || '')
  if (/任务|目标/i.test(text)) return '#526b7a'
  if (/开单|完成|实际|销售/i.test(text)) return '#526b7a'
  if (/剩余|缺口|差额/i.test(text)) return '#806b47'
  if (/率|percent|rate/i.test(text)) return '#806b47'
  return '#6B7280'
}

const sortRowsForChart = (rows = [], columns = [], lowFirst = false, preferredColumn = '') => {
  const targetColumn = preferredColumn
    || columns.find(column => isRateColumn(column))
    || Object.keys(rows[0] || {}).find(column => isRateColumn(column))
  if (!targetColumn) return rows
  return [...rows].sort((a, b) => {
    const left = toNumber(a?.[targetColumn]) || 0
    const right = toNumber(b?.[targetColumn]) || 0
    return lowFirst ? left - right : right - left
  })
}

const renderChartSpec = (chart, data) => {
  const labelColumn = data.columns?.[0]
  const numericColumns = data.columns?.slice(1) || []
  const dataset = data?.dataset || null
  const preferredSortColumn = data.sortColumn || ''
  const sortedRows = sortRowsForChart(data.rows || [], data.columns || [], Boolean(data.lowFirst), preferredSortColumn)
  const colorPalette = ['#425f83', '#8297a4', '#a28e72', '#696780', '#56616e', '#b0bac6']
  const shortSeriesName = (name) => String(name || '')
    .replace(/^年度/, '')
    .replace(/^总/, '')
    .replace('任务金额', '任务')
    .replace('开单金额', '开单')
    .replace('剩余任务金额', '剩余缺口')

  if (data.chartType === 'trend') {
    chart.setOption({
      backgroundColor: 'transparent',
      color: colorPalette,
      tooltip: { trigger: 'axis' },
      legend: { top: 0, textStyle: { color: '#6B7280', fontSize: 11 } },
      grid: { left: 34, right: 18, top: 34, bottom: 28, containLabel: true },
      xAxis: {
        type: 'category',
        data: sortedRows.map(row => row[labelColumn]),
        axisLabel: { color: '#9CA3AF', fontSize: 11, hideOverlap: true },
        axisLine: { lineStyle: { color: '#E5E7EB' } },
      },
      yAxis: {
        type: 'value',
        axisLabel: { color: '#9CA3AF', fontSize: 11 },
        splitLine: { lineStyle: { color: '#F3F4F6', type: 'dashed' } },
      },
      series: numericColumns.map((column, columnIndex) => ({
        name: column,
        type: columnIndex === 0 ? 'bar' : 'line',
        smooth: true,
        barMaxWidth: 18,
        symbolSize: columnIndex === 0 ? 0 : 6,
        itemStyle: { borderRadius: columnIndex === 0 ? [4, 4, 0, 0] : 0 },
        data: sortedRows.map(row => row[column]),
      })),
    })
    return
  }

  if (data.chartType === 'combo') {
    const categoryRows = sortedRows.slice(0, 12)
    const rateColumn = numericColumns.find(column => /率|percent|rate/i.test(column)) || numericColumns[numericColumns.length - 1]
    const barColumns = numericColumns
      .filter(column => column !== rateColumn && !/剩余|缺口|remain/i.test(column))
      .slice(0, 2)
    chart.setOption({
      backgroundColor: 'transparent',
      color: colorPalette,
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      legend: {
        type: 'scroll',
        top: 2,
        left: 8,
        right: 8,
        itemWidth: 10,
        itemHeight: 8,
        icon: 'roundRect',
        formatter: shortSeriesName,
        textStyle: { color: '#6B7280', fontSize: 10 },
      },
      grid: { left: 42, right: 38, top: 68, bottom: 44, containLabel: true },
      xAxis: {
        type: 'category',
        data: categoryRows.map(row => row[labelColumn]),
        axisLabel: { color: '#9CA3AF', fontSize: 11, interval: 0, rotate: categoryRows.length > 4 ? 24 : 0, hideOverlap: true, margin: 12 },
        axisLine: { lineStyle: { color: '#E5E7EB' } },
      },
      yAxis: [
        {
          type: 'value',
          axisLabel: {
            color: '#9CA3AF',
            fontSize: 11,
            formatter: value => {
              const axisColumn = barColumns.find(column => isAmountColumn(column)) || barColumns[0] || ''
              return formatChartAmount(value, dataset, axisColumn)
            },
          },
          splitLine: { lineStyle: { color: '#F3F4F6', type: 'dashed' } },
        },
        {
          type: 'value',
          axisLabel: { color: '#9CA3AF', fontSize: 11, formatter: '{value}%' },
          splitLine: { show: false },
        },
      ],
      series: [
        ...barColumns.map((column) => ({
          name: column,
          type: 'bar',
          barMaxWidth: 18,
          itemStyle: { borderRadius: [4, 4, 0, 0], color: getMetricColor(column) },
          label: isAmountColumn(column) ? {
            show: true,
            position: 'top',
            color: '#6B7280',
            fontSize: 10,
            formatter: ({ value }) => formatChartAmount(value, dataset, column),
          } : undefined,
          data: categoryRows.map(row => ({
            value: row[column],
          })),
        })),
        {
          name: rateColumn,
          type: 'line',
          yAxisIndex: 1,
          smooth: true,
          symbolSize: 6,
          lineStyle: { width: 2.5, color: getMetricColor(rateColumn) },
          label: {
            show: true,
            position: 'top',
            color: '#6B7280',
            fontSize: 10,
            distance: 6,
            formatter: ({ value }) => `${formatDisplayValue(value)}%`,
          },
          data: categoryRows.map(row => ({
            value: row[rateColumn],
            itemStyle: { color: getStatusColor(row[rateColumn]) },
          })),
        },
      ],
    })
    return
  }

  if (data.chartType === 'horizontalRateBar' || data.chartType === 'horizontalDrill') {
    const categoryRows = sortedRows.slice(0, 12).reverse()
    const rateColumn = numericColumns.find(column => isRateColumn(column)) || numericColumns[numericColumns.length - 1]
    const remainColumn = numericColumns.find(column => /剩余|缺口|remain/i.test(column))
    const series = [
      {
        name: rateColumn,
        type: 'bar',
        barMaxWidth: 14,
        itemStyle: { borderRadius: [0, 5, 5, 0] },
        label: {
          show: true,
          position: 'right',
          color: '#6B7280',
          fontSize: 10,
          formatter: ({ value }) => `${formatDisplayValue(value)}%`,
        },
        data: categoryRows.map(row => ({
          value: row[rateColumn],
          itemStyle: { color: getStatusColor(row[rateColumn]) },
        })),
      },
    ]
    if (data.chartType === 'horizontalDrill' && remainColumn) {
      series.push({
        name: remainColumn,
        type: 'bar',
        barMaxWidth: 10,
        itemStyle: { borderRadius: [0, 4, 4, 0], color: '#806b47' },
        label: {
          show: true,
          position: 'right',
          color: '#9CA3AF',
          fontSize: 10,
          formatter: ({ value }) => formatChartAmount(value, dataset, remainColumn),
        },
        data: categoryRows.map(row => row[remainColumn]),
      })
    }
    chart.setOption({
      backgroundColor: 'transparent',
      color: colorPalette,
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      legend: {
        show: series.length > 1,
        top: 2,
        right: 8,
        itemWidth: 10,
        itemHeight: 8,
        textStyle: { color: '#6B7280', fontSize: 10 },
      },
      grid: { left: 78, right: 58, top: series.length > 1 ? 34 : 14, bottom: 18, containLabel: true },
      xAxis: {
        type: 'value',
        axisLabel: { color: '#9CA3AF', fontSize: 11, formatter: value => `${value}%` },
        splitLine: { lineStyle: { color: '#F3F4F6', type: 'dashed' } },
      },
      yAxis: {
        type: 'category',
        data: categoryRows.map(row => row[labelColumn]),
        axisLabel: { color: '#6B7280', fontSize: 11 },
        axisLine: { show: false },
        axisTick: { show: false },
      },
      series,
    })
    return
  }

  if (data.chartType === 'bar') {
    const valueColumn = numericColumns[0]
    chart.setOption({
      backgroundColor: 'transparent',
      color: [colorPalette[0]],
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      grid: { left: 34, right: 18, top: 18, bottom: 48, containLabel: true },
      xAxis: {
        type: 'category',
        data: sortedRows.slice(0, 8).map(row => row[labelColumn]),
        axisLabel: { color: '#9CA3AF', fontSize: 11, interval: 0, rotate: sortedRows.length > 5 ? 18 : 0 },
        axisLine: { lineStyle: { color: '#E5E7EB' } },
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          color: '#9CA3AF',
          fontSize: 11,
          formatter: value => isAmountColumn(valueColumn) ? formatChartAmount(value, dataset, valueColumn) : value,
        },
        splitLine: { lineStyle: { color: '#F3F4F6', type: 'dashed' } },
      },
      series: [{
        type: 'bar',
        barMaxWidth: 22,
        itemStyle: { borderRadius: [5, 5, 0, 0] },
        label: {
          show: true,
          position: 'top',
          color: '#6B7280',
          fontSize: 11,
          fontWeight: 600,
          formatter: ({ value }) => (isAmountColumn(valueColumn) ? formatChartAmount(value, dataset, valueColumn) : formatDisplayValue(value)),
        },
        data: sortedRows.slice(0, 8).map(row => ({
          value: row[valueColumn],
          itemStyle: { color: isRateColumn(valueColumn) ? getStatusColor(row[valueColumn]) : colorPalette[0] },
        })),
      }],
    })
    return
  }

  const valueColumn = numericColumns[0]
  chart.setOption({
    color: colorPalette,
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['48%', '74%'],
      center: ['50%', '52%'],
      avoidLabelOverlap: true,
      label: {
        show: true,
        color: '#6B7280',
        fontSize: 11,
        lineHeight: 16,
        formatter: ({ name, percent, value }) => `${name}\n${formatDisplayValue(value)} · ${percent}%`,
      },
      labelLine: {
        show: true,
        length: 10,
        length2: 8,
        lineStyle: {
          color: 'rgba(0, 0, 0, 0.7)',
        },
      },
      data: sortedRows.slice(0, 6).map(row => ({ name: row[labelColumn], value: row[valueColumn] })),
    }],
  })
}

const chartRenderSignature = (data, key = '') => [
  key,
  data?.chartType || '',
  data?.title || '',
  Array.isArray(data?.columns) ? data.columns.join('|') : '',
  Array.isArray(data?.rows) ? data.rows.length : 0,
  data?.lowFirst ? 'low' : 'high',
].join('::')

const scheduleChartResize = (chart) => {
  if (!chart) return
  requestAnimationFrame(() => chart.resize())
}

const resizeRenderedCharts = () => {
  requestAnimationFrame(() => {
    document
      .querySelectorAll('.ax-inline-visual-chart, .ax-main-chart, .ax-side-extra-chart-canvas, .ax-report-chart-canvas, .ax-office-chart')
      .forEach((el) => {
        const chart = echarts.getInstanceByDom(el)
        if (chart) chart.resize()
      })
    if (chartDialogRef.value) {
      const dialogChart = echarts.getInstanceByDom(chartDialogRef.value)
      if (dialogChart) dialogChart.resize()
    }
  })
}

const initPreviewChart = (el, data, key) => {
  if (!el || !data?.rows?.length || !data?.columns?.length) return
  const signature = chartRenderSignature(data, key)
  nextTick(() => {
    const chart = echarts.getInstanceByDom(el) || echarts.init(el)
    const cached = chartElementCache.get(el)
    if (cached?.signature === signature && cached?.data === data) {
      return
    }
    renderChartSpec(chart, data)
    chartElementCache.set(el, { signature, data })
    scheduleChartResize(chart)
  })
}

const initLogChart = (el, data, key) => {
  if (!el || !data?.rows?.length || !data?.columns?.length) return
  const signature = chartRenderSignature(data, key)
  nextTick(() => {
    const chart = echarts.getInstanceByDom(el) || echarts.init(el)
    const cached = chartElementCache.get(el)
    if (cached?.signature === signature && cached?.data === data) {
      return
    }
    renderChartSpec(chart, data)
    chartElementCache.set(el, { signature, data })
    scheduleChartResize(chart)
  })
}

const renderDialogChart = () => {
  if (!chartViewerVisible.value || chartViewerMode.value !== 'chart' || !chartDialogRef.value || !chartViewerSpec.value) return
  if (chartViewerSpec.value.chartType === 'metric') return
  nextTick(() => {
    const chart = echarts.getInstanceByDom(chartDialogRef.value) || echarts.init(chartDialogRef.value)
    renderChartSpec(chart, chartViewerSpec.value)
    chart.resize()
  })
}

// 监听日志更新，自动展开最新节点
watch(() => session.state.logs.length, (len) => {
  if (len > 0) {
    logOpen[len - 1] = true
    if (!session.state.workflow.run_id) scheduleChatScroll(26, 'smooth')
    schedulePanelScroll(60, 'auto', shouldFollowPanelBottom())
  }
}, { flush: 'post' })

watch(() => session.state.logs.map(log => log.pulseText || '').join('|'), (signature) => {
  if (!signature) return
  if (!session.state.workflow.run_id) scheduleChatScroll(26, 'smooth')
  schedulePanelScroll(60, 'auto', shouldFollowPanelBottom())
}, { flush: 'post' })

watch(() => session.state.status, (s) => {
  syncPendingConfirmationMessage()
  syncCompletedResultMessage()
  if (s === 'completed') {
    nextTick(() => {
      scheduleChatReportTop(0, 'auto')
      if (hasSideReport.value) scrollPanelToReportTop()
    })
  }
  if (s === 'waiting_confirmation') {
    if (!session.state.workflow.run_id) scheduleChatScroll(26, 'smooth')
    schedulePanelScroll(60, 'auto', true)
  }
})

watch(() => session.state.result, () => {
  syncPendingConfirmationMessage()
  syncCompletedResultMessage()
}, { flush: 'post' })

watch(() => hasSideReport.value, (ready) => {
  if (ready && session.state.status === 'completed') {
    scrollPanelToReportTop()
    scheduleChatReportTop(0, 'auto')
  }
}, { flush: 'post' })

watch(() => [chartViewerVisible.value, chartViewerSpec.value, chartViewerMode.value], ([visible]) => {
  if (visible) {
    renderDialogChart()
    return
  }

  if (chartDialogRef.value) {
    const chart = echarts.getInstanceByDom(chartDialogRef.value)
    if (chart) chart.dispose()
  }

  chartViewerMode.value = 'chart'
}, { flush: 'post' })

watch(() => chartViewerMode.value, (mode) => {
  if (mode === 'chart') {
    renderDialogChart()
    return
  }

  if (chartDialogRef.value) {
    const chart = echarts.getInstanceByDom(chartDialogRef.value)
    if (chart) chart.dispose()
  }
})

watch(() => messages.length, () => {
  scheduleChatScroll(24, 'smooth')
}, { flush: 'post' })

const handleReturnToRunning = () => {
  switchViewToRunning()
  const targetId = runningSessionId.value || completedTaskId.value
  if (targetId) {
    setActiveHistory(targetId)
  } else {
    setActiveHistory(null)
  }
}

watch(() => pendingRestoreId.value, async (historyId) => {
  if (!historyId) return
  const item = findHistoryById(historyId)
  if (!item) {
    ElMessage.warning('未找到对应的历史对话记录')
    clearRestoreRequest()
    return
  }
  const options = takePendingRestoreOptions()
  await restoreHistory(item, options)
  if (!options?.readonly) {
    datasetId.value = null
    isDatasetManuallySelected.value = false
  }
  clearRestoreRequest()
}, { flush: 'post', immediate: true })

watch(canViewCharts, (allowed) => {
  if (!allowed) {
    chartViewerVisible.value = false
  }
})

watch(canViewFullscreenReport, (allowed) => {
  if (!allowed) {
    reportViewerVisible.value = false
  }
})

// 已选模型被后端过滤（未测通/同名去重/权限不足）时回退 Auto，避免 el-select 显示裸 id（bug 2026-08-26）
const sanitizeModelSelection = () => {
  if (modelId.value != null && !aiModels.value.some(m => Number(m.id) === Number(modelId.value))) {
    modelId.value = null
  }
}

onMounted(async () => {
  window.addEventListener('datapulse-create-fresh-chat', handleExternalFreshChat)
  loadFeatureFlags()
  refreshAskCapabilities()
  loadHistory()

  // 从 sessionStorage 还原输入状态
  const cached = getSessionCache()
  if (cached.query) query.value = cached.query
  if (cached.modelId !== undefined) modelId.value = cached.modelId

  try {
    const res = await getBookshelfDatasets()
    datasets.value = res.datasets || []
    markDatasetsLoaded()
    sanitizeDatasetSelection()
    await loadQuestions()
  } catch {}

  try {
    const modelRes = await getActiveAIModels()
    aiModels.value = modelRes.models || []
    sanitizeModelSelection()
  } catch {}

  if (session.state.selectedDatasetId && !isDatasetVisible(session.state.selectedDatasetId)) {
    session.state.selectedDatasetId = null
  }

  // 页面重新打开时不自动回灌旧结果；历史恢复仍通过显式操作触发。
  // 守卫细节见 clearStaleSessionState 定义处（L1346 区域）。
  clearStaleSessionState()
})

// keep-alive 重新激活时刷新引用数据（数据集、模型可能在其他页面被修改）
onActivated(async () => {
  refreshAskCapabilities()
  try {
    const res = await getBookshelfDatasets()
    datasets.value = res.datasets || []
    markDatasetsLoaded()
    sanitizeDatasetSelection()
  } catch {}
  try {
    const modelRes = await getActiveAIModels()
    aiModels.value = modelRes.models || []
    sanitizeModelSelection()
  } catch {}
  loadHistory()
  // keep-alive 切回也会复用旧实例上的 reactive 状态；同样需要清掉刷新/上一次卡死时的残留
  clearStaleSessionState()
})

watch(datasetId, refreshAskCapabilities)
// 将关键输入状态持久化到 sessionStorage，页面跳转后还原
watch([query, datasetId, modelId, isDatasetManuallySelected], ([q, d, m, manual]) => {
  setSessionCache({ query: q, datasetId: manual ? d : null, modelId: m })
}, { flush: 'post' })

onDeactivated(() => {
  if(questionQueue.value.length)pauseQuestionQueue('已离开问数页，返回后可继续队列')
  // keep-alive 停用时的轻量清理（不销毁组件状态）
  if (chatScrollTimer) clearTimeout(chatScrollTimer)
  if (panelScrollTimer) clearTimeout(panelScrollTimer)
  clearReportTopScrollTimers()
})

onUnmounted(() => {
  window.removeEventListener('datapulse-create-fresh-chat', handleExternalFreshChat)
  stopTimer()
  if (chatScrollTimer) clearTimeout(chatScrollTimer)
  if (panelScrollTimer) clearTimeout(panelScrollTimer)
  clearReportTopScrollTimers()
  if (activePrintFrame?.parentNode) {
    activePrintFrame.parentNode.removeChild(activePrintFrame)
    activePrintFrame = null
  }
  if (chartDialogRef.value) {
    const chart = echarts.getInstanceByDom(chartDialogRef.value)
    if (chart) chart.dispose()
  }
})
</script>

<style scoped>
/* ===== 页面布局 ===== */
/* 新版外壳：工作台改为全宽画布（去掉悬浮卡片外壳），内容仍在居中轨道内 */
.ax-page {
  height: 100%;
  background: var(--bg-page, #f5f7fa);
  overflow: hidden;
  font-family: var(--font-sans, 'Microsoft YaHei UI', 'Microsoft YaHei', 'PingFang SC', sans-serif);
  font-size: 14px;
  color: var(--text-title);
  padding: 0;
  box-sizing: border-box;
  --ax-content-width: 960px;
  --ax-content-gutter: 24px;
}

.ax-page :is(button, div, span) {
  transition:
    color 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    background-color 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    border-color 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    opacity 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.ax-shell {
  height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.ax-workspace {
  flex: 1;
  min-height: 0;
  display: flex;
  overflow: hidden;
  gap: 0;
  border: 0;
  border-radius: 0;
  background: #FFFFFF;
  box-shadow: none;
  backdrop-filter: none;
}

.ax-workspace.is-detail-hidden {
  max-width: none;
  width: 100%;
  margin: 0 auto;
}

/* ===== 对话区 ===== */
.ax-chat-panel {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  background: #FFFFFF;
  border-radius: 0;
}

.ax-chat-panel.is-detail-hidden {
  max-width: none;
  width: 100%;
  margin: 0 auto;
  border-radius: 0;
}

.ax-content-track {
  width: min(100% - calc(var(--ax-content-gutter) * 2), var(--ax-content-width));
  max-width: var(--ax-content-width);
  margin-left: auto;
  margin-right: auto;
  box-sizing: border-box;
}

.ax-header-track {
  flex: 0 0 auto;
}

.ax-header-track :deep(.ax-header) {
  width: 100%;
  padding-left: 0;
  padding-right: 0;
}

.ax-chat-content {
  flex: 1 0 auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ax-composer-track {
  flex: 0 0 auto;
  /* 贴底通栏：突破 960px 居中轨道，dock 背景/分隔线全宽，内容内部限宽 */
  width: calc(100% - 80px);
  max-width: 1120px;
  padding: 0;
}

/* 只读视图提示条 */
.ax-readonly-banner {
  flex: 0 0 auto;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13.5px;
  line-height: 1.5;
  cursor: pointer;
  margin: 0 20px 12px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.ax-readonly-banner:hover {
  transform: translateY(-1px);
}

.ax-readonly-banner.banner-running {
  background: linear-gradient(90deg, rgba(66, 95, 131, 0.06) 0%, rgba(66, 95, 131, 0.02) 100%);
  border-left: 4px solid #425f83;
  color: #8b6064;
  box-shadow: 0 3px 10px rgba(66, 95, 131, 0.08);
}

.ax-readonly-banner.banner-running:hover {
  background: linear-gradient(90deg, rgba(66, 95, 131, 0.1) 0%, rgba(66, 95, 131, 0.04) 100%);
  box-shadow: 0 4px 14px rgba(66, 95, 131, 0.14);
}

.ax-readonly-banner.banner-completed {
  background: linear-gradient(90deg, rgba(82, 107, 122, 0.06) 0%, rgba(82, 107, 122, 0.02) 100%);
  border-left: 4px solid #526b7a;
  color: #526b7a;
  box-shadow: 0 3px 10px rgba(82, 107, 122, 0.08);
}

.ax-readonly-banner.banner-completed:hover {
  background: linear-gradient(90deg, rgba(82, 107, 122, 0.1) 0%, rgba(82, 107, 122, 0.04) 100%);
  box-shadow: 0 4px 14px rgba(82, 107, 122, 0.14);
}

.ax-readonly-banner.banner-pending_confirmation {
  background: linear-gradient(90deg, rgba(128, 107, 71, 0.06) 0%, rgba(128, 107, 71, 0.02) 100%);
  border-left: 4px solid #806b47;
  color: #806b47;
  box-shadow: 0 3px 10px rgba(128, 107, 71, 0.08);
}

.ax-readonly-banner.banner-pending_confirmation:hover {
  background: linear-gradient(90deg, rgba(128, 107, 71, 0.1) 0%, rgba(128, 107, 71, 0.04) 100%);
  box-shadow: 0 4px 14px rgba(128, 107, 71, 0.14);
}

.ax-readonly-banner.banner-failed {
  background: linear-gradient(90deg, rgba(178, 147, 150, 0.06) 0%, rgba(178, 147, 150, 0.02) 100%);
  border-left: 4px solid #b29396;
  color: #8b6064;
  box-shadow: 0 3px 10px rgba(178, 147, 150, 0.08);
}

.ax-readonly-banner.banner-failed:hover {
  background: linear-gradient(90deg, rgba(178, 147, 150, 0.1) 0%, rgba(178, 147, 150, 0.04) 100%);
  box-shadow: 0 4px 14px rgba(178, 147, 150, 0.14);
}

.ax-spin-ring-small {
  position: relative;
  width: 16px;
  height: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.ax-spin-ring-track-small {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid currentColor;
  opacity: 0.25;
}
.ax-spin-ring-bar-small {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid transparent;
  border-top-color: currentColor;
  animation: ax-ring-spin-small 0.8s linear infinite;
}
@keyframes ax-ring-spin-small {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.ax-readonly-banner-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.ax-readonly-banner-text {
  flex: 1;
  line-height: 1.4;
}

/* 聊天区 */
.ax-chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 0 0 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: #FFFFFF;
}

.ax-chat-panel.is-detail-hidden .ax-chat-body {
  padding-left: 0;
  padding-right: 0;
}

/* 消息 */
.ax-msg-list {
  display: flex;
  flex-direction: column;
  gap: 0;
  width: 100%;
}
.ax-msg-wrap {
  animation: ax-fadein 0.3s ease-out;
  width: 100%;
  max-width: var(--ax-content-width);
}

.ax-chat-panel.is-detail-hidden .ax-msg-list {
  width: 100%;
  align-items: stretch;
}

.ax-chat-panel.is-detail-hidden .ax-msg-wrap {
  width: 100%;
  max-width: var(--ax-content-width);
}

.ax-chat-panel :deep(.cmp) {
  width: 100%;
  max-width: none;
  margin: 0;
}

/* dock 通栏，内容与消息阅读区对齐（960px 居中） */
.ax-chat-panel :deep(.cmp-dock) {
  padding-left: max(20px, calc((100% - var(--ax-content-width, 960px)) / 2));
  padding-right: max(20px, calc((100% - var(--ax-content-width, 960px)) / 2));
}
@keyframes ax-fadein {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

/* AI回复包装 */
.ax-ai-wrap {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin: 10px 0;
}
.ax-ai-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}
.ax-ai-avatar {
  width: 40px;
  height: 40px;
  position: relative;
  overflow: visible;
  background: transparent;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 0;
  box-shadow: 0 4px 12px rgba(66, 95, 131, 0.18);
  padding: 0;
}

.ax-ai-avatar::before {
  content: none;
}

.ax-ai-avatar::after {
  content: '';
  position: absolute;
  right: 1px;
  bottom: 1px;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #526b7a;
  box-shadow:
    0 0 0 3px #FFFFFF,
    0 4px 9px rgba(82, 107, 122, 0.18);
}

.ax-ai-avatar-img {
  display: none;
}

.ax-ai-avatar-svg {
  width: 40px;
  height: 40px;
  display: block;
}
.ax-ai-name {
  font-size: 14.5px;
  font-weight: 700;
  color: #1E293B;
  letter-spacing: 0.2px;
}
.ax-ai-cards {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding-left: 52px;
  max-width: 900px;
}

.ax-chat-panel.is-detail-hidden .ax-ai-cards {
  max-width: 880px;
}

/* 通用卡片样式优化 */
.ax-card {
  background: #ffffff;
  border-radius: 6px;
  border: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow: 
    0 1px 3px rgba(15, 23, 42, 0.04),
    0 4px 12px rgba(15, 23, 42, 0.03);
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.ax-card:hover {
  box-shadow: 
    0 2px 6px rgba(15, 23, 42, 0.05),
    0 8px 20px rgba(15, 23, 42, 0.06);
}

.ax-result-chain {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  padding-top: 14px;
  margin-top: 1px;
  border-top: 1px dashed rgba(17, 24, 39, 0.1);
  animation: ax-curtain-open 0.32s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: top center;
}

.ax-result-chain > * {
  width: 100%;
}

.ax-result-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  max-width: 720px;
  padding: 30px 24px;
  border-radius: 4px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.92) 0%, rgba(248, 249, 250, 0.88) 100%);
  border: 1px dashed rgba(17, 24, 39, 0.1);
  box-shadow: 0 16px 28px rgba(15, 23, 42, 0.04);
  text-align: center;
}

.ax-result-empty-icon {
  font-size: 32px;
  line-height: 1;
  opacity: 0.85;
}

.ax-result-empty-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-title, #111827);
}

.ax-result-empty-desc {
  font-size: 13px;
  line-height: 1.75;
  color: var(--text-secondary, #6B7280);
  max-width: 520px;
}

.ax-chat-panel.is-detail-hidden .ax-result-chain,
.ax-chat-panel.is-detail-hidden .ax-inline-visuals,
.ax-chat-panel.is-detail-hidden .ax-flow-handoff,
.ax-chat-panel.is-detail-hidden .ax-confirm-card {
  max-width: 880px;
}

.ax-inline-visuals {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  max-width: 980px;
  padding: 14px;
  border-radius: 6px;
  border: 1px solid rgba(66, 95, 131, 0.1);
  background: linear-gradient(180deg, #edf2f8 0%, #ffffff 100%);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.035);
}

.ax-inline-visuals.is-single {
  width: min(100%, 980px);
}

.ax-inline-visuals-head {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.ax-inline-visuals-kicker {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #425f83;
}

.ax-inline-visuals-title {
  margin-top: 5px;
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.ax-inline-visuals-caption {
  margin-top: 4px;
  font-size: 11px;
  line-height: 1.65;
  color: #9CA3AF;
}

.ax-inline-visuals-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.ax-inline-visuals-grid.is-single {
  grid-template-columns: minmax(0, 1fr);
  justify-content: start;
}

.ax-inline-visual-card {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 12px;
  border-radius: 5px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #ffffff;
}

.ax-inline-visual-card-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}

.ax-inline-visual-card-title {
  font-size: 13px;
  font-weight: 600;
  color: #111827;
  line-height: 1.5;
}

.ax-inline-visual-card-subtitle {
  margin-top: 3px;
  font-size: 11px;
  color: #9CA3AF;
}

.ax-inline-visual-chart {
  height: 320px;
  border-radius: 5px;
  overflow: hidden;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.ax-inline-visuals-grid.is-single .ax-inline-visual-chart {
  height: 360px;
}

/* 加载动画 */
.ax-thinking-loading {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  background: #FFFFFF;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 6px;
  width: fit-content;
  min-width: 320px;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.04);
}
.ax-dots {
  display: flex;
  gap: 4px;
}
.ax-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #1A1A1A;
  animation: dot-pulse 1.2s ease-in-out infinite;
}
.ax-dots span:nth-child(2) { animation-delay: 0.2s; }
.ax-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes dot-pulse {
  0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
  40% { opacity: 1; transform: scale(1); }
}
.ax-thinking-text {
  font-size: 13px;
  color: #6B7280;
}

/* 确认区 */
.ax-flow-handoff {
  width: 100%;
  padding: 12px 14px;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: linear-gradient(180deg, #edf2f5 0%, #ffffff 100%);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.035);
}

.ax-flow-handoff-kicker {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #1A1A1A;
}

.ax-flow-handoff-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.ax-flow-badge {
  flex: none;
  padding: 3px 8px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  border: 1px solid rgba(26, 26, 26, 0.12);
  background: #F3F4F6;
  color: #1A1A1A;
}

.ax-flow-badge.is-advanced {
  border-color: rgba(82, 107, 122, 0.22);
  background: #edf2f5;
  color: #526b7a;
}

.ax-flow-handoff-title {
  margin-top: 5px;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.55;
  color: #111827;
}

.ax-flow-handoff-desc {
  margin-top: 5px;
  font-size: 12px;
  line-height: 1.65;
  color: #6B7280;
}

.ax-clarify-strip {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  width: 100%;
  padding: 8px 12px;
  margin-bottom: 8px;
  border: 1px solid rgba(66, 95, 131, 0.18);
  border-radius: 4px;
  background: rgba(66, 95, 131, 0.04);
  font-size: 13px;
  line-height: 1.5;
}
.ax-clarify-icon {
  flex: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: rgba(66, 95, 131, 0.12);
  color: #425f83;
  font-size: 12px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.ax-clarify-text {
  color: #334155;
}
.ax-clarify-reason {
  display: block;
  color: #94a3b8;
  font-size: 12px;
}
.ax-clarify-chips {
  display: inline-flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-left: auto;
}
.ax-clarify-chip {
  border: 1px solid rgba(66, 95, 131, 0.35);
  background: #fff;
  color: #425f83;
  border-radius: 999px;
  padding: 3px 12px;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}
.ax-clarify-chip:hover:not(:disabled) {
  background: #425f83;
  color: #fff;
}
.ax-clarify-chip:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
/* 纠正条/错字卡自由输入：推荐候选都不是时直接输入新问句 */
.ax-clarify-freeform {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}
.ax-clarify-freeform-inline {
  flex: 1;
  min-width: 220px;
  max-width: 360px;
  width: auto;
}
.ax-clarify-input {
  flex: 1;
  min-width: 0;
  height: 30px;
  padding: 0 10px;
  border: 1px solid #d7c6c8;
  border-radius: 6px;
  font-size: 13px;
  color: #333;
  background: #fff;
  outline: none;
}
.ax-clarify-input:focus {
  border-color: #8b6064;
}
.ax-clarify-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.ax-clarify-send {
  flex-shrink: 0;
  height: 30px;
  padding: 0 14px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  color: #fff;
  background: #8b6064;
  cursor: pointer;
}
.ax-clarify-send:hover:not(:disabled) {
  background: #8b6064;
}
.ax-clarify-send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
/* 错字短路纠正卡（第 0 层快检）：细条的醒目放大版，只出此卡 */
.ax-early-clarify {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  padding: 14px 16px;
  margin-bottom: 8px;
  border: 1px solid rgba(66, 95, 131, 0.3);
  border-radius: 5px;
  background: rgba(66, 95, 131, 0.05);
}
.ax-early-clarify-head {
  display: flex;
  align-items: center;
  gap: 8px;
}
.ax-early-clarify-title {
  color: #334155;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.5;
}
.ax-early-clarify-body {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}
.ax-early-clarify-label {
  color: #617085;
  font-size: 13px;
}
.ax-early-clarify-chip {
  padding: 5px 14px;
  font-size: 13px;
  font-weight: 600;
}
.ax-early-clarify-continue {
  align-self: flex-start;
  border: none;
  background: transparent;
  color: #94a3b8;
  font-size: 12px;
  padding: 2px 0;
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 3px;
}
.ax-early-clarify-continue:hover:not(:disabled) {
  color: #425f83;
}
.ax-early-clarify-continue:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.ax-confirm-card {
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 5px;
  background: #fff;
  width: 100%;
  padding: 12px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
}
.ax-confirm-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}
.ax-confirm-badge {
  flex: 0 0 auto;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  background: #f5f2ec;
  color: #806b47;
}
.ax-confirm-q {
  flex: 1 1 auto;
  font-size: 13px;
  color: var(--text-title);
  line-height: 1.5;
}
.ax-confirm-opts {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.ax-confirm-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.ax-confirm-row {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  min-height: 48px;
  text-align: left;
  padding: 7px 10px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  color: #111827;
  background: #fff;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.12s;
}
.ax-confirm-row:hover {
  background: #F3F4F6;
  border-color: rgba(26, 26, 26, 0.2);
}
.ax-confirm-row-top {
  border-color: rgba(26, 26, 26, 0.24);
  background: #F3F4F6;
  font-weight: 600;
}
.ax-confirm-row-top .ax-confirm-rank {
  background: #1A1A1A;
  color: #fff;
}
.ax-confirm-row-top .ax-confirm-score {
  background: rgba(26, 26, 26, 0.1);
  color: #1A1A1A;
  font-weight: 700;
}
.ax-confirm-rank {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 5px;
  background: rgba(26, 26, 26, 0.06);
  color: #1A1A1A;
  font-size: 10px;
  font-weight: 700;
}
.ax-confirm-info {
  flex: 0 1 auto;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.ax-confirm-row-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 13px;
  font-weight: 600;
  color: #111827;
}
.ax-confirm-row-desc {
  font-size: 11px;
  line-height: 1.4;
  color: #9CA3AF;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.ax-confirm-recommended {
  flex: 0 0 auto;
  padding: 1px 5px;
  border-radius: 4px;
  background: #425f83;
  color: #fff;
  font-size: 10px;
  font-weight: 600;
}
.ax-confirm-spacer {
  flex: 1 0 auto;
}
.ax-confirm-score {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 48px;
  height: 20px;
  padding: 0 7px;
  border-radius: 999px;
  background: rgba(26, 26, 26, 0.06);
  color: #1A1A1A;
  font-size: 11px;
  font-weight: 600;
}
.ax-confirm-toggle {
  margin-top: 4px;
  width: 100%;
  height: 32px;
  border-radius: 4px;
  border: 1px dashed rgba(26, 26, 26, 0.2);
  background: #fff;
  color: #1A1A1A;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.ax-confirm-toggle:hover {
  background: #F3F4F6;
}

.ax-confirm-freeform {
  margin-top: 10px;
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.ax-confirm-textarea {
  flex: 1 1 auto;
  min-width: 0;
  min-height: 36px;
  height: 36px;
  resize: none;
  padding: 8px 10px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: #fff;
  font-size: 12px;
  line-height: 1.5;
  color: #111827;
  outline: none;
  box-sizing: border-box;
}

.ax-confirm-textarea:focus {
  border-color: rgba(26, 26, 26, 0.35);
  box-shadow: 0 0 0 2px rgba(26, 26, 26, 0.06);
}

.ax-confirm-textarea::placeholder {
  color: #9CA3AF;
}

.ax-confirm-send {
  flex: 0 0 auto;
  height: 36px;
  padding: 0 14px;
  border-radius: 4px;
  border: none;
  background: #425f83;
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.ax-confirm-send:disabled,
.ax-confirm-row:disabled,
.ax-confirm-toggle:disabled {
  opacity: 0.55;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.ax-confirm-submitted {
  max-width: 760px;
  padding: 14px 16px;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: linear-gradient(180deg, #edf2f5 0%, #ffffff 100%);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.035);
}

.ax-confirm-submitted-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.ax-confirm-submitted-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #425f83;
  box-shadow: 0 0 0 5px rgba(66, 95, 131, 0.08);
}

.ax-confirm-submitted-title {
  font-size: 13px;
  font-weight: 700;
  color: #425f83;
}

.ax-confirm-submitted-desc {
  font-size: 12px;
  line-height: 1.65;
  color: #6B7280;
}

/* 状态提示区 */
.ax-error-card,
.ax-cancel-card {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 12px 16px;
  border-radius: 6px;
  max-width: 760px;
}

.ax-error-card {
  background: #edf2f8;
  border: 1px solid #edf2f8;
  color: var(--error);
}

.ax-cancel-card {
  align-items: flex-start;
  position: relative;
  overflow: hidden;
  gap: 12px;
  padding: 14px 16px;
  background:
    linear-gradient(90deg, rgba(0, 0, 0, 0.035) 1px, transparent 1px),
    linear-gradient(180deg, rgba(0, 0, 0, 0.035) 1px, transparent 1px),
    radial-gradient(circle at 12% 18%, rgba(66, 95, 131, 0.16), transparent 30%),
    linear-gradient(135deg, #edf2f5 0%, #edf2f8 54%, #edf2f8 100%);
  background-size: 18px 18px, 18px 18px, auto, auto;
  border: 1px solid rgba(66, 95, 131, 0.22);
  color: #111827;
  box-shadow:
    0 12px 28px rgba(66, 95, 131, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.84);
}

.ax-cancel-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  border-left: 3px solid #425f83;
  pointer-events: none;
}

.ax-cancel-card::after {
  content: '';
  position: absolute;
  right: 14px;
  top: 13px;
  width: 58px;
  height: 16px;
  border-top: 1px solid rgba(66, 95, 131, 0.2);
  border-right: 1px solid rgba(66, 95, 131, 0.42);
  transform: skewX(-24deg);
  pointer-events: none;
}

.ax-cancel-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  position: relative;
  margin-top: 2px;
  border-radius: 50%;
  background:
    radial-gradient(circle, rgba(255, 255, 255, 0.96) 0 30%, transparent 31%),
    conic-gradient(from 210deg, rgba(66, 95, 131, 0.18), rgba(66, 95, 131, 0.85), rgba(66, 95, 131, 0.18));
  box-shadow:
    0 0 0 4px rgba(66, 95, 131, 0.06),
    0 0 18px rgba(66, 95, 131, 0.28);
  flex: 0 0 auto;
}

.ax-cancel-icon::before,
.ax-cancel-icon::after {
  content: '';
  position: absolute;
  background: #425f83;
  border-radius: 999px;
}

.ax-cancel-icon::before {
  width: 14px;
  height: 2px;
  transform: rotate(45deg);
}

.ax-cancel-icon::after {
  width: 14px;
  height: 2px;
  transform: rotate(-45deg);
}

.ax-cancel-icon-core {
  position: absolute;
  inset: 7px;
  border-radius: 50%;
  border: 1px solid rgba(66, 95, 131, 0.28);
}

.ax-cancel-copy {
  position: relative;
  z-index: 1;
  min-width: 0;
}

.ax-cancel-kicker {
  margin-bottom: 3px;
  color: #425f83;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.ax-cancel-title {
  font-size: 14px;
  font-weight: 780;
  color: #111827;
}

.ax-cancel-desc {
  margin-top: 3px;
  font-size: 12px;
  line-height: 1.6;
  color: #6B7280;
}

.ax-link-btn {
  background: none;
  border: none;
  color: #1A1A1A;
  cursor: pointer;
  font-size: 12px;
  padding: 4px 5px;
}

.ax-link-btn:hover {
  text-decoration: underline;
}

.ax-link-btn.danger {
  color: #425f83;
}

/* ===== 右侧面板 ===== */
.ax-detail-panel {
  width: clamp(360px, 34vw, 440px);
  max-width: 42vw;
  height: 100%;
  max-height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-left: 1px solid rgba(17, 24, 39, 0.07);
  background: #FFFFFF;
  box-shadow: none;
  flex-shrink: 0;
}
/* 新版右侧容器：ReasoningPanel（弹性占满）+ 侧栏报告（固定底部）纵向排列 */
.ax-detail-panel-container {
  width: clamp(360px, 34vw, 440px);
  max-width: 42vw;
  height: 100%;
  max-height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #FFFFFF;
  flex-shrink: 0;
}
/* 推理面板优先占满剩余空间，保留最小可用高度；内容在其内部滚动 */
.ax-detail-panel-container > .reasoning-panel {
  flex: 1 1 auto;
  min-height: 260px;
}
/* 侧栏报告封顶 45% 高度并内部滚动，避免长报告把推理面板挤成 0 */
.ax-detail-panel-container > .ax-side-report {
  flex: 0 1 auto;
  min-height: 0;
  max-height: 45%;
  overflow-y: auto;
  overscroll-behavior: contain;
}
.ax-panel-header {
  padding: 28px 28px 24px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 1px solid rgba(17, 24, 39, 0.07);
  background: #FFFFFF;
  flex-shrink: 0;
}
.ax-panel-heading {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 0;
}
.ax-panel-eyebrow {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: 0;
  text-transform: none;
  color: #425f83;
}
.ax-panel-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.ax-panel-title {
  font-size: 21px;
  font-weight: 800;
  color: #111827;
}
.ax-panel-state {
  display: inline-flex;
  align-items: center;
  height: 28px;
  padding: 0 12px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  background: rgba(17, 24, 39, 0.06);
  color: #6B7280;
  box-shadow: inset 0 0 0 1px rgba(17, 24, 39, 0.05);
}
.ax-panel-state.running {
  background: rgba(17, 24, 39, 0.88);
  color: rgba(255, 255, 255, 0.96);
}
.ax-panel-state.completed {
  background: rgba(82, 107, 122, 0.12);
  color: #526b7a;
}
.ax-panel-state.canceled {
  background: rgba(128, 107, 71, 0.12);
  color: #806b47;
}
.ax-panel-state.error {
  background: rgba(66, 95, 131, 0.1);
  color: #425f83;
}
.ax-panel-state.waiting_confirmation {
  background: rgba(128, 107, 71, 0.12);
  color: #806b47;
}
.ax-panel-desc {
  margin: 0;
  font-size: 14px;
  line-height: 1.65;
  color: #7B8491;
  max-width: 360px;
}
.ax-panel-close {
  width: 38px;
  height: 38px;
  border-radius: 6px;
  border: 1px solid rgba(17, 24, 39, 0.06);
  background: rgba(255, 255, 255, 0.92);
  cursor: pointer;
  color: var(--text-muted);
  font-size: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: none;
}

.ax-panel-close:hover {
  color: #1A1A1A;
  border-color: rgba(66, 95, 131, 0.14);
  background: rgba(255, 255, 255, 1);
}
.ax-panel-content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 6px 0 14px;
  overscroll-behavior: contain;
}

/* 数据预览 */
.ax-preview {
  gap: 14px;
}

/* 汇总报告 */
.ax-report-view {
  padding: 0;
}
.ax-report-full {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.ax-kpi-shelf {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.ax-side-section-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}
.ax-side-dataset-name {
  margin-top: 4px;
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}
.ax-side-meta {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  justify-content: flex-end;
}
.ax-side-meta-chip {
  display: inline-flex;
  align-items: center;
  height: 22px;
  padding: 0 9px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.88);
  color: #6B7280;
  font-size: 10px;
  font-weight: 600;
  box-shadow: inset 0 0 0 1px rgba(17, 24, 39, 0.06);
}
.ax-kpi-card {
  flex: 1;
  min-width: 120px;
  border: 1px solid rgba(17, 24, 39, 0.08);
  border-radius: 6px;
  padding: 14px;
  text-align: center;
  background: linear-gradient(180deg, rgba(255, 255, 255, 1) 0%, rgba(251, 252, 253, 0.96) 100%);
  box-shadow:
    0 14px 24px rgba(15, 23, 42, 0.035),
    inset 0 1px 0 rgba(255, 255, 255, 0.92);
}

.ax-kpi-card.is-explained {
  min-height: 92px;
  padding: 14px 16px;
  text-align: left;
}

.ax-kpi-card.is-subject-metric {
  position: relative;
  overflow: hidden;
  border-color: var(--metric-accent-border);
  background: linear-gradient(180deg, var(--metric-accent-soft) 0%, #ffffff 72%);
}

.ax-kpi-card.is-subject-metric::before {
  content: '';
  position: absolute;
  inset: 0 auto 0 0;
  width: 4px;
  background: var(--metric-accent);
}

.ax-kpi-subject {
  margin-bottom: 4px;
  color: var(--metric-accent);
  font-size: 11px;
  font-weight: 800;
  line-height: 1.2;
}

.ax-kpi-card.is-subject-metric .ax-kpi-value {
  color: var(--metric-accent);
}

.ax-kpi-card.is-tone-good .ax-kpi-value {
  color: #526b7a;
}

.ax-kpi-card.is-tone-warn .ax-kpi-value {
  color: #806b47;
}

.ax-kpi-card.is-tone-danger .ax-kpi-value {
  color: #425f83;
}

.ax-kpi-value {
  font-size: 22px;
  font-weight: 800;
  color: rgba(17, 24, 39, 0.92);
  line-height: 1.2;
}
.ax-kpi-label {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 6px;
}

.ax-kpi-hint {
  margin-top: 8px;
  color: #6B7280;
  font-size: 11px;
  line-height: 1.55;
}
.ax-main-chart {
  height: 208px;
  border-radius: 6px;
  overflow: hidden;
  background: #fff;
  border: 1px solid rgba(17, 24, 39, 0.08);
}
.ax-insight-metric {
  min-height: 164px;
  border-radius: 6px;
  border: 1px solid rgba(17, 24, 39, 0.08);
  background: linear-gradient(180deg, #FFFFFF 0%, #edf2f5 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 18px;
}
.ax-insight-metric-value {
  font-size: 25px;
  line-height: 1.2;
  font-weight: 800;
  color: rgba(17, 24, 39, 0.92);
}
.ax-insight-metric-label {
  margin-top: 7px;
  font-size: 12px;
  color: #6B7280;
}
.ax-preview-table {
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid rgba(17, 24, 39, 0.06);
}
.ax-report-md {
  font-size: 13px;
  line-height: 1.72;
  color: var(--text-title);
}
.ax-report-md :deep(h1),
.ax-report-md :deep(h2) {
  color: #111827;
  margin: 14px 0 7px;
}
.ax-report-md :deep(table) {
  width: 100%;
  border-collapse: collapse;
}
.ax-report-md :deep(td),
.ax-report-md :deep(th) {
  border: 1px solid var(--border);
  padding: 5px 8px;
  font-size: 12px;
  text-align: left;
  vertical-align: top;
}
.ax-report-md :deep(th) {
  background: var(--bg-muted);
  font-weight: 600;
}
.ax-download-row {
  text-align: center;
  padding-top: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
.ax-primary-btn {
  height: 34px;
  padding: 0 16px;
  border-radius: 999px;
  background: rgba(17, 24, 39, 0.9);
  color: #fff;
  border: 1px solid rgba(17, 24, 39, 0.14);
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow:
    0 10px 18px rgba(15, 23, 42, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.14);
}
.ax-primary-btn:hover {
  transform: translateY(-1px) scale(1.01);
  box-shadow:
    0 12px 22px rgba(15, 23, 42, 0.14),
    inset 0 1px 0 rgba(255, 255, 255, 0.18);
}

.ax-primary-btn:active {
  transform: scale(0.94);
}

.ax-secondary-btn,
.ax-ghost-btn {
  height: 34px;
  padding: 0 15px;
  border-radius: 999px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.92);
  color: #6B7280;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.ax-btn-label {
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
}

.ax-btn-icon {
  position: relative;
  width: 14px;
  height: 14px;
  display: inline-flex;
  flex-shrink: 0;
}

.ax-btn-icon-stem,
.ax-btn-icon-head,
.ax-btn-icon-tray {
  position: absolute;
  box-sizing: border-box;
}

.ax-btn-icon-stem {
  left: 6px;
  top: 1px;
  width: 2px;
  height: 6px;
  background: currentColor;
  border-radius: 999px;
}

.ax-btn-icon-head {
  left: 4px;
  top: 5px;
  width: 6px;
  height: 6px;
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
  transform: rotate(45deg);
}

.ax-btn-icon-tray {
  position: absolute;
  left: 1px;
  right: 1px;
  bottom: 0;
  height: 4px;
  border: 2px solid currentColor;
  border-top: none;
  border-radius: 0 0 3px 3px;
  box-sizing: border-box;
}

.ax-secondary-btn:hover,
.ax-ghost-btn:hover {
  border-color: rgba(26, 26, 26, 0.14);
  background: rgba(243, 244, 246, 0.92);
  color: #1A1A1A;
  transform: translateY(-1px);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.05);
}

.ax-secondary-btn:active,
.ax-ghost-btn:active,
.ax-panel-close:active,
.ax-link-btn:active,
.ax-confirm-row:active {
  transform: scale(0.985);
}

.ax-side-report {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 0 14px 14px;
  padding: 14px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 6px;
  background: linear-gradient(180deg, #edf2f5 0%, #ffffff 100%);
}

.ax-side-report-head {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.ax-side-report-titlebar {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.ax-side-fullscreen-btn {
  flex-shrink: 0;
  height: 32px;
  padding: 0 12px;
}

.ax-side-confidence {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 4px;
}

.ax-side-confidence-chip {
  display: inline-flex;
  align-items: center;
  height: 24px;
  padding: 0 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 600;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #ffffff;
  color: #6B7280;
}

.ax-side-confidence-chip.is-success {
  background: #edf2f5;
  border-color: rgba(82, 107, 122, 0.16);
  color: #526b7a;
}

.ax-side-confidence-chip.is-info {
  background: #F3F4F6;
  border-color: rgba(26, 26, 26, 0.1);
  color: #1A1A1A;
}

.ax-side-confidence-chip.is-warning {
  background: #f5f2ec;
  border-color: rgba(128, 107, 71, 0.16);
  color: #806b47;
}

.ax-route-decision {
  margin-top: 4px;
  padding: 8px 10px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #edf2f5;
  color: #6B7280;
  font-size: 12px;
  line-height: 1.6;
}

.ax-route-review-note {
  margin: 0;
  padding: 8px 10px;
  border-radius: 4px;
  background: rgba(26, 26, 26, 0.04);
  color: #6B7280;
  font-size: 12px;
  line-height: 1.55;
}

.ax-side-report-kicker {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #1A1A1A;
}

.ax-side-report-title {
  margin: 0;
  font-size: 16px;
  line-height: 1.4;
  color: #111827;
}

.ax-side-report-desc {
  margin: 0;
  font-size: 12px;
  line-height: 1.65;
  color: #6B7280;
}

.ax-business-report {
  gap: 12px;
}

.ax-management-narrative {
  display: grid;
  gap: 10px;
}

.ax-management-narrative.is-dialog {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.ax-management-narrative.is-single-focus,
.ax-management-narrative.is-dialog.is-single-focus {
  grid-template-columns: minmax(0, 1fr);
}

.ax-management-narrative-card {
  padding: 12px 14px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 6px;
  background: linear-gradient(180deg, #ffffff 0%, #edf2f5 100%);
}

.ax-management-narrative.is-single-focus .ax-management-narrative-card {
  border-radius: 4px;
  background: #ffffff;
}

.ax-management-narrative-title {
  margin-bottom: 8px;
  color: #111827;
  font-size: 13px;
  font-weight: 800;
  line-height: 1.35;
}

.ax-management-narrative.is-single-focus .ax-management-narrative-title {
  font-size: 14px;
}

.ax-management-narrative-body {
  color: #374151;
  font-size: 13px;
  line-height: 1.75;
}

.ax-management-narrative-body :deep(p) {
  margin: 0 0 8px;
}

.ax-management-narrative-body :deep(ul) {
  margin: 0;
  padding-left: 18px;
}

.ax-management-narrative-body :deep(li) {
  margin: 4px 0;
}

.ax-business-summary {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.ax-business-summary-text {
  margin: 6px 0 0;
  font-size: 13px;
  line-height: 1.75;
  color: #111827;
}

.ax-filter-answer-card {
  padding: 14px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 4px;
  background: linear-gradient(180deg, #edf2f5, rgba(255, 255, 255, 0.96));
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.04);
}

.ax-filter-answer-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.ax-filter-answer-list {
  display: grid;
  gap: 8px;
  margin-top: 12px;
}

.ax-filter-answer-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto auto;
  align-items: center;
  gap: 10px;
  width: 100%;
  min-height: 38px;
  padding: 8px 10px;
  border: 1px solid rgba(0, 0, 0, 0.22);
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.82);
  color: #111827;
  text-align: left;
  cursor: pointer;
}

.ax-filter-answer-row:hover {
  border-color: rgba(26, 26, 26, 0.2);
  background: #fff;
}

.ax-filter-answer-name {
  min-width: 0;
  overflow: hidden;
  font-size: 13px;
  font-weight: 800;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ax-filter-answer-metric {
  color: #1A1A1A;
  font-size: 12px;
  font-weight: 800;
  white-space: nowrap;
}

.ax-business-risk-pill,
.ax-office-rate {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 24px;
  padding: 0 9px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}

.ax-business-risk-pill.good,
.ax-office-rate.good {
  color: #526b7a;
  background: #edf2f5;
}

.ax-business-risk-pill.warn,
.ax-office-rate.warn {
  color: #806b47;
  background: #f5f2ec;
}

.ax-business-risk-pill.danger,
.ax-office-rate.danger {
  color: #425f83;
  background: #edf2f8;
}

.ax-business-risk-pill.neutral,
.ax-office-rate.neutral {
  color: #6B7280;
  background: #F3F4F6;
}

.ax-office-rate {
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
  line-height: 1.1;
}

.ax-office-rate small {
  font-size: 9px;
  font-weight: 600;
  color: currentColor;
  opacity: 0.8;
}

.ax-office-tag {
  margin-left: 6px;
  color: #6B7280;
  font-size: 11px;
  font-weight: 700;
}

.ax-kpi-shelf-compact .ax-kpi-card {
  min-width: calc(50% - 4px);
  padding: 10px;
}

.ax-office-overview-card {
  padding: 12px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 5px;
  background: #ffffff;
}

.ax-office-overview-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.ax-office-overview-chart {
  width: 100%;
  height: 320px;
  overflow: hidden;
}

.ax-office-overview-dialog {
  margin-bottom: 16px;
}

.ax-office-card-list,
.ax-office-report-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ax-office-report-grid {
  gap: 14px;
}

.ax-office-card {
  border: 1px solid var(--office-accent-border, rgba(0, 0, 0, 0.08));
  border-radius: 5px;
  background: #ffffff;
  overflow: hidden;
}

.ax-office-card-dialog {
  border-radius: 6px;
  border-color: var(--office-accent-border, rgba(0, 0, 0, 0.08));
}

.ax-office-card-head {
  width: 100%;
  min-height: 58px;
  border: none;
  background: #FFFFFF;
  padding: 12px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  text-align: left;
  cursor: pointer;
}

.ax-office-card .ax-office-card-head {
  background: linear-gradient(90deg, var(--office-accent-soft, #FFFFFF) 0%, #FFFFFF 72%);
  border-left: 4px solid var(--office-accent, transparent);
}

.ax-office-card-dialog .ax-office-card-head {
  background: linear-gradient(90deg, var(--office-accent-soft, #FFFFFF) 0%, #FFFFFF 72%);
  border-left: 4px solid var(--office-accent, transparent);
}

.ax-office-card-head:hover {
  background: #edf2f5;
}

.ax-office-head-main {
  flex: 1 1 auto;
  min-width: 0;
}

.ax-office-head-actions {
  flex: 0 0 auto;
  display: inline-flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  min-width: 0;
}

.ax-office-leaf-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 24px;
  padding: 0 10px;
  border-radius: 999px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.92);
  color: #111827;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.75);
}

.ax-office-drill-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-width: 48px;
  min-height: 24px;
  padding: 0 8px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.62);
  color: #6B7280;
  line-height: 1;
  opacity: 0.82;
  transition: border-color 0.18s ease, color 0.18s ease, background 0.18s ease, opacity 0.18s ease;
}

.ax-office-card-head:hover .ax-office-drill-toggle,
.ax-rep-drill-head:hover .ax-office-drill-toggle,
.ax-office-drill-toggle.is-open {
  border-color: var(--office-accent-border, rgba(66, 95, 131, 0.18));
  background: #ffffff;
  color: var(--office-accent, #425f83);
  opacity: 1;
}

.ax-office-drill-toggle span {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 11px;
  font-weight: 800;
}

.ax-office-drill-toggle i {
  width: 6px;
  height: 6px;
  margin-top: -2px;
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
  transform: rotate(45deg);
  transition: transform 0.18s ease;
}

.ax-office-drill-toggle.is-open {
  background: var(--office-accent-soft, #edf2f5);
}

.ax-office-drill-toggle.is-open i {
  margin-top: 2px;
  transform: rotate(225deg);
}

.ax-office-drill-toggle.is-small {
  min-width: 54px;
  min-height: 22px;
  padding: 0 7px;
}

.ax-office-drill-toggle.is-small span {
  font-size: 10px;
}

.ax-office-card .ax-office-card-head:hover {
  background: linear-gradient(90deg, var(--office-accent-soft, #edf2f5) 0%, #edf2f5 72%);
}

.ax-office-card-dialog .ax-office-card-head:hover {
  background: linear-gradient(90deg, var(--office-accent-soft, #edf2f5) 0%, #edf2f5 72%);
}

.ax-office-name {
  font-size: 14px;
  line-height: 1.4;
  font-weight: 700;
  color: #111827;
}

.ax-office-subtitle {
  margin-top: 4px;
  font-size: 11px;
  line-height: 1.45;
  color: #9CA3AF;
}

.ax-office-kpis {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  padding: 10px 12px 0;
}

.ax-office-kpis span {
  min-width: 0;
  padding: 7px 8px;
  border-radius: 4px;
  background: #edf2f5;
  color: #6B7280;
  font-size: 11px;
  line-height: 1.45;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ax-office-copy,
.ax-chart-copy {
  margin: 0;
  color: #6B7280;
  font-size: 12px;
  line-height: 1.75;
}

.ax-office-copy {
  padding: 10px 12px 12px;
}

.ax-office-drill {
  margin: 0 12px 12px;
  position: relative;
  padding: 12px 0 0 14px;
  border-top: 1px dashed rgba(0, 0, 0, 0.1);
}

.ax-office-drill::before {
  content: '';
  position: absolute;
  left: 2px;
  top: 13px;
  bottom: 4px;
  width: 3px;
  border-radius: 999px;
  background: var(--office-accent-soft, rgba(66, 95, 131, 0.12));
  border: 1px solid var(--office-accent-border, rgba(66, 95, 131, 0.16));
}

.ax-drill-path {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 26px;
  padding: 0 10px;
  border-radius: 999px;
  background: var(--office-accent-soft, #edf2f5);
  color: #6B7280;
  font-size: 12px;
  font-weight: 700;
}

.ax-drill-path i {
  width: 18px;
  height: 1px;
  background: var(--office-accent, #425f83);
  position: relative;
}

.ax-drill-path i::after {
  content: '';
  position: absolute;
  right: -1px;
  top: -3px;
  width: 6px;
  height: 6px;
  border-top: 1px solid var(--office-accent, #425f83);
  border-right: 1px solid var(--office-accent, #425f83);
  transform: rotate(45deg);
}

.ax-drill-path strong {
  color: var(--office-accent, #425f83);
}

.ax-drill-insight-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  margin-top: 10px;
}

.ax-drill-insight-card {
  min-width: 0;
  padding: 9px 10px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #ffffff;
}

.ax-drill-insight-card span {
  display: block;
  margin-bottom: 4px;
  color: #9CA3AF;
  font-size: 11px;
  font-weight: 700;
}

.ax-drill-insight-card strong {
  display: block;
  color: #111827;
  font-size: 13px;
  line-height: 1.35;
}

.ax-drill-insight-card.is-good {
  border-color: rgba(82, 107, 122, 0.16);
  background: #edf2f5;
}

.ax-drill-insight-card.is-risk {
  border-color: rgba(66, 95, 131, 0.14);
  background: #edf2f8;
}

.ax-chart-copy-drill {
  margin-top: 10px;
  padding: 8px 10px;
  border-radius: 4px;
  background: #FFFFFF;
}

.ax-drill-table-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: -4px;
  color: #111827;
}

.ax-drill-table-head span {
  font-size: 13px;
  font-weight: 800;
}

.ax-drill-table-head small {
  color: #9CA3AF;
  font-size: 11px;
  font-weight: 500;
}

.ax-office-drill-actions {
  display: flex;
  justify-content: flex-end;
  margin: 8px 0;
}

.ax-office-chart-open {
  height: 28px;
  padding: 0 10px;
  font-size: 11px;
}

.ax-office-chart {
  width: 100%;
  height: 260px;
  overflow: hidden;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #fff;
}

.ax-office-empty-drill {
  margin-top: 8px;
  padding: 14px;
  border: 1px dashed rgba(66, 95, 131, 0.28);
  border-radius: 5px;
  background: linear-gradient(180deg, #edf2f5 0%, #ffffff 100%);
  color: #6B7280;
  font-size: 12px;
  line-height: 1.7;
}

.ax-office-chart-dialog {
  height: 320px;
}

.ax-office-detail-wrap {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 12px;
  margin-top: 10px;
}

.ax-office-detail-wrap.is-dialog {
  grid-template-columns: minmax(0, 1fr);
}

.ax-office-detail-table {
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 4px;
  background: #ffffff;
}

.ax-office-detail-row {
  display: grid;
  grid-template-columns: minmax(82px, 1fr) minmax(118px, 1.12fr) minmax(78px, 0.78fr) minmax(66px, 0.64fr) minmax(124px, 1fr) minmax(74px, 0.74fr);
  gap: 8px;
  align-items: center;
  min-height: 36px;
  padding: 7px 10px;
  color: #374151;
  font-size: 11px;
  line-height: 1.35;
}

.ax-office-detail-row:nth-child(odd):not(.is-head) {
  background: #edf2f5;
}

.ax-office-detail-row.is-head {
  min-height: 32px;
  color: #9CA3AF;
  background: #edf2f5;
  font-weight: 700;
}

.ax-detail-name {
  color: #111827;
  font-weight: 700;
}

.ax-detail-rate,
.ax-detail-tag {
  font-weight: 700;
}

.ax-detail-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 22px;
  width: fit-content;
  max-width: 100%;
  padding: 0 8px;
  border-radius: 999px;
  background: #F3F4F6;
  line-height: 1;
}

.ax-detail-progress {
  min-width: 0;
}

.ax-detail-rate.good,
.ax-detail-tag.good {
  color: #526b7a;
  background: #edf2f5;
}

.ax-detail-rate.warn,
.ax-detail-tag.warn {
  color: #806b47;
  background: #f5f2ec;
}

.ax-detail-rate.danger,
.ax-detail-tag.danger {
  color: #425f83;
  background: #edf2f8;
}

.ax-office-bars {
  display: grid;
  gap: 8px;
  align-content: start;
}

.ax-office-bar-row {
  display: grid;
  grid-template-columns: minmax(54px, 74px) minmax(0, 1fr) minmax(48px, 64px);
  gap: 8px;
  align-items: center;
  color: #6B7280;
  font-size: 11px;
  line-height: 1.35;
}

.ax-office-bar-row span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ax-office-bar-row strong {
  color: #111827;
  font-size: 11px;
  text-align: right;
}

.ax-office-bar-row.is-gap {
  margin-top: -2px;
}

.ax-office-bar-track {
  display: block;
  position: relative;
  height: 8px;
  width: 100%;
  overflow: hidden;
  border-radius: 999px;
  background: #F3F4F6;
}

.ax-office-bar-track i,
.ax-office-bar-track b {
  position: absolute;
  inset: 0 auto 0 0;
  min-width: 2px;
  border-radius: inherit;
}

.ax-office-bar-track .is-rate.good {
  background: #526b7a;
}

.ax-office-bar-track .is-rate.warn {
  background: #806b47;
}

.ax-office-bar-track .is-rate.danger {
  background: #425f83;
}

.ax-office-bar-track .is-gap {
  background: #806b47;
}

.ax-compare-matrix {
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 4px;
  background: #ffffff;
}

.ax-compare-row {
  position: relative;
  width: 100%;
  display: grid;
  grid-template-columns: minmax(110px, 1.05fr) minmax(88px, 0.8fr) minmax(88px, 0.8fr) minmax(88px, 0.8fr) minmax(70px, 0.65fr) minmax(220px, 1.4fr) minmax(82px, 0.75fr);
  gap: 10px;
  align-items: center;
  min-height: 44px;
  padding: 9px 12px;
  border: 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  background: transparent;
  color: #374151;
  font-size: 12px;
  line-height: 1.35;
  text-align: left;
}

.ax-compare-row:not(.is-head) {
  background: linear-gradient(90deg, var(--office-accent-soft, transparent) 0%, #ffffff 46%);
}

.ax-compare-row:not(.is-head)::before {
  content: '';
  position: absolute;
  inset: 0 auto 0 0;
  width: 4px;
  background: var(--office-accent);
}

.ax-compare-row:last-child {
  border-bottom: 0;
}

button.ax-compare-row {
  cursor: pointer;
}

button.ax-compare-row:hover {
  background: linear-gradient(90deg, var(--office-accent-soft, #edf2f5) 0%, #edf2f5 70%);
}

.ax-compare-row.is-head {
  min-height: 36px;
  color: #9CA3AF;
  background: #edf2f5;
  font-weight: 700;
}

.ax-compare-row span {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ax-compare-matrix.is-compact .ax-compare-row {
  grid-template-columns: minmax(78px, 1fr) minmax(64px, 0.75fr) minmax(64px, 0.75fr) minmax(62px, 0.75fr) minmax(58px, 0.7fr) minmax(92px, 1fr) minmax(70px, 0.72fr);
  min-height: 38px;
  padding: 8px 10px;
  gap: 7px;
  font-size: 11px;
}

.ax-compare-matrix.is-compact .ax-compare-row.is-head {
  min-height: 32px;
}

.ax-compare-matrix.is-compact .ax-office-bar-track {
  height: 7px;
}

.ax-compare-row .ax-detail-name {
  color: var(--office-accent);
}

.ax-compare-row .ax-office-bar-track .is-rate {
  background: var(--office-accent);
}

.ax-rep-drill-list {
  grid-column: 1 / -1;
  display: grid;
  gap: 8px;
  margin-top: 2px;
  padding-top: 10px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

.ax-rep-drill-list.is-dialog {
  margin-top: 4px;
}

.ax-rep-drill-title {
  color: #6B7280;
  font-size: 12px;
  font-weight: 700;
}

.ax-rep-drill-card {
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 4px;
  background: #FFFFFF;
}

.ax-rep-drill-head {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 9px 10px;
  border: 0;
  background: transparent;
  color: inherit;
  cursor: pointer;
  text-align: left;
}

.ax-rep-drill-head:hover {
  background: rgba(26, 26, 26, 0.04);
}

.ax-rep-drill-name {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #111827;
  font-size: 13px;
  font-weight: 800;
}

.ax-rep-drill-subtitle {
  margin-top: 2px;
  color: #9CA3AF;
  font-size: 11px;
}

.ax-rep-drill-summary {
  margin: 0;
  padding: 0 10px 9px;
  color: #6B7280;
  font-size: 12px;
  line-height: 1.6;
}

.ax-rep-person-table {
  margin: 0 10px 10px;
}

@media (max-width: 900px) {
  .ax-office-detail-wrap,
  .ax-office-detail-wrap.is-dialog {
    grid-template-columns: minmax(0, 1fr);
  }

  .ax-drill-insight-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .ax-drill-table-head {
    align-items: flex-start;
    flex-direction: column;
    gap: 3px;
  }

  .ax-office-detail-table {
    overflow-x: auto;
  }

  .ax-office-detail-row {
    min-width: 760px;
  }

  .ax-compare-matrix {
    overflow-x: auto;
  }

  .ax-compare-row {
    min-width: 860px;
  }

  .ax-management-narrative.is-dialog {
    grid-template-columns: minmax(0, 1fr);
  }
}

.ax-wide-btn {
  width: 100%;
}

.ax-side-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  border-radius: 6px;
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.ax-side-section-title {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #9CA3AF;
}

/* 内嵌图表 */
.ax-chart-embed {
  height: 188px;
  margin: 6px 0;
  border-radius: 6px;
  overflow: hidden;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.ax-chart-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 6px;
}

/* mini 表格 */
.ax-mini-table-wrap {
  margin: 0;
}
.ax-mini-table {
  border-radius: 6px;
  overflow: hidden;
}
.ax-table-more {
  text-align: center;
  padding: 5px;
  font-size: 11px;
  color: var(--text-muted);
}

.ax-mini-table :deep(.el-table__header-wrapper th) {
  background: #edf2f5;
  color: #6B7280;
  font-size: 11px;
  font-weight: 600;
  height: 34px;
  text-align: left;
}

.ax-mini-table :deep(.el-table__body-wrapper td) {
  font-size: 11px;
  color: #111827;
  text-align: left;
}

.ax-mini-table :deep(.el-table__row:nth-child(even) td) {
  background: #edf2f5;
}

.ax-mini-table :deep(.el-table__inner-wrapper::before) {
  display: none;
}

.ax-preview :deep(.el-table__header-wrapper th) {
  background: #edf2f5;
  color: #6B7280;
  font-size: 11px;
  font-weight: 600;
  height: 34px;
  text-align: left;
}

.ax-preview :deep(.el-table__body-wrapper td) {
  font-size: 11px;
  color: #111827;
  text-align: left;
}

.ax-preview :deep(.el-table__row:nth-child(even) td) {
  background: #edf2f5;
}

.ax-preview :deep(.el-table__inner-wrapper::before) {
  display: none;
}

.ax-side-extra-charts {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 12px;
  margin-top: 12px;
}

.ax-side-chart-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 12px;
}

.ax-side-extra-chart-card {
  padding: 12px 12px 10px;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #FFFFFF;
}

.ax-side-extra-chart-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 8px;
}

.ax-side-extra-chart-title {
  font-size: 13px;
  font-weight: 700;
  color: #111827;
}

.ax-side-extra-chart-action {
  height: 26px;
  padding: 0 10px;
  font-size: 11px;
}

.ax-side-extra-chart-canvas {
  width: 100%;
  height: 280px;
}

.ax-insight-metric-compact {
  min-height: 180px;
}

/* 日志时间 */
.ax-log-time {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  background: #edf2f5;
  color: var(--text-muted);
  font-size: 12px;
  margin-top: 8px;
}

.ax-log-time-label {
  color: #6B7280;
  font-weight: 600;
}

.ax-log-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 10px;
}

.ax-log-section-title {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #9CA3AF;
}

.ax-log-inline-action {
  align-self: flex-end;
}

.ax-log-section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.ax-log-markdown {
  padding: 12px 14px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #FFFFFF;
  font-size: 12px;
  line-height: 1.8;
  color: #111827;
}

.ax-log-markdown :deep(h1),
.ax-log-markdown :deep(h2),
.ax-log-markdown :deep(h3) {
  margin: 0 0 8px;
  color: #111827;
  font-size: 13px;
}

.ax-log-markdown :deep(p),
.ax-log-markdown :deep(ul),
.ax-log-markdown :deep(ol) {
  margin: 0 0 8px;
}

.ax-log-markdown :deep(ul),
.ax-log-markdown :deep(ol) {
  padding-left: 18px;
}

.ax-report-dialog-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

:deep(.ax-report-dialog .el-dialog__header) {
  display: none;
}

.ax-report-dialog-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 2px 2px 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.ax-report-dialog-title-block {
  min-width: 0;
  flex: 1;
}

.ax-report-dialog-title {
  margin: 6px 0 0;
  font-size: 24px;
  line-height: 1.22;
  font-weight: 700;
  color: #111827;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ax-report-dialog-subtitle {
  margin: 7px 0 0;
  max-width: min(980px, 72vw);
  color: #6B7280;
  font-size: 14px;
  line-height: 1.45;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ax-report-dialog-content {
  max-height: 72vh;
  overflow-y: auto;
  padding: 2px 6px 8px 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.ax-report-dialog-overview {
  width: 100%;
  max-width: 1120px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
  gap: 14px;
}

.ax-report-dialog-content.is-template-comparison .ax-report-dialog-overview {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.ax-report-dialog-content.is-template-ranking .ax-report-chart-grid {
  grid-template-columns: minmax(0, 1fr);
}

.ax-report-dialog-content.is-template-detail .ax-report-dialog-overview {
  grid-template-columns: minmax(0, 1fr);
}

.ax-report-dialog-content.is-template-detail .ax-report-stage-metrics .ax-kpi-shelf {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.ax-report-stage-section {
  max-width: 1120px;
  width: 100%;
  margin: 0 auto;
  padding: 16px 18px 16px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 4px;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.ax-report-stage-summary {
  background: linear-gradient(180deg, #ffffff 0%, #FFFFFF 100%);
}

.ax-report-stage-metrics {
  align-self: stretch;
}

.ax-report-stage-metrics .ax-kpi-shelf {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.ax-report-stage-metrics .ax-kpi-card {
  min-width: 0;
}

.ax-report-stage-title {
  margin-bottom: 12px;
  font-size: 20px;
  font-weight: 700;
  line-height: 1.25;
  color: #111827;
}

.ax-report-core-conclusion {
  display: grid;
  gap: 5px;
  margin: 0 0 12px;
  padding: 12px 14px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 4px;
  background: linear-gradient(180deg, #edf2f5 0%, #ffffff 100%);
}

.ax-report-core-conclusion span {
  color: #1A1A1A;
  font-size: 12px;
  font-weight: 800;
}

.ax-report-core-conclusion strong {
  color: #111827;
  font-size: 15px;
  line-height: 1.7;
  font-weight: 800;
}

.ax-report-bullet-list {
  margin: 0;
  padding-left: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: #111827;
  font-size: 14px;
  line-height: 1.8;
}

.ax-report-bullet-list-compact {
  gap: 6px;
  font-size: 13px;
  line-height: 1.7;
  margin-bottom: 12px;
}

.ax-report-sections {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.ax-report-section-card {
  padding: 12px 14px 12px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #FFFFFF;
}

.ax-report-section-card-dialog {
  padding: 16px 18px 16px;
  border-radius: 4px;
  background: #ffffff;
}

.ax-report-section-title {
  margin-bottom: 10px;
  font-size: 18px;
  font-weight: 700;
  line-height: 1.35;
  color: #111827;
}

.ax-report-chart-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.ax-report-chart-card {
  padding: 14px 14px 12px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #ffffff;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.06);
}

.ax-report-chart-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.ax-report-chart-title {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
}

.ax-report-chart-subtitle {
  margin-top: 3px;
  font-size: 12px;
  color: #9CA3AF;
}

.ax-report-chart-canvas {
  width: 100%;
  height: 340px;
}

.ax-report-table-stack {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 10px;
}

.ax-report-table-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.ax-report-table-card {
  padding: 14px 14px 12px;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #FFFFFF;
}

.ax-report-table-card-dialog {
  background: #ffffff;
}

.ax-report-table-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.ax-report-table-title {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
}

.ax-report-table-desc {
  margin-top: 4px;
  font-size: 12px;
  line-height: 1.7;
  color: #9CA3AF;
}

.ax-preview-table-report {
  margin-top: 2px;
}

.ax-preview-table-report :deep(.el-table__header-wrapper th) {
  background: #edf2f5;
  color: #6B7280;
  font-size: 11px;
  font-weight: 600;
  height: 34px;
  text-align: left;
}

.ax-preview-table-report :deep(.el-table__body-wrapper td) {
  font-size: 11px;
  color: #111827;
  text-align: left;
}

.ax-preview-table-report :deep(.el-table__row:nth-child(even) td) {
  background: #edf2f5;
}

.ax-preview-table-report :deep(.el-table__inner-wrapper::before) {
  display: none;
}

.ax-preview-table-report-dialog :deep(.el-table__body-wrapper) {
  max-height: 360px;
  overflow-y: auto;
}

.ax-insight-metric-report {
  min-height: 280px;
}

.ax-report-md-compact {
  font-size: 12px;
  line-height: 1.8;
}

@media (max-width: 1100px) {
  .ax-report-dialog-overview {
    grid-template-columns: 1fr;
  }

  .ax-report-chart-grid {
    grid-template-columns: 1fr;
  }

  .ax-report-table-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .ax-report-dialog-title {
    font-size: 21px;
  }

  .ax-report-stage-section {
    padding: 14px 14px 14px;
  }

  .ax-report-stage-title {
    font-size: 18px;
  }

  .ax-report-bullet-list {
    font-size: 13px;
  }

  .ax-report-chart-grid {
    grid-template-columns: 1fr;
  }

  .ax-report-chart-canvas,
  .ax-insight-metric-report {
    height: 240px;
    min-height: 240px;
  }
}

.ax-chart-dialog-body {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-height: 420px;
}

@keyframes ax-curtain-open {
  from {
    opacity: 0;
    clip-path: inset(0 0 100% 0 round 18px);
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    clip-path: inset(0 0 0 0 round 18px);
    transform: translateY(0);
  }
}

@keyframes ax-stop-beam {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.ax-chart-dialog-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.ax-chart-dialog-kicker {
  font-size: 11px;
  letter-spacing: 0.08em;
  color: #9CA3AF;
}

.ax-chart-dialog-switch {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px;
  border-radius: 999px;
  background: #F3F4F6;
}

.ax-chart-switch-btn {
  border: none;
  background: transparent;
  color: #6B7280;
  font-size: 12px;
  line-height: 1;
  padding: 8px 12px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.18s ease;
}

.ax-chart-switch-btn.is-active {
  background: #ffffff;
  color: #1A1A1A;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.ax-chart-dialog-canvas {
  width: 100%;
  height: 68vh;
  min-height: 420px;
}

.ax-chart-dialog-table {
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 6px;
  overflow: hidden;
  background: #ffffff;
}

.ax-chart-dialog-table-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  font-size: 12px;
  color: #9CA3AF;
  background: #edf2f5;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.ax-insight-metric-large {
  min-height: 420px;
}

:global(.ax-toast-modern.el-message) {
  min-width: 0;
  width: auto;
  max-width: min(420px, calc(100vw - 32px));
  padding: 9px 13px;
  border: 1px solid rgba(66, 95, 131, 0.12);
  border-radius: 4px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(248, 249, 250, 0.98));
  box-shadow:
    0 10px 28px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(10px);
}

:global(.ax-toast-modern .el-message__content) {
  color: #374151;
  font-size: 12px;
  font-weight: 760;
  line-height: 1.35;
}

:global(.ax-toast-modern .el-message__icon) {
  margin-right: 8px;
  font-size: 14px;
}

:global(.ax-toast-modern.el-message--success) {
  border-color: rgba(82, 107, 122, 0.16);
}

:global(.ax-toast-modern.el-message--success .el-message__icon) {
  color: #526b7a;
}

:global(.ax-toast-stop.el-message) {
  border-color: rgba(128, 107, 71, 0.18);
  background:
    linear-gradient(180deg, rgba(245, 242, 236, 0.98), rgba(245, 242, 236, 0.98));
}

:global(.ax-toast-stop .el-message__content) {
  color: #806b47;
}

:global(.ax-toast-stop .el-message__icon) {
  color: #806b47;
}

/* 动画 */
.ax-collapse-enter-active,
.ax-collapse-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}
.ax-collapse-enter-from,
.ax-collapse-leave-to {
  opacity: 0;
  max-height: 0;
}
.ax-collapse-enter-to,
.ax-collapse-leave-from {
  opacity: 1;
  max-height: 800px;
}

.ax-slide-up-enter-active,
.ax-slide-up-leave-active {
  transition: all 0.2s ease;
}
.ax-slide-up-enter-from,
.ax-slide-up-leave-to {
  transform: translateY(10px);
  opacity: 0;
}

.ax-panel-slide-enter-active,
.ax-panel-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.ax-panel-slide-enter-from,
.ax-panel-slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* 滚动区 */
.ax-chat-body::-webkit-scrollbar,
.ax-panel-content::-webkit-scrollbar {
  width: 5px;
}
.ax-chat-body::-webkit-scrollbar-thumb,
.ax-panel-content::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 4px;
}

@media (max-width: 1280px) {
  .ax-page {
    padding: 0;
  }

  .ax-detail-panel,
  .ax-detail-panel-container {
    width: 400px;
    max-width: 42vw;
  }
}

@media (max-width: 1080px) {
  .ax-page {
    height: 100%;
    min-height: 0;
  }

  .ax-workspace {
    flex-direction: column;
  }

  .ax-detail-panel,
  .ax-detail-panel-container {
    width: 100%;
    max-width: none;
    border-left: none;
    border-top: 1px solid rgba(0, 0, 0, 0.08);
    min-height: 320px;
    max-height: 42vh;
  }

  /* 纵向堆叠时容器较矮：推理面板保底 200px（容纳完整头部+步骤条+Tab），报告占剩余并各自内部滚动 */
  .ax-detail-panel-container > .reasoning-panel {
    min-height: 200px;
  }
  .ax-detail-panel-container > .ax-side-report {
    flex: 1 1 auto;
    max-height: none;
  }
}
</style>

<style scoped>
.ax-page { background:#f4f7fa; --ax-content-width:1000px; }
.ax-workspace, .ax-chat-panel, .ax-chat-body { background:#f4f7fa; }
.ax-header-track :deep(.ax-header) { background:transparent; min-height:64px; border-color:#dce5eb; }
.path-selector { display:flex;align-items:center;justify-content:space-between;gap:18px;padding:16px 0 8px;flex-wrap:wrap; }
.path-tabs { display:flex;gap:4px;padding:4px;background:#dce5eb;border-radius:9px; }
.path-tabs button { display:flex;flex-direction:column;align-items:flex-start;gap:2px;padding:9px 16px;border:0;background:transparent;border-radius:6px;color:#75857c;font:inherit;cursor:pointer; }
.path-tabs button[aria-pressed="true"] { background:white;color:#344652;box-shadow:0 2px 6px #3446520a; }
.path-tabs button:disabled { cursor:not-allowed;opacity:.5; }
.path-tabs small { font-size:11px; }.path-tabs span { font-size:13px;font-weight:500; }
.path-scope,.path-policy-note { color:#7c8d82;font-size:11px; }.path-policy-note { margin-top:4px;margin-bottom:0; }
.ax-ai-meta { margin-bottom:16px; }.ax-ai-cards { gap:18px;padding-left:0;max-width:none; }.ax-ai-wrap { margin:10px 0 20px; }
.ax-ai-name { font-size:12px;color:#73867a; }.ax-ai-avatar { width:28px;height:28px; }
.ax-msg-list { gap:30px; }.ax-result-chain { background:#fff;border:1px solid #dce5eb;border-radius:10px;padding:24px;box-shadow:0 4px 20px #34465204; }
.ax-inline-visual-card { box-shadow:none; }.ax-composer-track { padding-top:12px;background:#f4f7fa; }
@media(max-width:1080px){.ax-workspace{flex-direction:column}.ax-chat-panel{min-height:0;flex:1}.ax-chat-body{min-height:0}.ax-detail-panel-container{max-height:42vh}.ax-content-track{width:calc(100% - 32px)}}
@media(max-width:700px){.path-tabs{width:100%}.path-tabs button{flex:1;padding:8px}.path-scope{font-size:11px}.ax-result-chain{padding:16px}.ax-page{--ax-content-gutter:16px}}
@media(prefers-reduced-motion:reduce){.ax-page :deep(*){animation:none!important;transition:none!important;scroll-behavior:auto!important}}
</style>

<style scoped src="../styles/analysisStudio.css"></style>

<style scoped>.html-report-reader{display:block;width:100%;height:72dvh;min-height:400px;border:0;border-radius:10px;background:#edf2f8}</style>
