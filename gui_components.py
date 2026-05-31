import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from numerical_engine import simpson_rule_simple, simpson_rule_compuesta, funcion_segura
import timeit

from numerical_engine import simpson_rule_simple, simpson_rule_compuesta, funcion_segura

class SimpsonRule13App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de Regla de Simpson 1/3")
        self.geometry("1050x750")
        ctk.set_appearance_mode("Light")

        self.font_titulo = ("Raleway", 24, "bold")
        self.font_subtitulo = ("Raleway", 14)
        self.font_label = ("Raleway", 12, "bold")
        self.font_normal = ("Raleway", 12)
        self.font_mono = ("Consolas", 13, "bold")

        # Panel Izquierdo: Formulario
        self.frame_form = ctk.CTkFrame(self, width=340, fg_color="#ffffff", corner_radius=15)
        self.frame_form.pack(side="left", fill="y", padx=20, pady=20)

        ctk.CTkLabel(self.frame_form, text="Regla de Simpson 1/3", font=self.font_titulo, text_color="#21917b").pack(pady=(20, 0))
        ctk.CTkLabel(self.frame_form, text="Comparativa con Gráficas", font=self.font_subtitulo, text_color="#78a39c").pack(pady=(0, 15))
        ctk.CTkLabel(self.frame_form, text="Elaborado por Elihú Ibarra, Bryan Jeronimo y Alejandro Segovia", font=self.font_normal, text_color="#6a7b78").pack(pady=(0, 15))

        self.entry_funcion = self.crear_input("Funcion f(x)", "Ej: x**3 + 2*x - 5 (usa operadores de Python)")

        frame_limites = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        frame_limites.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(frame_limites, text="Límite Inferior (a)", font=self.font_label, text_color="#475569").pack(side="left")
        self.entry_a = ctk.CTkEntry(frame_limites, width=80)
        self.entry_a.pack(side="left", padx=(5, 10))

        ctk.CTkLabel(frame_limites, text="Límite Superior (b)", font=self.font_label, text_color="#475569").pack(side="left")
        self.entry_b = ctk.CTkEntry(frame_limites, width=80)
        self.entry_b.pack(side="left", padx=(5, 10))

        self.entry_n = self.crear_input("Intervalo (n). Sólo para versión compuesta. n debe ser par.", "Ej: 2, 8, 32...")

        # Checkboxes para seleccionar entre la variante simple o compuesta de la regla de Simpson 1/3 (o ambas)
        ctk.CTkLabel(self.frame_form, text="Métodos a evaluar:", font=self.font_label, text_color="#475569").pack(anchor="w", padx=20, pady=(0, 5))

        self.var_simple = ctk.BooleanVar(value=True)
        self.var_compuesta = ctk.BooleanVar(value=True)

        frame_checks = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        frame_checks.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkCheckBox(frame_checks, text="Simple", variable=self.var_simple, font=self.font_normal, fg_color="#21917b", text_color="#475569").pack(side="left", padx=(0, 15))
        ctk.CTkCheckBox(frame_checks, text="Compuesta", variable=self.var_compuesta, font=self.font_normal, fg_color="#21917b", text_color="#475569").pack(side="left")

        # Botón
        self.btn_calcular = ctk.CTkButton(self.frame_form, text="Calcular Integral", font=("Raleway", 14, "bold"), fg_color="#21917b", hover_color="#78a39c", height=50, command=self.ejecutar)
        self.btn_calcular.pack(fill="x", padx=20, pady=(10, 15))

        # Tarjeta de error
        self.frame_error = ctk.CTkFrame(self.frame_form, fg_color="#fef2f2", border_color="#fecaca", border_width=1, corner_radius=8)
        self.lbl_error_texto = ctk.CTkLabel(self.frame_error, text="", text_color="#831919", font=self.font_label, wraplength=260)
        self.lbl_error_texto.pack(pady=10, padx=10)

        # Tarjeta de Resultado de Versión Simple
        self.frame_resultado_simple = ctk.CTkFrame(self.frame_form, fg_color="#f0fdf4", border_color="#bbf7d0", border_width=1, corner_radius=8)
        ctk.CTkLabel(self.frame_resultado_simple, text="VERSIÓN SIMPLE", font=self.font_label, text_color="#21917b").pack(anchor="w", padx=15, pady=(10, 0))
        self.lbl_area_simple = ctk.CTkLabel(self.frame_resultado_simple, text="Área: ---", font=self.font_mono, text_color="#235134")
        self.lbl_area_simple.pack(anchor="w", padx=15)
        self.lbl_tiempo_simple = ctk.CTkLabel(self.frame_resultado_simple, text="Tiempo: ---", font=self.font_normal, text_color="#235134")
        self.lbl_tiempo_simple.pack(anchor="w", padx=15, pady=(0, 10))

        # Tarjeta de Resultado de Versión Compuesta
        self.frame_resultado_compuesta = ctk.CTkFrame(self.frame_form, fg_color="#f0fdf4", border_color="#bbf7d0", border_width=1, corner_radius=8)
        ctk.CTkLabel(self.frame_resultado_compuesta, text="VERSIÓN COMPUESTA", font=self.font_label, text_color="#21917b").pack(anchor="w", padx=15, pady=(10, 0))
        self.lbl_area_compuesta = ctk.CTkLabel(self.frame_resultado_compuesta, text="Área: ---", font=self.font_mono, text_color="#235134")
        self.lbl_area_compuesta.pack(anchor="w", padx=15)
        self.lbl_tiempo_compuesta = ctk.CTkLabel(self.frame_resultado_compuesta, text="Tiempo: ---", font=self.font_normal, text_color="#235134")
        self.lbl_tiempo_compuesta.pack(anchor="w", padx=15, pady=(0, 10))

        # Panel Derecho: Resultados de Gráfica 
        self.frame_grafica = ctk.CTkFrame(self, fg_color="#eef2f6")
        self.frame_grafica.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

        self.fig = plt.figure(figsize=(6, 5), dpi=100)
        self.fig.patch.set_facecolor("#eef2f6")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafica)

        # Navegación de herramientas
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_grafica)
        self.toolbar.update()
        self.toolbar.config(background="#eef2f6")
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def crear_input(self, titulo, placeholder):
        ctk.CTkLabel(self.frame_form, text=titulo, font=self.font_label, text_color="#475569").pack(anchor="w", padx=20)
        entry = ctk.CTkEntry(self.frame_form, placeholder_text=placeholder, height=35, font=self.font_normal)
        entry.pack(fill="x", padx=20, pady=(0,15))
        return entry
    
    def ocultar_tarjetas(self):
        # Oculta todas las tarjetas de resultados y errores para limpiar la pantalla
        self.frame_error.pack_forget()
        self.frame_resultado_simple.pack_forget()
        self.frame_resultado_compuesta.pack_forget()

    def mostrar_error(self, mensaje):
        # Muestra una tarjeta con mensaje de error que corresponda al caso.
        self.ocultar_tarjetas()
        self.lbl_error_texto.configure(text=f"ADVERTENCIA: {mensaje}")
        self.frame_error.pack(fill="x", padx=20, pady=5)
    
    def ejecutar(self):
        # Limpieza de resultados por cada nueva ejecución
        self.ocultar_tarjetas()
        usar_simple = self.var_simple.get()
        usar_compuesta = self.var_compuesta.get()

        if not usar_simple and not usar_compuesta:
            self.mostrar_error("Selecciona al menos un método a evaluar.")
            return
        
        # 1. Validación de la Función
        func_str = self.entry_funcion.get().strip()
        if not func_str:
            self.mostrar_error("La función está vacía. Por favor escribe una ecuación.")
            return

        # 2. Validación de Límites
        str_a = self.entry_a.get().strip()
        str_b = self.entry_b.get().strip()

        if not str_a or not str_b:
            self.mostrar_error("Los límites no se definieron correctamente. Ingresa el límite inferior y superior.")
            return
        try:
            a = float(str_a)
            b = float(str_b)
        except ValueError:
            self.mostrar_error("Los límites 'a' y 'b' deben ser valores numéricos.")
            return
        if a >= b:
            self.mostrar_error("El límite inferior 'a' debe ser menor que el superior 'b'.")
            return
        
        # 3. Validación de Intervalos (sólo con la versión compuesta)
        n = 0
        if usar_compuesta:
            str_n = self.entry_n.get().strip()
            if not str_n:
                self.mostrar_error("El valor de intervalos 'n' está vacío. Se requiere para la versión compuesta.")
                return
            try:
                n = int(str_n)
            except ValueError:
                self.mostrar_error("El valor de 'n' debe ser un número entero.")
                return

            if n <= 0:
                self.mostrar_error("El valor de 'n' no puede ser negativo o igual a cero.")
                return
            if n % 2 != 0:
                self.mostrar_error("El valor de 'n' debe ser un número par.")
                return
            if n > 1000: # Límite para el valor de n para evitar overflow de memoria. Al tenerse un orden O(h^4), un valor de n superior a 1000 resulta redundante
                self.mostrar_error("Valor de 'n' demasiado alto (Límite: 1000). Debido a la rapidez de convergencia O(h^4) del método, un valor mayor es redundante y puede saturar la gráfica.")
                return
        
        # 4. Validar que la función sea matemáticamente correcta
        try:
            funcion_evaluable = funcion_segura(func_str)
            funcion_evaluable(a)
        except Exception as e:
            self.mostrar_error(f"Error matemático en la función. Verifique la sintaxis.")
            return
    
        repeticiones = 100 # Num. de reps para obtener promedio con timeit
        
        # Cálculo con el uso de la versión simple
        if usar_simple:
            resultado_version_simple = simpson_rule_simple(funcion_evaluable, a, b)
            tarea_simple = lambda: simpson_rule_simple(funcion_evaluable, a, b)
            tiempo_total_s = timeit.timeit(stmt=tarea_simple, number=repeticiones)
            tiempo_promedio_microsegundos = (tiempo_total_s / repeticiones) * 1_000_000

            self.lbl_area_simple.configure(text=f"Área: {resultado_version_simple:.6f} u²")
            self.lbl_tiempo_simple.configure(text=f"Tiempo: {tiempo_promedio_microsegundos:.6f} µ segundos")
            self.frame_resultado_simple.pack(fill="x", padx=20, pady=5)

            # Cálculo con el uso de la versión compuesta
        if usar_compuesta:
            resultado_version_compuesta = simpson_rule_compuesta(funcion_evaluable, a, b, n)
            tarea_compuesta = lambda: simpson_rule_compuesta(funcion_evaluable, a, b, n)
            tiempo_total_s = timeit.timeit(stmt=tarea_compuesta, number=repeticiones)
            tiempo_promedio_microsegundos = (tiempo_total_s / repeticiones) * 1_000_000

            self.lbl_area_compuesta.configure(text=f"Área: {resultado_version_compuesta:.6f} u²")
            self.lbl_tiempo_compuesta.configure(text=f"Tiempo: {tiempo_promedio_microsegundos:.6f} µ segundos")
            self.frame_resultado_compuesta.pack(fill="x", padx=20, pady=5)

            # Invocar la función que dibuja la gráfica
        try:
            self.graficar(funcion_evaluable, a, b, n, usar_simple, usar_compuesta)
        except Exception as e:
            self.mostrar_error(f"Error al graficar: {str(e)}")
            
    def graficar(self, funcion, a, b, n, usar_simple, usar_compuesta):
        # Limpiar la gráfica por cada nueva ejecución
        self.fig.clf()

        # Calcular la cantidad de gráficas a trazar
        num_graficas = sum([usar_simple, usar_compuesta])
        indice_actual = 1

        # Trazar la versión simple
        if usar_simple:
            # orden de acomodo: add_subplot(filas, columnas, indice)
            ax = self.fig.add_subplot(num_graficas, 1, indice_actual)
            self.trazar_parabolas(ax, funcion, a, b, 2, "Regla de Simpson 1/3 (versión simple)")
            indice_actual += 1
        
        # Trazar la regla compuesta
        if usar_compuesta:
            ax = self.fig.add_subplot(num_graficas, 1, indice_actual)
            self.trazar_parabolas(ax, funcion, a, b, n, f"Regla de Simpson 1/3 (versión compuesta n={n})")

        # Ajustar espacios y mostrar
        self.fig.tight_layout()
        self.canvas.draw()
    
    def trazar_parabolas(self, ax, funcion, a, b, n, titulo): # Función auxiliar para parábolas
        x_continuo = np.linspace(a, b, 500)
        y_continuo = [funcion(xi) for xi in x_continuo]
        ax.plot(x_continuo, y_continuo, color="#1e293b", label="f(x) real", linewidth=2)

        delta_x = (b - a) / n
        x_puntos = [a + i * delta_x for i in range(n + 1)]
        y_puntos = [funcion(xi) for xi in x_puntos]

        for i in range(0, n, 2):
            x_seg = x_puntos[i:i+3]
            y_seg = y_puntos[i:i+3]

            coeficientes = np.polyfit(x_seg, y_seg, 2)
            x_parabola = np.linspace(x_seg[0], x_seg[2], 50)
            y_parabola = np.polyval(coeficientes, x_parabola)

            ax.fill_between(x_parabola, 0, y_parabola, color="#67995d", alpha=0.3, edgecolor="#78a39c", linewidth=1)
            ax.plot(x_seg, y_seg, 'ro', markersize=4)
        
        ax.set_title(titulo, fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(loc="upper right", fontsize=8)