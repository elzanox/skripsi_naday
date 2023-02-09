#include "WifiCam.hpp"
#include <WiFi.h>

//// Set your Static IP address
//IPAddress local_IP(192, 168, 137, 184);
//// Set your Gateway IP address
//IPAddress gateway(192, 168, 137, 1);
//IPAddress subnet(255, 255, 0, 0);

//static const char* WIFI_SSID = "esp32cam-yolo";
//static const char* WIFI_PASS = "yolo1234";

static const char* WIFI_SSID = "MAKAN";
static const char* WIFI_PASS = "LAPERBANGET";

const int flashLED = 4;
esp32cam::Resolution initialResolution;

WebServer server(80);

void
setup()
{
  Serial.begin(115200);
  Serial.println();
  delay(2000);
//  if(!WiFi.config(local_IP, gateway, subnet)) {
//  Serial.println("STA Failed to configure");
//}
  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("WiFi failure");
    delay(5000);
    ESP.restart();
  }
  Serial.println("WiFi connected");
  
  {
    using namespace esp32cam;

    initialResolution = Resolution::find(1024, 768);

    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(initialResolution);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    if (!ok) {

      
      Serial.println("camera initialize failure");
      delay(5000);
      ESP.restart();
    }
    Serial.println("camera initialize success");
    pinMode(flashLED,OUTPUT);
    digitalWrite(flashLED,50);
    Serial.println("FLASH LED ON");
  }

  Serial.println("camera starting");
  Serial.print("http://");
  Serial.println(WiFi.localIP());

  addRequestHandlers();
  server.begin();
}

void
loop()
{
  server.handleClient();
}
