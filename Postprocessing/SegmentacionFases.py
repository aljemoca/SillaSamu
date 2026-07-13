import pandas as pd
import os
import numpy as np

#ADAPTAR EL SCRIPT PARA QUE SE LEAN LAS FASES DEL CIRCUITO2 QUE VAN DESDE START HASTA EL STOP: HECHO hay que probar

# Comentario: con logger, tenemos toda la información, pero con ros2bat, la fase 0 se pierde. 
#
#
# El programa lee Ejecucion.csv secuencialmente y ejecuta una máquina de estaods para definir las fases
# Máquina de estados implementada:
#Reset: Se puede recibir un comando de fase: 0,1,2....10, Start
#       Si comando==Fase, go to estado Inicial y anota la fase
#       Si comando==Start, go to estado final, anota fase 0 y toma el tiempo t1
#Inicial: Se pueden recibir comandos de fase, Start, Stop, Fin de Fase, Error de Fase
#       Si comando ==Start, go to estado final, anota fase y toma el tiempo t1
#       Si comando ==30, go to estado reset, 
#Final: Se pueden recibir comandos Start, Fin de fase o error de fase
#       Si comando ==Stop, go to estado reset
#       Si comando == Fin de fase, toma el tiempo t2, go to estado Inicial y actualiza listaFases
#       Si comando == Error de fase, toma el tiempo t1 de nuevo, la fase no cambia

#IMPORTANTE: Cuando se tenga que repetir la fase, hay que volver al punto de partida y cuando se inicie, entonces ERROR de FASE. NO ANTES
#IMPORTANTE: Se pierde la duración del primere segmento si se utilizan los ficheros ros2bag

class SegmentacionFases:
    def __init__(self):
        self.listaFases=[]
        self.num_fases=11
#        self.t_inicial=None
#        self.t_final = None

    def leerFases(self):
        return self.listaFases

    def leerDirectorio(self):
        return self.directorio    

    def deteccionFases(self):
        self.estado = 0
        self.fase=0
        t1 = 0
        t2 = 0        
        for n in np.arange(len(self.df)):
            ent = self.df.iloc[n,2]
            t = self.df.iloc[n,0]
            if t >= self.pos:   
 #           if (t>=self.t_inicial) & (t<=self.t_final):
            #print(f'Ent:{ent},Tiempo:{t},EStado:{self.estado}')
                if self.estado == 0:   #Estado de Reset
                    if ent==0:
                        self.estado =1
                        self.fase = ent
                    if ent==20:
                        self.estado=2
                        self.fase = 0
                        t1 = t
                    if ent==50:
                        self.estado=1
                        self.fase=0
                        t2=t
                        self.listaFases.append([self.fase, t1, t2, t2-t1])
#                    if ent==30:
#                        t2=t
#                        self.listaFases.append([self.fase, t1, t2, t2-t1])

                elif self.estado == 1:  #Estado inicio de fase
                    if ent==20:  #Estaba solo igual, pero quiero que cambie de fase por si no se le da al fin
                        self.estado=2
                        t1=t
                    elif ent==30:
                        self.estado=0
                        break
                    elif ent !=50 and ent!=40:
                        self.fase=ent
                        t1 = t
                        self.estado=2
                
                elif self.estado == 2:  #Estado final de fase
                    if ent==40:
                        t1=t
                    if ent==50:
                        t2=t
                        self.estado=1
                        self.listaFases.append([self.fase, t1, t2, t2-t1])
                    if ent==30:
                        self.estado=0
                        t2=t
                        self.listaFases.append([self.fase, t1, t2, t2-t1])
                        break

    def deteccionStartStop(self):
        #Hay que tener en cuenta que la detección del Start Stop es diferente si se hace con ros2bag o con logger
        #En ros2bag no hay comando de start porque la grabación se inicia después de recibirlo
        #
        self.fase=0
        self.estado = 0
        t1 = 0
        t2 = 0        
        for n in np.arange(len(self.df)):
            ent = self.df.iloc[n,2]
            t = self.df.iloc[n,0]
 #           if (t>=self.t_inicial) & (t<=self.t_final):
            print(f'*****Ent:{ent},Tiempo:{t},Estado:{self.estado}')
            if t>=self.pos:
                if self.estado == 0:   #Estado Espera Start
                    if ent==20:
                        self.estado=1
                        t1 = t
                    if ent==30:  #En ros2bag puede no recibirse la entrada 20 porque la grabación se inicia después
                        t2=t           
                        self.listaFases.append([self.fase, t1, t2, t2-t1])
                elif self.estado == 1:  #Estado final de fase
                    if ent==30:
                        self.estado=0
                        t2=t
                        self.listaFases.append([self.fase, t1, t2, t2-t1])
                        break
                    if ent==20:  #Esto no es posible, peeeeero
                        t1=t

        #print(self.listaFases)             

