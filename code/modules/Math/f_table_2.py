import math
from math import log


""" TABLA DE FRECUENCIAS
INTERVAL -PT MEDIO -FREC ABSOL -FREC ABS ACUMU -RELATIVA -RELATIVA ACUMU"""

DATA = [1.4,4.4,9,8,7,10,21,12,35,32.1,17,6,10,22,25,
        5,9.4,8,7,10,11,12.2,35,32,17,6,10,22,25,
    ]

DECIMALES = 0
DATA = list(map(lambda x: round(x,DECIMALES) ,DATA))

# 1
NUM_DATOS = len(DATA)
DATA_MIN = min(DATA)
DATA_MAX = max(DATA)

RANGO = DATA_MAX - DATA_MIN


# 2
INTERVALOS = 1 + ((10/3)*log(NUM_DATOS))
if int(INTERVALOS) % 2 == 0:
    INTERVALOS +=1
INTERVALOS = int(INTERVALOS)


# 3
AMPLITUD = RANGO / INTERVALOS
AMPLITUD = round(AMPLITUD, 0)


#4


#5
PRIMER_LIM_INFERIOR = round(DATA_MIN)
LIMITES_INFERIORES = [PRIMER_LIM_INFERIOR]

#6
for i in range(INTERVALOS-1):
    LIM = round(LIMITES_INFERIORES[i] + AMPLITUD, DECIMALES)
    LIMITES_INFERIORES.append(LIM)

#7 
PRIMER_LIM_SUPERIOR = LIMITES_INFERIORES[1]
LIMITES_SUPERIORES = [PRIMER_LIM_SUPERIOR]

#8
for i in range(INTERVALOS-1):
    LIM = round(LIMITES_SUPERIORES[i] + AMPLITUD, DECIMALES)
    LIMITES_SUPERIORES.append(LIM)  

LIMITES = [(i,j) for i,j in zip(LIMITES_INFERIORES,LIMITES_SUPERIORES)]

#9
TABLA_FRECUENCIA = [[i,j,0,0] for i,j in LIMITES]


for d in DATA:
    for i in TABLA_FRECUENCIA:
        if i[0] <= d <= i[1]:
            i[2] += 1

TABLA_FRECUENCIA[0][3] = TABLA_FRECUENCIA[0][2]
FREC_ACUM = TABLA_FRECUENCIA[0][3]    
      
for t in TABLA_FRECUENCIA[1:]:
    FREC_ACUM += t[2]
    t[3] = FREC_ACUM


print()
print(f"DATA = {DATA}")
print()
print('INTERVALOS     - FREC ABS - FREC ACUM') 
for t in TABLA_FRECUENCIA:
    inter = f'[{t[0]} - {t[1]}['
    print( inter + f'-  {t[2]}       -  {t[3]}'.rjust(36-len(inter)," "))
