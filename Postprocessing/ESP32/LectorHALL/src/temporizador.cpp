#include "temporizador.hpp"

void temporizador::runTimer(void)
{
    //unsigned long int tiempo = millis();
    upTimer();
    if(_counter>=_timeout)
    {
        _counter=0;
        _flag=1;
    }
 }

void temporizador::upTimer(void)
{
    unsigned long int tiempo = millis();
    _counter = _counter + (tiempo-_oldtime);
    _oldtime = tiempo;
}