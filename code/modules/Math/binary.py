def decimalToBinary(number:str) -> str:
    try: 
        number = int(number)
    except:
        return
    
    if number == 0:
        return '0'
    elif number == 1:
        return '1'
     
    binary = ""   
    
    while number >= 1:
        binary += str(number % 2)
        
        number //= 2
    
    return binary[::-1]

def binaryToDecimal(binary:str) -> str:
    cont = 0
    dec_number = 0

    for i in range(len(binary)-1, -1, -1):
        if not binary[cont] in ['0', '1']:
            return 'Nan'
        dec_number += int(binary[cont]) * 2**(i)
        cont += 1
    return dec_number
   
def run(): 
    print(binaryToDecimal('11111111'))  
    

if __name__ == '__main__':
    run()