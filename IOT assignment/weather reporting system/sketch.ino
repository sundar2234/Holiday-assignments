#include <DHT.h>

#define DHTPIN 2     
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

void setup() {

    Serial.begin(9600);
    Serial.println("DHT22 Weather Reporting System");
    dht.begin();
}

void loop() {
    
    float temperature = dht.readTemperature(); 
    float humidity = dht.readHumidity();
 
    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("Error reading from DHT22 sensor!");
        return;
    }

    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println(" °C");

    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");
    Serial.println("---------------------------");
    delay(2000);
}
