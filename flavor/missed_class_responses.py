import random
import math

from constants import limit_status

first_missed_class = [
    "Poxa... Você estava indo tão bem",
    "Pra tudo tem a primeira vez, né?",
    "E eu que achava que você era um bom exemplo de aluno."
]

second_missed_class = [
    "Tá virando um hábito, hein?",
    "Putz, agora que tudo desanda",
    "De novo???"
]

half_past_the_limit = [
    "Você sabe que não é uma competição, né?",
    "Você ainda lembra onde é a sua sala?",
    "Você ta ciente do que você ta fazendo?"
]

at_the_limit = [
    "O professor sabe que você tá fazendo essa matéria?",
    "Espero que você não fique doente a partir de agora",
    "Sem emoção não tem graça, né?"
]

over_the_limit = [ 
    "MANO DO CÉU espero que seu professor não ligue pra faltas",
    "Você ri da cara do perigo, tô impressionado.",
    "O que mais me espanta é você ainda ter coragem de vir aqui me mandar isso."
]

general_responses = [
    "Aposto que essa aula era importante só porque você faltou kkkk",
    "Fiquei sabendo que hoje tinha prova surpresa",
    "Espero que você tenha uma boa explicação pra isso."
]

def choose_missed_class_response(missed_classes, limit):
    missed_classes_percent = (missed_classes * 100) / limit
    missed_classes_percent = math.floor(missed_classes_percent)

    if missed_classes == 1:
        return random.choice(first_missed_class + general_responses)
    elif missed_classes == 2:
        return random.choice(second_missed_class + general_responses)
    elif missed_classes_percent >= limit_status.WARNING and missed_classes < limit:
        return random.choice(half_past_the_limit + general_responses)
    elif missed_classes == limit:
        return random.choice(at_the_limit)
    else:
        return random.choice(over_the_limit)