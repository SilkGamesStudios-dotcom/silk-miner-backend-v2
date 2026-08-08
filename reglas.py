MINERALES = {
    "cobre":       {"prob_drop": 0.50, "rareza": 1},
    "hierro":      {"prob_drop": 0.30, "rareza": 2},
    "plata":       {"prob_drop": 0.15, "rareza": 3},
    "oro_mineral": {"prob_drop": 0.07, "rareza": 4},
    "diamante":    {"prob_drop": 0.03, "rareza": 5},
    "platino":     {"prob_drop": 0.01, "rareza": 6},
}

RECETAS = {
    # --- CPU (el motor del hashrate) ---
    "cpu_basica":      {"slot": "cpu", "requiere": {"cobre": 400}, "buff_hashrate": 0.03, "durabilidad_max": 20},
    "cpu_intermedia":  {"slot": "cpu", "requiere": {"cobre": 250, "hierro": 120}, "buff_hashrate": 0.07, "durabilidad_max": 25},
    "cpu_avanzada":    {"slot": "cpu", "requiere": {"hierro": 180, "plata": 60, "oro_mineral": 15}, "buff_hashrate": 0.12, "durabilidad_max": 30},
    "cpu_epica":       {"slot": "cpu", "requiere": {"plata": 120, "diamante": 10, "oro_mineral": 30}, "buff_hashrate": 0.20, "durabilidad_max": 35},
    "cpu_legendaria":  {"slot": "cpu", "requiere": {"diamante": 25, "platino": 4}, "buff_hashrate": 0.32, "durabilidad_max": 40},

    # --- Refrigeración ---
    "refri_basica":      {"slot": "refrigeracion", "requiere": {"cobre": 300}, "buff_hashrate": 0.02, "durabilidad_max": 25},
    "refri_intermedia":  {"slot": "refrigeracion", "requiere": {"cobre": 180, "hierro": 100}, "buff_hashrate": 0.05, "durabilidad_max": 30},
    "refri_avanzada":    {"slot": "refrigeracion", "requiere": {"hierro": 150, "plata": 50}, "buff_hashrate": 0.09, "durabilidad_max": 35},
    "refri_epica":       {"slot": "refrigeracion", "requiere": {"plata": 100, "diamante": 8}, "buff_hashrate": 0.14, "durabilidad_max": 40},
    "refri_legendaria":  {"slot": "refrigeracion", "requiere": {"diamante": 20, "platino": 3}, "buff_hashrate": 0.22, "durabilidad_max": 45},

    # --- Fuente de poder ---
    "fuente_basica":     {"slot": "fuente_poder", "requiere": {"cobre": 350}, "buff_hashrate": 0.02, "durabilidad_max": 20},
    "fuente_intermedia": {"slot": "fuente_poder", "requiere": {"cobre": 200, "hierro": 90}, "buff_hashrate": 0.05, "durabilidad_max": 25},
    "fuente_avanzada":   {"slot": "fuente_poder", "requiere": {"hierro": 160, "plata": 55}, "buff_hashrate": 0.08, "durabilidad_max": 30},
    "fuente_epica":      {"slot": "fuente_poder", "requiere": {"plata": 110, "diamante": 9}, "buff_hashrate": 0.13, "durabilidad_max": 35},
    "fuente_legendaria": {"slot": "fuente_poder", "requiere": {"diamante": 22, "platino": 3}, "buff_hashrate": 0.21, "durabilidad_max": 40},

    # --- Placa base ---
    "placa_basica":      {"slot": "placa_base", "requiere": {"cobre": 380}, "buff_hashrate": 0.02, "durabilidad_max": 22},
    "placa_intermedia":  {"slot": "placa_base", "requiere": {"cobre": 220, "hierro": 110}, "buff_hashrate": 0.06, "durabilidad_max": 27},
    "placa_avanzada":    {"slot": "placa_base", "requiere": {"hierro": 170, "plata": 58}, "buff_hashrate": 0.10, "durabilidad_max": 32},
    "placa_epica":       {"slot": "placa_base", "requiere": {"plata": 115, "diamante": 10}, "buff_hashrate": 0.16, "durabilidad_max": 37},
    "placa_legendaria":  {"slot": "placa_base", "requiere": {"diamante": 24, "platino": 4}, "buff_hashrate": 0.26, "durabilidad_max": 42},

    # --- Memoria ---
    "memoria_basica":      {"slot": "memoria", "requiere": {"cobre": 320}, "buff_hashrate": 0.02, "durabilidad_max": 20},
    "memoria_intermedia":  {"slot": "memoria", "requiere": {"cobre": 190, "hierro": 95}, "buff_hashrate": 0.04, "durabilidad_max": 25},
    "memoria_avanzada":    {"slot": "memoria", "requiere": {"hierro": 155, "plata": 52}, "buff_hashrate": 0.07, "durabilidad_max": 30},
    "memoria_epica":       {"slot": "memoria", "requiere": {"plata": 105, "diamante": 9}, "buff_hashrate": 0.11, "durabilidad_max": 35},
    "memoria_legendaria":  {"slot": "memoria", "requiere": {"diamante": 21, "platino": 3}, "buff_hashrate": 0.18, "durabilidad_max": 40},

    # --- Antena WiFi ---
    "antena_basica":      {"slot": "antena_wifi", "requiere": {"cobre": 250}, "buff_hashrate": 0.01, "durabilidad_max": 25},
    "antena_intermedia":  {"slot": "antena_wifi", "requiere": {"cobre": 150, "hierro": 70}, "buff_hashrate": 0.03, "durabilidad_max": 30},
    "antena_avanzada":    {"slot": "antena_wifi", "requiere": {"hierro": 120, "plata": 40}, "buff_hashrate": 0.05, "durabilidad_max": 35},
    "antena_epica":       {"slot": "antena_wifi", "requiere": {"plata": 90, "diamante": 6}, "buff_hashrate": 0.08, "durabilidad_max": 40},
    "antena_legendaria":  {"slot": "antena_wifi", "requiere": {"diamante": 16, "platino": 2}, "buff_hashrate": 0.13, "durabilidad_max": 45},

    # --- Chasis ---
    "chasis_basico":      {"slot": "chasis", "requiere": {"cobre": 300}, "buff_hashrate": 0.01, "durabilidad_max": 35},
    "chasis_intermedio":  {"slot": "chasis", "requiere": {"cobre": 180, "hierro": 85}, "buff_hashrate": 0.02, "durabilidad_max": 42},
    "chasis_avanzado":    {"slot": "chasis", "requiere": {"hierro": 140, "plata": 45}, "buff_hashrate": 0.04, "durabilidad_max": 50},
    "chasis_epico":       {"slot": "chasis", "requiere": {"plata": 95, "diamante": 7}, "buff_hashrate": 0.06, "durabilidad_max": 58},
    "chasis_legendario":  {"slot": "chasis", "requiere": {"diamante": 18, "platino": 3}, "buff_hashrate": 0.10, "durabilidad_max": 65},

    # --- Firmware ---
    "firmware_basico":     {"slot": "firmware", "requiere": {"cobre": 450, "hierro": 50}, "buff_hashrate": 0.04, "durabilidad_max": 15},
    "firmware_intermedio": {"slot": "firmware", "requiere": {"hierro": 200, "plata": 40}, "buff_hashrate": 0.08, "durabilidad_max": 18},
    "firmware_avanzado":   {"slot": "firmware", "requiere": {"plata": 130, "oro_mineral": 25}, "buff_hashrate": 0.14, "durabilidad_max": 22},
    "firmware_epico":      {"slot": "firmware", "requiere": {"oro_mineral": 45, "diamante": 12}, "buff_hashrate": 0.22, "durabilidad_max": 26},
    "firmware_legendario": {"slot": "firmware", "requiere": {"diamante": 28, "platino": 5}, "buff_hashrate": 0.35, "durabilidad_max": 30},

    # --- Amuleto (slot especial) ---
    "amuleto_basico":     {"slot": "amuleto", "requiere": {"plata": 30}, "buff_hashrate": 0.01, "durabilidad_max": 50},
    "amuleto_intermedio": {"slot": "amuleto", "requiere": {"plata": 60, "oro_mineral": 10}, "buff_hashrate": 0.02, "durabilidad_max": 55},
    "amuleto_avanzado":   {"slot": "amuleto", "requiere": {"oro_mineral": 30, "diamante": 5}, "buff_hashrate": 0.03, "durabilidad_max": 60},
    "amuleto_epico":      {"slot": "amuleto", "requiere": {"diamante": 15, "platino": 2}, "buff_hashrate": 0.05, "durabilidad_max": 65},
    "amuleto_legendario": {"slot": "amuleto", "requiere": {"platino": 6}, "buff_hashrate": 0.08, "durabilidad_max": 70},
}

