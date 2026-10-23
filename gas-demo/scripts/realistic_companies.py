# -*- coding: utf-8 -*-
"""
真实企业名称字典：为江城燃气 80 家工商业大客户配置具有行业真实质感的企业全称。
严格排除任何“模拟”、“客户（模拟）”等虚假字样。
"""

REAL_COMPANY_NAMES = {
    # ====== 滨江分公司 (BINJIANG) 商业街区、高端酒店与都市轻工 ======
    "DEMO-BINJIANG-S1-W1-商业-1": "武汉江城大酒店餐饮管理有限公司",
    "DEMO-BINJIANG-S1-W1-商业-2": "武汉汉口江滩富力威斯汀酒店",
    "DEMO-BINJIANG-S1-W1-工业-1": "武汉长江光电仪器精密仪器厂",
    "DEMO-BINJIANG-S1-W1-工业-2": "湖北长投特种生物科技萃取中心",

    "DEMO-BINJIANG-S1-W2-商业-1": "武汉楚天新世界商业经营管理有限公司",
    "DEMO-BINJIANG-S1-W2-商业-2": "武汉香格里拉大酒店有限公司",
    "DEMO-BINJIANG-S1-W2-工业-1": "武汉无线电二厂精密电子装配车间",
    "DEMO-BINJIANG-S1-W2-工业-2": "湖北现代包装制品热熔涂层分厂",

    "DEMO-BINJIANG-S2-W1-商业-1": "武汉湖锦酒楼管理服务有限公司汉口店",
    "DEMO-BINJIANG-S2-W1-商业-2": "武汉汉口喜来登大酒店",
    "DEMO-BINJIANG-S2-W1-工业-1": "武汉立中合金精密压铸分公司",
    "DEMO-BINJIANG-S2-W1-工业-2": "湖北天门纺机武汉精密试验基地",

    "DEMO-BINJIANG-S2-W2-商业-1": "武汉武商集团股份有限公司国际广场",
    "DEMO-BINJIANG-S2-W2-商业-2": "武汉江城马哥孛罗酒店",
    "DEMO-BINJIANG-S2-W2-工业-1": "武汉中车长江车辆热工检修车间",
    "DEMO-BINJIANG-S2-W2-工业-2": "湖北华纺功能性纤维热定型制造厂",

    # ====== 沙湖分公司 (SHAHU) 老工业制造、重工铸锻、特种金属（含4家重点欠费大户） ======
    "DEMO-SHAHU-S1-W1-商业-1": "武汉沙湖水乡生态渔村餐饮管理有限公司",
    "DEMO-SHAHU-S1-W1-商业-2": "武汉楚河汉街万达瑞华酒店",
    "DEMO-SHAHU-S1-W1-工业-1": "武汉沙湖重型铸锻装备制造有限公司",  # 重点催收大户
    "DEMO-SHAHU-S1-W1-工业-2": "湖北金轮特种合金材料热轧车间",

    "DEMO-SHAHU-S1-W2-商业-1": "武汉销品茂商业管理有限责任公司",
    "DEMO-SHAHU-S1-W2-商业-2": "武汉凯德1818商用物业服务中心",
    "DEMO-SHAHU-S1-W2-工业-1": "湖北武钢沙湖冷轧精密薄板特热分厂",  # 重点催收大户
    "DEMO-SHAHU-S1-W2-工业-2": "武汉长动重型汽轮机机壳热处理车间",

    "DEMO-SHAHU-S2-W1-商业-1": "武汉艳阳天商贸发展有限公司沙湖店",
    "DEMO-SHAHU-S2-W1-商业-2": "武汉光明万丽酒店",
    "DEMO-SHAHU-S2-W1-工业-1": "武汉特种热能工程无缝钢管制造厂",  # 重点催收大户
    "DEMO-SHAHU-S2-W1-工业-2": "湖北华塑管道高温挤塑加工基地",

    "DEMO-SHAHU-S2-W2-商业-1": "武汉绿地缤纷城商业运营管理公司",
    "DEMO-SHAHU-S2-W2-商业-2": "武汉马可孛罗商务大厦后勤服务中心",
    "DEMO-SHAHU-S2-W2-工业-1": "中车特种轨道装备精密机加成型厂",  # 重点催收大户
    "DEMO-SHAHU-S2-W2-工业-2": "湖北兴发沙湖有机硅热聚合实验车间",

    # ====== 经开分公司 (JINGKAI) 汽车产业链、整车热压热处理、机械重工 ======
    "DEMO-JINGKAI-S1-W1-商业-1": "武汉经开万达广场投资有限公司",
    "DEMO-JINGKAI-S1-W1-商业-2": "武汉沌口华美达安可酒店",
    "DEMO-JINGKAI-S1-W1-工业-1": "东风乘用车制造热工热压成型分厂",
    "DEMO-JINGKAI-S1-W1-工业-2": "湖北三环汽车方向机精密锻压车间",

    "DEMO-JINGKAI-S1-W2-商业-1": "武汉永旺梦乐城经开购物中心餐饮部",
    "DEMO-JINGKAI-S1-W2-商业-2": "武汉车都金谷国际酒店",
    "DEMO-JINGKAI-S1-W2-工业-1": "东风本田汽车零部件热处理热浸锌分部",
    "DEMO-JINGKAI-S1-W2-工业-2": "武汉万向汽车制动系统表面处理基地",

    "DEMO-JINGKAI-S2-W1-商业-1": "武汉湘鄂情餐饮文化服务有限公司沌口分部",
    "DEMO-JINGKAI-S2-W1-商业-2": "武汉名流皇冠假日酒店",
    "DEMO-JINGKAI-S2-W1-工业-1": "武汉康明斯燃油系统发动机高温试验站",
    "DEMO-JINGKAI-S2-W1-工业-2": "湖北航天重工特种车桥加工车间",

    "DEMO-JINGKAI-S2-W2-商业-1": "武汉经开国际体育中心配套商业区",
    "DEMO-JINGKAI-S2-W2-商业-2": "武汉南太子湖商务度假酒店",
    "DEMO-JINGKAI-S2-W2-工业-1": "法雷奥车灯武汉热成型制造工段",
    "DEMO-JINGKAI-S2-W2-工业-2": "武汉敏实汽车零部件高温热压车间",

    # ====== 临港分公司 (LINGANG) 长江船舶钢构、港口物流保税、石化与粮食烘干 ======
    "DEMO-LINGANG-S1-W1-商业-1": "武汉阳逻保税港口餐饮配送管理有限公司",
    "DEMO-LINGANG-S1-W1-商业-2": "武汉长江航运枢纽国际海员大厦",
    "DEMO-LINGANG-S1-W1-工业-1": "武昌船舶重工阳逻特种钢构热切割车间",
    "DEMO-LINGANG-S1-W1-工业-2": "中交二航局港机重工热弯管热处理基地",

    "DEMO-LINGANG-S1-W2-商业-1": "武汉港发商业运营管理有限公司",
    "DEMO-LINGANG-S1-W2-商业-2": "武汉临港国际大酒店",
    "DEMO-LINGANG-S1-W2-工业-1": "中粮粮油武汉粮食物流热风烘干深加工厂",
    "DEMO-LINGANG-S1-W2-工业-2": "湖北金港特种复合保温板材发泡车间",

    "DEMO-LINGANG-S2-W1-商业-1": "武汉阳逻摩尔城商业管理有限公司",
    "DEMO-LINGANG-S2-W1-商业-2": "武汉长江世纪之星商务酒店",
    "DEMO-LINGANG-S2-W1-工业-1": "湖北长江集装箱特种涂装烘烤基地",
    "DEMO-LINGANG-S2-W1-工业-2": "武汉奥克化学环氧衍生材料热工车间",

    "DEMO-LINGANG-S2-W2-商业-1": "武汉新港大厦商用物业管理中心",
    "DEMO-LINGANG-S2-W2-商业-2": "武汉阳逻经济开发区水上专家楼",
    "DEMO-LINGANG-S2-W2-工业-1": "宝武武汉重工临港大型构件热煨弯管车间",
    "DEMO-LINGANG-S2-W2-工业-2": "湖北宏泰绿色建材高温煅烧陶粒基地",

    # ====== 高新分公司 (GAOXIN) 光谷光通信、半导体芯片、生物制药 ======
    "DEMO-GAOXIN-S1-W1-商业-1": "武汉大米先生餐饮连锁光谷软件园店",
    "DEMO-GAOXIN-S1-W1-商业-2": "武汉光谷希尔顿酒店",
    "DEMO-GAOXIN-S1-W1-工业-1": "长飞光纤光缆高温等离子气相沉积试验厂",
    "DEMO-GAOXIN-S1-W1-工业-2": "武汉精测电子半导体热工标定中心",

    "DEMO-GAOXIN-S1-W2-商业-1": "武汉光谷天地商业综合体美食天地",
    "DEMO-GAOXIN-S1-W2-商业-2": "武汉光谷华美达大酒店",
    "DEMO-GAOXIN-S1-W2-工业-1": "武汉华星光电高温高纯特种加热动力分厂",
    "DEMO-GAOXIN-S1-W2-工业-2": "湖北新冶钢高新合金棒线退火车间",

    "DEMO-GAOXIN-S2-W1-商业-1": "武汉光谷未来科技城集中餐饮管理中心",
    "DEMO-GAOXIN-S2-W1-商业-2": "武汉光谷凯悦酒店",
    "DEMO-GAOXIN-S2-W1-工业-1": "武汉高德红外传感器芯片封装烧结基地",
    "DEMO-GAOXIN-S2-W1-工业-2": "湖北国创高新特种改性沥青热熔加工分厂",

    "DEMO-GAOXIN-S2-W2-商业-1": "武汉中商平价光谷世界城商业运营部",
    "DEMO-GAOXIN-S2-W2-商业-2": "武汉未来之光国际青年商务酒店",
    "DEMO-GAOXIN-S2-W2-工业-1": "烽火通信科技光传输设备高频钎焊分部",
    "DEMO-GAOXIN-S2-W2-工业-2": "湖北人福医药高纯水蒸汽发生制药动力中心",
}

def get_real_customer_name(cid: str, default_name: str) -> str:
    """根据客户 ID 获取真实企业名称"""
    if cid in REAL_COMPANY_NAMES:
        return REAL_COMPANY_NAMES[cid]
    # 若为汇总桶，去掉“汇总桶”粗糙字样，替换为规范账户
    if "居民汇总桶" in default_name:
        return default_name.replace("居民汇总桶", "居民生活用气汇总账户")
    if "公益机构汇总桶" in default_name:
        return default_name.replace("公益机构汇总桶", "公益机构集中用气汇总账户")
    # 去除任何“（模拟）”字样
    return default_name.replace("（模拟）", "").replace("(模拟)", "").replace("模拟", "")
