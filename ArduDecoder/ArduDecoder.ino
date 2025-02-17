/*
 * PPM generator originally written by David Hasko
 * on https://code.google.com/p/generate-ppm-signal/ 
 */

//////////////////////CONFIGURATION///////////////////////////////
#define CHANNEL_NUMBER 8  //set the number of chanels
#define CHANNEL_DEFAULT_VALUE 1500  //set the default servo value
#define FRAME_LENGTH 22500  //set the PPM frame length in microseconds (1ms = 1000µs)
#define PULSE_LENGTH 300  //set the pulse length
#define onState 1  //set polarity of the pulses: 1 is positive, 0 is negative
#define sigPin 10  //set PPM signal output pin on the arduino

/*this array holds the servo values for the ppm signal
 change theese values in your code (usually servo values move between 1000 and 2000)*/
int ppm[CHANNEL_NUMBER];
int j = 1000;
String input;
String Ost_input;
void setup(){  
  Serial.begin(115200);
  

  //initiallize default ppm values
  for(int i=0; i<CHANNEL_NUMBER; i++){
      ppm[i]= CHANNEL_DEFAULT_VALUE;
  }

  pinMode(sigPin, OUTPUT);
  digitalWrite(sigPin, !onState);  //set the PPM signal pin to the default state (off)
  
  cli();
  TCCR1A = 0; // set entire TCCR1 register to 0
  TCCR1B = 0;
  
  OCR1A = 100;  // compare match register, change this
  TCCR1B |= (1 << WGM12);  // turn on CTC mode
  TCCR1B |= (1 << CS11);  // 8 prescaler: 0,5 microseconds at 16mhz
  TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt
  sei();

}

void loop(){

  //j+=10;
  //for(int i=0; i<CHANNEL_NUMBER; i++){
  //    ppm[i]= j;
  //}
  //if (j>2000){
  //  j = 1000;
  //}
  
  if (Serial.available()>0){
    input = "";
    while(Serial.available()>0){
      input += (char)Serial.read();
    }
    Serial.println(input);

    int index = input.indexOf(',');
    int len = input.length();
    int last_index = 0;
    Ost_input = input.substring(index,len);
    Serial.println(input.substring(last_index,index).toFloat());
    ppm[0] = map(input.substring(last_index,index).toFloat(), -40, 40, 1000, 2000);
    input = Ost_input.substring(1,len - index);
    last_index = index;
    Serial.println(input);

    index = input.indexOf(',');
    len = input.length();
    last_index = 0;
    Ost_input = input.substring(index,len);
    Serial.println(last_index,index);
    ppm[1] = map(input.substring(last_index,index).toFloat(), -40, 40, 1000, 2000);
    input = Ost_input.substring(1,len - index);
    last_index = index;
    Serial.println(input);

    index = input.indexOf(',');
    len = input.length();
    last_index = 0;
    Ost_input = input.substring(index,len);
    Serial.println(last_index,index);
    ppm[2] = map(input.substring(last_index,index).toFloat(), 0, 40, 1000, 2000);
    input = Ost_input.substring(1,len - index);
    last_index = index;
    Serial.println(input);

    index = input.indexOf(',');
    len = input.length();
    last_index = 0;
    Ost_input = input.substring(index,len);
    Serial.println(last_index,index);
    ppm[3] = map(input.substring(last_index,index).toFloat(), -40, 40, 1000, 2000);
    input = Ost_input.substring(1,len - index);
    last_index = index;
    Serial.println(input);

    delay (500);

    
    /*
    float k;
    char *token = strtok(token, ",");
    k = atof(token);// AIL +-40
    Serial.println(k);
    ppm[0] = map(k, -40, 40, 1000, 2000);

    token = strtok(NULL, ",");
    k = atof(token);// Ele +-40
    Serial.println(k);
    ppm[1] = map(k, -40, 40, 1000, 2000);
    
    token = strtok(NULL, ",");
    k = atof(token);// Thr 0 - 30
    Serial.println(k);
    ppm[2] = map(k, 0, 30, 1000, 2000);

    token = strtok(NULL, ",");
    k = atof(token);// Rud хз
    Serial.println(k);
    ppm[3] = map(k, -40, 40, 1000, 2000);
    */
  }
  




  for(int i=0; i<CHANNEL_NUMBER; i++){
      //Serial.println(ppm[i]);
  }
  //while(token != NULL){
      
  //}
  
  /*
    Here modify ppm array and set any channel to value between 1000 and 2000. 
    Timer running in the background will take care of the rest and automatically 
    generate PPM signal on output pin using values in ppm array
  */
  
}

ISR(TIMER1_COMPA_vect){  //leave this alone
  static boolean state = true;
  
  TCNT1 = 0;
  
  if (state) {  //start pulse
    digitalWrite(sigPin, onState);
    OCR1A = PULSE_LENGTH * 2;
    state = false;
  } else{  //end pulse and calculate when to start the next pulse
    static byte cur_chan_numb;
    static unsigned int calc_rest;
  
    digitalWrite(sigPin, !onState);
    state = true;

    if(cur_chan_numb >= CHANNEL_NUMBER){
      cur_chan_numb = 0;
      calc_rest = calc_rest + PULSE_LENGTH;// 
      OCR1A = (FRAME_LENGTH - calc_rest) * 2;
      calc_rest = 0;
    }
    else{
      OCR1A = (ppm[cur_chan_numb] - PULSE_LENGTH) * 2;
      calc_rest = calc_rest + ppm[cur_chan_numb];
      cur_chan_numb++;
    }     
  }
}
