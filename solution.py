import random
from collections import deque
from statistics import mean, stdev
import math

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

JORNADA = 480  # 8 horas

NUM_VENDEDORES = 2
NUM_TECNICOS = 3
NUM_ESPECIALIZADOS = 1

NUM_REPLICAS = 900

GANANCIAS = {
    1: 0,
    2: 350,
    3: 500,
    4: 750
}

# =========================================================
# FUNCIONES ALEATORIAS
# =========================================================

def tiempo_entre_llegadas():
    return random.expovariate(1 / 20)


def tipo_servicio():

    r = random.random()

    if r < 0.45:
        return 1
    elif r < 0.70:
        return 2
    elif r < 0.80:
        return 3
    else:
        return 4


def tiempo_vendedor():
    return max(0, random.normalvariate(5, 2))


def tiempo_reparacion():
    return random.expovariate(1 / 20)


def tiempo_cambio_equipo():
    return random.expovariate(1 / 15)

# =========================================================
# CLIENTE
# =========================================================

class Cliente:

    contador = 0

    def __init__(self, llegada):

        Cliente.contador += 1

        self.id = Cliente.contador
        self.llegada = llegada
        self.tipo = tipo_servicio()

        self.inicio_vendedor = None
        self.fin_vendedor = None

        self.inicio_tecnico = None
        self.fin_tecnico = None

        self.salida = None

# =========================================================
# SIMULACIÓN DE UNA RÉPLICA
# =========================================================

