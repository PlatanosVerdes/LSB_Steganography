from PIL import Image
from colorama import Fore, Back, Style
import math  # Utilizado sólo para redondear hacia abajo
import os #Para obtener path
import docopt #Args

ENDING_CHARACTER = "11111111"

def to_bits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def xor_bit(a,b):
    return a^b

def oget_lsb(byte):
    return byte[-1]

def get_bin(number):
    return bin(number)[2:].zfill(8)

def converter_binary2decimal(binary):
    return int(binary, 2)

def converter_ascii2char(number):
    return chr(number)

def get_ascii(caracter):
    return ord(caracter)

def get_bits_list(text,key):
    list = []
    for character in text:
        representation_ascii = get_ascii(character)
        representation_binaria = get_bin(representation_ascii)
        for bit in representation_binaria:
            list.append(bit)
    for bit in key:
        list.append(bit)
    return list

def change_last_bit(byte, nuevo_bit):
    return byte[:-1] + str(nuevo_bit)

def modify_color(color_original, bit):
    color_binario = get_bin(color_original)
    color_modificado = change_last_bit(color_binario, bit)
    return converter_binary2decimal(color_modificado)


def hide_text(mensaje, ruta_imagen_original, ruta_imagen_salida,key):
    print("Ocultando mensaje...".format(mensaje))
    imagen = Image.open(ruta_imagen_original)
    pixeles = imagen.load()

    tamaño = imagen.size
    anchura = tamaño[0]
    altura = tamaño[1]

    list = get_bits_list(mensaje,key)
    contador = 0
    longitud = len(list)
    for x in range(anchura):
        for y in range(altura):
            if contador < longitud:
                pixel = pixeles[x, y]

                rojo = pixel[0]
                verde = pixel[1]
                azul = pixel[2]

                if contador < longitud:
                    rojo_modificado = modify_color(rojo, list[contador])
                    contador += 1
                else:
                    rojo_modificado = rojo

                if contador < longitud:
                    verde_modificado = modify_color(verde, list[contador])
                    contador += 1
                else:
                    verde_modificado = verde

                if contador < longitud:
                    azul_modificado = modify_color(azul, list[contador])
                    contador += 1
                else:
                    azul_modificado = azul

                pixeles[x, y] = (
                    rojo_modificado, verde_modificado, azul_modificado)
            else:
                break
        else:
            continue
        break

    if contador >= longitud:
        print(Fore.GREEN + "Mensaje escrito correctamente")
    else:
        print(Fore.RED + "Advertencia: no se pudo escribir todo el mensaje, sobraron {} caracteres".format(
            math.floor((longitud - contador) / 8)))

    print("")
    print(Style.RESET_ALL)
    imagen.save(ruta_imagen_salida)

def show_text(ruta_imagen,key):
    imagen = Image.open(ruta_imagen)
    pixeles = imagen.load()

    tamaño = imagen.size
    anchura = tamaño[0]
    altura = tamaño[1]

    byte = ""
    mensaje = ""

    for x in range(anchura):
        for y in range(altura):
            pixel = pixeles[x, y]

            rojo = pixel[0]
            verde = pixel[1]
            azul = pixel[2]

            byte += oget_lsb(get_bin(rojo))
            if len(byte) >= 8:
                if byte == key:
                    break
                mensaje += converter_ascii2char(
                    converter_binary2decimal(byte))
                byte = ""

            byte += oget_lsb(get_bin(verde))
            if len(byte) >= 8:
                if byte == key:
                    break
                mensaje += converter_ascii2char(
                    converter_binary2decimal(byte))
                byte = ""

            byte += oget_lsb(get_bin(azul))
            if len(byte) >= 8:
                if byte == key:
                    break
                mensaje += converter_ascii2char(
                    converter_binary2decimal(byte))
                byte = ""

        else:
            continue
        break
    return mensaje

def ask_number():
    correcto = False
    num = 0
    while(not correcto):
        try:
            num = int(input("Introduce un number entero: "))
            correcto = True
        except ValueError:
            print(Fore.RED + "Error, introduce un number entero")
        print(Style.RESET_ALL)
    return num

def extension(cadena):
    extension = ".png"
    sep = '.'
    rest = cadena.split(sep)
    return rest[0]+extension


def main():
    salir = False
    opcion = 0
    text = ""
    path = ""
    while not salir:
        #path = os.path.abspath(os.getcwd())
        imagen = ""
        text = ""
        print(Fore.BLUE + "- LSB - Steganography -")
        print(Style.RESET_ALL)
        print("1. Ocultar mensaje")
        print("2. Leer mensaje")
        print("3. Salir")
        print("")

        opcion = ask_number()
        if opcion == 1:
            key = ENDING_CHARACTER
            text = input("Texto a ocultar: ")
            imagen = input("Nombre de la imagen con extension: ")
            imagen_salida = extension(input("Nombre de la imagen de salida: "))
            new_key = to_bits(input("Clave: "))
            key = xor_bit(int(ENDING_CHARACTER),new_key[0])
            #key = ''.join(str(x) for x in new_key)
            print(key)
            #path = path + "\\" + imagen
            #imagen_salida = "hide"+imagen
            hide_text(text, imagen, imagen_salida,key)
        elif opcion == 2:
            key = ENDING_CHARACTER
            new_key = to_bits(input("Clave: "))
            #key = ''.join(str(x) for x in new_key)
            imagen = extension(input("Nombre de la imagen con extension: "))
            print("")
            #path = path + "\\" + imagen
            mensaje = show_text(imagen,key)
            if(mensaje != ""):
                print("El mensaje oculto es:")
                print(Fore.GREEN + mensaje)
            else:
                print(Fore.RED + "No hay ningun mensaje")           
            print(Style.RESET_ALL)
        elif opcion == 3:
            salir = True
        else:
            print("Introduce un number entre 1 y 3")


if __name__ == "__main__":
    main()
