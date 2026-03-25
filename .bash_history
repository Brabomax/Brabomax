pip install git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git
nano bot_iq.py
python3 bot_iq.py
> bot.py && nano bot.py
> bot.py      # esse sinal de > sozinho limpa o arquivo
nano bot.py   # abre o arquivo vazio no editor nano
python3 bot_iq.py
pip uninstall iqoptionapi
pip install git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git
python3 bot.py
> bot.py      # esse sinal de > sozinho limpa o arquivo
nano bot.py   # abre o arquivo vazio no editor nano
python3 bot.py
> bot.py      # esse sinal de > sozinho limpa o arquivo
nano bot.py   # abre o arquivo vazio no editor nano
python3 bot.py
> bot.py      # esse sinal de > sozinho limpa o arquivo
nano bot.py   # abre o arquivo vazio no editor nano
python3 bot.py
> bot.py      # esse sinal de > sozinho limpa o arquivo
nano bot.py   # abre o arquivo vazio no editor nano
python3 bot.py
pip show iqoptionapi
pip uninstall iqoptionapi -y
pip install iqoptionapi==6.6.9
pip install git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git@c0e4d2a
pip install git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git@master
python3 bot.py
> bot.py      # esse sinal de > sozinho limpa o arquivo
nano bot.py   # abre o arquivo vazio no editor nano
python3 bot.py
nano bot.py
python3 bot.py
> bot.py      # esse sinal de > sozinho limpa o arquivo
nano bot.py   # abre o arquivo vazio no editor nano
python3 bot.py
> bot.py      # esse sinal de > sozinho limpa o arquivo
nano bot.py   # abre o arquivo vazio no editor nano
python3 bot.py
> bot.py      # esse sinal de > sozinho limpa o arquivo
nano bot.py   # abre o arquivo vazio no editor nano
python3 bot.py
> bot.py      # esse sinal de > sozinho limpa o arquivo
nano bot.py   # abre o arquivo vazio no editor nano
python3 bot.py
> bot.py      # esse sinal de > sozinho limpa o arquivo
nano bot.py   # abre o arquivo vazio no editor nano
python3 bot.py
> bot.py      # esse sinal de > sozinho limpa o arquivo
nano bot.py   # abre o arquivo vazio no editor nano
ssh root@201.76.43.11
nano bot.py
> bot.py && nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
pip install telethon iqoptionapi requests websocket-client
python3 bot.py
rm session.session
python3 bot.py
nano bot.py
python3 bot.py
nano bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python bot.py
> bot.py && nano bot.py
python bot.py
> bot.py && nano bot.py
python bot.py
> bot.py && nano bot.py
python bot.py
root@vps64496:~# Loaded: loaded (/etc/systemd/system/bot3.service; enabled)
-bash: syntax error near unexpected token `('

ssh root@201.76.43.11
python3 bot.py
ssh root@201.76.43.11
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
tmux new -s botvip
nano bot.py
tmux attach
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
ssh root@201.76.43.11
python bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
pip install numpy
pip3 install numpy
pkg update && pkg upgrade
y
pkg update && pkg upgrade
pkg install python-numpy
python bot.py
python3 bot.py
pip install iqoptionapi
pip install websocket-client
pip install requests
pip install numpy
python3 bot.py
pip uninstall iqoptionapi
pip install git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git
python3 bot.py
nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
python bot.py
ssh root@201.76.43.11
> bot.py && nano bot.py
python3 bot.py
import re
import time
import threading
import asyncio
import pytz
import queue
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from iqoptionapi.stable_api import IQ_Option
# CONFIGURAÇÕES
API_ID = 36196547
API_HASH = "e679d02988ac881917672f5f713bcf01"
EMAIL_IQ = "btdoistt@gmail.com"
SENHA_IQ = "Lorena09"
BR = pytz.timezone('America/Sao_Paulo')
iq = IQ_Option(EMAIL_IQ, SENHA_IQ)
client = TelegramClient('sessao_pirai_v18', API_ID, API_HASH)
sinais_ativos = set()
fila_mensagens = queue.Queue()
# envia resultado para fila
def enviar_resultado(chat_id, texto):
# loop de envio
async def vigia_fila():
# espera vela fechar
def esperar_ate_segundo_59(horario_entrada, minuto):
# verifica resultado
def verificar_na_iq(par_raw, direcao, horario_entrada, chat_id):
# captura sinais
@client.on(events.NewMessage)
async def handler(event):
# inicia bot
async def main():
asyncio.run(main())import re
import time
import threading
import asyncio
import pytz
import queue
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from iqoptionapi.stable_api import IQ_Option
# CONFIGURAÇÕES
API_ID = 36196547
API_HASH = "e679d02988ac881917672f5f713bcf01"
EMAIL_IQ = "btdoistt@gmail.com"
SENHA_IQ = "Lorena09"
BR = pytz.timezone('America/Sao_Paulo')
iq = IQ_Option(EMAIL_IQ, SENHA_IQ)
client = TelegramClient('sessao_pirai_v18', API_ID, API_HASH)
sinais_ativos = set()
fila_mensagens = queue.Queue()
# envia resultado para fila
def enviar_resultado(chat_id, texto):
# loop de envio
async def vigia_fila():
# espera vela fechar
def esperar_ate_segundo_59(horario_entrada, minuto):
# verifica resultado
def verificar_na_iq(par_raw, direcao, horario_entrada, chat_id):
# captura sinais
@client.on(events.NewMessage)
async def handler(event):
# inicia bot
async def main():
> bot.py && nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
pip uninstall iqoptionapi
pip install git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git
> bot.py && nano bot.py
python3 bot.py
pip uninstall iqoptionapi
pip install git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git
> bot.py && nano bot.py
python3 bot.py
pip uninstall iqoptionapi
pip install git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
pip uninstall iqoptionapi
pip install git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git
pip uninstall iqoptionapi
pip install git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git
pip uninstall iqoptionapi
pip install git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git
pip uninstall iqoptionapi
pip install git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git
pkg install git -y
git clone https://github.com/Lu-Yi-Hsun/iqoptionapi.git
cd iqoptionapi
python3 -m pip install .
> bot.py && nano bot.py
python3 bot.py
pip uninstall iqoptionapi -y
cd ~/iqoptionapi        # pasta que você clonou do GitHub
python3 -m pip install .
2pip uninstall iqoptionapi -y
cd ~/iqoptionapi
python3 -m pip install .
cd ~/iqoptionapi
python3 -m pip install .
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
rm -rf sessao_pirai_v18.session
python3 bot.py
rm -rf sessao_pirai_v18.session
python3 bot.py
python bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
> bot.py && nano bot.py
python bot.py
> bot.py && nano bot.py
python bot.py
> bot.py && nano bot.py
python bot.py
nano bot.py
python bot.py
nano bot.py
python bot.py
> bot.py && nano bot.py
python bot.py
> bot.py && nano bot.py
python bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
> bot.py && nano bot.py
pip uninstall iqoptionapi -y
pip install iqoptionapi
nano bot.py
python3 bot.py
pip install iqoptionapi
pip install git+https://github.com/Lu-Yi-Hsun/iqoptionapi.git
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
# Instalar apenas requests
pip install requests
# Executar
python3 bot.py
# Instalar apenas requests
pip install requests
# Executar
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
ssh root@201.76.43.11
> bot.py && nano bot.py
python3 bot.py
pkg update
pkg upgrade
pkg install python
pip install websocket-client
pip install requests
pip install asyncio
nano deriv_bot.py
python deriv_bot.py
nano deriv_bot.py
python deriv_bot.py
nano deriv_bot.py
python deriv_bot.py
nano deriv_bot.py
python deriv_bot.py
python3 bot.py
pip install deriv-api
pip install python-deriv-api websockets
pip install websockets requests
nano deriv_bot.py
,> deriv_bot.py
nano deriv_bot.py
python deriv_bot.py
> deriv_bot.py
nano deriv_bot.py
python deriv_bot.py
pip install -U pip
pip install python-deriv-api websockets requests
> deriv_bot.py
nano deriv_bot.py
python deriv_bot.py
nano deriv_bot.py
python deriv_bot.py
nano deriv_bot.py
> deriv_bot.py
nano deriv_bot.py
python deriv_bot.py
> deriv_bot.py
nano deriv_bot.py
python deriv_bot.py
rm deriv_bot.py
nano deriv_bot.py
python deriv_bot.py
rm deriv_bot.py
nano deriv_bot.py
python deriv_bot.py
python3 bot.py
nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
> bot.py && nano bot.py
nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
nano bot.py
python3 bot.py
> bot.py && nano bot.py
python3 bot.py
ssh root@201.76.43.11
nano bot.py
python deriv_bot.py
python3 bot.py
ssh root@201.76.43.11
python3 bot.py
ssh root@201.76.43.11
python3 bot.py
ssh root@201.76.43.11
python3 bot.py
ssh root@201.76.43.11
> bot.py && nano bot.py
python bot.py
ssh root@201.76.43.11
> bot.py && nano bot.py
python bot.py
python seu_bot.py
python bot.py
vncserver :1
python bot.py
vncserver :1
python bot.py
lt --port 5000 --subdomain pirai-v26 --open false
pkg install cloudflared -y
python bot_web.py
nano bot_web.py
python bot_web.py
nano bot_web.py
python bot_web.py
nano bot_web.py
python bot_web.py
nano bot_web.py
python bot_web.py
nano bot_web.py
python bot_web.py
cloudflared tunnel --url http://127.0.0.1:5000
nano bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
python bot_socio3.py
> bot_socio3.py
nano bot_socio3.py
> bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
python bot_socio3.py
rm session_*.sqlite
python bot_socio3.py
nano bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
> bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
python bot_socio3.py
nano bot_socio3.py