# Los 9 slots de equipo por rig
SLOTS_RIG = ["cpu", "refrigeracion", "fuente_poder", "placa_base", "memoria", "antena_wifi", "chasis", "firmware", "amuleto"]

# Bonus extra si el rig tiene los 9 slots equipados (cualquier tier) — premia armar el rig completo
BONUS_RIG_COMPLETO = 0.25

NIVELES = [
    {"nombre": "Novato",   "oro_minado_min": 0},
    {"nombre": "Aprendiz", "oro_minado_min": 5_000_000},
    {"nombre": "Minero",   "oro_minado_min": 25_000_000},
    {"nombre": "Veterano", "oro_minado_min": 100_000_000},
    {"nombre": "Experto",  "oro_minado_min": 500_000_000},
    {"nombre": "Maestro",  "oro_minado_min": 2_000_000_000},
    {"nombre": "Leyenda",  "oro_minado_min": 10_000_000_000},
]

# ---------- NIVELES POR DISPOSITIVO (experiencia individual de cada ESP32/celular) ----------
# Cada share exitoso suma XP al dispositivo que lo mandó. Al subir de nivel, ese
# dispositivo produce más Oro (buff_oro se suma al resto de buffs en /submit) — es
# la forma en que "sube de nivel" un minero, tipo MMORPG: no cambia el hashrate físico
# real (eso lo manda el hardware), pero sí cuánto Oro vale cada prueba que resuelve.
#
# Va de Nivel 1 a Nivel 10000 (NIVEL_MAX_DISPOSITIVO). La curva de XP se arma por
# tramos, cada uno más lento que el anterior — a propósito no es gratis subir:
#   Niveles 1-10:      igual que el sistema original (rápido, ~35 días 1 solo device 24/7).
#   Niveles 11-100:    +3% de XP por nivel — ronda el año de juego real para llegar.
#   Niveles 101-1000:  +0.3% de XP por nivel — años de juego, ya requiere varios devices.
#   Niveles 1001-10000: +0.05% de XP por nivel — end-game: en la práctica solo se
#                       acerca alguien combinando VARIOS dispositivos + VIP + los
#                       buffs de XP de BUFFS_XP_ORO (se compran EXCLUSIVAMENTE con
#                       Oro farmeado, no con tickets ni USDT — así el nivel más alto
#                       siempre se gana jugando/minando, nunca se compra directo).
# El buff de Oro también crece por tramos, con techo duro en +160% para que nunca
# se vuelva absurdo pagar por share, ni siquiera en Nivel 10000.
XP_POR_SHARE = 1.0
NIVEL_MAX_DISPOSITIVO = 10000


