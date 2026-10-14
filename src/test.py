from src.predict_intent import predict_intent

sentences = [
    "daw makanch",
    "lgaz ma ykhdemch",
    "Daw rah yroho w yji fel dar",
    "Imta yarja3 daw ?",
    "Kifach nkhaless la facture ta3i",
    "how can I pay my bill online",
    "J'ai payé en ligne mais le paiement n'apparaît pas",
    "Kayen rihet gaz fel cuisine",
    "Ma kayench daw fel houma kamla",
    "Le gaz est coupé dans tout le quartier",
    "Le chauffage ne reçoit plus de gaz",
    "Gaz kayen fel houma mais machi fel dar",
    "La facture ta3i estimée, pourquoi ?",
    "J'ai reçu deux factures pour la même période",
    "Kifach n3ared 3la facture ghalia ?",
    "Le compteur affiche des chiffres bizarres",
    "L'index du compteur est incorrect",
    "Mon compteur tourne trop vite",
    "Qui contacter pour changer un compteur défectueux ?",
    "Kifach nbelagh 3la panne",
]

for sentence in sentences:
    predictions = predict_intent(sentence)

    print(f"\nSentence: {sentence}")
    print(f"Predicted: {predictions[0][0]}")
    print(f"Confidence: {predictions[0][1]:.3f}")