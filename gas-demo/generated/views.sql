CREATE OR REPLACE VIEW v_gas_org AS
SELECT
  (fields->>'business_key')::text AS "business_key",
  (fields->>'org_id')::text AS "org_id",
  (fields->>'org_name')::text AS "org_name",
  (fields->>'parent_id')::text AS "parent_id",
  (NULLIF(fields->>'org_level', ''))::numeric::bigint AS "org_level",
  (fields->>'org_path')::text AS "org_path",
  (fields->>'org_name_path')::text AS "org_name_path",
  (NULLIF(fields->>'sales_enabled', ''))::numeric::bigint AS "sales_enabled",
  (fields->>'data_version')::text AS "data_version",
  fields->>'org_id' AS "组织编码",
  fields->>'org_path' AS "组织编码路径"
FROM raw_gas_org;

CREATE OR REPLACE VIEW v_gas_sales AS
SELECT
  (fields->>'business_key')::text AS "business_key",
  (fields->>'month')::text AS "month",
  (fields->>'org_id')::text AS "org_id",
  (fields->>'org_name')::text AS "org_name",
  (fields->>'org_path')::text AS "org_path",
  (fields->>'branch_id')::text AS "branch_id",
  (fields->>'branch_name')::text AS "branch_name",
  (fields->>'center_id')::text AS "center_id",
  (fields->>'data_version')::text AS "data_version",
  (fields->>'user_type')::text AS "user_type",
  (NULLIF(fields->>'volume_m3', ''))::numeric::bigint AS "volume_m3",
  (NULLIF(fields->>'price_yuan_m3', ''))::numeric AS "price_yuan_m3",
  (NULLIF(fields->>'theoretical_revenue_yuan', ''))::numeric AS "theoretical_revenue_yuan",
  (NULLIF(fields->>'revenue_yuan', ''))::numeric AS "revenue_yuan",
  (NULLIF(fields->>'audit_difference_yuan', ''))::numeric AS "audit_difference_yuan",
  (NULLIF(fields->>'actual_meter_m3', ''))::numeric::bigint AS "actual_meter_m3",
  (NULLIF(fields->>'estimated_meter_m3', ''))::numeric::bigint AS "estimated_meter_m3",
  (fields->>'tax_basis')::text AS "tax_basis",
  (fields->>'exception_code')::text AS "exception_code",
  fields->>'org_id' AS "组织编码",
  fields->>'org_path' AS "组织编码路径"
FROM raw_gas_sales_monthly;

CREATE OR REPLACE VIEW v_gas_supply_sources AS
SELECT
  (fields->>'business_key')::text AS "business_key",
  (fields->>'month')::text AS "month",
  (fields->>'org_id')::text AS "org_id",
  (fields->>'org_name')::text AS "org_name",
  (fields->>'org_path')::text AS "org_path",
  (fields->>'branch_id')::text AS "branch_id",
  (fields->>'branch_name')::text AS "branch_name",
  (fields->>'center_id')::text AS "center_id",
  (fields->>'data_version')::text AS "data_version",
  (fields->>'source')::text AS "source",
  (NULLIF(fields->>'inlet_m3', ''))::numeric::bigint AS "inlet_m3",
  (NULLIF(fields->>'purchase_price_yuan_m3', ''))::numeric AS "purchase_price_yuan_m3",
  (NULLIF(fields->>'purchase_cost_yuan', ''))::numeric AS "purchase_cost_yuan",
  (NULLIF(fields->>'loss_threshold', ''))::numeric AS "loss_threshold",
  (fields->>'measurement_basis')::text AS "measurement_basis",
  (fields->>'allocation_basis')::text AS "allocation_basis",
  fields->>'org_id' AS "组织编码",
  fields->>'org_path' AS "组织编码路径"
FROM raw_gas_supply_monthly;

