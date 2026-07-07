
#include <Arduino.h>
//#include <temporizador.hpp>

class Potenciometro
{
	uint16_t _adc_raw; //Dato bruto recibido por el convertidor ADC
	uint16_t _TsAdc; //Periodo de lectura del dato del potenciómetro (1000)*.
	uint16_t _adc_raw_q,_adc_raw_q_old; //Valor cuantizado del potenciómetro
	uint8_t _Nvel; //Número de velocidades diferentes seleccionables (mejor potencia de dos)
	uint8_t adcPin;
	temporizador  tadc;
	uint8_t _flag;
public:
	uint16_t delta;

	Potenciometro()
	{
		_TsAdc=500;	//Muestreo del potenciómetro en ms
		tadc.resetTimer(); //temporizador para la lectura de datos del ADC
		_Nvel = 8;  //Número de niveles distintos de velocidad  (incluyendo 0)
		_flag = 0;
        adcPin = 36; //REVISAR SI ESTO ES ASÍ
	};
	void run(void){
        tadc.upTimer();
		if(tadc.getTime()>=_TsAdc)
		{
			tadc.resetTimer();
			_adc_raw = analogRead(adcPin);
			delta = 4096/(_Nvel);
			_adc_raw_q=delta*( (_adc_raw+delta/2)/delta);
			if(_adc_raw_q!=_adc_raw_q_old)
			{
				_flag=1;
				_adc_raw_q_old=_adc_raw_q;
			}
		}
	};

	void setTsAdc(uint32_t value){_TsAdc=value;};
	void setADCpin(uint8_t p){adcPin = p; pinMode(p,INPUT);};
	void setNiveles(uint8_t value){_Nvel = value;};
	uint8_t isNewConversionFlagSet(void){return _flag;};
	uint16_t readValue(void){ _flag = 0; return _adc_raw_q;};
	uint8_t readQValue(void){_flag=0; return _adc_raw_q/delta;};
};

