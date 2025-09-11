# 🚦 Simulador de Planificación de Procesos – SIGET

Este proyecto implementa un **simulador de planificación de procesos** en Python, como parte de la unidad de Sistemas Operativos.  
El simulador demuestra cómo diferentes algoritmos gestionan procesos del sistema **SIGET** (movilidad urbana).

## 📌 Objetivos
- Comprender la gestión de procesos y los algoritmos de planificación.  
- Analizar el desempeño de cada algoritmo en escenarios simulados.  
- Aplicar teoría de sistemas operativos en una solución práctica.  

## ⚙️ Algoritmos implementados
- **FIFO (First In, First Out)** → Procesos según orden de llegada.  
- **SJF (Shortest Job First)** → Atiende primero al proceso más corto.  
- **Round-Robin (RR)** → Ejecución con reparto equitativo (quantum configurable).  
- **Prioridad (preemptiva)** → Los procesos críticos se ejecutan de inmediato.  

## 📂 Estructura del repositorio
```
📦 simulador-planificador
 ┣ 📜 simulador_planificador_extendido.py   # Código fuente principal
 ┣ 📜 salida_fifo_sjf.txt                   # Ejecución de los algoritmos
 ┣ 📜 Informe_Simulador_SIGET.pdf           # Informe técnico (máx. 2 páginas)
 ┗ 📜 README.md                             # Documentación del repositorio
```

## ▶️ Ejecución
1. Clonar este repositorio:
   ```bash
   git clone https://github.com/usuario/simulador-planificador.git
   cd simulador-planificador
   ```
2. Ejecutar el simulador:
   ```bash
   python simulador_planificador_extendido.py
   ```

## 📊 Resultados
El simulador muestra en consola:
- **Evolución de los estados**: Nuevo → Listo → En ejecución → Bloqueado → Terminado.  
- **Métricas de desempeño**: turnaround, tiempo de espera y tiempo de respuesta.  

Los resultados detallados se encuentran en el archivo [`salida_fifo_sjf.txt`](./salida_fifo_sjf.txt).

## 📑 Informe
Se incluye el documento () con:
- Objetivos y decisiones de diseño.  
- Algoritmos utilizados y observaciones.  
- Conclusiones sobre el mejor enfoque para el SIGET.  

## 🎥 Evidencia en video
🔗 [Enlace al video de ejecución](#) *(agregar aquí Drive/YouTube/GitHub Video)*

## 👩‍💻 Autor
Proyecto académico desarrollado por Manuela García Soto 
Ingeniería de Software – Sistemas Operativos  
