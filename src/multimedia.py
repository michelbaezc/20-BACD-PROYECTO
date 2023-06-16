import webbrowser as wb
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import pyautogui
import subprocess
import time
import requests
import keyboard
import pygame
import cv2
import os
import re
import subprocess
from pyudev import Context, Monitor, MonitorObserver
import threading
import numpy as np
import pyttsx3
from PIL import Image, ImageTk

#Definicion del color de fondo
colorFondo="#061848"

# Creación de ventana principal
window = tk.Tk()
window.config(bg=colorFondo, cursor="circle")
# Pygame para reproducir musica
pygame.mixer.init()

# Largo y ancho de la ventana
width  = window.winfo_screenwidth()
height = window.winfo_screenheight()

# Creación de funciones para cada servicio de streaming
def funcion_Netflix():
    command = "chromium-browser --kiosk https://www.netflix.com/mx"
    subprocess.call(command, shell=True)

def funcion_Amazon():
    command = "chromium-browser --kiosk https://www.primevideo.com"
    subprocess.call(command, shell=True)

def funcion_Disney():
    command = "chromium-browser --kiosk https://www.disneyplus.com/es-mx"
    subprocess.call(command, shell=True)

def funcion_Spotify():
    command = "chromium-browser --kiosk https://www.open.spotify.com"
    subprocess.call(command, shell=True)

def funcion_HBO():
    command = "chromium-browser --kiosk https://www.hbomax.com/mx/es"
    subprocess.call(command, shell=True)

def funcion_Youtube():
    command = "chromium-browser --kiosk https://www.youtube.com"
    subprocess.call(command, shell=True)    
    
def pantCompleta():
    pyautogui.press("F11")

def apagar():
    subprocess.call(['shutdown', "-h", "now"])

def funcion_Salir():
    labelSalir = Label(window, text="Hasta pronto.",
             fg="#fff",    # Foreground
             bg=colorFondo,   # Background
             font=("Verdana Bold",60))
    labelSalir.place(relx=0, rely=0, relheight=1, relwidth=1)
    window.after(5000, apagar)

def reinicio():
    subprocess.run(["reboot"])

def obtener_redes_wifi():
    # Comando para obtener la lista de redes Wi-Fi disponibles
    comando = 'sudo iwlist wlan0 scan'
    
    # Ejecutar el comando en la terminal y capturar la salida
    resultado = subprocess.check_output(comando, shell=True, text=True)
    
    # Buscar los SSID en la salida utilizando expresiones regulares
    ssids = re.findall(r'ESSID:"(.*?)"', resultado)
    
    return ssids

def conectarRed(ssid, password):
    global labelConfig
    
    arch = '/etc/wpa_supplicant/wpa_supplicant.conf'
    subprocess.call(['sudo', "chmod", "777", arch])
    
    with open(arch, 'w') as fp:
                    fp.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev')
    with open(arch, 'a') as fp:
                    fp.write('\nupdate_config=1')
    with open(arch, 'a') as fp:
                    fp.write('\ncountry=MX')
    with open(arch, 'a') as fp:
                    fp.write('\nnetwork={ \n')
    with open(arch, 'a') as fp:
                    fp.write('\tssid="{}" \n'.format(str(ssid)))
    with open(arch, 'a') as fp:
                    fp.write('\tpsk="{}" \n'.format(str(password)))    
    with open(arch, 'a') as fp:
                    fp.write('\tkey_mgmt=WPA-PSK')
    with open(arch, 'a') as fp:
                    fp.write('\n}')
    labelConfig = Label(window, text="Aplicando configuración\nRequiere reiniciar",
                    fg="#fff",    # Foreground
                    bg=colorFondo,   # Background
                    font=("Verdana Bold",60))
    labelConfig.place(relx=0, rely=0, relwidth=1, relheight=1)
    window.after(4000, reinicio)


