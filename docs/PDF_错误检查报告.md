# LogicDetector ACL 2026 论文 PDF 错误检查报告

**检查日期**: 2026-04-08  
**检查对象**: logic_detector_acl2026_final.pdf  
**检查人**: 火眼团队

---

## 🔴 严重错误（必须修复）

### 1. LaTeX 源文件名片段泄露
**位置**: Line 102  
**问题**: `inputtechd evelopments ummary.tex`  
**说明**: LaTeX 编译时的临时文件名片段混入正文  
**修复**: 删除此行内容

---

### 2. 参考文献中混入 Python 代码
**位置**: Line 1603-1617 (Goffredo et al. 引用处)  
**问题**: 
```
python3 -m logicdetector --port 8000 assessment in the age of instruction-following large
language models. In Proceedings of the 2022 ConAPI Integration:
ference on Empirical Methods in Natural Language
Processing,
pages 1234–1245.
import requests

response = requests.post('http://localhost:8000/analyze',
json={'text': ''})
print(response.json())
```
**说明**: 代码片段混入参考文献，严重排版错误  
**修复**: 删除所有代码，保留正确的引用格式

---

### 3. 版本号不一致
**位置**: 
- Line 103, 108, 189, 205: **v2.0**
- Line 1977 (Appendix B): **v3.2**

**修复**: 统一为 v2.0 或 v3.2

---

### 4. 表格编号顺序混乱
**位置**: Line 1457-1459  
**问题**:
```
Line 1457: Table 9: Cross-model generalization results
Line 1459: Table 6: Module contribution analysis
```
**说明**: Table 6 应该在 Table 9 之前  
**修复**: 重新排序表格编号

---

### 5. 数字范围缺少连字符
**位置**: Line 334  
**问题**: `achieving 6070% accuracy`  
**应为**: `achieving 60-70% accuracy`

---

### 6. PDF 行号混入正文
**位置**: 全文多处  
**问题**: `001`, `002`, `003`... 等行号被提取到文本中  
**说明**: PDF 生成时未正确移除行号  
**修复**: 重新生成 PDF，关闭行号显示

---

## 🟡 拼写/格式错误

### 7. 复合词缺少连字符
| 位置 | 错误 | 正确 |
|------|------|------|
| Line 21 | learningbased | learning-based |
| Line 22 | reasoningbased | reasoning-based |
| Line 22 | selfconsistency-based | self-consistency-based |
| Line 22 | multisampling | multi-sampling |
| Line 97 | uncertaintybased | uncertainty-based |
| Line 97 | embeddingbased | embedding-based |
| Line 312 | selfconsistency | self-consistency |
| Line 572 | learningbased | learning-based |
| Line 1558 | privacysensitive | privacy-sensitive |
| Line 1351 | crossmodel | cross-model |
| Line 1740 | multimodule | multi-module |
| Line 314 | neurosymbolic | neuro-symbolic |
| Line 1888 | neurosymbolic | neuro-symbolic |

---

### 8. 专有名词大小写/格式不统一
| 位置 | 问题 | 建议 |
|------|------|------|
| Line 1594 | Llm-check | LLM-Check |
| Line 1875, 1932 | Bertscore | BERTScore |
| Line 1924 | Kgbert | KG-BERT |
| Line 1830 | nlp | NLP |
| Line 1875 | long form | long-form |
| Line 1793-1794 | retrieval augmented | retrieval-augmented |
| Line 1810 | knowledgeintensive | knowledge-intensive |
| Line 1637 | expertannotated | expert-annotated |
| Line 1017 | Multisampling | Multi-sampling |
| Line 1874 | Factscore | FActScore |
| Line 1894 | Proofwriter | ProofWriter |
| Line 1915 | Neurologic | NeuroLogic |
| Line 1854 | concept learner | Concept Learner |

---

### 9. 人名格式问题
| 位置 | 问题 | 建议 |
|------|------|------|
| Line 1582, 1893 | Oyvind | Øyvind (如有特殊字符) |
| Line 1829 | Küttler | ✓ 正确 |
| Line 1829 | Rocktäschel | ✓ 正确 |
| Line 1792 | DwivediYu | Dwivedi-Yu |
| Line 1886 | Jeevana Priya Inala | ✓ 正确 |
| Line 1901 | S. M. Zaman | ✓ 正确 |
| Line 1902 | Vaishnavi Rawte, Aman Chadha | ✓ 正确 |
| Line 1871, 1944 | Xinxi Lyu, Yinqiao Lyu | ✓ 正确 |

---

### 10. 页码范围断开
| 位置 | 问题 | 说明 |
|------|------|------|
| Line 1816 | `pages 1–` (换行) `10` | 应在一行 |
| Line 1830 | `pages 9459–` (换行) `9474` | 应在一行 |
| Line 1585 | `pages 3882–` (换行) `3890` | 应在一行 |

