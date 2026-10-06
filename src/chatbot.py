from src.predict_intent import predict_intent
from src.rag import retrieve_response


def chatbot_response(user_message):
    # 1. Predict the intent
    prediction = predict_intent(user_message)

    print("DEBUG prediction:", prediction)

    intent = prediction[0][0]

    # 2. Retrieve knowledge for that intent
    rag_result = retrieve_response(intent)

    # 3. Return a response
    if rag_result["found"]:
        return rag_result["response"]

    return (
        "Je suis désolé, mais je ne dispose pas actuellement "
        "d'informations vérifiées pour répondre à cette demande."
    )


if __name__ == "__main__":
    message = input("Vous : ")

    response = chatbot_response(message)

    print("\nBot :", response)