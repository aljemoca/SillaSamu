#include <Arduino.h>

class temporizador
{
    private:
	// ** Variable that decreases down to zero.
	unsigned long int _timeout;
	unsigned long int _counter;
    unsigned char _flag;
    unsigned long int _oldtime;

    public:

    temporizador(){_timeout=0;resetTimer();};
    void setTimeout(unsigned long int value){_timeout=value;};
    unsigned long int getTimeout(void){return _timeout;};
    unsigned long int getTime(void){return _counter;};
    void upTimer(void);
    void runTimer(void);
    unsigned char expired(void){return _flag;};
    void resetFlag(void){_flag=1;};
    void resetTimer(void){_counter=0;_flag=0;_oldtime=millis();};


};