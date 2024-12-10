#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 5
#define SensorPin A0  // pH meter Analog output
#define Offset -3  // Deviation compensate
#define LED 13
#define samplingInterval 20
#define printInterval 800
#define ArrayLenth 40 // Times of collection

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

int pHArray[ArrayLenth]; // Store average value
int pHArrayIndex = 0;

// Function declaration
double avergearray(int* arr, int number);

void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
  Serial.println("pH meter experiment!");
  
  // Initialize temperature sensor
  sensors.begin();
}

void loop() {
  static unsigned long samplingTime = millis();
  static unsigned long printTime = millis();
  static float pHValue, voltage;

  // Read pH value
  if (millis() - samplingTime > samplingInterval) {
    pHArray[pHArrayIndex++ % ArrayLenth] = analogRead(SensorPin);
    voltage = avergearray(pHArray, ArrayLenth) * 5.0 / 1024.0;
    pHValue = 3.5 * voltage + Offset;
    samplingTime = millis();
  }

  // Print pH and temperature
  if (millis() - printTime > printInterval) {
    Serial.print("PH: ");
    Serial.print(pHValue, 2);
    digitalWrite(LED, !digitalRead(LED)); // Toggle LED

    sensors.requestTemperatures();
    float temperature = sensors.getTempCByIndex(0);
    if (temperature != DEVICE_DISCONNECTED_C) {
      Serial.print(" Temperature: ");
      Serial.println(temperature);
    } else {
      Serial.println(" Temperature sensor disconnected!");
    }

    printTime = millis();
  }
}

double avergearray(int* arr, int number) {
  if (number <= 0) {
    Serial.println("Error: invalid array length!");
    return 0;
  }

  long amount = 0;
  int min = arr[0], max = arr[0];

  for (int i = 0; i < number; i++) {
    if (arr[i] < min) {
      min = arr[i];
    } else if (arr[i] > max) {
      max = arr[i];
    }
    amount += arr[i];
  }

  // Exclude the minimum and maximum values
  amount -= min;
  amount -= max;

  return (double)amount / (number - 2);
}
