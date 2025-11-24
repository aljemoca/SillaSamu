
#include <Arduino.h>

/* Documentation
 * AnalogWrite( Uno, Nano, Mini) pins: 3, 5, 6, 9, 10, 11 at a 490 Hz (pins 5 and 6: 980 Hz)
 * Serial Uno, Nano, Mini  0(RX), 1(TX)

  OJO con el filtro RC que se ponga a la salida del PWM, porque la respuesta debe limitar el
  tiempo de muestreo de la señal del joystick manual. SamplingTime is in ms. Fc = 10Hz


  Para el manejo o control del Joystick, el Arduino recibe dos comandos
  
  - Cnx, donde n puede ser 0 para control interno o 1 para control externo
  
  - Jvalue1,value2x donde value1 y value2 son enteros sin signo de 8 bits
  
  Cuando se recibe un comando correcto, el sistema devuelve Okx
  En caso contrario Nokx

  El programa es simple. Por defecto el Arduino nano arranca en modo interno, o control por joystick manual
  En ese estado, adquiere las señales del joystick y genera un PWM a las salidas para el controlador. El software
  hace de puente entre el mando físico y el controlador del motor. Si se cambia a control externo, son los valores
  recibios por el arduino los que establecen las salidas para el controlador.

  Hay que tener en cuenta que el micro se pone en modo interno cuando han transcurrido 10s sin actividad 
  en el puerto serie del Arduino.

  Adicionalmente existen otros comandos:

  - Ix     
      El comando Ix sirve para determinar identificarse. El Arduino respondería Ax
  - Rx
      Se solicita el valor del Joystick. La respuesta tiene el mismo formato que el comando J. Ejemplo R100,200x 
  - Sx
      Se solicita el estado del Arduino. Éste tiene dos estados: modo manual (0) o modo remoto (1)
      La respuesta es similar al comando Cx. Ejemplo: S1x (Arduino está en modo remoto) S0x (Arduino en modo manual)


  Hay que tener en cuenta que el micro se pone en modo interno cuando han transcurrido 10s sin actividad 
  en el puerto serie del Arduino.


//Global variables
unsigned char State;
+a través del PWM. 

*/
#define AnalogOutX 5
#define AnalogOutY 6
#define InternalJoystick 0
#define ExternalJoystick 1
#define SamplingTime 50
#define WatchdogTimeout 10000

/*
  El watchdog time es el tiempo en ms que tarda el Arduino en ponerse en el estado inicial
*/

//Functions
int parser(char *, unsigned char *);
void communication(unsigned char *);
unsigned long conversion_time, conv_time_old;
unsigned char State,PowerOn;
int Output_Analog_Channels[2];
int Input_Analog_Channels[2];
unsigned long  wdt, wdt_old;  //wdt

void setup()
{
  /*
    Configuración de las variables globales
    State -> Establece modo manual o modo externo
    conversion_time -> Se configura por defecto a 50ms para el convertidor analogico digital
  */
  State = InternalJoystick;   //Estado por defecto del Arduino. En este estado, la silla se gobierna de fomra manual con el Joystick
  PowerOn =1;     //Este variable determina si el Joystick manual está encendido. Si no lo está, PowerOn se pone a 0, y se desactiva el control remoto
  conv_time_old=millis();   //Contador de tiempo para la conversión de tiempo.
  wdt_old=millis();    //Contador de tiempo del perro guardián,para hacer que el Joystick retorne al modo manual.
  conversion_time = SamplingTime;   
  Output_Analog_Channels[0] = AnalogOutX;   //Canal analógico de salida que controla el eje X
  Output_Analog_Channels[1] = AnalogOutY;   //Canal analógico de salida que controla el eje Y
  Input_Analog_Channels[0]= A0;   //Canales para la lectura del joystick manual
  Input_Analog_Channels[1]= A1;   

  
  Serial.begin(115200);
  
}


void loop()
{
  int Outputs[2], temp[2];  //These values should be in the range from 0 to 255 for the analogWrite function
                   //The channels X and Y are indexed as 0 and 1 respectively
 unsigned char temp_buf[2];    //Contiene los valores recibidos para los canales X e Y
  unsigned char i;             
  int adc[2];       //Canales X e Y del joystick manual
    
  communication(temp_buf);

  //ADConversion
  conversion_time = millis();
  
  if(conversion_time >= (SamplingTime+conv_time_old))
  {
    conv_time_old=conversion_time;
    for(i=0;i<2;i++)
    {
        adc[i] = analogRead(Input_Analog_Channels[i]);
    }
    if(adc[0] <10 && adc[1]<10)
       PowerOn=0;
    else
      PowerOn=1;
    
    if(State==InternalJoystick)
    {
      for(i=0;i<2;i++)
      {
        Outputs[i] = map(adc[i],0,1024,0,255);
        temp_buf[i] = (unsigned char)Outputs[i];
        analogWrite(Output_Analog_Channels[i],Outputs[i]);        
      }
    }else
    {
      for(i=0;i<2;i++)
      {
        temp[i] = (int)temp_buf[i];
        /*Serial.println(temp[0]);
        Serial.println(temp[1]);*/
        Outputs[i] = map(temp[i],0,255,0,255);
        analogWrite(Output_Analog_Channels[i],Outputs[i]);        
      }
      if(PowerOn==0)
        State=InternalJoystick;
    }  
  }

  wdt = millis();
  if(wdt >= (wdt_old+WatchdogTimeout))
  {
    wdt_old=wdt;
    State=InternalJoystick;  
  }


}


