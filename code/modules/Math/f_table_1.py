import math
from math import log, sqrt
from unicodedata import name

def tablaFrecuencia(DATA):
    """ TABLA DE FRECUENCIAS
    INTERVAL -PT MEDIO -FREC ABSOL -FREC ABS ACUMU -RELATIVA -RELATIVA ACUMU"""
    DECIMALES = 2
    
    try:
        for i in range(len(DATA)):
            DATA[i]=int(DATA[i])
    except:
        return '...'

    
    #DATA = list(map(lambda x: round(x,DECIMALES) ,DATA))

    # 1
    NUM_DATOS = len(DATA)
    DATA_MIN = min(DATA)
    DATA_MAX = max(DATA)

    RANGO = DATA_MAX - DATA_MIN
    PRECISION = 10**(-1 *DECIMALES) 
    DATA.sort()
    MEDIANA = DATA[int(round(NUM_DATOS/2, 0))]


    # 2
    #INTERVALOS = 1 + ((10/3)*log(NUM_DATOS))
    INTERVALOS = sqrt(NUM_DATOS)
    INTERVALOS = int(round(INTERVALOS,0))


    # 3
    AMPLITUD = RANGO / INTERVALOS
    AMPLITUD = round(AMPLITUD, DECIMALES)


    #4
    EXCEDENTE = (INTERVALOS*AMPLITUD)-RANGO-PRECISION
    if EXCEDENTE < 0:
        AMPLITUD += PRECISION
        EXCEDENTE = (INTERVALOS*AMPLITUD)-RANGO-PRECISION
    EXCEDENTE = round(EXCEDENTE, DECIMALES)


    #5
    PRIMER_LIM_INFERIOR = round(DATA_MIN - (EXCEDENTE/2), DECIMALES)
    #PRIMER_LIM_INFERIOR = round(DATA_MIN, DECIMALES)
    LIMITES_INFERIORES = [PRIMER_LIM_INFERIOR]


    #6
    for i in range(INTERVALOS-1):
        LIM = round(LIMITES_INFERIORES[i] + AMPLITUD, DECIMALES)
        LIMITES_INFERIORES.append(LIM)


    #7 
    PRIMER_LIM_SUPERIOR = LIMITES_INFERIORES[1] - PRECISION
    LIMITES_SUPERIORES = [PRIMER_LIM_SUPERIOR]

    #8
    for i in range(INTERVALOS-1):
        LIM = round(LIMITES_SUPERIORES[i] + AMPLITUD, DECIMALES)
        LIMITES_SUPERIORES.append(LIM)  

    LIMITES = [(i,j) for i,j in zip(LIMITES_INFERIORES,LIMITES_SUPERIORES)]

    #9 [limInf,Limsup,FrecAbs,FrecAcum,FrecRel,FrecRelAcum]
    TABLA_FRECUENCIA = [[i,j,0,0,0,0,0] for i,j in LIMITES]

    # FRECUENCIA ABSOLUTA
    PROMEDIO = 0
    for d in DATA:
        PROMEDIO += d
        for i in TABLA_FRECUENCIA:
            if i[0] <= d <= i[1]:
                i[2] += 1
    PROMEDIO = round(PROMEDIO/NUM_DATOS, DECIMALES)

    # ACUMULADA 
    TABLA_FRECUENCIA[0][3] = TABLA_FRECUENCIA[0][2]
    FREC_ACUM = TABLA_FRECUENCIA[0][3]       
    for t in TABLA_FRECUENCIA[1:]:
        FREC_ACUM += t[2]
        t[3] = FREC_ACUM

    # RELATIVA
    for t in TABLA_FRECUENCIA:
        FREC_RELATIVA = t[2] / NUM_DATOS
        t[4] = round(FREC_RELATIVA, DECIMALES)

    # RELATIVA ACUMULADA
    TABLA_FRECUENCIA[0][5] = TABLA_FRECUENCIA[0][4]
    FREC_R_ACUM = TABLA_FRECUENCIA[0][5] 
    for t in TABLA_FRECUENCIA[1:]:
        FREC_R_ACUM += t[4]
        t[5] = round(FREC_R_ACUM, DECIMALES)

    # MARCA CLASE
    for t in TABLA_FRECUENCIA:
        MARCA_CLASE = (t[0] + t[1])/2
        t[6] = round(MARCA_CLASE, DECIMALES)


    # print()
    # print(f"DATA = {DATA} - {NUM_DATOS}")
    # print()
    # print('INTERVALOS       - M CLASE  - FREC AB  - FREC ACU - FREC REL - FR ACU') 
    # for t in TABLA_FRECUENCIA:
    #     inter = f'[{t[0]}' + ' - ' + f'{t[1]}'+ '['
    #     print(inter.ljust(17, " "), end="") 
    #     print(f'- {t[6]}'.ljust(11," "), end="")
    #     print(f'- {t[2]}'.ljust(11," "), end="")
    #     print(f'- {t[3]}'.ljust(11," "), end="")
    #     print(f'- {t[4]}'.ljust(11," "), end="")
    #     print(f'- {t[5]}'.ljust(11," "))
    # print()
    # print(f'PROMEDIO: {PROMEDIO}')
    # print(f'MEDIANA: {MEDIANA}')

    tabla = ('`INTERVALOS       - M CLASE  - FREC AB  - FREC ACU - FREC REL - FR ACU\n')
    for t in TABLA_FRECUENCIA:
        inter = f'[{t[0]}' + ' - ' + f'{t[1]}'+ '['
        tabla += inter.ljust(17, " ")
        tabla += f'- {t[6]}'.ljust(11," ")
        tabla += f'- {t[2]}'.ljust(11," ")
        tabla += f'- {t[3]}'.ljust(11," ")
        tabla += f'- {t[4]}'.ljust(11," ")
        tabla += f'- {t[5]}'.ljust(11," ") + '\n'
    tabla += '`'
    
    return tabla

    
if __name__ == '__main__':
    DATA = [1.4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,9,8,7,10,21,12,35.4,32,17,6,10,22,25,
        5,9,8,7,10,11,12,35,32,17,6,36,10,22,25,
] +[1.4,4,9,8,7,10,21,12,35.4,32,17,6,10,22,25,
        5,9,8,7,10,11,9,12,26,32,17,23,36,10,22,25,
]   
    print(tablaFrecuencia(DATA))
