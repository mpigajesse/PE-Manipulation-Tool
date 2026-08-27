# PE BEAR - Guide Complet du Code

## Table des matières

1. [Architecture globale](#architecture-globale)
2. [Sections principales](#sections-principales)
3. [Flux d'exécution](#flux-dexécution)
4. [Composants clés](#composants-clés)
5. [Fonctionnalités détaillées](#fonctionnalités-détaillées)

---

## Architecture globale

### Structure générale

`
fichier_exe.py
├── Imports (pefile, os, sys, math, hashlib, ctypes, etc.)
├── Activation ANSI (Windows 10+)
├── Configuration globale (classe Config)
├── Classe principale (PEBear)
│   ├── Section 1: Chargement/Sauvegarde
│   ├── Section 2: Affichage/Formatage
│   ├── Section 3: Analyse PE
│   ├── Section 4: Menus interactifs
│   ├── Section 5: Édition spécifique
│   └── Section 6: Utilitaires
└── Point d'entrée (main())
`

### Paradigme

- **Orienté objet** - Classe PEBear encapsule toute la logique
- **Modulaire** - Sections bien séparées avec responsabilités claires
- **Commenté** - Chaque section et fonction documentée
- **Robuste** - Gestion d'erreurs complète

---

## Sections principales

### Section 1: Chargement et Sauvegarde

**Responsabilité:** Gérer les fichiers PE (lecture/écriture disque)

**Fonctions clés:**
- charger_fichier(chemin) - Charge un PE en mémoire
- sauvegarder(chemin) - Écrit les modifications sur disque

**Détails:**
- Valide l'existence du fichier
- Parse le format PE avec pefile.PE()
- Calcule le checksum correct
- Affiche un résumé des infos chargées

### Section 2: Affichage et Formatage

**Responsabilité:** Rendre les données lisibles

**Fonctions clés:**
- fficher_entete() - En-tête principal
- fficher_section(titre) - Titre de section
- fficher_tableau(entetes, lignes) - Tableau formaté
- fficher_succes/erreur/avertissement/info() - Messages colorés

**Détails:**
- Codes ANSI pour couleurs (vert, rouge, jaune, bleu, cyan)
- Tableaux avec alignement automatique des colonnes
- Messages standardisés avec tags

### Section 3: Analyse du PE

**Responsabilité:** Extraire et afficher les infos du PE

**Fonctions clés:**
- _afficher_en_tetes() - Headers (DOS, FILE, OPTIONAL)
- _afficher_sections() - Tableau des sections
- _afficher_imports() - DLL et fonctions importées
- _afficher_exports() - Symboles exportés
- _afficher_ressources() - Types de ressources
- _afficher_signature() - Statut signature numérique
- _afficher_overlay() - Données après le PE
- _afficher_tls() - TLS callbacks

**Détails:**
- Lecture directe des structures PE
- Calcul d'entropie Shannon
- Hashing SHA-256
- Détection d'archives dans overlay

### Section 4: Menus interactifs

**Responsabilité:** Navigation et interaction utilisateur

**Menus:**
- menu_principal() - Menu racine
- menu_sections() - Gestion sections
- menu_imports_exports() - Gestion imports/exports
- menu_edition() - Édition propriétés
- menu_injection() - Injection code
- menu_securite() - Protections

**Détails:**
- Format vertical pour lisibilité
- Boucles jusqu'à retour
- Gestion d'erreurs des saisies

### Section 5: Édition spécifique

**Responsabilité:** Modifier le PE

**Fonctions clés:**
- oir_section() - Détails d'une section
- modifier_droits_section() - Changer R/W/X
- modifier_point_entree() - Changer Entry Point
- modifier_image_base() - Changer ImageBase
- modifier_horodatage() - Changer timestamp
- injecter_code() - Injection binaire
- jouter/extraire_overlay() - Gestion overlay

**Détails:**
- Affichage des valeurs actuelles
- Confirmation avec couleurs
- Logging dans le journal des modifications

### Section 6: Utilitaires

**Responsabilité:** Fonctions d'aide

**Fonctions clés:**
- _human_size() - Conversion octets lisible
- _calculer_entropie() - Entropie Shannon
- _generer_shellcode() - Shellcode simple
- fficher_hex_dump() - Affichage hexadécimal

**Détails:**
- Conversion Ko/Mo/Go automatique
- Formule entropie Shannon complète
- Shellcode NOP (pas exécution réelle)

---

## Flux d'exécution

### Démarrage
1. **Activation ANSI** - Active couleurs sur Windows
2. **Création Config** - Initialise constantes
3. **Appel main()** - Point d'entrée

### Mode interactif
1. Affiche en-tête
2. Liste les fichiers PE du dossier
3. Demande un fichier (numéro, chemin, ou 'q')
4. Charge le fichier choisi
5. Ouvre le menu principal

### Menu principal
1. Affiche options (1-9)
2. Demande un choix
3. Exécute l'action correspondante
4. Revient au menu (boucle)

### Exemple: Analyser un fichier
\\\
main()
  → Demande chemin ou numéro
  → charger_fichier(chemin)
    → Valide fichier
    → Lit fichier en bytearray
    → Parse PE avec pefile
    → Affiche résumé
  → menu_principal()
    → Affiche options
    → Demande choix (1)
    → analyser_tout()
      → afficher_en_tetes()
      → afficher_sections()
      → afficher_imports()
      → ... (toutes les analyses)
    → Revient au menu
\\\

---

## Composants clés

### Classe Config

Centralise les constantes:
- CONSOLE_WIDTH - Largeur terminal (100 caractères)
- COLORS - Codes ANSI (rouge, vert, jaune, etc.)
- CHARS - Caractères ASCII (=, |, +, -, etc.)

**Usage:**
\\\python
couleur = Config.COLORS['green']
print(f"{couleur}Texte vert{Config.COLORS['reset']}")
\\\

### Classe PEBear

Encapsule toute la logique PE:
- self.chemin - Chemin du fichier chargé
- self.pe - Objet PE (pefile.PE)
- self.donnees_brutes - Contenu binaire
- self.modifications - Journal des modifications

**Cycle de vie:**
1. Création: pebear = PEBear()
2. Chargement: pebear.charger_fichier(chemin)
3. Navigation: pebear.menu_principal()
4. Sauvegarde: pebear.sauvegarder(chemin_sortie)

### Gestion des erreurs

**Niveaux:**
- Erreurs critiques - Arrête l'opération (rouge)
- Avertissements - Continue avec prudence (jaune)
- Info - Données secondaires (bleu)

**Approche:**
- Try/except sur toutes les opérations
- Messages d'erreur explicites
- Pas de crash silencieux

---

## Fonctionnalités détaillées

### 1. Analyse PE complète

**Étapes:**
1. Affiche DOS Header (e_magic, e_lfanew)
2. Affiche FILE Header (Machine, Sections, Timestamp)
3. Affiche OPTIONAL Header (Magic, EP, ImageBase)
4. Affiche les droits de protection (ASLR, DEP, CFG)
5. Liste les sections avec entropie et SHA-256
6. Affiche les imports/exports
7. Détecte ressources
8. Vérifie signature numérique
9. Analyse overlay
10. Détecte TLS callbacks

**Données affichées:**
- Toutes les adresses en hexadécimal
- Tailles en format lisible (B, KB, MB)
- Entropie de chaque section (0-8)
- Hashes SHA-256
- Horodatage converti en date lisible

### 2. Édition de propriétés

**Modification du point d'entrée:**
1. Affiche l'adresse actuelle
2. Demande la nouvelle RVA
3. Valide le format hexadécimal
4. Modifie OPTIONAL_HEADER.AddressOfEntryPoint
5. Enregistre dans le journal

**Modification ImageBase:**
1. Affiche l'adresse actuelle
2. Demande la nouvelle adresse
3. Modifie OPTIONAL_HEADER.ImageBase
4. Enregistre dans le journal

**Modification horodatage:**
1. Affiche la date actuelle
2. Demande nouvelle date (YYYY-MM-DD HH:MM:SS ou 'now')
3. Convertit en timestamp Unix
4. Modifie FILE_HEADER.TimeDateStamp
5. Enregistre dans le journal

### 3. Injection de code

**Processus:**
1. Demande source (fichier ou shellcode)
2. Charge les données
3. Demande section cible
4. Demande offset dans la section
5. Écrit les données dans le bytearray
6. Enregistre dans le journal

**Shellcode généré:**
- 32 instructions NOP (0x90)
- Placeholder pour démonstration
- Pas d'exécution réelle

### 4. Gestion des protections

**ASLR (0x0040):**
- Randomise l'adresse de base
- À désactiver pour testing
- À garder en production

**DEP (0x0100):**
- Prévient l'exécution depuis la pile
- Protection essentielle
- À toujours activer

**CFG (0x4000):**
- Control Flow Guard
- Protection advanced
- Support Windows 10+

**Affichage:**
- État actuel en couleur (vert=actif, rouge=inactif)
- Menu pour activer/désactiver
- Enregistrement dans le journal

---

## Questions importantes

### Q1: Pourquoi pefile?
**R:** pefile est le parser PE pur Python le plus complet, sans dépendances externes.

### Q2: Comment fonctionne l'entropie?
**R:** Entropie Shannon mesure l'aléatoire (0=texte, 8=données compressées/chiffrées).

### Q3: Peut-on patcher sans malware?
**R:** Oui - éditer le EP, ImageBase, etc. sert au reverse engineering légitime.

### Q4: Comment protéger le code injected?
**R:** Utiliser les droits des sections (R/W/X) et les protections du PE.

### Q5: L'overlay peut-il contenir du malware?
**R:** Oui - c'est une zone non-mappée souvent exploitée par les malwares.

---

## Points de sécurité

1. **Validation** - Tous les chemins sont validés
2. **Erreurs** - Gestion complète sans crashes
3. **Permissions** - Vérification des droits d'accès
4. **Intégrité** - Checksum recalculé après modification
5. **Audit** - Journal complet des modifications

---

## Performance

- **Fichiers < 100 MB** - Chargement en mémoire OK
- **Analyse complète** - Quelques secondes
- **Affichage** - O(n) où n = nombre de sections/imports
- **Cache** - Section cache pour optimisation future

---

**Version:** 2.0.0  
**Date:** 27 Août 2026  
**Status:** Production ✅
