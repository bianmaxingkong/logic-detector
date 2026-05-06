"""
补充知识库：常识事实（supplement 后合并到 CFEVER 索引中）

覆盖 CFEVER 缺失的基本常识：
- 地理常识（首都、河流、山脉）
- 物理常识（重力、温度、光速）
- 生物常识（植物、动物、人体）
- 历史常识
- 数学常识
- 日常常识

格式：[(claim, label), ...]
label: 'supports' = 事实正确, 'refutes' = 事实错误
"""

COMMON_SENSE_FACTS = [
    # ============ 地理 ============
    ("美國的首都是華盛頓哥倫比亞特區。", "supports"),
    ("美國的首都是紐約。", "refutes"),
    ("美國的首都是華盛頓。", "supports"),
    ("中國的首都是北京。", "supports"),
    ("中國的首都是上海。", "refutes"),
    ("中国的首都是北京。", "supports"),
    ("英國的首都是倫敦。", "supports"),
    ("英國的首都是巴黎。", "refutes"),
    ("法蘭西的首都是巴黎。", "supports"),
    ("法蘭西的首都是倫敦。", "refutes"),
    ("日本的首都是東京。", "supports"),
    ("日本的首都是大阪。", "refutes"),
    ("俄羅斯的首都是莫斯科。", "supports"),
    ("俄羅斯的首都是聖彼得堡。", "refutes"),
    ("澳大利亞的首都是坎培拉。", "supports"),
    ("澳大利亞的首都是雪梨。", "refutes"),
    ("加拿大的首都是渥太華。", "supports"),
    ("加拿大的首都是多倫多。", "refutes"),
    ("印度的首都是新德里。", "supports"),
    ("印度的首都是孟買。", "refutes"),
    ("德國的的首都是柏林。", "supports"),
    ("地球是圓的。", "supports"),
    ("地球是平的。", "refutes"),
    ("地球圍繞太陽公轉。", "supports"),
    ("地球绕着太阳转。", "supports"),
    ("地球绕太阳公转。", "supports"),
    ("地球围绕太阳转。", "supports"),
    ("地球自轉一圈需要24小時。", "supports"),
    ("太陽從東方升起。", "supports"),
    ("太陽從西方升起。", "refutes"),
    ("太陽從西邊落下。", "supports"),
    ("太陽從東邊落下。", "refutes"),
    ("月球是地球的衛星。", "supports"),
    ("中國最長的河流是長江。", "supports"),
    ("中國最長的河流是黃河。", "refutes"),
    ("中国最长的河流是长江。", "supports"),
    ("世界最高峰是聖母峰。", "supports"),
    ("世界最高峰是聖母峰（珠穆朗瑪峰）。", "supports"),
    ("世界上面積最大的國家是俄羅斯。", "supports"),
    ("世界上面積最大的國家是中國。", "refutes"),
    ("太平洋是世界上面積最大的海洋。", "supports"),
    ("太平洋是世界上面積最小的海洋。", "refutes"),
    ("北極在南極的北邊。", "supports"),
    ("南極比北極更寒冷。", "supports"),

    # ============ 物理/科学 ============
    ("水在攝氏一百度沸騰。", "supports"),
    ("水在攝氏0度結冰。", "supports"),
    ("水在攝氏一百度結冰。", "refutes"),
    ("光速約為每秒三十萬公里。", "supports"),
    ("聲音在真空中無法傳播。", "supports"),
    ("聲音的傳播速度比光慢。", "supports"),
    ("重力加速度約為每秒平方九點八米。", "supports"),
    ("地球的重力比月球大。", "supports"),
    ("水的密度比油大。", "supports"),
    ("鐵比木頭重。", "supports"),
    ("能量守恆定律指出能量不能被創造或消滅。", "supports"),
    ("萬有引力是牛頓發現的。", "supports"),
    ("相對論是愛因斯坦提出的。", "supports"),
    ("自然數包括零和正整數。", "supports"),
    ("圓周率π約等於3.14159。", "supports"),
    ("一個標準大氣壓約等於101.325千帕。", "supports"),
    ("世界上最大的動物是藍鯨。", "supports"),
    ("世界上最大的動物是大象。", "refutes"),

    # ============ 生物 ============
    ("人類離不開氧氣。", "supports"),
    ("植物通過光合作用產生氧氣。", "supports"),
    ("心臟是人體最重要的器官之一。", "supports"),
    ("人體最堅硬的物質是牙齒。", "supports"),
    ("人類有23對染色體。", "supports"),
    ("鳥類是恆溫動物。", "supports"),
    ("鯨魚是哺乳動物。", "supports"),
    ("鯨魚是魚類。", "refutes"),
    ("蝙蝠是哺乳動物。", "supports"),
    ("蝙蝠是鳥類。", "refutes"),
    ("企鵝是鳥類。", "supports"),
    ("企鵝是哺乳動物。", "refutes"),
    ("蜘蛛是節肢動物。", "supports"),
    ("蜘蛛是昆蟲。", "refutes"),

    # ============ 历史 ============
    ("秦始皇統一了中國。", "supports"),
    ("牛頓發現了萬有引力。", "supports"),
    ("愛因斯坦提出了相對論。", "supports"),
    ("哥倫布發現了美洲。", "supports"),
    ("孔子是中國古代的偉大思想家。", "supports"),
    ("第二次世界大戰於1939年爆發。", "supports"),
    ("中華人民共和國成立於1949年。", "supports"),

    # ============ 生活/社交 ============
    ("水的化學式是H2O。", "supports"),
    ("水的化學式是CO2。", "refutes"),
    ("二氧化碳的化學式是CO2。", "supports"),
    ("健康飲食應該包含蔬菜水果。", "supports"),
    ("睡眠對於身體健康至關重要。", "supports"),
    ("經常運動有益健康。", "supports"),
    ("吸煙有害健康。", "supports"),
    ("飲用過量酒精有害健康。", "supports"),
    ("一天有24小時。", "supports"),
    ("一年有365天。", "supports"),
    ("一週有7天。", "supports"),
    ("一小時有60分鐘。", "supports"),
    ("一年有十二個月。", "supports"),
    ("一月是一年的第一個月。", "supports"),
    ("聖誕節是12月25日。", "supports"),
    ("聖誕節是12月24日。", "refutes"),
    ("雷雨時不應在大樹下躲避。", "supports"),

    # ============ 人物 ============
    ("蘇格拉底是古希臘哲學家。", "supports"),
    ("蘇格拉底是中國哲學家。", "refutes"),
    ("孔子是中國人。", "supports"),
    ("孫中山是中國近代革命家。", "supports"),
    ("莎士比亞是英國著名戲劇家。", "supports"),
    ("牛頓是英國物理學家。", "supports"),
    ("愛因斯坦是德國出生的物理學家。", "supports"),
]


def build_supplement_kb():
    """构建补充 KB 保存为 json（供 build_cfever_index.py 使用）"""
    import json
    import os
    from pathlib import Path

    out_path = Path(__file__).parent.parent / "data" / "cfever_index" / "supplement_kb.json"
    output = [
        {"claim": c, "label": l, "domain": "常识"}
        for c, l in COMMON_SENSE_FACTS
    ]
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"补充知识库已保存: {out_path}")
    print(f"  共 {len(output)} 条 ({sum(1 for x in output if x['label']=='supports')} supports + {sum(1 for x in output if x['label']=='refutes')} refutes)")
    return output


if __name__ == "__main__":
    build_supplement_kb()
