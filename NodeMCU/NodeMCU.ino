/*
 * Instituto Tecnológico de Costa Rica
 * Computer Engineering
 * Taller de Programación
 * 
 * Código Servidor
 * Implementación del servidor NodeMCU
 * Proyecto 2, Semestre 1
 * 2019
 * 
 * Profesor: Milton Villegas Lemus
 * Autor: Santiago Gamboa Ramírez
 *        Emanuel Marín Gutiérrez
 *        Alejandro Vásquez Oviedo
 * 
 * Restricciónes: Biblioteca ESP8266WiFi instalada
 */
#include <ESP8266WiFi.h>

//Cantidad maxima de clientes es 1
#define MAX_SRV_CLIENTS 1
//Puerto por el que escucha el servidor
#define PORT 7070

/*
 * ssid: Nombre de la Red a la que se va a conectar el Arduino
 * password: Contraseña de la red
 * 
 * Este servidor no funciona correctamente en las redes del TEC,
 * se recomienda crear un hotspot con el celular
 */

// Nombre y contraseña de la red definidos
const char* ssid = "WifiCarE";
const char* password = "12345678";


// servidor con el puerto y variable con la maxima cantidad de 

WiFiServer server(PORT);
WiFiClient serverClients[MAX_SRV_CLIENTS];

/*
 * Intervalo de tiempo que se espera para comprobar que haya un nuevo mensaje
 */
unsigned long previousMillis = 0, temp = 0;
const long interval = 100;

/*
 * Pin donde está conectado el sensor de luz
 * Señal digital, lee 0 si hay luz y 1 si no hay.
 */
#define ldr D8 //GPIO15
#define blvl A0 //ADC
/**;
 * Variables para manejar las luces con el registro de corrimiento.
 * Utilizan una función propia de Arduino llamada shiftOut.
 * shiftOut(ab,clk,MSBFIRST,data), la función recibe 2 pines, el orden de los bits 
 * y un dato de 8 bits.
 * El registro de corrimiento tiene 8 salidas, desde QA a QH. Nosotros usamos 6 de las 8 salidas
 * Ejemplos al enviar data: 
 * data = B00000000 -> todas encendidas
 * data = B11111111 -> todas apagadas
 * data = B00001111 -> depende de LSBFIRST o MSBFIRST la mitad encendida y la otra mitad apagada
 */
#define ab  D6//GPIO12
#define clk D7//GPIO13 
/*
 * Variables para controlar los motores.
 * EnA y EnB son los que habilitan las salidas del driver.
 * EnA = 0 o EnB = 0 -> free run (No importa que haya en las entradas el motor no recibe potencia)
 * EnA = 0 -> Controla la potencia (Para regular la velocidad utilizar analogWrite(EnA,valor), 
 * con valor [0-1023])
 * EnB = 0 -> Controla la dirección, poner en 0 para avanzar directo.
 * In1 e In2 son inputs de driver, controlan el giro del motor de potencia
   * In1 = 0 ∧ In2 = 1 -> Moverse hacia adelante
   * In1 = 1 ∧ In2 = 0 -> Moverse en reversa
 * In3 e In4 son inputs de driver, controlan la dirección del carro
 * In3 = 0 ∧ In4 = 1 -> Gira hacia la izquierda
 * In3 = 1 ∧ In4 = 0 -> Gira hacia la derecha
 */
#define EnA D5 
#define In1 D4
#define In2 D3 
#define EnB D2 
#define In3 D1
#define In4 D0 

byte data = 0b11111111;
bool flag = true;

/**
 * Función de configuración.
 * Se ejecuta la primera vez que el módulo se enciende.
 * Si no puede conectarse a la red especificada entra en un ciclo infinito 
 * hasta ser reestablecido y volver a llamar a la función de setup.
 * La velocidad de comunicación serial es de 115200 baudios, tenga presente
 * el valor para el monitor serial.
 */
void setup() {
  Serial.begin(115200); 
  pinMode(In1,OUTPUT);//D4
  pinMode(In2,OUTPUT);//D3 
  pinMode(In3,OUTPUT);//D1
  pinMode(In4,OUTPUT);//D0
  pinMode(EnA,OUTPUT);//D5
  pinMode(EnB,OUTPUT);//D2
  pinMode(clk,OUTPUT);//D7
  pinMode(ab,OUTPUT);//D6
  
  pinMode(ldr,INPUT); //D8
  pinMode(blvl,INPUT); //A0

  analogWrite(EnA,0);
  analogWrite(EnB,0);
  shiftOut(ab, clk, MSBFIRST, data);

  // ip estática para el servidor
  IPAddress ip(192,168,43,200);
  IPAddress gateway(192,168,43,1);
  IPAddress subnet(255,255,255,0);

  WiFi.config(ip, gateway, subnet);

  // Modo para conectarse a la red
  WiFi.mode(WIFI_STA);
  // Intenta conectar a la red
  WiFi.begin(ssid, password);

  uint8_t i = 0;
  while (WiFi.status() != WL_CONNECTED && i++ < 20) delay(500);
  if (i == 21) {
    Serial.print("\nCould not connect to: "); Serial.println(ssid);
    while (1) delay(500);
  } else {
    Serial.println("\nIt´s connected");
    Serial.println("IP addressed: ");
    Serial.println(WiFi.localIP());
  }
  server.begin();
  server.setNoDelay(true);

}


