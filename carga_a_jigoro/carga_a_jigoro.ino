
#define tpo 2000
#define motorDPos 13
#define motorDNeg 12
#define motorIPos 8
#define motorINeg 7
#define enD 11
#define enI 10
int instruc;

void setup(){
  Serial.begin(9600);
}


void loop(){
  instruc=0; 
  analogWrite(enD, 90);
  analogWrite(enI, 105); 
  if (Serial.available()>0) {         
    instruc = Serial.read();
  }
  
  if ( instruc == 'w') {
    digitalWrite(motorDNeg, LOW);
    digitalWrite(motorIPos, LOW);
    digitalWrite(motorDPos, HIGH);
    digitalWrite(motorINeg, HIGH);
  }
  
  else if ( instruc == 's'){
    digitalWrite(motorDPos, LOW);
    digitalWrite(motorINeg, LOW);
    digitalWrite(motorDNeg, HIGH);
    digitalWrite(motorIPos, HIGH);
  }
  
  else if (instruc == 'a') { 
    digitalWrite(motorDPos, HIGH);
    digitalWrite(motorINeg, LOW);
    digitalWrite(motorDNeg, LOW);
    digitalWrite(motorIPos, HIGH);
  }
  
  else if (instruc == 'd') { 
    digitalWrite(motorDPos, LOW);
    digitalWrite(motorINeg, HIGH);
    digitalWrite(motorDNeg, HIGH);
    digitalWrite(motorIPos, LOW);
  }
  else if (instruc == 'q') { 
    digitalWrite(motorDPos, LOW);
    digitalWrite(motorINeg, LOW);
    
    digitalWrite(motorDNeg, LOW);
    digitalWrite(motorIPos, LOW);
  }
  
  if (instruc == 'a' || instruc == 'd') { delay(100); }
  else { delay (100); }
  
  digitalWrite(motorDPos, LOW);
  digitalWrite(motorINeg, LOW);
  digitalWrite(motorDNeg, LOW);
  digitalWrite(motorIPos, LOW);
}



