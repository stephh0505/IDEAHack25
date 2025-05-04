#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>

#define TFT_CS  15
#define TFT_DC  2
#define TFT_RST 4
#define CHAR_SZ 3
#define C_HEIGHT 8 * 3
#define C_WIDTH 6 * 3

Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC, TFT_RST);

void setup() {
  tft.begin();
  tft.setRotation(1);  // This rotation works

  tft.fillScreen(ILI9341_BLACK);

  // Define text
  String text = "SY BAU.";
  tft.setTextSize(CHAR_SZ);
  tft.setTextColor(ILI9341_WHITE);

  Serial.begin(115200);

  setCenter("");
}

void loop() {
  // Nothing her
  // tft.setCursor(x, y);
  // tft.println(text);
}

void setCenter(String s) {
  int height = tft.height();
  int width = tft.width();
  int cHeight = height - C_HEIGHT;
  int cWidth = width - C_WIDTH;
  tft.setCursor(cHeight, cWidth);
  Serial.println(width);
  Serial.println(height);
  tft.println(cHeight);
  tft.println(height);
  tft.println(cWidth);
  tft.println(width);
}