#    def delimitaUsuario(self,info):
#        nombre_su = self.directorio+'name_movil.csv'
#        nombre_tipo = self.directorio+'tipo_exp.csv'
#        nombre_modo = self.directorio+'modo_exp.csv'
#        dsu = pd.read_csv(nombre_su,sep=';',encoding='utf-8-sig', header=None)
#        dti = pd.read_csv(nombre_tipo,sep=';',encoding='utf-8-sig', header=None)
#        dmo = pd.read_csv(nombre_modo,sep=';',encoding='utf-8-sig', header=None)
#        su_res = dsu[dsu.iloc[:,2]==info[0]] 
#        if len(su_res)>0:
#            self.t_inicial = su_res.iloc[0,0]  



    def main(self,directorio,info=None,logger=True,pos =None):
        #Esta función recibe el nombre del directorio donde están los csv
        #info es una lista con Sujeto, tipo y modo. Solo necesaria en modo logger
        #logger permite baserse en logger o en ros2bag
        self.df = pd.DataFrame()
        self.pos = pos
        print(f'Tiempo inicial {self.pos}')
        if logger:
            self.directorio = directorio+'/logger/'
            nombre_ej = self.directorio+'Ejecucion.csv'
            self.df = pd.read_csv(
                nombre_ej,
                sep=';',  #Esto solo vale para logger
                encoding='utf-8-sig',
                header=None   #Esto solo vale para logger, para ros2bag hay que quitarlo
            )
#            self.t_inicial=self.df.iloc[0,0]
#            self.t_final=self.df.iloc[-1,0]
#            self.delimitaUsuario(info)

        else:
            pos = directorio.rfind('/')
            nombre = directorio[pos+1:]
            self.directorio = directorio+'/'+nombre+'_0_csv/'
            nombre_ej = self.directorio+'Ejecucion.csv'
            self.df = pd.read_csv(
                nombre_ej,
                sep=';',  #Esto solo vale para logger
                encoding='utf-8-sig',
                header=None   #Esto solo vale para logger, para ros2bag hay que quitarlo
            )
            print(self.df)
            self.pos = self.df.iloc[0][2]
#            self.t_inicial=self.df.iloc[0,0]
#            self.t_final=self.df.iloc[-1,0]
        #Buscamos las partes del CSV de Ejecución que estén asociados al usuario, tipo y modo especificados
        #print(self.df)
        if info is not None:
            circuito = info[1]
        else:
            pos=directorio.rfind('/')
            subcadena = directorio[pos+1:]
            pos=subcadena.find('_')
            circuito = int(subcadena[pos+1])
        
        if circuito==0:
            self.deteccionFases()
            #print('Por aquí')
        else:
            self.deteccionStartStop()
            #print('Por allá')
#if __name__=='__main__':
#    seg = SegmentacionFases()
#    directorio = 'C:/Users/alber/Documents/GitHub/SillaSamu/Postprocessing/samuchair_bag/USUARIO1_0_2_2026_06_15-09_15_59' #De ejemplo
#    seg.main(directorio)


