import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

from numerical_engine import simpson_rule_simple, simpson_rule_compuesta, funcion_segura

class SimpsonRule13App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de regla de Simpson 1/3")
        self.geometry("1000x750")
        ctk.set_appearance_mode("Light")

        self.frame_form = ctk.CTkFrame(self, width=320, fg_color="#ffffff", corner_radius=15)
        self.frame_form.pack(side="left", fill="y", padx=20, pady=20)

        ctk.CTkLabel(self.frame_form, text="Regla de Simpson 1/3", font=("Raleway", 24, "bold"), text_color="#21917b").pack(pady=(20, 0))
        ctk.CTkLabel(self.frame_form, text="Comparativa de Gráficas", font=("Raleway", 14), text_color="#78a39c").pack(pady=(0, 15))

        self.entry_funcion = self.crear_input("Funcion f(x)", "Ej: x**3 + 2*x - 5")

        frame_limites = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        frame_limites.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(frame_limites, text="Límite Inferior (a)", font=("Raleway", 12, "bold"), text_color="#475569").pack(side="left")
        self.entry_a = ctk.CTkEntry(frame_limites, width=80)
        self.entry_a.pack(side="left", padx=(5, 10))

        ctk.CTkLabel(frame_limites, text="Límite Superior (b)", font=("Raleway", 12, "bold"), text_color="#475569").pack(side="left")
        self.entry_b = ctk.CTkEntry(frame_limites, width=80)
        self.entry_b.pack(side="left", padx=(5, 10))

        self.entry_n = self.crear_input("Intervalo (n). Sólo para versión compuesta. n debe ser par.", "Ej: 2, 8, 32...")

        # Checkboxes para seleccionar entre la variante simple o compuesta de la regla de Simpson 1/3 (o ambas)
        ctk.CTkLabel(self.frame_form, text="Métodos a evaluar:", font=("Raleway", 12, "bold"), text_color="#475569").pack(anchor="w", padx=20, pady=(0, 5))

        self.var_simple = ctk.BooleanVar(value=True)
        self.var_compuesta = ctk.BooleanVar(value=True)

        frame_checks = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        frame_checks.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkCheckBox(frame_checks, text="Simple", variable=self.var_simple, fg_color="#21917b", text_color="#475569").pack(side="left", padx=(0, 10))
        ctk.CTkCheckBox(frame_checks, text="Compuesta", variable=self.var_compuesta, fg_color="#21917b", text_color="#475569").pack(side="left")

        # Botón
        self.btn_calcular = ctk.CTkButton(self.frame_form, text="Calcular Integral", font=("Raleway", 14, "bold"), fg_color="#21917b", hover_color="#78a39c", height=50, command=self.ejecutar)
        self.btn_calcular.pack(fill="x", padx=20, pady=20)

        # Resultados
        self.lbl_resultado_simple = ctk.CTkLabel(self.frame_form, text="", font=("monospace", 14), text_color="#21917b", justify="left")
        self.lbl_resultado_simple.pack(pady=2, padx=10, fill="x")

        self.lbl_resultado_compuesta = ctk.CTkLabel(self.frame_form, text="", font=("monospace", 14), text_color="#21917b", justify="left")
        self.lbl_resultado_compuesta.pack(pady=2, padx=10, fill="x")
        
        # Gráfica
        self.frame_grafica = ctk.CTkFrame(self, fg_color="#eef2f6")
        self.frame_grafica.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

        self.fig = plt.figure(figsize=(6, 5), dpi=100)
        self.fig.patch.set_facecolor("#eef2f6")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafica)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def crear_input(self, titulo, placeholder):
        ctk.CTkLabel(self.frame_form, text=titulo, font=("Inter", 12, "bold"), text_color="#475569").pack(anchor="w", padx=20)
        entry = ctk.CTkEntry(self.frame_form, placeholder_text=placeholder, height=35)
        entry.pack(fill="x", padx=20, pady=(0,15))
        return entry
    
    def ejecutar(self):
        # Limpieza de resultados por cada nueva ejecución
        self.lbl_resultado_simple.configure(text="")
        self.lbl_resultado_compuesta.configure(text="")

        try:
            usar_simple = self.var_simple.get()
            usar_compuesta = self.var_compuesta.get()

            if not usar_simple and not usar_compuesta:
                raise ValueError("Selecciona al menos un método.")

            func_str = self.entry_funcion.get()
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())

            funcion_evaluable = funcion_segura(func_str)
            funcion_evaluable(a)

            # Valor predeterminado del número de intervalos para versión compuesta
            n = 0

            # Cálculo con el uso de la versión simple
            if usar_simple:
                inicio = time.perf_counter()
                resultado_version_simple = simpson_rule_simple(funcion_evaluable, a, b)
                final = time.perf_counter()
                tiempo_us = (final - inicio) * 1_000_000 # milisegundos

                texto = f"VERSIÓN SIMPLE:\nÁrea: {resultado_version_simple:.6f} u^2\nTiempo: {tiempo_us:.2f} µ segundos"
                self.lbl_resultado_simple.configure(text=texto, text_color="#67995d")

            # Cálculo con el uso de la versión compuesta
            if usar_compuesta:
                try:
                    n = int(self.entry_n.get())
                except ValueError:
                    raise ValueError("Inserta un valor par positivo para 'n' (versión compuesta).")
                
                inicio = time.perf_counter()
                resultado_version_compuesta = simpson_rule_simple(funcion_evaluable, a, b)
                final = time.perf_counter()
                tiempo_us = (final - inicio) * 1_000_000 # milisegundos

                texto = f"VERSIÓN COMPUESTA:\nÁrea: {resultado_version_compuesta:.6f} u^2\nTiempo: {tiempo_us:.2f} µ segundos"
                self.lbl_resultado_compuesta.configure(text=texto, text_color="#67995d")

            # Invocar la función que dibuja la gráfica
            self.graficar(funcion_evaluable, a, b, n, usar_simple, usar_compuesta)
        
        except Exception as e:
            self.lbl_resultado_simple.configure(text=f"Error: {str(e)}", text_color="#843232")
    
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