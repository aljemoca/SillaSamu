#include <Arduino.h>
#include <temporizador.hpp>
#include <Window.hpp>

#define CLOCKWISE 1
//#define COUNTERCLOCKWISE -1
#define COUNTERCLOCKWISE 2
#define STOP 0


class Hall
{
    private:

        unsigned long int _time;
        float _freq;
        unsigned char _flag;
        unsigned long int _counter,_old_counter;
        unsigned long int _ccr1;

        uint8_t _value;
	    uint8_t _old_value;
	    int8_t _turn;  //Para el sentido del giro Avance 1, Atras -1 y parado 0
	    int8_t _turnfiltered;
	    uint8_t _position; //Izquierda 0 y derecha 1
        uint16_t _step;  //Pasos contados desde la última lectura

        
    public:
        unsigned int _port[3];
        temporizador t;
        hw_timer_t *_timer = NULL;

        Hall(){_flag=0; reset(); p.setTimeout(500); ventana.create(5,1), _value=0; _old_value=0;_step=0;};
        void setPin(unsigned char *pines);
        void setHwTimer(unsigned int value); // Timer 0, divisor de reloj 800};
        unsigned long getTime(void){_flag=0;return _time;};
        void updateCCR1(void){_ccr1 = timerRead(_timer);};
        void writeCCR1(unsigned long int value){_ccr1 = value;};
        float getFreq(){_flag=0;return _freq;};
        unsigned char timeReady(void){return _flag;};
        uint16_t getHallSteps(){return _step;};
	    void	clearHallSteps(){_step=0;};
        void reset(void){_counter=30000;_old_counter=30000;_time=30000;t.resetTimer();_step=0;};
        void run(void);



        temporizador p;
	    window<int8_t> ventana;
    	void setHallPosition(uint8_t posicion){_position=posicion;};//Izquierda o Derecha
    	uint8_t readValue(){return _value;};
    	int8_t wheelMovement(){return _turnfiltered;};

    };