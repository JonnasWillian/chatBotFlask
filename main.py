from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Variável global para armazenar o estado de cada usuário
users_state = {}

if __name__ == "__main__":
    app.run(debug=True)

def handle_initial_message(user_response, user_id):
    response = MessagingResponse()
    if user_response.lower() == 'iniciar':
        users_state[user_id] = 'question1'
        response.message("Qual é o seu nome?")
    else:
        response.message("Digite 'iniciar' para começar.")
    return str(response)


def handle_question1(user_response, user_id):
    response = MessagingResponse()
    users_state[user_id] = 'question2'
    response.message("Qual é a sua idade?")
    return str(response)


def handle_question2(user_response, user_id):
    response = MessagingResponse()
    users_state[user_id] = 'question3'
    response.message("Qual é o motivo do seu contato?")
    return str(response)


def handle_question3(user_response, user_id):
    response = MessagingResponse()
    users_state[user_id] = 'waiting_for_agent'
    response.message("Obrigado. Um atendente entrará em contato com você em breve.")
    # Aqui você pode adicionar a lógica para notificar um atendente
    return str(response)


@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():
    user_response = request.form.get('Body')
    user_id = request.form.get('From')

    if user_id not in users_state:
        users_state[user_id] = 'initial'

    if users_state[user_id] == 'initial':
        return handle_initial_message(user_response, user_id)
    elif users_state[user_id] == 'question1':
        return handle_question1(user_response, user_id)
    elif users_state[user_id] == 'question2':
        return handle_question2(user_response, user_id)
    elif users_state[user_id] == 'question3':
        return handle_question3(user_response, user_id)
    elif users_state[user_id] == 'waiting_for_agent':
        response = MessagingResponse()
        response.message("Um atendente entrará em contato com você em breve.")
        return str(response)

    return str(MessagingResponse().message("Desculpe, não entendi. Tente novamente."))


if __name__ == "__main__":
    app.run(debug=True)