def simular():

    # -----------------------------------------------------
    # Variables locales
    # -----------------------------------------------------

    reloj = 0

    proxima_llegada = tiempo_entre_llegadas()

    eventos_vendedores = []
    eventos_tecnicos = []
    eventos_especializados = []

    vendedores_libres = NUM_VENDEDORES
    tecnicos_libres = NUM_TECNICOS
    especializados_libres = NUM_ESPECIALIZADOS

    cola_vendedores = deque()
    cola_tecnicos = deque()
    cola_especializados = deque()

    clientes_atendidos = 0
    ganancia_total = 0

    espera_vendedor_total = 0
    espera_tecnico_total = 0

    clientes_por_tipo = {
        1: 0,
        2: 0,
        3: 0,
        4: 0
    }

    tiempo_ocupado_vendedores = 0
    tiempo_ocupado_tecnicos = 0
    tiempo_ocupado_especializados = 0

    # =====================================================
    # FUNCIONES INTERNAS
    # =====================================================

    def iniciar_servicio_vendedor(cliente, tiempo_actual):

        nonlocal vendedores_libres
        nonlocal tiempo_ocupado_vendedores
        nonlocal espera_vendedor_total

        vendedores_libres -= 1

        cliente.inicio_vendedor = tiempo_actual

        espera_vendedor_total += (
            tiempo_actual - cliente.llegada
        )

        servicio = tiempo_vendedor()

        tiempo_ocupado_vendedores += servicio

        fin = tiempo_actual + servicio

        eventos_vendedores.append((fin, cliente))

    # -----------------------------------------------------

    def iniciar_servicio_tecnico(cliente, tiempo_actual):

        nonlocal tecnicos_libres
        nonlocal tiempo_ocupado_tecnicos
        nonlocal espera_tecnico_total

        tecnicos_libres -= 1

        cliente.inicio_tecnico = tiempo_actual

        espera_tecnico_total += (
            tiempo_actual - cliente.fin_vendedor
        )

        servicio = tiempo_reparacion()

        tiempo_ocupado_tecnicos += servicio

        fin = tiempo_actual + servicio

        eventos_tecnicos.append((fin, cliente))

    # -----------------------------------------------------

    def iniciar_servicio_especializado(cliente, tiempo_actual):

        nonlocal especializados_libres
        nonlocal tiempo_ocupado_especializados
        nonlocal espera_tecnico_total

        especializados_libres -= 1

        cliente.inicio_tecnico = tiempo_actual

        espera_tecnico_total += (
            tiempo_actual - cliente.fin_vendedor
        )

        if cliente.tipo == 3:
            servicio = tiempo_cambio_equipo()
        else:
            servicio = tiempo_reparacion()

        tiempo_ocupado_especializados += servicio

        fin = tiempo_actual + servicio

        eventos_especializados.append((fin, cliente))

    # =====================================================
    # BUCLE PRINCIPAL
    # =====================================================

    while True:

        tiempos = []

        if proxima_llegada is not None:
            tiempos.append(("llegada", proxima_llegada))

        if eventos_vendedores:
            tiempos.append(
                ("fin_vendedor", min(eventos_vendedores)[0])
            )

        if eventos_tecnicos:
            tiempos.append(
                ("fin_tecnico", min(eventos_tecnicos)[0])
            )

        if eventos_especializados:
            tiempos.append(
                ("fin_especializado",
                 min(eventos_especializados)[0])
            )

        if not tiempos:
            break

        evento, tiempo_evento = min(
            tiempos,
            key=lambda x: x[1]
        )

        reloj = tiempo_evento

        # =================================================
        # LLEGADA
        # =================================================

        if evento == "llegada":

            cliente = Cliente(reloj)

            if vendedores_libres > 0:
                iniciar_servicio_vendedor(cliente, reloj)
            else:
                cola_vendedores.append(cliente)

            siguiente = reloj + tiempo_entre_llegadas()

            if siguiente <= JORNADA:
                proxima_llegada = siguiente
            else:
                proxima_llegada = None

        # =================================================
        # FIN VENDEDOR
        # =================================================

        elif evento == "fin_vendedor":

            fin, cliente = min(eventos_vendedores)

            eventos_vendedores.remove((fin, cliente))

            vendedores_libres += 1

            cliente.fin_vendedor = reloj

            # siguiente cliente vendedor
            if cola_vendedores:

                siguiente_cliente = (
                    cola_vendedores.popleft()
                )

                iniciar_servicio_vendedor(
                    siguiente_cliente,
                    reloj
                )

            # reparación
            if cliente.tipo in [1, 2]:

                if tecnicos_libres > 0:

                    iniciar_servicio_tecnico(
                        cliente,
                        reloj
                    )

                elif (
                    especializados_libres > 0 and
                    len(cola_especializados) == 0
                ):

                    iniciar_servicio_especializado(
                        cliente,
                        reloj
                    )

                else:

                    cola_tecnicos.append(cliente)

            # cambio equipo
            elif cliente.tipo == 3:

                if especializados_libres > 0:

                    iniciar_servicio_especializado(
                        cliente,
                        reloj
                    )

                else:

                    cola_especializados.append(cliente)

            # venta
            else:

                cliente.salida = reloj

                clientes_por_tipo[cliente.tipo] += 1
                clientes_atendidos += 1

                nonlocal_gain = GANANCIAS[cliente.tipo]

                ganancia_total += nonlocal_gain

        # =================================================
        # FIN TÉCNICO
        # =================================================

        elif evento == "fin_tecnico":

            fin, cliente = min(eventos_tecnicos)

            eventos_tecnicos.remove((fin, cliente))

            tecnicos_libres += 1

            cliente.fin_tecnico = reloj
            cliente.salida = reloj

            clientes_por_tipo[cliente.tipo] += 1
            clientes_atendidos += 1

            ganancia_total += GANANCIAS[cliente.tipo]

            if cola_tecnicos:

                siguiente_cliente = (
                    cola_tecnicos.popleft()
                )

                iniciar_servicio_tecnico(
                    siguiente_cliente,
                    reloj
                )

        # =================================================
        # FIN ESPECIALIZADO
        # =================================================

        elif evento == "fin_especializado":

            fin, cliente = min(eventos_especializados)

            eventos_especializados.remove((fin, cliente))

            especializados_libres += 1

            cliente.fin_tecnico = reloj
            cliente.salida = reloj

            clientes_por_tipo[cliente.tipo] += 1
            clientes_atendidos += 1

            ganancia_total += GANANCIAS[cliente.tipo]

            cliente_prioridad = None

            for c in cola_especializados:

                if c.tipo == 3:

                    cliente_prioridad = c
                    break

            if cliente_prioridad:

                cola_especializados.remove(
                    cliente_prioridad
                )

                iniciar_servicio_especializado(
                    cliente_prioridad,
                    reloj
                )

            elif cola_tecnicos:

                siguiente_cliente = (
                    cola_tecnicos.popleft()
                )

                iniciar_servicio_especializado(
                    siguiente_cliente,
                    reloj
                )

    # =====================================================
    # RESULTADOS DE LA RÉPLICA
    # =====================================================

    util_vendedores = (
        tiempo_ocupado_vendedores /
        (NUM_VENDEDORES * JORNADA)
    ) * 100

    util_tecnicos = (
        tiempo_ocupado_tecnicos /
        (NUM_TECNICOS * JORNADA)
    ) * 100

    util_especializados = (
        tiempo_ocupado_especializados /
        (NUM_ESPECIALIZADOS * JORNADA)
    ) * 100

    return {
        "ganancia": ganancia_total,
        "clientes": clientes_atendidos,
        "espera_vendedor":
            espera_vendedor_total /
            max(clientes_atendidos, 1),

        "espera_tecnico":
            espera_tecnico_total /
            max(clientes_atendidos, 1),

        "util_vendedores": util_vendedores,
        "util_tecnicos": util_tecnicos,
        "util_especializados":
            util_especializados
    }

