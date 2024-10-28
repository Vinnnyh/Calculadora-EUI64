import tkinter as tk
import re

def calcular_ipv6():
    direccion_macO = entrada_mac.get()
    if validar_direccion(direccion_macO):
        resultado_text.delete("1.0",tk.END)
        resultado.set("")
        #Eliminar caracteres especiales#
        eliminar_dict = {':':'', '-':'', '.':'', ',':''}
        direccion_macO = entrada_mac.get()
        direccion_macM = direccion_macO.translate(str.maketrans(eliminar_dict))
        resultado_text.insert(tk.END, f"{direccion_macM}\n")
        print(direccion_macM)

        #Cortar direccion y agregar FFFE#
        corte = len(direccion_macM) // 2
        direccion_macM_con_fffe = "".join([direccion_macM[:corte], "FFFE", direccion_macM[corte:]])
        resultado_text.insert(tk.END, f"{direccion_macM_con_fffe}\n")
        print(direccion_macM_con_fffe)

        #agrupar#
        grupos = [direccion_macM_con_fffe[i:i+4] for i in range(0, len(direccion_macM_con_fffe), 4)]
        direccion_mac_dividida = ":".join(grupos)
        resultado_text.insert(tk.END, f"{direccion_mac_dividida}\n")
        print(direccion_mac_dividida)

        #convertir a binario#
        binario_dos_primeros_digitos = bin(int(direccion_mac_dividida[:2], 16))[2:].zfill(8)
        resultado_text.insert(tk.END, f"{binario_dos_primeros_digitos}\n")
        print(binario_dos_primeros_digitos)

        #invertir 0 y 1#
        if binario_dos_primeros_digitos[6] == '0':
            binario_dos_primeros_digitosinv = binario_dos_primeros_digitos[:6] + '1' + binario_dos_primeros_digitos[7:]
        else:
            binario_dos_primeros_digitosinv = binario_dos_primeros_digitos[:6] + '0' + binario_dos_primeros_digitos[7:]
        resultado_text.insert(tk.END, f"{binario_dos_primeros_digitosinv}\n")
        print(binario_dos_primeros_digitosinv)

        #convertir a hexa#
        hexa = hex(int(binario_dos_primeros_digitosinv, 2))[2:].zfill(2)

        direccion_ipv6 = hexa + direccion_mac_dividida[2:]
        print(direccion_ipv6)
        resultado.set(direccion_ipv6)

        boton_copiar.pack(pady=5)
    else:
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, "Ingrese una direccion válida")
        resultado.set("")
def validar_direccion(direccion_mac):
    patron = re.compile(r'^(([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}|([0-9A-Fa-f]{4}[.]){2}[0-9A-Fa-f]{4}|[0-9A-Fa-f]{12})$')
    return bool(re.match(patron, direccion_mac))

def copiar_ipv6():
    pyperclip.copy(resultado.get())

# Creación Tkinter
root = tk.Tk()
root.title("Calculadora EUI-64")
root.geometry("450x480")
root.resizable(False, False)
root.configure(bg="#e6e6e6")  

fuente = ("Arial", 12)
color_boton = "#697aba"
color_letra_boton = "white"
color_marco_entrada = "#c0c0c0"

etiqueta_mac = tk.Label(root, text="Dirección MAC:", bg="#e6e6e6", font=fuente)
etiqueta_mac.pack(pady=(20, 5))

entrada_mac = tk.Entry(root, justify="center", font=fuente, bg=color_marco_entrada)
entrada_mac.pack(pady=5)

boton_calcular = tk.Button(root, text="Calcular IPv6", command=calcular_ipv6, width=20, bg=color_boton, fg=color_letra_boton, font=fuente)
boton_calcular.pack(pady=10)

resultado_text = tk.Text(root, height=7, width=22, font=fuente, bg=color_marco_entrada)
resultado_text.pack(pady=10)

resultado = tk.StringVar()

resultado_label = tk.Label(root, textvariable=resultado, bg="#e6e6e6", font=fuente)
resultado_label.pack(pady=5)

boton_copiar = tk.Button(root, text="Copiar", command=copiar_ipv6, bg=color_boton, fg=color_letra_boton, font=fuente)
boton_copiar.pack_forget()

root.mainloop()