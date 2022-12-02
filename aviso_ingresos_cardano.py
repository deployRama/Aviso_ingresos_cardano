import os
import json
from time import sleep
import pandas as pd
import requests
from pathlib import Path
import datetime

bot_token = '' #Aqui hay que poner el bot_token que nos da Telegram
chat_id # =  Aqui va el chat_id del grupo de telegram, hay que darle privilegios de admin al bot

def telegram_bot_sendtext(bot_message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' \
                + str(chat_id) + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


class wallet():
    nombre = None
    address = None
    b_anterior = None
    b_actual = None
    


path = str(Path.cwd()) + "/wallets.xlsx" #Aqui se puede modificar el path y el nombre del archivo donde se encuentran las wallets a chequear
data = pd.read_excel(path)

x = 0

while x <= data.__len__()-1:
    globals()["wallet"+str(x)] = wallet()
    x +=1
x = 0
l = 0
a = 0

print("Entramos al loop de toma de datos iniciales\n")

while l <= data.__len__()-1:
    try:
            (globals()["wallet"+str(x)]).nombre = data.iloc[l,0]
            (globals()["wallet"+str(x)]).address = data.iloc[l,1]
            consulta = os.popen("curl https://pool.pm/wallet/"+(globals()["wallet"+str(x)]).address).read()
            (globals()["wallet"+str(x)]).b_anterior = round(json.loads(consulta)["lovelaces"]/1000000,2)
            print("\nYa tomamos el dato del balance de la wallet",(globals()["wallet"+str(x)]).nombre)
            print("\nDormimos 5 segundos y seguimos consultando")
            sleep(5)
            l +=1
            x +=1
            
    except KeyboardInterrupt:
                exit()
    except Exception as e:
            sleep(5)
            a +=1
            l +=1
            x +=1
            print(e)
            print("Fallo al tomar datos de balance inicial de", (globals()["wallet"+str(x)]).nombre )
            if a >= 50:
                telegram_bot_sendtext("Chequear loop de errores en bot de consulta wallet cardano error en wallet")
                a = 0
            else:
                pass
            continue
        
print("\nEntramos al loop de comparacion de balances")

while True:

    try:
        x = 0
        
        while x <= data.__len__()-1:
            try:
                print("\nProcedemos a tomar el dato del balance actual de la wallet",(globals()["wallet"+str(x)]).nombre,"\n")
                consulta = os.popen("curl https://pool.pm/wallet/"+(globals()["wallet"+str(x)]).address).read()
                (globals()["wallet"+str(x)]).b_actual = round(json.loads(consulta)["lovelaces"]/1000000,2)
                if (globals()["wallet"+str(x)]).b_actual > (globals()["wallet"+str(x)]).b_anterior:
                    diferencia = round((globals()["wallet"+str(x)]).b_actual - (globals()["wallet"+str(x)]).b_anterior,2)
                    telegram_bot_sendtext("Hubo un ingreso de " + str(diferencia)+ " adas en la wallet " + str((globals()["wallet"+str(x)]).nombre))
                    (globals()["wallet"+str(x)]).b_anterior = (globals()["wallet"+str(x)]).b_actual
                else:
                    (globals()["wallet"+str(x)]).b_anterior = (globals()["wallet"+str(x)]).b_actual
                x +=1
                print("\nDormimos 5 segundos y seguimos consultando\n")
                sleep(5)
                
            except KeyboardInterrupt:
                exit()    
                
            except Exception as e:
                print(e)
                print("Fallo en la comprobacion de los balances actuales")
                print("Dormimos 5 segundos y seguimos consultando")
                sleep(5)
                x +=1
                continue
            
        print(f"La hora actual es {datetime.datetime.today()}\n")
        print("Dormiremos 60 minutos\n")
        print(f"Reanudaremos la consulta a las {datetime.datetime.today()+datetime.timedelta(hours=1)}\n")
        sleep(3600)
    
    except KeyboardInterrupt:
            exit()
        
    except Exception as e:
        print(e)
        print("Fallo en la comprobacion de los balances actuales")
        print("Dormimos 5 segundos y seguimos consultando")
        sleep(5)
        continue
