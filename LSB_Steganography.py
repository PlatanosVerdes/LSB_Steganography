from PIL import Image
from colorama import Fore, Back, Style
import math  # Utilizado sólo para redondear hacia abajo
import os

ENDING_CHARACTER = "11111111"

def oget_lsb(byte):
    return byte[-1]

def get_bin(numero):
    return bin(numero)[2:].zfill(8)

def converter_binario2decimal(binario):
    return int(binario, 2)

def converter_ascii2char(numero):
    return chr(numero)

def get_ascii(caracter):
    return ord(caracter)

def get_bits_list(texto):
    lista = []
    for letra in texto:
        representacion_ascii = get_ascii(letra)
        representacion_binaria = get_bin(representacion_ascii)
        for bit in representacion_binaria:
            lista.append(bit)
    for bit in ENDING_CHARACTER:
        lista.append(bit)
    return lista

def change_last_bit(byte, nuevo_bit):
    return byte[:-1] + str(nuevo_bit)

def modify_color(color_original, bit):
    color_binario = get_bin(color_original)
    color_modificado = change_last_bit(color_binario, bit)
    return converter_binario2decimal(color_modificado)


def hide_text(mensaje, ruta_imagen_original, ruta_imagen_salida):
    print("Ocultando mensaje...".format(mensaje))
    imagen = Image.open(ruta_imagen_original)
    pixeles = imagen.load()

    tamaño = imagen.size
    anchura = tamaño[0]
    altura = tamaño[1]

    lista = get_bits_list(mensaje)
    contador = 0
    longitud = len(lista)
    for x in range(anchura):
        for y in range(altura):
            if contador < longitud:
                pixel = pixeles[x, y]

                rojo = pixel[0]
                verde = pixel[1]
                azul = pixel[2]

                if contador < longitud:
                    rojo_modificado = modify_color(rojo, lista[contador])
                    contador += 1
                else:
                    rojo_modificado = rojo

                if contador < longitud:
                    verde_modificado = modify_color(verde, lista[contador])
                    contador += 1
                else:
                    verde_modificado = verde

                if contador < longitud:
                    azul_modificado = modify_color(azul, lista[contador])
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

def show_text(ruta_imagen):
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
                if byte == ENDING_CHARACTER:
                    break
                mensaje += converter_ascii2char(
                    converter_binario2decimal(byte))
                byte = ""

            byte += oget_lsb(get_bin(verde))
            if len(byte) >= 8:
                if byte == ENDING_CHARACTER:
                    break
                mensaje += converter_ascii2char(
                    converter_binario2decimal(byte))
                byte = ""

            byte += oget_lsb(get_bin(azul))
            if len(byte) >= 8:
                if byte == ENDING_CHARACTER:
                    break
                mensaje += converter_ascii2char(
                    converter_binario2decimal(byte))
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
            num = int(input("Introduce un numero entero: "))
            correcto = True
        except ValueError:
            print(Fore.RED + "Error, introduce un numero entero")
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
    texto = ""
    path = ""
    while not salir:
        #path = os.path.abspath(os.getcwd())
        imagen = ""
        texto = ""
        print(Fore.BLUE + "- LSB - Steganography -")
        print(Style.RESET_ALL)
        print("1. Ocultar mensaje")
        print("2. Leer mensaje")
        print("3. Salir")
        print("")

        opcion = ask_number()

        if opcion == 1:
            texto = input("Texto a ocultar: ")
            imagen = input("Nombre de la imagen con extension: ")
            imagen_salida = extension(input("Nombre de la imagen de salida: "))
            #path = path + "\\" + imagen
            #imagen_salida = "hide"+imagen
            hide_text(texto, imagen, imagen_salida)
        elif opcion == 2:
            imagen = input("Nombre de la imagen con extension: ")
            print("")
            #path = path + "\\" + imagen
            mensaje = show_text(imagen)
            if(mensaje != ""):
                print("El mensaje oculto es:")
                print(Fore.GREEN + mensaje)
            else:
                print(Fore.RED + "No hay ningun mensaje")           
            print(Style.RESET_ALL)
        elif opcion == 3:
            salir = True
        else:
            print("Introduce un numero entre 1 y 3")


if __name__ == "__main__":
    main()
