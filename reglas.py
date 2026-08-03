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
