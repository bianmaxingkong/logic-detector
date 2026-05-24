# LogicDetector ACL 2026 Paper PDF Error Check Report

**Check Date**: 2026-04-08  
**Check Target**: logic_detector_acl2026_final.pdf  
**Checked By**: Huoyan Team

---

## 🔴 Critical Errors (Must Fix)

### 1. LaTeX Source File Name Fragment Leaked
**Location**: Line 102  
**Issue**: `inputtechd evelopments ummary.tex`  
**Description**: Temporary LaTeX compilation file name fragment mixed into the body text  
**Fix**: Delete this line

---

### 2. Python Code Mixed into References
**Location**: Lines 1603-1617 (Goffredo et al. citation)  
**Issue**: Code snippet mixed into the bibliography, causing severe formatting issues  
**Description**: Python code (import requests, etc.) appearing inside citation text  
**Fix**: Delete all code, retain correct citation format

---

### 3. Version Number Inconsistency
**Location**:
- Lines 103, 108, 189, 205: **v2.0**
- Line 1977 (Appendix B): **v3.2**

**Fix**: Unify to either v2.0 or v3.2

---

### 4. Table Number Order Chaos
**Location**: Lines 1457-1459  
**Issue**:
```
Line 1457: Table 9: Cross-model generalization results
Line 1459: Table 6: Module contribution analysis
```
**Description**: Table 6 should appear before Table 9  
**Fix**: Reorder table numbers

---

### 5. Number Range Missing Hyphen
**Location**: Line 334  
**Issue**: `achieving 6070% accuracy`  
**Should be**: `achieving 60-70% accuracy`

---

### 6. PDF Line Numbers Mixed into Body Text
**Location**: Multiple locations throughout  
**Issue**: Line numbers `001`, `002`, `003`... extracted into the text  
**Description**: PDF generation did not properly remove line numbers  
**Fix**: Regenerate PDF with line numbers disabled

---

## 🟡 Spelling/Formatting Errors

### 7. Compound Words Missing Hyphens
| Location | Error | Correct |
|----------|-------|---------|
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

### 8. Proper Noun Capitalization/Formatting Inconsistency
| Location | Issue | Suggestion |
|----------|-------|------------|
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

### 9. Name Formatting Issues
| Location | Issue | Suggestion |
|----------|-------|------------|
| Line 1582, 1893 | Oyvind | Øyvind (if special characters available) |
| Line 1829 | Küttler | ✓ Correct |
| Line 1829 | Rocktäschel | ✓ Correct |
| Line 1792 | DwivediYu | Dwivedi-Yu |
| Line 1886 | Jeevana Priya Inala | ✓ Correct |
| Line 1901 | S. M. Zaman | ✓ Correct |
| Line 1902 | Vaishnavi Rawte, Aman Chadha | ✓ Correct |
| Line 1871, 1944 | Xinxi Lyu, Yinqiao Lyu | ✓ Correct |

---

### 10. Page Range Breaks
| Location | Issue | Description |
|----------|-------|-------------|
| Line 1816 | `pages 1–` (line break) `10` | Should be on one line |
| Line 1830 | `pages 9459–` (line break) `9474` | Should be on one line |
| Line 1585 | `pages 3882–` (line break) `3890` | Should be on one line |

---

### 11. arXiv Citation Format Inconsistency
| Location | Issue |
|----------|-------|
| Lines 1855, 1875, 1904, 1916 | `arXiv preprint` then line break before arXiv ID |
| Line 1924 | `arXiv` on separate line before `preprint arXiv:...` |

**Suggestion**: Unify to `arXiv preprint arXiv:XXXX.XXXXX.`

---

### 12. Number Range Format Inconsistency
| Location | Issue |
|----------|-------|
| Lines 1432, 1529 | `(22 50 types)` missing arrow or "to" |
| Lines 1433, 1529 | `(100 1000+ facts)` missing arrow or "to" |

