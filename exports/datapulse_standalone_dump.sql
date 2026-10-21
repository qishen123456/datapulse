-- ====================================================================
-- DataPulse Standard Enterprise Data Schema & Seed Data (v2.0 Standalone)
-- 自编标准企业数据层级与核心架构数据库 Schema
-- ====================================================================

-- 1. 创建销售业绩主表
DROP TABLE IF EXISTS public.smart_sales_performance CASCADE;

CREATE TABLE public.smart_sales_performance (
    id SERIAL PRIMARY KEY,
    year VARCHAR(4) NOT NULL DEFAULT '2026',
    month INTEGER CHECK (month BETWEEN 1 AND 12),
    quarter VARCHAR(2) CHECK (quarter IN ('Q1', 'Q2', 'Q3', 'Q4')),
    group_name VARCHAR(100) NOT NULL DEFAULT '智问科技集团',
    bu_name VARCHAR(100) NOT NULL,            -- 事业部 (企业服务/消费电子/跨境电商/云软件)
    region_name VARCHAR(100),                  -- 区域分公司 (华东/华南/华北/西南/海外)
    department_name VARCHAR(100),              -- 业务团队 (直营零售部/渠道分销部/大客户部)
    business_line VARCHAR(100),                -- 细分业务线 (硬件/SaaS服务/定制开发)
    node_level VARCHAR(20) NOT NULL,           -- 层级: '集团' | '事业部' | '分公司' | '团队'
    target_amount NUMERIC(15, 2) DEFAULT 0,    -- 目标任务金额 (元)
    actual_billing_amount NUMERIC(15, 2) DEFAULT 0, -- 实际开单金额 (元)
    last_year_billing_amount NUMERIC(15, 2) DEFAULT 0, -- 去年同期金额 (元)
    completion_rate NUMERIC(8, 4) GENERATED ALWAYS AS (
        CASE WHEN target_amount > 0 THEN ROUND(actual_billing_amount / target_amount, 4) ELSE 0 END
    ) STORED,
    owner_name VARCHAR(50),                    -- 负责人
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE public.smart_sales_performance IS 'DataPulse 标准销售业绩明细与汇总主表';
COMMENT ON COLUMN public.smart_sales_performance.bu_name IS '事业部名称';
COMMENT ON COLUMN public.smart_sales_performance.region_name IS '区域分公司名称';
COMMENT ON COLUMN public.smart_sales_performance.department_name IS '业务团队名称';
COMMENT ON COLUMN public.smart_sales_performance.node_level IS '层级级别';

-- 2. 插入自编层级标准测试 Seed 数据 (2026年)

-- L1: 集团大盘
INSERT INTO public.smart_sales_performance (year, month, quarter, group_name, bu_name, region_name, department_name, business_line, node_level, target_amount, actual_billing_amount, last_year_billing_amount, owner_name) VALUES
('2026', 8, 'Q3', '智问科技集团', '全集团', '总部大盘', '全公司', '全业务', '集团', 5000000000.00, 2680000000.00, 2400000000.00, '张伟');

-- L2: 四大事业部汇总
INSERT INTO public.smart_sales_performance (year, month, quarter, group_name, bu_name, region_name, department_name, business_line, node_level, target_amount, actual_billing_amount, last_year_billing_amount, owner_name) VALUES
('2026', 8, 'Q3', '智问科技集团', '企业服务事业部', '', '', '总额(未拆分)', '事业部', 1800000000.00, 968000000.00, 890000000.00, '李洋'),
('2026', 8, 'Q3', '智问科技集团', '消费电子事业部', '', '', '总额(未拆分)', '事业部', 1500000000.00, 854000000.00, 780000000.00, '王明'),
('2026', 8, 'Q3', '智问科技集团', '跨境电商事业部', '', '', '总额(未拆分)', '事业部', 900000000.00, 510000000.00, 450000000.00, '陈晨'),
('2026', 8, 'Q3', '智问科技集团', '云软件事业部', '', '', '总额(未拆分)', '事业部', 800000000.00, 348000000.00, 280000000.00, '郑丽');

-- L3: 区域分公司明细 (以企业服务事业部为例)
INSERT INTO public.smart_sales_performance (year, month, quarter, group_name, bu_name, region_name, department_name, business_line, node_level, target_amount, actual_billing_amount, last_year_billing_amount, owner_name) VALUES
('2026', 8, 'Q3', '智问科技集团', '企业服务事业部', '华东分公司', '', '企业解决方案', '分公司', 500000000.00, 280000000.00, 250000000.00, '谢强'),
('2026', 8, 'Q3', '智问科技集团', '企业服务事业部', '华南分公司', '', '企业解决方案', '分公司', 450000000.00, 245000000.00, 230000000.00, '胡杰'),
('2026', 8, 'Q3', '智问科技集团', '企业服务事业部', '华北分公司', '', '企业解决方案', '分公司', 400000000.00, 210000000.00, 190000000.00, '程敏'),
('2026', 8, 'Q3', '智问科技集团', '企业服务事业部', '西南分公司', '', '企业解决方案', '分公司', 250000000.00, 133000000.00, 120000000.00, '何洁'),
('2026', 8, 'Q3', '智问科技集团', '企业服务事业部', '海外分公司', '', '企业解决方案', '分公司', 200000000.00, 100000000.00, 100000000.00, '雷波');

-- L4: 业务团队明细 (华东分公司下属团队)
INSERT INTO public.smart_sales_performance (year, month, quarter, group_name, bu_name, region_name, department_name, business_line, node_level, target_amount, actual_billing_amount, last_year_billing_amount, owner_name) VALUES
('2026', 8, 'Q3', '智问科技集团', '企业服务事业部', '华东分公司', '大客户部', 'KA金融方案', '团队', 250000000.00, 150000000.00, 130000000.00, '李飞'),
('2026', 8, 'Q3', '智问科技集团', '企业服务事业部', '华东分公司', '渠道分销部', '代理渠道', '团队', 150000000.00, 80000000.00, 75000000.00, '刘军'),
('2026', 8, 'Q3', '智问科技集团', '企业服务事业部', '华东分公司', '直营零售部', '中小企业直营', '团队', 100000000.00, 50000000.00, 45000000.00, '王勇');

-- 3. 创建标准数据字典表
DROP TABLE IF EXISTS public.smart_data_dictionary CASCADE;

CREATE TABLE public.smart_data_dictionary (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    column_name VARCHAR(100) NOT NULL,
    semantic_name VARCHAR(100) NOT NULL,
    data_type VARCHAR(50) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO public.smart_data_dictionary (table_name, column_name, semantic_name, data_type, description) VALUES
('smart_sales_performance', 'year', '年份', 'VARCHAR(4)', '业务统计对应年份，如 2026'),
('smart_sales_performance', 'month', '月份', 'INTEGER', '业务统计对应月份 (1-12)'),
('smart_sales_performance', 'quarter', '季度', 'VARCHAR(2)', '对应业务季度 (Q1, Q2, Q3, Q4)'),
('smart_sales_performance', 'group_name', '集团名称', 'VARCHAR(100)', '最高经营主体集团全称'),
('smart_sales_performance', 'bu_name', '事业部', 'VARCHAR(100)', '业务板块/事业部层级名称'),
('smart_sales_performance', 'region_name', '区域分公司', 'VARCHAR(100)', '区域或地理大区分公司名称'),
('smart_sales_performance', 'department_name', '业务团队', 'VARCHAR(100)', '具体业务部门或划拨团队'),
('smart_sales_performance', 'business_line', '细分业务线', 'VARCHAR(100)', '产品或行业细分方向'),
('smart_sales_performance', 'node_level', '层级级别', 'VARCHAR(20)', '组织节点层级 (集团/事业部/分公司/团队)'),
('smart_sales_performance', 'target_amount', '任务金额', 'NUMERIC(15,2)', '年度或月度目标预算金额(元)'),
('smart_sales_performance', 'actual_billing_amount', '年度开单金额', 'NUMERIC(15,2)', '累计实际完成或开单总额(元)'),
('smart_sales_performance', 'last_year_billing_amount', '去年同期金额', 'NUMERIC(15,2)', '上一年度相同周期开单金额(元)'),
('smart_sales_performance', 'completion_rate', '达成率', 'NUMERIC(8,4)', '实际完成金额与目标金额的比率'),
('smart_sales_performance', 'owner_name', '负责人', 'VARCHAR(50)', '节点或指标归口责任人');