CREATE OR REPLACE VIEW v_gas_profit_inputs AS
SELECT
  (fields->>'business_key')::text AS "business_key",
  (fields->>'month')::text AS "month",
  (fields->>'org_id')::text AS "org_id",
  (fields->>'org_name')::text AS "org_name",
  (fields->>'org_path')::text AS "org_path",
  (fields->>'branch_id')::text AS "branch_id",
  (fields->>'branch_name')::text AS "branch_name",
  (fields->>'center_id')::text AS "center_id",
  (fields->>'data_version')::text AS "data_version",
  (NULLIF(fields->>'installation_revenue_yuan', ''))::numeric AS "installation_revenue_yuan",
  (NULLIF(fields->>'installation_cost_yuan', ''))::numeric AS "installation_cost_yuan",
  (NULLIF(fields->>'value_added_revenue_yuan', ''))::numeric AS "value_added_revenue_yuan",
  (NULLIF(fields->>'value_added_cost_yuan', ''))::numeric AS "value_added_cost_yuan",
  (NULLIF(fields->>'distribution_cost_yuan', ''))::numeric AS "distribution_cost_yuan",
  (NULLIF(fields->>'admin_expense_yuan', ''))::numeric AS "admin_expense_yuan",
  (NULLIF(fields->>'finance_expense_yuan', ''))::numeric AS "finance_expense_yuan",
  (NULLIF(fields->>'impairment_yuan', ''))::numeric AS "impairment_yuan",
  (NULLIF(fields->>'pretax_profit_target_yuan', ''))::numeric AS "pretax_profit_target_yuan",
  fields->>'org_id' AS "组织编码",
  fields->>'org_path' AS "组织编码路径"
FROM raw_gas_profit_monthly;

CREATE OR REPLACE VIEW v_gas_ar AS
SELECT
  (fields->>'business_key')::text AS "business_key",
  (fields->>'month')::text AS "month",
  (fields->>'org_id')::text AS "org_id",
  (fields->>'org_name')::text AS "org_name",
  (fields->>'org_path')::text AS "org_path",
  (fields->>'branch_id')::text AS "branch_id",
  (fields->>'branch_name')::text AS "branch_name",
  (fields->>'center_id')::text AS "center_id",
  (fields->>'data_version')::text AS "data_version",
  (fields->>'customer_id')::text AS "customer_id",
  (fields->>'customer_name')::text AS "customer_name",
  (fields->>'object_kind')::text AS "object_kind",
  (fields->>'user_type')::text AS "user_type",
  (NULLIF(fields->>'opening_yuan', ''))::numeric AS "opening_yuan",
  (NULLIF(fields->>'billed_yuan', ''))::numeric AS "billed_yuan",
  (NULLIF(fields->>'collected_yuan', ''))::numeric AS "collected_yuan",
  (NULLIF(fields->>'adjustment_yuan', ''))::numeric::bigint AS "adjustment_yuan",
  (NULLIF(fields->>'closing_yuan', ''))::numeric AS "closing_yuan",
  (NULLIF(fields->>'aging_0_30_yuan', ''))::numeric AS "aging_0_30_yuan",
  (NULLIF(fields->>'aging_31_90_yuan', ''))::numeric AS "aging_31_90_yuan",
  (NULLIF(fields->>'aging_91_180_yuan', ''))::numeric AS "aging_91_180_yuan",
  (NULLIF(fields->>'aging_181_365_yuan', ''))::numeric AS "aging_181_365_yuan",
  (NULLIF(fields->>'aging_365_plus_yuan', ''))::numeric AS "aging_365_plus_yuan",
  (NULLIF(fields->>'provision_yuan', ''))::numeric AS "provision_yuan",
  (fields->>'collection_status')::text AS "collection_status",
  (fields->>'aging_basis')::text AS "aging_basis",
  fields->>'org_id' AS "组织编码",
  fields->>'org_path' AS "组织编码路径"
FROM raw_gas_ar_monthly;

CREATE OR REPLACE VIEW v_gas_growth AS
SELECT
  (fields->>'business_key')::text AS "business_key",
  (fields->>'month')::text AS "month",
  (fields->>'org_id')::text AS "org_id",
  (fields->>'org_name')::text AS "org_name",
  (fields->>'org_path')::text AS "org_path",
  (fields->>'branch_id')::text AS "branch_id",
  (fields->>'branch_name')::text AS "branch_name",
  (fields->>'center_id')::text AS "center_id",
  (fields->>'data_version')::text AS "data_version",
  (fields->>'user_type')::text AS "user_type",
  (NULLIF(fields->>'opening_users', ''))::numeric::bigint AS "opening_users",
  (NULLIF(fields->>'applied_users', ''))::numeric::bigint AS "applied_users",
  (NULLIF(fields->>'connected_users', ''))::numeric::bigint AS "connected_users",
  (NULLIF(fields->>'churn_users', ''))::numeric::bigint AS "churn_users",
  (NULLIF(fields->>'ending_users', ''))::numeric::bigint AS "ending_users",
  (NULLIF(fields->>'bottle_conversion_users', ''))::numeric::bigint AS "bottle_conversion_users",
  (NULLIF(fields->>'potential_users', ''))::numeric::bigint AS "potential_users",
  fields->>'org_id' AS "组织编码",
  fields->>'org_path' AS "组织编码路径"