def configRed():
    labelTitulo = Label(window, text="Configuracion de Red",
             fg="#fff",    # Foreground
             bg=colorFondo,   # Background
             font=("Verdana Bold",60))
    labelTitulo.place(relx=0.3, rely=0.05)
    botonClose.place(relx=0.9, rely=0.9) # Posición del botón de cerrar

    # Llamado de cada botón
    botonNetflix.place_forget()
    botonAmazon.place_forget()
    botonDisney.place_forget()
    botonSpotify.place_forget()
    botonHBO.place_forget()
    botonYoutube.place_forget()
    botonConfig.place_forget()
    botonSalir.place_forget()
    botonUsb.place_forget()
    botonNoUsb.place_forget()

    #Label para mostrar las redes disponibles
    ssid_label.pack()
    ssid_label.place(relx=0.25, rely=0.35) 
    redes_wifi = obtener_redes_wifi()
    
    for red in redes_wifi:
        ssid_listbox.insert(tk.END, red)
    ssid_listbox.pack()
    ssid_listbox.place(relx=0.45, rely=0.25, relwidth=0.25)

    # Etiqueta y campo de texto para la contraseña
     
    password_label.pack()
    password_label.place(relx=0.25, rely=0.55)
    
    password_entry.pack()
    password_entry.place(relx=0.45, rely=0.55, relheight=0.05, relwidth=0.25)

    # Botón para conectar a Internet
    botonConectar.pack()
    botonConectar.place(relx=0.4, rely=0.75, relheight=0.1, relwidth=0.2)

    # Etiqueta para mostrar el resultado
    resultado_label = tk.Label(window, text="")
    resultado_label.pack()

def funcion_Usb():
    # Llamado de cada botón
    botonNetflix.place_forget()
    botonAmazon.place_forget()
    botonDisney.place_forget()
    botonSpotify.place_forget()
    botonHBO.place_forget()
    botonYoutube.place_forget()
    botonConfig.place_forget()
    botonSalir.place_forget()
    botonUsb.place_forget()
    botonNoUsb.place_forget()
    labelBienvenida.place_forget()
    botonConectar.place_forget()
    
    gui = GUI()
    gui.root.mainloop()

