import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

def ajustar_brillo_contraste(imagen, brillo=0, contraste=0):
        if brillo != 0:
            if brillo > 0:
                shadow = brillo
                max = 255
            else:
                shadow = 0
                max = 255 + brillo
            alpha_b = (max - shadow) / 255
            gamma_b = shadow

            buf = cv2.addWeighted(imagen, alpha_b, imagen, 0, gamma_b)
        else:
            buf = imagen.copy()

        if contraste != 0:
            f = 131 * (contraste + 127) / (127 * (131 - contraste))
            alpha_c = f
            gamma_c = 127 * (1 - f)

            buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

        return buf
    
def convertir_escala_grises():
    if imagen is not None:
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        mostrar_imagen_cv(gris, panel_ajustado)

def suavizar_imagen():
    if imagen is not None:
        valor = suavizar_slider.get()
        suavizada = cv2.GaussianBlur(imagen, (valor, valor), 0)
        mostrar_imagen_cv(suavizada, panel_ajustado)
        
def aplicar_filtro_bilateral():
    if imagen is not None:
        valor = bilateral_slider.get()
        filtrada = cv2.bilateralFilter(imagen, valor, 75, 75)
        mostrar_imagen_cv(filtrada, panel_ajustado)
        
def aplicar_apertura():
    if imagen is not None:
        kernel_size = apertura_slider.get()
        if kernel_size % 2 == 0:
            kernel_size += 1
        imagen_apertura = realizar_apertura(imagen, kernel_size)
        mostrar_imagen_cv(imagen_apertura, panel_ajustado)

def detectar_bordes():
    if imagen is not None:
        valor = bordes_slider.get()
        bordes = cv2.Canny(imagen, valor, valor * 2)
        mostrar_imagen_cv(bordes, panel_ajustado)

def aplicar_ajuste():
    if imagen is not None:
        brillo = brillo_slider.get()
        contraste = contraste_slider.get()
        imagen_ajustada = ajustar_brillo_contraste(imagen, brillo, contraste)
        mostrar_imagen_cv(imagen_ajustada, panel_ajustado)
        
def aplicar_grises():
    if imagen is not None:
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        mostrar_imagen_cv(gris, panel_ajustado)
        
def aplicar_suavizado():
    if imagen is not None:
        valor = suavizar_slider.get()
        if valor % 2 == 0:
            valor += 1
        suavizada = cv2.GaussianBlur(imagen, (valor, valor), 0)
        mostrar_imagen_cv(suavizada, panel_ajustado)

def aplicar_cierre():
    if imagen is not None:
        kernel_size = cierre_slider.get()
        if kernel_size % 2 == 0:
            kernel_size += 1
        imagen_cierre = realizar_cierre(imagen, kernel_size)
        mostrar_imagen_cv(imagen_cierre, panel_ajustado)

def aplicar_erosion():
    if imagen is not None:
        kernel_size = erosion_slider.get()
        if kernel_size % 2 == 0:
            kernel_size += 1
        imagen_erosionada = realizar_erosion(imagen, kernel_size)
        mostrar_imagen_cv(imagen_erosionada, panel_ajustado)

def aplicar_dilatacion():
    if imagen is not None:
        kernel_size = dilatacion_slider.get()
        if kernel_size % 2 == 0:
            kernel_size += 1
        imagen_dilatada = realizar_dilatacion(imagen, kernel_size)
        mostrar_imagen_cv(imagen_dilatada, panel_ajustado)

def realizar_apertura(imagen, kernel_size):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    apertura = cv2.morphologyEx(imagen, cv2.MORPH_OPEN, kernel)
    return apertura

def realizar_cierre(imagen, kernel_size):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    cierre = cv2.morphologyEx(imagen, cv2.MORPH_CLOSE, kernel)
    return cierre

def realizar_dilatacion(imagen, kernel_size):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    dilatada = cv2.dilate(imagen, kernel, iterations=1)
    return dilatada

def realizar_erosion(imagen, kernel_size):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    erosionada = cv2.erode(imagen, kernel, iterations=1)
    return erosionada

def cargar_imagen():
    global imagen, imagen_path
    imagen_path = filedialog.askopenfilename()
    if imagen_path:
        imagen = cv2.imread(imagen_path, cv2.IMREAD_COLOR)
        mostrar_imagen_cv(imagen, panel_original)
        
def actualizar_brillo_contraste(val):
    brillo = brillo_slider.get()
    contraste = contraste_slider.get()
    imagen_ajustada = ajustar_brillo_contraste(imagen, brillo, contraste)
    mostrar_imagen_cv(imagen_ajustada, panel_ajustado)

def mostrar_imagen_cv(imagen, panel):
    imagen_tk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)))
    panel.config(image=imagen_tk)
    panel.image = imagen_tk

root = Tk()
root.title("Segmentador de Grietas")

panel_original = Label(root)
panel_original.grid(row=0, column=0, padx=10, pady=10)

panel_ajustado = Label(root)
panel_ajustado.grid(row=0, column=1, padx=10, pady=10)

btn_cargar = Button(root, text="Cargar Imagen", command=cargar_imagen)
btn_cargar.grid(row=1, column=0)

# panel_segmentada = Label(root)
# panel_segmentada.grid(row=0, column=2, padx=10, pady=10)

brillo_slider = Scale(root, from_=-100, to=100, orient=HORIZONTAL, command=actualizar_brillo_contraste, label="Brillo")
brillo_slider.grid(row=1, column=1)
contraste_slider = Scale(root, from_=-100, to=100, orient=HORIZONTAL, command=actualizar_brillo_contraste, label="Contraste")
contraste_slider.grid(row=1, column=2)
btn_ajuste = Button(root, text="Aplicar Ajuste", command=aplicar_ajuste)
btn_ajuste.grid(row=1, column=3)

btn_grises = Button(root, text="Escala de Grises", command=aplicar_grises)
btn_grises.grid(row=2, column=0)

suavizar_slider = Scale(root, from_=1, to=10, orient=HORIZONTAL, label="Suavizar")
suavizar_slider.grid(row=2, column=1)
btn_suavizar = Button(root, text="Suavizar Imagen", command=aplicar_suavizado)
btn_suavizar.grid(row=2, column=2)

apertura_slider = Scale(root, from_=1, to=10, orient=HORIZONTAL, label="Apertura")
apertura_slider.grid(row=5, column=1)
btn_apertura = Button(root, text="Aplicar Apertura", command=aplicar_apertura)
btn_apertura.grid(row=5, column=2)

cierre_slider = Scale(root, from_=1, to=10, orient=HORIZONTAL, label="Cierre")
cierre_slider.grid(row=6, column=1)
btn_cierre = Button(root, text="Aplicar Cierre", command=aplicar_cierre)
btn_cierre.grid(row=6, column=2)

erosion_slider = Scale(root, from_=1, to=10, orient=HORIZONTAL, label="Erosión")
erosion_slider.grid(row=7, column=1)
btn_erosion = Button(root, text="Aplicar Erosión", command=aplicar_erosion)
btn_erosion.grid(row=7, column=2)

dilatacion_slider = Scale(root, from_=1, to=10, orient=HORIZONTAL, label="Dilatación")
dilatacion_slider.grid(row=8, column=1)
btn_dilatacion = Button(root, text="Aplicar Dilatación", command=aplicar_dilatacion)
btn_dilatacion.grid(row=8, column=2)
#/Users/aldoescamillaresendiz/Downloads/PDIGrietas.py/Users/aldoescamillaresendiz/Downloads/PDIGrietas.py
root.mainloop()