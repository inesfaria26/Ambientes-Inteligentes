# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import random
import requests
from rasa_sdk.events import SlotSet
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import transformers
from transformers import pipeline
"""""
class ActionGuardarDados(Action):
    def name(self) -> Text:
        return "action_dados"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        idade = tracker.get_slot("idade")
        sexo = tracker.get_slot("sexo")
        saturacao = tracker.get_slot("saturacaoO2")
        frequencia = tracker.get_slot("frequencia")

        if saturacao is None or frequencia is None or idade is None or sexo is None:
            dispatcher.utter_message(text="Eu não sei os seus dados.")
        else:
            dispatcher.utter_message(
                text=f"O valor de saturação de oxigénio é {saturacao} kg e o valor da frequência cardíaca é {frequencia} cm. Tem {idade} anos e é do sexo {sexo}.")
        return []
"""""


API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": "Bearer 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"}
def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad response status
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle request errors here
        print("Request Error:", e)
        return None
    except ValueError as e:
        # Handle JSON decoding errors here
        print("JSON Decode Error:", e)
        return None

class ActionCriarPlanoComplementar(Action):

    def name(self) -> Text:
        return "action_tratamento_complementar"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_input = tracker.latest_message['text']
        payload = {"inputs": user_input}

        try:
            response_data = query(payload)
            if response_data:
                answer = response_data[0]["generated_text"]
                dispatcher.utter_message(text=answer)
            else:
                dispatcher.utter_message(text="A resposta da API não contém o texto gerado.")
        except Exception as e:
            dispatcher.utter_message(text=f"Ocorreu um erro durante a chamada da API: {str(e)}")

        return []
"""""
class ActionCriarPlanoComplementar(Action):

    def name(self) -> Text:
        return "action_tratamento_complementar"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Obter informações sobre o tratamento prescrito pelo médico

        tratamento1 = tracker.get_slot("tratamento_comp")
        if not tratamento1:
            dispatcher.utter_message("Desculpe, não consegui encontrar informações sobre o tratamento prescrito pelo médico.")
            return []
        # Contexto sobre o tratamento prescrito pelo médico

        contexto = f"O tratamento prescrito pelo médico inclui {tratamento1}. Como tratamento complementar, sugiro o seguinte:"
        # Load do modelo de geração de texto

        model = pipeline("text-generation")
        # Gerar tratamento complementar
        response = model(contexto, max_length=50, num_return_sequences=1)[0]['generated_text']

        dispatcher.utter_message(f"Aqui está o seu plano complementar: {response}")

        return []
"""""
class ActionQualidadeAr(Action):
    def name(self) -> Text:
        return "action_qualidade_ar"

    def extract_value(self, text: str, keyword: str) -> float:
        """Extrai um valor a partir de uma palavra-chave no texto."""
        match = re.search(rf"{keyword}\s*:\s*([-+]?\d*\.\d+|\d+)", text)
        return float(match.group(1)) if match else None

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #if tracker.latest_message.get("intent", {}).get("name") == "informar sobre a qualidade do ar" or "avisar sobre a qualidade do ar":
            # Obter o valor da entidade diretamente do tracker

            longitude = next(tracker.get_latest_entity_values("informar_cidade1"), None)
            latitude = next(tracker.get_latest_entity_values("informar_cidade2"), None)

            #latitude = tracker.get_slot("informar_cidade2")
            #longitude = tracker.get_slot("informar_cidade1")

            print(latitude)
            print(longitude)

            if longitude and latitude:
                qualidade = self.obter_qualidade(latitude, longitude)
                dispatcher.utter_message(f"A qualidade do ar na sua cidade é de {qualidade}.")
            else:
                dispatcher.utter_message("Dados errados. Forneça novamente os seus dados")

            return []
        #else:
            #dispatcher.utter_message("Por favor, forneça os seus dados de localização.")
        #return []

    def obter_qualidade(self, lat, lon: str) -> str:
        api_key = 'e56a058a29d2855eb09daf3639552b97'
        # Substitua esta URL pela API que fornece informações sobre a qualidade do ar
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

        resposta = requests.get(url)
        dados = resposta.json()
        qualidade = dados["main"]["aqi"]

        return qualidade