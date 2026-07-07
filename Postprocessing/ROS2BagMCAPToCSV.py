import mcap
from mcap.reader import make_reader
from mcap_ros2.decoder import Decoder
import os
import pandas as pd
from pathlib import Path


class ROS2BagMCAPToCSV:
    def __init__(self):
        self.decoder = Decoder()


    @staticmethod
    def flatten_dict(d, parent_key='', sep='.'):
        items = []

        # 1. Intentar convertir a diccionario de todas las formas posibles
        if hasattr(d, '__getstate__'):
            data_map = d.__getstate__()
        elif hasattr(d, 'get_fields_and_field_types'): # Específico de algunas versiones de ROS2
            data_map = {field: getattr(d, field) for field in d.get_fields_and_field_types().keys()}
        elif hasattr(d, '__dict__'):
            data_map = vars(d)
        elif isinstance(d, dict):
            data_map = d
        else:
            # Si llegamos aquí y es un objeto, intentamos ver si tiene un .data (común en String.msg)
            if hasattr(d, 'data'):
                return {parent_key: str(d.data)}
            return {parent_key: str(d)}

        for k, v in data_map.items():
            if k.startswith('_'): continue

            new_key = f"{parent_key}{sep}{k}" if parent_key else k

            # 2. Análisis del valor 'v'
            # Si es un objeto complejo (pero no un string/número/bytes)
            if hasattr(v, '__dict__') or hasattr(v, '__getstate__') or isinstance(v, dict):
                # Caso especial: Si el objeto tiene un .data que es el valor real
                if hasattr(v, 'data') and not (hasattr(v.data, '__dict__') or isinstance(v.data, dict)):
                    val = v.data
                    if isinstance(val, bytes): val = val.decode('utf-8', errors='ignore')
                    items.append((new_key, val))
                else:
                    items.extend(ROS2BagMCAPToCSV.flatten_dict(v, new_key, sep=sep).items())

            # 3. Tratamiento de tipos básicos
            elif isinstance(v, bytes):
                items.append((new_key, v.decode('utf-8', errors='ignore')))
            elif isinstance(v, list) or isinstance(v, tuple):
                # Si la lista contiene bytes, decodificarlos
                clean_list = [x.decode('utf-8', errors='ignore') if isinstance(x, bytes) else x for x in v]
                items.append((new_key, str(clean_list)))
            elif v is None:
                items.append((new_key, ""))
            else:
                # Forzamos que sea un tipo básico de Python
                items.append((new_key, v))

        return dict(items)


    def process_single_file(self, mcap_path):
        output_dir = os.path.splitext(mcap_path)[0] + "_csv"
        #output_dir = "mcap2csv"
        os.makedirs(output_dir, exist_ok=True)
        
        data_by_topic = {}
        processed_count = 0
        
        print(f"📂 Abriendo: {os.path.basename(mcap_path)}")
        
        try:
            with open(mcap_path, "rb") as f:
                reader = make_reader(f)
                
                # Usamos un try-except DENTRO del bucle para salvar lo procesado hasta el error
                try:
                    for schema, channel, message in reader.iter_messages():
                        try:
                            topic_name = channel.topic
                            ros_msg = self.decoder.decode(schema, message)

                            msg_dict = {
                                slot: getattr(ros_msg, slot) 
                                for slot in dir(ros_msg) 
                                if not slot.startswith('_') and not callable(getattr(ros_msg, slot))
                            }

                            record = {
                                "log_time_s": message.log_time / 1e9,
                                "publish_time_s": message.publish_time / 1e9,
                                **self.flatten_dict(msg_dict)
                            }

                            if topic_name not in data_by_topic:
                                data_by_topic[topic_name] = []
                            data_by_topic[topic_name].append(record)
                            processed_count += 1
                            
                        except Exception as msg_err:
                            # Si falla un mensaje individual (decodificación), saltamos al siguiente
                            continue

                except Exception as stream_err:
                    # Este es el error "unpack_from" (corrupción de buffer)
                    print(f"⚠️ Corrupción detectada en el stream. Se recuperaron {processed_count} mensajes.")
                    print(f"Detalle del error: {stream_err}")

            # EXPORTACIÓN (Se ejecuta aunque el bucle de arriba haya fallado a mitad)
            if not data_by_topic:
                print(f"❌ No se pudieron recuperar datos de {os.path.basename(mcap_path)}")
                return

            for topic_name, records in data_by_topic.items():
                df = pd.DataFrame(records)
                clean_name = topic_name.strip("/").replace("/", "_")
                output_file = os.path.join(output_dir, f"{clean_name}.csv")
                
                df.to_csv(
                    output_file, 
                    index=False,
                    quoting=3,  #Sin comillas
                    decimal='.',
                    escapechar='\\',
                    header=None,
                    sep=';',
                    encoding='utf-8-sig'
                )
            
            print(f"✅ Datos recuperados guardados en: {output_dir}")

        except Exception as e:
            print(f"❌ Error crítico en el archivo {mcap_path}: {e}")

            
    def run_recursive(self, root_folder):
        """Busca y procesa todos los .mcap en la carpeta y subcarpetas."""
        mcap_files = []
        for root, dirs, files in os.walk(root_folder):
            for file in files:
                if file.endswith(".mcap"):
                    #print(file)
                    mcap_files.append(os.path.join(root, file).replace('\\','/'))
        
        if not mcap_files:
            print("No se encontraron archivos .mcap en el directorio seleccionado.")
            return

        print(f"🔍 Se encontraron {len(mcap_files)} archivos. Iniciando conversión...")
        for path in mcap_files:
            print(f"🚀 Procesando: {path}")
            self.process_single_file(path)
        print("\n✨ ¡Proceso finalizado!")

        
        
        