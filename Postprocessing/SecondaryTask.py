
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class SecondaryTask:

    def __init__(self):
        self.tr_at=None
        self.tr_nat=None
        self.ErroresComision=None
        self.tr=None
        self.ErroresOmision=None

    def lecturaDatos(self):
        if len(self.tr):
            return [np.mean(self.tr), self.ErroresComision, self.ErroresOmision]
        else:
            return [0, self.ErroresComision, self.ErroresOmision]

    def  encuentra_impulsos(self,df_a,df_t,busca=0):
        #Poner busca 1 para buscar atendidos y 0 para los no atendidos
        pos = np.where(df_a.iloc[:,2]==busca)
        #print(pos)
        t =  np.array(df_a.iloc[:,0])
        t = t[pos]
        #print( t )
        #print( np.array(df_a['data']))

        tiempos = []
        for tt in t:
            indice = np.abs(np.array(df_t.iloc[:,0]) - tt).argmin()
        #   print(indice)
            tiempos = np.append(tiempos, np.array(df_t.iloc[:,2])[indice])
        
        self.data=np.array(tiempos)/1000
        return (self.data)

    def main(self, folder_path, display=False):

        if folder_path:
            file_a = folder_path +'/Attended.csv'
            file_t = folder_path + '/diff_time.csv'
#            if not 'logger' in folder_path:
#               df_a = pd.read_csv(file_a,encoding='utf-8-sig',quotechar='"',header=False, skipinitialspace=True)
#               df_t = pd.read_csv(file_t,encoding='utf-8-sig',quotechar='"',header=False, skipinitialspace=True)
#            else:
            df_a = pd.read_csv(file_a,encoding='utf-8-sig',header=None, sep=';',quotechar='"')
            df_t = pd.read_csv(file_t,encoding='utf-8-sig',header=None, sep=';',quotechar='"')
            print(df_a.head())
            print(df_t.head())
            #if 'logger' not in folder_path:
            #    random_time = np.diff(df_a['log_time_s'])-0.5  #No quitar 0.5, que sirve para compensar el retardo de publicación
            #else:    
            random_time = np.diff(df_a.iloc[:,0])-0.5  #No quitar 0.5, que sirve para compensar el retardo de publicación
            if display:
                plt.stem(df_a.iloc[:,0],df_a.iloc[:,2])
                plt.title('Attended')
                plt.xlabel('Time')
                plt.show()
                plt.plot(df_t.iloc[:,0],df_t.iloc[:,2],'-o')
                plt.ylabel('Diff_time (s)')
                plt.xlabel('Time')
                plt.show()

            
            self.tr_at=self.encuentra_impulsos(df_a,df_t,1)  #Todos los pulsos clasificados como 1 son los atendidos
            self.tr_nat= self.encuentra_impulsos(df_a,df_t,0)  #Los pulsos clasificados como 0 son los no atendidos

            self.ErroresComision = np.sum(self.tr_nat<3)
            self.ErroresOmision = np.sum(self.tr_at>3)
            self.tr = self.tr_nat[np.where(self.tr_at<3)]

            print(f"Errores de comisión: {self.ErroresComision}" )
            print(f"Errores de omision: {self.ErroresOmision}"   )
            print(f"Tiempos de reacción:  {self.tr}" )
            #print(np.sum(self.tr_nat<3))
            return self.lecturaDatos()
            
        else:
            print("No se seleccionó ningún archivo")
    
