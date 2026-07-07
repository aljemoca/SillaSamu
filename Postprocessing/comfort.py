import numpy as np
from scipy.signal import savgol_filter
import pandas as pd
import matplotlib.pyplot as plt



# Analizar desde Start hasta Stop
# Analizar la trayectoria para que se dibuje mejor
# para el jerk hay que eliinar la parte inicial en el que la silla está parada AUNQUE MEJOR SERÍA USARLO SOLO PARA EL CIRCUITO FINAL
# NO TIENE SENTIDO EN EL CIRCUITO INICIAL POR TENER MUCHOS ARRANQUES Y PARADAS
#Hay que guardar la trayectoria




class comfort:

    def __init__(self):
        self.jerk_value=0
        self.rt=0
        self.jerk_list=[]
        self.rt_list=[]

    def leerDatos(self):
        return self.jerk_list, self.rt_list
       
    def calcular_aceleracion_y_jerk(self, velocidad, dt, window_length=5, polyorder=3):
        """
        Calcula la aceleración y su derivada (jerk) a partir de una serie temporal de 
        distancias recorridas entre muestras consecutivas, usando el filtro de Savitzky-Golay.

        Parámetros:
        -----------
        distancias : array-like
            Lista o array con las distancias recorridas entre cada muestra.
        dt : float
            Intervalo de muestreo en segundos.
        window_length : int, opcional
            Tamaño de la ventana para Savitzky-Golay (debe ser impar y > polyorder).
        polyorder : int, opcional
            Orden del polinomio usado en Savitzky-Golay.

        Retorna:
        --------
        aceleracion : np.ndarray
            Array con los valores de aceleración estimados (m/s^2).
        jerk : np.ndarray
            Array con los valores de la derivada de la aceleración (m/s^3).
        """
    #    distancias = np.array(distancias)

        # Aceleración (1ª derivada de velocidad)
        #aceleracion = savgol_filter(velocidad, window_length, polyorder, deriv=1, delta=dt)

        # Jerk (derivada de la aceleración, es decir 2ª derivada de la velocidad)
        jerk = savgol_filter(velocidad, window_length, polyorder, deriv=2, delta=dt)

        #return aceleracion, jerk
        return jerk


    def representa_posicion(self,left,right,dibujar=False):
        '''ESTO ES FALSO, HAY QUE SABER LA CONVERSIÓN
        Supongamos el plano (x,y). La coordenada y representa el avance.
        Los datos del hall representan, a falta de escala, el avance
        de la parte derecha e izquierda de la silla. La coordenada x
        se toma como la diferencia de ambas, mientras que la y el promedio
        '''
        Npulsos = 550  #Número de pulsos asociados a una vuelta completa
        R = 15.5   #Radio de la rueda en cm
        k = 2*np.pi*R  / Npulsos   #Constante de conversión de pulsos a cm 
        D = 55   #Distancia entre ruedas
        rt = 0   #Longitud recorrida en cm
        
        left_cm = left*k
        right_cm = right*k
        l = (left_cm+right_cm)/2
        rt = np.sum(np.abs(l))   #Es importante que sea en valor absoluto
        angulo = np.cumsum(np.arctan((-right_cm+left_cm)/D))  #Ajustar la constante
        dx=l*np.sin(angulo)
        dy=l*np.cos(angulo)
        #x,y = dx,dy
        x,y = np.cumsum(dx),np.cumsum(dy)
        if dibujar:
            plt.plot(x,y)
            plt.title('Trajectory')
            plt.xlabel('x (cm)')
            plt.ylabel('y (cm)')
            plt.grid(visible=True)
            plt.show()
            
            plt.plot(left,label='left')
            plt.plot(right,label='right')
            plt.ylabel('Hall pulses')
            plt.xlabel('Samples')
            plt.grid(visible=True)
            plt.legend()
            plt.show()
            
        return x,y,rt


    def calcula_jerk(self,datal,datar,dtl,dtr,dibujar=False):
        a=np.array(datal)
        b=np.array(datar)
        #a=np.ones(100)*100
        #b=np.ones(100)*200
        x,y,rt=self.representa_posicion(a,b,dibujar)
        at=np.array(dtl)
        bt=np.array(dtr)
        dt=(np.diff(at)+np.diff(bt))/2
        #print(dt)
        #vl = (a[1:]+b[1:])/2*dt
        #vg = (a[1:]-b[1:])/dt
        vx = np.diff(a)/dt
        vy = np.diff(b)/dt
        t = np.mean(dt)
        jerkx=self.calcular_aceleracion_y_jerk(vx,t)
        jerky=self.calcular_aceleracion_y_jerk(vy,t)
        #jerkl = calcular_aceleracion_y_jerk(vl,t)
        #jerkg = calcular_aceleracion_y_jerk(vg,t)
        #jerk  = calcular_aceleracion_y_jerk(v,t)
        return (np.sqrt(jerkx**2+jerky**2)),rt
        #return jerkl,jerkg
        #print((a[1:]+b[1:])/2*dt)
        #return jerk


    def main(self,folder_path, fases, dibujar=False):    
        if folder_path:
            file_r = folder_path +'right_wheel_steps.csv'
            file_l = folder_path + 'left_wheel_steps.csv'
            #print(file_l)
