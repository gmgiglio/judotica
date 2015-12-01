
#define tpo 2000
#define motorDPos 13
#define motorDNeg 12
#define motorIPos 8
#define motorINeg 7
#define enD 11
#define enI 10
int x,y;

void setup(){
  Serial.begin(9600);
  x = 128;
  y = 128;
}

void loop(){
  if (Serial.available()>0) {         
     x = int(Serial.read());
     y = int(Serial.read());
  }
  
  int _x = x - 128;
  int _y = y - 128;
  
  int motDer = 2*_x + 2*_y;
  int motIzq = 2*_x - 2*_y;
  if ( motDer > 0){
    digitalWrite(motorDNeg, LOW);
    digitalWrite(motorDPos, HIGH);
  }else{
    digitalWrite(motorDNeg, HIGH);
    digitalWrite(motorDPos, LOW);
    motDer = -motDer;
  }
  
  if ( motIzq > 0){
    digitalWrite(motorIPos, HIGH);
    digitalWrite(motorINeg, LOW);
  }else{
    digitalWrite(motorIPos, LOW);
    digitalWrite(motorINeg, HIGH);
    motIzq = -motIzq;
  }
  
  analogWrite(enD, motDer);
  //motDer = 0.92 * motDer;
  analogWrite(enI, motIzq);
  Serial.println(motIzq);
  Serial.println(motDer);
  
  
}



