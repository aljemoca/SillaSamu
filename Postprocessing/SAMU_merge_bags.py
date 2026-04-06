import os
import argparse
from mcap.reader import make_reader
from mcap.writer import Writer
from mcap_ros2_support.reader import read_ros2_messages
import tkinter as tk
from tkinter import filedialog


def merge_mcap_files(input_folder, output_file):
    # 1. Obtener y ordenar todos los ficheros .mcap de la carpeta
    bag_files = sorted([
        os.path.join(input_folder, f) 
        for f in os.listdir(input_folder) 
        if f.endswith(".mcap")
    ])

    if not bag_files:
        print(f"No se encontraron archivos .mcap en {input_folder}")
        return

    print(f"Fusionando {len(bag_files)} archivos...")

    with open(output_file, "wb") as f_out:
        writer = Writer(f_out)
        writer.start("ros2msg", profile="ros2") # Perfil para ROS2

        # Diccionario para evitar duplicar la declaración de canales (tópicos)
        channels = {}

        for bag_path in bag_files:
            print(f"Procesando: {os.path.basename(bag_path)}")
            
            with open(bag_path, "rb") as f_in:
                reader = make_reader(f_in)
                
                # Leer cada mensaje del archivo actual
                for schema, channel, message in reader.iter_messages():
                    
                    # Si el canal no ha sido registrado en el nuevo archivo, lo registramos
                    if channel.topic not in channels:
                        # Registramos esquema y canal
                        schema_id = writer.register_schema(
                            name=schema.name,
                            encoding=schema.encoding,
                            data=schema.data
                        )
                        channels[channel.topic] = writer.register_channel(
                            schema_id=schema_id,
                            topic=channel.topic,
                            message_encoding=channel.message_encoding,
                            metadata=channel.metadata
                        )
                    
                    # Escribir el mensaje en el archivo consolidado
                    writer.add_message(
                        channel_id=channels[channel.topic],
                        log_time=message.log_time,
                        data=message.data,
                        publish_time=message.publish_time,
                        sequence=message.sequence
                    )
        
        writer.finish()
    print(f"\nÉxito. Archivo fusionado guardado en: {output_file}")

#if __name__ == "__main__":
#    parser = argparse.ArgumentParser(description="Fusionar segmentos MCAP de ROS2")
#    parser.add_argument("folder", help="Carpeta que contiene los segmentos .mcap")
#    parser.add_argument("-o", "--output", default="merged_session.mcap", help="Nombre del archivo de salida")
    
#    args = parser.parse_args()
#    merge_mcap_files(args.folder, args.output)  
  
def main():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    folder_path = filedialog.askdirectory(title="Selecciona la carpeta raíz para buscar MCAPs")

    if folder_path:
        merge_mcap_files(folder_path, "merged.mcap")
    else:
        print("Operación cancelada.")

if __name__ == '__main__':
    main()