def _generar_niveles_dispositivo():
    xp = [0, 200, 600, 1500, 3500, 7500, 15000, 30000, 60000, 120000]           # niveles 1-10
    buff = [0.00, 0.01, 0.02, 0.04, 0.06, 0.09, 0.12, 0.16, 0.20, 0.25]          # niveles 1-10

    for _ in range(11, 101):                                                     # niveles 11-100
        xp.append(round(xp[-1] * 1.03))
        buff.append(round(buff[-1] + 0.005, 5))
    for _ in range(101, 1001):                                                   # niveles 101-1000
        xp.append(round(xp[-1] * 1.003))
        buff.append(round(buff[-1] + 0.0005, 5))
    for _ in range(1001, NIVEL_MAX_DISPOSITIVO + 1):                             # niveles 1001-10000
        xp.append(round(xp[-1] * 1.0005))
        buff.append(round(min(buff[-1] + 0.00005, 1.60), 5))

    return [
        {"nombre": f"Nivel {n}", "xp_min": xp[n - 1], "buff_oro": buff[n - 1]}
        for n in range(1, NIVEL_MAX_DISPOSITIVO + 1)
    ]


# Se genera UNA sola vez al importar el módulo (10.000 filas, trivial en memoria) y
# se busca por bisección en cada share — nunca se recalcula ni se recorre en loop.
NIVELES_DISPOSITIVO = _generar_niveles_dispositivo()
_NIVELES_DISPOSITIVO_XP_MIN = [n["xp_min"] for n in NIVELES_DISPOSITIVO]


def calcular_nivel_dispositivo(experiencia):
    import bisect
    i = bisect.bisect_right(_NIVELES_DISPOSITIVO_XP_MIN, experiencia) - 1
    i = max(0, min(i, len(NIVELES_DISPOSITIVO) - 1))
    return NIVELES_DISPOSITIVO[i]


def siguiente_nivel_dispositivo(experiencia):
    import bisect
    i = bisect.bisect_right(_NIVELES_DISPOSITIVO_XP_MIN, experiencia)
    if i >= len(NIVELES_DISPOSITIVO):
        return None  # ya está en Nivel 10000, el tope
    return NIVELES_DISPOSITIVO[i]


# ---------- BUFFS DE EXPERIENCIA (se compran EXCLUSIVAMENTE con Oro — nunca con tickets ni USDT) ----------
# Multiplican la XP que gana UN dispositivo específico por share mientras estén activos.
# Es la única forma de acelerar la subida de nivel más allá de jugar/minar — pensado para
# quien ya farmeó bastante Oro y lo quiere reinvertir en progreso, no para comprar nivel
# directo con dinero real. Se aplican a un rig (mac) elegido por el usuario a la vez.
BUFFS_XP_ORO = {
    "xp_x2_24h": {"nombre": "Doble Experiencia — 24 horas",  "multiplicador": 2.0, "duracion_horas": 24,  "costo_oro": 50_000},
    "xp_x2_72h": {"nombre": "Doble Experiencia — 3 días",    "multiplicador": 2.0, "duracion_horas": 72,  "costo_oro": 130_000},
    "xp_x3_24h": {"nombre": "Triple Experiencia — 24 horas", "multiplicador": 3.0, "duracion_horas": 24,  "costo_oro": 90_000},
    "xp_x3_72h": {"nombre": "Triple Experiencia — 3 días",   "multiplicador": 3.0, "duracion_horas": 72,  "costo_oro": 230_000},
}


# ---------- VIP PREMIUM (suscripción mensual por rig completo, pago manual en USDT) ----------
VIP_PRECIO_USDT_MES = 0.60
VIP_DIAS_POR_PAGO = 30
VIP_BUFF_ORO = 0.03       # +3% Oro adicional por share, si el rig está completo y con VIP activo
VIP_BUFF_DROP = 0.02      # +2% probabilidad extra de drop de minerales/piezas raras

