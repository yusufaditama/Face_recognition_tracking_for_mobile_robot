#include <Servo.h>
Servo servox;
Servo servoy;
int pos;
int t=90;
int u= 60;

//int trig= 11;            // put the trigger pin to digital pin 11 on the arduino
//int echo= 10;            // put the echo pin to digital pin 12 on the arduino
//int maximumRange = 200; //kebutuhan akan maksimal range
//int minimumRange = 00; //kebutuhan akan minimal range
//long duration, distance; //waktu untuk kalkulasi jarak
 
// Motor A
 
int enA = 5;
int in1 = 12;
int in2 = 13;
 
// Motor B
 
int enB = 3;
int in3 = 7;
int in4 = 8;

void setup() {

  servox.attach(6);
  servoy.attach(9);
  Serial.begin (9600);

  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  //pinMode(trig, OUTPUT);    // set pin trig to OUTPUT
  //pinMode(echo, INPUT);     // set pin echo to INPUT

  servox.write(t);
  servoy.write(u);
}

void  loop() {

digitalWrite(trig, LOW);delayMicroseconds(2);
digitalWrite(trig, HIGH);delayMicroseconds(10);
digitalWrite(trig, LOW);
duration = pulseIn(echo, HIGH);
 
//perhitungan untuk dijadikan jarak
distance = duration/58.2;
Serial.println(distance);

if (distance > 30){
  /*Sumbu X*/
 if (Serial.available()>0)
 {
  pos = Serial.read();
  Serial.println(pos);
    if (pos==49 || pos ==1)
    {
      t = t+5;
      servox.write(t);
      belokKanan();
    }
    else if (pos==50 || pos ==2)
    {
      t = t-5;
      servox.write(t);
      belokKiri();
    }
    else if (pos==48 || pos==0)
    {
      servox.write(t);
      jalan();
    }
    

   /*Sumbu Y*/
    if (pos==51 || pos ==3)
    {
      u = u-5;
      servoy.write(u);
    }
    else if (pos==52 || pos ==4)
    {
      u = u+5;
      servoy.write(u);
    }
    else if (pos==53 || pos==5)
    {
      servoy.write(u);
    }
 }
}
 //Serial.println(pos);
 else if (distance < 31){
  Serial.end();
  berhenti();   
 }

}

void jalan(){
  //kiri
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enA, 65);

  //kanan
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB, 60);
}

void belokKiri(){
  //kiri
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enA, 50);

  //kanan
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB, 100);
}

void belokKanan(){
  //kiri
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enA, 100);

  //kanan
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB, 50);
}

void berhenti(){
  //kiri
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enA, 0);

  //kanan
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB, 0);
}
  
  
  
  
  
 
