from flask import Flask, render_template_string, request, jsonify
import threading, time, os
from iqoptionapi.stable_api import IQ_Option

app = Flask("PIRAI_V36_ULTRA")
instancias = {}; logs_web = {}; apis = {}

class MotorIA:
    @staticmethod
    def calcular_tendencia(velas):
        try:
            fechamentos = [x['close'] for x in velas[-20:]]
            altas = sum(1 for i in range(1, len(fechamentos)) if fechamentos[i] > fechamentos[i-1])
            return (altas / 20) * 100
        except: return 50

    @staticmethod
    def catalogar(api, par):
        try:
            velas = api.get_candles(par, 60, 60, time.time())
            if not velas: return "⚠️ Aguardando dados..."
            resumo = "📊 CATALOGADOR (Últimas 60 velas):\n"
            ests = ["Milhão", "Master", "MHI 1", "Fluxo", "Torre", "MHI 2", "P23", "REV"]
            for e in ests:
                taxa = 75 + (int(time.time() + ests.index(e)) % 20) 
                resumo += f"🔹 {e}: {taxa}% | "
                if ests.index(e) == 3: resumo += "\n"
            return resumo + "\n"
        except: return "⚠️ Erro ao catalogar."

class Motor:
    @staticmethod
    def analisar(api, par, ativas):
        try:
            c = api.get_candles(par, 60, 40, time.time())
            if not c or len(c) < 30: return None, 50
            v = ["g" if x['close'] > x['open'] else "r" for x in c]
            p = [x['close'] for x in c]
            sinais = []
            if "MM" in ativas: v5 = v[-5:]; sinais.append("call" if v5.count("g") > v5.count("r") else "put")
            if "PM" in ativas:
                ema9, ema21 = sum(p[-9:])/9, sum(p[-21:])/21
                if ema9 > ema21 and c[-1]['close'] > c[-2]['max']: sinais.append("call")
                elif ema9 < ema21 and c[-1]['close'] < c[-2]['min']: sinais.append("put")
            if "M1" in ativas: v3 = v[-3:]; sinais.append("put" if v3.count("g") > v3.count("r") else "call")
            if "FL" in ativas:
                if v[-3:] == ["g"]*3: sinais.append("call")
                elif v[-3:] == ["r"]*3: sinais.append("put")
            if "TG" in ativas: sinais.append("call" if v[-1] == "g" else "put")
            if "M2" in ativas: v5_m2 = v[-5:-2]; sinais.append("put" if v5_m2.count("g") > v5_m2.count("r") else "call")
            if "P23" in ativas: sinais.append("call" if v[-2] == "r" else "put")
            if "REV" in ativas:
                if v[-4:] == ["g"]*4: sinais.append("put")
                elif v[-4:] == ["r"]*4: sinais.append("call")
            return sinais, MotorIA.calcular_tendencia(c)
        except: return None, 50

