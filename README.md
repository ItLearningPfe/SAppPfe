📊 Optimisation du Recouvrement des Loyers – Data Analysis & Dashboard
📌 Contexte du projet

Ce projet a été réalisé dans le cadre d’un projet de fin d’études en collaboration avec Sergic, groupe immobilier français fondé en 1963 à Lille.

Les impayés de loyers représentent un risque financier majeur pour les sociétés de gestion immobilière. Une problématique spécifique concerne les locataires ayant quitté leur logement sans solder leurs dettes, ce qui complique fortement le processus de recouvrement.

L'objectif de ce projet est d'utiliser l'analyse de données afin de mieux comprendre les facteurs associés aux impayés et d'identifier des actions préventives pour limiter ces situations à l'avenir.

🎯 Enjeux métier

Réduire les pertes financières liées aux impayés

Optimiser le processus de recouvrement

Mettre en place des actions préventives

🎯 Objectifs du projet

La problématique principale est la suivante :

Comment l’analyse des données peut-elle aider le service de recouvrement à identifier les facteurs clés des impayés des locataires partis et à mettre en place des actions préventives ?

Les objectifs sont :

Identifier les KPI pertinents

Découvrir les corrélations entre variables et impayés

Identifier les facteurs de risque

Proposer des recommandations concrètes

Développer une application interactive d'analyse

🛠 Technologies utilisées
Python

Python a été choisi pour :

la richesse de son écosystème data

sa reconnaissance dans l'industrie

sa polyvalence pour l'analyse et la visualisation

Bibliothèques principales

pandas

numpy

scipy

matplotlib

seaborn

Streamlit

L’application interactive a été développée avec Streamlit afin de :

visualiser les indicateurs clés

explorer les données

analyser les corrélations

filtrer dynamiquement les résultats

📂 Jeu de données
Caractéristiques principales
Indicateur	Valeur
Nombre d'observations	39 000
Nombre de variables	129
Valeurs manquantes	23,1 %
Autres caractéristiques

aucune ligne dupliquée

présence d’une variable personnelle : NOM_CLIENT

absence de clé primaire

variables de types variés :

numériques

catégorielles

booléennes

textuelles

🔎 Méthodologie

Le projet suit plusieurs étapes d'analyse de données.

1️⃣ Data Profiling

Analyse exploratoire pour comprendre :

la structure du dataset

la qualité des données

les valeurs manquantes

les anomalies

2️⃣ Anonymisation des données

Afin de respecter le RGPD, les données personnelles ont été anonymisées.

Variables concernées :

noms

prénoms

Cette étape garantit la confidentialité des données tout en conservant leur valeur analytique.

3️⃣ Nettoyage des données

Plusieurs opérations ont été réalisées :

standardisation des données

gestion des valeurs manquantes

traitement des valeurs aberrantes

suppression des colonnes non pertinentes

renommage de certaines variables

Suppression des colonnes avec trop de valeurs nulles

Les variables contenant plus de 70 % de valeurs manquantes ont été supprimées :

Date de naissance

École

Date de perte d’immeuble

df = df.drop([
'NAISSANCE_ANNEE','NAISSANCE_MOIS','NAISSANCE_JOUR',
'PERTE_ANNEE','PERTE_MOIS','PERTE_JOUR',
'TAG_PERDU_ET_NON_CLOTURE'
], axis=1)
Gestion des valeurs manquantes

Certaines valeurs ont été remplacées :

Variable	Valeur de remplacement
Lieu de naissance	Inconnu
Civilité	NON RENSEIGNE
Gestion des valeurs aberrantes

Les valeurs extrêmes de la variable solde_client ont été conservées car elles correspondent à des impayés de clients professionnels.

4️⃣ Enrichissement des données

Plusieurs transformations ont été réalisées :

création d’une clé primaire

fusion des colonnes code_societe et code_client

jointure avec la table type de bail

réduction du nombre de catégories

Simplification de la civilité

38 catégories → 5 catégories

Mme

Mr

Couple

SOC

Non renseigné

Ajout de données géographiques

Ajout des variables :

