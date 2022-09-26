import math
from math import log, sqrt

def tablaFrecuencia(DATA, DECIMALES=0,INTERVALOS=None):
    """ TABLA DE FRECUENCIAS
    INTERVAL -PT MEDIO -FREC ABSOL -FREC ABS ACUMU -RELATIVA -RELATIVA ACUMU"""
    
    try:
        DATA = list(map(lambda x: round(float(x),DECIMALES) ,DATA))
    except:
        return 'La lista debe contener solo numeros'
 
    # 1
    NUM_DATOS = len(DATA)
    DATA_MIN = min(DATA)
    DATA_MAX = max(DATA)
    RANGO = round(DATA_MAX - DATA_MIN, DECIMALES)
    PRECISION = round(10**(-1 *DECIMALES), DECIMALES) 
    DATA.sort()
    MEDIANA = DATA[int(round(NUM_DATOS/2))]

    #2
    if INTERVALOS is None:
        INTERVALOS = 1 + (math.log(NUM_DATOS, 10)*3.3)      
    INTERVALOS = int(round(INTERVALOS,DECIMALES))     

    # 3
    AMPLITUD = RANGO / INTERVALOS
    AMPLITUD = round(AMPLITUD, DECIMALES)

    #4
    EXCEDENTE = (INTERVALOS*AMPLITUD)-RANGO-PRECISION
    if EXCEDENTE < 0:
        AMPLITUD += PRECISION
        EXCEDENTE = (INTERVALOS*AMPLITUD)-RANGO-PRECISION
    EXCEDENTE = round(EXCEDENTE, DECIMALES)

    TDF = {}
    TDF["num_de_datos"] = len(DATA)
    TDF["minimo"] = min(DATA)
    TDF["maximo"] = max(DATA)
    TDF["rango"] = round(DATA_MAX - DATA_MIN, DECIMALES)
    TDF["precision"] = round(10**(-1 *DECIMALES), DECIMALES)
    TDF["mediana"] = DATA[int(round(NUM_DATOS/2))]
    TDF["intervalos"] = int(round(INTERVALOS,DECIMALES))   
    TDF["amplitud"] = round(AMPLITUD, DECIMALES)
    TDF["excedente"] = round(EXCEDENTE, DECIMALES)


    #5
    PRIMER_LIM_INFERIOR = round(DATA_MIN - (EXCEDENTE/2), DECIMALES)
    LIMITES_INFERIORES = [PRIMER_LIM_INFERIOR]

    #6
    for i in range(INTERVALOS-1):
        LIM = round(LIMITES_INFERIORES[i] + AMPLITUD, DECIMALES)
        LIMITES_INFERIORES.append(LIM)

    #7 
    PRIMER_LIM_SUPERIOR = round(LIMITES_INFERIORES[1] - PRECISION, DECIMALES)
    LIMITES_SUPERIORES = [PRIMER_LIM_SUPERIOR]

    #8
    for i in range(INTERVALOS-1):
        LIM = round(LIMITES_SUPERIORES[i] + AMPLITUD, DECIMALES)
        LIMITES_SUPERIORES.append(LIM)  

    LIMITES = [(i,j) for i,j in zip(LIMITES_INFERIORES,LIMITES_SUPERIORES)]
    
    TABLA_FRECUENCIA = [[i,j,0,0,0,0,0] for i,j in LIMITES]
        
    # FRECUENCIA ABSOLUTA
    PROMEDIO = 0
    MODA = {
        "moda":[DATA[0]],
        "frecuencia": DATA.count(DATA[0])
    }
    
    for d in DATA:
        
        if DATA.count(d) > MODA["frecuencia"]:
            MODA["moda"] = [d]
            MODA["frecuencia"] = DATA.count(d)
            
        elif DATA.count(d) == MODA["frecuencia"] and d not in MODA["moda"]:
            MODA["moda"].append(d)
            
        PROMEDIO += d
        for i in TABLA_FRECUENCIA:
            if i[0] <= d <= i[1]:
                i[2] += 1
    PROMEDIO = round(PROMEDIO/NUM_DATOS, DECIMALES)
    
    TABLA = {
        "amplitud": AMPLITUD,
        "intervalos": INTERVALOS,
        "precision": PRECISION,
        "excendente": EXCEDENTE,
        "minimo": DATA_MIN,
        "maximo": DATA_MAX,
        "mediana": MEDIANA,
        "promedio": PROMEDIO,
        "moda": MODA,
        "filas": [            
            {
                "limite_inferior": 1,
                "limite_superior": 1,
                "marca_clase" : 1,
                "frecuencia_absoluta": 1,
                "frecuencia_acumulada": 1,
                "frecuencia_relativa": 1,
                "relativa_acumulada": 1,
                "datos": []           
                
            }]
        
    }
    #9 [limInf,Limsup,FrecAbs,FrecAcum,FrecRel,FrecRelAcum]

    # ACUMULADA 
    TABLA_FRECUENCIA[0][3] = TABLA_FRECUENCIA[0][2]
    FREC_ACUM = TABLA_FRECUENCIA[0][3]       
    for t in TABLA_FRECUENCIA[1:]:
        FREC_ACUM += t[2]
        t[3] = FREC_ACUM

    # RELATIVA
    for t in TABLA_FRECUENCIA:
        FREC_RELATIVA = t[2] / NUM_DATOS
        t[4] = round(FREC_RELATIVA, 2)

    # RELATIVA ACUMULADA
    TABLA_FRECUENCIA[0][5] = TABLA_FRECUENCIA[0][4]
    FREC_R_ACUM = TABLA_FRECUENCIA[0][5] 
    for t in TABLA_FRECUENCIA[1:]:
        FREC_R_ACUM += t[4]
        t[5] = round(FREC_R_ACUM, 2)

    # MARCA CLASE
    for t in TABLA_FRECUENCIA:
        MARCA_CLASE = (t[0] + t[1])/2
        t[6] = round(MARCA_CLASE, DECIMALES)

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
    DATA = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,9,8,7,10,21,12,32,17,6,10,22,25,
        5,9,8,7,10,11,12,35,32,17,6,36,10,22,25,
] +[1.4,4,9,8,7,10,21,12,35.4,32,17,6,10,22,25,
        5,9,8,7,10,11,9,12,26,32,17,23,36,10,22,25,
]   
    DATA = [i for i in range(1,25) ] + [5,6]
    print(tablaFrecuencia(DATA))
