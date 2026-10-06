import pandas as pd

FILE = "data/dataset_facture.xlsx"
df = pd.read_excel(FILE)
MOVE_TO_CATCH_UP = {
    # Daridja Arabic
    "علاش لازم نخلص هاد الرتاج؟",
    "ما فهمتش علاش فاتورة الرتاج طالعة بزاف.",
    "علاش مبلغ الرتاج طالع بزاف؟",
    "علاش هاد التسوية كبيرة بزاف؟",
    "علاش زدتوا هاد المبلغ في الفاتورة؟",
    "علاش لازم نخلص فرق كبير هكا؟",
    "ما فهمتش منين جا هاد المبلغ تاع الرتاج.",
    "ما نعرفش علاش حسبتولي هاد التسوية.",
    "علاش زدتوا الرتاج في الفاتورة تاعي؟",

    # Daridja Latin
    "3lach lazem nkhalas had rattrapage?",
    "mafhamtch 3lach facture ta3 rattrapage tal3a bzf",
    "3lach montant ta3 rattrapage tal3 bzf?",
    "3lach taswiya hadi kbira bzf?",
    "3lach zedtou had montant fel facture?",
    "3lach lazem nkhalas far9 kbir haka?",
    "mafhamtch menin ja had montant ta3 rattrapage",
    "ma3labalich 3lach 7sebtouli had taswiya",
    "3lach zedtou rattrapage fel facture ta3i?",

    # Mixed
    "علاش لازم nkhalas had rattrapage؟",
    "Je ne comprends pas علاش facture ta3 rattrapage طالعة بزاف.",
    "Pourquoi montant ta3 rattrapage طالع بزاف؟",
    "علاش la régularisation هادي كبيرة بزاف؟",
    "علاش زدتوا ce montant في facture؟",
    "Pourquoi لازم nkhalas فرق كبير هكا؟",
    "ما فهمتش d'où vient le montant ta3 rattrapage.",
    "Je ne sais pas علاش حسبتولي هاد taswiya.",
    "Pourquoi زدتوا le rattrapage في facture ta3i؟",
}

mask = (
    (df["Intent"] == "dispute_catch_up_bill")
    & df["Phrase"].isin(MOVE_TO_CATCH_UP)
)

print("Rows to move:", mask.sum())

df.loc[mask, "Intent"] = "catch_up_bill"

df.to_excel(FILE, index=False)

print("Cleanup completed.")