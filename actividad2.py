import sys
import unicodedata
import time
from scapy.all import IP, ICMP, send

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")

def cesar_cipher(texto, desplazamiento):
    resultado = ""
    for char in texto:
        if char.isalpha():
            nueva_pos = (ord(char) - ord('a') + desplazamiento) % 26
            resultado += chr(nueva_pos + ord('a'))
        else:
            resultado += char
    return resultado

def enviar_icmp_stealth(mensaje, destino="8.8.8.8"):
    icmp_id = 0x1234   
    seq = 0
    for char in mensaje:
        payload = (
            char.encode() +              # primer byte = char
            b"\x00" * 8 +                # "8 primeros bytes" ICMP coherentes
            bytes(range(0x10, 0x38))     # desde 0x10 a 0x37
        )

        paquete = IP(dst=destino)/ICMP(id=icmp_id, seq=seq)/payload
        send(paquete, verbose=0)
        print(f"Sent 1 packets.")
        print(f".")
        seq += 1
        time.sleep(1)  # simular ping normal

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
    print("\nEnviando caracteres por ICMP stealth...")
    enviar_icmp_stealth(cifrado, destino)
