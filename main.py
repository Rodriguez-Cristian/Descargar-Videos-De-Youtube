import tkinter as tk
from pytube import YouTube  # Importa la clase YouTube de la biblioteca pytube 
#----->pip install pytube
import webbrowser  # Importa el módulo webbrowser para abrir URLs en el navegador
import requests  # Importa el módulo requests para hacer solicitudes HTTP
#----->pip install requests
import json  # Importa el módulo json para trabajar con datos en formato JSON
import re #soporte expresiones regulares
from tkinter import messagebox
import os #para usar carpetas
#import ttkboostrap as tkk

class YouTubeDownloader:
    def __init__(self, master):
        self.master = master
        self.master.title("Descargar Videos De Youtube")  # Establece el título de la ventana principal

        # Crear y configurar widgets (etiquetas, campos de entrada y botones)
        self.label_search = tk.Label(master, text="Introduce el nombre del video de YouTube:",font=('Calibri',15))  # Etiqueta para la entrada del nombre del video
        self.label_search.grid(row=0,column=0,padx=5,pady=5)  # Empaqueta la etiqueta en la ventana

        self.entry_search = tk.Entry(master, width=50,justify="center")  # Campo de entrada para el nombre del video
        self.entry_search.grid(row=1,column=0,padx=10,pady=10)  # Empaqueta el campo de entrada en la ventana

        # Botón para buscar y abrir el video en YouTube
        self.button_search = tk.Button(master, text="Buscar Video", command=self.search_and_open_video,width=50)
        self.button_search.grid(row=2,column=0,padx=5,pady=5)  # Empaqueta el botón en la ventana

        # Variable de instancia para almacenar la URL del video
        self.video_url = None

        # Variable de instancia para almacenar el nombre del video (usado para búsqueda)
        self.video_name = None
        
        # Botón para descargar el video
        self.button_download = tk.Button(master, text="Descargar Video", command=self.download_video,width=50)
        self.button_download.grid(row=3,column=0,padx=5,pady=5)  # Empaqueta el botón en la ventana

    # Método para buscar y abrir un video en YouTube
    def search_and_open_video(self):
        self.video_name = self.entry_search.get()  # Obtiene el nombre del video ingresado por el usuario
        if self.video_name:
            video_id = self.search_video_id(self.video_name)  # Busca el ID del video en YouTube
            if video_id:
                self.video_url = f"https://www.youtube.com/watch?v={video_id}"  # Almacena la URL del video
                webbrowser.open(self.video_url)  # Abre la URL en el navegador web predeterminado
            else:
                error_message = "No se encontró ningún video con ese nombre."
                messagebox.showerror("Error", error_message)
        else:
            error_message = "Por favor, introduce el nombre del video."
            messagebox.showerror("Error", error_message)

    # Método para buscar el ID de un video en YouTube
    def search_video_id(self, video_name):
        api_key = "ACA VA SU CLAVE DE API"  # Clave de la API de YouTube (debes reemplazarla con tu propia clave)
        params = {
            "key": api_key, #Clave
            "q": video_name, #Nombre del video
            "part": "snippet", #Clave especifica para incluir el video
            "type": "video", #indicamos que busco un video en youtube
            "maxResults": 2 # aca pongo la cantidad de resultados que quiero
        }
        search_url = "https://www.googleapis.com/youtube/v3/search"  # URL de la API de búsqueda de YouTube
        response = requests.get(search_url, params=params)  # Realiza una solicitud GET a la API de YouTube
        data = json.loads(response.text)  # Convierte la respuesta JSON en un diccionario de Python
        if "items" in data and len(data["items"]) > 0:
            video_id = data["items"][0]["id"]["videoId"]  # Extrae el ID del primer video encontrado
            return video_id
        else:
            return None

    

    # Método para descargar un video de YouTube
    def download_video(self):
        self.search_and_open_video()  # Buscar y abrir el video para obtener la URL
        
        if self.video_url:  # Verifica si se ha almacenado una URL
            try:
                yt = YouTube(self.video_url)  # Crea una instancia de la clase YouTube con la URL del video
                video = yt.streams.get_highest_resolution()  # Obtiene la mejor resolución disponible del video
                
                # Crear la carpeta 'videos' si no existe
                if not os.path.exists('videos'):
                    os.makedirs('videos')

                # Obtener el nombre del archivo sin la extensión
                video_name = video.title
                # Reemplazar caracteres no permitidos en los nombres de archivo
                video_name = video_name.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
                # Crear la ruta completa del archivo
                file_path = os.path.join('videos', f'{video_name}.mp4')
                
                print("Descargando:", video.title)  # Imprime el título del video que se está descargando
                video.download(output_path='videos', filename=f'{video_name}.mp4')  # Descarga el video en la carpeta 'videos' con el nombre del archivo
                print("¡Descarga completada!")  # Imprime un mensaje indicando que la descarga ha finalizado
            except Exception as e:
                print("Ocurrió un error:", str(e))  # Imprime un mensaje de error si ocurre un error durante la descarga
        else:
            error_message = "No se ha encontrado ninguna URL de video. Por favor, busca un video primero."
            messagebox.showerror("Error", error_message)


            

def main():
    root = tk.Tk()  # Crea una instancia de la clase Tk para la ventana principal
    root.iconbitmap("icoYou.ico")
    app = YouTubeDownloader(root)  # Crea una instancia de la clase YouTubeDownloader
    root.mainloop()  # Inicia el bucle principal de la interfaz gráfica
    
if __name__ == "__main__":
    main()  # Ejecuta la función principal cuando el script se ejecuta directamente