/*
 * Función principal que llama a las otras funciones y recibe los mensajes del cliente
 * Esta función comprueba que haya un nuevo mensaje y llama a la función de procesar
 * para interpretar el mensaje recibido.
 */
void loop() {

  lightsensor();
  unsigned long currentMillis = millis();
  uint8_t i;
  //check if there are any new clients
  if (server.hasClient()) {
    for (i = 0; i < MAX_SRV_CLIENTS; i++) {
      //find free/disconnected spot
      if (!serverClients[i] || !serverClients[i].connected()) {
        if (serverClients[i]) serverClients[i].stop();
        serverClients[i] = server.available();
        continue;
      }
    }
    //no free/disconnected spot so reject
    WiFiClient serverClient = server.available();
    serverClient.stop();
  }

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    for (i = 0; i < MAX_SRV_CLIENTS; i++) {
      // El cliente existe y está conectado
      if (serverClients[i] && serverClients[i].connected()) {
        // El cliente tiene un nuevo mensaje
        if(serverClients[i].available()){
          // Leemos el cliente hasta el caracter '\r'
          String mensaje = serverClients[i].readStringUntil('\r');
          // Eliminamos el mensaje leído.
          serverClients[i].flush();
          
          // Preparamos la respuesta para el cliente
          String respuesta; 
          procesar(mensaje, &respuesta);
          Serial.println(mensaje);
          // Escribimos la respuesta al cliente.
          serverClients[i].println(respuesta);
        }  
        serverClients[i].stop();
      }
    }
  }
}

/*
 * Función para dividir los comandos en pares llave, valor
 * para ser interpretados y ejecutados por el Carro
 * Un mensaje puede tener una lista de comandos separados por ;
 * Se analiza cada comando por separado.
 * Esta función es semejante a string.split(char) de python
 * 
 */

void procesar(String input, String * output){
  //Buscamos el delimitador ;
  Serial.println("Checking input....... ");
  int comienzo = 0, delComa, del2puntos;
  bool result = false;
  delComa = input.indexOf(';',comienzo);
  
  while(delComa>0){
    String comando = input.substring(comienzo, delComa);
    Serial.print("Processing comando: ");
    Serial.println(comando);
    del2puntos = comando.indexOf(':');
    /*
    * Si el comando tiene ':', es decir tiene un valor
    * se llama a la función implementar 
    */
    if(del2puntos>0){
        String llave = comando.substring(0,del2puntos);
        String valor = comando.substring(del2puntos+1);

        Serial.print("(llave, valor) = ");
        Serial.print(llave);
        Serial.println(valor);
        //Una vez separado en llave valor 
        *output = implementar(llave,valor); 
    }
    else if(comando == "sense"){
      *output = getSense();         
    }     
    comienzo = delComa+1;
    delComa = input.indexOf(';',comienzo);
  }
}

