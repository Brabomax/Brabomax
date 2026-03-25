# ============================================
# MARCA D'AGUA DE AUTORIA
# Autor original: Antonio Flávio
# Assinatura: ANTONIO_FLAVIO_WATERMARK_V1
# ============================================
#
# Recorte do fluxo de entradas e resultados extraido de bot_sinais.py
# Inclui: operar, checagem de resultado, martingale, processamento WIN/LOSS e envio para canais

def checar_resultado_oficial(id_ordem, par, timeframe_min=15):
    # 🚀 VERIFICAÇÃO ULTRA-RÁPIDA - Sem logs desnecessários
    if config.get('timing_verificacao_imediata', False):
        # Modo ultra-rápido: verificação instantânea sem logs
        pass
    else:
        log(f"[{par}] Verificando resultado da operação...", "INFO")

    # 🚨 CORREÇÃO: Calcula timeout inteligente baseado no timeframe e tempo restante da vela
    from datetime import datetime, timedelta
    agora = obter_hora_brasilia()

    # Validação do timeframe (mínimo 1, máximo 60 minutos)
    timeframe_min = max(1, min(timeframe_min, 60))

    # Calcular quando a vela vai fechar com base no horário da operação
    # A vela começa no início do quadrante do timeframe
    minuto_atual = agora.minute

    # 🚨 CORREÇÃO: Calcular o início da vela com base no timeframe
    if timeframe_min == 5:
        # M5: O quadrante começa no múltiplo de 5 minutos mais próximo
        minuto_inicio_vela = (minuto_atual // 5) * 5
    elif timeframe_min == 15:
        # M15: O quadrante começa no múltiplo de 15 minutos mais próximo
        minuto_inicio_vela = (minuto_atual // 15) * 15
    else:
        # Para outros timeframes, usar o cálculo padrão
        minuto_inicio_vela = (minuto_atual // timeframe_min) * timeframe_min

    # O fim da vela é o início mais o timeframe
    minuto_fim_vela = minuto_inicio_vela + timeframe_min

    if minuto_fim_vela >= 60:
        minuto_fim_vela = minuto_fim_vela - 60
        hora_fim = agora.hour + 1
        if hora_fim >= 24:
            hora_fim = 0
    else:
        hora_fim = agora.hour

    # Tempo quando a vela atual termina
    fim_vela = agora.replace(hour=hora_fim, minute=minuto_fim_vela, second=0, microsecond=0)

    # Se a vela termina no dia seguinte, ajusta
    if fim_vela <= agora:
        fim_vela += timedelta(days=1)

    # Calcula tempo restante até o fim da vela + buffer proporcional ao timeframe
    tempo_restante = (fim_vela - agora).total_seconds()

    # 🚨 FIX: Se o tempo restante for muito curto (ex: trade aberto no último segundo),
    # significa que a vela alvo é a PRÓXIMA, não a atual que está expirando.
    # Limite: 50% do timeframe (ex: se faltar menos de 2.5m para vela M5, ajusta)
    if tempo_restante < (timeframe_min * 60 * 0.5):
        log(f"[ADJUST] Tempo restante muito curto ({tempo_restante:.0f}s). Ajustando alvo para próxima vela...", "TIMING")
        fim_vela += timedelta(minutes=timeframe_min)
        tempo_restante = (fim_vela - agora).total_seconds()
        log(f"[ADJUST] Novo alvo: {fim_vela.strftime('%H:%M:%S')} (Falta: {tempo_restante:.0f}s)", "TIMING")

    # Buffer proporcional ao timeframe: M1=30s, M5=60s, M15=90s
    buffer = max(30, timeframe_min * 12)  # Proporcional ao timeframe

    timeout_minimo = max(90, tempo_restante + buffer)  # No mínimo 90 segundos

    log(f"[{par}] Aguardando fim da vela M{timeframe_min} (timeout: {timeout_minimo:.0f}s)...", "INFO")

    try:
        with lock_api:
            win, lucro = api.check_win_v4(id_ordem)
        return float(lucro)
    except Exception:
        pass
    
    inicio = time.time()
    timeout = timeout_minimo
    tempo_minimo_para_verificacao = timeframe_min * 60  # Tempo mínimo em segundos
    
    # 🚀 ZERO DELAY: Configuração de verificação ultra-rápida (Forçada)
    check_interval = 0.01  # Sempre 10ms
    log(f"[{par}] Modo ZERO DELAY (Polling Ativo 10ms)", "ZERO_DELAY")

    while time.time() - inicio < timeout:
        try:
            with lock_api:
                result = api.get_optioninfo_v2(10)
            closed = result.get('msg', {}).get('closed_options', []) if isinstance(result, dict) else []
            for opt in closed:
                oid_val = opt.get('id', [None])
                oid = oid_val[0] if isinstance(oid_val, list) else oid_val
                if str(oid) == str(id_ordem):
                    win = opt.get('win')
                    amount = float(opt.get('amount', 0))
                    win_amount = float(opt.get('win_amount', 0))
                    lucro = 0.0 if win == 'equal' else (win_amount - amount)
                    return float(lucro)
        except Exception:
            pass
        
        # 🚀 ZERO DELAY: Polling ativo
        time.sleep(check_interval)
    log(f"[{par}] Resultado não disponível no tempo limite.", "ERRO")
    return 0.0

def checar_resultado_digital(id_ordem, par, timeframe_min=15):
    # 🚀 VERIFICAÇÃO ULTRA-RÁPIDA - Sem logs desnecessários
    if config.get('timing_verificacao_imediata', False):
        # Modo ultra-rápido: verificação instantânea sem logs
        pass
    else:
        log(f"[{par}] Verificando resultado da operação (Digital)...", "INFO")

    # 🚨 CORREÇÃO: Calcula timeout inteligente baseado no timeframe e tempo restante da vela
    from datetime import datetime, timedelta
    agora = obter_hora_brasilia()

    # Validação do timeframe (mínimo 1, máximo 60 minutos)
    timeframe_min = max(1, min(timeframe_min, 60))

    # Calcular quando a vela vai fechar com base no horário da operação
    # A vela começa no início do quadrante do timeframe
    minuto_atual = agora.minute

    # 🚨 CORREÇÃO: Calcular o início da vela com base no timeframe
    if timeframe_min == 5:
        # M5: O quadrante começa no múltiplo de 5 minutos mais próximo
        minuto_inicio_vela = (minuto_atual // 5) * 5
    elif timeframe_min == 15:
        # M15: O quadrante começa no múltiplo de 15 minutos mais próximo
        minuto_inicio_vela = (minuto_atual // 15) * 15
    else:
        # Para outros timeframes, usar o cálculo padrão
        minuto_inicio_vela = (minuto_atual // timeframe_min) * timeframe_min

    # O fim da vela é o início mais o timeframe
    minuto_fim_vela = minuto_inicio_vela + timeframe_min

    if minuto_fim_vela >= 60:
        minuto_fim_vela = minuto_fim_vela - 60
        hora_fim = agora.hour + 1
        if hora_fim >= 24:
            hora_fim = 0
    else:
        hora_fim = agora.hour

    # Tempo quando a vela atual termina
    fim_vela = agora.replace(hour=hora_fim, minute=minuto_fim_vela, second=0, microsecond=0)

    # Se a vela termina no dia seguinte, ajusta
    if fim_vela <= agora:
        fim_vela += timedelta(days=1)

    # Calcula tempo restante até o fim da vela + buffer proporcional ao timeframe
    tempo_restante = (fim_vela - agora).total_seconds()

    # 🚨 FIX: Se o tempo restante for muito curto (ex: trade aberto no último segundo),
    # significa que a vela alvo é a PRÓXIMA, não a atual que está expirando.
    # Limite: 50% do timeframe (ex: se faltar menos de 2.5m para vela M5, ajusta)
    if tempo_restante < (timeframe_min * 60 * 0.5):
        log(f"[ADJUST] Tempo restante muito curto ({tempo_restante:.0f}s). Ajustando alvo para próxima vela...", "TIMING")
        fim_vela += timedelta(minutes=timeframe_min)
        tempo_restante = (fim_vela - agora).total_seconds()
        log(f"[ADJUST] Novo alvo: {fim_vela.strftime('%H:%M:%S')} (Falta: {tempo_restante:.0f}s)", "TIMING")

    # Buffer proporcional ao timeframe: M1=30s, M5=60s, M15=90s
    buffer = max(30, timeframe_min * 12)  # Proporcional ao timeframe

    timeout_minimo = max(90, tempo_restante + buffer)  # No mínimo 90 segundos

    log(f"[{par}] Aguardando fim da vela M{timeframe_min} (timeout: {timeout_minimo:.0f}s)...", "INFO")

    inicio = time.time()
    timeout = timeout_minimo
    
    # 🚀 ZERO DELAY: Configuração de verificação ultra-rápida (Forçada)
    check_interval = 0.01  # Sempre 10ms
    log(f"[{par}] Modo ZERO DELAY (Polling Ativo 10ms)", "ZERO_DELAY")
    
    while time.time() - inicio < timeout:
        try:
            ok, lucro = api.check_win_digital_v2(id_ordem)
            if ok:
                return float(lucro)
        except Exception:
            pass
        
        # 🚀 ZERO DELAY: Polling ativo
        time.sleep(check_interval)
    log(f"[{par}] Resultado digital não disponível no tempo limite.", "ERRO")
    return 0.0

def revalidar_resultado_final(id_ordem, par, modo_exec, tentativas=20, intervalo=1.0):
    """
    Revalida resultado quando a primeira consulta retorna 0.0.
    Evita perder fechamento por atraso pontual da API.
    """
    for _ in range(max(1, tentativas)):
        try:
            with lock_api:
                if modo_exec == 'DIGITAL':
                    ok, lucro = api.check_win_digital_v2(id_ordem)
                    if ok:
                        return float(lucro)
                else:
                    win, lucro = api.check_win_v4(id_ordem)
                    if win in ('win', 'loose', 'equal'):
                        return float(lucro)
        except Exception:
            pass
        time.sleep(max(0.05, intervalo))
    return 0.0

def aguardar_e_publicar_resultado_tecnico_sem_execucao(sinal, par, direcao, tf):
    """
    Fecha o sinal mesmo quando a ordem falha na corretora.
    Aguarda o fechamento da vela e publica um resultado técnico para não deixar sinal aberto.
    """
    try:
        agora = obter_hora_brasilia()
        h_base = sinal.get('hora') if sinal else None
        if not isinstance(h_base, datetime):
            h_base = agora
        fechamento = h_base + timedelta(minutes=max(1, int(tf)))
        espera = (fechamento - agora).total_seconds() + 2
        if espera > 0:
            time.sleep(min(espera, (max(1, int(tf)) * 60) + 5))

        velas = pegar_velas_blindada(par, 3, max(1, int(tf)) * 60)
        resultado = "DOJI"
        if velas and len(velas) >= 2:
            vela = velas[-2]
            abertura = float(vela.get('open', 0))
            fechamento_vela = float(vela.get('close', 0))
            if fechamento_vela > abertura:
                resultado = "WIN" if direcao.upper() == "CALL" else "LOSS"
            elif fechamento_vela < abertura:
                resultado = "WIN" if direcao.upper() == "PUT" else "LOSS"

        gale_nivel = sinal.get('gale_nivel', 0) if sinal else 0
        hora_sinal = sinal.get('hora') if sinal else None
        hora_str = hora_sinal.strftime("%H:%M") if isinstance(hora_sinal, datetime) else None
        adicionar_resultado_dia(par, tf, direcao, resultado, gale_nivel, hora_str)
        texto = formatar_resultado_canal(
            par,
            "Sem Execução (Ajuste Técnico)",
            resultado,
            gale_nivel,
            None,
            hora_str
        )
        notificar_canal(texto, 'resultados')
        log(f"[{par}] Resultado técnico publicado após falha de execução: {resultado}", "RESULTADOS")
    except Exception as e:
        log(f"[{par}] Erro ao publicar resultado técnico sem execução: {e}", "ERRO")

def processar_win(valor, par, tipo_operacao="Entrada Inicial", estrategia_id=None, sinal=None):
    global lucro_sessao, wins, lucro_anterior, prejuizo_acumulado, masa_wins_atuais, ciclo_atual, passo_atual, liberado_para_real, ultimo_status_operacao, stats_estrategias, aguardando_resultado_operacao
    
    # 🛡️ Reset agrupamento de BLOQUEIOS após WIN (mantém bloqueios e operações separados)
    reset_agrupamento_bloqueio()

    lucro_sessao += valor
    wins += 1
    
    # Adiciona resultado à lista do dia
    gale_nivel = sinal.get('gale_nivel', 0) if sinal else 0
    tf = sinal.get('tf', 1) if sinal else 1
    direcao = sinal.get('dir', 'CALL') if sinal else 'CALL'
    hora_sinal = sinal.get('hora') if sinal else None
    hora_str = hora_sinal.strftime("%H:%M") if hora_sinal else None
    adicionar_resultado_dia(par, tf, direcao, "WIN", gale_nivel, hora_str)
    
    # 💾 Atualiza timestamp de última operação e salva estado IMEDIATAMENTE
    global ultima_operacao
    ultima_operacao = obter_hora_brasilia()
    save_state_now()  # Salvamento imediato, sem debouncing

    if estrategia_id:
        if estrategia_id not in stats_estrategias:
            stats_estrategias[estrategia_id] = {"wins": 0, "loss": 0, "lucro": 0.0}
        stats_estrategias[estrategia_id]["wins"] += 1
        stats_estrategias[estrategia_id]["lucro"] += valor

    if config['filtro_virtual']:
        liberado_para_real = False
        log("Retornando ao Modo Virtual...", "VIRTUAL")

    if config['modo_gestao'] in ["SOROS", "SOROS_GALE"]:
        lucro_anterior += valor
        if wins > 0 and wins % config['soros_niveis'] == 0:
            lucro_anterior = 0.0
        # ✅ Lógica de dívida uniforme para SOROS/SOROS_GALE
        if prejuizo_acumulado < 0:
            prejuizo_acumulado += valor  # Soma o valor do win (positivo) à dívida (negativa)
            if prejuizo_acumulado >= 0: # Se a dívida for quitada
                log(f"[RECUP] Dívida de ${abs(prejuizo_acumulado - valor):.2f} quitada com o win de ${valor:.2f}", "WIN")
                prejuizo_acumulado = 0.0 # Zera a dívida
            else:
                log(f"[RECUP] Win de ${valor:.2f} reduziu a dívida para ${abs(prejuizo_acumulado):.2f}", "INFO")

    # ✅ ATUALIZADO: A dívida é atualizada com o valor total do win
    elif config['modo_gestao'] in ["MARTINGALE_RECUPERACAO", "MARTINGALE_RECUPERACAO_PROGRESSIVA"]:
        if prejuizo_acumulado < 0:
            prejuizo_acumulado += valor  # Soma o valor do win (positivo) à dívida (negativa)
            if prejuizo_acumulado >= 0: # Se a dívida for quitada
                log(f"[RECUP] Dívida de ${abs(prejuizo_acumulado - valor):.2f} quitada com o win de ${valor:.2f}", "WIN")
                prejuizo_acumulado = 0.0 # Zera a dívida
            else:
                log(f"[RECUP] Win de ${valor:.2f} reduziu a dívida para ${abs(prejuizo_acumulado):.2f}", "INFO")

    elif config['modo_gestao'] == "RECUPERACAO_SEPARADA":
        prejuizo_acumulado = 0.0

    elif config['modo_gestao'] == "MARTINGALE":
        # ✅ Lógica de dívida uniforme para MARTINGALE normal
        if prejuizo_acumulado < 0:
            prejuizo_acumulado += valor  # Soma o valor do win (positivo) à dívida (negativa)
            if prejuizo_acumulado >= 0: # Se a dívida for quitada
                log(f"[RECUP] Dívida de ${abs(prejuizo_acumulado - valor):.2f} quitada com o win de ${valor:.2f}", "WIN")
                prejuizo_acumulado = 0.0 # Zera a dívida
            else:
                log(f"[RECUP] Win de ${valor:.2f} reduziu a dívida para ${abs(prejuizo_acumulado):.2f}", "INFO")

    elif "MASANIELLO" in config['modo_gestao']:
        masa_wins_atuais += 1
        if prejuizo_acumulado < 0:
            prejuizo_acumulado += valor  # Soma o valor do win (positivo) à dívida (negativa)
            if prejuizo_acumulado >= 0: # Se a dívida for quitada
                log(f"[RECUP] Dívida de ${abs(prejuizo_acumulado - valor):.2f} quitada com o win de ${valor:.2f}", "WIN")
                prejuizo_acumulado = 0.0 # Zera a dívida
            else:
                log(f"[RECUP] Win de ${valor:.2f} reduziu a dívida para ${abs(prejuizo_acumulado):.2f}", "INFO")

    elif config['modo_gestao'] == "CICLOS":
        ciclo_atual = 0
        passo_atual = 0
        # ✅ Lógica de dívida uniforme para CICLOS
        if prejuizo_acumulado < 0:
            prejuizo_acumulado += valor  # Soma o valor do win (positivo) à dívida (negativa)
            if prejuizo_acumulado >= 0: # Se a dívida for quitada
                log(f"[RECUP] Dívida de ${abs(prejuizo_acumulado - valor):.2f} quitada com o win de ${valor:.2f}", "WIN")
                prejuizo_acumulado = 0.0 # Zera a dívida
            else:
                log(f"[RECUP] Win de ${valor:.2f} reduziu a dívida para ${abs(prejuizo_acumulado):.2f}", "INFO")
        # 🛡️ REMOVIDO: Notificação de ciclo finalizado para chat privado
        # bot.send_message(MEU_ID, "🔄 <b>Ciclo de gestão finalizado com um WIN!</b>", parse_mode="HTML")
        
    elif config['modo_gestao'] == "MAO_FIXA":
        # ✅ Lógica de dívida uniforme para MAO_FIXA
        if prejuizo_acumulado < 0:
            prejuizo_acumulado += valor  # Soma o valor do win (positivo) à dívida (negativa)
            if prejuizo_acumulado >= 0: # Se a dívida for quitada
                log(f"[RECUP] Dívida de ${abs(prejuizo_acumulado - valor):.2f} quitada com o win de ${valor:.2f}", "WIN")
                prejuizo_acumulado = 0.0 # Zera a dívida
            else:
                log(f"[RECUP] Win de ${valor:.2f} reduziu a dívida para ${abs(prejuizo_acumulado):.2f}", "INFO")

    # ✅ ALTERADO: Mensagem de WIN mais descritiva
    relatorio_atual = obter_texto_relatorio()
    
    tipo_conta = "🟢 DEMO" if config.get('tipo') == "PRACTICE" else "🔴 REAL"
    ultimo_status_operacao = f"✅ WIN [{par}] +${valor:.2f}"
    
    # Formato específico para canais
    gale_nivel = sinal.get('gale_nivel', 0) if sinal else 0
    hora_op = None
    if sinal:
        h_exec = sinal.get('h_execucao')
        if h_exec:
            if isinstance(h_exec, datetime):
                hora_op = h_exec.strftime("%H:%M")
            else:
                hora_op = str(h_exec)[:5]
    texto_win = formatar_resultado_canal(par, tipo_operacao, "WIN", gale_nivel, None, hora_op)
    
    notificar_canal(texto_win, 'resultados')
    aguardando_resultado_operacao = False
    
    # 🛡️ REMOVIDO: Notificação de resultado para chat privado
    # Os resultados já são enviados para os canais configurados
    # log(f"[{par}] Win ({tipo_operacao}) +{valor:.2f}", "WIN")
    verificar_stops()


def processar_loss(valor, par, tipo_operacao="Entrada Inicial", estrategia_id=None, sinal=None):
    global lucro_sessao, loss, lucro_anterior, prejuizo_acumulado, masa_loss_atuais, ciclo_atual, passo_atual, liberado_para_real, ultimo_status_operacao, stats_estrategias, aguardando_resultado_operacao
    
    # 🛡️ Reset agrupamento de BLOQUEIOS após LOSS
    reset_agrupamento_bloqueio()

    lucro_sessao += valor
    loss += 1
    
    # Adiciona resultado à lista do dia
    gale_nivel = sinal.get('gale_nivel', 0) if sinal else 0
    tf = sinal.get('tf', 1) if sinal else 1
    direcao = sinal.get('dir', 'CALL') if sinal else 'CALL'
    hora_sinal = sinal.get('hora') if sinal else None
    hora_str = hora_sinal.strftime("%H:%M") if hora_sinal else None
    adicionar_resultado_dia(par, tf, direcao, "LOSS", gale_nivel, hora_str)
    
    # 💾 Atualiza timestamp de última operação e salva estado IMEDIATAMENTE
    global ultima_operacao
    ultima_operacao = obter_hora_brasilia()
    save_state_now()  # Salvamento imediato, sem debouncing

    if estrategia_id:
        if estrategia_id not in stats_estrategias:
            stats_estrategias[estrategia_id] = {"wins": 0, "loss": 0, "lucro": 0.0}
        stats_estrategias[estrategia_id]["loss"] += 1
        stats_estrategias[estrategia_id]["lucro"] += valor

    if config['filtro_virtual']:
        liberado_para_real = False
        log("Retornando ao Modo Virtual...", "VIRTUAL")

    if config['modo_gestao'] in ["SOROS", "SOROS_GALE"]:
        lucro_anterior = 0.0
        # ✅ Lógica de dívida uniforme para SOROS/SOROS_GALE
        prejuizo_acumulado += valor  # Soma o valor do loss (negativo) à dívida
        log(f"[RECUP] Novo loss de ${valor:.2f}. Dívida total atualizada para ${abs(prejuizo_acumulado):.2f}", "LOSS")

    # ✅ ATUALIZADO: A dívida é atualizada com o valor total do loss
    elif config['modo_gestao'] in ["MARTINGALE", "MARTINGALE_RECUPERACAO", "MARTINGALE_RECUPERACAO_PROGRESSIVA", "RECUPERACAO_SEPARADA"]:
        prejuizo_acumulado += valor  # Soma o valor do loss (negativo) à dívida
        log(f"[RECUP] Novo loss de ${valor:.2f}. Dívida total atualizada para ${abs(prejuizo_acumulado):.2f}", "LOSS")

    elif "MASANIELLO" in config['modo_gestao']:
        masa_loss_atuais += 1
        if lucro_sessao < 0:
            prejuizo_acumulado += valor  # Soma o valor do loss (negativo) à dívida existente

    elif config['modo_gestao'] == "CICLOS":
        passo_atual += 1
        if passo_atual >= len(config['lista_ciclos'][ciclo_atual]):
            passo_atual = 0
            ciclo_atual += 1
            if ciclo_atual >= len(config['lista_ciclos']):
                ciclo_atual = 0
        # ✅ Lógica de dívida uniforme para CICLOS
        prejuizo_acumulado += valor  # Soma o valor do loss (negativo) à dívida
        log(f"[RECUP] Novo loss de ${valor:.2f}. Dívida total atualizada para ${abs(prejuizo_acumulado):.2f}", "LOSS")

    elif config['modo_gestao'] == "MAO_FIXA":
        # ✅ Lógica de dívida uniforme para MAO_FIXA
        prejuizo_acumulado += valor  # Soma o valor do loss (negativo) à dívida
        log(f"[RECUP] Novo loss de ${valor:.2f}. Dívida total atualizada para ${abs(prejuizo_acumulado):.2f}", "LOSS")

    # ✅ ALTERADO: Mensagem de LOSS mais descritiva
    relatorio_atual = obter_texto_relatorio()
    tipo_conta = "🟢 DEMO" if config.get('tipo') == "PRACTICE" else "🔴 REAL"
    ultimo_status_operacao = f"❌ LOSS [{par}] {valor:.2f}"
    
    # Formato específico para canais
    gale_nivel = sinal.get('gale_nivel', 0) if sinal else 0
    hora_op = None
    if sinal:
        h_exec = sinal.get('h_execucao')
        if h_exec:
            if isinstance(h_exec, datetime):
                hora_op = h_exec.strftime("%H:%M")
            else:
                hora_op = str(h_exec)[:5]
    texto_loss = formatar_resultado_canal(par, tipo_operacao, "LOSS", gale_nivel, None, hora_op)
    
    notificar_canal(texto_loss, 'resultados')
    aguardando_resultado_operacao = False
    
    # 🛡️ REMOVIDO: Notificação de resultado para chat privado
    # Os resultados já são enviados para os canais configurados
    # log(f"[{par}] Loss ({tipo_operacao}) {valor:.2f}", "LOSS")
    verificar_stops()


def operar(sinal):
    global ops_ativas, liberado_para_real, cooldown_ate, aguardando_resultado_operacao
    if verificar_stops():
        return
    
    with lock_ops:


        ops_ativas += 1
    try:
        par, dir_op, tf = sinal['par'], sinal['dir'], sinal['tf']
        aguardando_resultado_operacao = True
        
        # 🛡️ VERIFICAÇÃO CRÍTICA: Filtro de tipo de mercado (SÍNCRONO)
        # Deve ser executado ANTES de qualquer processamento para bloquear OTC imediatamente
        if config['tipo_mercado'] != "TODOS":
            is_otc = "-OTC" in par.upper()
            if config['tipo_mercado'] == "ABERTO" and is_otc:
                log(f"🛡️ [{par}] Operação BLOQUEADA: Mercado OTC bloqueado - Operação apenas em mercado aberto", "FILTRO")
                sinal['status'] = 'bloqueado'
                aguardando_resultado_operacao = False
                return
            elif config['tipo_mercado'] == "OTC" and not is_otc:
                log(f"🛡️ [{par}] Operação BLOQUEADA: Mercado Aberto bloqueado - Operação apenas em OTC", "FILTRO")
                sinal['status'] = 'bloqueado'
                aguardando_resultado_operacao = False
                return
        
        if sinal.get('estrategia_id'):
            log(f"Preparando entrada por {sinal.get('origem_texto')} em [{par}]...", "INFO")
        if config['inverter_sinal']:
            dir_op_original = dir_op.upper()
            dir_op = 'PUT' if dir_op.upper() == 'CALL' else 'CALL'
            log(f"[{par}] Sinal {dir_op_original} invertido para {dir_op}", "INFO")

        # 🔗 VERIFICAÇÃO DE CONFLUÊNCIAS
        confluencias_ativas = config.get('confluencias', {})
        if confluencias_ativas and any(confluencias_ativas.values()):
            # Pega velas para análise de confluências
            velas_confluencias = pegar_velas_blindada(par, 200, tf * 60)
            if velas_confluencias:
                aprovado, resultados = confluencias.verificar_confluencias(velas_confluencias, dir_op, confluencias_ativas)
                
                if aprovado:
                    log(f"🔗 [{par}] Confluências APROVADAS para {dir_op.upper()}", "CONFLUENCIA")
                    # Log detalhado das confluências aprovadas
                    for nome, resultado in resultados.items():
                        if resultado['aprovado']:
                            log(f"  ✅ {nome}: {resultado['mensagem']}", "CONFLUENCIA")
                else:
                    log(f"🔗 [{par}] Confluências REPROVADAS para {dir_op.upper()}", "CONFLUENCIA")
                    # Log detalhado das confluências reprovadas
                    for nome, resultado in resultados.items():
                        if not resultado['aprovado']:
                            log(f"  ❌ {nome}: {resultado['mensagem']}", "CONFLUENCIA")
                    
                    # Notifica sobre rejeição por confluências
                    nomes_conf = confluencias.obter_nomes_confluencias()
                    confluencias_ativas_nomes = [nomes_conf.get(nome, nome) for nome, ativa in confluencias_ativas.items() if ativa]
                    
                    enviar_notificacao_bloqueio(par, dir_op, tf, sinal['hora'], "Confluências", confluencias_ativas_nomes, "Pelo menos uma confluência não confirmou o sinal")
                    
                    sinal['status'] = 'bloqueado_confluencias'
                    aguardando_resultado_operacao = False
                    return
            else:
                log(f"🔗 [{par}] Não foi possível verificar confluências (sem dados)", "CONFLUENCIA")
        else:
            log(f"🔗 [{par}] Nenhuma confluência ativa - sinal liberado", "CONFLUENCIA")

        em_simulacao = False
        if config['filtro_virtual'] and not liberado_para_real:
            em_simulacao = True
            log(f"[{par}] Entrada VIRTUAL (Aguardando {config['virtual_condicao']})", "VIRTUAL")

        if not em_simulacao:
            if sinal.get('filtro_msg') != "OK":
                aguardando_resultado_operacao = False
                return
            modo_exec = sinal.get('modo_exec') or selecionar_modo_para_sinal(par)
            
            # --- MELHORIA: PRÉ-PREPARAÇÃO ULTRA-RÁPIDA ---
            # Pré-carrega payout e modo em paralelo ANTES da hora de execução
            payout = sinal.get('payout_pre', 0) or checar_payout(par)
            modo_exec = sinal.get('modo_exec') or selecionar_modo_para_sinal(par)
            
            # Se payout zerado, tenta uma vez rápida
            if payout == 0:
                payout = checar_payout(par)

            alvo = sinal['hora']
            agora_ini = obter_hora_brasilia()
            if agora_ini < alvo:
                # Calcula tempo exato com precisão de milissegundos
                tempo_espera = (alvo - agora_ini).total_seconds()
                if tempo_espera > 0.001:  # Só espera se for > 1ms
                    # Para tempos muito curtos (< 50ms), usa busy-wait otimizado
                    if tempo_espera < 0.05:
                        import time as time_module
                        tempo_inicial = time_module.perf_counter()
                        while (time_module.perf_counter() - tempo_inicial) < tempo_espera:
                            pass  # Busy-wait otimizado para microssegundos
                    else:
                        # Para tempos maiores, sleep com precisão melhorada
                        time.sleep(tempo_espera - 0.001)  # Ajusta 1ms antes
            
            limite_toler = sinal['hora'] + timedelta(seconds=config.get('tolerancia', 0))
            if obter_hora_brasilia() > limite_toler:
                try:
                    tf = int(sinal.get('tf', 1))
                    sinal['status'] = 'expirado'
                    log(f"[{par}] Tolerância excedida antes da entrada. Sinal expirado (TF M{tf}).", "INFO")
                    msg_exp = f"⏳ <b>Entrada Expirada</b>\n<b>[{par}]</b> TF M{tf}\n🕒 Alvo perdido, não reagendado."
                    # 🛡️ REMOVIDO: Notificação para chat privado
                    # bot.send_message(MEU_ID, msg_exp, parse_mode="HTML")
                except:
                    pass
                aguardando_resultado_operacao = False
                return

            # --- MELHORIA: NOTIFICAÇÃO DE PAYOUT ---
            if config['payout_min'] > 0 and payout < config['payout_min']:
                motivo_pay = "Payout Baixo" if payout > 0 else "Ativo Fechado ou Indisponível"
                log(f"[{par}] Entrada cancelada: {motivo_pay} ({payout}%)", "FILTRO")
                msg_cancel = f"⚠️ <b>Entrada Cancelada: {motivo_pay}</b>\n<b>[{par}]</b> Payout: {payout}% (Mínimo: {config['payout_min']}%)"
                # 🛡️ REMOVIDO: Notificação para chat privado
                # bot.send_message(MEU_ID, msg_cancel, parse_mode="HTML")
                aguardando_resultado_operacao = False
                return
            
            valor_entrada = calcular_valor_entrada(0, payout)

            if risco_excede_stop(valor_entrada):
                msg_risco = f"🛑 <b>Entrada Cancelada por Risco de Stop</b>\n<b>[{par}]</b> O valor de entrada ${valor_entrada:.2f} ultrapassaria o limite de perda da sessão."
                # 🛡️ REMOVIDO: Notificação para chat privado
                # bot.send_message(MEU_ID, msg_risco, parse_mode="HTML")
                aguardando_resultado_operacao = False
                return

            # 🚀 ZERO DELAY: Removido delay artificial - máxima velocidade
            if config['delay'] > 0:
                log(f"⚠️ DELAY CONFIGURADO ({config['delay']}s) - DESATIVE PARA ZERO DELAY ABSOLUTO!", "ZERO_DELAY_ALERT")
                log(f"🚀 RECOMENDAÇÃO: Use delay=0 para máxima performance", "ZERO_DELAY_ALERT")
                # Apenas avisa, mas não executa delay para manter performance
            
            
            limite_toler2 = sinal['hora'] + timedelta(seconds=config.get('tolerancia', 0))
            if obter_hora_brasilia() > limite_toler2:
                try:
                    tf = int(sinal.get('tf', 1))
                    sinal['status'] = 'expirado'
                    origem = "Manual" if sinal.get('manual') else (sinal.get('origem_texto') or "Automático")
                    log(f"[{par}] Tolerância excedida antes do envio. Sinal expirado ({origem}, TF M{tf}).", "INFO")
                    msg_titulo = "Entrada Manual Descartada" if sinal.get('manual') else "Entrada Expirada"
                    # 🛡️ REMOVIDO: Notificação para chat privado
                    # bot.send_message(MEU_ID, f"⏳ <b>{msg_titulo}</b>\n<b>[{par}]</b> {origem}\n🕒 Alvo perdido, não reagendado.", parse_mode="HTML")
                except:
                    pass
                aguardando_resultado_operacao = False
                return

            # 🕐 VERIFICAÇÃO DE TIMING: Se está entrando tarde na vela
            esta_tarde, segundos_restantes, percentual_passado = verificar_entrada_tarde_na_vela(tf, obter_hora_brasilia())
            
            if esta_tarde:
                log(f"⚠️ Entrando tarde na vela: {percentual_passado*100:.1f}% passado, {segundos_restantes:.0f}s restantes", "TIMING")
                # 🚨 AGORA PERMITE ENTRADAS COM MENOS DE 30s - Só avisa mas não cancela
                if segundos_restantes < 30:
                    log(f"⚠️ Entrada permitida com {segundos_restantes:.0f}s restantes - expirará na próxima vela", "TIMING")
            
            # 🛡️ Reset agrupamento ao iniciar uma operação real (ENVIAR PARA API)
            reset_agrupamento_bloqueio()

            # 🚀 EXECUÇÃO API ULTRA-RÁPIDA
            with lock_api:

                import time as time_module
                t_net_ini = time_module.perf_counter()
                try:
                    if modo_exec == 'DIGITAL':
                        status, id_ordem = api.buy_digital_spot_v2(par, valor_entrada, dir_op, tf)
                    else:
                        status, id_ordem = api.buy(valor_entrada, par, dir_op, tf)
                except Exception as e:
                    log(f"Erro API: {e}", "ERRO")
                    status, id_ordem = False, None
                t_net = time_module.perf_counter() - t_net_ini
                
                # PRIORIDADE TOTAL: Se a ordem foi enviada, foca em confirmar antes de logar
                if not status:
                    # 🛡️ REMOVIDO: Notificação para chat privado
                    # bot.send_message(MEU_ID, f"❌ <b>Falha ao Enviar Entrada</b>\n<b>[{par}]</b> A API retornou um erro. Tente novamente.", parse_mode="HTML")
                    log(f"❌ Falha ao enviar entrada para [{par}]", "ERRO")
                    aguardar_e_publicar_resultado_tecnico_sem_execucao(sinal, par, dir_op, tf)
                    aguardando_resultado_operacao = False
                    return

                t_send = obter_hora_brasilia()
                aguardando_resultado_operacao = True
                
                # LOGS E TELEGRAM SOMENTE DEPOIS DA ORDEM CONFIRMADA
                # Isso garante que o processamento de texto/rede do bot não atrase a próxima ação crítica (monitoramento)
                try:
                    hora_entrada = t_send.strftime("%H:%M:%S")
                    
                    # 🚀 LOGGING OTIMIZADO PARA MÁXIMA VELOCIDADE
                    delta_ms = abs((t_send - alvo).total_seconds() * 1000)
                    
                    # 🛡️ REMOVIDO: Notificação de operação para chat privado
                    # Obot agora apenas envia sinais e resultados para canais/grupos configurados
                    # Os sinais já são enviados quando detectados/agendados
                    # Os resultados são enviados automaticamente quando processados
                    # def _send_tg():
                    #     try:
                    #         msg_corpo = formatar_sinal_canal(par, dir_op, tf, hora_entrada, valor_entrada, payout)
                    #         msg = bot.send_message(MEU_ID, msg_corpo, parse_mode="HTML")
                    #         sinal['msg_id'] = msg.message_id
                    #         sinal['msg_corpo'] = msg_corpo
                    #     except:
                    #         pass
                    # threading.Thread(target=_send_tg, daemon=True).start()


                    # Log otimizado - apenas essencial
                    log(f"[{par}] {dir_op.upper()} ${valor_entrada:.2f} ({modo_exec}, {payout}%, M{tf})", "ENTRADA")
                    
                    # Estatísticas rápidas
                    global exec_total, exec_ok_1s
                    exec_total += 1
                    delta = delta_ms / 1000
                    if delta <= 1.0:
                        exec_ok_1s += 1
                    if exec_total % 10 == 0:  # Só loga estatísticas a cada 10 execuções
                        taxa = (exec_ok_1s / exec_total) * 100 if exec_total > 0 else 0
                        log(f"📊 Timing: Δ={delta:.3f}s, rede={t_net:.3f}s, ≤1s={taxa:.1f}%", "STATS")
                except:
                    pass
        else:
            status = True
            id_ordem = None
        # Removido delay desnecessário após envio da ordem
        # O monitoramento será feito de forma assíncrona

        if em_simulacao:
            velas_sim = pegar_velas_blindada(par, 2)
            if velas_sim:
                cl = float(velas_sim[-1]['close'])
                op = float(velas_sim[-1]['open'])
                res_sim = "DOJI"
                if cl > op:
                    res_sim = "CALL"
                elif cl < op:
                    res_sim = "PUT"
                cond_win = (res_sim == dir_op.upper())
                cond_loss = (res_sim != dir_op.upper() and res_sim != "DOJI")
                global virtual_contador
                alvo = config['virtual_condicao']
                meta = config['virtual_qtd']
                atingiu = False
                if alvo == "WIN" and cond_win:
                    atingiu = True
                elif alvo == "LOSS" and cond_loss:
                    atingiu = True
                if atingiu:
                    virtual_contador += 1
                    log(f"Simulação: OK ({virtual_contador}/{meta})", "VIRTUAL")
                    if virtual_contador >= meta:
                        liberado_para_real = True
                        virtual_contador = 0
                        # 🛡️ REMOVIDO: Notificação para chat privado
                        # bot.send_message(MEU_ID, "👻 <b>Modo Virtual Concluído!</b>\nO robô foi liberado para operar com entradas REAIS.", parse_mode="HTML")
                else:
                    if res_sim != "DOJI":
                        virtual_contador = 0
                        log("Simulação: Reset.", "VIRTUAL")
            aguardando_resultado_operacao = False
            return

        resultado = checar_resultado_digital(id_ordem, par, tf) if (not em_simulacao and modo_exec == 'DIGITAL') else checar_resultado_oficial(id_ordem, par, tf)
        if resultado == 0 and not em_simulacao:
            log(f"[{par}] Resultado 0.0 na primeira consulta. Revalidando...", "INFO")
            resultado = revalidar_resultado_final(id_ordem, par, modo_exec, tentativas=20, intervalo=1.0)
        estrategia_id = sinal.get('estrategia_id')
        if resultado > 0:
            processar_win(resultado, par, sinal.get('origem_texto', "Entrada Inicial"), estrategia_id=estrategia_id, sinal=sinal)

            try:
                if int(config.get('intervalo_operacoes', 0)) > 0:
                    cooldown_ate = obter_hora_brasilia() + timedelta(seconds=int(config.get('intervalo_operacoes', 0)))
                    log(f"⏱️ Intervalo entre operações iniciado por {int(config.get('intervalo_operacoes', 0))}s.", "INFO")
            except:
                pass
        elif resultado < 0:
            if verificar_stops():
                return
            faz_gale = True
            if config["gales"] == 0:
                faz_gale = False
            modos_sem_gale = ["RECUPERACAO_SEPARADA", "MASANIELLO", "CICLOS", "MAO_FIXA"]
            if config["modo_gestao"] in modos_sem_gale:
                faz_gale = False
            if faz_gale:
                # Chama martingale passando o sinal para agrupamento
                fazer_martingale(par, dir_op, tf, payout, resultado, estrategia_id=estrategia_id, hora_base=sinal['hora'], agendamento_completo=sinal.get('agendamento_completo', False), sinal=sinal)
            else:
                processar_loss(resultado, par, sinal.get('origem_texto', "Entrada Inicial"), estrategia_id=estrategia_id, sinal=sinal)

                try:
                    if int(config.get('intervalo_operacoes', 0)) > 0:
                        cooldown_ate = obter_hora_brasilia() + timedelta(seconds=int(config.get('intervalo_operacoes', 0)))
                        log(f"⏱️ Intervalo entre operações iniciado por {int(config.get('intervalo_operacoes', 0))}s.", "INFO")
                except:
                    pass
        else:
            global ultimo_status_operacao
            ultimo_status_operacao = f"⚪️ DOJI [{par}]"
            texto_doji = f"⚪️ <b>DOJI na Entrada Inicial</b>\n<b>[{par}]</b> Preço de abertura e fechamento foram iguais. Sem perdas."

            gale_nivel = sinal.get('gale_nivel', 0) if sinal else 0
            tf_res = sinal.get('tf', 1) if sinal else 1
            direcao = sinal.get('dir', 'CALL') if sinal else 'CALL'
            hora_sinal = sinal.get('hora') if sinal else None
            hora_str = hora_sinal.strftime("%H:%M") if hora_sinal else None
            adicionar_resultado_dia(par, tf_res, direcao, "DOJI", gale_nivel, hora_str)
            notificar_canal(
                formatar_resultado_canal(
                    par,
                    sinal.get('origem_texto', "Entrada Inicial"),
                    "DOJI",
                    gale_nivel,
                    None,
                    hora_str
                ),
                'resultados'
            )
            aguardando_resultado_operacao = False
            
            # 🛡️ REMOVIDO: Notificação de DOJI para chat privado
            # log apenas
            log(f"⚠️ DOJI na entrada [{par}]", "INFO")

            try:
                if int(config.get('intervalo_operacoes', 0)) > 0:
                    cooldown_ate = obter_hora_brasilia() + timedelta(seconds=int(config.get('intervalo_operacoes', 0)))
                    log(f"⏱️ Intervalo entre operações iniciado por {int(config.get('intervalo_operacoes', 0))}s.", "INFO")
            except:
                pass
    except Exception as e:
        log(f"Erro na operação: {e}", "ERRO")
        aguardando_resultado_operacao = False
        traceback.print_exc()
    finally:
        sinal['status'] = 'concluido'
        aguardando_resultado_operacao = False
        try:
            if sinal.get('estrategia'):
                global estrategia_em_andamento
                estrategia_em_andamento = False
                log(f"✅ Estratégia {sinal.get('estrategia_id', 'N/A')} concluída para {sinal.get('par', 'N/A')} - Liberando para novas análises", "ESTRATEGIA")
        except:
            pass
        with lock_ops:
            ops_ativas -= 1

def fazer_martingale(par, dir_op, tf, payout, perda_inicial, estrategia_id=None, hora_base=None, agendamento_completo=False, sinal=None):
    global lucro_sessao, cooldown_ate
    perda_total = perda_inicial
    for g in range(1, config["gales"] + 1):
        if not rodando:
            break
        if verificar_stops():
            break
        if config['gale_inteligente']:
            if config['filtro_tendencia'] or config['filtro_3ma'] or config['tipo_mercado'] != "TODOS":
                aprov, mot = executar_filtros(par, dir_op)
                if not aprov:
                    # 🛡️ REMOVIDO: Notificação de gale bloqueado para chat privado
                    log(f"🛡️ Gale {g} bloqueado por filtro: [{par}] - {mot}", "FILTRO")
                    break
        payout_step = checar_payout(par)
        valor = calcular_valor_entrada(g, payout_step)

        # 🚀 LÓGICA DE INVERSÃO DE GALE
        dir_gale = dir_op
        if config.get('inverter_gale_alternado', False):
            # Alterna a cada gale: G1 Inverte, G2 Original, G3 Inverte...
            # Gale 1, 3, 5... (ímpares) -> Inverte
            if g % 2 != 0:
                dir_gale = 'PUT' if dir_op.upper() == 'CALL' else 'CALL'
        elif config.get('inverter_gale_1', False):
            # Inverte a partir do Gale 1 e mantem invertido
            dir_gale = 'PUT' if dir_op.upper() == 'CALL' else 'CALL'
        
        if dir_gale != dir_op:
            log(f"🔄 Gale {g} Invertido: {dir_op} -> {dir_gale}", "INFO")

        if risco_excede_stop(valor):
            # 🚀 Envia mensagem Telegram em thread separada (rápida) - EVITA DELAY
            def _send_tg_gale_cancelado():
                try:
                    texto_cancelado = f"🛑 <b>Gale {g} Cancelado por Risco de Stop</b>\n<b>[{par}]</b> O valor de entrada ${valor:.2f} ultrapassaria o limite de perda da sessão."
                    if sinal and sinal.get('msg_id') and sinal.get('msg_corpo'):
                        sinal['msg_corpo'] += "\n\n" + texto_cancelado
                        bot.edit_message_text(sinal['msg_corpo'], MEU_ID, sinal['msg_id'], parse_mode="HTML")
                    else:
                        bot.send_message(MEU_ID, texto_cancelado, parse_mode="HTML")
                except:
                    pass
            threading.Thread(target=_send_tg_gale_cancelado, daemon=True).start()
            break
        
        modo_exec = selecionar_modo_para_sinal(par)
        
        # 🎯 FIX CRÍTICO: Cálculo Universal de Timing para Gales (SEM DRIFT)
        # O objetivo é entrar na PRÓXIMA VELA DISPONÍVEL imediatamente após o resultado.
        agora = obter_hora_brasilia()
        
        # Calcula o início da vela atual (baseado no timeframe)
        minuto_inicio_vela = (agora.minute // tf) * tf
        inicio_vela_atual = agora.replace(minute=minuto_inicio_vela, second=0, microsecond=0)
        fim_vela_atual = inicio_vela_atual + timedelta(minutes=tf)
        
        # Diferença em relação ao início da vela
        segundos_passados = (agora - inicio_vela_atual).total_seconds()
        
        # 🚀 LÓGICA ULTRA-GALE: 
        # Se o resultado saiu logo no início da vela (até 6s), entra na vela atual AGORA.
        # Se demorou mais, aguarda o início exato da próxima vela.
        if segundos_passados <= 6:
            h_gale_alvo = agora + timedelta(milliseconds=100) # Entrada imediata
            log(f"🚀 Gale {g} AGRESSIVO: entrando na vela atual ({segundos_passados:.1f}s passados)", "GALE_AGRESSIVO")
        else:
            h_gale_alvo = fim_vela_atual
            log(f"⏳ Gale {g}: aguardando início da próxima vela ({h_gale_alvo.strftime('%H:%M:%S')})", "GALE_TIMING")
            
        # 🚀 EXECUÇÃO DIRETA PARA GALES
        tempo_ate_gale = (h_gale_alvo - obter_hora_brasilia()).total_seconds()

        
        # Sleep simplificado para gales

        
        # Sleep simplificado para gales
        tempo_ate_exec = (h_gale_alvo - obter_hora_brasilia()).total_seconds()
        if tempo_ate_exec > 0:
            time.sleep(tempo_ate_exec)
        
        t_send_gale = obter_hora_brasilia()
        with lock_api:
            if modo_exec == 'DIGITAL':
                status, id_gale = api.buy_digital_spot_v2(par, valor, dir_gale, tf)
            else:
                status, id_gale = api.buy(valor, par, dir_gale, tf)
        t_api_response = obter_hora_brasilia()
        api_delay_ms = (t_api_response - t_send_gale).total_seconds() * 1000
        
        if status:
            hora_gale = t_send_gale.strftime("%H:%M:%S")
            # 🚀 LOG IMEDIATO: Mostra timing da API sem esperar Telegram
            log(f"🔄 Gale {g}: API executada em {api_delay_ms:.0f}ms", "GALE_TIMING")
            
            # 🛡️ REMOVIDO: Notificação de gale para chat privado
            # Os gales agora são tratados automaticamente sem notificações para o chat privado
            # O resultado final será enviado para os canais configurados
            texto_gale = f"🔄 <b>Enviando Gale {g}</b>\n<b>[{par}]</b> {dir_gale.upper()} | ${valor:.2f} ({hora_gale})\n🎛️ Modo: <b>{modo_exec}</b> • TF M{tf}\n⚡ API: {api_delay_ms:.0f}ms"
            
            # Gales não são mais enviados para o chat privado
            # if config.get('timing_sem_delay_telegram', False) or (sinal and sinal.get('msg_id')):
            #     if sinal and sinal.get('msg_id') and sinal.get('msg_corpo'):
            #         sinal['msg_corpo'] += "\n\n" + texto_gale
            #         bot.edit_message_text(sinal['msg_corpo'], MEU_ID, sinal['msg_id'], parse_mode="HTML")
            #     else:
            #         bot.send_message(MEU_ID, texto_gale, parse_mode="HTML")
            # else:
            #     def _send_tg_gale():
            #         try:
            #             bot.send_message(MEU_ID, texto_gale, parse_mode="HTML")
            #         except:
            #             pass
            #     threading.Thread(target=_send_tg_gale, daemon=True).start()
                
            # Monitoramento assíncrona - remove delay bloqueante
            res = checar_resultado_digital(id_gale, par, tf) if modo_exec == 'DIGITAL' else checar_resultado_oficial(id_gale, par, tf)
            if res > 0:
                # Atualiza o gale_nivel no sinal antes de processar o win
                if sinal:
                    sinal['gale_nivel'] = g
                processar_win(res + perda_total, par, f"Gale {g}", estrategia_id=estrategia_id, sinal=sinal)
                try:
                    if int(config.get('intervalo_operacoes', 0)) > 0:
                        cooldown_ate = obter_hora_brasilia() + timedelta(seconds=int(config.get('intervalo_operacoes', 0)))
                        log(f"⏱️ Intervalo entre operações iniciado por {int(config.get('intervalo_operacoes', 0))}s.", "INFO")
                except:
                    pass
                return
            elif res < 0:
                perda_total += res
        else:
            # 🛡️ REMOVIDO: Notificação de falha de gale para chat privado
            # log de falha é feito pela função principal
            log(f"❌ Falha ao enviar Gale {g} para [{par}]", "ERRO")
            break
    processar_loss(perda_total, par, f"Gale {config['gales']} (Final)", estrategia_id=estrategia_id, sinal=sinal)
    try:
        if int(config.get('intervalo_operacoes', 0)) > 0:
            cooldown_ate = obter_hora_brasilia() + timedelta(seconds=int(config.get('intervalo_operacoes', 0)))
            log(f"⏱️ Intervalo entre operações iniciado por {int(config.get('intervalo_operacoes', 0))}s.", "INFO")
    except:
        pass



def formatar_sinal_canal(par, dir_op, tf, horario, valor_entrada=None, payout=None, nome_canal=None):
    from datetime import datetime
    agora = obter_hora_brasilia()
    data_fmt = agora.strftime("%d/%m/%Y")
    gales = config.get('gales', 1)
    
    direcao = "🟢 CALL" if dir_op.upper() == "CALL" else "🔴 PUT"
    nome_fmt = nome_canal if nome_canal else "CANAL"
    
    msg = f"""🤖 {nome_fmt}

📅 {data_fmt}
📊 IQ Option | Exnova | Bullex | Avalon | Broker10
♻️ Gerenciamento: {gales} Gale(s)


━━━━━━━━━━━━━━━━━━━
🎯 ENTRADA CONFIRMADA
━━━━━━━━━━━━━━━━━━━


📊 Ativo: {par}
⏱️ Timeframe: M{tf}
🕐 Horário: {horario}
📉 Direção: {direcao}


⏰ Atualizado às {agora.strftime('%H:%M')}"""
    
    return msg

def formatar_resultado_canal(par, tipo_operacao, resultado, gale_nivel=0, nome_canal=None, hora_operacao=None):
    agora = obter_hora_brasilia()
    data_fmt = agora.strftime("%d/%m/%Y")
    
    if resultado == "WIN":
        if gale_nivel == 0:
            resultado_texto = "✅ WIN"
        elif gale_nivel == 1:
            resultado_texto = "✅ WIN G1"
        elif gale_nivel == 2:
            resultado_texto = "✅ WIN G2"
        else:
            resultado_texto = f"✅ WIN G{gale_nivel}"
    elif resultado == "LOSS":
        resultado_texto = "❌ LOSS"
    elif resultado == "DOJI":
        resultado_texto = "⚪️ EMPATE (DOJI)"
    else:
        resultado_texto = "⚠️ RESULTADO INDEFINIDO"
    
    nome_fmt = nome_canal if nome_canal else "CANAL"
    hora_op = hora_operacao if hora_operacao else agora.strftime("%H:%M")
    
    msg = f"""🤖 {nome_fmt}

📅 {data_fmt}
📊 IQ Option | Exnova | Bullex | Avalon | Broker10


━━━━━━━━━━━━━━━━━━━
📊 RESULTADO OFICIAL
━━━━━━━━━━━━━━━━━━━


🎯 Operação: {par} | M1 | {hora_op}
🏆 Resultado: {resultado_texto}


⏰ Atualizado às {agora.strftime('%H:%M')}"""
    
    return msg

def adicionar_resultado_dia(par, tf, direcao, resultado, gale_nivel=0, hora_str=None):
    """Adiciona um resultado à lista do dia"""
    global resultados_dia, data_resultados
    
    agora = obter_hora_brasilia()
    hoje = agora.date()
    
    # Se mudou o dia, reinicia a lista
    if data_resultados != hoje:
        resultados_dia = []
        data_resultados = hoje
        salvar_resultados_dia()
    
    # Usa o horário passado (horário agendado do sinal) ou o atual
    if hora_str is None:
        hora_str = agora.strftime("%H:%M")
    
    # Formato: M1;GBPUSD-OTC;CALL;01:15 ✅²
    direcao_fmt = direcao.upper()
    
    # Emoji superscrito para gale
    superscritos = {1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵'}
    
    if resultado == "WIN":
        if gale_nivel > 0:
            sup = superscritos.get(gale_nivel, str(gale_nivel))
            resultado_fmt = f"✅{sup}"
        else:
            resultado_fmt = "✅"
    elif resultado == "DOJI":
        resultado_fmt = "⚪️"
    else:
        resultado_fmt = "⛔️"
    
    resultado_item = {
        'tf': tf,
        'par': par,
        'direcao': direcao_fmt,
        'hora': hora_str,
        'resultado': resultado_fmt,
        'gale': gale_nivel,
        'timestamp': agora
    }
    
    resultados_dia.append(resultado_item)
    salvar_resultados_dia()
    log(f"📊 Resultado adicionado ao dia: M{tf};{par};{direcao_fmt};{hora_str} {resultado_fmt}", "RESULTADOS")

def salvar_resultados_dia():
    """Salva os resultados do dia em arquivo JSON"""
    global resultados_dia, data_resultados
    try:
        dados = {
            'data': data_resultados.isoformat() if data_resultados else None,
            'resultados': []
        }
        for r in resultados_dia:
            item = {
                'tf': r.get('tf'),
                'par': r.get('par'),
                'direcao': r.get('direcao'),
                'hora': r.get('hora'),
                'resultado': r.get('resultado'),
                'gale': r.get('gale')
            }
            if 'timestamp' in r and r['timestamp']:
                if hasattr(r['timestamp'], 'isoformat'):
                    item['timestamp'] = r['timestamp'].isoformat()
                else:
                    item['timestamp'] = str(r['timestamp'])
            dados['resultados'].append(item)
        
        with open(RESULTADOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log(f"❌ Erro ao salvar resultados: {e}", "ERRO")

def carregar_resultados_dia():
    """Carrega os resultados do dia de arquivo JSON"""
    global resultados_dia, data_resultados
    try:
        if not os.path.exists(RESULTADOS_FILE):
            return
        with open(RESULTADOS_FILE, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        if not dados or not dados.get('resultados'):
            return
        
        data_str = dados.get('data')
        if data_str:
            data_resultados = datetime.strptime(data_str, "%Y-%m-%d").date()
            agora = obter_hora_brasilia()
            if data_resultados == agora.date():
                for r in dados['resultados']:
                    r['timestamp'] = None
                resultados_dia = dados['resultados']
                log(f"📂 Resultados carregados: {len(resultados_dia)} itens", "RESULTADOS")
            else:
                log(f"📂 Resultados são de outro dia ({data_str}), limpando...", "RESULTADOS")
                resultados_dia = []
                data_resultados = agora.date()
                salvar_resultados_dia()
    except Exception as e:
        log(f"❌ Erro ao carregar resultados: {e}", "ERRO")

def formatar_resultados_parciais(nome_canal=None, max_linhas=80):
    """Formata a mensagem de resultados parciais"""
    global resultados_dia, data_resultados
    
    if not resultados_dia:
        return None
    
    agora = obter_hora_brasilia()
    data_fmt = agora.strftime("%d/%m/%Y")
    
    total = len(resultados_dia)
    wins = sum(1 for r in resultados_dia if r['resultado'].startswith('✅'))
    losses = total - wins
    
    wins_g1 = sum(1 for r in resultados_dia if r.get('gale', 0) == 1)
    wins_g2 = sum(1 for r in resultados_dia if r.get('gale', 0) == 2)
    wins_g0 = wins - wins_g1 - wins_g2  # Entrada inicial
    
    linhas = []
    resultados_exibicao = resultados_dia[-max_linhas:] if max_linhas and len(resultados_dia) > max_linhas else resultados_dia
    omitidos = max(0, len(resultados_dia) - len(resultados_exibicao))
    for r in resultados_exibicao:
        linhas.append(f"M{r['tf']} | {r['par']} | {r['direcao']} | {r['hora']} {r['resultado']}")
    
    gales = config.get('gales', 1)
    percentual = (wins / total * 100) if total > 0 else 0
    
    gale_atual = gales
    
    nome_fmt = nome_canal if nome_canal else "CANAL"
    placar = f"{wins}x{losses}"
    
    msg = f"""🤖 {nome_fmt}

📅 {data_fmt}
📊 IQ Option | Exnova | Bullex | Avalon | Broker10
♻️ Gale atual: G{gales}


━━━━━━━━━━━━━━━━━━━
📈 PLACAR DO DIA
━━━━━━━━━━━━━━━━━━━


"""
    if omitidos > 0:
        msg += f"... ({omitidos} resultado(s) mais antigos omitidos)\n\n"
    msg += "\n".join(linhas)
    msg += f"""


🔰 Placar: {placar}
📊 Assertividade: {percentual:.2f}%


✅ Win Inicial: {wins_g0} ({wins_g0/total*100 if total > 0 else 0:.2f}%)
🥇 Win G1: {wins_g1} ({wins_g1/total*100 if total > 0 else 0:.2f}%)
🥈 Win G2: {wins_g2} ({wins_g2/total*100 if total > 0 else 0:.2f}%)


⏰ Atualizado às {agora.strftime('%H:%M')}"""
    
    return msg

def enviar_resultados_parciais_para_canais(forcado=False):
    """Envia o relatório parcial de forma segura e retorna True/False."""
    msg = formatar_resultados_parciais(max_linhas=80)
    if not msg:
        return False
    notificar_canal(msg, 'resultados')
    if forcado:
        log("📊 Relatório parcial enviado manualmente para os canais", "RESULTADOS")
    return True

def thread_verificacao_resultados():
    """Thread que verifica a cada minuto se deve enviar resultados parciais"""
    global thread_resultados_iniciada, ultimo_envio_parcial_hora, ultimo_envio_parcial_data
    
    if thread_resultados_iniciada:
        return
    thread_resultados_iniciada = True
    
    while True:
        try:
            agora = obter_hora_brasilia()
            hora = agora.hour
            minuto = agora.minute
            
            # Verifica se é 23:58 - envia relatório final e reinicia
            if hora == 23 and minuto == 58:
                if enviar_resultados_parciais_para_canais():
                    log("📊 Relatório diário enviado às 23:58", "RESULTADOS")
                # Reinicia para o próximo dia
                global resultados_dia, data_resultados
                resultados_dia = []
                data_resultados = agora.date()
                salvar_resultados_dia()
                ultimo_envio_parcial_hora = None
                ultimo_envio_parcial_data = agora.date()
                time.sleep(120)  # Espera 2 minutos para não enviar novamente
                
            # Verifica se é hora exata (a cada hora) - envia parcial
            elif minuto == 0 and hora > 0:
                if ultimo_envio_parcial_data != agora.date() or ultimo_envio_parcial_hora != hora:
                    if enviar_resultados_parciais_para_canais():
                        log(f"📊 Relatório parcial enviado às {hora:02d}:00", "RESULTADOS")
                    ultimo_envio_parcial_hora = hora
                    ultimo_envio_parcial_data = agora.date()
                time.sleep(60)  # Espera 1 minuto para não enviar novamente
            else:
                time.sleep(30)  # Verifica a cada 30 segundos
                
        except Exception as e:
            log(f"Erro na thread de verificação de resultados: {e}", "ERRO")
            time.sleep(60)

def menu_canais():
    canais = config.get('canais', [])
    texto = "📢 <b>Gerenciar Canais e Grupos</b>\n\n"
    
    if not canais:
        texto += "Nenhum canal cadastrado.\nUse o botão abaixo para adicionar."
    else:
        texto += f"Total: {len(canais)} canal(is) cadastrado(s)\n\n"
        for i, canal in enumerate(canais):
            status = "✅ ATIVO" if canal.get('enabled', True) else "❌ INATIVO"
            tipo = canal.get('tipo', 'FREE')
            nome = canal.get('nome', 'Sem nome')
            texto += f"<b>{i+1}. {nome}</b> ({tipo})\n"
            texto += f"   Status: {status}\n"
            ativos = canal.get('ativos', {})
            sinais = "📊" if ativos.get('sinais', True) else "🚫"
            resultados = "💰" if ativos.get('resultados', True) else "🚫"
            texto += f"   {sinais} Sinais {resultados} Resultados\n\n"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("➕ Adicionar Canal/Grupo", callback_data='add_canal'))
    
    if canais:
        markup.add(types.InlineKeyboardButton("✏️ Editar Canal", callback_data='edit_canal_selecionar'))
        markup.add(types.InlineKeyboardButton("🗑️ Excluir Canal", callback_data='del_canal_selecionar'))
    
    markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu Principal", callback_data='main_menu'))
    
    return texto, markup

def quebrar_mensagem_telegram(mensagem, limite=3900):
    """Divide mensagens longas para evitar erro de tamanho no Telegram."""
    if not mensagem or len(mensagem) <= limite:
        return [mensagem]
    partes = []
    bloco_atual = ""
    for linha in mensagem.splitlines(True):
        if len(bloco_atual) + len(linha) <= limite:
            bloco_atual += linha
        else:
            if bloco_atual:
                partes.append(bloco_atual)
            if len(linha) <= limite:
                bloco_atual = linha
            else:
                # Linha isolada muito longa: quebra bruta
                for i in range(0, len(linha), limite):
                    partes.append(linha[i:i + limite])
                bloco_atual = ""
    if bloco_atual:
        partes.append(bloco_atual)
    return [p for p in partes if p]

def editar_canal_menu(canal_idx):
    canal = config['canais'][canal_idx]
    nome = canal.get('nome', 'Sem nome')
    tipo = canal.get('tipo', 'FREE')
    enabled = canal.get('enabled', True)
    ativos = canal.get('ativos', {'sinais': True, 'gales': True, 'resultados': True, 'avisos': True})
    
    texto = f"✏️ <b>Editar Canal</b>\n\n"
    texto += f"<b>Nome:</b> {nome}\n"
    texto += f"<b>Tipo:</b> {tipo}\n"
    texto += f"<b>Status:</b> {'✅ ATIVO' if enabled else '❌ INATIVO'}\n\n"
    texto += "<b>Conteúdo:</b>\n"
    texto += f"📊 Sinais: {'✅' if ativos.get('sinais') else '❌'}\n"
    texto += f"📈 Gales: {'✅' if ativos.get('gales') else '❌'}\n"
    texto += f"💰 Resultados: {'✅' if ativos.get('resultados') else '❌'}\n"
    texto += f"🔔 Avisos: {'✅' if ativos.get('avisos') else '❌'}"
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📝 Alterar Nome", callback_data=f'edit_canal_nome_{canal_idx}'),
        types.InlineKeyboardButton("🔄 Alterar Tipo", callback_data=f'canal_tipo_{canal_idx}'),
    )
    markup.add(
        types.InlineKeyboardButton("🔄 Ativar/Desativar", callback_data=f'canal_toggle_{canal_idx}')
    )
    markup.add(
        types.InlineKeyboardButton("📊 Sinais", callback_data=f'canal_sinais_{canal_idx}'),
        types.InlineKeyboardButton("💰 Resultados", callback_data=f'canal_resultados_{canal_idx}')
    )
    markup.add(types.InlineKeyboardButton("💾 Salvar e Voltar", callback_data='menu_canais'))
    
    return texto, markup

def enviar_para_canais(mensagem, tipo_conteudo='sinais'):
    canais = config.get('canais', [])
    
    if not canais:
        return
    
    for canal in canais:
        if not canal.get('enabled', True):
            continue
        
        ativos = canal.get('ativos', {})
        if not ativos.get(tipo_conteudo, True):
            continue
        
        chat_id = canal.get('id')
        nome_canal = canal.get('nome', 'CANAL')
        if chat_id:
            try:
                mensagem_formatada = mensagem.replace("🤖 CANAL", f"🤖 {nome_canal}")
                partes = quebrar_mensagem_telegram(mensagem_formatada)
                for parte in partes:
                    bot.send_message(chat_id, parte, parse_mode="HTML")
            except Exception as e:
                log(f"Erro ao enviar para canal {chat_id}: {e}", "ERRO")

def notificar_canal(mensagem, tipo_conteudo='avisos'):
    enviar_para_canais(mensagem, tipo_conteudo)

def menu_principal():
