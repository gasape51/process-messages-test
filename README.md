# process-messages-test

# Objectif

Évaluation du composant logiciel `process_messages` via des tests automatisés.

## Prérequis

- Python 3.10+
- Linux (pour l'exécutable)

## Installation

```bash
pip install -r requirements.txt
```

## Lancer les tests

```bash

```

## Stratégie de test

### 1. Tests fonctionnels

| ID  | Objectif                                         | Entrée                                                                                 | Résultat Attendu                                                                             |
| --- | ------------------------------------------------ | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| F01 | Exécution nominale                              | Fichiers `messages.csv` et `contacts.csv` valides (exemples fournis dans le sujet) | Sortie `0`, Création de fichiers JSON dans `/output`                                    |
| F02 | Unicité des fichiers                            | `messages.csv` avec 2 messages distincts valides                                     | Création de 2 fichiers JSON distincts dans /`output`                                       |
| F03 | Gestion de la valeur par défaut (`direction`) | Champ direction vide                                                                    | Le champ `direction` dans le JSON doit être `"originating"` par défaut                  |
| F04 | Convention de nommage des fichiers               | Message avec un `id` spécifique                                                      | Le fichier doit être nommé `<id_du_message>.json`                                         |
| F05 | Intégrité de la structure JSON                 | Exécution "standard"                                                                   | Le JSON contient  les clés :` id`, `datetime`, `direction`, `content`, `contact` |
| F06 | Exactitude de l'identifiant                      | Message avec un UUID v4 spécifique                                                     | Le champ `id` du JSON correspond à l'UUID du CSV                                          |
| F07 | Conversion du format de date                     | Timestamp UNIX                                                                          | Date convertie en isoformat `YYYY-MM-DDThh:mm:ss`                                          |
| F08 | Encodage du contenu                              | Champ `content` en texte clair                                                        | Le contenu du message est encodé en base64 dans le JSON                                     |
| F09 | Résolution du contact                           | Lien entre `messages.contact` et `contacts.id`                                      | Le champ `contact` du JSON affiche le *nom* du contact (string) et non son ID             |
| F10 | Présence de colonnes supplémentaires           | Présence de colonnes non spécifiées dans les CSV d'entrée                           | Le programme ignore les colonnes supplémentaires et traite les données normalement          |

### 2. Tests de robustesse

| ID  | Objectif                               | Entrée                                                     | Résultat Attendu                                     |
| --- | -------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------------- |
| R01 | Gestion de fichier manquant (messages) | Chemin vers `messages.csv` inexistant                     | Sortie différente de 0                               |
| R02 | Gestion de fichier manquant (contacts) | Chemin vers `contacts.csv` inexistant                     | Sortie différente de 0                               |
| R03 | Paramètre manquant à l'execution     | Absence de l'argument `/output`                           | Sortie                                                |
| R04 | Fichier `messages.csv` vide          | Fichier contenant uniquement le header                      | Sortie 0, aucun fichiers JSON créé dans `/output` |
| R05 | Résolution de contact inconnu         | ID contact dans `messages.csv` absent de `contacts.csv` | Sortie différente de 0                               |

### 3. Tests de performance

## Résultats
