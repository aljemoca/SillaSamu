#include <Hall.hpp>

void Hall::setPin(unsigned char *pines)
{
     unsigned char i; 
     for(i=0;i<3;i++)
     {
        _port[i] = pines[i];
        pinMode(_port[i], GPIO_MODE_INPUT);  
     }

};


void Hall::setHwTimer(unsigned int value)
{
   /*Configuramos el timer hardware para que tenga un prescaler de 800, lo que 
   hace que la fuente de reloj sea de 10us para un reloj de 80Mhz y cuenta
   ascendente.
   Documentation: https://deepbluembedded.com/esp32-timers-timer-interrupt-tutorial-arduino-ide/?utm_content=cmp-true
   */
   _timer = timerBegin(value, 800, true); // Timer 0, divisor de reloj 800. Cada paso es de 10us
   timerAlarmWrite(_timer, 65536, true); // Salta interrupción cada 65.536 * 10us = 655ms = 0.65s
   timerAlarmEnable(_timer); // Habilitar la alarma

}

void Hall::run(void)
{

   unsigned long int tiempo;

	  uint8_t Medida_hall_motor[3];
	  uint8_t i;
//	  uint8_t secuencia_hall[8][2] ={ {0,0},{3,5},{6,3},{2,1},{5,6},{1,4},{4,2},{0,0}};
	  uint8_t secuencia_hall[8][2] ={ {0,0},{3,5},{6,3},{2,1},{5,6},{1,4},{4,2},{0,0}};
	  	/*La primera columna de la matriz bidimensional representa la secuencia
	  	 * para avance, la segunda para retroceso. Dependiendo de si la rueda
	  	 * es la derecha o la izquierda, el giro se invierte y da resultados distintos
	  	 * para avance y retroceso*/



   t.upTimer();
   p.upTimer();
   _counter = timerRead(_timer);


	if(_counter < _old_counter)
	{
      tiempo = _ccr1;      	
		if(tiempo>100)
		{
			if(t.getTime()<400)
			{
				_time = tiempo;
				_freq = 1111.1F/(float)_time; //Ajustar la constante
				_step++;
			}
			else
			{
				_time = 30000;
				_freq = 0.0;
			}
			_flag=1;

		};
		t.resetTimer();
	}
	_old_counter = _counter;
	if(_time>=30000)
		_flag=1;




	  for(i=0;i<3;i++)
		  Medida_hall_motor[i] = digitalRead(_port[i]);
	  _old_value = _value;
	  _value = Medida_hall_motor[0]+ 2*Medida_hall_motor[1] + 4*Medida_hall_motor[2];
	  if(_old_value != _value)
	  {
		  	  p.resetTimer();
			  if(secuencia_hall[_old_value][_position]==_value)
				  _turn = CLOCKWISE;
			  if(secuencia_hall[_old_value][1-_position]==_value)
				  _turn = COUNTERCLOCKWISE;
			  ventana.write(_turn);
	  }else
	  {

		  if(p.getTime()>500)
		  {
			  _turn= STOP;
			  ventana.write(_turn);
		  }
	  }
	  if(ventana.isFull())
		  _turnfiltered = ventana.median();


}