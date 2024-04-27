import random
import time
from openai import OpenAI

class Car:
    def __init__(self):
        self.state = "desligado"
        self.speed = 0
        self.engine_temp = 90  # Normal operating temperature in degrees Celsius
        self.fuel_level = 100  # Fuel level as a percentage

    def turn_on(self):
        self.state = "ligado"
        self.speed = 0
        self.update_data()

    def turn_off(self):
        self.state = "desligado"
        self.speed = 0
        self.update_data()

    def drive(self):
        self.state = "dirigindo"
        self.speed = random.randint(30, 100)
        self.fuel_level -= random.uniform(0.1, 0.5)
        self.engine_temp += random.uniform(0, 2)
        self.update_data()

    def stop(self):
        self.state = "estacionado"
        self.speed = 0
        self.update_data()

    def update_data(self):
        print(f"Estado: {self.state}, Velocidade: {self.speed} km/h, Temperatura do Motor: {self.engine_temp}°C, Nível de Combustível: {self.fuel_level}%")

    def get_current_info(self):
        return {
            "Estado": self.state,
            "Velocidade": self.speed,
            "Temperatura": self.engine_temp,
            "Nível de Combustível": self.fuel_level
        }

def answer_question_with_gpt4(car, question):
    info = car.get_current_info()
    context = f"O estado do carro é {info['Estado']}. A velocidade atual é {info['Velocidade']} km/h. " \
              f"Restam {info['Nível de Combustível']}% de combustível." \
              f"A temperatura do motor é {info['Temperatura']}°C. "
    
    prompt = f"{context} {question}"
    
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    history = [
        {"role": "system", "content": "Você é um assistente inteligente e deve apenas responder a pergunta em português do Brasil e nada mais."},
        {"role": "user", "content": prompt},
    ]

    completion = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=history,
        temperature=0.7,
        stream=True,
    )
    
    # Agora o loop continua até que todo o conteúdo seja impresso
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
         
    
    print()
   

def main():
    my_car = Car() 
    my_car.turn_on()
    my_car.drive()   

    print("Faça perguntas sobre o carro. Digite 'end' para terminar.")


    while True:
        question = input("Qual é a sua pergunta? ")

        if question.lower() == "fim":
            print("Programa finalizado.")
            break

        answer_question_with_gpt4(my_car, question)
       

# Chamada da função principal
main()