String implementar(String llave, String valor){
  /**
   * La variable result puede cambiar para beneficio del desarrollador
   * Si desea obtener más información al ejecutar un comando.
   */
  String result="ok;";
  Serial.print("Comparing llave: ");
  Serial.println(llave);
  int pwm = valor.toInt();
  //#CÓDIGO PARA MOVER EL CARRO HACIA ADELANTE O HACIA ATRAS
  if(llave == "pwm"){
    Serial.print("Move....: ");
    Serial.println(valor);
    int valorInt = valor.toInt();
    
    //Mover hacia atras
    if (valorInt < 0 && valorInt >= -1023){
    analogWrite(EnA,abs(valorInt));
    digitalWrite(In1,LOW);
    digitalWrite(In2,HIGH);
    data &= 0b11110011;
    Serial.println(data);
    shiftOut(ab, clk, MSBFIRST, 0b11110011);
    } 
    //Mover hacia adelante
    else if (valorInt > 0 and valorInt <= 1023){
    analogWrite(EnA,valorInt);
    digitalWrite(In1,HIGH);
    digitalWrite(In2,LOW);  
    }
    //No mover
    else if (valorInt == 0){
      analogWrite(EnA,0);
      analogWrite(EnB,0);
    }
    else{
      return "valor fuera de rango";
    }
  }
  //#CÓDIGO PARA MOVER EL CARRO A LA IZQUIERDA O A LA DERECHA
  else if(llave == "dir"){
    switch (valor.toInt()){
      case 1:
        Serial.println("Girando derecha");
        analogWrite(EnB,1023);
        digitalWrite(In3,LOW);
        digitalWrite(In4,HIGH);
        //# CÓDIGO PARA GIRAR DERECHA
        break;
      case -1:
        Serial.println("Girando izquierda");
        analogWrite(EnB,1023);
        digitalWrite(In3,HIGH);
        digitalWrite(In4,LOW);
        //# CÓDIGO PARA GIRAR IZQUIERDA
        break;
       default:
        Serial.println("directo");
        analogWrite(EnB,1023);
        digitalWrite(In3,LOW);
        digitalWrite(In4,LOW);        
        //# CÓDIGO PARA NO GIRAR 
        break;
    }
  }
  //#CÓDIGO PARA EL ENCENDIDO Y APAGADO DE LAS LUCES
  else if(llave[0] == 'l'){
    Serial.println("Cambiando Luces");
    Serial.print("valor luz: ");
    Serial.println(valor);
    switch (llave[1]){
      case 'f':
        Serial.println("Luces frontales");
        if (valor == "0"){
          flag=true;
          data &= 0b11111100;
          Serial.println(data);  
        }
        else {
          flag=false;
          data |= 0b00000011;
          Serial.println(data);
        }
        //# CÓDIGO PARA ENCENDER O APAGAR LUCES FRONTALES
        break;
      case 'b':
        Serial.println("Luces traseras");
        if (valor == "0"){
        data &= 0b11110011;
        Serial.println(data);
        }
        else{
        data |= 0b00001100;
        Serial.println(data);
        }
        //# CÓDIGO PARA ENCENDER O APAGAR LUCES TRASERAS
        break;
      case 'l':
        Serial.println("Luces izquierda");
        if (valor == "0"){
        data &= 0b11011111;
        Serial.println(data);
        }
        else{
        data |= 0b00100000;
        Serial.println(data);
        }
        //# CÓDIGO PARA ENCENDER O APAGAR DIRECCIONAL IZQUIERDA
        break;
      case 'r':
        Serial.println("Luces derechas");
        if (valor == "0"){
        data &= 0b11101111;
        Serial.println(data);
        }
        else{
        data |= 0b00010000;
        Serial.println(data);
        }        
        //# CÓDIGO PARA ENCENDER O APAGAR DIRECCIONAL DERECHA
        break;
      default:
        Serial.println("Ninguna de las anteriores");
        break;
    }
  }
  //#CÓDIGO PARA EL MOVIMIENTO ESPECIAL "CIRCLE"
  else if(llave == "circle"){
    switch(valor.toInt()){
      case 1:
        analogWrite(EnA,1000);
        digitalWrite(In1,HIGH);
        digitalWrite(In2,LOW);
        analogWrite(EnB,1023);
        digitalWrite(In3,LOW);
        digitalWrite(In4,HIGH);
        delay(7500);
        analogWrite(EnA,0);
        analogWrite(EnB,1023);
        digitalWrite(In3,LOW);
        digitalWrite(In4,LOW);
        //#CÓDIGO PARA EL MOVIMIENTO ESPECIAL "CIRCLE" HACIA ADELANTE Y A LA DERECHA
        break;

      case -1:
        analogWrite(EnA,1000);
        digitalWrite(In1,HIGH);
        digitalWrite(In2,LOW);
        analogWrite(EnB,1023);
        digitalWrite(In3,HIGH);
        digitalWrite(In4,LOW);
        delay(7500);
        analogWrite(EnA,0);
        analogWrite(EnB,1023);
        digitalWrite(In3,LOW);
        digitalWrite(In4,LOW); 
        //#CÓDIGO PARA EL MOVIMIENTO ESPECIAL "CIRCLE" HACIA ADELANTE Y A LA IZQUIERDA
        break; 
    }
  }
  //#CÓDIGO PARA EL MOVIMIENTO ESPECIAL "INFINITE"
  else if (llave == "infinite"){
        analogWrite(EnA,1000);
        digitalWrite(In1,HIGH);
        digitalWrite(In2,LOW);
        analogWrite(EnB,1023);
        digitalWrite(In3,LOW);
        digitalWrite(In4,HIGH);
        delay(6000);
        analogWrite(EnA,1000);
        digitalWrite(In1,HIGH);
        digitalWrite(In2,LOW);
        analogWrite(EnB,1023);
        digitalWrite(In3,HIGH);
        digitalWrite(In4,LOW);
        delay(6000);
        analogWrite(EnA,0);
        analogWrite(EnB,1023);
        digitalWrite(In3,LOW);
        digitalWrite(In4,LOW);
  }
  //#CÓDIGO PARA EL MOVIMIENTO ESPECIAL "ZIGZAG"
  else if (llave == "zigzag"){
        analogWrite(EnA,1000);
        digitalWrite(In1,HIGH);
        digitalWrite(In2,LOW);
        analogWrite(EnB,1000);
        digitalWrite(In3,HIGH);
        digitalWrite(In4,LOW);
        delay(1000);
        digitalWrite(In3,LOW);
        digitalWrite(In4,HIGH);
        delay(800);
        digitalWrite(In3,HIGH);
        digitalWrite(In4,LOW);
        delay(1000);
        digitalWrite(In3,LOW);
        digitalWrite(In4,HIGH);
        delay(800);
        digitalWrite(In3,HIGH);
        digitalWrite(In4,LOW);
        delay(1000);
        digitalWrite(In3,LOW);
        digitalWrite(In4,HIGH);
        delay(800);
        analogWrite(EnA,0);
        analogWrite(EnB,1023);
        digitalWrite(In3,LOW);
        digitalWrite(In4,LOW);
  }
  //#CÓDIGO PARA EL COMANDO ESPECIAL "KATARSYS"
  else if (llave=="katarsys"){
    analogWrite(EnA,1000);
    digitalWrite(In1,HIGH);
    digitalWrite(In2,LOW);
    analogWrite(EnB,1023);
    digitalWrite(In3,HIGH);
    digitalWrite(In4,LOW);
    delay(7200);
    digitalWrite(In3,LOW);
    digitalWrite(In3,LOW);
    delay(1000);
    digitalWrite(In3,HIGH);
    digitalWrite(In4,LOW);
    delay(7200);
    digitalWrite(In3,LOW);
    digitalWrite(In4,LOW);
    delay(1000);
    digitalWrite(In3,HIGH);
    digitalWrite(In4,LOW);
    delay(7200);
    digitalWrite(In3,LOW);
    digitalWrite(In4,LOW);
    delay(1000);
    digitalWrite(In3,HIGH);
    digitalWrite(In4,LOW);
    delay(7200);
    analogWrite(EnA,0);
    analogWrite(EnB,1023);
    digitalWrite(In3,LOW);
    digitalWrite(In4,LOW);
  }
  else{
    result = "Undefined key value: " + llave+";";
    Serial.println(result);
    //Se envia un mensaje indicandole al usurio que el comando ingresado no pertenece al conjunto de comandos definidos
  }
  shiftOut(ab, clk, MSBFIRST, data);
  //shiftOut, función precosntruida ideal para el manejo de luces en conjunto con el registro de corrimiento
  return result;
}

