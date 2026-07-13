# SeleccionFichero
# Programa para seleccionar el directorio para analizar

import numpy as np
import os
from pathlib import Path
import sys
#import ipywidgets as widgets
#from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from ROS2BagMCAPToCSV import ROS2BagMCAPToCSV
import shutil

#Hay que retocar este programa porque en un mismo día pueden haber varios sujetos. Hay que seleccionar el segmento de datos
#que va desde el nombre del sujeto y hasta la parada ESTÁ HECHO PERO HAY QUE PROBARLO


class SeleccionDirectorio:

    def __init__(self):
        self.Sujeto = None
        self.Exp = None
        self.Modo =None
        self.Fecha = None
        self.Hora = None
        self.pos = None
        self.dir_bus = None

    def leerDatos(self):
        return self.Sujeto,self.Exp,self.Modo,self.pos


    def ConvertirLoggerNew(self,nombre):
        nombre=nombre+'/logger/'
        control = False
        #inicio=0

        carpeta = Path(nombre)
        if carpeta.exists() and carpeta.is_dir():
            shutil.rmtree(carpeta)
            print(f"Carpeta {carpeta.name} borrada con éxito.")

        # 2. La creamos de nuevo (vacía)
        carpeta.mkdir(parents=True, exist_ok=True)
        print(f"Carpeta {carpeta.name} creada de nuevo desde cero.")
        # 2. Buscar RECURSIVAMENTE (En la carpeta y todas sus subcarpetas)
        # El '**/*' le dice que entre a todo, y '*subcadena*' busca el texto
        carpeta_base = Path("C:/Users/alber/Documents/GitHub/SillaSamu/Postprocessing/logger")
        subcadena = self.Fecha.replace('_','')
        archivos_encontrados = list(carpeta_base.glob(f"**/*{subcadena}*"))
        df = pd.DataFrame()
        topics_name =set()

        # Mostrar los resultados
        for archivo in archivos_encontrados:
            print('NOMBRE DE ARCHIVO')
            print(archivo)  # Imprime la ruta completa limpia
            df = pd.read_csv(archivo,sep=';',encoding='utf-8-sig')
            res = df[(df['topic']=='directorio_grabacion') & (df['value']==self.dir_bus)   ]
            print(f"Resultados encontrados {str(res['timestamp_s']),res['value']}, subcadena {self.Cadena}")

            if (len(res)>0):
                for n in np.arange(len(res)):
                    if self.Cadena in res.iloc[n,2]:
                        control = True
                        self.pos = res.iloc[n,0]
                        pri= df[ (df['topic']=='Ejecucion') & (df['value']=='20')   ]
                        
                        #pri= df[ (df['value']=='20') ]
                        print(f"Resultado de pri: {pri}")

                        if len(pri):
                            #fin = df[ (df['topic']=='Ejecucion') & (df['value']=='30') ]
                            #if res.iloc[n,0] < pri.iloc[0,0]:
                            #self.pos = pri.iloc[-1,0] #No recuerdo bien por qué puse esto, pero no funciona siempre
                            for npri in np.arange(len(pri)):
                                if self.pos < pri.iloc[npri,0]:
                                    self.pos = pri.iloc[npri,0]
                                    break
                            #self.pos = pri.iloc[0,0] #Algunas veces hay que usar -1,0, como está en el renglón de arriba


   
#            if (len(res)>0) & (control==False) :
#                if self.Cadena in str(res['value']):
#                       control=True
            
            if (control):
                topics_name.update(set(df['topic']))

                for top in topics_name:
                    #print('-----------------')
                    #print(top)
                    data = df[ df['topic']==top]
                    #print(data)
                    archivo = nombre+str(top)+'.csv'
                    data.to_csv(
                        archivo, 
                        mode='a', 
                        index=False, 
                        header=False,
                        sep=';', 
                        encoding='utf-8-sig'
                    )