class GUI:
    def __init__(self):
        self.root = window
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.geometry("500x500")
        self.root.title("Reproductor Multimedia")

        self.media_type_var = tk.StringVar()
        self.media_type_var.set("Seleccione el tipo de archivo")

        # Cargar las imágenes
        self.music_image = Image.open("/home/pi/Desktop/RASPBERRY/proyecto/iconos/musica.png")  # Reemplaza "music_icon.png" con tu propia imagen
        self.photos_image = Image.open("/home/pi/Desktop/RASPBERRY/proyecto/iconos/fotos.png")  # Reemplaza "photos_icon.png" con tu propia imagen
        self.videos_image = Image.open("/home/pi/Desktop/RASPBERRY/proyecto/iconos/video.png")  # Reemplaza "videos_icon.png" con tu propia imagen


        # Convertir las imágenes a PhotoImage
        self.music_photo = ImageTk.PhotoImage(self.music_image)
        self.photos_photo = ImageTk.PhotoImage(self.photos_image)
        self.videos_photo = ImageTk.PhotoImage(self.videos_image)

        # Crear los botones con las imágenes
        music_button = tk.Button(self.root, image=self.music_photo, borderwidth=0, bg=colorFondo, cursor="X_cursor",command=lambda: self.check_usb("Música"))
        music_button.pack()

        photos_button = tk.Button(self.root, image=self.photos_photo, borderwidth=0, bg=colorFondo, cursor="X_cursor", command=lambda: self.check_usb("Fotos"))
        photos_button.pack()

        videos_button = tk.Button(self.root, image=self.videos_photo, borderwidth=0, bg=colorFondo, cursor="X_cursor", command=lambda: self.check_usb("Videos"))
        videos_button.pack()
        
        music_button.place  (relx=0.2,  rely=0.4)
        photos_button.place  (relx=0.45, rely=0.4)
        videos_button.place  (relx=0.7,  rely=0.4)
        botonClose.pack()
        botonClose.place(relx=0.9, rely=0.9) # Posición del botón de cerrar

        self.media_playing = False
        self.media_thread = None
    
    def exit_fullscreen(self, event):
        self.root.attributes("-fullscreen", False)

    def check_usb(self,media_type):

        # Verificar si una USB está conectada
        usb_path = "/media/pi"  # Ruta donde se montan las USB en Raspberry Pi
        usb_files = os.listdir(usb_path)

        if len(usb_files) > 0:
            usb = os.path.join(usb_path, usb_files[0])

            if media_type == "Música":
                self.media_thread = threading.Thread(target=self.play_music, args=(usb,))
                self.media_thread.start()
            elif media_type == "Fotos":
                self.media_thread = threading.Thread(target=self.show_images, args=(usb,))
                self.media_thread.start()
            elif media_type == "Videos":
                self.media_thread = threading.Thread(target=self.play_videos, args=(usb,))
                self.media_thread.start()

            self.media_playing = True
            self.media_thread.start()


    def show_images(self, usb):
        image_files = []

        for file in os.listdir(usb):
            if file.endswith((".jpg", ".png")):
                image_files.append(file)

        while self.media_playing:
            for file in image_files:
                if not self.media_playing:
                    break

                image_path = os.path.join(usb, file)
                self.show_image(image_path)
                
    def show_image(self, image_path):
        image = cv2.imread(image_path)
        cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Image", image)
        key = cv2.waitKey(3000)  # Muestra cada imagen durante 3 segundos

        if key == ord("q"):
            self.media_playing = False
        cv2.destroyAllWindows()

    def play_videos(self, usb):
        video_files = []

        for file in os.listdir(usb):
            if file.endswith((".mp4", ".avi")):
                video_files.append(file)

        while self.media_playing:
            for file in video_files:
                if not self.media_playing:
                    break

                video_path = os.path.join(usb, file)
                self.play_video(video_path)
    
    def play_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        screen_width, screen_height = pyautogui.size()

        cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.resizeWindow("Video", screen_width, screen_height)

        self.stop_event = threading.Event()
        self.stop_event.clear()
        
        def stop_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.stop_event.set()

        cv2.setMouseCallback("Video", stop_callback)

        while cap.isOpened() and self.media_playing and not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                break

            frame_height, frame_width, _ = frame.shape
            frame_ratio = frame_width / frame_height

            if frame_ratio > screen_width / screen_height:
                target_width = screen_width
                target_height = int(screen_width / frame_ratio)
            else:
                target_width = int(screen_height * frame_ratio)
                target_height = screen_height

            margin_x = (screen_width - target_width) // 2
            margin_y = (screen_height - target_height) // 2

            display = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
            resized_frame = cv2.resize(frame, (target_width, target_height))
            display[margin_y:margin_y + target_height, margin_x:margin_x + target_width] = resized_frame

            cv2.imshow("Video", display)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.media_playing = False
                break

        cap.release()
        cv2.destroyAllWindows()

    def stop_media(self):
        self.media_playing = False
        if self.media_thread:
            self.media_thread.join()
        cap.release()
        cv2.destroyAllWindows()
    
    def play_music(self, usb):
        music_files = []

        for file in os.listdir(usb):
            if file.endswith(".mp3"):
                music_files.append(file)

        while self.media_playing:
            for file in music_files:
                if not self.media_playing:
                    break

                music_path = os.path.join(usb, file)
                pygame.mixer.init()
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy() and self.media_playing:
                    continue