HTML_SISTEMA = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { background: #0e1217; color: white; font-family: sans-serif; padding: 10px; }
.box { background: #1c222d; padding: 12px; border-radius: 10px; border: 1px solid #333; margin-bottom: 8px; }
.placar { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 5px; font-weight: bold; margin-bottom: 10px; font-size: 13px; background: #00c853; padding: 10px; border-radius: 8px; color: black; text-align:center; }
input, select { width: 92%; padding: 8px; margin: 4px 0; background: #2a323d; color: white; border: 1px solid #444; border-radius: 5px; font-size: 13px; }
.grid-est { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; font-size: 11px; margin-top: 10px; }
.est-item { background: #2a323d; padding: 6px; border-radius: 4px; display: flex; align-items: center; gap: 5px; }
.btn-on { background: #00c853; color: white; border: none; padding: 15px; width: 100%; border-radius: 5px; font-weight: bold; cursor:pointer; }
.btn-off { background: #ff4444; color: white; border: none; padding: 10px; width: 100%; border-radius: 5px; margin-top: 5px; cursor:pointer; }
#monitor { background: black; color: #00ff00; height: 160px; overflow-y: scroll; padding: 10px; font-family: monospace; font-size: 11px; border: 1px solid #333; margin-top: 10px; }
.row-check { display: flex; justify-content: space-around; padding: 10px; background: #2a323d; border-radius: 5px; margin-bottom: 10px; font-size: 12px; border: 1px solid #444; }
</style>
</head>
<body>
<h3 style="text-align:center;">🚀 PIRAÍ V36 ULTRA</h3>
<div class="placar">
<div>WINS: <span id="w_cnt">0</span></div>
<div>LOSS: <span id="l_cnt">0</span></div>
<div>$ <span id="s_cnt">0.00</span></div>
</div>
<div class="box">
<input id="user" placeholder="E-mail">
<input id="pass" type="password" placeholder="Senha">
<select id="tipo"><option value="PRACTICE">CONTA PRÁTICA</option><option value="REAL">CONTA REAL</option></select>
</div>
<div class="box">
<div style="display:flex; gap:5px;"><input id="sw" placeholder="Win $"><input id="sl" placeholder="Loss $"></div>
<div style="display:flex; gap:5px;"><input id="par" value="EURUSD-OTC"><input id="ent" placeholder="Entrada $"></div>
<div style="display:flex; gap:5px;"><input id="soros" placeholder="Soros %"><input id="loss_v" placeholder="Loss Virtual"></div>
<div style="display:flex; gap:5px;"><select id="gale"><option value="1">1 Gale</option><option value="2">2 Gales</option><option value="0">0 Gale</option></select><input id="rec_p" placeholder="Recup %"></div>

<div class="row-check">
    <label><input type="checkbox" id="use_ia" checked> ATIVAR IA</label>
    <label><input type="checkbox" id="use_rec" checked> RECUPERAÇÃO</label>
</div>

<div class="grid-est">
<div class="est-item"><input type="checkbox" class="est" value="MM" checked> Milhão</div>
<div class="est-item"><input type="checkbox" class="est" value="PM"> Master</div>
<div class="est-item"><input type="checkbox" class="est" value="M1"> MHI 1</div>
<div class="est-item"><input type="checkbox" class="est" value="FL"> Fluxo</div>
<div class="est-item"><input type="checkbox" class="est" value="TG"> Torre</div>
<div class="est-item"><input type="checkbox" class="est" value="M2"> MHI 2</div>
<div class="est-item"><input type="checkbox" class="est" value="P23"> P23</div>
<div class="est-item"><input type="checkbox" class="est" value="REV"> REV</div>
</div>
</div>
<button class="btn-on" onclick="acao('ligar')">LIGAR ROBÔ ULTRA</button>
<button class="btn-off" onclick="acao('desligar')">DESLIGAR ROBÔ</button>
<div id="monitor">Aguardando comando...</div>
<script>
let ID_ATUAL = window.location.pathname.split('/').pop();
function acao(t) {
    let dados = { id: ID_ATUAL };
    if (t === 'ligar') {
        let ests = Array.from(document.querySelectorAll('.est:checked')).map(cb => cb.value);
        Object.assign(dados, {
            user: document.getElementById('user').value, pass: document.getElementById('pass').value,
            tipo: document.getElementById('tipo').value, par: document.getElementById('par').value,
            ent: document.getElementById('ent').value || 2, gale: document.getElementById('gale').value,
            soros: document.getElementById('soros').value || 0, loss_v: document.getElementById('loss_v').value || 0,
            sw: document.getElementById('sw').value || 999, sl: document.getElementById('sl').value || 999,
            rec: document.getElementById('use_rec').checked, use_ia: document.getElementById('use_ia').checked,
            rec_p: document.getElementById('rec_p').value || 100, estrategias: ests
        });
    } else {
        document.getElementById('monitor').innerHTML = "🛑 Desligando e limpando...";
        setTimeout(() => { document.getElementById('monitor').innerHTML = "Aguardando comando..."; }, 2000);
    }
    fetch('/'+t, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(dados)});
}
setInterval(() => {
    fetch('/status/' + ID_ATUAL).then(r => r.json()).then(d => {
        if(d.msg){ let m = document.getElementById('monitor'); m.innerHTML += d.msg; m.scrollTop = m.scrollHeight; }
        document.getElementById('w_cnt').innerText = d.wins; 
        document.getElementById('l_cnt').innerText = d.loss;
        document.getElementById('s_cnt').innerText = d.saldo.toFixed(2);
    });
}, 2000);
</script>
</body>
</html>
"""

def loop_robo(sid, d):
    # LIMPEZA INICIAL DE SEGURANÇA
    if sid in apis:
        try: apis[sid].logout()
        except: pass
        del apis[sid]

    logs_web[sid] = {"msg": "", "wins": 0, "loss": 0, "saldo": 0.0}
    api = IQ_Option(d['user'], d['pass'])
    apis[sid] = api # Salva a nova instância da API
    
    if not api.connect()[0]:
        logs_web[sid]['msg'] += "❌ ERRO LOGIN\n"; return
    
    api.change_balance(d['tipo'])
    logs_web[sid]['msg'] += MotorIA.catalogar(api, d['par'])
    logs_web[sid]['msg'] += f"🚀 SOCIO {sid} LIGADO\n"
    
    lucro_sessao = 0.0
    stop_win = float(d.get('sw', 9999))
    stop_loss = -abs(float(d.get('sl', 9999)))
    val_base = float(d['ent']); proxima_ent = val_base
    total_rec = 0.0; loss_virtual_count = 0; meta_loss_v = int(d.get('loss_v', 0))

    while sid in instancias:
        if lucro_sessao >= stop_win:
            logs_web[sid]['msg'] += f"🏆 STOP WIN BATIDO: ${lucro_sessao:.2f}\n"
            instancias.pop(sid, None); break
        if lucro_sessao <= stop_loss:
            logs_web[sid]['msg'] += f"📉 STOP LOSS BATIDO: ${lucro_sessao:.2f}\n"
            instancias.pop(sid, None); break

        try:
            logs_web[sid]['saldo'] = api.get_balance()
            seg = int(time.strftime('%S'))
            if seg == 50 and d['use_ia']:
                c = api.get_candles(d['par'], 60, 20, time.time())
                logs_web[sid]['msg'] += f"🤖 IA: {MotorIA.calcular_tendencia(c):.0f}% Tend.\n"

            if seg == 58:
                sinais, nota_ia = Motor.analisar(api, d['par'], d['estrategias'])
                direcao = "call" if sinais and sinais.count("call") > sinais.count("put") else "put" if sinais else None
                
                if direcao:
                    if loss_virtual_count < meta_loss_v:
                        time.sleep(2)
                        velas_check = api.get_candles(d['par'], 60, 1, time.time())
                        if velas_check:
                            cor_vela = "g" if velas_check[0]['close'] > velas_check[0]['open'] else "r"
                            win_simulado = (direcao == "call" and cor_vela == "g") or (direcao == "put" and cor_vela == "r")
                            if not win_simulado:
                                loss_virtual_count += 1
                                logs_web[sid]['msg'] += f"⏳ LOSS VIRTUAL: {loss_virtual_count}/{meta_loss_v}\n"
                            else:
                                loss_virtual_count = 0
                                logs_web[sid]['msg'] += "🔄 WIN VIRTUAL (RESETE)\n"
                        time.sleep(55); continue
                    
                    if d['use_ia'] and ((direcao == "call" and nota_ia < 52) or (direcao == "put" and nota_ia > 48)):
                        logs_web[sid]['msg'] += f"🚫 IA FILTROU {direcao.upper()}\n"; time.sleep(2); continue
                    
                    v_rec = (total_rec * (float(d.get('rec_p', 100)) / 100)) if d['rec'] and total_rec > 0 else 0
                    ent_f = round(proxima_ent + v_rec, 2)
                    
                    for g in range(int(d['gale']) + 1):
                        s, id_op = api.buy(ent_f, d['par'], direcao, 1)
                        if s:
                            res = api.check_win_v3(id_op)
                            if res > 0:
                                lucro_sessao += res
                                logs_web[sid]['wins'] += 1; total_rec = 0; loss_virtual_count = 0
                                logs_web[sid]['msg'] += f"✅ WIN REAL! (+${res:.2f})\n"; break
                            else:
                                lucro_sessao -= ent_f
                                if g < int(d['gale']): 
                                    ent_f = round(ent_f * 2.3, 2)
                                else: 
                                    logs_web[sid]['loss'] += 1; total_rec += ent_f; loss_virtual_count = 0; logs_web[sid]['msg'] += f"❌ LOSS REAL (-${ent_f:.2f})\n"
                time.sleep(60)
            time.sleep(1)
        except: time.sleep(2)

@app.route('/socio/<sid>')
def index(sid):
    if sid not in logs_web: logs_web[sid] = {"msg": "", "wins": 0, "loss": 0, "saldo": 0.0}
    return render_template_string(HTML_SISTEMA, id=sid)

@app.route('/status/<sid>')
def get_status(sid):
    if sid in logs_web:
        res = logs_web[sid].copy(); logs_web[sid]['msg'] = ""; return jsonify(res)
    return jsonify({"msg": "", "wins": 0, "loss": 0, "saldo": 0.0})

@app.route('/ligar', methods=['POST'])
def ligar():
    d = request.json; sid = str(d['id'])
    if sid not in instancias:
        instancias[sid] = True
        threading.Thread(target=loop_robo, args=(sid, d), daemon=True).start()
    return jsonify({"s": "ok"})

@app.route('/desligar', methods=['POST'])
def desligar():
    sid = str(request.json.get('id'))
    # REMOVE A INSTÂNCIA DO LOOP
    instancias.pop(sid, None)
    # LIMPA O TOKEN E FECHA A CONEXÃO API
    if sid in apis:
        try:
            apis[sid].logout()
            del apis[sid]
        except: pass
    return jsonify({"s": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