latitude

longitude

à partir du code postal.

📊 Analyse descriptive

Objectif :

Décrire et comprendre la distribution des impayés avant toute modélisation.

Indicateurs statistiques
Indicateur	Valeur
Total des impayés	3 320 688,81 €
Moyenne	846,68 €
Médiane	173,49 €
Écart-type	2 446,83 €
% locataires partis	78,89 %
📉 Interprétation
Distribution asymétrique

moyenne élevée : 846 €

médiane faible : 173 €

Cela signifie que quelques cas extrêmes tirent la moyenne vers le haut.

Forte variabilité

L'écart-type élevé indique une grande hétérogénéité des situations d’impayés.

Locataires partis

Près de 80 % des impayés concernent des locataires ayant quitté leur logement, ce qui suggère des failles dans les procédures de sortie et de recouvrement.

🎯 Variable cible

La variable étudiée est :

Est_Impaye

Variable binaire :

Valeur	Signification
0	Pas d'impayé
1	Impayé

Cette variable permet d’identifier les facteurs associés au risque d’impayé.

📊 Analyse des corrélations
Méthodes statistiques utilisées
Variables qualitatives

Test du Chi²

V de Cramer

T de Tschuprow

Variables quantitatives

Test de normalité Shapiro-Wilk

Test Mann-Whitney

Ces tests permettent d’identifier les relations significatives entre variables et impayés.

🔎 Résultats principaux
Civilité

Association statistiquement significative.

Civilité	Taux d'impayés
Femme ou Homme	43,7 %
Société	40,7 %
Couple	26 %
Homme	21,5 %
Femme	18,6 %

V de Cramer : 0.255

Type de bail

Association significative mais faible.

Type de bail	Taux d'impayés
Régime fiscal inconnu	30 %
Logement conventionné	18 %
Meublé para-hôtelier	13 %

V de Cramer : 0.097

Ville

Association significative :

V de Cramer : 0.216

Villes les plus à risque :

Le Bourget

Asnières-sur-Seine

Bordeaux

Sevran

Paris

Châtillon

Marseille

Résidences

Certaines résidences présentent des taux particulièrement élevés :

Résidence	Taux d'impayés
TWENTY CAMPUS LE BOURGET	49,38 %
TWENTY CAMPUS ASNIERES	33,22 %
TC VILLENEUVE D'ASCQ OLYMPIUM	29,65 %
Durée d’occupation

Les locataires en impayé ont tendance à rester plus longtemps.

Situation	Durée médiane
Impayés	16 mois
Payeurs	11 mois

Différence statistiquement significative.

🖥 Application Streamlit

L’application interactive comprend plusieurs onglets.

📈 KPI

total des impayés

moyenne des impayés

filtre par année

filtre par résidence

graphique des impayés par mois

Observation :

👉 pics d'impayés en mai et septembre

📊 Corrélations

analyse statistique

top des modalités à risque

exploration des relations entre variables

📉 Graphiques

nuages de points

graphiques circulaires

graphiques à barres

cartes géographiques

📋 Profiling

statistiques descriptives

distribution des variables

détection des valeurs aberrantes

🚨 Constats majeurs
Distribution très asymétrique

Quelques impayés très élevés influencent fortement les indicateurs.

Locataires partis

78,89 % des impayés concernent des locataires ayant quitté leur logement.

Concentration géographique

Certaines villes et résidences concentrent une grande part des impayés.

Durée d’occupation

Les locataires en impayé ont une durée d’occupation plus longue.

💡 Recommandations

améliorer la qualité et la complétude des données

mettre en place une segmentation des locataires

adapter les politiques de recouvrement selon le type de bail

renforcer les garanties financières pour certains profils

surveiller particulièrement certaines zones géographiques

⚠ Limitations du projet
Données

Certaines variables contenaient plus de 80 % de valeurs manquantes, empêchant leur exploitation :

école fréquentée

situation professionnelle

âge des locataires

Technique

Limites liées à Streamlit :

moins de fonctionnalités que Power BI

graphiques parfois moins réactifs

développement plus complexe car basé sur du code