def principal():
    global botonConectar
    try:
        request = requests.get("http://www.google.com", timeout=5)
    except (requests.ConnectionError, requests.Timeout):
        labelWifi = Label(window, image=img_nowifi,
                       bg=colorFondo)
    else:
        labelWifi = Label(window, image=img_wifi,
                       bg=colorFondo)
    labelWifi.place(relx=0.95, rely=0.05)

    labelTitulo.place(relx=0.3, rely=0.05)
    
    def detectar_usb(observer, device):
        usb_conectada = False

        for dev in context.list_devices(subsystem='block', DEVTYPE='disk'):
            if dev.get('ID_BUS') == 'usb':
                usb_conectada = True
                break

        if usb_conectada:
            botonNoUsb.place_forget()
            botonUsb.pack()
            botonUsb.place(relx=0.2, rely=0.7)
            
        else:
            botonUsb.place_forget()
            botonNoUsb.pack()
            botonNoUsb.place(relx=0.2, rely=0.7)
      
    # Crear un objeto Context de pyudev
    context = Context()

    # Crear un monitor para detectar eventos de cambio en los dispositivos
    monitor = Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block')

    # Verificar el estado inicial de la USB
    usb_conectada = False
    for device in context.list_devices(subsystem='block', DEVTYPE='disk'):
        if device.get('ID_BUS') == 'usb':
            usb_conectada = True
            botonNoUsb.place_forget()
            botonUsb.pack()
            botonUsb.place   (relx=0.2, rely=0.7)
            break

    # Crear un observador para monitorear los eventos de cambio
    observer = MonitorObserver(monitor, detectar_usb)
    observer.start()

    # Actualizar el estado si la USB ya está conectada
    if usb_conectada:
        botonNoUsb.place_forget()
        botonUsb.pack()
        botonUsb.place   (relx=0.2, rely=0.7)
    else:
        botonUsb.place_forget()
        botonNoUsb.pack()
        botonNoUsb.place   (relx=0.2, rely=0.7)
    # Llamado de cada botón
    botonNetflix.pack   ()
    botonAmazon.pack    ()
    botonDisney.pack    ()
    botonSpotify.pack   ()
    botonHBO.pack       ()
    botonYoutube.pack   ()
    botonSalir.pack     ()
    

    botonNetflix.place  (relx=0.2,  rely=0.15)
    botonAmazon.place   (relx=0.45, rely=0.15)
    botonDisney.place   (relx=0.7,  rely=0.15)
    botonHBO.place      (relx=0.2,  rely=0.4)
    botonSpotify.place  (relx=0.45, rely=0.4)
    botonYoutube.place  (relx=0.7,  rely=0.4)
    botonConfig.place   (relx=0.45, rely=0.7)
    botonSalir.place    (relx=0.7, rely=0.7) 

    #Se oculta la pagina de bienvenida
    labelBienvenida.place_forget()
    #conectar_button.place_forget()
    botonClose.place_forget()
    ssid_listbox.place_forget()
    password_entry.place_forget()
    ssid_label.place_forget()
    password_label.place_forget()
    botonConectar.place_forget()

img_netflix = tk.PhotoImage(file="./iconos/netflix.png")
img_prime   = tk.PhotoImage(file="./iconos/prime.png")
img_disney  = tk.PhotoImage(file="./iconos/disney.png")
img_spotify = tk.PhotoImage(file="./iconos/spotify.png")
img_hbo     = tk.PhotoImage(file="./iconos/hbo.png")
img_youtube = tk.PhotoImage(file="./iconos/youtube.png")
img_config  = tk.PhotoImage(file="./iconos/config.png")
img_salir   = tk.PhotoImage(file="./iconos/salir.png")
img_wifi    = tk.PhotoImage(file="./iconos/wifi.png")
img_nowifi  = tk.PhotoImage(file="./iconos/nowifi.png")
img_usb  = tk.PhotoImage(file="./iconos/usb.png")
img_nousb  = tk.PhotoImage(file="./iconos/no_usb.png")
img_musica  = tk.PhotoImage(file="./iconos/musica.png")
img_fotos  = tk.PhotoImage(file="./iconos/fotos.png")
img_video  = tk.PhotoImage(file="./iconos/video.png")

# Creación de los botones
botonConectar = tk.Button(window, text="Conectar",
                          cursor="X_cursor",
                          command=lambda:conectarRed(ssid_listbox.get(tk.ACTIVE), password_entry.get()))

