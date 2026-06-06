# -*- coding: utf-8 -*-
"""CES 12 类未拆分训练集分类库，由 train_ces_model.py 从 Excel 生成。"""

CES_TAXONOMY = [
  {
    "code": "1",
    "category": "美学景观体验",
    "description": "自然景观观赏、园林设计审美、赏花季相、拍照打卡、夜景灯光",
    "subcategories": [
      {
        "key": "sub_c01_s01",
        "name": "自然景观观赏",
        "keywords": [
          "景色",
          "景致",
          "景观",
          "风景",
          "美景",
          "山景",
          "湖景",
          "园景",
          "全景",
          "视野",
          "观景",
          "好看",
          "漂亮",
          "美丽",
          "优美",
          "绝美",
          "很美",
          "真美",
          "如画",
          "赏心悦目"
        ]
      },
      {
        "key": "sub_c01_s02",
        "name": "园林设计审美",
        "keywords": [
          "园林",
          "园艺",
          "造景",
          "景观设计",
          "亭台",
          "亭子",
          "楼阁",
          "水榭",
          "长廊",
          "廊桥",
          "拱桥",
          "假山",
          "喷泉",
          "雕塑",
          "造型",
          "建筑设计",
          "设计感"
        ]
      },
      {
        "key": "sub_c01_s03",
        "name": "赏花季相",
        "keywords": [
          "赏花",
          "花海",
          "花季",
          "花开",
          "开花",
          "花花",
          "樱花",
          "荷花",
          "莲花",
          "梅花",
          "菊花",
          "杜鹃",
          "月季",
          "薰衣草",
          "格桑花",
          "向日葵",
          "郁金香",
          "桃花",
          "油菜花",
          "凤凰花",
          "紫荆花",
          "簕杜鹃",
          "三角梅",
          "落羽杉",
          "红叶",
          "黄叶"
        ]
      },
      {
        "key": "sub_c01_s04",
        "name": "拍照打卡",
        "keywords": [
          "拍照",
          "打卡",
          "摄影",
          "出片",
          "取景",
          "合影",
          "自拍",
          "相机",
          "航拍",
          "机位",
          "网红"
        ]
      },
      {
        "key": "sub_c01_s05",
        "name": "夜景灯光",
        "keywords": [
          "夜景",
          "灯光",
          "灯会",
          "灯光秀",
          "霓虹",
          "亮化",
          "彩灯",
          "亮灯",
          "夜游",
          "晚霞",
          "夕阳",
          "落日",
          "日落",
          "日出",
          "黄昏",
          "朝霞"
        ]
      }
    ]
  },
  {
    "code": "2",
    "category": "游憩活动与运动体验",
    "description": "散步跑步、骑行徒步、游乐场与游乐设施、露营野餐、球类健身",
    "subcategories": [
      {
        "key": "sub_c02_s01",
        "name": "散步跑步",
        "keywords": [
          "散步",
          "漫步",
          "走走",
          "逛逛",
          "慢跑",
          "跑步",
          "晨跑",
          "夜跑",
          "健步",
          "快走",
          "遛弯"
        ]
      },
      {
        "key": "sub_c02_s02",
        "name": "骑行徒步",
        "keywords": [
          "徒步",
          "登山",
          "爬山",
          "远足",
          "骑行",
          "骑车",
          "自行车",
          "单车",
          "山地车",
          "绿道",
          "步道"
        ]
      },
      {
        "key": "sub_c02_s03",
        "name": "游乐场与游乐设施",
        "keywords": [
          "游乐场",
          "游乐设施",
          "儿童乐园",
          "摩天轮",
          "过山车",
          "旋转木马",
          "碰碰车",
          "海盗船",
          "滑梯",
          "秋千",
          "蹦床",
          "攀爬",
          "攀岩",
          "乐园"
        ]
      },
      {
        "key": "sub_c02_s04",
        "name": "露营野餐",
        "keywords": [
          "露营",
          "野餐",
          "帐篷",
          "天幕",
          "野炊",
          "餐垫",
          "放风筝",
          "风筝",
          "草坪野餐",
          "草地野餐"
        ]
      },
      {
        "key": "sub_c02_s05",
        "name": "球类健身",
        "keywords": [
          "打球",
          "足球",
          "篮球",
          "羽毛球",
          "乒乓球",
          "网球",
          "排球",
          "健身",
          "锻炼",
          "运动",
          "太极",
          "广场舞",
          "瑜伽"
        ]
      }
    ]
  },
  {
    "code": "3",
    "category": "蓝空间亲水体验",
    "description": "滨海沙滩、湖河湿地、亲水戏水、栈道观景",
    "subcategories": [
      {
        "key": "sub_c03_s01",
        "name": "滨海沙滩",
        "keywords": [
          "海景",
          "海滨",
          "海岸",
          "海滩",
          "海边",
          "海湾",
          "海水",
          "海浪",
          "海风",
          "沙滩",
          "沙子",
          "沙质",
          "礁石",
          "赶海",
          "滨海",
          "沿海",
          "临海",
          "看海",
          "观海"
        ]
      },
      {
        "key": "sub_c03_s02",
        "name": "湖河湿地",
        "keywords": [
          "湖水",
          "湖面",
          "湖畔",
          "水库",
          "池塘",
          "河流",
          "河边",
          "小溪",
          "溪流",
          "湿地",
          "水岸",
          "红树林",
          "芦苇",
          "水系"
        ]
      },
      {
        "key": "sub_c03_s03",
        "name": "亲水戏水",
        "keywords": [
          "亲水",
          "戏水",
          "玩水",
          "踩水",
          "涉水",
          "游泳",
          "水上",
          "水边",
          "喷泉玩水"
        ]
      },
      {
        "key": "sub_c03_s04",
        "name": "栈道观景",
        "keywords": [
          "栈道",
          "观景台",
          "眺望",
          "远眺",
          "瞭望",
          "俯瞰",
          "海景台",
          "观景廊"
        ]
      }
    ]
  },
  {
    "code": "4",
    "category": "生态自然与生物感知",
    "description": "植物与绿化、动物与观鸟、生境与生态、空气与自然接触",
    "subcategories": [
      {
        "key": "sub_c04_s01",
        "name": "植物与绿化",
        "keywords": [
          "植物",
          "植被",
          "森林",
          "树林",
          "树木",
          "绿树",
          "大树",
          "古树",
          "树荫",
          "树影",
          "绿化",
          "草坪",
          "草地",
          "绿地",
          "绿意",
          "绿油油",
          "青翠",
          "郁郁葱葱",
          "花草",
          "花木"
        ]
      },
      {
        "key": "sub_c04_s02",
        "name": "动物与观鸟",
        "keywords": [
          "鸟类",
          "海鸥",
          "白鹭",
          "候鸟",
          "观鸟",
          "松鼠",
          "猴子",
          "蝴蝶",
          "蜻蜓",
          "蜜蜂",
          "鸟语花香",
          "小鸟",
          "鱼儿"
        ]
      },
      {
        "key": "sub_c04_s03",
        "name": "生境与生态",
        "keywords": [
          "生态",
          "生境",
          "自然生态",
          "生态环境",
          "生物",
          "栖息",
          "多样性",
          "原生态",
          "野趣",
          "自然环境"
        ]
      },
      {
        "key": "sub_c04_s04",
        "name": "空气与自然接触",
        "keywords": [
          "空气清新",
          "清新空气",
          "天然氧吧",
          "氧吧",
          "负离子",
          "大自然",
          "亲近自然",
          "接触自然",
          "自然气息"
        ]
      }
    ]
  },
  {
    "code": "5",
    "category": "文化遗产与地方认同",
    "description": "历史遗产、地方符号、城市记忆、民俗节庆",
    "subcategories": [
      {
        "key": "sub_c05_s01",
        "name": "历史遗产",
        "keywords": [
          "历史",
          "古建筑",
          "古迹",
          "遗址",
          "文物",
          "文保",
          "古城",
          "古镇",
          "老街",
          "文化遗产",
          "传统",
          "庙宇",
          "寺庙",
          "祠堂",
          "故居",
          "纪念碑",
          "纪念馆",
          "纪念台"
        ]
      },
      {
        "key": "sub_c05_s02",
        "name": "地方符号",
        "keywords": [
          "地标",
          "象征",
          "符号",
          "名片",
          "代表性",
          "地方特色",
          "深圳特色",
          "岭南",
          "南粤",
          "本土",
          "铜像",
          "邓小平",
          "小平"
        ]
      },
      {
        "key": "sub_c05_s03",
        "name": "城市记忆",
        "keywords": [
          "城市记忆",
          "历史记忆",
          "特区",
          "改革开放",
          "渔村变迁",
          "城市变迁",
          "深圳记忆",
          "一国两制"
        ]
      },
      {
        "key": "sub_c05_s04",
        "name": "民俗节庆",
        "keywords": [
          "民俗",
          "节庆",
          "庙会",
          "花市",
          "民俗活动",
          "传统节日",
          "文化节"
        ]
      }
    ]
  },
  {
    "code": "6",
    "category": "教育科普与认知体验",
    "description": "自然教育、展陈解说、研学观察",
    "subcategories": [
      {
        "key": "sub_c06_s01",
        "name": "自然教育",
        "keywords": [
          "自然教育",
          "生态教育",
          "环境教育",
          "科普教育",
          "科普",
          "学知识",
          "长知识"
        ]
      },
      {
        "key": "sub_c06_s02",
        "name": "展陈解说",
        "keywords": [
          "展览",
          "展馆",
          "博物馆",
          "陈列",
          "展示",
          "展品",
          "美术馆",
          "科技馆",
          "规划馆",
          "展览馆",
          "讲解",
          "解说",
          "说明牌",
          "介绍牌",
          "科普牌"
        ]
      },
      {
        "key": "sub_c06_s03",
        "name": "研学观察",
        "keywords": [
          "研学",
          "学习",
          "观察",
          "了解",
          "认识",
          "增长见识",
          "开阔眼界",
          "校外",
          "实践"
        ]
      }
    ]
  },
  {
    "code": "7",
    "category": "精神恢复与心理舒适",
    "description": "放松疗愈、安静独处、安全安心、压力缓解",
    "subcategories": [
      {
        "key": "sub_c07_s01",
        "name": "放松疗愈",
        "keywords": [
          "放松",
          "放空",
          "疗愈",
          "治愈",
          "抚慰",
          "惬意",
          "舒适",
          "舒服",
          "自在",
          "悠闲",
          "休闲"
        ]
      },
      {
        "key": "sub_c07_s02",
        "name": "安静独处",
        "keywords": [
          "安静",
          "宁静",
          "清静",
          "幽静",
          "静谧",
          "清净",
          "独处",
          "发呆",
          "发发呆"
        ]
      },
      {
        "key": "sub_c07_s03",
        "name": "安全安心",
        "keywords": [
          "安心",
          "舒心",
          "放心",
          "踏实",
          "安全感",
          "很安全",
          "比较安全"
        ]
      },
      {
        "key": "sub_c07_s04",
        "name": "压力缓解",
        "keywords": [
          "减压",
          "解压",
          "舒缓",
          "压力",
          "烦恼",
          "疲惫",
          "疲劳",
          "烦躁",
          "焦虑",
          "放松心情",
          "心情好",
          "心情舒畅",
          "心旷神怡",
          "神清气爽"
        ]
      }
    ]
  },
  {
    "code": "8",
    "category": "社交亲子与全龄共享",
    "description": "亲子活动、朋友聚会、社区邻里、老年友好、宠物友好",
    "subcategories": [
      {
        "key": "sub_c08_s01",
        "name": "亲子活动",
        "keywords": [
          "亲子",
          "小孩",
          "孩子",
          "小朋友",
          "儿童",
          "宝宝",
          "遛娃",
          "带娃",
          "亲子活动",
          "带孩子",
          "带小孩"
        ]
      },
      {
        "key": "sub_c08_s02",
        "name": "朋友聚会",
        "keywords": [
          "朋友",
          "闺蜜",
          "兄弟",
          "聚会",
          "聚餐",
          "结伴",
          "相伴",
          "约会",
          "同学"
        ]
      },
      {
        "key": "sub_c08_s03",
        "name": "社区邻里",
        "keywords": [
          "社区",
          "邻里",
          "附近居民",
          "周边居民",
          "家门口",
          "街坊",
          "居民"
        ]
      },
      {
        "key": "sub_c08_s04",
        "name": "老年友好",
        "keywords": [
          "老年人",
          "老人",
          "长者",
          "长辈",
          "老少",
          "全家",
          "一家人",
          "家庭",
          "轮椅"
        ]
      },
      {
        "key": "sub_c08_s05",
        "name": "宠物友好",
        "keywords": [
          "宠物",
          "遛狗",
          "遛猫",
          "狗狗",
          "带狗",
          "带宠物",
          "宠物友好"
        ]
      }
    ]
  },
  {
    "code": "9",
    "category": "可达交通与游线导向",
    "description": "公共交通到达、停车设施、入口步行、导向标识、无障碍通行",
    "subcategories": [
      {
        "key": "sub_c09_s01",
        "name": "公共交通到达",
        "keywords": [
          "地铁",
          "公交",
          "公交车",
          "公交站",
          "巴士",
          "交通方便",
          "交通便利",
          "交通",
          "可达",
          "到达",
          "打车",
          "自驾"
        ]
      },
      {
        "key": "sub_c09_s02",
        "name": "停车设施",
        "keywords": [
          "停车",
          "停车场",
          "车位",
          "停车位",
          "停车难",
          "停车贵",
          "免费停车",
          "不好停车"
        ]
      },
      {
        "key": "sub_c09_s03",
        "name": "入口步行",
        "keywords": [
          "入口",
          "出入口",
          "门口",
          "大门",
          "步行",
          "走路",
          "步行到",
          "步行可达"
        ]
      },
      {
        "key": "sub_c09_s04",
        "name": "导向标识",
        "keywords": [
          "标识",
          "指示牌",
          "路标",
          "导向",
          "指引",
          "导航",
          "地图",
          "路线图"
        ]
      },
      {
        "key": "sub_c09_s05",
        "name": "无障碍通行",
        "keywords": [
          "无障碍",
          "坡道",
          "电梯",
          "轮椅通行",
          "推车",
          "婴儿车"
        ]
      }
    ]
  },
  {
    "code": "10",
    "category": "设施维护与管理服务",
    "description": "设施维护修缮、卫生保洁、安全管理、台风灾后恢复",
    "subcategories": [
      {
        "key": "sub_c10_s01",
        "name": "设施维护修缮",
        "keywords": [
          "设施",
          "设备",
          "维护",
          "修缮",
          "修理",
          "维修",
          "破损",
          "损坏",
          "坏了",
          "老旧",
          "老化",
          "破旧",
          "座椅",
          "长椅",
          "凉亭",
          "垃圾桶",
          "照明",
          "路灯",
          "配套",
          "设施齐全"
        ]
      },
      {
        "key": "sub_c10_s02",
        "name": "卫生保洁",
        "keywords": [
          "卫生",
          "干净",
          "整洁",
          "清洁",
          "保洁",
          "脏",
          "垃圾",
          "异味",
          "臭味",
          "脏乱",
          "公厕",
          "厕所",
          "卫生间",
          "洗手间",
          "洗手池"
        ]
      },
      {
        "key": "sub_c10_s03",
        "name": "安全管理",
        "keywords": [
          "安保",
          "保安",
          "管理",
          "服务",
          "工作人员",
          "管理员",
          "秩序员",
          "护栏",
          "危险",
          "注意安全",
          "安全管理"
        ]
      },
      {
        "key": "sub_c10_s04",
        "name": "台风灾后恢复",
        "keywords": [
          "台风",
          "灾后",
          "灾害",
          "重建",
          "倒伏",
          "修复",
          "台风后恢复",
          "灾后恢复"
        ]
      }
    ]
  },
  {
    "code": "11",
    "category": "空间承载与秩序体验",
    "description": "空间开阔感知、拥挤与排队、动线秩序、场地容量",
    "subcategories": [
      {
        "key": "sub_c11_s01",
        "name": "空间开阔感知",
        "keywords": [
          "空间",
          "开阔",
          "宽敞",
          "空旷",
          "辽阔",
          "地方大",
          "面积大",
          "占地面积",
          "场地大",
          "大草坪"
        ]
      },
      {
        "key": "sub_c11_s02",
        "name": "拥挤与排队",
        "keywords": [
          "拥挤",
          "人多",
          "人太多",
          "人很多",
          "好多人",
          "很多人",
          "人山人海",
          "爆满",
          "排队",
          "排长队",
          "等待",
          "高峰期",
          "人流量",
          "客流"
        ]
      },
      {
        "key": "sub_c11_s03",
        "name": "动线秩序",
        "keywords": [
          "动线",
          "路线",
          "走线",
          "路径",
          "秩序",
          "有序",
          "流畅",
          "合理"
        ]
      },
      {
        "key": "sub_c11_s04",
        "name": "场地容量",
        "keywords": [
          "容量",
          "承载",
          "限流",
          "预约",
          "场地容量"
        ]
      }
    ]
  },
  {
    "code": "12",
    "category": "环境舒适与微气候",
    "description": "遮阴通风、湿热体感、空气质量、噪音环境",
    "subcategories": [
      {
        "key": "sub_c12_s01",
        "name": "遮阴通风",
        "keywords": [
          "遮阴",
          "遮阳",
          "树荫",
          "阴凉",
          "绿荫",
          "暴晒",
          "很晒",
          "太晒",
          "晒太阳",
          "太阳晒",
          "遮阳不足",
          "通风",
          "微风",
          "凉风"
        ]
      },
      {
        "key": "sub_c12_s02",
        "name": "湿热体感",
        "keywords": [
          "海风",
          "清爽",
          "凉快",
          "凉爽",
          "闷热",
          "潮湿",
          "湿热",
          "体感",
          "炎热",
          "太晒",
          "很热",
          "太热",
          "热死",
          "热得",
          "天气热"
        ]
      },
      {
        "key": "sub_c12_s03",
        "name": "空气质量",
        "keywords": [
          "空气质量",
          "空气好",
          "空气差",
          "空气不好",
          "雾霾",
          "扬尘",
          "空气不怎么"
        ]
      },
      {
        "key": "sub_c12_s04",
        "name": "噪音环境",
        "keywords": [
          "噪音",
          "嘈杂",
          "吵闹",
          "吵",
          "喧嚣",
          "喧闹",
          "不吵",
          "吵闹声"
        ]
      }
    ]
  }
]

