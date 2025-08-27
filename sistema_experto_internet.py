import tkinter as tk
from tkinter import ttk
import clips

env = clips.Environment()
env.clear()

# Reglas
env.build('(defrule reglaWifi (wifiCaido) => (assert(reiniciarModem)))')
env.build('(defrule reglaDNS (dnsError) => (assert(cambiarDNS)))')
env.build('(defrule reglaGrave (wifiCaido)(dnsError) => (assert(contactarProveedor)))')
env.build('(defrule reglaRouterApagado (routerApagado) => (assert(encenderRouter)))')
env.build('(defrule reglaLucesRojas (lucesRojas) => (assert(revisarRouter)))')


def diagnosticar():
    env.reset()
    salida.delete("1.0", tk.END)

    seleccion = opcion.get()
    if seleccion == "wifiCaido":
        env.assert_string("(wifiCaido)")
    elif seleccion == "dnsError":
        env.assert_string("(dnsError)")
    elif seleccion == "routerApagado":
        env.assert_string("(routerApagado)")
    elif seleccion == "lucesRojas":
        env.assert_string("(lucesRojas)")

    # Mostrar hechos antes de correr
    salida.insert(tk.END, "Hechos:\n")
    for fact in env.facts():
        salida.insert(tk.END, f"- {fact}\n")

    # Mostrar reglas activadas antes de correr
    salida.insert(tk.END, "Reglas activadas:\n")
    for act in env.activations():
        salida.insert(tk.END, f"- {act}\n")

    env.run()

    recomendaciones = []
    for fact in env.facts():
        f = str(fact)
        if "reiniciarModem" in f:
            recomendaciones.append("Reiniciar el módem")
        if "cambiarDNS" in f:
            recomendaciones.append("Cambiar los DNS en la configuración")
        if "contactarProveedor" in f:
            recomendaciones.append("Contactar al proveedor de internet")
        if "encenderRouter" in f:
            recomendaciones.append("Revisa el cable de alimentación de energía")
        if "revisarRouter" in f:
            recomendaciones.append("Revisar el router")

    if recomendaciones:
        salida.insert(tk.END, "Recomendación:\n\n")
        for r in recomendaciones:
            salida.insert(tk.END, f"- {r}\n")
    else:
        salida.insert(tk.END, "No se activó ninguna regla.\n")

def limpiar():
    opcion.set("")
    salida.delete("1.0", tk.END)

root = tk.Tk()
root.title("Sistema Experto - Problemas de Internet")
root.geometry("600x400")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Seleccione el hecho observado:").grid(row=0, column=0, sticky="w")

# Variable de selección única
opcion = tk.StringVar(value="")

ttk.Radiobutton(frame, text="El WiFi está caído", variable=opcion, value="wifiCaido").grid(row=1, column=0, sticky="w", pady=2)
ttk.Radiobutton(frame, text="Error de DNS", variable=opcion, value="dnsError").grid(row=2, column=0, sticky="w", pady=2)
ttk.Radiobutton(frame, text="El router está apagado", variable=opcion, value="routerApagado").grid(row=3, column=0, sticky="w", pady=2)
ttk.Radiobutton(frame, text="Las luces del router están rojas", variable=opcion, value="lucesRojas").grid(row=4, column=0, sticky="w", pady=2)

# Botones
btns = ttk.Frame(frame)
btns.grid(row=5, column=0, pady=10, sticky="w")
ttk.Button(btns, text="Diagnosticar", command=diagnosticar).grid(row=0, column=0, padx=5)
ttk.Button(btns, text="Limpiar", command=limpiar).grid(row=0, column=1, padx=5)

# Área de resultados
salida = tk.Text(frame, width=70, height=10)
salida.grid(row=6, column=0, pady=10)

root.mainloop()
