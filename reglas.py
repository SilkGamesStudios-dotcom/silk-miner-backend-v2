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
# dispositivo produce más Oro (buff_oro se suma al resto de buffs en /submit).
XP_POR_SHARE = 1.0

NIVELES_DISPOSITIVO = [
    {"nombre": "Nivel 1", "xp_min": 0,     "buff_oro": 0.00},
    {"nombre": "Nivel 2", "xp_min": 200,   "buff_oro": 0.01},
    {"nombre": "Nivel 3", "xp_min": 600,   "buff_oro": 0.02},
    {"nombre": "Nivel 4", "xp_min": 1500,  "buff_oro": 0.04},
    {"nombre": "Nivel 5", "xp_min": 3500,  "buff_oro": 0.06},
    {"nombre": "Nivel 6", "xp_min": 7500,  "buff_oro": 0.09},
    {"nombre": "Nivel 7", "xp_min": 15000, "buff_oro": 0.12},
    {"nombre": "Nivel 8", "xp_min": 30000, "buff_oro": 0.16},
    {"nombre": "Nivel 9", "xp_min": 60000, "buff_oro": 0.20},
    {"nombre": "Nivel 10","xp_min": 120000,"buff_oro": 0.25},
]


def calcular_nivel_dispositivo(experiencia):
    nivel_actual = NIVELES_DISPOSITIVO[0]
    for nivel in NIVELES_DISPOSITIVO:
        if experiencia >= nivel["xp_min"]:
            nivel_actual = nivel
    return nivel_actual


def siguiente_nivel_dispositivo(experiencia):
    for nivel in NIVELES_DISPOSITIVO:
        if experiencia < nivel["xp_min"]:
            return nivel
    return None  # ya está en el nivel máximo


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

# ---------- RACHA DE LOGIN DIARIO (recompensa por entrar seguido, ciclo de 7 días) ----------
# Se reclama una vez al día. Si el usuario reclama en días calendario consecutivos, avanza al
# siguiente día de la racha; si se salta un día, vuelve a empezar en el día 1. Al completar el
# día 7 y reclamar, el siguiente reclamo vuelve a arrancar en el día 1.
RECOMPENSAS_RACHA = [
    {"dia": 1, "oro": 100,  "tickets": 0},
    {"dia": 2, "oro": 200,  "tickets": 0},
    {"dia": 3, "oro": 0,    "tickets": 5},
    {"dia": 4, "oro": 400,  "tickets": 0},
    {"dia": 5, "oro": 0,    "tickets": 10},
    {"dia": 6, "oro": 800,  "tickets": 0},
    {"dia": 7, "oro": 2000, "tickets": 15},
]

# ---------- MISIONES DIARIAS (se resetean solas cada día, según shares minados hoy) ----------
MISIONES_DIARIAS = [
    {"id": "mision_5",  "nombre": "Minar 5 shares hoy",  "shares_requeridos": 5,  "recompensa_oro": 200},
    {"id": "mision_20", "nombre": "Minar 20 shares hoy", "shares_requeridos": 20, "recompensa_oro": 1000},
]


# Dificultad FIJA por dispositivo — no cambia con la cantidad de usuarios.
# Calibrada para que un ESP32 individual encuentre un share cada ~25s.
DIFICULTAD_DISPOSITIVO = 4  # ajustar tras medir hashrate real del ESP32

# Recompensa por share — esta es la que se ajusta según el volumen total de la red.
# Empieza en un valor base y se recalcula semanalmente (ver ajustar_recompensa_por_share).
RECOMPENSA_POR_SHARE = 1000.0  # placeholder inicial, se recalcula con el cron semanal

META_ORO_SEMANAL = 50_000_000 * 24 * 7  # meta total de emisión de la red por semana

COSTO_DIARIO_USDT = 0.05
ROTACION_JOB_SEGUNDOS = 25  # alineado a que un share tarde ~25s en promedio

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

# Cada cuántos niveles alcanzados se entrega 1 ticket (moneda de logro, para la tienda de canje / mercado)
MINIJUEGOS_NIVELES_POR_TICKET = 4

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
TIENDA_CANJE = {
    "canje_electricidad_1": {
        "nombre": "1 día de electricidad (1 dispositivo)",
        "costo_tickets": 6,
        "tipo": "electricidad",
        "dias": 1,
    },
    "canje_electricidad_3": {
        "nombre": "3 días de electricidad (1 dispositivo)",
        "costo_tickets": 15,
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
