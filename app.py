import streamlit as st
import pandas as pd
from src.automata import identifier_dfa,number_dfa,delimiter_pda
from src.parser import analyze_program
st.set_page_config(page_title="Smart Language Analyzer",page_icon="🧩",layout="wide")
st.title("🧩 Smart Programming Language Lexical & Syntax Analyzer")
st.caption("DFA • Pushdown Automata • Context-Free Grammars")
page=st.sidebar.radio("NAVIGATION",["Dashboard","Identifier DFA","Numeric DFA","Delimiter PDA","Syntax Analyzer (CFG)","Test Bench & Theory"])
st.sidebar.caption("Formal Languages and Automata | Combined Task 2 + Task 3")
def result(ok,msg): (st.success if ok else st.error)(("ACCEPTED — " if ok else "REJECTED — ")+msg)
def show(rows,cols):
    if rows: st.dataframe(pd.DataFrame(rows,columns=cols),use_container_width=True,hide_index=True)
    else: st.info("No trace available.")

if page=="Dashboard":
    st.subheader("Project Dashboard")
    st.write("A mini compiler front-end demonstrating lexical recognition and syntax validation.")
    a,b,c,d=st.columns(4); a.metric("DFA recognizers","2"); b.metric("Stack PDA","1"); c.metric("CFG statement types","2"); d.metric("Core modules","5")
    st.graphviz_chart('''digraph G { rankdir=TB; node [shape=box,style="rounded,filled",fillcolor="#eaf2fb"];
    A [label="Source Input"]; B [label="DFA Token Recognition\\nIdentifier + Number"]; C [label="PDA Delimiter Stack"];
    D [label="CFG Syntax Parser"]; E [label="Accepted / Rejected\\nTokens + Trace + Error"]; A->B->C->D->E; }''')
    st.markdown("### Example teaching-language program")
    st.code("score = mark1 + mark2 * 2;\\nif (score >= 50) {\\n    result = score;\\n}",language="c")
    st.info("This is a small educational language, not a complete Python, C or Java compiler.")

elif page=="Identifier DFA":
    st.subheader("Identifier Recognition — DFA")
    st.write("First character: letter or underscore. Remaining characters: letters, digits or underscores.")
    st.graphviz_chart('''digraph D { rankdir=LR; node [shape=circle]; start [shape=point]; q1 [shape=doublecircle];
    start->q0; q0->q1 [label="letter / _"]; q1->q1 [label="letter / digit / _"];
    q0->dead [label="other"]; q1->dead [label="other"]; dead [shape=box,label="DEAD"]; }''')
    x=st.text_input("Enter identifier",placeholder="student_name")
    if st.button("Run identifier DFA",type="primary"):
        ok,tr,state=identifier_dfa(x); result(ok,"Valid identifier." if ok else "Must start with a letter or underscore.")
        st.write("Final state:",state); show(tr,["Input","Input class","State","Action"])

elif page=="Numeric DFA":
    st.subheader("Numeric Constant Recognition — DFA")
    st.write("Integer = digit+ ; decimal = digit+ '.' digit+. Signs and exponent notation are excluded.")
    st.graphviz_chart('''digraph N { rankdir=LR; node [shape=circle]; start [shape=point]; q1 [shape=doublecircle]; q3 [shape=doublecircle];
    start->q0; q0->q1 [label="digit"]; q1->q1 [label="digit"]; q1->q2 [label="."];
    q2->q3 [label="digit"]; q3->q3 [label="digit"]; q0->dead [label="other"]; q2->dead [label="other"]; dead [shape=box]; }''')
    x=st.text_input("Enter numeric constant",placeholder="125.75")
    if st.button("Run numeric DFA",type="primary"):
        ok,tr,state=number_dfa(x); result(ok,"Valid integer or decimal." if ok else "Invalid numeric constant.")
        st.write("Final state:",state); show(tr,["Input","Input class","State","Action"])

elif page=="Delimiter PDA":
    st.subheader("Balanced Delimiter Checker — PDA")
    st.write("Opening delimiters are pushed; matching closing delimiters pop the stack.")
    st.graphviz_chart('''digraph P { rankdir=LR; node [shape=box,style="rounded"]; R [label="Read symbol"]; O [label="Opening?"];
    PUSH [label="PUSH"]; C [label="Closing?"]; M [label="Matches stack top?"]; POP [label="POP"];
    REJ [label="Reject",color=red]; END [label="End of input"]; ACC [label="Accept if stack empty",shape=doublecircle];
    R->O; O->PUSH [label="yes"]; PUSH->R; O->C [label="no"]; C->M [label="yes"];
    M->POP [label="yes"]; POP->R; M->REJ [label="no"]; C->R [label="no"]; R->END [label="EOF"]; END->ACC; }''')
    x=st.text_area("Enter source fragment",placeholder="if (a[2] > b) { total = (x+y); }")
    if st.button("Run delimiter PDA",type="primary"):
        ok,tr,stack=delimiter_pda(x); result(ok,"All delimiters correctly nested." if ok else "Mismatch or unmatched opener.")
        show(tr,["Read symbol","Stack after input","Stack action"])

elif page=="Syntax Analyzer (CFG)":
    st.subheader("Mini Programming Language Syntax Analyzer — CFG")
    st.code("Program -> Statement+\\nStatement -> Assignment | IfStatement\\nAssignment -> id = Expr ;\\nIfStatement -> if ( Condition ) { Statement+ }\\nCondition -> Expr RelOp Expr\\nRelOp -> < | > | <= | >= | == | !=\\nExpr -> Term ((+ | -) Term)*\\nTerm -> Factor ((* | /) Factor)*\\nFactor -> ( Expr ) | id | number")
    sample="score = mark1 + mark2 * 2;\\nif (score >= 50) {\\n    result = score;\\n}"
    src=st.text_area("Source code",value=sample,height=190)
    if st.button("Analyze syntax",type="primary"):
        ok,steps,msg,tokens=analyze_program(src); result(ok,msg)
        l,r=st.columns([1,2])
        with l: st.markdown("#### Tokens"); st.write(tokens)
        with r: st.markdown("#### Grammar / parser trace"); show([(s,) for s in steps],["Production or action"])

elif page=="Test Bench & Theory":
    st.subheader("Test Bench — Expected Results")
    examples={
    "Identifier DFA":[["student_name","Accept"],["_value","Accept"],["2student","Reject"],["first-name","Reject"]],
    "Numeric DFA":[["123","Accept"],["45.67","Accept"],[".75","Reject"],["12.3.4","Reject"]],
    "Delimiter PDA":[["{(a+b)}","Accept"],["([{}])","Accept"],["([)]","Reject"],["((x)","Reject"]],
    "CFG Syntax":[["x = a+b;","Accept"],["total = 8.5 * count;","Accept"],["if (x >= 10) { y = x; }","Accept"],["x = + a;","Reject"],["if (x 10) { y = 1; }","Reject"]]}
    for title,rows in examples.items():
        st.markdown("#### "+title); st.table(pd.DataFrame(rows,columns=["Input","Expected result"]))
    st.markdown("### Model selection and limitations")
    st.write("- DFA recognizes regular identifier and numeric-token patterns.")
    st.write("- PDA uses stack memory for nested delimiters.")
    st.write("- CFG describes recursive expressions and statement syntax.")
    st.write("- The parser performs syntax analysis only; it does not perform semantic checks, type checking, code generation or execution.")
    st.write("- Only the operators and statements listed in the grammar are supported.")
st.divider()
st.caption("Academic demonstration project • Formal Languages and Automata")
