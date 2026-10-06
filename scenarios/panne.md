# Sonelgaz Customer Service Chatbot

# Scenario — Panne / Dépannage

## Objective

This scenario handles customer requests related to electricity and gas breakdowns.

The chatbot identifies the customer's problem and guides them toward:

- reporting an electricity outage;
- reporting a gas outage;
- reporting a meter problem;
- reporting voltage problems;
- reporting damage to electrical appliances;
- checking interruption and restoration information;
- reporting dangerous situations.

---

# 1. Panne d'électricité

## 1.1 Je n'ai plus d'électricité

### Intent

`electricity_outage`

### Bot

> Je comprends. Vous n'avez plus d'électricité à votre domicile.
>
> Vérifiez d'abord si la coupure concerne uniquement votre logement ou également les logements voisins.
>
> Si la coupure concerne uniquement votre domicile, vous pouvez signaler la panne afin qu'elle soit prise en charge.

### → If other homes are also affected

`neighborhood_outage`

---

## 1.2 Coupure uniquement chez moi

### Intent

`electricity_outage`

### Bot

> Si vos voisins ont toujours de l'électricité et que la coupure concerne uniquement votre logement, il peut s'agir d'un problème local.
>
> Vous pouvez signaler la panne en précisant votre adresse et les circonstances du problème.

---

## 1.3 Coupure dans tout le quartier

### Intent

`neighborhood_outage`

### Bot

> Si plusieurs logements de votre quartier sont privés d'électricité, il peut s'agir d'une panne affectant le réseau local.
>
> Vous pouvez signaler la panne en précisant la zone concernée.

---

## 1.4 Coupure générale

### Intent

`neighborhood_outage`

### Bot

> Si la coupure concerne plusieurs rues ou une zone importante, il peut s'agir d'une panne générale du réseau.
>
> Veuillez signaler la panne en indiquant votre localisation afin de faciliter son identification.

---

## 1.5 Coupure intermittente

### Intent

`electricity_outage`

### Bot

> Si l'électricité se coupe et revient régulièrement, vous pouvez signaler cette perturbation afin qu'elle soit vérifiée.

---

## 1.6 Électricité faible / problème de tension

### Intent

`voltage_problem`

### Bot

> Si votre alimentation électrique est anormalement faible, il peut s'agir d'un problème de tension.
>
> Vous pouvez signaler la perturbation afin qu'elle soit vérifiée.

---

# 2. Panne de gaz

## 2.1 Je n'ai plus de gaz

### Intent

`gas_outage`

### Bot

> Vous n'avez plus d'alimentation en gaz à votre domicile.
>
> Vérifiez si le problème concerne uniquement votre logement ou également les logements voisins.
>
> Vous pouvez ensuite signaler la panne.

---

## 2.2 Coupure de gaz dans mon logement

### Intent

`gas_outage`

### Bot

> Si la coupure de gaz concerne uniquement votre logement, signalez le problème en précisant votre adresse et les circonstances de la coupure.

---

## 2.3 Coupure de gaz dans le quartier

### Intent

`gas_outage`

### Bot

> Si plusieurs logements de votre quartier sont concernés par la coupure de gaz, précisez la zone concernée lors du signalement.

---

## 2.4 Pression de gaz faible

### Intent

`gas_outage`

### Bot

> Si vous constatez une pression de gaz anormalement faible, signalez le problème afin qu'il puisse être vérifié.

---

## 2.5 Problème d'alimentation en gaz

### Intent

`gas_outage`

### Bot

> Si votre alimentation en gaz est interrompue ou insuffisante, vous pouvez signaler le problème en précisant votre adresse et les circonstances.

---

# 3. Problème de compteur

## 3.1 Mon compteur fonctionne mal

### Intent

`meter_problem`

### Bot

> Si votre compteur fonctionne anormalement, vous pouvez signaler le problème afin qu'il soit vérifié.

---

## 3.2 Le compteur affiche une erreur

### Intent

`meter_problem`

### Bot

> Si votre compteur affiche un message ou un code d'erreur, indiquez le message affiché lors du signalement.

---

## 3.3 Le compteur est bloqué

### Intent

`meter_problem`

### Bot

> Si votre compteur est bloqué ou ne fonctionne plus correctement, vous pouvez demander une vérification du compteur.

---

## 3.4 Je pense que mon compteur est défectueux

### Intent

`meter_problem`

### Bot

> Si vous pensez que votre compteur est défectueux, signalez le problème afin qu'il puisse être contrôlé par le service compétent.

---

## 3.5 Comment faire vérifier/remplacer le compteur ?

### Intent

`meter_problem`

### Bot

> Si vous souhaitez faire vérifier ou remplacer un compteur qui semble défectueux, vous devez signaler le problème afin qu'il soit examiné par le service compétent.

---

# 4. Problème de tension électrique

## 4.1 Surtension

### Intent

`voltage_problem`

### Bot

> Si vous constatez une surtension ou une variation anormale de la tension électrique, signalez rapidement le problème.
>
> Si vos appareils sont exposés à un danger, évitez toute manipulation présentant un risque.

---

## 4.2 Baisse de tension

### Intent

`voltage_problem`

### Bot

> Si vous constatez une baisse de tension ou une alimentation électrique anormalement faible, vous pouvez signaler le problème afin qu'il soit vérifié.

