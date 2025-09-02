import sys
import unicodedata
from scapy.all import IP, ICMP, send

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto

def cesar_cipher(texto, desplazamiento):
    resultado = ""
    for char in texto:
        if char.isalpha():  # Solo letras
            nueva_pos = (ord(char) - ord('a') + desplazamiento) % 26
            resultado += chr(nueva_pos + ord('a'))
        else:
            resultado += char  # Mantener espacios
    return resultado

def enviar_icmp_por_caracter(mensaje, destino="8.8.8.8"):
    for char in mensaje:
        paquete = IP(dst=destino)/ICMP()/char.encode()
        send(paquete, verbose=0)
        print(f"Sent 1 packets")
        print(f".")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: sudo python3 lab1.py \"texto a cifrar\" desplazamiento")
        sys.exit(1)

    texto = sys.argv[1]
    desplazamiento = int(sys.argv[2])
    destino = sys.argv[3] if len(sys.argv) == 4 else "8.8.8.8"

    texto_normalizado = normalizar_texto(texto)
    cifrado = cesar_cipher(texto_normalizado, desplazamiento)
    print("Mensaje cifrado:", cifrado)

    print("\nEnviando caracteres por ICMP...")
    enviar_icmp_por_caracter(cifrado, destino)
