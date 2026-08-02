MINERALES = {
    "cobre":       {"prob_drop": 0.50, "rareza": 1},
    "hierro":      {"prob_drop": 0.30, "rareza": 2},
    "plata":       {"prob_drop": 0.15, "rareza": 3},
    "oro_mineral": {"prob_drop": 0.07, "rareza": 4},
    "diamante":    {"prob_drop": 0.03, "rareza": 5},
    "platino":     {"prob_drop": 0.01, "rareza": 6},
}

RECETAS = {
    "pieza_basica":     {"requiere": {"cobre": 500}, "buff_hashrate": 0.03},
    "pieza_intermedia": {"requiere": {"cobre": 300, "hierro": 150}, "buff_hashrate": 0.07},
    "pieza_avanzada":   {"requiere": {"hierro": 200, "plata": 80, "oro_mineral": 20}, "buff_hashrate": 0.12},
    "pieza_epica":      {"requiere": {"plata": 150, "diamante": 15, "oro_mineral": 40}, "buff_hashrate": 0.20},
    "pieza_legendaria": {"requiere": {"diamante": 30, "platino": 5}, "buff_hashrate": 0.35},
}

NIVELES = [
    {"nombre": "Novato",   "oro_minado_min": 0},
    {"nombre": "Aprendiz", "oro_minado_min": 5_000_000},
    {"nombre": "Minero",   "oro_minado_min": 25_000_000},
    {"nombre": "Veterano", "oro_minado_min": 100_000_000},
    {"nombre": "Experto",  "oro_minado_min": 500_000_000},
    {"nombre": "Maestro",  "oro_minado_min": 2_000_000_000},
    {"nombre": "Leyenda",  "oro_minado_min": 10_000_000_000},
]

# Dificultad FIJA por dispositivo — no cambia con la cantidad de usuarios.
# Calibrada para que un ESP32 individual encuentre un share cada ~25s.
DIFICULTAD_DISPOSITIVO = 4  # ajustar tras medir hashrate real del ESP32

# Recompensa por share — esta es la que se ajusta según el volumen total de la red.
# Empieza en un valor base y se recalcula semanalmente (ver ajustar_recompensa_por_share).
RECOMPENSA_POR_SHARE = 1000.0  # placeholder inicial, se recalcula con el cron semanal

META_ORO_SEMANAL = 50_000_000 * 24 * 7  # meta total de emisión de la red por semana

COSTO_DIARIO_USDT = 0.01
ROTACION_JOB_SEGUNDOS = 25  # alineado a que un share tarde ~25s en promedio

# Paquetes de electricidad prepagada (precio POR CADA ESP32 que tenga el usuario)
PAQUETES_ELECTRICIDAD = {
    "10_dias": {"dias": 10, "precio_usdt_por_esp32": 0.10},
    "30_dias": {"dias": 30, "precio_usdt_por_esp32": 0.27},   # ~10% descuento
    "90_dias": {"dias": 90, "precio_usdt_por_esp32": 0.75},   # ~17% descuento
}


def calcular_nivel(oro_historico):
    nivel_actual = NIVELES[0]
    for nivel in NIVELES:
        if oro_historico >= nivel["oro_minado_min"]:
            nivel_actual = nivel
    return nivel_actual
