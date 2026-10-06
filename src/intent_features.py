import re
import numpy as np


# ============================================================
# INTENT SIGNALS
# ============================================================

SIGNALS = {

    # --------------------------------------------------------
    # HOW TO PAY / PAYMENT METHODS
    # --------------------------------------------------------

    "how_to_pay": [

        # French / English
        r"\bcomment\b.*\b(payer|paie|paiement|régler|regler)\b",
        r"\bcomment\b.*\b(faire)\b.*\b(payer|régler|regler)\b",
        r"\bhow\b.*\b(pay|payment)\b",
        r"\bwhere\b.*\b(pay|payer)\b",
        r"\bou\b.*\bpayer\b",
        r"\boù\b.*\bpayer\b",

        # Darja / Arabizi
        r"\bkifach\b.*\b(nkhalas|nkhlas|n9der|payer|paye)\b",
        r"\bkifeh\b.*\b(nkhalas|nkhlas|n9der)\b",
        r"\bwin\b.*\b(nkhalas|nkhlas|payer|paye)\b",
        r"\bfin\b.*\b(nkhalas|nkhlas|payer|paye)\b",

        # Arabic
        r"كيفاش.*(نخلص|نقدر نخلص|ندير)",
        r"كيف.*(نخلص|نقدر نخلص)",
        r"وين.*(نخلص|نقدر نخلص)",
        r"فين.*(نخلص|نقدر نخلص)",

        # Payment-method questions
        r"\b(bwach|b[ae]ch)\b.*\b(nkhalas|nkhlas|payer)\b",
        r"\b(way|ways|means|method|methods)\b.*\b(pay|payment)\b",
        r"\b(moyens|méthodes|methodes|façons|facons)\b.*\b(paiement|payer)\b",

        # Arabic
        r"بواش.*(نخلص|الدفع)",
        r"وش.*(طرق|وسائل).*الدفع",
        r"واش.*(طرق|وسائل).*الدفع",
        r"بأي طريقة.*(نخلص|الدفع)",
    ],


    # --------------------------------------------------------
    # ONLINE / REMOTE PAYMENT
    # --------------------------------------------------------

    "online_payment": [

        # French / English
        r"\ben ligne\b",
        r"\bonline\b",
        r"\binternet\b",
        r"\bplateforme\b",
        r"\bsite\b",
        r"\bapplication\b",
        r"\bapp\b",
        r"\btéléphone\b",
        r"\btelephone\b",
        r"\bà distance\b",
        r"\ba distance\b",
        r"\bpar téléphone\b",
        r"\bpar internet\b",

        # Darja / Arabizi
        r"\bonline\b",
        r"\bplateforme\b",
        r"\bsite\b",
        r"\bapplication\b",
        r"\btéléphone\b",
        r"\btelephone\b",
        r"\binternet\b",

        # Arabic
        r"موقع",
        r"منصة",
        r"الهاتف",
        r"تلفون",
        r"التلفون",
        r"الإنترنت",
        r"انترنت",
        r"إلكتروني",
        r"عن بعد",
    ],


    # --------------------------------------------------------
    # PAYMENT PROBLEM
    # --------------------------------------------------------

    "payment_problem": [

        # Explicit problem words
        r"\bproblem\b",
        r"\bproblème\b",
        r"\bprobleme\b",
        r"\bmochkil\b",
        r"\bmochkel\b",

        # Arabic
        r"مشكل",
        r"مشكلة",
        r"مشاكل",

        # Failure / refusal / error
        r"\berreur\b",
        r"\berror\b",
        r"\bfailed\b",
        r"\bfail\b",
        r"\brefused\b",
        r"\brefuse\b",
        r"\brejected\b",
        r"\breject\b",
        r"\bblocked\b",
        r"\bblocage\b",
        r"\bbloqué\b",
        r"\bbloque\b",
        r"\béchoué\b",
        r"\bechoue\b",

        # French expressions
        r"paiement.*(échoué|echoue|refusé|refuse|bloqué|bloque)",
        r"paiement.*ne fonctionne pas",
        r"paiement.*ne marche pas",
        r"paiement.*impossible",
        r"transaction.*(refusée|refusee|échoue|echoue)",
        r"transaction.*ne passe pas",
        r"n.?arrive pas.*payer",
        r"ne peux pas.*payer",
        r"impossible.*payer",

        # Darja / Arabizi
        r"ما.*(قدرتش|نقدرش).*خلص",
        r"ما.*(مشاش|نجحش|تقبلش|تدوزش).*الدفع",
        r"ما.*(مشاش|نجحش|تقبلش|تدوزش).*الخلاص",

        r"الدفع.*(ما مشاش|ما نجحش|مبلوكي|مرفوض|ترفض)",
        r"الخلاص.*(ما مشاش|ما نجحش|مبلوكي|مرفوض|ترفض)",

        r"ما قدرتش.*(نخلص|نكمل).*الدفع",
        r"ما قدرتش.*(نخلص|نكمل).*paiement",
        r"ما نقدرش.*(نخلص|نكمل).*الدفع",

        r"عندي.*(مشكل|مشكلة).*الدفع",
        r"كاين.*(مشكل|مشكلة).*الدفع",
        r"عندي.*(مشكل|مشكلة).*الخلاص",
        r"كاين.*(مشكل|مشكلة).*الخلاص",

        r"\bmochkil\b.*\b(paiement|payment|khlas|khla[st]|nkhalas)\b",
        r"\bproblem\b.*\b(paiement|payment|khlas|nkhalas)\b",

        r"\bma\b.*\b(mchach|naj7ch|trefed|tdouzch)\b.*\b(paiement|payment|nkhalas)\b",

        # Payment doesn't work
        r"paiement.*marche pas",
        r"paiement.*marche[p ]?pas",
        r"payment.*doesn.?t work",
        r"payment.*not working",
    ],


    # --------------------------------------------------------
    # BILL NOT RECEIVED
    # --------------------------------------------------------

    "bill_not_received": [

        # French
        r"pas reçu.*facture",
        r"pas recue.*facture",
        r"n.?ai pas reçu.*facture",
        r"n.?ai pas recue.*facture",
        r"facture.*pas reçue",
        r"facture.*pas recue",
        r"facture.*n.?est pas arrivée",
        r"facture.*n.?est pas arrivee",

        # English
        r"not received.*bill",
        r"didn.?t receive.*bill",
        r"have not received.*bill",
        r"haven.?t received.*bill",
        r"bill.*not received",

        # Darja / Arabizi
        r"ma jatnich.*facture",
        r"ma wslatlich.*facture",
        r"ma waslatnich.*facture",
        r"ma wslatch.*facture",
        r"ma wasletlich.*facture",
        r"facture.*ma jatnich",
        r"facture.*ma wslatlich",
        r"facture.*ma waslatnich",
        r"facture.*ma wslatch",

        # I didn't find / see my bill
        r"ma l9itch.*facture",
        r"ma l9it.*facture",
        r"facture.*ma banetlich",
        r"ma banetlich.*facture",

        # Arabizi
        r"mal79tnich.*facture",
        r"mal9tnich.*facture",
        r"mal9itnich.*facture",

        # Arabic
        r"ما جاتنيش.*الفاتورة",
        r"ما وصلتش.*الفاتورة",
        r"ما وصلتنيش.*الفاتورة",
        r"ما لقيتش.*الفاتورة",
        r"الفاتورة.*ما جاتنيش",
        r"الفاتورة.*ما وصلتش",
        r"الفاتورة.*ما وصلتنيش",
        r"الفاتورة.*ما لقيتش",
        r"مازال.*(نستنى|نستنا).*الفاتورة",
        r"مازال.*الفاتورة.*ما.*(جات|وصلت)",

        # Still waiting for the bill
        r"mazal.*(n?stanna|n?tsenna).*facture",
        r"mazal.*facture.*ma.*(jat|wsl|wasl)",


        r"\bwin\b.*\bfacture\b",
        r"\bfacture\b.*\bwin\b",
        r"\blfatoura\b.*\b(ma jatnich|ma waslatnich|ma wslatch)\b",
        r"\b(ma jatnich|ma waslatnich|ma wslatch)\b.*\blfatoura\b",
        r"\b(facture|lfatoura)\b.*\b(ta3i|ta3|hada|had chhar)\b.*\b(ma jatnich|ma waslatnich|ma wslatch)\b",
        r"\blfatoura\b.*\bmajatnich\b",
        r"\bmajatnich\b.*\bfacture\b",
    ],


    # --------------------------------------------------------
    # UNPAID BILL
    # --------------------------------------------------------

    "unpaid_bill": [

        # French
        r"facture.*impayée",
        r"facture.*impayee",
        r"pas payé.*facture",
        r"pas paye.*facture",
        r"n.?ai pas.*payé.*facture",
        r"n.?ai pas.*paye.*facture",
        r"pas encore payé.*facture",
        r"pas encore paye.*facture",

        # English
        r"bill.*not paid",
        r"bill.*unpaid",
        r"not paid.*bill",
        r"haven.?t paid.*bill",
        r"didn.?t pay.*bill",

        # Darja / Arabizi
        r"ma khlastch.*facture",
        r"ma khlasthech.*facture",
        r"mazal.*ma.*khlastch.*facture",
        r"mazal.*ma.*khlasthech.*facture",

        r"mazal.*(khla|khlas|pay).*facture",
        r"mazal.*3liya.*facture",
        r"ba9i.*3liya.*facture",
        r"ba9i.*(nkhalas|nkhalles).*facture",

        # Arabic
        r"ما خلصتش.*الفاتورة",
        r"ما خلصتهاش.*الفاتورة",
        r"مازال.*ما خلصتش.*الفاتورة",
        r"مازال.*ما خلصتهاش.*الفاتورة",
        r"مازال.*عليا.*الفاتورة",
        r"باقي.*عليا.*الفاتورة",

        # Explicit unpaid status
        r"\bimpayée\b",
        r"\bimpayee\b",
        r"\bunpaid\b",
        r"\bnon.?payée\b",
        r"\bnon.?payee\b",
    ],


    # ========================================================
    # NEW: VOLTAGE PROBLEM
    # ========================================================

    "voltage_problem": [

        # French
        r"\bcourant\b.*\b(faible|faibl|bas)\b",
        r"\b(faible|faibl|bas)\b.*\bcourant\b",

        r"\btension\b.*\b(faible|basse)\b",
        r"\b(faible|basse)\b.*\btension\b",

        r"\bcourant\b.*\b(da3ef|da3if|daif)\b",
        r"\b(da3ef|da3if|daif)\b.*\bcourant\b",

        # Darja / Arabizi
        r"\bkahraba\b.*\b(da3fa|da3ef|da3if|daif|faible)\b",
        r"\b(da3fa|da3ef|da3if|daif)\b.*\b(kahraba|courant)\b",

        # Common short expressions
        r"\bcourant faible\b",
        r"\bcourant da3ef\b",
        r"\bcourant da3if\b",
        r"\bel courant da3ef\b",
        r"\bel courant da3if\b",

        # Arabic
        r"التيار.*(ضعيف|ضعيفة)",
        r"(ضعيف|ضعيفة).*التيار",
        r"الكهرباء.*(ضعيفة|ضعيف)",
        r"(ضعيفة|ضعيف).*الكهرباء",
        r"الضو.*(ضعيف|ضعيفة)",
    ],

        # ========================================================
    # WRONG METER READING
    # ========================================================

    "wrong_meter_reading": [

        # French
        r"\b(lecture|relevé|releve|index)\b.*\b(compteur)\b",
        r"\b(compteur)\b.*\b(lecture|relevé|releve|index)\b",
        r"\b(lecture|relevé|releve|index)\b.*\b(incorrect|incorrecte|faux|fausse|erreur|différent|different|mauvais)\b",
        r"\b(compteur)\b.*\b(erreur|faux|fausse|incorrect|incorrecte)\b",

        # Darja / Arabizi
        r"\b(lecture|relevé|releve|index)\b.*\b(compteur|lcompteur)\b",
        r"\b(compteur|lcompteur)\b.*\b(lecture|relevé|releve|index)\b",
        r"\b(compteur)\b.*\b(ghalta|galet|ghalet|khata2|machi s7i7|mokhtalef)\b",
        r"\b(ra9em)\b.*\b(compteur)\b.*\b(mokhtalef|ghalet|galet)\b",

        # Arabic
        r"(قراءة|القراءة|relevé|الـ?index).*(العداد|الكونتور).*(غلط|غالطة|خطأ|ماشي صحيحة|مختلف)",
        r"(العداد|الكونتور).*(قراءة|القراءة).*(غلط|غالطة|خطأ|ماشي صحيحة|مختلف)",
        r"(رقم).*(العداد|الكونتور).*(مختلف|غلط|خطأ)",
    ],


    # ========================================================
    # NEW: NEIGHBORHOOD OUTAGE
    # ========================================================

    "neighborhood_outage": [

        # Neighborhood / area indicators
        r"\bhouma\b",
        r"\bhoum(a|i)\b",
        r"\bquartier\b",
        r"\bquartiers\b",
        r"\bvoisins?\b",
        r"\bvoisinage\b",
        r"\brue\b",
        r"\bzone\b",
        r"\bquartier\b",

        # Arabic neighborhood indicators
        r"الحومة",
        r"الحي",
        r"المنطقة",
        r"الجيران",

        # Explicit outage + neighborhood combinations
        r"\b(ma|makan|makach|kaynach)\b.*\b(electricite|électricité|kahraba|kahraba)\b.*\b(houma|quartier)\b",
        r"\b(electricite|électricité|kahraba)\b.*\b(maqto3a|مقطوعة)\b.*\b(houma|quartier)\b",

        r"\b(houma|quartier)\b.*\b(maqto3a|ma kaynach|makanch|makan ch|pas d.?électricité|pas d.?electricite)\b",

        # Common Darja forms
        r"ma kaynach.*electricite.*houma",
        r"ma kaynach.*kahraba.*houma",
        r"makan electricte.*houma",
        r"makan electricite.*houma",
        r"toute la houma.*kahraba",
        r"toute la houma.*electricite",

        # French forms
        r"électricité.*coupée.*quartier",
        r"electricite.*coupee.*quartier",
        r"pas d.?électricité.*quartier",
        r"pas d.?electricite.*quartier",
        r"tout le quartier.*sans électricité",
        r"tout le quartier.*sans electricite",

        # Arabic
        r"الكهرباء.*مقطوعة.*الحي",
        r"الكهرباء.*مقطوعة.*الحومة",
        r"ماكانش.*الكهرباء.*الحي",
        r"ماكانش.*الكهرباء.*الحومة",
        r"ما كايناش.*الكهرباء.*الحي",
        r"ما كايناش.*الكهرباء.*الحومة",
    ],
}


# ============================================================
# FEATURE EXTRACTION
# ============================================================

def extract_intent_features(texts):
    """
    Create explicit intent features.

    Each matched intent signal receives a value of 3.0.
    Otherwise the feature receives 0.0.

    Feature order:
        1. how_to_pay
        2. online_payment
        3. payment_problem
        4. bill_not_received
        5. unpaid_bill
        6. voltage_problem
        7. neighborhood_outage
    """

    features = []

    for text in texts:

        text = str(text).lower().strip()

        row = []

        for patterns in SIGNALS.values():

            matched = any(
                re.search(
                    pattern,
                    text,
                    flags=re.IGNORECASE
                )
                for pattern in patterns
            )

            row.append(
                3.0 if matched else 0.0
            )

        features.append(row)

    return np.asarray(
        features,
        dtype=np.float32
    )