# ---------- CERTIFICADOS (activos de prestigio, se ganan al alcanzar ciertos niveles de dispositivo) ----------
# Cada certificado se otorga UNA vez por dispositivo (no se repite al volver a pasar por ese nivel).
# Se pueden equipar a un rig para sumar su buff_oro, vender en el mercado oficial (con comisión) o
# tradear directo entre usuarios acordando el pago en Oro.
CERTIFICADOS = {
    "certificado_bronce": {"nombre": "Certificado de Bronce", "nivel_dispositivo_requerido": "Nivel 4",  "buff_oro": 0.01},
    "certificado_plata":  {"nombre": "Certificado de Plata",  "nivel_dispositivo_requerido": "Nivel 7",  "buff_oro": 0.02},
    "certificado_oro":    {"nombre": "Certificado de Oro",    "nivel_dispositivo_requerido": "Nivel 10", "buff_oro": 0.04},
}

# Al vender un certificado en el mercado oficial, esta comisión se descuenta en Oro del monto
# que recibe el vendedor (queda "quemada", no va a nadie — mantiene la economía interna equilibrada).
COMISION_MERCADO_CERTIFICADOS = 0.05  # 5%

# ---------- LOGROS (medallas visibles, se otorgan solas al cumplir la condición) ----------
LOGROS = {
    "minero_novato": {"nombre": "Minero Novato",   "descripcion": "Llegar a 1.000 Oro histórico",        "campo": "oro_historico", "valor": 1_000},
    "minero_elite":  {"nombre": "Minero Élite",    "descripcion": "Llegar a 1.000.000 Oro histórico",    "campo": "oro_historico", "valor": 1_000_000},
    "coleccionista": {"nombre": "Coleccionista",   "descripcion": "Conseguir 3 certificados",             "campo": "certificados",  "valor": 3},
    "suscriptor_vip":{"nombre": "Suscriptor Fiel", "descripcion": "Activar VIP en algún rig",             "campo": "vip",           "valor": 1},
}

# ---------- MISIONES DIARIAS (se resetean solas cada día, según shares minados hoy) ----------
# ---------- RACHA DE LOGIN DIARIO (ciclo de 7 días, se reinicia si se salta un día) ----------
# Cada día que el usuario reclama, avanza un día en el ciclo. Si se salta un día entero sin
# reclamar, el ciclo vuelve al día 1 — no hay perdón por inactividad, así se mantiene el valor
# de la racha. Cada día del ciclo da Oro o Tickets (nunca los dos), y el día 7 es el más grande
# a propósito, como cierre del ciclo antes de reiniciar.
RACHA_RECOMPENSAS = [
    {"dia": 1, "oro": 300,  "tickets": 0},
    {"dia": 2, "oro": 600,  "tickets": 0},
    {"dia": 3, "oro": 0,    "tickets": 3},
    {"dia": 4, "oro": 1200, "tickets": 0},
    {"dia": 5, "oro": 0,    "tickets": 6},
    {"dia": 6, "oro": 2500, "tickets": 0},
    {"dia": 7, "oro": 0,    "tickets": 15},
]

MISIONES_DIARIAS = [
    {"id": "mision_5",  "nombre": "Minar 5 shares hoy",  "shares_requeridos": 5,  "recompensa_oro": 200},
    {"id": "mision_20", "nombre": "Minar 20 shares hoy", "shares_requeridos": 20, "recompensa_oro": 1000},
]

