import sys
import unicodedata
from scapy.all import rdpcap, ICMP

# Lista básica de palabras comunes en español
PALABRAS_COMUNES = {
    "el", "la", "los", "las", "de", "y", "en", "un", "una", "que", "se", "por", "con",
    "para", "no", "sí", "si", "del", "al", "lo", "como", "más", "pero", "su", "sus"
}

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")

def descifrar(texto, desplazamiento):
    resultado = ""
    for char in texto:
        if char.isalpha():
            nueva_pos = (ord(char) - ord('a') - desplazamiento) % 26
            resultado += chr(nueva_pos + ord('a'))
        else:
            resultado += char
    return resultado

def evaluar_probabilidad(texto):
    palabras = texto.split()
    comunes = sum(1 for p in palabras if p in PALABRAS_COMUNES)
    return comunes

def colorear_verde(texto):
    return f"\033[92m{texto}\033[0m"  # ANSI verde

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: sudo python3 read.py cesar.pcapng")
        sys.exit(1)

    archivo_pcap = sys.argv[1]

    # Leer paquetes desde el archivo pcapng
    packets = rdpcap(archivo_pcap)
    mensaje_cifrado = []

    for pkt in packets:
        if ICMP in pkt and pkt[ICMP].type == 8:  # Echo Request
            data = bytes(pkt[ICMP].payload)
            if data:
                try:
                    char = data.decode(errors="ignore")
                    mensaje_cifrado.append(char)
                except:
                    pass

    mensaje = "".join(mensaje_cifrado)
    mensaje = normalizar_texto(mensaje)

    print("Mensaje cifrado recibido:", mensaje)

    # Generar todas las combinaciones posibles (desplazamientos 1-25)
    resultados = []
    for d in range(1, 26):
        desc = descifrar(mensaje, d)
        score = evaluar_probabilidad(desc)
        resultados.append((d, desc, score))

    # Seleccionar la mejor opción
    mejor = max(resultados, key=lambda x: x[2])

    print("\nPosibles mensajes (desplazamientos 1-25):\n")
    with open("posibles_mensajes.txt", "w", encoding="utf-8") as f:
        for d, desc, score in resultados:
            if d == mejor[0]:
                print(colorear_verde(f"Desplazamiento {d}: {desc}"))
                f.write(f"* Desplazamiento {d}: {desc}\n")
            else:
                print(f"Desplazamiento {d}: {desc}")
                f.write(f"Desplazamiento {d}: {desc}\n")

    print("\nResultados guardados en 'posibles_mensajes.txt'")
