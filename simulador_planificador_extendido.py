
# simulador_planificador_extendido.py
# Simulador de planificación de procesos (FIFO, SJF, Round-Robin y Prioridad preemtiva)

from dataclasses import dataclass, field
from typing import List, Optional
import heapq

@dataclass(order=True)
class Proceso:
    sort_index: int = field(init=False, repr=False)
    pid: int
    llegada: int              # tiempo de llegada al sistema
    prioridad: int            # prioridad (1 = mayor urgencia)
    tamano_datos: int         # tamaño de datos (informativo)
    rafaga: int               # tiempo de CPU estimado (rafaga)
    estado: str = field(default="Nuevo")  # Nuevo, Listo, En ejecución, Bloqueado, Terminado
    restante: int = field(init=False)
    tiempo_inicio: Optional[int] = None
    tiempo_fin: Optional[int] = None
    tiempo_respuesta: Optional[int] = None
    tiempo_espera: int = 0
    ultima_vez_listo: Optional[int] = None
    
    def __post_init__(self):
        self.restante = self.rafaga
        self.sort_index = (self.prioridad, self.llegada, self.pid)

def simular(procesos: List[Proceso], algoritmo: str="RR", quantum: int=2, tiempo_max: int=200):
    """
    Simula la planificación de CPU.
    - procesos: lista de Proceso
    - algoritmo: "RR", "PRIORIDAD", "FIFO", "SJF"
    """
    procs = [Proceso(pid=p.pid, llegada=p.llegada, prioridad=p.prioridad, tamano_datos=p.tamano_datos, rafaga=p.rafaga) for p in procesos]
    tiempo = 0
    linea_tiempo = []
    ejecutando = None
    cola_rr = []
    heap_prioridad = []
    cola_fifo = []
    heap_sjf = []
    terminados = []
    
    def revisar_llegadas(t):
        for p in procs:
            if p.llegada == t and p.estado == "Nuevo":
                p.estado = "Listo"
                p.ultima_vez_listo = t
                if algoritmo == "RR":
                    cola_rr.append(p)
                elif algoritmo == "PRIORIDAD":
                    heapq.heappush(heap_prioridad, (p.prioridad, p.llegada, p.pid, p))
                elif algoritmo == "FIFO":
                    cola_fifo.append(p)
                elif algoritmo == "SJF":
                    heapq.heappush(heap_sjf, (p.rafaga, p.llegada, p.pid, p))
                linea_tiempo.append(f"[t={t}] Llegó P{p.pid} -> Listo (rafaga={p.rafaga}, prio={p.prioridad})")
    
    def elegir_siguiente():
        if algoritmo == "RR" and cola_rr:
            return cola_rr.pop(0)
        elif algoritmo == "PRIORIDAD" and heap_prioridad:
            return heapq.heappop(heap_prioridad)[3]
        elif algoritmo == "FIFO" and cola_fifo:
            return cola_fifo.pop(0)
        elif algoritmo == "SJF" and heap_sjf:
            return heapq.heappop(heap_sjf)[3]
        return None
    
    uso_quantum = 0
    while tiempo < tiempo_max and (len(terminados) < len(procs)):
        revisar_llegadas(tiempo)
        
        if ejecutando is None:
            ejecutando = elegir_siguiente()
            if ejecutando:
                ejecutando.estado = "En ejecución"
                if ejecutando.tiempo_inicio is None:
                    ejecutando.tiempo_inicio = tiempo
                    ejecutando.tiempo_respuesta = ejecutando.tiempo_inicio - ejecutando.llegada
                ejecutando.tiempo_espera += (tiempo - ejecutando.ultima_vez_listo) if ejecutando.ultima_vez_listo is not None else 0
                linea_tiempo.append(f"[t={tiempo}] P{ejecutando.pid} comienza ejecución (restante={ejecutando.restante})")
                uso_quantum = 0
        
        if ejecutando:
            ejecutando.restante -= 1
            uso_quantum += 1
            linea_tiempo.append(f"[t={tiempo}] P{ejecutando.pid} ejecuta (restante={ejecutando.restante})")
            
            if ejecutando.restante <= 0:
                ejecutando.estado = "Terminado"
                ejecutando.tiempo_fin = tiempo + 1
                linea_tiempo.append(f"[t={tiempo+1}] P{ejecutando.pid} termina. Turnaround={ejecutando.tiempo_fin - ejecutando.llegada}, Respuesta={ejecutando.tiempo_respuesta}, Espera={ejecutando.tiempo_espera}")
                terminados.append(ejecutando)
                ejecutando = None
                uso_quantum = 0
            else:
                if algoritmo == "RR" and uso_quantum >= quantum:
                    ejecutando.estado = "Listo"
                    ejecutando.ultima_vez_listo = tiempo + 1
                    cola_rr.append(ejecutando)
                    linea_tiempo.append(f"[t={tiempo+1}] Quantum expiró para P{ejecutando.pid} -> Listo")
                    ejecutando = None
                    uso_quantum = 0
                elif algoritmo == "PRIORIDAD":
                    if heap_prioridad and heap_prioridad[0][0] < ejecutando.prioridad:
                        ejecutando.estado = "Listo"
                        ejecutando.ultima_vez_listo = tiempo + 1
                        heapq.heappush(heap_prioridad, (ejecutando.prioridad, ejecutando.llegada, ejecutando.pid, ejecutando))
                        linea_tiempo.append(f"[t={tiempo+1}] P{ejecutando.pid} preemptado por proceso de mayor prioridad -> Listo")
                        ejecutando = None
        tiempo += 1
    
    resumen = []
    for p in terminados:
        tat = p.tiempo_fin - p.llegada
        rt = p.tiempo_respuesta if p.tiempo_respuesta is not None else -1
        wt = p.tiempo_espera
        resumen.append((p.pid, p.llegada, p.prioridad, p.rafaga, tat, rt, wt))
    
    for p in procs:
        if p.estado != "Terminado" and p.tiempo_fin is None:
            linea_tiempo.append(f"[t={tiempo}] P{p.pid} no terminó (estado={p.estado}, restante={p.restante})")
    
    salida = "\n".join(linea_tiempo)
    salida += "\n\n--- RESUMEN DE METRICAS ---\n"
    salida += "PID | llegada | prio | rafaga | turnaround | respuesta | espera\n"
    for s in resumen:
        salida += f"P{s[0]:<2}  |   {s[1]:<5} |  {s[2]:<3} |  {s[3]:<6} |    {s[4]:<7} |   {s[5]:<8} |  {s[6]:<6}\n"
    if resumen:
        avg_tat = sum(s[4] for s in resumen) / len(resumen)
        avg_rt = sum(s[5] for s in resumen) / len(resumen)
        avg_wt = sum(s[6] for s in resumen) / len(resumen)
        salida += f"\nPromedios -> Turnaround: {avg_tat:.2f}, Respuesta: {avg_rt:.2f}, Espera: {avg_wt:.2f}\n"
    return salida

if __name__ == '__main__':
    procesos_ejemplo = [
        Proceso(pid=1, llegada=0, prioridad=2, tamano_datos=500, rafaga=6),
        Proceso(pid=2, llegada=1, prioridad=1, tamano_datos=200, rafaga=3),
        Proceso(pid=3, llegada=2, prioridad=3, tamano_datos=800, rafaga=8),
    ]
    print("=== Simulación FIFO ===\n")
    print(simular(procesos_ejemplo, algoritmo="FIFO"))
    print("\n=== Simulación SJF ===\n")
    print(simular(procesos_ejemplo, algoritmo="SJF"))
    print("\n=== Simulación Round-Robin (quantum=2) ===\n")
    print(simular(procesos_ejemplo, algoritmo="RR", quantum=2))
    print("\n=== Simulación Prioridad (preemtiva) ===\n")
    print(simular(procesos_ejemplo, algoritmo="PRIORIDAD"))