#            if 'logger' in folder_path:
            df_r = pd.read_csv(file_r,sep=';',encoding='utf-8-sig',header=None)
            df_l = pd.read_csv(file_l,sep=';',encoding='utf-8-sig',header=None)
#            else
# #              df_r = pd.read_csv(file_r,encoding='utf-8-sig',filer_r)
  #              df_l = pd.read_csv(file_l,encoding='utf-8-sig')
                
            #print(df_r.head())
            #print(df_l.head())
            #print(fases)
            for f in np.arange(len(fases)):
                ent = fases[f][1:3]
                pos_r=df_r[df_r.iloc[:, 0].between(ent[0], ent[1])]
                pos_l=df_l[df_l.iloc[:, 0].between(ent[0], ent[1])]
                #print(f"Pos_r: {pos_r}")
                #print(f"Pos_l: {pos_l}")
                
                try:
                    self.jerk_value,self.rt=self.calcula_jerk(pos_l.iloc[:,2],pos_r.iloc[:,2],pos_l.iloc[:,0],pos_r.iloc[:,0])
                    self.jerk_list.append(np.mean(self.jerk_value))
                    self.rt_list.append(self.rt)
                except:
                    pass

            if len(fases)>1:
                pos_r=df_r[df_r.iloc[:,0].between(fases[0][1],fases[-1][1])]
                pos_l=df_l[df_l.iloc[:,0].between(fases[0][1],fases[-1][1])]
                self.jerk_value,self.rt=self.calcula_jerk(pos_l.iloc[:,2],pos_r.iloc[:,2],pos_l.iloc[:,0],pos_r.iloc[:,0],dibujar=dibujar)
            if dibujar:
                plt.plot(np.abs(self.jerk_value))
                plt.title('')
                plt.ylabel('Jerk')
                plt.xlabel('Sample')
                plt.show()
            
            print('***********************')
            print(f'Longitud recorrida: {self.rt} cm')
        else:
            print("No se seleccionó ningún archivo")
    

#if __name__=='__main__':
#    con = comfort()
#    directorio = 'C:/Users/alber/Documents/GitHub/SillaSamu/Postprocessing/samuchair_bag/USUARIO1_0_2_2026_06_15-09_15_59/logger/'
#    fases=[[0, 1781507796.2417665, 1781507809.2409952, 12.999228715896606], 
#           [1, 1781507826.2412388, 1781507844.7425234, 18.5012845993042], 
#           [2, 1781507853.7417424, 1781507862.741225, 8.99948263168335], 
#           [3, 1781507866.2417548, 1781507884.2412417, 17.999486923217773], 
#           [4, 1781507888.2413, 1781507906.7412827, 18.499982595443726]
#        ]
#    con.main(directorio,fases)