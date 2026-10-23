"""Deterministic business simulation, not measured company data or tariff policy.
Keeps existing schemas, organization IDs and local record namespace stable.
"""
import calendar
import hashlib
import math
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP


def cents(x):
    return int(Decimal(str(x)).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)*100)


def noise(key, low=0, high=1):
    u=int.from_bytes(hashlib.sha256(str(key).encode()).digest()[:8],'big')/2**64
    return low+(high-low)*u


def apply(tables, money):
    sales=tables['gas_sales_monthly']
    # Independent service-area sizes, customer mix and monthly operating fluctuations.
    profiles={'BINJIANG':[.66,.25,.08,.01],'SHAHU':[.59,.22,.18,.01],
              'JINGKAI':[.20,.12,.67,.01],'LINGANG':[.30,.16,.53,.01],'GAOXIN':[.45,.28,.26,.01]}
    names=['居民','商业','工业','公益机构']
    weights=[]
    for r in sales:
        y,m=map(int,r['month'].split('-'));t=r['user_type'];b=r['branch_id']
        mix=profiles[b][names.index(t)]/[.49,.20,.30,.01][names.index(t)]
        demand=noise(r['org_id'],.65,1.35)*mix*noise(r['business_key'],.94,1.06)
        demand*=calendar.monthrange(y,m)[1]/30.44
        if t=='工业' and m==2: demand*=.65 # holiday shutdown, demo assumption
        if t=='商业' and m in (1,2): demand*=1.08
        if b=='LINGANG' and t=='工业' and r['month'] in ('2026-08','2026-09'): demand*=.78 if m==8 else .64
        weights.append(r['volume_m3']*demand)
    # Retain the documented 2024 annual anchor, without equal grid allocations.
    scale=1_850_000_000/sum(v for r,v in zip(sales,weights) if r['month'].startswith('2024'))
    for r,v in zip(sales,weights):
        y,m=map(int,r['month'].split('-'));t=r['user_type'];b=r['branch_id']
        r['volume_m3']=round(v*scale)
        price=({'居民':2.55,'商业':3.60,'工业':3.48,'公益机构':2.58}[t])
        if t in ('商业','工业'):
            price+=.07*math.cos((m-2)/12*2*math.pi)+noise((b,t),-.12,.09)+noise((r['org_id'],r['month'],t),-.025,.025)
            if r['month']>='2026-07':price+=.09 # delayed downstream price adjustment
        r['price_yuan_m3']=money(price)
        r['theoretical_revenue_yuan']=money(r['volume_m3']*r['price_yuan_m3'])
        r['revenue_yuan']=money(r['theoretical_revenue_yuan']+r['audit_difference_yuan'])
        ratio=(.085 if b=='SHAHU' else .018)*noise((r['org_id'],r['month']),.6,1.5)
        if t=='工业':ratio*=.4
        if b=='SHAHU' and r['month']>='2026-07':ratio*=1.45
        r['estimated_meter_m3']=round(r['volume_m3']*ratio)
        r['actual_meter_m3']=r['volume_m3']-r['estimated_meter_m3']
    current=sum(r['volume_m3'] for r in sales if r['month'].startswith('2024'))
    first=sales[0];first['volume_m3']+=1_850_000_000-current
    first['actual_meter_m3']=first['volume_m3']-first['estimated_meter_m3']
    first['theoretical_revenue_yuan']=money(first['volume_m3']*first['price_yuan_m3'])
    first['revenue_yuan']=money(first['theoretical_revenue_yuan']+first['audit_difference_yuan'])
    by_center=defaultdict(list);by_grid={}
    for r in sales:
        by_center[(r['month'],r['center_id'])].append(r)
        by_grid[(r['month'],r['org_id'],r['user_type'])]=r
    sources=defaultdict(list)
    for r in tables['gas_supply_monthly']:sources[(r['month'],r['org_id'])].append(r)
    loss_base={'BINJIANG':.023,'SHAHU':.041,'JINGKAI':.019,'LINGANG':.028,'GAOXIN':.022}
    for (month,center),rows in sources.items():
        b=rows[0]['branch_id'];y,m=map(int,month.split('-'))
        rate=loss_base[b]+noise((center,month),-.004,.004)+.002*math.cos((m-1)/12*2*math.pi)
        if b=='SHAHU' and month>='2026-07':rate+=.012 # metering mismatch scenario, not all physical leakage
        inlet=round(sum(r['volume_m3'] for r in by_center[(month,center)])/(1-rate))
        lng=(.18 if m in (1,2,12) else .065)*noise((center,month,'lng'),.8,1.2)
        shares=[.8-lng,.2,lng];left=inlet
        for i,r in enumerate(rows):
            r['inlet_m3']=left if i==len(rows)-1 else round(inlet*shares[i]);left-=r['inlet_m3']
            price=2.24+.035*(y-2024)+.10*math.cos((m-1)/12*2*math.pi)+[0,.08,.46][i]+noise((center,month,i),-.035,.035)
            if month>='2026-05':price+=.13 # upstream cost increase before downstream adjustment
            r['purchase_price_yuan_m3']=money(price)
            r['purchase_cost_yuan']=money(r['inlet_m3']*r['purchase_price_yuan_m3'])
    for r in tables['gas_profit_monthly']:
        y,m=map(int,r['month'].split('-'));season=1+.22*math.sin((m-3)/12*2*math.pi)
        for key in ('installation_revenue_yuan','installation_cost_yuan','value_added_revenue_yuan','value_added_cost_yuan'):
            r[key]=money(r[key]*season*noise((r['org_id'],r['month'],key),.85,1.15))
        volume=sum(x['volume_m3'] for x in by_center[(r['month'],r['org_id'])])
        r['distribution_cost_yuan']=money(volume*.21*noise((r['org_id'],m),.9,1.1))
        for key in ('admin_expense_yuan','finance_expense_yuan','impairment_yuan'):
            r[key]=money(r[key]*noise((r['org_id'],r['month'],key),.75,1.25))
        r['pretax_profit_target_yuan']=money(600000*noise(r['org_id'],.5,1.4)*season)
    # Monthly invoice cohorts; FIFO collections and exact integer-cent aging.
    states={};groups=defaultdict(list)
    for r in tables['gas_ar_monthly']:groups[(r['month'],r['org_id'],r['user_type'])].append(r)
    for key,rows in groups.items():
        bill_total=cents(by_grid[key]['revenue_yuan']);left=bill_total
        share=noise((key[1],key[2]),.42,.72)
        for i,r in enumerate(rows):
            billed=left if i==len(rows)-1 else round(bill_total*share);left-=billed
            y,m=map(int,r['month'].split('-'));end=date(y,m,calendar.monthrange(y,m)[1])
            risk=r['branch_id']=='SHAHU' and r['user_type']=='工业' and i==0
            cid=r['customer_id']
            if cid not in states:
                starting=round(billed*(.8 if risk else noise(cid,.12,.45)))
                states[cid]=[[date(2023,11,30),starting]]
            debt=states[cid];opening=sum(v for _,v in debt);debt.append([end,billed])
            ratio=noise((cid,r['month']),.965,1.045)
            if risk:ratio=noise((cid,r['month']),.76,.95)
            if risk and r['org_id']=='SHAHU-S1-W1' and r['month']>='2025-01':ratio=noise((cid,r['month']),.16,.32)
            if m in (6,12):ratio+=.045 # collection campaigns
            collection=min(opening+billed,max(0,round(billed*ratio)))
            pay=collection
            for cohort in debt:
                take=min(pay,cohort[1]);cohort[1]-=take;pay-=take
                if not pay:break
            states[cid]=[c for c in debt if c[1]]
            age=[0]*5
            for day,value in states[cid]:
                days=(end-day).days;idx=0 if days<=30 else 1 if days<=90 else 2 if days<=180 else 3 if days<=365 else 4
                age[idx]+=value
            r.update(opening_yuan=opening/100,billed_yuan=billed/100,collected_yuan=collection/100,
                     closing_yuan=sum(age)/100,aging_basis='月末账单结算批次，先冲最早欠款；账龄按出账日至快照日，非逾期天数')
            for name,value in zip(['0_30','31_90','91_180','181_365','365_plus'],age):r[f'aging_{name}_yuan']=value/100
            r['provision_yuan']=money(sum(v*w for v,w in zip(age,[.01,.03,.10,.30,.70]))/100)
            r['collection_status']='重点催收' if sum(age[2:])>billed*.5 else '正常'
            from realistic_companies import get_real_customer_name
            r['customer_name'] = get_real_customer_name(r['customer_id'], r.get('customer_name') or f"{r['org_name']}{r['user_type']}用气账户")
    user_state={}
    for r in tables['gas_growth_monthly']:
        key=(r['org_id'],r['user_type']);y,m=map(int,r['month'].split('-'))
        opening=user_state.get(key,r['opening_users']);base=r['applied_users']
        applied=max(0,round(base*noise(r['business_key'],.6,1.5)*(1.25 if m in (9,10,11) else .65 if m==2 else 1)))
        connected=round(applied*noise((r['business_key'],'connect'),.68,.94));churn=round(connected*noise((r['business_key'],'churn'),.04,.19))
        ending=opening+connected-churn;user_state[key]=ending
        r.update(opening_users=opening,applied_users=applied,connected_users=connected,churn_users=churn,ending_users=ending,potential_users=max(ending,r['potential_users']),bottle_conversion_users=round(connected*.18) if r['user_type']=='居民' else 0)
    for r in tables['gas_safety_monthly']:
        y,m=map(int,r['month'].split('-'));gysp=r['branch_id']=='GYSP'
        due=0 if gysp else round(r['due_inspect']*noise(r['business_key'],.65,1.4))
        inspected=round(due*noise((r['business_key'],'coverage'),.81,.98))
        emergency=round((5 if gysp else 18)*noise((r['business_key'],'emergency'),.4,1.9))
        r.update(due_inspect=due,inspected=inspected,not_at_home=due-inspected,three_piece_installed=round(inspected*noise((r['org_id'],y),.4,.78)),emergency_total=emergency,emergency_on_time=max(0,emergency-round(emergency*noise((r['business_key'],'late'),.01,.17))),leak_count=round(emergency*noise((r['business_key'],'leak'),.02,.20)))
    # Split coarse legacy ledger blocks into inspectable physical sections.
    assets=[]
    for parent in tables['gas_network_assets']:
        for section in range(50):
            asset=dict(parent)
            asset['network_id']=asset['business_key']=f"{parent['network_id']}-{section+1:03}"
            assets.append(asset)
    tables['gas_network_assets']=assets
    weights=[noise(r['network_id'],8,160) for r in assets];total=sum(weights);remaining=1700000
    for i,(r,w) in enumerate(zip(assets,weights)):
        length=remaining if i==len(assets)-1 else round(1700000*w/total);remaining-=length;r['length_km']=length/100
        old=r['branch_id']=='SHAHU' and noise(r['network_id'])<.7
        year=1997+int(noise((r['network_id'],'year'),0,8)) if old else 2007+int(noise((r['network_id'],'year'),0,17))
        r['laid_date']=f'{year}-{1+int(noise((i,"month"),0,12)):02}-15'
        r['material']='钢管' if r['pressure_level']!='低压' or old else 'PE'
        r['gis_loaded_date']='' if noise((r['network_id'],'gis'))<(.32 if old else .07) else f'{max(year,2022)}-09-01'
    amap={r['network_id']:r for r in assets}
    cutoff=date(2026,9,30)
    for i,r in enumerate(tables['gas_hazard_orders']):
        # Varied discovery dates and asset links; retain two known critical overdue cases.
        found=date(2024,1,1)+timedelta(days=int(noise((r['hazard_id'],'found'),0,1004)))
        due=found+timedelta(days=7 if r['severity']=='重大' else 15 if i%3==0 else 30)
        pool=[a for a in assets if a['org_id']==r['org_id']]
        asset=pool[int(noise((i,'asset'),0,len(pool)))];r['network_id']=asset['network_id']
        delay=int(noise((i,'delay'),3,48));completed=found+timedelta(days=delay)
        opened=r['severity']=='重大' or i%11==0 or completed>cutoff
        r.update(found_date=found.isoformat(),due_date=due.isoformat(),completed_date='' if opened else completed.isoformat(),status='未闭环' if opened else '已闭环')
        if r['severity']!='重大':r['hazard_type']=['阀门渗漏','第三方施工风险','防腐层破损','管线占压','标识缺失'][i%5]
