# Sonelgaz Customer Service Chatbot

# Scenario — Raccordement / Connection

## Objective

This scenario handles customer requests related to connecting a property or installation to the Sonelgaz electricity or gas network.

The chatbot identifies the customer's request and guides them toward:

* understanding the connection procedure;
* identifying the type of connection;
* asking about eligibility and conditions;
* preparing the required documents;
* submitting a connection request;
* understanding the technical study;
* understanding connection costs and payment;
* following the progress of a request;
* reporting problems with an existing connection request.

---

# 1. Demande de raccordement

## 1.1 General connection procedure

### Intent

`connection_procedure`

### Bot

> Pour demander un raccordement, vous devez déposer une demande auprès du service compétent.
>
> Le type de raccordement, les documents nécessaires et les conditions applicables dépendent de votre projet et de votre installation.
>
> Souhaitez-vous un raccordement à l'électricité ou au gaz ?

---

## 1.2 New connection

### Intent

`new_connection`

### Bot

> Si vous souhaitez raccorder un nouveau logement ou une nouvelle installation au réseau, vous devez déposer une demande de raccordement auprès du service compétent.
>
> Votre demande sera ensuite examinée selon les conditions applicables.

---

## 1.3 Connection for a new construction

### Intent

`new_construction_connection`

### Bot

> Si le raccordement concerne une nouvelle construction, préparez les documents relatifs au logement ou au projet et déposez une demande auprès du service compétent.

---

# 2. Type de raccordement

## 2.1 Electricity connection

### Intent

`electricity_connection`

### Bot

> Pour un raccordement électrique, vous devez déposer une demande auprès du service compétent.
>
> Les conditions techniques dépendent notamment des caractéristiques du logement et du réseau disponible.

---

## 2.2 Low-voltage connection

### Intent

`low_voltage_connection`

### Bot

> Si votre demande concerne un raccordement électrique en basse tension (BT), le service compétent déterminera les conditions techniques applicables à votre installation.

---

## 2.3 Gas connection

### Intent

`gas_connection`

### Bot

> Pour un raccordement au réseau de gaz, une demande doit être déposée auprès du service compétent.
>
> Les conditions techniques et les travaux nécessaires dépendent de la situation du logement et du réseau disponible.

---

## 2.4 Electricity and gas connection

### Intent

`electricity_gas_connection`

### Bot

> Si vous souhaitez raccorder votre logement à la fois à l'électricité et au gaz, vous devez préciser les deux besoins lors du dépôt de votre demande.

---

# 3. Documents nécessaires

## 3.1 Required documents

### Intent

`connection_documents`

### Bot

> Les documents nécessaires dépendent du type de raccordement et de la situation du demandeur.
>
> Le dossier peut notamment nécessiter des documents d'identification, des documents relatifs au logement ou à la propriété et les documents techniques demandés par le service compétent.
>
> Vérifiez la liste exacte auprès de l'agence ou du service chargé du raccordement.

---

## 3.2 Missing document

### Intent

`missing_connection_document`

### Bot

> Si un document demandé manque dans votre dossier, vous devez le fournir afin que votre demande puisse être traitée.
>
> Contactez le service compétent pour confirmer le document manquant.

---

## 3.3 Documents for new construction

### Intent

`connection_documents`

### Bot

> Pour une nouvelle construction, préparez les documents relatifs au projet et au logement ainsi que les documents administratifs et techniques demandés par le service compétent.

---

# 4. Conditions de raccordement

## 4.1 Eligibility

### Intent

`connection_eligibility`

### Bot

> L'acceptation d'une demande de raccordement dépend notamment de la situation du logement, de la disponibilité du réseau et des conditions techniques et administratives applicables.
>
> Le service compétent doit examiner votre demande pour confirmer sa recevabilité.

---

## 4.2 Network availability

### Intent

`network_availability`

### Bot

> La possibilité de raccorder un logement dépend notamment de la présence et de la capacité du réseau à proximité.
>
> Une vérification technique peut être nécessaire avant de confirmer le raccordement.

---

# 5. Étude technique

## 5.1 Technical study

### Intent

`technical_study`

### Bot

> Une étude technique peut être réalisée après le dépôt de la demande afin de déterminer les conditions nécessaires au raccordement.
>
> Les travaux et caractéristiques techniques dépendent de la situation du projet et du réseau disponible.

---

## 5.2 Connection works

### Intent

`connection_works`

### Bot

> Les travaux nécessaires au raccordement dépendent des résultats de l'étude technique.
>
> Le service compétent peut vous informer des travaux à réaliser et des conditions applicables à votre dossier.

---

# 6. Coût et paiement

## 6.1 Connection cost

### Intent

`connection_cost`

### Bot

> Le coût d'un raccordement dépend notamment des caractéristiques du projet et des travaux nécessaires.
>
> Le montant applicable doit être établi dans le cadre de votre dossier de raccordement.

---

## 6.2 Payment of connection costs

### Intent

`connection_payment`

### Bot

> Une fois les conditions et le montant du raccordement établis, le paiement doit être effectué selon les modalités communiquées par le service compétent.

---

## 6.3 Cost question or dispute

### Intent

`connection_cost_dispute`

### Bot

> Si vous souhaitez obtenir des explications concernant le montant demandé pour votre raccordement, contactez le service compétent afin de demander les informations relatives à son établissement.

---

# 7. Suivi de la demande

## 7.1 Application status

### Intent

`connection_status`

### Bot

> Si vous avez déjà déposé une demande de raccordement, vous pouvez contacter le service compétent pour connaître l'état d'avancement de votre dossier.
>
> Préparez votre référence de demande si vous en disposez.

---

## 7.2 Delayed connection

### Intent

`connection_delay`

### Bot

> Si votre demande de raccordement semble prendre plus de temps que prévu, contactez le service compétent avec la référence de votre dossier afin de vérifier son état d'avancement.

---

## 7.3 Connection request rejected

### Intent

`connection_rejection`

### Bot

> Si votre demande de raccordement a été refusée, demandez au service compétent les motifs du refus et les éventuelles conditions à remplir pour présenter une nouvelle demande.

---

# 8. Problème avec le raccordement

## 8.1 Connection not completed

### Intent

`connection_not_completed`

### Bot

> Si les travaux de raccordement n'ont pas été terminés, contactez le service compétent avec votre référence de dossier afin de vérifier l'état des travaux.

---

## 8.2 Problem after connection

### Intent

`connection_problem`

### Bot

> Si vous rencontrez un problème après la réalisation du raccordement, précisez la nature du problème afin de déterminer s'il s'agit d'un problème de raccordement ou d'une panne.

### → If it is a breakdown

`report_breakdown`

---

# Escalation

When the chatbot cannot determine the applicable connection procedure:

> Pour obtenir des informations précises sur votre demande de raccordement, veuillez contacter le service compétent ou vous rapprocher de votre agence commerciale avec les documents relatifs à votre projet.

The chatbot should not confirm eligibility, connection cost, technical feasibility, or completion date without verified information from official Sonelgaz information.
