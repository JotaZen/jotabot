
def decimalToBinary(number: str) -> str:
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
   
   
def run(): 
    print(decimalToBinary('127'))  
    

if __name__ == '__main__':
    run()