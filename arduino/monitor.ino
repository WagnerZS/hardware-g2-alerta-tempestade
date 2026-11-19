#include "DHT.h"

// =========================
// CONFIGURAÇÃO DOS PINOS
// =========================

#define PINO_DHT 2
#define TIPO_DHT DHT11

const int PINO_HALL = A0;
const int PINO_LED_VERMELHO = 13;
const int PINO_BUZZER = 7;

DHT dht(PINO_DHT, TIPO_DHT);

unsigned long ultimaLeitura = 0;

const unsigned long intervaloLeitura = 2000;

String comandoRecebido = "";

void setup() {

  Serial.begin(9600);

  dht.begin();

  pinMode(PINO_LED_VERMELHO, OUTPUT);
  pinMode(PINO_BUZZER, OUTPUT);

  desligarAlerta();
}

void loop() {
  verificarSerial();

  if (millis() - ultimaLeitura >= intervaloLeitura) {
    ultimaLeitura = millis();

    enviarSensores();
  }
}

void enviarSensores() {
  int valorMagnetico = analogRead(PINO_HALL);

  float umidade = dht.readHumidity();
  float temperatura = dht.readTemperature();

  if (isnan(umidade) || isnan(temperatura)) {
    Serial.println("ERRO_DHT");
    return;
  }

  Serial.print("{\"temp\":");
  Serial.print(temperatura, 1);

  Serial.print(",\"umid\":");
  Serial.print(umidade, 1);

  Serial.print(",\"mag\":");
  Serial.print(valorMagnetico);

  Serial.println("}");
}

void verificarSerial() {
  while (Serial.available() > 0) {
    char caractere = Serial.read();

    if (caractere == '\n') {
      comandoRecebido.trim();

      if (comandoRecebido == "A") {
        ativarAlerta();
      } else if (comandoRecebido == "N") {
        desligarAlerta();
      }
      comandoRecebido = "";
    } else {
      comandoRecebido += caractere;
    }
  }
}

void ativarAlerta() {
  digitalWrite(PINO_LED_VERMELHO, HIGH);

  tone(PINO_BUZZER, 2000);
}

void desligarAlerta() {
  digitalWrite(PINO_LED_VERMELHO, LOW);

  noTone(PINO_BUZZER);
}