FROM raw_gas_growth_monthly;

CREATE OR REPLACE VIEW v_gas_safety AS
SELECT
  (fields->>'business_key')::text AS "business_key",
  (fields->>'month')::text AS "month",
  (fields->>'org_id')::text AS "org_id",
  (fields->>'org_name')::text AS "org_name",
  (fields->>'org_path')::text AS "org_path",
  (fields->>'branch_id')::text AS "branch_id",
  (fields->>'branch_name')::text AS "branch_name",
  (fields->>'center_id')::text AS "center_id",
  (fields->>'data_version')::text AS "data_version",
  (NULLIF(fields->>'due_inspect', ''))::numeric::bigint AS "due_inspect",
  (NULLIF(fields->>'inspected', ''))::numeric::bigint AS "inspected",
  (NULLIF(fields->>'not_at_home', ''))::numeric::bigint AS "not_at_home",
  (NULLIF(fields->>'three_piece_installed', ''))::numeric::bigint AS "three_piece_installed",
  (NULLIF(fields->>'emergency_total', ''))::numeric::bigint AS "emergency_total",
  (NULLIF(fields->>'emergency_on_time', ''))::numeric::bigint AS "emergency_on_time",
  (NULLIF(fields->>'leak_count', ''))::numeric::bigint AS "leak_count",
  fields->>'org_id' AS "组织编码",
  fields->>'org_path' AS "组织编码路径"
FROM raw_gas_safety_monthly;

CREATE OR REPLACE VIEW v_gas_network AS
SELECT
  (fields->>'business_key')::text AS "business_key",
  (fields->>'network_id')::text AS "network_id",
  (fields->>'org_id')::text AS "org_id",
  (fields->>'org_name')::text AS "org_name",
  (fields->>'org_path')::text AS "org_path",
  (fields->>'branch_id')::text AS "branch_id",
  (fields->>'branch_name')::text AS "branch_name",
  (fields->>'center_id')::text AS "center_id",
  (fields->>'data_version')::text AS "data_version",
  (fields->>'pressure_level')::text AS "pressure_level",
  (NULLIF(fields->>'length_km', ''))::numeric AS "length_km",
  (fields->>'material')::text AS "material",
  (CASE WHEN fields->>'laid_date' ~ '^[0-9]{13}$' THEN (to_timestamp((fields->>'laid_date')::numeric/1000) AT TIME ZONE 'Asia/Shanghai')::date ELSE NULLIF(fields->>'laid_date', '')::date END)::date AS "laid_date",
  (CASE WHEN fields->>'gis_loaded_date' ~ '^[0-9]{13}$' THEN (to_timestamp((fields->>'gis_loaded_date')::numeric/1000) AT TIME ZONE 'Asia/Shanghai')::date ELSE NULLIF(fields->>'gis_loaded_date', '')::date END)::date AS "gis_loaded_date",
  fields->>'org_id' AS "组织编码",
  fields->>'org_path' AS "组织编码路径"
FROM raw_gas_network_assets;