**Suggestion**: Change to `(22 → 50 types)` or `(22 to 50 types)`

---

### 13. Performance Data Formatting Issues
| Location | Issue | Should Be |
|----------|-------|-----------|
| Line 856 | `1015s` | `10-15s` |
| Line 1682 | `10,000+` (line break) `queries/day` | Same line |

---

### 14. Anonymous Placeholders Not Cleaned
| Location | Content |
|----------|---------|
| Line 4 | `Anonymous ACL submission` |
| Line 1567 | `[Anonymous Funding]` |
| Line 1975 | `GitHub: [Anonymous]` |

**Description**: May be kept for double-blind review; replace for final version

---

## 🟢 Content Verification (Correct Parts)

### Key Data Consistency Check ✓
- 600 test instances: consistent throughout ✓
- 81.7% accuracy: consistent throughout ✓
- 83.3% F1 score: consistent throughout ✓
- 22 fallacy types: consistent throughout ✓
- 150+ detection patterns: consistent throughout ✓
- 100+ common knowledge facts: consistent throughout ✓
- Fusion weights (0.4, 0.3, 0.2, 0.1): consistent throughout ✓
- <1s response time: consistent throughout ✓
- <100MB memory: consistent throughout ✓

### Citation Consistency Check ✓
- Alansari and Luqman (2025): 7 citations, consistent format ✓
- All arXiv IDs formatted correctly ✓

---

## 📋 Fix Priorities

### P0 - Immediate Fix (Affects Reviewer Impression)
1. ✅ Delete LaTeX file name (`inputtechd evelopments ummary.tex`)
2. ✅ Clean Python code from references
3. ✅ Unify version numbers (v2.0 or v3.2)
4. ✅ Fix table number order
5. ✅ Fix `6070%` → `60-70%`

### P1 - High Priority (Formatting Standards)
6. Add hyphens to all compound words (learning-based, etc.)
7. Unify proper noun capitalization (LLM-Check, BERTScore, etc.)
8. Fix page range break issues
9. Fix number range format `(22 → 50)`

### P2 - Medium Priority (Detail Refinement)
10. Unify arXiv citation format
11. Fix `1015s` → `10-15s`
12. Check name spellings (Dwivedi-Yu, etc.)

### P3 - Low Priority (Optional)
13. Replace Anonymous placeholders (if determined)
14. Remove PDF line numbers (if affecting readability)

---

## 🔧 Fix Suggestions

### LaTeX Source File Check List
```bash
# 1. Check and delete all debug code
grep -r "python3 -m" paper/
grep -r "import requests" paper/
grep -r "\\.tex" paper/

# 2. Check version numbers
grep -r "v2\\.0\\|v3\\.2" paper/

# 3. Check compound words
grep -r "learningbased\\|reasoningbased\\|selfconsistency" paper/

# 4. Check proper nouns
grep -r "Llm-check\\|Bertscore\\|Kgbert\\|Factscore" paper/

# 5. Check number ranges
grep -r "6070\\|1015s\\|22 50\\|100 1000" paper/
```

### Recommended Tools
- **Grammarly**: Spell and grammar checking
- **LaTeX Workshop (VSCode)**: Real-time preview
- **Overleaf**: Online collaborative editing
- **pandoc**: Format conversion and checking

---

## 📊 Error Statistics

| Category | Count |
|----------|-------|
| Critical Errors | 6 |
| Spelling/Formatting Errors | 30+ |
| Proper Noun Issues | 12 |
| Citation Format Issues | 8 |
| **Total** | **56+** |

---

## ✅ Post-Fix Checklist

- [ ] Recompile PDF
- [ ] Remove all line numbers
- [ ] Check reference completeness
- [ ] Verify table number order
- [ ] Run spell check
- [ ] Manual full-text readthrough
- [ ] Generate final version

---

**Report Generated**: 2026-04-08 11:45  
**Check Tools**: pdftotext + manual review  
**Suggestion**: Fix P0-level errors immediately, then resubmit
