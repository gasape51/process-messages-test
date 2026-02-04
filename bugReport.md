# Rapport de Bugs

## Bugs Critiques

### BUG 1: Limitation à 10 fichiers de sortie maximum

- **Tests:** F11, P02-P06
- **Description:** Le binaire ne génère que 10 fichiers JSON maximum, quelle que soit la quantité de messages en entrée
- **Attendu:** Génération d'autant de fichiers que de messages valides
- **Obtenu:** Maximum 10 fichiers créés

## Bugs Majeurs

### BUG 2: Absence de validation des champs/colonnes obligatoires

- **Tests:** R06, R08, R09
- **Description:** Le programme accepte des `messages.csv` avec des champs/colonnes obligatoires vides ou absents
- **Exemples:**
  - Colonne `content` manquante en entrée génère un JSON avec l'erreur encodée en base64 dans `content` (R06)
  - Champ `content` vide en entrée génère `"content": ""` (R08)
  - Champ `id` vide en entrée génère un fichier `.json` (sans nom car id est vide) (R09)
- **Attendu:** sortie différente de 0 avec message d'erreur
- **Obtenu:** Sortie à 0 et génération de fichiers invalides

### BUG 3: Valeur par défaut non appliquée pour le champ direction

- **Tests:** F03
- **Description:** Lorsque le champ `direction` est vide, la valeur par défaut `"originating"` n'est pas appliquée
- **Attendu:** `"direction": "originating"`
- **Obtenu:** `"direction": ""`

### BUG 4: Format de date incorrect

- **Tests:** F07
- **Description:** La conversion du timestamp en entrée ne respecte pas l'isoformat demandé en sortie
- **Attendu:** `"2026-02-02T16:35:00"` (UTC)
- **Obtenu:** `"2026-02-02T18:35:00+01:00"` (heure locale + décalage)
- **Commentaire :** Le binaire semble appliquer le fuseau horaire local (UTC+1) puis ajoute manuellement un décalage de 1H ce qui fait un décalage de 2h

### BUG 5: Absence de validation du type de données

- **Tests:** R19, R20
- **Description:** Le programme ne valide pas les types de données d'entrée
- **Exemples:**
  - ID non UUID (ex: "12345") en entrée accepté et fichier `12345.json` créé (R19)
  - Contact de type string au lieu de int → accepté (R20)
- **Attendu:** Sortie à 1 et/ou message d'erreur
- **Obtenu:** Traitement normal avec les données invalides

### BUG 6: Absence de validation du champ direction

- **Test:** R14
- **Description:** Les valeurs invalides pour `direction` sont acceptées
- **Attendu:** Seules les valeurs `"originating"`, `"destinating"` ou vide (défaut) doivent être acceptées
- **Obtenu:** N'importe quelle valeur est acceptée et ajoutée dans le champ `direction` json

## Bugs Modérés

### BUG 7: Comportement non défini pour les ID dupliqués

- **Test:** R17
- **Description:** Lorsque deux messages ont le même ID, seul le dernier est conservé (écrasement du 1er JSON)
- **Attendu:** Erreur ou création de 2 fichiers distincts en suivant une règle qui ajoute un élément distinctif dans le nom du JSON
- **Obtenu:** Un seul fichier créé, pas d'erreur signalée et sortie à 0
- **Commentaire:** Le comportement attendu n'est pas clairement défini dans le sujet

### BUG 8: Gestion d'un CSV sans header

- **Test:** R18
- **Description:** Sans ligne d'en-tête, le programme réussit sans erreur silenciusement mais ne génère aucun fichier
- **Attendu:** Erreur explicite ou sortie à1
- **Obtenu:** Sortie à 0, aucun fichier créé, aucun message d'erreur

### BUG 9: Gestion des colonnes supplémentaires

- **Test:** F10
- **Description:** Présence de colonnes supplémentaires provoque une erreur
- **Erreur (extrait stderr) :** `ValueError: too many values to unpack (expected 2)`
- **Attendu:** Les colonnes supplémentaires doivent être ignorées (interprétation du sujet)
- **Obtenu:** sortie à 1 et message d'erreur

### BUG 10: Gestion de messages très long

- **Test:** R21
- **Description:** Les messages avec un contenu avec beaucoup caractères provoquent une erreur CSV
- **Erreur (extrait stderr):** `csv.Error: field larger than field limit (131072)`
- **Attendu:** Traitement normal ou message erreur explicite
- **Commentaire:** Ce cas n'est pas couvert par le sujet
