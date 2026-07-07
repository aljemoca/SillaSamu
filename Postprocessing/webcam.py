
import numpy as np
import os
import cv2
import math
import pandas as pd




class webcam:

    def __init__(self):
        self.ratio =  0.103   #conversion ratio in cm/px
        self.mv = None
        self.me = None
        self.mo = None


    def trajectory_parameters(self, ent, val):
        pos = np.where(val==1)
        self.mv = np.sqrt(np.var(ent[pos],ddof=1))
        self.me = np.sum(np.abs(ent[pos]))/len(ent[pos])
        self.mo = np.sum(ent[pos])/len(ent[pos])
        
        return self.mv,self.me,self.mo

    def leerParametros(self):
        return self.mv,self.me,self.mo


    def cargar_imagenes_de_directorio(self,ruta_directorio,rango):
        """
        Carga todas las imágenes (archivos .jpg, .png, etc.) de un directorio dado.

        Args:
            ruta_directorio (str): La ruta completa del directorio donde están las imágenes.

        Returns:
            list: Una lista de tuplas, donde cada tupla contiene (nombre_archivo, imagen_cargada).
                Retorna una lista vacía si el directorio no existe o no contiene imágenes.
        """
        imagenes = []
        if not os.path.isdir(ruta_directorio):
            print(f"Error: El directorio '{ruta_directorio}' no existe.")
            return imagenes

        print(f"Buscando imágenes en: {ruta_directorio}")
        for nombre_archivo in os.listdir(ruta_directorio):
            pos_punto = nombre_archivo.rfind('.')
            pos_raya = nombre_archivo.rfind('_')
            n_frame = int(nombre_archivo[pos_raya+1:pos_punto])
            #print(f"Número de frame:{n_frame}, Rango: {rango}")
            if (n_frame>=rango[0]) & (n_frame<=rango[1]):
                print(f"Número de frame:{n_frame}")
            # Construye la ruta completa al archivo
                ruta_completa_archivo = os.path.join(ruta_directorio, nombre_archivo)

            # Verifica si es un archivo (no un subdirectorio)
                if os.path.isfile(ruta_completa_archivo):
                    # Intenta leer la imagen. cv2.imread retorna None si no es una imagen válida.
                    imagen = cv2.imread(ruta_completa_archivo)
                    #imagen = cv2.cvtColor(imgagen, cv2.COLOR_BGR2RGB)
                    if imagen is not None:
                        imagenes.append((nombre_archivo, imagen))
                        #print(f"Cargada: {nombre_archivo}")
                    else:
                        print(f"Saltando archivo (no es una imagen o está corrupto): {nombre_archivo}")
        
        if not imagenes:
            print("No se encontraron imágenes en el directorio.")
        
        return imagenes


    #def segmentar_curva_por_color(imagen, lower_hsv_bound=(40/2,0,0), upper_hsv_bound=(70/2,255,255)):
    def segmentar_curva_por_color(self,imagen, lower_hsv_bound=(85, 100, 100), 
        upper_hsv_bound=(105, 255, 255)):
        """
        Segmenta una imagen por un rango de color HSV específico para encontrar la curva.

        Args:
            imagen (np.array): La imagen de entrada (en formato BGR de OpenCV).
            lower_hsv_bound (tuple): Tupla (H, S, V) que define el límite inferior del color.
            upper_hsv_bound (tuple): Tupla (H, S, V) que define el límite superior del color.

        Returns:
            np.array: Una imagen binaria (máscara) donde los píxeles de la curva son blancos (255)
                    y el resto son negros (0).
                    
        """
    
        """
        Segmenta una imagen por un rango de color HSV específico para encontrar la curva.

        Args:
            imagen (np.array): La imagen de entrada (en formato BGR de OpenCV).
            lower_hsv_bound (tuple): Tupla (H, S, V) que define el límite inferior del color.
            upper_hsv_bound (tuple): Tupla (H, S, V) que define el límite superior del color.

        Returns:
            np.array: Una imagen binaria (máscara) donde los píxeles de la curva son blancos (255)
                    y el resto son negros (0).
                    
        """
        
        
        # 1. Convertir la imagen de BGR a HSV
        hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

        # 2. Crear la máscara usando el rango de color HSV
        # Los píxeles dentro del rango serán blancos (255), el resto negros (0)
        mascara = cv2.inRange(hsv, lower_hsv_bound, upper_hsv_bound)

        return mascara


    def esqueletizar_imagen(self,imagen_binaria):
        """
        Realiza la esqueletización de una imagen binaria (Zhang-Suen o similar).
        La imagen de entrada debe ser binaria (0 o 255).

        Args:
            imagen_binaria (np.array): La imagen binaria de entrada (máscara).

        Returns:
            np.array: La imagen esqueletizada (línea central del objeto).
        """
        # Asegurarse de que la imagen sea binaria (0 o 255) y de tipo CV_8UC1
        # Y que los objetos sean blancos (255) sobre fondo negro (0)
        imagen_binaria = imagen_binaria.copy() # Trabajar con una copia para no modificar la original
        if imagen_binaria.max() == 0: # Si la imagen está toda a cero (no hay objeto), retornar tal cual
            return imagen_binaria
        
        imagen_binaria[imagen_binaria == 255] = 1 # Convertir 255 a 1 para el algoritmo

        skeleton = np.zeros(imagen_binaria.shape, dtype=np.uint8)
        
        # Elemento estructurante para las operaciones de erosión y dilatación
        kernel = np.ones((3,3), np.uint8)
                      
        while True:
            eroded = cv2.erode(imagen_binaria, kernel)
            dilated = cv2.dilate(eroded, kernel)
            
            # Diferencia entre la imagen erosionada y dilatada para obtener los "puntos límite"
            temp = cv2.subtract(imagen_binaria, dilated)
            
            # Intersección entre la imagen y los puntos límite para obtener los píxeles a eliminar
            # Esto es un paso crucial del algoritmo de esqueletización (Zhang-Suen)
            # Aquí simplificado, pero la idea es ir eliminando píxeles del borde
            # sin desconectar el esqueleto.
            
            # Para esqueletización más robusta, a veces se usa una secuencia de pasos más complejos.
            # Aquí estamos usando una aproximación más sencilla que es útil.
            # Una implementación común de Zhang-Suen:
            # P = np.zeros_like(eroded)
            # ... (lógica del algoritmo de Zhang-Suen, que es un poco larga) ...
            # If this is too complex, we can use a simpler approach for straight lines/simple curves
            
            # Para propósitos prácticos de extracción de línea central de una curva:
            # El algoritmo de Zhang-Suen es complejo para implementar "al vuelo" si no lo tienes.
            # Una alternativa más simple para líneas y curvas gruesas es el "thinning" o adelgazamiento.
            # Pero cv2.ximgproc.thinning() está en un módulo "contrib" y es más avanzado.
            
            # Vamos a usar una aproximación común para esqueletización que se ve en ejemplos de OpenCV
            # Usando cv2.erode y cv2.dilate de forma iterativa
            
            # Esta es una aproximación al algoritmo de Zhang-Suen
            # La idea es mantener el esqueleto y eliminar el resto
            
            # Si la imagen no tiene más píxeles que eliminar, el proceso se detiene.
            # Esto es una simplificación de un algoritmo de esqueletización.
            # Para una esqueletización robusta, especialmente en formas complejas,
            # cv2.ximgproc.thinning(src, thinningType) del módulo contrib de OpenCV sería ideal
            # pero requiere una instalación específica de opencv-contrib-python.

            # Dada la complejidad de Zhang-Suen manual, y que el usuario busca coordenadas de una curva,
            # voy a ofrecer una alternativa que se usa a veces o simplificar la lógica.

            # Mejor, vamos a usar una implementación de Zhang-Suen directamente, que es la más común:
            # Asegurarse que la imagen sea de tipo CV_8UC1 y que los valores sean 0 y 255
            
            # Convertir a 0 y 1 para el algoritmo, y de vuelta a 0 y 255 al final
            # La esqueletización iterativa que busca el esqueleto central.
            
            # Para el algoritmo de esqueletización, la imagen debe ser binaria con 0s y 1s.
            img_copy = imagen_binaria.copy()
            img_copy[img_copy == 255] = 1 # El algoritmo espera 0s y 1s

            skeleton = np.zeros(img_copy.shape, dtype=np.uint8)
            
            done = False
            while not done:
                eroded = cv2.erode(img_copy, kernel)
                temp = cv2.dilate(eroded, kernel)
                temp = cv2.subtract(img_copy, temp)
                
                # Condición de parada: Si no se eliminó ningún píxel en esta iteración
                done = np.sum(temp) == 0

                skeleton = cv2.bitwise_or(skeleton, temp) # Acumular los píxeles eliminados
                img_copy = eroded.copy() # Actualizar la imagen para la siguiente iteración

            return skeleton * 255 # Convertir de nuevo a 0 y 255


    def contiene_linea(self,image,umbral=9):
        #This function tries to discern if the image contains a line or not
        #To accomplish this goal, the algorithm counts for white pixels in the image. If the
        #percentage is greater than a  given threshold, the image is considered to be valid.
        
        res = True
        if len(image.shape) > 2:
            print("Advertencia: La imagen no parece estar en escala de grises (tiene más de 2 dimensiones).")
            print("Se intentará convertir a escala de grises si es BGR o RGB.")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
        # Obtener el total de píxeles en la imagen
        total_pixels = image.shape[0] * image.shape[1]

        if total_pixels == 0:
            return 0.0 # Evitar división por cero

        # Contar los píxeles blancos (valor 255)
        # np.sum(imagen_grayscale == 255) cuenta cuántos elementos son True en la condición
        num_pixels_blancos = np.sum(image == 255)

        # Calcular el porcentaje
        porcentaje_blancos = (num_pixels_blancos / total_pixels) * 100
        if porcentaje_blancos > umbral or porcentaje_blancos<1:
            res=False

        return res, porcentaje_blancos


    

    def encontrar_pixel_mas_cercano_al_centro(self,mascara_binaria):
        """
        Encuentra las coordenadas del píxel blanco de una máscara binaria
        que está más cerca del centro de la imagen.

        Args:
            mascara_binaria (np.array): La máscara binaria (blanco=255, negro=0).

        Returns:
            tuple or None: Las coordenadas (x, y) del píxel más cercano, o None si no hay píxeles blancos.
        """
        alto, ancho = mascara_binaria.shape
        centro_x, centro_y = ancho // 2, alto // 2

        # Obtener las coordenadas (filas, columnas) de todos los píxeles blancos
        # np.where devuelve dos arrays: uno para las filas y otro para las columnas
        filas_blancas, cols_blancas = np.where(mascara_binaria == 255)

        if len(filas_blancas) == 0:
            return None # No hay píxeles blancos en la máscara

        # Crear un array de puntos (x, y) para facilitar los cálculos
        puntos_blancos = np.column_stack((cols_blancas, filas_blancas)) # (x, y)

        # Calcular las distancias de todos los puntos al centro
        # Usamos np.linalg.norm para calcular la distancia euclidiana de forma eficiente
        distancias = np.linalg.norm(puntos_blancos - np.array([centro_x, centro_y]), axis=1)

        # Encontrar el índice del punto con la distancia mínima
        indice_mas_cercano = np.argmin(distancias)

        # Obtener las coordenadas del píxel más cercano
        pixel_mas_cercano_x, pixel_mas_cercano_y = puntos_blancos[indice_mas_cercano]

        return (pixel_mas_cercano_x, pixel_mas_cercano_y)
    

    def main(self,folder_path=None,fases=None,display=False):
        out=[]
        # ¡IMPORTANTE!: Reemplaza esta ruta con la ruta real de tu directorio de imágenes
        if folder_path:
            #directorio_de_mis_imagenes = '.\\fotos\\' # Ejemplo en Linux/macOS
            print(folder_path)
            pos = folder_path.rfind('/')
            subcadenafinal = folder_path[0:pos]
            pos = subcadenafinal.rfind('/')
            subcadenafinal = subcadenafinal[0:pos]
            pos =  subcadenafinal.rfind('/')
            subcadenafinal = subcadenafinal[pos+1:]
            subcadenainicial= folder_path[:pos]
            pos = subcadenainicial.rfind('/')
            
            directorio_de_mis_imagenes = subcadenainicial[0:pos]+'/fotos/'+ subcadenafinal
            print(f"Directorio de imágenes: {directorio_de_mis_imagenes}")
        # directorio_de_mis_imagenes = 'C:\\Users\\TuUsuario\\MisImagenes' # Ejemplo en Windows
            file_frame = folder_path +'frame.csv'

            #print(file_l)
            df_frame = pd.read_csv(file_frame,sep=';',encoding='utf-8-sig',header=None)

            #if 'logger' in folder_path:
            #    df_frame = pd.read_csv(file_frame,sep=';',encoding='utf-8-sig',header=None)
            #else:
            #    df_frame = pd.read_csv(file_frame,encoding='utf-8-sig',header=None,sep=';')
                
            print(df_frame.head())
            #print(df_l.head())
            print(fases)

            for f in np.arange(len(fases)):
                ent = fases[f][1:3]
                print(f"Ent: {ent}")
                print(f"Fase: {fases[f][0]}")
                pos_r=df_frame[df_frame.iloc[:, 0].between(ent[0], ent[1])]    
                print(pos_r)
                print('------')
                #lista_de_imagenes_cargadas = self.cargar_imagenes_de_directorio(directorio_de_mis_imagenes,[pos_r['data'].iloc[0], pos_r['data'].iloc[-1]])
                lista_de_imagenes_cargadas = self.cargar_imagenes_de_directorio(directorio_de_mis_imagenes,[pos_r.iloc[0,2], pos_r.iloc[-1,2]])
                #self.jerk_value,self.rt=self.calcula_jerk(pos_l.iloc[:,2],pos_r.iloc[:,2],pos_l.iloc[:,0],pos_r.iloc[:,0],dibujar=False)
                #self.jerk_list.append(np.mean(self.jerk_value))
                #self.rt_list.append(self.rt)


            #lista_de_imagenes_cargadas = self.cargar_imagenes_de_directorio(directorio_de_mis_imagenes)
        
                y_i = np.zeros(len(lista_de_imagenes_cargadas))   #Distance to the center of the image
                v_i = np.zeros(len(lista_de_imagenes_cargadas))   #This matrix contains if the element y_i is correct or not
                angulo_i = np.zeros(len(lista_de_imagenes_cargadas))
        
                print(f"Resolución de las imágenes {lista_de_imagenes_cargadas[0][1].shape}")
                for n in range(len(lista_de_imagenes_cargadas)):
                    amostrar=n
                    #print(f"\nSe han cargado {len(lista_de_imagenes_cargadas)} imágenes.")
                    # Opcional: Mostrar la primera imagen para verificar
                    print(f"Mostrando la primera imagen: {lista_de_imagenes_cargadas[amostrar][0]}")
                    #cv2.imshow('imagen',cv2.resize(lista_de_imagenes_cargadas[amostrar][1],(500,500)))
                    if display:
                        cv2.imshow(lista_de_imagenes_cargadas[amostrar][0],lista_de_imagenes_cargadas[amostrar][1])
                    imagen_converted = self.segmentar_curva_por_color(lista_de_imagenes_cargadas[amostrar][1])
                    #cv2.imshow('imagen2',cv2.resize(imagen_converted,(500,500)))
                    if display:
                        cv2.imshow('imagen2',imagen_converted)
                        
                #imagen_converted = cv2.dilate(imagen_converted, np.ones((10,10),np.uint8), iterations=5)
                    imagen_converted = cv2.erode(imagen_converted, np.ones((3,3),np.uint8), iterations=2)
                #imagen_converted=cv2.resize(imagen_converted,(500,500))
                
                    contornos, _ = cv2.findContours(imagen_converted.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    if len(contornos) > 0:
                        mayor_contorno = max(contornos, key=cv2.contourArea) #Pensar cambiar esto
                        mascara = np.zeros_like(imagen_converted)
                        cv2.drawContours(mascara, [mayor_contorno], -1, 255, thickness=-1)
                                #mascara = np.zeros_like(imagen_converted)
                        #cv2.drawContours(mascara, [mayor_contorno], -1, 255, thickness=-1)
                        ys, xs = np.where(mascara == 255)
                        pixeles_objeto = np.stack((xs, ys), axis=1)

                        #imagen_color = cv2.cvtColor(imagen_converted, cv2.COLOR_GRAY2BGR)
                        ##cv2.drawContours(imagen_color, [mayor_contorno], -1, (0, 255, 0), 2)
                        #cv2.imshow('Mayor objeto', mascara)


                        alto, ancho = imagen_converted.shape
                        centro_imagen = np.array([ancho // 2, int( 3*alto/4) ])

                        distancias = np.linalg.norm(pixeles_objeto - centro_imagen, axis=1) 
                        indice_min = np.argmin(distancias)
                        punto_mas_cercano = pixeles_objeto[indice_min]
                        
                        #imagen_converted = cv2.erode(imagen_converted, np.ones((5,5),np.uint8), iterations=2)
                        #porcentage = contiene_linea(imagen_converted)
                        #print(f"{porcentage}%")
                        #x,y = encontrar_pixel_mas_cercano_al_centro(imagen_converted)
                        x,y = punto_mas_cercano[0],punto_mas_cercano[1]
            
                        M = cv2.moments(mayor_contorno)
                        try:
                            cx = int(M['m10'] / M['m00'])
                            cy = int(M['m01'] / M['m00'])

                            # 2. Calcular el ángulo (como vimos antes)
                            angulo_rad = 0.5 * math.atan2(2 * M['mu11'], M['mu20'] - M['mu02'])
                            angulo_i[n]=angulo_rad*180/np.pi

                            pendiente= np.tan(angulo_rad)
                            A = -pendiente
                            B=1
                            C = pendiente*cx -cy
                            d = A*centro_imagen[0] + B*centro_imagen[1] +C           
                            #s = np.sign(d)*np.sign(pendiente)

                            yi = d*np.sign(pendiente)/np.sqrt(A**2+B**2)*self.ratio   #Distancia en cm
                            #yi = np.linalg.norm(punto_mas_cercano - centro_imagen)
                            y_i[n] =yi
                            v_i[n], porcentage = self.contiene_linea(mascara)

                            # 3. Calcular el punto final de la flecha (longitud de 100 píxeles)
                            largo_flecha = 100
                            # Usamos cos y sin para proyectar el ángulo desde el centro
                            # Nota: multiplicamos por -1 en 'dy' porque el eje Y en imágenes está invertido
                            endpoint_x = int(cx + largo_flecha * math.cos(angulo_rad))
                            endpoint_y = int(cy + largo_flecha * math.sin(angulo_rad))
                        except:
                            y_i[n]=-1
                            v_i[n]=0
                            yi=-1
                    else:
                        # 2. Si no hay contornos, crear una máscara negra o manejar el error
                        print("Advertencia: No se detectó la línea cian en esta imagen.")
                        mascara = np.zeros_like(imagen_converted)
                        y_i[n]=-100
                        v_i[n]=0
                        yi=-1
                    

                    color = cv2.cvtColor(mascara,cv2.COLOR_GRAY2BGR)
                    #print(yi)
                    #imagen_converted = esqueletizar_imagen(imagen_converted)
                    cv2.circle(color,(centro_imagen[0],centro_imagen[1]),5,(0,255,0),1)
                    if y_i[n]!=-1:
                        cv2.circle(color, (cx,cy),5, (255,0,0),2)
                        # cv2.arrowedLine(imagen, punto_inicio, punto_fin, color(BGR), grosor, tipLength)
                        cv2.arrowedLine(color, (cx, cy), (endpoint_x, endpoint_y), (0, 0, 255), 3, tipLength=0.3)
                    if display:
                        cv2.imshow("Distancia: "+str(y_i[n])+" cm", color)
                        cv2.waitKey(0) # Espera a que se presione una tecla
                        cv2.destroyAllWindows()
                    
                print( y_i,v_i,angulo_i)
                print(self.trajectory_parameters(y_i,v_i))
                out.append([f,self.trajectory_parameters(y_i,v_i)])
        return out
    
# --- EJEMPLO DE USO ---
#if __name__ == "__main__":
#    web = webcam()
#    web.main()
#
#else:
#    print("\nNo se pudieron cargar imágenes.")
    