# =========================================================
# EJECUTAR RÉPLICAS
# =========================================================

ganancias = []
clientes = []
esperas_vendedor = []
esperas_tecnico = []

util_vendedores = []
util_tecnicos = []
util_especializados = []

for i in range(NUM_REPLICAS):

    resultado = simular()

    ganancias.append(resultado["ganancia"])
    clientes.append(resultado["clientes"])

    esperas_vendedor.append(
        resultado["espera_vendedor"]
    )

    esperas_tecnico.append(
        resultado["espera_tecnico"]
    )

    util_vendedores.append(
        resultado["util_vendedores"]
    )

    util_tecnicos.append(
        resultado["util_tecnicos"]
    )

    util_especializados.append(
        resultado["util_especializados"]
    )

# =========================================================
# ANÁLISIS ESTADÍSTICO
# =========================================================

media_ganancia = mean(ganancias)
desv_ganancia = stdev(ganancias)

# Intervalo 95% usando Z = 1.96

z = 1.96

error = (
    z *
    (desv_ganancia / math.sqrt(NUM_REPLICAS))
)

ic_inferior = media_ganancia - error
ic_superior = media_ganancia + error

# =========================================================
# RESULTADOS FINALES
# =========================================================

print("\n==============================")
print("RESULTADOS DE SIMULACIÓN")
print("==============================\n")

print(f"Réplicas ejecutadas: {NUM_REPLICAS}")

print("\n----- GANANCIA -----")

print(f"Ganancia promedio: "
      f"${media_ganancia:.2f}")

print(f"Desviación estándar: "
      f"${desv_ganancia:.2f}")

print("\nIntervalo de confianza 95%:")

print(f"[${ic_inferior:.2f}, "
      f"${ic_superior:.2f}]")

print("\n----- CLIENTES -----")

print(f"Clientes promedio: "
      f"{mean(clientes):.2f}")

print("\n----- ESPERAS -----")

print(f"Espera promedio vendedor: "
      f"{mean(esperas_vendedor):.2f} min")

print(f"Espera promedio técnico: "
      f"{mean(esperas_tecnico):.2f} min")

print("\n----- UTILIZACIÓN -----")

print(f"Vendedores: "
      f"{mean(util_vendedores):.2f}%")

print(f"Técnicos: "
      f"{mean(util_tecnicos):.2f}%")

print(f"Técnico especializado: "
      f"{mean(util_especializados):.2f}%")