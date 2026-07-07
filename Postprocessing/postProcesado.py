#Este es el archivo principal que procesa toda la información

import SeleccionFichero
import SegmentacionFases
import comfort
import webcam
import SecondaryTask
import os
import numpy as  np
import pandas as pd


# Probar con logger que contengan los dos circuitos de forma consecutiva, con registro basal
# Desarrollar un script que permita obtener los comandos para cada segmento del circuito 1 y lo
#   compare con el caso ideal
# Adaptar el análisis de los tiempos de atención para la tarea secundaria. El jerk solo se
#   determina para el circuito final.
# Procesamiento de los tests psicométricos NASA y SUS
# 





def post():
    logger = True     #Indicar si usamos el logger o mcap cuando ponemos a False
    fichero_salida = 'Resultados.csv'  #Nombre del fichero donde se van acumulando los resultados de los ficheros seleccionados
    sf = SeleccionFichero.SeleccionDirectorio()
    folder_name = sf.main()  # Lee los ficheros de ROS2BAG y LOGGER y los convierte a los csv correspondientes
    Sujeto,Exp,Modo,inicio = sf.leerDatos()  #Leemos Sujeto, Exp, y Modo y el instante donde comienza el experimento en el modo logger
    print('----------------------------')
    print(f'Sujeto:{Sujeto},Exp:{Exp},Modo:{Modo},Inicio:{inicio}')
    print('----------------------------')
    print(f"Nombre del directorio: {folder_name}")
    seg = SegmentacionFases.SegmentacionFases()  #Este fichero selecciona
    #seg.main(folder_name,[Sujeto,Exp,Modo],logger=True)  #La información de Sujeto, exp, modo solo hace falta en modo logger, que es el usado por defecto
    seg.main(folder_name,logger=logger ,pos=inicio)  #La información de Sujeto, exp, modo solo hace falta en modo logger, que es el usado por defecto
    csv_folder_name = seg.leerDirectorio()
    fases = seg.leerFases() #Devuelve las fases en una lista de listas
    print('----------------------------')
    print(f"Fases: {fases}")  # Matriz con los intervalos de tiempo de cada fase.
                              # [fase, inicio, fin, duracion]
    print('----------------------------')
    print(f"Nombre del directorio que contiene los csvs: {csv_folder_name}")
    con = comfort.comfort()
    con.main(csv_folder_name,fases,dibujar=True)
    jerk,distancia = con.leerDatos()
    print('----------------------------')
    print(f'Jerk:{jerk},Distancia:{distancia}')
    print('----------------------------')
    if Exp==0:
        web=webcam.webcam()
        traj = web.main(folder_path=csv_folder_name,fases=fases,display=False )
        print('--------------------------------')                
        print("Trajectory features")
        print(traj)
        print('--------------------------------')
    else:
        st = SecondaryTask.SecondaryTask()
        out_st = st.main(folder_path=csv_folder_name,display=True)
        print('--------------------------------')                
        print("Secondary Task")
        print(out_st)
        print('--------------------------------')  

    #información para guardar en el archivo Resultados.csv
    fases=np.array(fases)
    print(jerk)
    datos=[]
    for n in np.arange(len(fases)):
        #print(f"{fases[n,0]},{jerk[n]},{traj[n][1]}")
        print(f"{n},{jerk[n]}")
        if Exp==0:
            datos.append([Sujeto, Exp, Modo, logger, fases[n,0], fases[n,1], fases[n,2], fases[n,3], jerk[n], distancia[n], traj[n][1][0], traj[n][1][1], traj[n][1][2] ,0,0,0])
        else:    
            datos.append([Sujeto, Exp, Modo, logger, fases[n,0], fases[n,1], fases[n,2], fases[n,3], jerk[n], distancia[n], 0, 0, 0, out_st[0], out_st[1], out_st[2]  ])
            
    columnas = ['Sujeto', 'Exp', 'Modo', 'Logger','Fase','Tini','Tfinal','Duracion','Jerk','Distancia','Mv','Me','Mo','RT','Ec','Eo']

    df_datos = pd.DataFrame(datos,columns=columnas)
    print(df_datos.head())
    if os.path.exists(fichero_salida):
        print(f"El archivo '{fichero_salida}' ya existe. Añadiendo nuevas filas al final...")
        df_datos.to_csv(fichero_salida, mode='a', header=False, sep=';', encoding='utf-8-sig',index=False)
    else:
        print(f"El archivo '{fichero_salida}' no existe. Creándolo por primera vez con cabeceras...")
    
        # Si no existe, lo creamos de forma normal (por defecto escribe las cabeceras)
        df_datos.to_csv(fichero_salida, header=True,sep=';', encoding='utf-8-sig',index=False)
    print('Datos guardados')       


if __name__ == '__main__':
    post()