CREATE OR REPLACE VIEW v_gas_hazards AS
SELECT
  (fields->>'business_key')::text AS "business_key",
  (fields->>'hazard_id')::text AS "hazard_id",
  (fields->>'org_id')::text AS "org_id",
  (fields->>'org_name')::text AS "org_name",
  (fields->>'org_path')::text AS "org_path",
  (fields->>'branch_id')::text AS "branch_id",
  (fields->>'branch_name')::text AS "branch_name",
  (fields->>'center_id')::text AS "center_id",
  (fields->>'data_version')::text AS "data_version",
  (fields->>'network_id')::text AS "network_id",
  (CASE WHEN fields->>'found_date' ~ '^[0-9]{13}$' THEN (to_timestamp((fields->>'found_date')::numeric/1000) AT TIME ZONE 'Asia/Shanghai')::date ELSE NULLIF(fields->>'found_date', '')::date END)::date AS "found_date",
  (CASE WHEN fields->>'due_date' ~ '^[0-9]{13}$' THEN (to_timestamp((fields->>'due_date')::numeric/1000) AT TIME ZONE 'Asia/Shanghai')::date ELSE NULLIF(fields->>'due_date', '')::date END)::date AS "due_date",
  (CASE WHEN fields->>'completed_date' ~ '^[0-9]{13}$' THEN (to_timestamp((fields->>'completed_date')::numeric/1000) AT TIME ZONE 'Asia/Shanghai')::date ELSE NULLIF(fields->>'completed_date', '')::date END)::date AS "completed_date",
  (fields->>'severity')::text AS "severity",
  (fields->>'hazard_type')::text AS "hazard_type",
  (fields->>'status')::text AS "status",
  (CASE WHEN fields->>'as_of_date' ~ '^[0-9]{13}$' THEN (to_timestamp((fields->>'as_of_date')::numeric/1000) AT TIME ZONE 'Asia/Shanghai')::date ELSE NULLIF(fields->>'as_of_date', '')::date END)::date AS "as_of_date",
  fields->>'org_id' AS "组织编码",
  fields->>'org_path' AS "组织编码路径"
FROM raw_gas_hazard_orders;

CREATE OR REPLACE VIEW v_gas_supply_balance AS
WITH s AS (
 SELECT month,center_id,branch_id,branch_name,SUM(volume_m3) AS sales_m3,
 SUM(revenue_yuan) AS sales_revenue_yuan,SUM(estimated_meter_m3) AS estimated_m3
 FROM v_gas_sales GROUP BY month,center_id,branch_id,branch_name
), p AS (
 SELECT month,org_id,org_name,org_path,SUM(inlet_m3) AS inlet_m3,
 SUM(purchase_cost_yuan) AS purchase_cost_yuan,MAX(loss_threshold) AS loss_threshold
 FROM v_gas_supply_sources GROUP BY month,org_id,org_name,org_path
)
SELECT p.*,s.branch_id,s.branch_name,s.sales_m3,s.sales_revenue_yuan,s.estimated_m3,
 p.inlet_m3-s.sales_m3 AS loss_m3,
 (p.inlet_m3-s.sales_m3)/NULLIF(p.inlet_m3,0) AS loss_rate,
 p.org_id AS "组织编码",p.org_path AS "组织编码路径"
FROM p JOIN s ON p.month=s.month AND p.org_id=s.center_id;

CREATE OR REPLACE VIEW v_gas_profit AS
SELECT f.*,COALESCE(b.sales_m3,0) AS sales_m3,
 COALESCE(b.sales_revenue_yuan,0) AS sales_revenue_yuan,
 COALESCE(b.purchase_cost_yuan,0) AS purchase_cost_yuan,
 COALESCE(b.sales_revenue_yuan,0)+f.installation_revenue_yuan+f.value_added_revenue_yuan AS total_revenue_yuan,
 COALESCE(b.sales_revenue_yuan,0)+f.installation_revenue_yuan+f.value_added_revenue_yuan
 -COALESCE(b.purchase_cost_yuan,0)-f.installation_cost_yuan-f.value_added_cost_yuan
 -f.distribution_cost_yuan-f.admin_expense_yuan-f.finance_expense_yuan-f.impairment_yuan AS pretax_profit_yuan
FROM v_gas_profit_inputs f LEFT JOIN v_gas_supply_balance b ON f.month=b.month AND f.org_id=b.org_id;

CREATE OR REPLACE VIEW v_gas_ar_summary AS
SELECT month,org_id,org_name,org_path,branch_id,branch_name,user_type,
 SUM(opening_yuan) AS opening_yuan,SUM(billed_yuan) AS billed_yuan,SUM(collected_yuan) AS collected_yuan,
 SUM(closing_yuan) AS closing_yuan,SUM(provision_yuan) AS provision_yuan,
 SUM(aging_181_365_yuan+aging_365_plus_yuan) AS aging_over_180_yuan,
 org_id AS "组织编码",org_path AS "组织编码路径"
FROM v_gas_ar GROUP BY month,org_id,org_name,org_path,branch_id,branch_name,user_type;
