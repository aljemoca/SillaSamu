#!/usr/bin/env python3
import os
import sys
import pandas as pd



import tkinter as tk
from tkinter import filedialog
from mcap.reader import make_reader
from mcap_ros2_support.decoder import Decoder

class ros2bagMCAP_to_csv(self):


    def flatten_dict(d, parent_key='', sep='.'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                items.append((new_key, str(v)))
            else:
                items.append((new_key, v))
        return dict(items)

    def process_mcap_to_csv(mcap_path, output_dir=None):
        if not os.path.exists(mcap_path):
            print(f"❌ No existe: {mcap_path}")
            return

        if output_dir is None:
            output_dir = os.path.splitext(mcap_path)[0] + "_csv"
        os.makedirs(output_dir, exist_ok=True)

        print(f"📂 Procesando MCAP: {mcap_path}")

        # Diccionario para acumular datos por tópico
        data_by_topic = {}

        with open(mcap_path, "rb") as f:
            reader = make_reader(f)
            decoder = Decoder()

            # iter_messages decodifica automáticamente usando el esquema del archivo
            for schema, channel, message in reader.iter_messages():
                topic_name = channel.topic

                # Decodificar el mensaje a un objeto de Python
                ros_msg = decoder.decode(schema, message)

                # Convertir el objeto ROS a un diccionario simple
                # Accedemos a los campos del mensaje dinámicamente
                msg_dict = {}
                for slot in dir(ros_msg):
                    if not slot.startswith('_') and not callable(getattr(ros_msg, slot)):
                        msg_dict[slot] = getattr(ros_msg, slot)

                # Preparar la fila para el CSV
                record = {
                    "log_time_s": message.log_time / 1e9,
                    "publish_time_s": message.publish_time / 1e9,
                    **flatten_dict(msg_dict)
                }

                if topic_name not in data_by_topic:
                    data_by_topic[topic_name] = []
                data_by_topic[topic_name].append(record)

        # Guardar cada tópico en un CSV independiente
        for topic_name, records in data_by_topic.items():
            df = pd.DataFrame(records)
            clean_name = topic_name.strip("/").replace("/", "_")
            csv_path = os.path.join(output_dir, f"{clean_name}.csv")
            df.to_csv(csv_path, index=False)
            print(f"  ✅ Guardado {len(records)} mensajes en: {csv_path}")

            
    def main(args=None):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Selecciona el mcap",
            filetypes=[("MCAP files", "*.mcap")]
        )

        if file_path:
            process_mcap_to_csv(file_path)
        else:
            print("No se seleccionó ningún archivo")

        
    if __name__ == '__main__':
        main()     
# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Uso: python ros2bag_to_csv_recursive.py carpeta_raiz")
#         sys.exit(1)

#     root_dir = sys.argv[1]
#     db3_files = find_all_db3(root_dir)

#     print(f"Se encontraron {len(db3_files)} archivos .db3 en {root_dir}")

#     for db3_path in db3_files:
#         try:
#             ros2bag_to_csv(db3_path)
#         except Exception as e:
#             print(f"❌ Error procesando {db3_path}: {e}")