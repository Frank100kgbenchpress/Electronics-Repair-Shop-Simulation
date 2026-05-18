# Informe de Simulación — Taller “Happy Computing”

## 1. Introducción

El presente informe analiza el comportamiento operativo del taller de reparaciones electrónicas “Happy Computing” mediante una **simulación de eventos discretos**. El objetivo es estimar la ganancia diaria, el nivel de utilización de recursos y el comportamiento de espera de los clientes bajo condiciones de incertidumbre.

---

## 2. Descripción del sistema

El taller ofrece cuatro tipos de servicios:

| Tipo | Servicio | Ganancia |
|------|----------|----------|
| 1 | Reparación por garantía | $0 |
| 2 | Reparación fuera de garantía | $350 |
| 3 | Cambio de equipo | $500 |
| 4 | Venta de equipos reparados | $750 |

### Recursos disponibles

- 2 Vendedores  
- 3 Técnicos  
- 1 Técnico especializado  

---

## 3. Modelo de simulación

El sistema se modela como una **simulación de eventos discretos con colas y recursos limitados**.

### 3.1 Llegadas de clientes
- Distribución exponencial
- Media: 20 minutos

### 3.2 Tipos de servicio

- Tipo 1: 0.45  
- Tipo 2: 0.25  
- Tipo 3: 0.10  
- Tipo 4: 0.20  

### 3.3 Tiempos de servicio

- Vendedor: \( N(5, 2) \)
- Técnico: Exponencial con media 20 min
- Técnico especializado: Exponencial con media 15 min

---

## 4. Reglas del sistema

1. Todo cliente es atendido inicialmente por un vendedor.
2. Según el tipo de servicio:
   - Tipo 1 y 2 → técnico
   - Tipo 3 → técnico especializado
   - Tipo 4 → finaliza tras el vendedor
3. Si no hay recursos disponibles, el cliente espera en cola FIFO.
4. El técnico especializado prioriza clientes de tipo 3 sobre reparaciones.

---

## 5. Metodología experimental

Se realizaron:

- **900 réplicas independientes**
- Duración de cada simulación: **480 minutos**
- Se estimaron:
  - Ganancia promedio
  - Intervalo de confianza al 95%
  - Esperas promedio
  - Utilización de recursos

---

## 6. Resultados

### 6.1 Ganancia

- Ganancia promedio: **$6898.17**
- Desviación estándar: **$2019.54**

### Intervalo de confianza (95%)

\[
[6766.22,\ 7030.11]
\]

---

### 6.2 Clientes atendidos

- Promedio de clientes por jornada: **24.05**

---

### 6.3 Tiempos de espera

- Espera promedio en vendedor: **0.05 minutos**
- Espera promedio en técnicos: **0.17 minutos**

---

### 6.4 Utilización de recursos

| Recurso | Utilización |
|----------|------------|
| Vendedores | 12.51% |
| Técnicos | 22.73% |
| Técnico especializado | 8.80% |

---

## 7. Análisis de resultados

### 7.1 Estabilidad del sistema

Con 900 réplicas se observa una **alta estabilidad estadística**, evidenciada por la reducción del intervalo de confianza respecto a simulaciones con menos repeticiones.

La media de ganancia converge a aproximadamente **$6900 por jornada**.

---

### 7.2 Baja utilización de recursos

Los tres tipos de recursos presentan baja utilización:

- Vendedores: ~12%
- Técnicos: ~23%
- Técnico especializado: <10%

Esto indica que el sistema opera con **capacidad ociosa significativa**.

---

### 7.3 Congestión del sistema

Los tiempos de espera siguen siendo muy bajos, lo que confirma que:

> El sistema no presenta congestión ni cuellos de botella relevantes bajo la demanda simulada.

---

## 8. Conclusiones

- El sistema presenta **baja carga operativa**.
- No existen colas significativas ni saturación de recursos.
- El taller está **sobredimensionado respecto a la demanda actual**.
- La ganancia promedio es estable alrededor de **$6900 por jornada**.
- El incremento a 900 réplicas permitió obtener estimaciones más precisas y un intervalo de confianza más estrecho.

---

## 9. Recomendaciones

- Evaluar reducción de personal o redistribución de recursos.
- Analizar escenarios con mayor demanda para mejorar eficiencia.
- Considerar estudios de optimización costo-beneficio.
- Incrementar aún más las réplicas si se requiere precisión adicional.

---

## 10. Conclusión final

El sistema simulado opera en condiciones de baja utilización, sin congestión y con alta capacidad ociosa. Aunque el sistema es estable y predecible, su eficiencia operativa es baja debido al bajo aprovechamiento de los recursos disponibles.
