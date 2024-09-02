"""
Una herramienta simple que convierte entre diferentes monedas usando tasas de cambio en tiempo real
Esta ha sido mi fuente de información principal: https://medium.com/@solidlucho/tkinter-crea-interfaces-gr%C3%A1ficas-en-python-de-forma-sencilla-50d131f84883 junto a esta: https://exchangeratesapi.io/documentation/
Vamos a utilizar esta API: https://exchangeratesapi.io/?utm_source=envatotuts&utm_medium=ThirdParties&utm_content=Tutorial 
"""

import tkinter as tk
import requests as rq

def calcular_cambio():
    try:
        # Obtener los valores de las entradas y convertirlos a float para la cantidad y a str para las monedas
        from_currency = var1.get()
        to_currency = var2.get()
        amount = float(var3.get())

        # Parámetros para la solicitud
        params = {
            "access_key": api_key,
            "from": from_currency,
            "to": to_currency,
            "amount": amount
        }

        response = rq.get(base_url, params={"access_key": api_key})
        if response.status_code == 200:
            data = response.json()
            rates = data['rates']
            
            # Si la moneda base es EUR, el valor está en la tasa directamente
            if from_currency == "EUR":
                conversion_result = rates[to_currency] * amount
            elif to_currency == "EUR":
                conversion_result = amount / rates[from_currency]
            else:
                # Para cualquier otra conversión no involucrando EUR directamente
                conversion_result = (rates[to_currency] / rates[from_currency]) * amount

            resultado_etiqueta.config(text=f"Resultado: {conversion_result:.2f} {to_currency}")
        else:
            resultado_etiqueta.config(text=f"Error en la solicitud: {response.status_code}")

    except ValueError:
        resultado_etiqueta.config(text="Por favor, ingresa valores numéricos válidos.")
    except Exception as e:
        resultado_etiqueta.config(text=f"Ocurrió un error: {e}")

# Configuración de la API
api_key = "# Introduce tu API Key (consiguela gratis para 250 peticiones en https://exchangeratesapi.io/)"
# base_url = "https://api.exchangeratesapi.io/v1/convert" Esta url no nos funcionaba, nos daba un error 403
base_url = "https://api.exchangeratesapi.io/v1/latest"

# Configuración de la ventana
window = tk.Tk()
window.title("Conversor de divisas en tiempo real")

ancho_pantalla = window.winfo_screenwidth()
alto_pantalla = window.winfo_screenheight()

ancho_ventana = 800
alto_ventana = 600
posicion_x = (ancho_pantalla - ancho_ventana) // 2 
posicion_y = (alto_pantalla - alto_ventana) // 2

window.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

etiqueta = tk.Label(window, text="Cambio de divisas", font=("Arial", 16), fg="green", height=5)
etiqueta.pack()

# Cuadros de texto para el input del usuario
etiqueta_1 = tk.Label(window, text="¿Qué divisa tienes?", font=("Arial", 16), height=1)
etiqueta_1.pack()
var1 = tk.StringVar()
cuadro_texto_1 = tk.Entry(window, width=30, textvariable=var1)
cuadro_texto_1.pack()

etiqueta_2 = tk.Label(window, text="¿A qué divisa quieres convertir?", font=("Arial", 16), height=1)
etiqueta_2.pack()
var2 = tk.StringVar()
cuadro_texto_2 = tk.Entry(window, width=30, textvariable=var2)
cuadro_texto_2.pack()

etiqueta_3 = tk.Label(window, text="¿Cuánto quieres convertir?", font=("Arial", 16), height=1)
etiqueta_3.pack()
var3 = tk.StringVar()
cuadro_texto_3 = tk.Entry(window, width=30, textvariable=var3)
cuadro_texto_3.pack()

resultado_etiqueta = tk.Label(window, text="", font=("Arial", 16), height=2)
resultado_etiqueta.pack()

boton = tk.Button(window, text="Calcular", command=calcular_cambio, height=5, width=60, bg="green")
boton.pack()

window.mainloop()