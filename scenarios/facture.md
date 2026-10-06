# Sonelgaz Customer Service Chatbot

# Scenario — Facture / Bill

## Objective

This scenario handles customer requests related to Sonelgaz electricity and gas bills.

The chatbot identifies the customer's request and guides them toward:

- understanding their bill;
- understanding their consumption and charges;
- disputing a bill;
- paying a bill;
- resolving unpaid bills or disconnection;
- reporting a missing bill;
- updating customer information.

---

# 1. Understand My Bill

## 1.1 General bill explanation

### Intent

`understand_bill`

### Bot

> Bien sûr. Je peux vous aider à comprendre votre facture, notamment la consommation, les index, les charges, les taxes et le montant à payer.
>
> Que souhaitez-vous comprendre ?
>
> 1. Ma consommation
> 2. Le montant à payer
> 3. Les index
> 4. R / E / M
> 5. Une facture de rattrapage

---

## 1.2 Consumption calculation

### Intent

`consumption_calculation`

### Bot

> La consommation est calculée à partir des relevés du compteur, notamment l'ancien index et le nouvel index.
>
> Souhaitez-vous comprendre les index indiqués sur votre facture ?

---

## 1.3 Amount breakdown

### Intent

`amount_breakdown`

### Bot

> Le montant à payer peut comprendre la consommation ainsi que différents frais, taxes et éventuels montants restant dus.
>
> Si vous pensez que le montant est incorrect, vous pouvez choisir « Contester ma facture ».

---

## 1.4 R / E / M

### Intent

`rem_r_meaning`

### Bot

> Les lettres R, E et M correspondent au type de relevé indiqué sur la facture.
>
> Si vous contestez le relevé indiqué, vous pouvez choisir « Contester mon relevé ».

---

## 1.5 Catch-up / recovery bill

### Intent

`catch_up_bill`

### Bot

> Une facture de rattrapage ou de régularisation peut correspondre à une régularisation de la consommation facturée.
>
> Si vous n'êtes pas d'accord avec cette facture, vous pouvez faire une réclamation.

### → If customer disagrees

`dispute_catch_up_bill`

---

# 2. Dispute My Bill

## 2.1 General dispute

### Intent

`dispute_bill`

### Bot

> Je peux vous aider à identifier le problème avec votre facture.
>
> Quel est le problème ?
>
> 1. Montant trop élevé
> 2. Index incorrect
> 3. Relevé estimé contesté
> 4. Facture de rattrapage
> 5. J'ai déjà payé mais la facture apparaît impayée

---

## 2.2 Amount too high

### Intent

`high_or_abnormal_amount`

### Bot

> Si le montant de votre facture vous semble anormal par rapport à votre consommation habituelle, vous pouvez vérifier les index et les informations indiquées sur la facture.
>
> Si le problème persiste, vous pouvez déposer une réclamation auprès de votre agence commerciale.

---

## 2.3 Wrong meter reading

### Intent

`wrong_meter_reading`

### Bot

> Si l'index indiqué sur votre facture ne correspond pas à votre compteur, vous pouvez signaler cette erreur auprès de votre agence commerciale.

---

## 2.4 Estimated reading disputed

### Intent

`dispute_estimated_reading`

### Bot

> Votre facture indique un relevé estimé. Si vous contestez cette estimation, vous pouvez signaler le problème auprès de votre agence commerciale.

---

## 2.5 Catch-up bill disputed

### Intent

`dispute_catch_up_bill`

### Bot

> Si vous contestez le montant d'une facture de rattrapage ou de régularisation, vous pouvez déposer une réclamation auprès de votre agence commerciale.

---

## 2.6 Paid but still shown as unpaid

### Intent

`paid_but_unpaid_status`

### Bot

> Si vous avez déjà payé votre facture mais qu'elle apparaît toujours comme impayée, vérifiez votre justificatif de paiement et contactez le service commercial afin de faire vérifier votre situation.

---

# 3. Pay My Bill

## 3.1 Payment methods

### Intent

`bill_payment_methods`

### Bot

> Plusieurs moyens de paiement sont disponibles, notamment auprès des agences commerciales et des bureaux de poste. Des moyens de paiement à distance sont également disponibles.

---

## 3.2 Payment deadline

### Intent

`bill_payment_deadline`

### Bot

> La date limite de paiement est indiquée sur votre facture. Vérifiez votre facture pour connaître l'échéance applicable.

---

## 3.3 Online payment

### Intent

`online_bill_payment`

### Bot

> Vous pouvez utiliser les moyens de paiement à distance proposés par Sonelgaz.

---

## 3.4 Payment problem

### Intent

`payment_problem`

### Bot

> Si votre paiement n'a pas abouti, vérifiez les informations saisies et le moyen de paiement utilisé. Si le problème persiste, contactez le service concerné.

---

# 4. Unpaid Bill / Disconnection

## 4.1 Unpaid bill

### Intent

`unpaid_bill`

### Bot

> Si vous avez une facture impayée, vous pouvez procéder à son règlement avec l'un des moyens de paiement disponibles.

---

## 4.2 Disconnection

### Intent

`disconnection`

### Bot

> Vous n'avez plus d'électricité ?
>
> Vérifions d'abord s'il s'agit :
>
> 1. d'une panne générale ou locale ;
> 2. d'une coupure liée à une facture impayée.
>
> Si vous pensez qu'il s'agit d'une coupure pour impayé, vérifiez votre situation de paiement.

---

## 4.3 Restoration after payment

### Intent

`restoration_after_payment`

### Bot

> Si vous avez réglé vos factures impayées mais que le service n'est toujours pas rétabli, contactez le service compétent afin de signaler votre situation.

---

# 5. Other Bill Requests

## 5.1 Bill not received

### Intent

`bill_not_received`

### Bot

> Si vous n'avez pas reçu votre facture, vous pouvez vous présenter à votre agence commerciale avec une ancienne facture de consommation.

---

## 5.2 Update customer information

### Intent

`update_customer_information`

### Bot

> Pour modifier ou rectifier les informations figurant sur votre facture, vous devez adresser une demande à votre agence commerciale avec les justificatifs nécessaires.

---

# Escalation

When the chatbot cannot resolve the customer's request:

> Pour obtenir une assistance concernant votre situation, veuillez contacter le service compétent ou vous rapprocher de votre agence commerciale.

For a formal dispute, the chatbot should guide the customer toward the appropriate Sonelgaz commercial channel rather than attempting to make a decision about whether the bill is actually wrong.