int lightsensor(){
  if (flag==true){
    int fotores;
    fotores = digitalRead(ldr);
    if (fotores==0){
      data |= 0b00000011;
      delay(500);
    }
    else{
      data &= 0b11111100;
      delay(500);
    }
    shiftOut(ab, clk, MSBFIRST, data);
  }
  else if (flag==false){
    //Serial.println("Se está ejecuntado el comando lf");
  }
}

/**
 * Función para obtener los valores de telemetría del auto
 */
String getSense(){
  //# CÓDIGO PARA LEER LOS VALORES DESEADOS
  int batterylvl = FuncBateria();
  int light = digitalRead(ldr);

  char sense [16];
  sprintf(sense, "blvl:%d;ldr:%d;", batterylvl, light);
  Serial.print("Sensing: ");
  Serial.println(sense);
  return sense;
}
float RatioFactor=2.48;
int FuncBateria(){
  float TotalVolt = 0.0;
  float Vvalue=0.0,Rvalue=0.0;

  for(unsigned int i=0;i<10;i++){
    Vvalue=Vvalue+analogRead(blvl);
    delay(5);
  }
  Vvalue=(float)Vvalue/10.0;
  Rvalue=(float)(Vvalue/1023.0)*3.3;
  TotalVolt=Rvalue*RatioFactor;
  if(TotalVolt>=7.5){
    return 100;
  }
  else if(TotalVolt>=7.4){
    return 90;
  }
  else if(TotalVolt>=7.3){
    return 80;
  }
  else if(TotalVolt>=7.2){
    return 70;
  }
  else if(TotalVolt>=7.1){
    return 60;
  }
  else if(TotalVolt>=7.0){
    return 50;
  }
  else if(TotalVolt>=6.9){
    return 40;
  }
  else if(TotalVolt>=6.8){
    return 30;
  }
  else if(TotalVolt>=6.7){
    return 20;
  }
  else if(TotalVolt>=6.6){
    return 10;
  }
  else if(TotalVolt<6.6){
    return 0;
  }
}