CES_TRAINING_STATS = {
  "dataset_id": "unsplit_20260523",
  "dataset_name": "未拆分 CES 指标评论分句分类结果",
  "category_count": 12,
  "subcategory_count": 51,
  "keyword_count": 589,
  "sample_count": 15485,
  "sentence_hit_count": 71575,
  "model": {
    "train_size": 11613,
    "validation_size": 3872,
    "main": {
      "micro_precision": 0.8962443095599393,
      "micro_recall": 0.8633290699799013,
      "micro_f1": 0.8794788273615636,
      "macro_precision": 0.857591699737846,
      "macro_recall": 0.8254384612735702,
      "macro_f1": 0.8403768359367944
    },
    "sub": {
      "micro_precision": 0.8871176217147781,
      "micro_recall": 0.8615663574865751,
      "micro_f1": 0.8741553157615426,
      "macro_precision": 0.7916688910437608,
      "macro_recall": 0.7680707114092323,
      "macro_f1": 0.7747820090232475
    },
    "all": {
      "micro_precision": 0.8910502656313853,
      "micro_recall": 0.8623294443345857,
      "micro_f1": 0.8764546276756103,
      "macro_precision": 0.8042256165093009,
      "macro_recall": 0.7789979018595824,
      "macro_f1": 0.7872762617686847
    }
  },
  "counts_by_category": [
    {
      "code": "1",
      "category": "美学景观体验",
      "sample_count": 8149,
      "sentence_hit_count": 15002
    },
    {
      "code": "2",
      "category": "游憩活动与运动体验",
      "sample_count": 6833,
      "sentence_hit_count": 11951
    },
    {
      "code": "3",
      "category": "蓝空间亲水体验",
      "sample_count": 4758,
      "sentence_hit_count": 9086
    },
    {
      "code": "4",
      "category": "生态自然与生物感知",
      "sample_count": 4488,
      "sentence_hit_count": 7362
    },
    {
      "code": "5",
      "category": "文化遗产与地方认同",
      "sample_count": 802,
      "sentence_hit_count": 1075
    },
    {
      "code": "6",
      "category": "教育科普与认知体验",
      "sample_count": 490,
      "sentence_hit_count": 625
    },
    {
      "code": "7",
      "category": "精神恢复与心理舒适",
      "sample_count": 3983,
      "sentence_hit_count": 5352
    },
    {
      "code": "8",
      "category": "社交亲子与全龄共享",
      "sample_count": 4090,
      "sentence_hit_count": 6176
    },
    {
      "code": "9",
      "category": "可达交通与游线导向",
      "sample_count": 3680,
      "sentence_hit_count": 6166
    },
    {
      "code": "10",
      "category": "设施维护与管理服务",
      "sample_count": 2637,
      "sentence_hit_count": 3530
    },
    {
      "code": "11",
      "category": "空间承载与秩序体验",
      "sample_count": 2451,
      "sentence_hit_count": 2993
    },
    {
      "code": "12",
      "category": "环境舒适与微气候",
      "sample_count": 1945,
      "sentence_hit_count": 2257
    }
  ],
  "counts_by_subcategory": [
    {
      "id": "sub_c01_s01",
      "code": "1",
      "category": "美学景观体验",
      "subcategory": "自然景观观赏",
      "sample_count": 5608
    },
    {
      "id": "sub_c01_s02",
      "code": "1",
      "category": "美学景观体验",
      "subcategory": "园林设计审美",
      "sample_count": 873
    },
    {
      "id": "sub_c01_s03",
      "code": "1",
      "category": "美学景观体验",
      "subcategory": "赏花季相",
      "sample_count": 1269
    },
    {
      "id": "sub_c01_s04",
      "code": "1",
      "category": "美学景观体验",
      "subcategory": "拍照打卡",
      "sample_count": 2687
    },
    {
      "id": "sub_c01_s05",
      "code": "1",
      "category": "美学景观体验",
      "subcategory": "夜景灯光",
      "sample_count": 1761
    },
    {
      "id": "sub_c02_s01",
      "code": "2",
      "category": "游憩活动与运动体验",
      "subcategory": "散步跑步",
      "sample_count": 3518
    },
    {
      "id": "sub_c02_s02",
      "code": "2",
      "category": "游憩活动与运动体验",
      "subcategory": "骑行徒步",
      "sample_count": 2119
    },
    {
      "id": "sub_c02_s03",
      "code": "2",
      "category": "游憩活动与运动体验",
      "subcategory": "游乐场与游乐设施",
      "sample_count": 1112
    },
    {
      "id": "sub_c02_s04",
      "code": "2",
      "category": "游憩活动与运动体验",
      "subcategory": "露营野餐",
      "sample_count": 1470
    },
    {
      "id": "sub_c02_s05",
      "code": "2",
      "category": "游憩活动与运动体验",
      "subcategory": "球类健身",
      "sample_count": 1896
    },
    {
      "id": "sub_c03_s01",
      "code": "3",
      "category": "蓝空间亲水体验",
      "subcategory": "滨海沙滩",
      "sample_count": 3312
    },
    {
      "id": "sub_c03_s02",
      "code": "3",
      "category": "蓝空间亲水体验",
      "subcategory": "湖河湿地",
      "sample_count": 1368
    },
    {
      "id": "sub_c03_s03",
      "code": "3",
      "category": "蓝空间亲水体验",
      "subcategory": "亲水戏水",
      "sample_count": 341
    },
    {
      "id": "sub_c03_s04",
      "code": "3",
      "category": "蓝空间亲水体验",
      "subcategory": "栈道观景",
      "sample_count": 707
    },
    {
      "id": "sub_c04_s01",
      "code": "4",
      "category": "生态自然与生物感知",
      "subcategory": "植物与绿化",
      "sample_count": 3442
    },
    {
      "id": "sub_c04_s02",
      "code": "4",
      "category": "生态自然与生物感知",
      "subcategory": "动物与观鸟",
      "sample_count": 598
    },
    {
      "id": "sub_c04_s03",
      "code": "4",
      "category": "生态自然与生物感知",
      "subcategory": "生境与生态",
      "sample_count": 818
    },
    {
      "id": "sub_c04_s04",
      "code": "4",
      "category": "生态自然与生物感知",
      "subcategory": "空气与自然接触",
      "sample_count": 936
    },
    {
      "id": "sub_c05_s01",
      "code": "5",
      "category": "文化遗产与地方认同",
      "subcategory": "历史遗产",
      "sample_count": 525
    },
    {
      "id": "sub_c05_s02",
      "code": "5",
      "category": "文化遗产与地方认同",
      "subcategory": "地方符号",
      "sample_count": 269
    },
    {
      "id": "sub_c05_s03",
      "code": "5",
      "category": "文化遗产与地方认同",
      "subcategory": "城市记忆",
      "sample_count": 23
    },
    {
      "id": "sub_c05_s04",
      "code": "5",
      "category": "文化遗产与地方认同",
      "subcategory": "民俗节庆",
      "sample_count": 42
    },
    {
      "id": "sub_c06_s01",
      "code": "6",
      "category": "教育科普与认知体验",
      "subcategory": "自然教育",
      "sample_count": 99
    },
    {
      "id": "sub_c06_s02",
      "code": "6",
      "category": "教育科普与认知体验",
      "subcategory": "展陈解说",
      "sample_count": 255
    },
    {
      "id": "sub_c06_s03",
      "code": "6",
      "category": "教育科普与认知体验",
      "subcategory": "研学观察",
      "sample_count": 206
    },
    {
      "id": "sub_c07_s01",
      "code": "7",
      "category": "精神恢复与心理舒适",
      "subcategory": "放松疗愈",
      "sample_count": 3376
    },
    {
      "id": "sub_c07_s02",
      "code": "7",
      "category": "精神恢复与心理舒适",
      "subcategory": "安静独处",
      "sample_count": 637
    },
    {
      "id": "sub_c07_s03",
      "code": "7",
      "category": "精神恢复与心理舒适",
      "subcategory": "安全安心",
      "sample_count": 69
    },
    {
      "id": "sub_c07_s04",
      "code": "7",
      "category": "精神恢复与心理舒适",
      "subcategory": "压力缓解",
      "sample_count": 443
    },
    {
      "id": "sub_c08_s01",
      "code": "8",
      "category": "社交亲子与全龄共享",
      "subcategory": "亲子活动",
      "sample_count": 2898
    },
    {
      "id": "sub_c08_s02",
      "code": "8",
      "category": "社交亲子与全龄共享",
      "subcategory": "朋友聚会",
      "sample_count": 1597
    },
    {
      "id": "sub_c08_s03",
      "code": "8",
      "category": "社交亲子与全龄共享",
      "subcategory": "社区邻里",
      "sample_count": 327
    },
    {
      "id": "sub_c08_s04",
      "code": "8",
      "category": "社交亲子与全龄共享",
      "subcategory": "老年友好",
      "sample_count": 747
    },
    {
      "id": "sub_c08_s05",
      "code": "8",
      "category": "社交亲子与全龄共享",
      "subcategory": "宠物友好",
      "sample_count": 154
    },
    {
      "id": "sub_c09_s01",
      "code": "9",
      "category": "可达交通与游线导向",
      "subcategory": "公共交通到达",
      "sample_count": 1976
    },
    {
      "id": "sub_c09_s02",
      "code": "9",
      "category": "可达交通与游线导向",
      "subcategory": "停车设施",
      "sample_count": 1360
    },
    {
      "id": "sub_c09_s03",
      "code": "9",
      "category": "可达交通与游线导向",
      "subcategory": "入口步行",
      "sample_count": 1275
    },
    {
      "id": "sub_c09_s04",
      "code": "9",
      "category": "可达交通与游线导向",
      "subcategory": "导向标识",
      "sample_count": 404
    },
    {
      "id": "sub_c09_s05",
      "code": "9",
      "category": "可达交通与游线导向",
      "subcategory": "无障碍通行",
      "sample_count": 64
    },
    {
      "id": "sub_c10_s01",
      "code": "10",
      "category": "设施维护与管理服务",
      "subcategory": "设施维护修缮",
      "sample_count": 1444
    },
    {
      "id": "sub_c10_s02",
      "code": "10",
      "category": "设施维护与管理服务",
      "subcategory": "卫生保洁",
      "sample_count": 1038
    },
    {
      "id": "sub_c10_s03",
      "code": "10",
      "category": "设施维护与管理服务",
      "subcategory": "安全管理",
      "sample_count": 509
    },
    {
      "id": "sub_c10_s04",
      "code": "10",
      "category": "设施维护与管理服务",
      "subcategory": "台风灾后恢复",
      "sample_count": 98
    },
    {
      "id": "sub_c11_s01",
      "code": "11",
      "category": "空间承载与秩序体验",
      "subcategory": "空间开阔感知",
      "sample_count": 741
    },
    {
      "id": "sub_c11_s02",
      "code": "11",
      "category": "空间承载与秩序体验",
      "subcategory": "拥挤与排队",
      "sample_count": 1338
    },
    {
      "id": "sub_c11_s03",
      "code": "11",
      "category": "空间承载与秩序体验",
      "subcategory": "动线秩序",
      "sample_count": 251
    },
    {
      "id": "sub_c11_s04",
      "code": "11",
      "category": "空间承载与秩序体验",
      "subcategory": "场地容量",
      "sample_count": 349
    },
    {
      "id": "sub_c12_s01",
      "code": "12",
      "category": "环境舒适与微气候",
      "subcategory": "遮阴通风",
      "sample_count": 663
    },
    {
      "id": "sub_c12_s02",
      "code": "12",
      "category": "环境舒适与微气候",
      "subcategory": "湿热体感",
      "sample_count": 1209
    },
    {
      "id": "sub_c12_s03",
      "code": "12",
      "category": "环境舒适与微气候",
      "subcategory": "空气质量",
      "sample_count": 114
    },
    {
      "id": "sub_c12_s04",
      "code": "12",
      "category": "环境舒适与微气候",
      "subcategory": "噪音环境",
      "sample_count": 172
    }
  ]
}
