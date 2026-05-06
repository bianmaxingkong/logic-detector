import sys; sys.path.insert(0, '.')
import re
from src.modules.logic_validator import LogicValidator, FallacyType

lv = LogicValidator()

# 测试现有规则 + 新加规则的匹配效果
print("=== 精确模式测试 ===")

# 形式逻辑精确匹配
pat_ac = r'P→Q[,，]+Q[,，]+(因此|所以) P'
pat_da = r'P→Q[,，]+¬P[,，]+(因此|所以) ¬Q'

tests_all = [
    'P→Q, Q, 因此 P',
    'P→Q, Q, 所以 P',
    'P→Q, Q, ∴P',
    'P→Q, ¬P, 因此 ¬Q',
    'P→Q, ¬P, 所以 ¬Q',
    'P→Q, ¬P, ∴¬Q',
]

for t in tests_all:
    ac = bool(re.search(pat_ac, t))
    da = bool(re.search(pat_da, t))
    lv_r = lv.validate(t)
    lv_ok = len(lv_r) > 0
    ac_label = 'AC' if ac else ''
    da_label = 'DA' if da else ''
    print(f'  {ac_label}{da_label}\tlv={lv_ok}\t{t}')

print()
print("=== 中文精确模式 ===")
# "只有才"模式
pat_only_ac = r'只有.*?才.*?[。，].*?(成功|实现|完成|发生|到了)[。，]所以.*'
for t in ['只有努力才能成功。他成功了。所以他努力了。']:
    m = re.search(pat_only_ac, t)
    lv_r = lv.validate(t)
    print(f'  lv={len(lv_r)>0}  reg={bool(m)}  \t{t[:50]}')

# "如果会"模式 - 用更严格的排除
# 排除：第二前提中包含了条件句前件的词（那其实是modus ponens）
pat_ac_if = r'如果(.{,4})[会就](.{,4})[。，]((?!下雨|努力|天晴|开门|涨价|起风|P|A)[^。，]{1,6})[。，]所以.*?'
# 这个不好，太人工了

# 更好的方案：modus ponens 第二句=前件（短词，一般1-3字）
#            肯定后件 第二句=后件变体（较长或含不同关键词）
# 量化方法：看第二句的字数
def is_short_premise(txt):
    """检查"如果"条件句后的第二句是否是短词（前件特征）"""
    m = re.search(r'如果([^。，]+)[。，]([^。，]+)[。，]([^。，]+)[。，]所以', txt)
    if m:
        second = m.group(3)  # 第二前提
        first_consequent = m.group(2)  # 条件句后件
        # 第二前提很短(<=3字)且与条件句后件不同 => 可能是前件
        if len(second) <= 4 and second not in first_consequent:
            return True  # modus ponens
        # 第二前提与条件句后件有重叠 => 可能是后件变体
        if any(c in first_consequent for c in second):
            return False  # 肯定后件
    return None  # 不确定

print()
print("=== 改进的匹配策略 ===")
tests_cn = [
    ('如果下雨，地面会湿。地面湿了。所以下雨了。', True),  # 谬误
    ('如果下雨，地面会湿。下雨了。所以地面会湿。', False), # 有效
    ('只有努力才能成功。他成功了。所以他努力了。', True),   # 谬误
    ('如果下雨，地面会湿。地面没湿。所以没下雨。', False),  # 有效(mt)
]

for t, expected in tests_cn:
    verdict = is_short_premise(t)
    print(f'  is_short_prem: {verdict}  expected: {"谬误" if expected else "有效"}  {t[:50]}')
