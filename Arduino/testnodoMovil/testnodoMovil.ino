

/*

 Nombre!   Si la longiud de lo recibido es mayor de dos, se considera el nombre del sujeto
#       G!  Indica que comienza el experimento
#       S!  Indica que el experimento ha acabado
#       Fx!  Marcamos una fase   x=0,1,2,......E!
#       Tx! Seleccionamos el tipo x=0,1
#       Mx!  Seleccionamos modo de operación x=0,1,2
#       E! Señalizar fase errónea

*/


// Definición de la velocidad del puerto serie (Baud rate)
const long BAUD_RATE = 115200;

// Variables para gestionar el tiempo (sin usar delay)
unsigned long tiempoAnterior = 0;
const long intervalo = 5000; // Intervalo de 5 segundos (5000 ms)
const long intervaloF = 2000; // Intervalo de 2 segundos para las 'F!'

// Variable para seguir el estado (paso) actual de la secuencia
int pasoActual = 0;

// Contador para la secuencia de 'F!'
int contadorF = 0;
const int maxF = 12; // Total de 'F!' a enviar

void setup() {
  // Inicializa la comunicación serial a 115200 bps
  Serial.begin(BAUD_RATE);
  Serial.println("Programa iniciado. Esperando 5 segundos para empezar la secuencia...");
  // Inicializa el tiempo para que el primer paso ocurra tras 5 segundos
  tiempoAnterior = millis(); 
}

void loop() {
  // El programa avanza basado en el valor de 'pasoActual' y el tiempo transcurrido
  static unsigned int  rep;
  unsigned long tiempoActual = millis();

  // ---------------------------------------------
  // PASOS CON INTERVALO DE 5 SEGUNDOS (5000ms)
  // ---------------------------------------------
  if (tiempoActual - tiempoAnterior >= intervalo) {
    tiempoAnterior = tiempoActual; // Reinicia el tiempo

    switch (pasoActual) {
      case 0:
        // 1. Mensaje inicial tras los primeros 5s
        Serial.println("Alejandro!");
        pasoActual = 1;
        rep=0;
        break;
      case 1:
        // 2. Mensaje 'Tx!' tras 5s
          Serial.print("T");
          Serial.print(rep);
          Serial.println("!");
          rep++;
          if(rep==2)
          {
            pasoActual = 2;
            rep=0;
          }
        break;
      case 2:
        // 3. Mensaje 'Mx!' tras 5s
          Serial.print("M");
          Serial.print(rep);
          Serial.println("!");
          rep++;
          if(rep==3)
          {
            pasoActual = 3;
            rep=0;
          }
        break;
      case 3:
        // 4. Mensaje 'G!' tras 5s
        Serial.println("G!");
        // Reiniciamos el tiempo para que el primer 'F!' empiece tras 2s
        // y pasamos al siguiente estado (bucle 'F!')
        tiempoAnterior = tiempoActual - (intervalo - intervaloF); 
        pasoActual = 4;
        break;
      case 5:
        // 6. Mensaje 'S!' tras 5s (después de la última 'F!')
        Serial.println("S!");
        pasoActual = 6; // Secuencia finalizada
        break;
      case 6:
        Serial.println("E!");
        // Mantiene el estado final, no hace nada más
        pasoActual = 7;
        break;
      case 7:
        Serial.println("!!!!!!");
        pasoActual = 8;
        break;
      case 8:
        Serial.println("aldkjfapoiqjefavñpaleroìu20394kfñc<.vadru0234º3nr, !");
        pasoActual = 0;
        break; 
    }
  }

  // ---------------------------------------------
  // PASO 5: Bucle de 'F!' (Intervalo de 2000ms)
  // ---------------------------------------------
  if (pasoActual == 4) {
    if (tiempoActual - tiempoAnterior >= intervaloF) {
      tiempoAnterior = tiempoActual; // Reinicia el tiempo de 2s
      
      if (contadorF < maxF) {
        // 5. Envía F!
        Serial.print("F");
        if(contadorF<10)
          Serial.print(contadorF);
        else
          Serial.print((char)('A'+contadorF-10));
        Serial.println("!");
        contadorF++;
      } else {
        // Cuando se envían 10 F!, pasa al siguiente estado
        // Mantiene el 'tiempoAnterior' para que la 'S!' se envíe tras 5s
        pasoActual = 5; 
        contadorF=0;
      }
    }
  }
}