# ---------- MISIONES SEMANALES (se resetean solas cada 7 días, cubren TODO el ecosistema) ----------
# A diferencia de las diarias (solo shares), estas empujan a usar la plataforma entera: jugar
# Arcade, tradear en el Mercado, comprar electricidad (con USDT o con Tickets), craftear,
# completar encuestas y abrir rigs nuevos. Las recompensas son Oro y Tickets — ambos se pueden
# vender en el Mercado a otros jugadores, así que toda misión termina alimentando el trade.
#
# A propósito NO son fáciles — "reto equilibrado" quiere decir que algunas se completan en un
# par de días si jugás fuerte, y otras están pensadas para toda la semana. Nada se regala: el
# usuario que no toca la plataforma en toda la semana simplemente no cobra nada, y eso es
# correcto — no hay premio por no jugar.
#
# "metrica" es la clave del contador semanal (ver Usuario.contadores_semana en models.py) que
# se compara contra "objetivo" para saber si la misión está completa.
MISIONES_SEMANALES = [
    # --- Arcade (jugar) — 3 escalones de dificultad sobre el mismo contador ---
    {"id": "sem_arcade_20",  "nombre": "Jugador de la semana",  "descripcion": "Jugá 20 partidas de Silk Arcade (cualquier combinación de juegos).",
     "metrica": "partidas_jugadas", "objetivo": 20,  "recompensa_oro": 6_000,   "recompensa_tickets": 8},
    {"id": "sem_arcade_150", "nombre": "Maratón de Arcade",     "descripcion": "Jugá 150 partidas de Silk Arcade esta semana.",
     "metrica": "partidas_jugadas", "objetivo": 150, "recompensa_oro": 45_000,  "recompensa_tickets": 60},
    {"id": "sem_arcade_500", "nombre": "Leyenda del Arcade",    "descripcion": "Jugá 500 partidas de Silk Arcade esta semana — el reto grande.",
     "metrica": "partidas_jugadas", "objetivo": 500, "recompensa_oro": 160_000, "recompensa_tickets": 220},

    # --- Mercado (tradear) ---
    {"id": "sem_mercado_comprar_5",  "nombre": "Comprador activo",  "descripcion": "Comprá 5 órdenes publicadas por otros jugadores en el Mercado.",
     "metrica": "ordenes_compradas", "objetivo": 5,  "recompensa_oro": 8_000,  "recompensa_tickets": 10},
    {"id": "sem_mercado_comprar_20", "nombre": "Trader de la semana", "descripcion": "Comprá 20 órdenes en el Mercado esta semana.",
     "metrica": "ordenes_compradas", "objetivo": 20, "recompensa_oro": 32_000, "recompensa_tickets": 40},
    {"id": "sem_mercado_publicar_10", "nombre": "Vendedor activo", "descripcion": "Publicá 10 órdenes de venta en el Mercado (minerales, tickets, piezas o certificados).",
     "metrica": "ordenes_publicadas", "objetivo": 10, "recompensa_oro": 9_000, "recompensa_tickets": 12},
    {"id": "sem_mercado_volumen_50k", "nombre": "Movés la economía", "descripcion": "Acumulá 50.000 de Oro en volumen tradeado en el Mercado (comprando y/o vendiendo).",
     "metrica": "volumen_oro_tradeado", "objetivo": 50_000, "recompensa_oro": 18_000, "recompensa_tickets": 25},

    # --- Electricidad (USDT y Tickets — ambos caminos cuentan, y a propósito ambos tienen misión) ---
    {"id": "sem_energia_usdt_1", "nombre": "Inversor de la semana", "descripcion": "Comprá al menos 1 paquete de electricidad pagado en USDT.",
     "metrica": "electricidad_compras_usdt", "objetivo": 1, "recompensa_oro": 7_000, "recompensa_tickets": 15},
    {"id": "sem_energia_tickets_3", "nombre": "Autosuficiente", "descripcion": "Canjeá electricidad con Tickets 3 veces esta semana (tienda de canje).",
     "metrica": "electricidad_compras_tickets", "objetivo": 3, "recompensa_oro": 5_000, "recompensa_tickets": 0},

    # --- Crafteo ---
    {"id": "sem_crafteo_5", "nombre": "Manos a la obra", "descripcion": "Crafteá 5 piezas para tus rigs.",
     "metrica": "piezas_crafteadas", "objetivo": 5, "recompensa_oro": 7_500, "recompensa_tickets": 10},

    # --- Encuestas (CPX — electricidad gratis, la plataforma también gana por esto) ---
    {"id": "sem_encuestas_3", "nombre": "Explorador de ofertas", "descripcion": "Completá 3 encuestas de CPX Research.",
     "metrica": "encuestas_completadas", "objetivo": 3, "recompensa_oro": 12_000, "recompensa_tickets": 20},

    # --- Expansión (abrir hardware nuevo) ---
    {"id": "sem_rig_nuevo_1", "nombre": "Expansión", "descripcion": "Pagá y abrí un rig nuevo esta semana (2do en adelante).",
     "metrica": "rigs_comprados", "objetivo": 1, "recompensa_oro": 25_000, "recompensa_tickets": 50},
]


# Dificultad FIJA por dispositivo — no cambia con la cantidad de usuarios.
# Calibrada para que un ESP32 individual encuentre un share cada ~25s.
DIFICULTAD_DISPOSITIVO = 4  # ajustar tras medir hashrate real del ESP32

# Recompensa por share — esta es la que se ajusta según el volumen total de la red.
# Empieza en un valor base y se recalcula semanalmente (ver ajustar_recompensa_por_share).
RECOMPENSA_POR_SHARE = 1000.0  # placeholder inicial, se recalcula con el cron semanal

META_ORO_SEMANAL = 50_000_000 * 24 * 7  # meta total de emisión de la red por semana

COSTO_DIARIO_USDT = 0.05
ROTACION_JOB_SEGUNDOS = 25  # alineado a que un share tarde ~25s en promedio (ESP32 genérico / celular)

# ---------- MINEROS OFICIALES SILK MINER v1 (roadmap — todavía no hay hardware real vendido) ----------
# Decisión de diseño para cuando exista el hardware: el dispositivo oficial resuelve un hash
# cada ~18s en vez de ~25s. IMPORTANTE — cómo se implementa esto CORRECTAMENTE cuando llegue el
# momento (para que sea trabajo real, no una promesa vacía ni un multiplicador de recompensa
# disfrazado):
#   NO se logra bajando la dificultad (cumple_dificultad cuenta ceros hexadecimales enteros —
#   cada paso de dificultad multiplica x16 la dureza, es un salto demasiado grosero para afinar
#   una reducción del 28% con precisión).
#   SÍ se logra dándole a los dispositivos oficiales su PROPIO ciclo de rotación de job (su
#   propio prev_hash, misma dificultad que todos), rotando cada 18s en vez de cada 25s — el
#   mismo mecanismo que ROTACION_JOB_SEGUNDOS, pero en un carril aparte solo para el modelo
#   oficial. Sigue siendo hash real, SHA-256 real, el chip real resolviendo — solo que su
#   ventana de tiempo para intentarlo es más corta, así que si el chip ya resuelve cómodo
#   dentro de 25s (como hoy), resolver en 18s es 100% verificable y nunca una simulación.
# Esto requiere identificar el dispositivo como oficial en el registro (campo de modelo en Rig)
# antes de servirle un job en este carril — no implementado todavía porque el hardware no existe
# aún; queda documentado acá para cuando se construya el endpoint real.
SILK_MINER_OFICIAL_ROTACION_SEGUNDOS = 18

