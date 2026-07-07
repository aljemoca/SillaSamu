
template <class T>
class window{
	T *_matrix,*copia;
	//T	_matrix[15];
	uint8_t _D;
	uint8_t _tam,_full;
	uint8_t _nelem;
	int8_t _pw;
	uint8_t counter;
public:
	/*window()
	{
		_tam=5;
		create(5);
	}*/
	void create(uint8_t lon,uint8_t decimation=1)
	{
		_matrix = new T[lon];
		copia = new T[lon];
	/*	if(lon >15)
			lon=15;
		*/if(decimation>lon)
			_D=lon;
		else
			_D=decimation;
		_tam=lon;
		clear();
	}

//	uint8_t isFull(void){ return  (_nelem==_tam);};
	uint8_t isFull(void){return _full;};
	void clear(void){
		uint8_t t;
		for(t=0;t<_tam;t++)
			_matrix[t]=0;
		_pw=0;
		_full=0;
		counter=0;
	};
	void write(T value)
	{
		_matrix[_pw]=value;
		_pw++;
		if(_pw==_tam)
			_pw=0;
		counter++;
		if(counter>=_D)
		{
			counter=0;
			_full=1;
		}
	};

	T	slope(void)
	{
		int8_t pr_ultimo;

		pr_ultimo = _pw-1;
		if(pr_ultimo <0 )
			pr_ultimo=_tam-pr_ultimo;
		_full=0;
		//return (_matrix[pr_ultimo]- _matrix[_pw])/_tam;
		return (_matrix[pr_ultimo]- _matrix[_pw]);
/*		uint8_t t;
		int16_t sumxi=0;
		int16_t sumxi2=0;
		float sumyixi=0;
		float sumyi = 0;
		T m;
		for(t=0;t<_tam;t++)
		{
			sumxi+=t;
			sumxi2+=t^2;
			sumyixi+= float(_matrix[t]*t);
			sumyi+=float(_matrix[t]);
		}
		m= static_cast<T>(  (sumyi)/();*/
	};

	T	mean(void)
	{
		uint8_t t;
		T res=0;
		for(t=0;t<_tam;t++)
			res+=_matrix[t];
		_full=0;
		return res/_tam;
	};

	T	median(void){
		uint8_t cambio,t;
		T temp;

	//	T *copia = new T[_tam];
	//	T copia[15];
		for(t=0;t<_tam;t++)
			copia[t]=_matrix[t];
		do
		{
			cambio=0;
			for(t=0;t<_tam-1;t++)
				if(copia[t]<copia[t+1])
			    {
					temp = copia[t];
			        copia[t] = copia[t+1];
			        copia[t+1] = temp;
			        cambio=1;
			    }
		}while(cambio==1);
		_full=0;
		temp = copia[_tam/2];
		//delete [] copia;
		return temp;
	}
};
