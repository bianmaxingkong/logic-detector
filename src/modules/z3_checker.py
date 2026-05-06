"""M3 replacement: Z3-based formal logic inference checker"""
import re
import z3

IMPLIES_SYMBOLS = {'→', '⇒', '->', '=>'}

def _has_arrow(s):
    return any(c in s for c in IMPLIES_SYMBOLS)

def extract_vars(text):
    """Extract proposition variables (A-Z, or Chinese content phrases)"""
    letters = sorted(set(re.findall(r'\b([A-Z])\b', text)))
    if letters:
        return letters
    result = set()
    for chunk in re.split(r'[。，,;、：:？！\s→∨∧¬↔⇒⇔()（）]', text):
        chunk = chunk.strip()
        if not chunk: continue
        if not any('\u4e00' <= c <= '\u9fff' for c in chunk): continue
        if chunk in {'如果','则','就','那么','因此','为','真','假','成立','不','没','或',
                     '且','和','与','因为','所以','而且','或者','但','但是', '了'}:
            continue
        base = re.sub(r'^(没|没有|不)|(不|没有|没了?|了)$', '', chunk)
        if not base: base = chunk
        if len(base) >= 2:
            result.add(base)
    return sorted(result)

def parse_clause(clause, var_map):
    """Parse a single logical clause into Z3 expression"""
    clause = clause.strip()
    if not clause:
        return None
    
    # ¬ / 非 prefix
    m = re.match(r'^(¬|非)\s*(.+)$', clause)
    if m:
        inner = parse_clause(m.group(2), var_map)
        return z3.Not(inner) if inner is not None else None
    
    # 如果/若/要是...则/就/那么... (Chinese implication)
    m = re.match(r'^(?:如果|若|要是)\s*(.+?)\s*(?:则|就|那么|便会|那|就)\s*(.+)$', clause)
    if m:
        a = parse_clause(m.group(1), var_map)
        b = parse_clause(m.group(2), var_map)
        return z3.Implies(a, b) if a is not None and b is not None else None
    
    # Arrow implication
    for arrow in IMPLIES_SYMBOLS:
        if arrow in clause:
            parts = clause.split(arrow, 1)
            a = parse_clause(parts[0].strip(), var_map)
            b = parse_clause(parts[1].strip(), var_map)
            return z3.Implies(a, b) if a is not None and b is not None else None
    
    # ∨ / 或
    if '∨' in clause:
        parts = clause.split('∨', 1)
        a = parse_clause(parts[0].strip(), var_map)
        b = parse_clause(parts[1].strip(), var_map)
        return z3.Or(a, b) if a is not None and b is not None else None
    if '或' in clause:
        parts = clause.split('或', 1)
        a = parse_clause(parts[0].strip(), var_map)
        b = parse_clause(parts[1].strip(), var_map)
        return z3.Or(a, b) if a is not None and b is not None else None
    
    # X为假 / X不成立
    m = re.match(r'^(.+?)\s*(?:为\s*假|不成立|为\s*否|是\s*假)\s*$', clause)
    if m:
        inner = parse_clause(m.group(1).strip(), var_map)
        return z3.Not(inner) if inner is not None else None
    
    # X为真 / X成立
    m = re.match(r'^(.+?)\s*(?:为\s*真|成立|是\s*真)\s*$', clause)
    if m:
        return var_map.get(m.group(1).strip())
    
    # 没/不 prefix
    for prefix in ['没', '没有', '不']:
        if clause.startswith(prefix) and len(clause) > len(prefix):
            inner = parse_clause(clause[len(prefix):], var_map)
            return z3.Not(inner) if inner is not None else None
    
    # Direct/fuzzy variable lookup
    if clause in var_map:
        return var_map[clause]
    for k, v in var_map.items():
        if k in clause or clause in k:
            return v
    return None


class Z3Checker:
    """M3 module: checks formal logic inference validity using Z3"""
    
    def __init__(self):
        pass  # Z3 is stateless, no init needed
    
    def check_inference(self, text):
        """Check if the logical inference in text is valid.
        
        Returns:
            (is_valid, result): 
                is_valid: True if inference is logically valid
                result: 'valid' / 'invalid' / 'unparsed'
        """
        text = text.strip()
        
        # Find conclusion
        conclusion = None
        premises_text = text
        
        for sep in ['因此', '∴']:
            idx = text.find(sep)
            if idx >= 0:
                rest = text[idx + len(sep):].strip()
                rest = re.sub(r'^[：:]', '', rest).strip()
                rest = rest.rstrip('。.！!？?，,')
                conclusion = rest
                premises_text = text[:idx]
                break
        
        if conclusion is None:
            return None, 'unparsed'
        
        vars_list = extract_vars(text)
        if not vars_list:
            return None, 'unparsed'
        
        var_map = {v: z3.Bool(v) for v in vars_list}
        
        is_symbolic = _has_arrow(premises_text) or '∨' in premises_text or '¬' in premises_text
        if is_symbolic:
            premises_raw = [s.strip() for s in re.split(r'[,，、，;；]', premises_text) if s.strip()]
        else:
            premises_raw = [s.strip() for s in re.split(r'[。，,；;]', premises_text) if s.strip()]
        
        premises = []
        for clause_text in premises_raw:
            if not clause_text: continue
            expr = parse_clause(clause_text, var_map)
            if expr is None:
                return None, 'unparsed'
            premises.append(expr)
        
        conc_expr = parse_clause(conclusion, var_map)
        if conc_expr is None or not premises:
            return None, 'unparsed'
        
        solver = z3.Solver()
        for p in premises:
            solver.add(p)
        solver.add(z3.Not(conc_expr))
        
        try:
            result = solver.check()
            is_valid = (result == z3.unsat)
            return is_valid, 'valid' if is_valid else 'invalid'
        except z3.Z3Exception:
            return None, 'unparsed'
    
    def __call__(self, text):
        """Syntactic sugar: call returns is_valid bool or None"""
        is_valid, _ = self.check_inference(text)
        return is_valid