# Carril intermedio: un ESP32 genérico armado por un reseller, pero corriendo firmware con
# LICENCIA paga (activada, atada a su MAC) — tiene prioridad sobre un dispositivo sin licencia,
# pero no tanta como el hardware oficial (que además vino calibrado y probado en fábrica). Así
# el orden de incentivos queda: sin licencia (gratis, 25s) < licenciado (paga la licencia +
# cuota, 21s) < Silk Miner oficial (compra el hardware, incluye licencia, 18s) — cada escalón
# se paga con algo real y da algo real a cambio.
LICENCIADO_GENERICO_ROTACION_SEGUNDOS = 21

# ---------- CUOTA DE MANTENIMIENTO MENSUAL (roadmap — para TODO dispositivo con licencia activa) ----------
# Tanto un Silk Miner oficial como un ESP32 de un reseller con licencia paga tienen que sostener
# una cuota mensual para mantener su carril de prioridad (18s o 21s). Se paga en Oro o en
# Tickets — NUNCA en USDT, a propósito: Oro y Tickets son saldo interno, así que el cobro es
# 100% automático (se descuenta solo, sin que ningún admin tenga que aprobar nada a mano cada
# mes). Esto es intencional: ya vimos que una cuota mensual en USDT significaría aprobar a mano
# ~12 pagos al año por cada dispositivo — inviable a escala. En Oro/Tickets no hay ese problema,
# y de paso le mete más movimiento real a esas dos monedas (que es justo lo que se buscaba).
#
# Precio calculado sobre el ancla de ESFUERZO real del juego (no el ancla de USDT que usa la
# Tienda): jugar Arcade da Oro y Tickets de la MISMA jugada — 8 niveles alcanzados dan 4.000 Oro
# Y 1 Ticket a la vez (ver MINIJUEGOS_ORO_POR_NIVEL y MINIJUEGOS_NIVELES_POR_TICKET). Esa es la
# tasa real de "cuánto cuesta ganar" cada moneda jugando: 1 Ticket ~ 4.000 Oro de esfuerzo. La
# cuota en Tickets se redondea siempre HACIA ARRIBA sobre esa equivalencia — igual que con USDT,
# pagar con el recurso más escaso nunca sale más barato en esfuerzo real.
CUOTA_MANTENIMIENTO_ORO_MENSUAL = 15_000
CUOTA_MANTENIMIENTO_TICKETS_MENSUAL = 4  # 15.000 / 4.000 = 3.75 -> redondeado arriba

# Interruptor por dispositivo: "auto" descuenta la cuota sola cada mes (de Oro primero, o de
# Tickets si el jugador lo configuró así) apenas se cumple el mes, sin que el jugador haga nada.
# "manual" espera a que el jugador la pague él mismo desde su panel.
# Si la cuota vence y NO se pagó (ni en automático por falta de saldo, ni a mano): el dispositivo
# NO se bloquea ni deja de minar — solo pierde el carril de prioridad y vuelve al ritmo estándar
# de 25s hasta que se pague de nuevo. La activación anti-clonación de la licencia (MAC atada) es
# perpetua y no se toca — lo único que depende de la cuota es la velocidad extra.
CUOTA_MANTENIMIENTO_MODOS = ["auto", "manual"]

# ---------- ELECTRICIDAD GRATIS POR ENCUESTA (CPX Research) ----------
# Al completar una encuesta/oferta en CPX, el usuario recibe 1 día de electricidad
# gratis para UN SOLO dispositivo (ESP32, celular o PC — todos minan igual, ver Rig
# en models.py). A propósito es poco: así el usuario vuelve a completar encuestas
# seguido para mantener sus dispositivos con luz, en vez de cubrirse por semanas
# de una sola vez. Comisión típica por encuesta (~$0.30-0.50) vs costo real de
# electricidad ($0.01/día/dispositivo) — la repetición es lo que genera ingresos reales.
ENCUESTA_DIAS_ELECTRICIDAD = 1       # días de electricidad que otorga cada encuesta completada
ENCUESTA_MAX_ESP32 = 1               # a cuántos dispositivos se les acredita por encuesta (el/los que menos días tengan)

