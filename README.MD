# Получение баланса через USSD запрос GSM шлюз GOIP 

```python
import requests
from goip_ussd import Goip_ussd

#Telegram bot token 
tg_bot_key = '6116365148:SdIma4ecXa0sPmVet3jnPDGkyB7AAGF7M0S'

#Telegram user id 
chat_id ='222218556'

goip = Goip_ussd(
    goip_url='http://192.168.1.254',
    goip_login="admin",
    goip_passw="admin",
    goip_ussd="*100#",
    lines_count=8
    )
#Получаем smskey    
goip.get_smskey()

#Отправляем запрос
goip.send_ussd()

#Получаем ответ
balance = goip.get_response()

#Закрываем USSD соединения 
goip.close_ussd()

msg = ""
for i  in balance:
    msg+="Линия {}: {}.\n".format(i, balance[i])

#Отправляем в Telegram
requests.get('https://api.telegram.org/bot'+tg_bot_key+'/sendMessage?chat_id='+chat_id+'&text='+msg)
```