---

### 11. arXiv 引用格式不一致
| 位置 | 问题 |
|------|------|
| Line 1855, 1875, 1904, 1916 | `arXiv preprint` 换行后才有 arXiv 号 |
| Line 1924 | `arXiv` 换行后 `preprint arXiv:...` |

**建议**: 统一格式为 `arXiv preprint arXiv:XXXX.XXXXX.`

---

### 12. 数字范围格式不统一
| 位置 | 问题 |
|------|------|
| Line 1432, 1529 | `(22 50 types)` 缺少箭头或"to" |
| Line 1433, 1529 | `(100 1000+ facts)` 缺少箭头或"to" |

**建议**: 改为 `(22 → 50 types)` 或 `(22 to 50 types)`

---

### 13. 性能数据格式问题
| 位置 | 问题 | 应为 |
|------|------|------|
| Line 856 | `1015s` | `10-15s` |
| Line 1682 | `10,000+` (换行) `queries/day` | 应在一行 |

---

### 14. 匿名占位符未清理
| 位置 | 内容 |
|------|------|
| Line 4 | `Anonymous ACL submission` |
| Line 1567 | `[Anonymous Funding]` |
| Line 1975 | `GitHub: [Anonymous]` |

**说明**: 如为双盲评审可保留，最终版本需替换

---

## 🟢 内容验证（正确部分）

### 关键数据一致性检查 ✓
- 600 测试实例：全文一致 ✓
- 81.7% 准确率：全文一致 ✓
- 83.3% F1 分数：全文一致 ✓
- 22 种谬误类型：全文一致 ✓
- 150+ 检测模式：全文一致 ✓
- 100+ 常识事实：全文一致 ✓
- 融合权重 (0.4, 0.3, 0.2, 0.1)：全文一致 ✓
- <1s 响应时间：全文一致 ✓
- <100MB 内存：全文一致 ✓

### 引用一致性检查 ✓
- Alansari and Luqman (2025): 7 处引用，格式统一 ✓
- 所有 arXiv 编号格式正确 ✓

---

## 📋 修复优先级

### P0 - 立即修复（影响评审印象）
1. ✅ 删除 LaTeX 文件名 (`inputtechd evelopments ummary.tex`)
2. ✅ 清理参考文献中的 Python 代码
3. ✅ 统一版本号 (v2.0 或 v3.2)
4. ✅ 修正表格编号顺序
5. ✅ 修复 `6070%` → `60-70%`

### P1 - 高优先级（格式规范）
6. 添加所有复合词连字符 (learning-based 等)
7. 统一专有名词大小写 (LLM-Check, BERTScore 等)
8. 修复页码范围断开问题
9. 修复数字范围格式 `(22 → 50)`

### P2 - 中优先级（细节完善）
10. 统一 arXiv 引用格式
11. 修复 `1015s` → `10-15s`
12. 检查人名拼写 (Dwivedi-Yu 等)

### P3 - 低优先级（可选）
13. 替换 Anonymous 占位符（如已确定）
14. 移除 PDF 行号（如影响阅读）

---

## 🔧 修复建议

### LaTeX 源文件检查清单
```bash
# 1. 检查并删除所有调试代码
grep -r "python3 -m" paper/
grep -r "import requests" paper/
grep -r "\.tex" paper/

# 2. 检查版本号
grep -r "v2\.0\|v3\.2" paper/

# 3. 检查复合词
grep -r "learningbased\|reasoningbased\|selfconsistency" paper/

# 4. 检查专有名词
grep -r "Llm-check\|Bertscore\|Kgbert\|Factscore" paper/

# 5. 检查数字范围
grep -r "6070\|1015s\|22 50\|100 1000" paper/
```

### 推荐工具
- **Grammarly**: 检查拼写和语法
- **LaTeX Workshop (VSCode)**: 实时预览
- **Overleaf**: 在线协作编辑
- **pandoc**: 格式转换和检查

---

## 📊 错误统计

| 类别 | 数量 |
|------|------|
| 严重错误 | 6 |
| 拼写/格式错误 | 30+ |
| 专有名词问题 | 12 |
| 引用格式问题 | 8 |
| **总计** | **56+** |

---

## ✅ 修复后检查清单

- [ ] 重新编译 PDF
- [ ] 删除所有行号
- [ ] 检查参考文献完整性
- [ ] 验证表格编号顺序
- [ ] 运行拼写检查
- [ ] 人工通读全文
- [ ] 生成最终版本

---

**报告生成时间**: 2026-04-08 11:45  
**检查工具**: pdftotext + 人工审核  
**建议**: 立即修复 P0 级别错误后重新提交