botonNetflix = tk.Button(window, image=img_netflix,
                         borderwidth=0, bg=colorFondo,
                         cursor="X_cursor",
                         command = funcion_Netflix)

botonAmazon = tk.Button(window, image=img_prime,
                         borderwidth=0, bg=colorFondo,
                         cursor="X_cursor",
                        command = funcion_Amazon)

botonDisney = tk.Button(window, image=img_disney,
                         borderwidth=0, bg=colorFondo,
                         cursor="X_cursor",
                        command = funcion_Disney)

botonSpotify = tk.Button(window, image=img_spotify,
                         borderwidth=0, bg=colorFondo,
                         cursor="X_cursor",
                         command = funcion_Spotify)

botonHBO = tk.Button(window, image=img_hbo,
                         borderwidth=0, bg=colorFondo,
                         cursor="X_cursor",
                         command = funcion_HBO)    

botonYoutube = tk.Button(window, image=img_youtube,
                         borderwidth=0, bg=colorFondo,
                         cursor="X_cursor",
                         command = funcion_Youtube)   

botonConfig = tk.Button(window, image=img_config,
                         borderwidth=0, bg=colorFondo,
                         cursor="X_cursor",
                         command = configRed)

botonSalir = tk.Button(window, image=img_salir,
                         borderwidth=0, bg=colorFondo,
                         cursor="X_cursor",
                         command = funcion_Salir)

botonUsb = tk.Button(window, image=img_usb,
                         borderwidth=0, bg=colorFondo,
                         cursor="X_cursor",
                         command = funcion_Usb)

botonNoUsb = tk.Label(window, image=img_nousb,
                         borderwidth=0, bg=colorFondo,
                         cursor="X_cursor")
                        

botonMusica = tk.Button(window, image=img_musica,
                         borderwidth=0, bg=colorFondo,
                         cursor="X_cursor")
                         #command = funcion_Musica)

botonFotos = tk.Button(window, image=img_fotos,
                         borderwidth=0, bg=colorFondo,
                         cursor="X_cursor")

botonVideo = tk.Button(window, image=img_video,
                         borderwidth=0, bg=colorFondo,
                         cursor="X_cursor")

botonClose = tk.Button(window,
                            text = "Volver",
                            command = principal,
                            bg="#000",  
                            borderwidth= 0.1,
                            fg="#fff",
                            cursor="X_cursor",
                            font=("Verdana Bold", 18))

ssid_label = tk.Label(window, text="Red Wi-Fi:",
                          fg="#fff",    # Foreground
                          bg=colorFondo,   # Background
                          font=("Verdana Bold",40))

ssid_listbox = tk.Listbox(window, fg="#fff",    # Foreground
                      bg=colorFondo,   # Background
                      cursor="X_cursor",
                      font=("Verdana Bold",14))

password_label = tk.Label(window, text="Contraseña:",
                    fg="#fff",    # Foreground
                    bg=colorFondo,   # Background
                    font=("Verdana Bold",40))

password_entry = tk.Entry(window, show="*")

                

#Creacion de los label
labelBienvenida = Label(window, text="Bienvenido",
                        fg="#fff",    # Foreground
                        bg=colorFondo,   # Background
                        font=("Verdana Bold",60))

labelTitulo = Label(window, text="Centro Multimedia",
                    fg="#fff",    # Foreground
                    bg=colorFondo,   # Background
                    font=("Verdana Bold",60))

# Geometria de la ventana
window.geometry("%dx%d" % (width, height))
# Atributos de la ventana, en este caso tiene que ser en pantalla completa
window.attributes('-fullscreen', True)
# Nombre de la ventana
window.title("Multimedia Center")

#label = tk.Label(window, text = "Hello")
#label.pack()

labelBienvenida.place(relx=0, rely=0, relheight=1, relwidth=1)
window.after(4000, principal)

window.mainloop()
