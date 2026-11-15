import re
TOKEN=re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|(==|!=|<=|>=|[+\-*/<>=(){};]))")
class SyntaxErrorFLA(Exception): pass

class Parser:
    def __init__(self,source):
        self.tokens=self.tokenize(source); self.pos=0; self.steps=[]
    @staticmethod
    def tokenize(source):
        out=[]; pos=0
        while pos<len(source):
            if not source[pos:].strip(): break
            m=TOKEN.match(source,pos)
            if not m: raise SyntaxErrorFLA(f"Unrecognized character near {source[pos:pos+10]!r}")
            a,b,c=m.groups(); out.append(a or b or c); pos=m.end()
        return out
    def cur(self): return self.tokens[self.pos] if self.pos<len(self.tokens) else "EOF"
    def take(self,expected=None):
        t=self.cur()
        if expected is not None and t!=expected: raise SyntaxErrorFLA(f"Expected '{expected}', found '{t}'")
        self.steps.append("Matched "+t); self.pos+=1; return t
    def program(self):
        self.steps.append("Program -> Statement+"); n=0
        while self.cur()!="EOF": self.statement(); n+=1
        if not n: raise SyntaxErrorFLA("Program must contain at least one statement")
        self.steps.append("Program -> accepted")
        return self.steps
    def statement(self):
        if self.cur()=="if": self.if_stmt()
        else: self.assignment()
    def assignment(self):
        self.steps.append("Assignment -> id = Expr ;")
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*",self.cur()):
            raise SyntaxErrorFLA("Assignment must start with an identifier")
        self.take(); self.take("="); self.expr(); self.take(";")
    def if_stmt(self):
        self.steps.append("IfStatement -> if ( Condition ) { Statement+ }")
        self.take("if"); self.take("("); self.condition(); self.take(")"); self.take("{")
        n=0
        while self.cur() not in ("}","EOF"): self.statement(); n+=1
        if not n: raise SyntaxErrorFLA("If block must contain at least one statement")
        self.take("}")
    def condition(self):
        self.steps.append("Condition -> Expr RelOp Expr"); self.expr()
        if self.cur() not in ("<",">","<=",">=","==","!="):
            raise SyntaxErrorFLA(f"Relational operator expected, found '{self.cur()}'")
        self.take(); self.expr()
    def expr(self):
        self.steps.append("Expr -> Term ((+ | -) Term)*"); self.term()
        while self.cur() in ("+","-"): self.take(); self.term()
    def term(self):
        self.steps.append("Term -> Factor ((* | /) Factor)*"); self.factor()
        while self.cur() in ("*","/"): self.take(); self.factor()
    def factor(self):
        if self.cur()=="(":
            self.steps.append("Factor -> ( Expr )"); self.take("("); self.expr(); self.take(")")
        elif re.fullmatch(r"\d+(?:\.\d+)?",self.cur()) or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*",self.cur()):
            self.steps.append("Factor -> id | number"); self.take()
        else: raise SyntaxErrorFLA(f"Operand expected, found '{self.cur()}'")

def analyze_program(source):
    p=None
    try:
        p=Parser(source); return True,p.program(),"The source follows the defined grammar.",p.tokens
    except SyntaxErrorFLA as e:
        return False,p.steps if p else [],str(e),p.tokens if p else []
