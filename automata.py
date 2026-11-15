def identifier_dfa(text):
    state="q0"; trace=[("START","—",state,"Initial")]
    if not text: return False,trace,state
    for ch in text:
        if state=="q0": state="q1" if ch.isalpha() or ch=="_" else "DEAD"
        else: state="q1" if ch.isalpha() or ch.isdigit() or ch=="_" else "DEAD"
        trace.append((ch,"letter/digit/underscore",state,"Transition"))
        if state=="DEAD": break
    return state=="q1",trace,state

def number_dfa(text):
    state="q0"; trace=[("START","—",state,"Initial")]
    if not text: return False,trace,state
    for ch in text:
        if state=="q0": state="q1" if ch.isdigit() else "DEAD"
        elif state=="q1": state="q1" if ch.isdigit() else ("q2" if ch=="." else "DEAD")
        elif state=="q2": state="q3" if ch.isdigit() else "DEAD"
        elif state=="q3": state="q3" if ch.isdigit() else "DEAD"
        trace.append((ch,"digit / decimal point",state,"Transition"))
        if state=="DEAD": break
    return state in ("q1","q3"),trace,state

def delimiter_pda(source):
    pairs={")":"(","]":"[","}":"{"}; opens=set(pairs.values())
    stack=[]; trace=[("START","empty","Initial stack")]
    for ch in source:
        action="Ignore non-delimiter"
        if ch in opens: stack.append(ch); action=f"PUSH {ch}"
        elif ch in pairs:
            if not stack or stack[-1]!=pairs[ch]:
                trace.append((ch," ".join(stack) or "empty",f"REJECT mismatch at {ch}"))
                return False,trace,stack
            action=f"POP {stack.pop()}"
        trace.append((ch," ".join(stack) or "empty",action))
    ok=not stack
    trace.append(("END","empty" if ok else " ".join(stack),"ACCEPT" if ok else "REJECT unmatched opener"))
    return ok,trace,stack