int parser(char *cadena, unsigned char *joy)
{
   unsigned char i,j;
   unsigned char poscoma=0,lon=0;
   unsigned char limites[2][2];

 
   while(cadena[lon]!=0 || lon> 12)
   {
     //Buscamos la posición de la coma.
      lon++;
      if(cadena[lon]==',')
        poscoma=lon;
   }
 
   
   if(poscoma==0 || i >12)
      return 0;

  
   limites[0][0]=1; 
   limites[0][1]=poscoma-1;  //El primer argumento {ejex} se encuentra entre la posición 1 y la anterior de la coma
   limites[1][0]=poscoma+1;
   limites[1][1]=lon-1;   //El segundo argumento {ejey} se encuentra después de la coma, y ocupa hasta el final, antes de la x


   for(j=0;j<2;j++)
   {
      joy[j]=0;    //Para cada argumento, recorremos cada dígito y lo convertimos en entero por codificación decimal posicional
     for(i=limites[j][1];i>=limites[j][0];i--)
        joy[j]+= (cadena[i]-'0')*pow(10,limites[j][1]-i);
   }
   return 1;
}


void communication(unsigned char *joy){
  static  char buffer_rx[12];
  static unsigned char i;
  static unsigned long int rx_time;
  //unsigned char temp[2];

  char byterx;
  static unsigned char input_packet;

  
  if((millis()-rx_time)> 200 || i>11)
  {
     /*Cada 200ms que no se haya recibido un carácter en el puerto serie, o si la longitud recibida es mayor de 11,
    se reinicia la búsqueda de un nuevo paquete de datos.*/
 
    i=0;
    rx_time=millis();
  }
  if(Serial.available())
  {
        wdt_old=wdt;   //Cada vez que se reciba algo, el sistema reseta el perro guardián que hace que 
                 //El estado de partida sea el interno.
        byterx=Serial.read();
     /*   Serial.print(i);
        Serial.print(',');
        Serial.print(rx_time);
        Serial.print(',');
        Serial.println(byterx);
        
     */ 
           /*Hasta que no se reciba un fin de paquete (x), el sistema está guardando 
        el carácter recibido en el buffer_rx. En este caso habilita un banderín que hace
        que se proceda a la lectura del paquete de entrada (input_packet=1)*/
        if(byterx=='x')
        {
          buffer_rx[i]=0;
          
          input_packet=1;
          i=0;
        }
        else
        {
          buffer_rx[i]=byterx;
          i++;
        }
        rx_time=millis();
  }
  if(input_packet)
  {
       /*
      En general este bloque analiza el primer comando de la cadena, que identifica la oepración a realizar. 
      Tan solo en el comando J, se invoca a la función parser para extraer el valor que se pondrá en el 
      PWM de salida para el control de los motores.
      */
      input_packet=0;
      char cadena[20];
      switch(buffer_rx[0])
      {
        case 'C':
          if(buffer_rx[1]<='1' && buffer_rx[1]>='0')
          {
            Serial.print("Okx");
            State=buffer_rx[1]-'0';
          }
          else
              Serial.print("Nokx");
          //Serial.println(State); //Para depuración
          break;  
        case 'J':
//          Serial.println(buffer_rx);  //Para depuración
          if(parser(buffer_rx,joy))
          {   
              //Serial.println(joy[0]); //Para depuración
              //Serial.println(joy[1]); //Para depuración
              Serial.print("Okx");
              //joy=temp;
          }
          else
              Serial.print("Nokx");
          break;
        case 'I':
          Serial.print("Ax");
          break;
        case 'R':
          Serial.print("R");
          Serial.print(joy[0]);
          Serial.print(",");
          Serial.print(joy[1]);
          Serial.print("x");
          break;
        case 'S':
          Serial.print("S");
          Serial.print(State);
          Serial.print("x");
          break;
        default:
          Serial.print("Nox");
      } 
  }
}  
