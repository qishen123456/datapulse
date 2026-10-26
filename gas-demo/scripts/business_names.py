"""Fictional business names; IDs, hierarchy and all numeric facts stay stable."""
PLACES = {
 'BINJIANG': [('滨江沿江营业所',['望江路','滨港路']),('滨江城西营业所',['锦澜社区','云麓社区'])],
 'SHAHU': [('沙湖东岸营业所',['汀兰社区','荷风路']),('沙湖北岸营业所',['湖畔新城','青荷路'])],
 'JINGKAI': [('经开东园服务中心',['智造产业园','兴业大道']),('经开西园服务中心',['科创产业园','丰裕路'])],
 'LINGANG': [('临港港区服务中心',['港兴工业园','临江物流园']),('临港新城营业所',['海棠社区','启航路'])],
 'GAOXIN': [('高新科创服务中心',['光谷科创园','星河产业园']),('高新生活服务中心',['麓林社区','文澜路'])],
 'GYSP': [('高压输配东线运维中心',['东环干线','滨江门站']),('高压输配西线运维中心',['西环干线','临港调压站'])],
}

def apply_names(tables, tree):
    names={r['org_id']:r['org_name'] for r in tables['gas_org']}
    places={}
    for branch, centers in PLACES.items():
        for c,(center,grids) in enumerate(centers,1):
            names[f'{branch}-S{c}']=center
            for g,place in enumerate(grids,1):
                code=f'{branch}-S{c}-W{g}'
                places[code]=place
                names[code]=place+('运维班组' if branch=='GYSP' else '服务网格')
    for rows in tables.values():
        for row in rows:
            row['org_name']=names[row['org_id']]
            if 'org_name_path' in row:
                row['org_name_path']='/'.join(names[k] for k in row['org_path'].strip('/').split('/'))
            if 'customer_name' in row:
                place=places[row['org_id']]
                typ=row['user_type'];i=int(row['customer_id'].rsplit('-',1)[-1])-1
                suffix={'商业':['悦里餐饮管理有限公司','泊庭酒店管理有限公司'],'工业':['恒拓精密制造有限公司','澄岳新材料有限公司']}
                row['customer_name']=place+suffix[typ][i] if typ in suffix else place+('居民户汇总' if typ=='居民' else '公共服务机构汇总')
    for node in tree['nodes']:
        node['name']=names[node['id']]
        node['path_names']=[names[k] for k in node['path_ids']]
    return names
