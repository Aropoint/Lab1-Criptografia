import sys
import unicodedata

def normalizar_texto(texto):
    # Pasar a minúsculas
    texto = texto.lower()
    # Eliminar tildes y diacríticos
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto

def cesar_cipher(texto, desplazamiento):
    resultado = ""
    for char in texto:
        if char.isalpha():  # Solo cifrar letras
            nueva_pos = (ord(char) - ord('a') + desplazamiento) % 26
            resultado += chr(nueva_pos + ord('a'))
        else:
            resultado += char  # Mantener espacios u otros caracteres
    return resultado

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 lab1.py \"texto a cifrar\" desplazamiento")
        sys.exit(1)

    texto = sys.argv[1]
    desplazamiento = int(sys.argv[2])

    texto_normalizado = normalizar_texto(texto)
    cifrado = cesar_cipher(texto_normalizado, desplazamiento)
    print(cifrado)