#            if (len(res)>0) and (control==True):
#                if self.Cadena not in str(res['value']):
#                    control=False
            res = df[(df['topic']=='Ejecucion') & (df['value']=='30') ]
            print(f"Res:{res}")
            if (len(res)>0) and (control==True):
                if self.pos is not None:
                    res = res[res['timestamp_s']>self.pos ]
                    if len(res):
                        control = False
 

    def ConvertirLogger(self,nombre):
        nombre=nombre+'/logger/'
        carpeta = Path(nombre)
        if carpeta.exists() and carpeta.is_dir():
            shutil.rmtree(carpeta)
            print(f"Carpeta {carpeta.name} borrada con éxito.")

        # 2. La creamos de nuevo (vacía)
        carpeta.mkdir(parents=True, exist_ok=True)
        print(f"Carpeta {carpeta.name} creada de nuevo desde cero.")
        # 2. Buscar RECURSIVAMENTE (En la carpeta y todas sus subcarpetas)
        # El '**/*' le dice que entre a todo, y '*subcadena*' busca el texto
        carpeta_base = Path("C:/Users/alber/Documents/GitHub/SillaSamu/Postprocessing/logger")
        subcadena = self.Fecha.replace('_','')
        archivos_encontrados = list(carpeta_base.glob(f"**/*{subcadena}*"))
        df = pd.DataFrame()
        topics_name =set()
        # Mostrar los resultados
        for archivo in archivos_encontrados:
            print('NOMBRE DE ARCHIVO')
            print(archivo)  # Imprime la ruta completa limpia
            df = pd.read_csv(archivo,sep=';',encoding='utf-8-sig')

            topics_name.update(set(df['topic']))

            for top in topics_name:
                #print('-----------------')
                #print(top)
                data = df[ df['topic']==top]
                #print(data)
                archivo = nombre+str(top)+'.csv'
                data.to_csv(
                    archivo, 
                    mode='a', 
                    index=False, 
                    header=False,
                    sep=';', 
                    encoding='utf-8-sig'
                )

    def DatosGenerales(self,name):
        posicion = name.rfind('/')
        subcadena = name[posicion+1:]
        self.dir_bus=subcadena
        print(f'nombre_directorio: {self.dir_bus}')
        posicion = subcadena.find('_')
        self.Sujeto = subcadena[:posicion]
        subcadena = subcadena[posicion+1:]
        posicion = subcadena.find('_')
        self.Exp = int(subcadena[:posicion])
        subcadena = subcadena[posicion+1:]
        posicion = subcadena.find('_')
        self.Modo = int(subcadena[:posicion])
        subcadena = subcadena[posicion+1:]
        posicion = subcadena.find('-')
        self.Fecha = (subcadena[:posicion])
        self.Hora = subcadena[posicion+1:]
        print(f'Sujeto:{self.Sujeto},Exp:{self.Exp},Modo:{self.Modo},Fecha:{self.Fecha}, Hora:{self.Hora}')
        self.Cadena = self.Sujeto+'_'+str(self.Exp)+'_'+ str(self.Modo)


    def main(self):
        self.root=tk.Tk()
        self.root.withdraw()
        self.root.attributes("-topmost", True)

        folder_path = filedialog.askdirectory(title="Selecciona la carpeta raíz para buscar MCAPs")
        print(f'DIRECTORIO : ->{folder_path}')
        self.DatosGenerales(folder_path)
        if folder_path:
            converter = ROS2BagMCAPToCSV()
            #m=Merge()
            #output_path = os.path.join(folder_path, "merged_session.mcap")
            #m.merge_mcap_files(folder_path, output_path)
            converter.run_recursive(folder_path)
            self.ConvertirLoggerNew(folder_path)
        else:
            print("Operación cancelada.")
        return folder_path
        

#if __name__ == '__main__':
#    sf = SeleccionFichero()
#    sf.main()

#    print("--- COMPROBACIÓN ---")
#    print("Python ejecutable desde aquí:", sys.executable)
#    print("Carpeta donde Python está buscando:", os.getcwd())
#    print("--------------------")