# Paquetes de electricidad prepagada (precio POR CADA ESP32 que tenga el usuario)
# Escalados x5 junto con COSTO_DIARIO_USDT (0.01 -> 0.05), manteniendo el mismo % de descuento por volumen.
PAQUETES_ELECTRICIDAD = {
    "10_dias": {"dias": 10, "precio_usdt_por_esp32": 0.50},
    "30_dias": {"dias": 30, "precio_usdt_por_esp32": 1.35},   # ~10% descuento
    "90_dias": {"dias": 90, "precio_usdt_por_esp32": 3.75},   # ~17% descuento
}


def calcular_nivel(oro_historico):
    nivel_actual = NIVELES[0]
    for nivel in NIVELES:
        if oro_historico >= nivel["oro_minado_min"]:
            nivel_actual = nivel
    return nivel_actual


# ---------- TOPE SEMANAL: tickets solo alcanzan para sostener 1 rig (regla de oro) ----------
# Aunque el usuario acumule miles de tickets jugando o comprándolos en el Mercado, el canje de
# tickets->electricidad tiene techo semanal. 42 = 6 dispositivos x 7 días (1 rig completo, 1 semana).
# Esto NO limita cuántos tickets puede tener o vender — solo cuánta electricidad puede "comprar" con
# ellos por semana. Para un 2do rig en adelante, el único camino es USDT, Encuesta, u Oro+Tickets
# (ver PRECIOS_RIG) — el canje de la tienda nunca abre hardware nuevo.
ELECTRICIDAD_TICKETS_DIAS_MAX_SEMANA = 42

# ---------- PRECIOS PARA ABRIR UN RIG NUEVO (2do en adelante — el 1ro siempre es gratis) ----------
# "tickets" queda FIJO en todas las filas (según se definió) — nunca escala con el número de rig.
# "oro" y "precio_usdt" sí escalan. El ancla real usada acá es la tasa de la tienda de canje
# (TIENDA_CANJE: 6 tickets = 1 día de electricidad de 1 dispositivo = COSTO_DIARIO_USDT), así que
# 500 tickets equivalen groso modo a ~83 días de electricidad de 1 equipo si se canjearan ahí —
# un valor de esfuerzo consistente con pedirle bastante más que "unos días de luz" para abrir hardware nuevo.
PRECIOS_RIG = {
    2: {"precio_usdt": 0.20, "tickets": 500, "oro": 3000},
    3: {"precio_usdt": 0.35, "tickets": 500, "oro": 6000},
    4: {"precio_usdt": 0.55, "tickets": 500, "oro": 10000},
}
# Rig 5 en adelante se calcula en código (ver precio_rig() más abajo) sobre la última fila cargada.
PRECIOS_RIG_INCREMENTO_USDT_POR_RIG = 0.25
PRECIOS_RIG_INCREMENTO_ORO_POR_RIG = 5000


def precio_rig(numero_rig: int) -> dict:
    """Precio (USDT, tickets, oro) para abrir el rig #numero_rig. Rig 1 no tiene precio (gratis)."""
    if numero_rig in PRECIOS_RIG:
        return PRECIOS_RIG[numero_rig]
    ultimo_definido = max(PRECIOS_RIG.keys())
    base = PRECIOS_RIG[ultimo_definido]
    pasos_extra = numero_rig - ultimo_definido
    return {
        "precio_usdt": round(base["precio_usdt"] + PRECIOS_RIG_INCREMENTO_USDT_POR_RIG * pasos_extra, 2),
        "tickets": base["tickets"],  # fijo siempre
        "oro": base["oro"] + PRECIOS_RIG_INCREMENTO_ORO_POR_RIG * pasos_extra,
    }


# ---------- CUPÓN DE SUBSIDIO (fidelización a quien paga completo en USDT) ----------
# Al aprobarse una orden 100% USDT (electricidad o rig nuevo) SIN cupón aplicado, se le genera
# automáticamente un cupón para su próxima recarga. Se aplica solo, sin código, y expira si no
# se usa a tiempo (para que no quede dando vueltas indefinidamente en cuentas inactivas).
CUPON_SUBSIDIO_PORCENTAJE = 10
CUPON_SUBSIDIO_DIAS_VALIDEZ = 30
CUPON_SUBSIDIO_MOTIVO = "Pagaste tu recarga completa la última vez"


# ---------- MINI-JUEGOS (Silk Arcade) ----------
# Juegos habilitados hoy. Todos comparten el mismo endpoint de registro de partida
# y la misma economía — para sumar uno nuevo solo hace falta agregarlo acá y
# programar su canvas en el frontend, el backend no distingue mecánica interna.
JUEGOS_DISPONIBLES = {
    "tetris":     {"nombre": "Tetris",              "emoji": "🧱", "descripcion": "El clásico de siempre — armá líneas completas antes de que se acumulen las piezas. La velocidad de caída sube con cada nivel."},
    "asteroides": {"nombre": "Asteroides",           "emoji": "🚀", "descripcion": "Esquivá y destruí asteroides con tu nave. Cada nivel suma más rocas y más velocidad."},
    "cazaminerales": {"nombre": "Cazador de Minerales", "emoji": "⛏️", "descripcion": "Recorré el tablero juntando cobre, hierro y plata mientras esquivás a los virus que te persiguen — el ritmo de Silk Miner, en modo arcade."},
    "invasion":   {"nombre": "Invasión de las Cuevas", "emoji": "👾", "descripcion": "Las mismas criaturas de tus cuevas bajan en oleadas — defendé tu base. Más oleadas y más rápido en cada nivel."},
}

