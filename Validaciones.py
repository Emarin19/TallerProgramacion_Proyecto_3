Num = {"a":"1","b":"2","c":"3","d":"4","e":"5","f":"6","g":"7","h":"8","i":"9","j":"0"}

def nombres(String):
    return nombres_aux(String,9,9,0)
def nombres_aux(String,i,n,Cont):
    for key in Num:
        a = String[i]
        b = Num[key]
        if a != b:
            pass
        else:
            return Cont+n
    i += 1
    Cont += 1
    return nombres_aux(String,i,n,Cont)

def edad(String):
    return edad_aux(String,9,9,0,0)
def edad_aux(String,i,n,ContA,ContB):
    for key in Num:
        a = String[i]
        b = Num[key]
        if a == b:
            ContA = ContA+n
            ContB = nombres_aux(String,ContA+4,ContA+4,0)
            ContC = año(String,ContB,ContB,0)
            return [ContA,ContB,ContC]
        else:
            pass
    i += 1
    ContA += 1
    return edad_aux(String,i,n,ContA,ContB)

def año(String,i,n,Cont):
    for key in Num:
        a = String[i]
        b = Num[key]
        if a == b:
            pass
        elif a == " ":
            return Cont+n
    i += 1
    Cont += 1
    return año(String,i,n,Cont)

"""
Validar que haya un " " entre la tempoarda y las competencias
Validad que Competencias, REP, RGP sean los últimos n caracteres
"""
def edad_a(String):
    return edad_a_aux(String,9,9,0,0)
def edad_a_aux(String,i,n,ContA,ContB):
    for key in Num:
        a = String[i]
        b = Num[key]
        if a == b:
            ContA = ContA+n
            ContB = nombres_aux(String,ContA+4,ContA+4,0)
            return [ContA,ContB]
        else:
            pass
    i += 1
    ContA += 1
    return edad_a_aux(String,i,n,ContA,ContB)
