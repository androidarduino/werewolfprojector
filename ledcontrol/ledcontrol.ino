#include <FastLED.h>
#include <Stepper.h>
#define STEPS 2038 // the number of steps in one revolution of your motor (28BYJ-48)

Stepper stepper(STEPS, 8, 10, 9, 11);
int currentDegree = 0; // real degree * 10

void turnToDegree(int degree) {
  float r = degree - currentDegree;
  r = r / 3600 * STEPS;
  currentDegree = degree;
  //Serial.print("stepper motor turning for ");
  //Serial.println(int(r));
  stepper.step(int(r)); // do 2038 steps -- corresponds to one revolution in one minute
}
#define LED_PIN     7
#define NUM_LEDS    14

CRGB leds[NUM_LEDS];

String inData;

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  stepper.setSpeed(12);// step motor runs at 12rpm
  Serial.println("Connected. Ready to Serve.");
}

String updateLEDs() {
  if (inData.length() != 22) return "500. Invalid length." + String(inData.length());
  for (int i=0; i < NUM_LEDS; i++) {
    char c = inData.charAt(i);
    switch(c) {
      case 'b': leds[i] = CRGB(0,0,0); break;
      case 'g': leds[i] = CRGB(0,255,0); break;
      case 'r': leds[i] = CRGB(255,0,0); break;
      case 'l': leds[i] = CRGB(0,0,255); break;
      case 'o': leds[i] = CRGB(255,165,0); break;
      case 's': leds[i] = CRGB(200,0,200); break;
      case 'w': leds[i] = CRGB(128,128,128); break;
      case 'y': leds[i] = CRGB(255,255,0); break;
      case 'c': leds[i] = CRGB(0,255,255); break;
    }
  }
  return "200. OK.";
}

void loop() {
  while (Serial.available() > 0)
  {
      char recieved = Serial.read();
      inData += recieved; 

      // Process message when new line character is recieved
      if (recieved == ',')
      {
          //Serial.print("Arduino Received: ");
          //Serial.print(inData);
          Serial.println(updateLEDs());
          inData = ""; // Clear recieved buffer
          int angle = Serial.parseInt();
          //Serial.print("turning to angle: ");
          //Serial.println(angle);
          turnToDegree(angle);
      }
  }
  FastLED.show();
  delay(100);
  /*
  leds[0] = CRGB(255, 0, 0);
  FastLED.show();
  delay(500);  
  leds[1] = CRGB(0, 255, 0);
  FastLED.show();
  delay(500);
  leds[2] = CRGB(160, 160, 160);
  FastLED.show();
  delay(500);
  leds[5] = CRGB(150, 0, 255);
  FastLED.show();
  delay(500);
  leds[9] = CRGB(255, 200, 20);
  FastLED.show();
  delay(500);
  leds[13] = CRGB(0, 0, 255);
  FastLED.show();
  delay(500);
  */
}
