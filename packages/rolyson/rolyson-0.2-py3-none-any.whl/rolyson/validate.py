def __OnlyNumber(value):
    if value is None:
        return None
        
    return ''.join(i for i in value if i.isdigit())

def __AllRepeated(_value):
    if (_value != '') and (len(_value) > 1):
        for i in range(2,len(_value)):
            if _value[i] != _value[i-1]:
                return False

    return True

def __GeneratesDigit(soma):
    numero = 11 - (soma % 11)
    if numero > 9:
        numero = 0

    return numero

def __getSum(posicao, inscricao, validPeso10=False):
    peso = 2
    soma = 0

    for i in range(posicao, 0, -1):
        soma = soma + peso * int(inscricao[i-1:i])
        peso = peso + 1
        if validPeso10:
            if peso == 10:
                peso = 2

    return soma

def validateCPF(value):
    inscricao = __OnlyNumber(value)

    if not inscricao:
        return False
        
    if (len(inscricao) == 11) and (not (__AllRepeated(inscricao))):
        pDV        = inscricao[-2:len(inscricao)]
        inscricao = inscricao[0:-2]

        Soma = __getSum(9, inscricao)
        inscricao = inscricao + str(__GeneratesDigit(Soma))

        Soma = __getSum(10, inscricao)
        inscricao = inscricao + str(__GeneratesDigit(Soma))

        return inscricao[-2:len(inscricao)] == pDV
        
    return False

def validateCNPJ(value):
    inscricao = __OnlyNumber(value)

    if not inscricao:
        return False

    if (len(inscricao) == 14) and (not (__AllRepeated(inscricao))):
        pDV        = inscricao[-2:len(inscricao)]
        inscricao = inscricao[0:-2]

        Soma = __getSum(12, inscricao, True)
        inscricao = inscricao + str(__GeneratesDigit(Soma))

        Soma = __getSum(13, inscricao, True)
        inscricao = inscricao + str(__GeneratesDigit(Soma))

        return inscricao[-2:len(inscricao)] == pDV
        
    return False   
