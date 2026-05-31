import numpy as np

def funcion_segura(expresion):
    expresion = expresion.replace('^', '**')
    diccionario = {
        "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp,
        "log": np.log, "sqrt": np.sqrt, "pi": np.pi, "e": np.e
    }
    return lambda x_val: eval(expresion, {"__builtins__": None}, {**diccionario, "x": x_val})

def simpson_rule_simple(f, a, b):
    if a == b:
        return 0.0 # El área de un punto es cero

    fx0 = f(a) # Función evaluada en el límite inferior de la integral definida
    fx1 = f((a + b) / 2) # Función evaluada en un valor intermedio (resta del lím. superior con el lím. inferior de la integral definida entre 2)
    fx2 = f(b) # Función evaluada en el límite superior de la integral definida

    resultado = (b - a) * ((fx0 + (4 * fx1) + fx2) / 6) # Fórmula de Regla de Simpson 1/3 simple
    return resultado

def simpson_rule_compuesta(f, a, b, n):
    if n <= 0:
        raise ValueError("El número de intervalos n debe ser un entero positivo mayor a cero.")

    if(n % 2 != 0): # n debe ser par obligatoriamente
        raise ValueError("Error: El número de intervalos n no es par. Favor de intentarlo de nuevo.")
    
    if a > b:
        raise ValueError("El límite inferior 'a' no puede ser mayor que el límite superior 'b'.")
    
    if a == b:
        return 0.0 # El área de un punto es cero

    # Inicializacion
    delta_x = (b - a) / n    
    resultado = 0.0

    for i in range(0, n + 1):
        xn = a + (i * delta_x) # Cálculo de xn, donde xn = xn-1 + delta de x. En esta línea, la fórmula se adapta con la suma de a con el producto de i por delta de x

        if(i == 0 or i == n): # Si se tiene xn = x0 o xn (donde n es el valor de intervalos delimitados), al resultado se suma la funcion evaluada en xn
            resultado += f(xn)
        elif (i % 2 != 0): # Si i es impar, al resultado se suma la funcion evaluada en xn multiplicada por 4
            resultado += 4 * f(xn)
        else:
            resultado += 2 * f(xn) # Si i es par, al resultado se suma la funcion evaluada en xn multiplicada por 2

    resultado *= (delta_x / 3) # El resultado final es la suma de todo lo anterior multiplicado por delta de x entre 3
    return resultado