# Oro que se entrega por nivel alcanzado en cualquier mini-juego (nivel_alcanzado * este valor)
MINIJUEGOS_ORO_POR_NIVEL = 500

# Cada cuántos niveles alcanzados se entrega 1 ticket (moneda de logro, para la tienda de canje / mercado).
# Antes era 4 — se subió a 8 (mitad de tickets por el mismo juego) a propósito: el Oro por nivel
# no cambia, pero el ticket tiene que sentirse ganado. Esto también protege el ancla de precios que
# usa Tickets como medio de pago (ver LICENCIA_SOFTWARE_* más abajo): si tickets salieran demasiado
# fácil, pagar con tiempo jugado terminaría siendo más barato que pagar con USDT, y nadie pagaría.
MINIJUEGOS_NIVELES_POR_TICKET = 8

# Ya no hay tope de partidas por día. En cambio, cada juego individual entra en un
# cooldown corto si insistís sin rotar a otro — esto empuja a rotar entre los 4 juegos
# (más impresiones publicitarias reales) en vez de limitar cuánto podés jugar en total.
# Índice = cantidad de partidas seguidas jugadas en ESE juego sin cambiar a otro (0-based).
# Ej: partida 1 y 2 en el mismo juego -> sin espera. Partida 3 -> 30s. Partida 4+ -> 60s (tope).
COOLDOWN_MINIJUEGO_ESCALADA_SEGUNDOS = [0, 0, 30, 60]

# Anti-bot simple: si el cliente reporta un nivel alto en muy poco tiempo, es sospechoso.
# El backend exige que duracion_segundos >= nivel_alcanzado * este valor, o rechaza la partida.
MINIJUEGOS_SEGUNDOS_MIN_POR_NIVEL = 8

# ---------- TIENDA DE CANJE (Gift Shop — se paga solo con Tickets) ----------
# REGLA GENERAL DE PRECIOS (aplica a todo lo que tenga un equivalente directo en USDT en
# la plataforma): el precio en Tickets siempre es el equivalente en USDT convertido al
# ancla real de la economía (1 ticket ≈ $0.0083, ver LICENCIA_SOFTWARE_* más abajo) MÁS
# UN 35% extra. Nunca 1:1. Así pagar con tiempo jugado nunca sale más barato que pagar con
# USDT — el camino en tickets siempre cuesta más en términos reales, aunque no cueste
# dinero. Esto no aplica a piezas/certificados de la tienda: esos no tienen un precio en
# USDT en la plataforma (se ganan farmeando o crafteando), así que no hay equivalente
# contra el cual calcular el +35%.
TIENDA_CANJE = {
    "canje_electricidad_1": {
        "nombre": "1 día de electricidad (1 dispositivo)",
        "costo_tickets": 8,   # equivalente USDT $0.05 -> ancla 6 tickets, +35% = 8.1 -> 8
        "tipo": "electricidad",
        "dias": 1,
    },
    "canje_electricidad_3": {
        "nombre": "3 días de electricidad (1 dispositivo)",
        "costo_tickets": 24,  # equivalente USDT $0.15 -> ancla 18 tickets, +35% = 24.3 -> 24
        "tipo": "electricidad",
        "dias": 3,
    },
    "canje_pieza_avanzada_random": {
        "nombre": "Pieza Avanzada al azar (sin craftear)",
        "costo_tickets": 30,
        "tipo": "pieza_random",
        "tier": "avanzada",
    },
    "canje_pieza_epica_random": {
        "nombre": "Pieza Épica al azar (sin craftear)",
        "costo_tickets": 70,
        "tipo": "pieza_random",
        "tier": "epica",
    },
    "canje_certificado_bronce": {
        "nombre": "Certificado de Bronce",
        "costo_tickets": 20,
        "tipo": "certificado",
        "certificado_id": "certificado_bronce",
    },
    "canje_certificado_plata": {
        "nombre": "Certificado de Plata",
        "costo_tickets": 45,
        "tipo": "certificado",
        "certificado_id": "certificado_plata",
    },
}

# ---------- LICENCIA DE SOFTWARE (roadmap — sistema anti-clonación, ver white paper de licencias) ----------
# PRÓXIMAMENTE: todavía no hay endpoints ni tabla para esto, son solo las constantes de precio
# ya definidas para cuando se implemente. Ancla real del valor de 1 ticket: $0.05 USDT / 6 =
# $0.0083 (el mismo peg que usa toda la economía de Tickets, aunque el precio EN LA TIENDA ya
# incluya su propio +35%, ver TIENDA_CANJE). A ese ancla, la licencia saldría en 480 tickets
# 1:1 — a propósito NO se deja así: lleva el mismo +35% que toda compra con Tickets, para que
# pagar con tiempo jugado nunca salga más barato que pagar con USDT.
LICENCIA_SOFTWARE_PRECIO_USDT = 4.0
LICENCIA_SOFTWARE_PRECIO_TICKETS = 650  # ancla (480) + 35%, redondeado
