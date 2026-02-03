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
| F09 | Résolution du contact                           | Lien entre `messages.contact` et `contacts.id`                                      | Le champ `contact` du JSON affiche le nom du contact (string) et non son ID               |
| F10 | Présence de colonnes supplémentaires           | Présence de colonnes non spécifiées dans les CSV d'entrée                           | Le programme ignore les colonnes supplémentaires et traite les données normalement          |

### 2. Tests de robustesse

| ID  | Objectif                                                               | Entrée                                                     | Résultat Attendu                                                      |
| --- | ---------------------------------------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------- |
| R01 | Gestion de fichier manquant (messages)                                 | Chemin vers `messages.csv` inexistant                     | Sortie différente de 0                                                |
| R02 | Gestion de fichier manquant (contacts)                                 | Chemin vers `contacts.csv` inexistant                     | Sortie différente de 0                                                |
| R03 | Paramètre manquant à l'execution                                     | Absence de l'argument `/output`                           | Sortie différente de 0 + affichage de l'aide ?? *                    |
| R04 | Fichier `messages.csv` vide                                          | Fichier contenant uniquement le header                      | Sortie 0, aucun fichiers JSON créé dans `/output`                  |
| R05 | Résolution de contact inconnu                                         | ID contact dans `messages.csv` absent de `contacts.csv` | Sortie différente de 0 *                                              |
| R06 | Colonne manquante                                                      | Colonne `content` absente                                | Sortie différente de 0                                                |
| R07 | Colonne manquante                                                      | Colonne `datetime` absente                               | Sortie différente de 0                                                |
| R08 | Champ obligatoire manquant                                             | Champ `content` manquant                                  | Sortie différente de 0                                                |
| R09 | Champ obligatoire manquant                                             | Champ `id` manquant                                       | Sortie différente de 0                                                |
| R10 | Champ obligatoire manquant                                             | Champ `datetime` manquant                                 | Sortie différente de 0                                                |
| R11 | Champ obligatoire manquant                                             | Champ `contact` manquant                                  | Sortie différente de 0                                                |
| R12 | Encodage caractères spéciaux                                         | Champ `content` contient des caractères spéciaux        | Sortie à 0                                                            |
| R13 | Date avant 1970 (epoch)                                                | Timestamp négatif (-86400)                                 | Sortie à 0 + champ `datetime` dans JSON à "1969-12-31T00:00:00" * |
| R14 | Champ `direction` invalide (ni vide,ni originating, ni destinating) | `direction` = invalid_direction                           | Sortie différent de 0                                                 |
| R15 | Mauvais séparateur CSV                                                | `;` au lieu de `,`                                      | Sortie différente de 0                                                |
| R16 | Gestion des virgules dans message                                      | virgules dans `content` et séparateur "                  | Sortie à 0                                                            |
| R17 | Duplication d'ID                                                       | Deux messages différents avec le même `id`              | Sortie à 0 et 2 fichiers JSON créés ? *                             |
| R18 | Header manquant                                                        | Le Header (1ere ligne) est manquant                         | Sortie différente de 0 OU message d'erreur ?? *                       |
| R19 | UUID invalide                                                          | ID message ="12345" (pas au format UUID v4)                 | Sortie différente de 0                                                |
| R20 | Type de champ invalide                                                 | String au lieu de int dans le champ `contact`             | Sortie différente de 0 *                                              |
| R21 | Gestion grand message                                                  | Champ `content` ~= 1Mo                                   | Sortie à 0                                                            |

### 3. Tests de performance

## Résultats
