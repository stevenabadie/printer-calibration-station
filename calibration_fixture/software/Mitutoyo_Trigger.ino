
#define LED    13
#define TEST    8
#define RLY     7


// Serial Command Inputs Variables

String Input_String = "";              // a String to hold incoming data

bool bStringComplete = false;         // whether the string is complete

String Command_String;

uint8_t Command_Char;

int8_t Cmd_Variable;


void Pulse_LED (void)
{
//  delay(1000);
  
  digitalWrite(RLY, HIGH);
  digitalWrite(LED, HIGH);
  delay(500);
  digitalWrite(LED, LOW);
  digitalWrite(RLY, LOW);
}

void Multi_Pulse_LED (uint8_t P_Num)
{
  delay(1000);
  
  for(uint8_t P_Count = 0; P_Count < P_Num; P_Count++)
  {
    digitalWrite(RLY, HIGH);
    digitalWrite(LED, HIGH);
    delay(500);
    digitalWrite(LED, LOW);
    digitalWrite(RLY, LOW);
    delay(500);
  }
  
}


void Parse_Command (void)
{

  // Commands

  // A        Close Relay for 500ms
  // ID?      Send TF_100 to Serial Port

  
  char Cmd_Str[6];

  Command_String.toCharArray(Cmd_Str, 2);

  if(!strcmp(Cmd_Str, "A"))
  {
    Pulse_LED();
    return;
  }

  if(!strcmp(Cmd_Str, "I"))
  {
    Serial.println("TF_100");
    return;
  }

  if(Command_String.charAt(1) != 0x20)
  {
    Serial.println("Unknown Command");
    return;
  }

  Command_String.remove(0, 1);

  Cmd_Variable = Command_String.toInt();

  Serial.print("Cmd Var = ");

  Serial.println(Cmd_Variable, DEC);

  if(!strcmp(Cmd_Str, "M"))               // Step Motor (Cmd_Variable) Steps Right
  {
    Multi_Pulse_LED(Cmd_Variable);
  }
  else
  {
    Serial.println("Unknown Command");
  }
}

void setup()
{
  Serial.begin(115200);

  Serial.println("Program Start");

  // Initialize Pins

  pinMode(LED, OUTPUT);
  pinMode(RLY, OUTPUT);
  pinMode(TEST, OUTPUT);

  digitalWrite(LED, LOW);
  digitalWrite(RLY, LOW);
  digitalWrite(TEST, LOW);

}

void loop()
{
  if (bStringComplete)
  {
    Command_String = Input_String;
    
//    Serial.println(Command_String);
    // clear the string:
    Input_String = "";
    bStringComplete = false;

    Parse_Command();
  }
}


void serialEvent()
{
  while (Serial.available())
  {
    // get the new byte:
    
    char inChar = (char)Serial.read();


    if((inChar == 'X') || (inChar == 'x'))                          // X or x - Stop Everything
    {
      
      return;
    }
    
    // add it to the inputString:
    
    Input_String += inChar;
    
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    
    if (inChar == '\n')
    {
      bStringComplete = true;
    }
  }
}