---

## 4.3 Courant instable

### Intent

`voltage_problem`

### Bot

> Si votre alimentation électrique est instable ou si la tension varie régulièrement, signalez cette perturbation afin qu'elle puisse être vérifiée.

---

## 4.4 Appareils électriques endommagés

### Intent

`damaged_appliance`

### Bot

> Si un appareil électrique a été endommagé à la suite d'une perturbation électrique, vous pouvez signaler le dommage.
>
> Conservez les documents et justificatifs relatifs à l'appareil et au dommage.

---

# 5. Appareil électrique endommagé

## 5.1 Mon appareil a été endommagé après une perturbation

### Intent

`damaged_appliance`

### Bot

> Si votre appareil a été endommagé après une perturbation électrique, vous pouvez déclarer le dommage auprès du service compétent.

---

## 5.2 Comment déclarer le sinistre ?

### Intent

`damaged_appliance`

### Bot

> Pour déclarer un dommage, indiquez les circonstances de l'incident et fournissez les documents ou justificatifs demandés.

---

## 5.3 Quels documents fournir ?

### Intent

`damaged_appliance`

### Bot

> Les documents nécessaires peuvent dépendre de la nature du sinistre.
>
> Préparez notamment les informations concernant l'appareil, le dommage constaté et les circonstances de l'incident.

---

## 5.4 Puis-je être indemnisé ?

### Intent

`damaged_appliance`

### Bot

> Si vous souhaitez demander une indemnisation à la suite d'un dommage électrique, votre demande doit être examinée par le service compétent.
>
> Le chatbot ne peut pas déterminer si une indemnisation est applicable à votre situation.

---

# 6. Coupure / Rétablissement

## 6.1 Pourquoi y a-t-il une coupure ?

### Intent

`report_breakdown`

### Bot

> Une coupure peut avoir différentes causes.
>
> Le chatbot ne peut pas déterminer à distance la cause technique exacte de la panne.
>
> Vous pouvez signaler la panne afin qu'elle soit vérifiée.

---

## 6.2 Quand l'électricité sera-t-elle rétablie ?

### Intent

`restoration`

### Bot

> Le délai de rétablissement dépend de la nature et de l'étendue de la panne.
>
> Le chatbot ne peut pas confirmer une heure de rétablissement sans information actualisée sur l'incident.

---

## 6.3 L'électricité n'a toujours pas été rétablie

### Intent

`restoration`

### Bot

> Si l'électricité n'a toujours pas été rétablie après le signalement d'une panne, signalez que le problème persiste.
>
> Indiquez votre localisation et, si disponible, la référence du signalement.

---

## 6.4 Comment signaler une panne ?

### Intent

`report_breakdown`

### Bot

> Je peux vous aider à identifier le type de panne à signaler.
>
> Veuillez préciser :
>
> 1. Panne d'électricité
> 2. Panne de gaz
> 3. Problème de compteur
> 4. Problème de tension
> 5. Appareil électrique endommagé
> 6. Situation dangereuse

---

# 7. Urgence / Danger

## 7.1 Câble électrique tombé

### Intent

`electrical_danger`

### Bot

> Un câble électrique tombé représente un danger.
>
> Ne touchez pas au câble et éloignez-vous de la zone.
>
> Signalez immédiatement la situation au service d'urgence compétent.

---

## 7.2 Poteau électrique endommagé

### Intent

`electrical_danger`

### Bot

> Un poteau électrique endommagé peut présenter un danger.
>
> Ne vous approchez pas de l'installation et signalez immédiatement la situation au service compétent.

---

## 7.3 Étincelles / danger électrique

### Intent

`electrical_danger`

### Bot

> Des étincelles ou une situation électrique dangereuse nécessitent une attention immédiate.
>
> Éloignez-vous de la zone et évitez de toucher l'installation.
>
> Contactez le service d'urgence compétent.

---

## 7.4 Odeur de gaz

### Intent

`gas_emergency`

### Bot

> Une odeur de gaz peut indiquer une situation dangereuse.
>
> Évitez toute flamme ou étincelle et éloignez-vous de la zone concernée.
>
> Contactez immédiatement le service d'urgence compétent.

---

## 7.5 Fuite de gaz

### Intent

`gas_emergency`

### Bot

> Une fuite de gaz constitue une situation d'urgence.
>
> Éloignez-vous de la zone dangereuse et contactez immédiatement le service d'urgence compétent.
>
> Ne tentez pas de réparer vous-même l'installation.

---

## 7.6 Situation dangereuse

### Intent

`electrical_danger`

### Bot

> Si vous constatez une situation présentant un danger électrique, éloignez-vous de la zone et évitez de toucher l'installation.
>
> Signalez immédiatement la situation au service compétent.

---

# Escalation

When the chatbot cannot resolve the customer's request:

> Pour signaler une panne ou obtenir une assistance concernant votre situation, veuillez contacter le service compétent ou vous rapprocher de votre agence commerciale.

For dangerous situations such as gas leaks, gas smell, fallen electrical cables or exposed electrical installations, the chatbot should prioritize safety instructions and direct the customer toward the appropriate emergency service.

The chatbot should not attempt to diagnose the technical cause of a breakdown or guarantee a restoration time.
