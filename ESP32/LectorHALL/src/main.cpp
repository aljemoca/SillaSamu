#include <Arduino.h>
#include <Hall.hpp>
#include <Potenciometro.hpp>

/*
  DESCRIPCIÓN DEL PROTOCOLO DE COMUNICACIONES DEL STM32 CON LA RASPBERRY DE LA SILLA SAMU

  Recepción: 0X34
  Respuesta: Paquete de 8 bytes con el siguiente formato   Cabecera, NivelPot, Giro rueda izquierda,
    MSB pasos rueda izquierda, LSB pasos rueda izquierda, Giro rueda derecha, MSB pasos rueda derecha,
    LSB pasos rueda derecha. 

  Recepción: Cualquier dato diferente a 0x34
  Respuesta: 0x1

  Tras la respuesta correcta, el STM32 inicializa la cuenta de pasos de cada rueda.
  El Giro de la rueda puede ser -1, 0, 1, indicando giro hacia atrás, parada, o giro hacia adelante.
  ESTO HABRÁ QUE VERIFICAR QUE VA BIEN
*/

// Mirar los puertos para cada uno de los sensores Hall
#define HallA_0 33
#define HallB_0 32
#define HallC_0 4    
#define Timer_0  0


#define HallA_1 13
#define HallB_1 14
#define HallC_1 27    
#define Timer_1 1

#define Pot_pin 36

Hall hall_motor[2];
Potenciometro pot;


// https://deepbluembedded.com/stm32-timers-tutorial-hardware-timers-explained/?utm_content=cmp-true

/* Below are the interrupts assigned to change at Hall inputs. Interrupt0 is called
as any change on inputs associated to Hall sensors of motor driver 0. The same applies
for the motor driver 1.  */
void Interrupt0()
{
  /*En la STM32 se tiene configurado un filtro digital, pero para poder implementarlo aquí, habría que 
  leer las entradas. No parece evidente  */
    hall_motor[0].updateCCR1(); 
    timerAlarmWrite(hall_motor[0]._timer, 65536,true); 
    timerAlarmEnable(hall_motor[0]._timer);
    timerWrite(hall_motor[0]._timer,0);  //In case the timerAlarmWrite does not reset the counter register
}
void Interrupt1()
{
    hall_motor[1].updateCCR1(); 
    timerAlarmWrite(hall_motor[1]._timer, 65536,true); 
    timerAlarmEnable(hall_motor[1]._timer);
    timerWrite(hall_motor[1]._timer,0);  //In case the timerAlarmWrite does not reset the counter register
}
void IRAM_ATTR timerInterrupcion0() {
  hall_motor[0].writeCCR1(65536); 
}

void IRAM_ATTR timerInterrupcion1() {
  hall_motor[1].writeCCR1(65536); 

}

void setup() {
  // put your setup code here, to run once:
  unsigned char hall_0[3]={HallA_0,HallB_0,HallC_0};
  unsigned char i;
  hall_motor[0].setPin(hall_0);  //Set the pins associated to left motor driver
  for(i=0;i<3;i++)
    attachInterrupt(hall_0[i],Interrupt0,CHANGE);   //Assign the interrupt to pin change
  hall_motor[0].setHwTimer(Timer_0);   //Timer attached to left motor driver
  timerAttachInterrupt(hall_motor[0]._timer, &timerInterrupcion0,true ); // Adjuntar la función de manejo de interrupción
            //Posiblemente hay que cambiar true por false. True admite disparo de la interrupción por flanco, mientras
            //que false por nivel
  timerStart(hall_motor[0]._timer);

  unsigned char hall_1[3]={HallA_1,HallB_1,HallC_1};
  hall_motor[1].setPin(hall_1);
  for(i=0;i<3;i++)
    attachInterrupt(hall_1[i],Interrupt1,CHANGE);
  hall_motor[1].setHwTimer(Timer_1);  //Timer attached to right motor driver
  timerAttachInterrupt(hall_motor[1]._timer, &timerInterrupcion1,true ); // Adjuntar la función de manejo de interrupción
  timerStart(hall_motor[1]._timer);

  Serial.begin(115200);   //Set communication to Raspberry trough the Serial Port.
  //pinMode(HallA,GPIO_MODE_INPUT);
  //pinMode(HallB,GPIO_MODE_INPUT);
  //pinMode(HallC,GPIO_MODE_INPUT);

  //attachInterrupt(HallA, HallInterrupt,CHANGE);
  //attachInterrupt(HallB, HallInterrupt,CHANGE);
  //attachInterrupt(HallC, HallInterrupt,CHANGE);

 // timer = timerBegin(0, 800, true); // Timer 0, divisor de reloj 800
 // timerAlarmWrite(timer, 65536, true); // Interrupción cada 1 segundo
 // timerAlarmEnable(timer); // Habilitar la alarma
 // pinMode(34, INPUT);  // Configura el pin como entrada (opcional para analógico)
  pot.setADCpin(Pot_pin);
  

}

void loop() {

/*
  Esta función permite establecer el diálogo con la RASPBERRY para mandar la información relativa 
  al estado del potenciométro y de los pasos de los sensores Hall desde la comunicación anterior.A0
  En el bucle principal, se procede a ejecutar las clases de los hall y el potenciométro para la lectura de
  la velocidad a configurar a la Silla del SAMU.

  Si se recibe el comando correcto, el STM32 responde mandando un paquete como el indicado en la cabecera
  de este fichero. Ese paquete contiene la información del nivel de velocidad seleccionado por el potenciómetro,
  el sentido de giro de cada rueda y los pasos desde la comunicación anterior. Se envían un total 8 bytes, incluyendo
  la cabecera. El STM32 borra la cuenta de pasos tras la transmisión. 

*/

  uint8_t i;
  uint8_t byte_rx;
  uint16_t data;
  uint8_t buffer_tx[8];
  for(i=0;i<2;i++)
    hall_motor[i].run();    //Execute hall motor objects 
  pot.run();
  /*Falta añadir el protocolo de comunicaciones con la RASPBERRY PI. Se sigue el modelo 
  que se usó en AgroSmart por compatibilidad */  

  //Serial.println(hall_motor[1].getHallSteps());   //To test communications
 // digitalWrite(10,0);  //Delete this line
  // put your main code here, to run repeatedly:
 // Serial.println(pot.readValue());
  if(Serial.available())
  {
      byte_rx = Serial.read();
      if(byte_rx==0x34)
      {
          buffer_tx[0]=0xaa;
          buffer_tx[1]=pot.readQValue();
          for(i=0;i<2;i++)
          {
            buffer_tx[2+3*i]=(hall_motor[i].wheelMovement());
            data=hall_motor[i].getHallSteps();
            hall_motor[i].clearHallSteps();
            buffer_tx[3+3*i] = (data&0xff00)>>8;
            buffer_tx[4+3*i] = (data&0x00ff);
          }
          for(i=0;i<8;i++)
            Serial.write(buffer_tx[i]);
      }
      else
              Serial.write(0x01);
    }
 /* if(pot.isNewConversionFlagSet())
      Serial.println(pot.readQValue());  // Lee el valor analógico (0-4095 por defecto)
*/
    
}

