import requests
import lxml.html as html
import datetime as dt

HOME_URL = 'https://www.clarin.com/horoscopo/' 

XPATH_SYMBOL = '//div[@class="row OpeningPostNormal"]//h2/span/text()'
XPATH_HOROSCOPE = '//div[@class="description"]/node()//text()'

def symbol(symbol):
    
    symbols_page = ['Aries','Tauro','Géminis','Cáncer','Leo','Virgo','Libra','Escorpio','Sagitario','Capricornio','Acuario','Piscis'] 

    if symbol in symbols_page:
        return symbol
    
    for i in symbols_page:
        if symbol == i.lower() or symbol == i.replace('é','e').replace('á','a') or symbol == i.replace('é','e').replace('á','a').lower():
            return i
    else: 
        return ""

def parseHome(horoscope_symbol):
    try:
        response = requests.get(HOME_URL)
        
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            
            XPATH_H = f'//div[@id="data-{symbol(horoscope_symbol)}"]/node()//text()'
            
            horoscope = parsed.xpath(XPATH_H) 
            data = {
                'day': dt.date.today().strftime('%d-%m-%Y'), 
                'horoscope':horoscope
                    }
           
            return data    

        else:
            raise ValueError(f'Error: {response.status_code}')
        
    except ValueError as ve:
        print(ve)


def run():
    while True:
        t = input("Signo Zodiacal: ")
        horoscope = parseHome(t)
        text = "\n".join(horoscope["horoscope"])
        print()
        print(f'Hoy {horoscope["day"]}, {symbol(t)}:')
        print()
        print(text)
        print()     
    
if __name__ == '__main__':
    run()











