# PE BEAR - FAQ Complète pour Révision

## 📖 Questions & Réponses Détaillées

### SECTION 1: MENU PRINCIPAL & NAVIGATION

---

## Q1: Qu'est-ce que le Menu Principal de PE BEAR?

**R:** Le menu principal est le hub de navigation central. Après charger un fichier PE, il affiche 7 options principales:

\\\
┌─────────────────────────────────────┐
│   MENU PRINCIPAL - PE BEAR v2.0     │
├─────────────────────────────────────┤
│ 1) Analyser tout                    │
│ 2) Gestion sections                 │
│ 3) Gestion Imports/Exports          │
│ 4) Édition propriétés               │
│ 5) Injection code                   │
│ 6) Sécurité & Protections           │
│ 7) Utilitaires                      │
│ 0) Quitter                          │
│                                     │
│ > Votre choix: _                    │
└─────────────────────────────────────┘
\\\

**Structure:**
- Option 1: Analyse globale rapide
- Options 2-6: Sous-menus spécialisés
- Option 0: Quitter l'application

---

## Q2: Que fait "1) Analyser tout"?

**R:** Lance une analyse complète et affiche TOUS les détails du PE:

**Étapes exécutées:**
1. Affiche DOS Header (signature, offsets)
2. Affiche FILE Header (architecture, sections, timestamp)
3. Affiche OPTIONAL Header (entry point, ImageBase, protections)
4. Affiche le tableau des sections
5. Affiche les imports (DLL + fonctions)
6. Affiche les exports (symboles exportés)
7. Affiche les ressources
8. Affiche la signature numérique
9. Affiche l'overlay (données additionnelles)
10. Affiche les TLS callbacks

**Output typique:** 10-50 KB de texte formaté (dépend du PE)

**Temps d'exécution:** 1-5 secondes (fichiers < 100 MB)

---

## Q3: Que contient le sous-menu "2) Gestion sections"?

**R:** Options pour manipuler les sections du PE:

\\\
SOUS-MENU: GESTION SECTIONS
├─ 1) Voir toutes les sections
│  └─ Affiche tableau avec nom, taille, droits, entropie
│
├─ 2) Voir détails section spécifique
│  └─ Demande numéro section
│  └─ Affiche toutes infos (addr, size, flags, entropy, hash)
│
├─ 3) Modifier droits (R/W/X)
│  └─ Demande section + nouveaux droits
│  └─ Modifie section header
│
├─ 4) Voir overlay
│  └─ Affiche données après le PE
│  └─ Calcule SHA-256
│
└─ 0) Retour au menu principal
\\\

**Cas d'usage:**
- Vérifier droits sections (sécurité)
- Analyser entropie (détecter chiffrement)
- Modifier permissions (testing)

---

## Q4: Qu'affiche "3) Gestion Imports/Exports"?

**R:** Deux opérations séparées:

**Imports (ce que CE programme utilise):**

\\\
Entrée: 1) Afficher imports

Affichage:
┌─────────────────────────────────┐
│ DLL: KERNEL32.dll (15 imports)  │
├─────────────────────────────────┤
│ • CreateFileA                   │
│ • ReadFile                      │
│ • CloseHandle                   │
│ ... (12 autres)                 │
└─────────────────────────────────┘
\\\

**Exports (ce que CE programme offre):**

\\\
Entrée: 2) Afficher exports

Affichage:
┌─────────────────────────────────┐
│ Exports trouvés: 8              │
├─────────────────────────────────┤
│ • GetConfig (RVA: 0x1234)       │
│ • SetOption (RVA: 0x2345)       │
│ • DoWork (RVA: 0x3456)          │
│ ... (5 autres)                  │
└─────────────────────────────────┘
\\\

**Utilité:**
- Imports = détecte malware signatures
- Exports = comprend API publiques

---

## Q5: Qu'affiche "4) Édition propriétés"?

**R:** Menu pour modifier des propriétés du PE:

\\\
SOUS-MENU: ÉDITION PROPRIÉTÉS
├─ 1) Modifier Entry Point (EP)
│  └─ Change AddressOfEntryPoint
│  └─ ⚠️ Application peut crash si adresse invalide
│
├─ 2) Modifier ImageBase
│  └─ Change adresse de base du PE
│  └─ Affecte toutes adresses absolues
│
├─ 3) Modifier horodatage (timestamp)
│  └─ Change FILE_HEADER.TimeDateStamp
│  └─ Affiche comme date lisible dans Propriétés
│
├─ 4) Modifier Section Name
│  └─ Change nom section (.text → .code)
│  └─ Cosmétique surtout
│
└─ 0) Retour
\\\

**Cas d'usage:**
- EP: Redirect code vers injection
- ImageBase: Corriger ASLR conflicts
- Horodatage: Corriger date compilation bug
- Nom: Obfuscation/masquage

---

## Q6: Qu'affiche "5) Injection code"?

**R:** Menu pour injecter du code:

\\\
SOUS-MENU: INJECTION CODE
├─ 1) Injecter shellcode
│  ├─ Choix source (fichier ou généré)
│  ├─ Choix section cible
│  ├─ Choix offset
│  └─ Écrit et reroute Entry Point
│
├─ 2) Générer shellcode placeholder
│  └─ 32 NOP (0x90)
│  └─ Pas exécution réelle
│
├─ 3) Ajouter overlay
│  ├─ Ajoute données après le PE
│  ├─ Non-mappé en mémoire
│  └─ Utile pour cache données
│
├─ 4) Extraire overlay
│  └─ Sauvegarde overlay en fichier
│
└─ 0) Retour
\\\

**Danger:** ⚠️ Peut corrompre le PE si mal fait

---

## Q7: Qu'affiche "6) Sécurité & Protections"?

**R:** Gestion des flags de protection:

\\\
SOUS-MENU: SÉCURITÉ
├─ 1) Afficher protections actuelles
│  ├─ ASLR (Address Space Layout Randomization)
│  ├─ DEP (Data Execution Prevention)
│  ├─ CFG (Control Flow Guard)
│  └─ État: activé (✓) ou désactivé (✗)
│
├─ 2) Activer/Désactiver ASLR
│  └─ Toggle flag DLL_DYNAMIC_BASE (0x0040)
│
├─ 3) Activer/Désactiver DEP
│  └─ Toggle flag DLLCHARACTERISTICS_NX_COMPAT (0x0100)
│
├─ 4) Activer/Désactiver CFG
│  └─ Toggle flag GUARD_CF (0x4000)
│
├─ 5) Détecter TLS callbacks
│  └─ Cherche fonctions TLS
│  └─ Affiche adresses si trouvées
│
└─ 0) Retour
\\\

**Importance:** Protections = sécurité application

---

## Q8: Qu'affiche "7) Utilitaires"?

**R:** Fonctions d'aide supplémentaires:

\\\
SOUS-MENU: UTILITAIRES
├─ 1) Afficher dump hexadécimal section
│  └─ Demande section
│  └─ Affiche bytes en hexa + ASCII
│
├─ 2) Calculer entropie manuelle
│  └─ Demande données
│  └─ Calcule Shannon entropy
│
├─ 3) Afficher ressources détaillées
│  └─ Liste tous types ressources
│  └─ Affiche comptes par type
│
├─ 4) Vérifier intégrité checksums
│  └─ Recalcule checksum
│  └─ Compare avec celui en-tête
│
└─ 0) Retour
\\\

**Usage:** Débugguage et vérification

---

### SECTION 2: LE PROJET PE BEAR GLOBALEMENT

---

## Q9: Qu'est-ce que PE BEAR exactement?

**R:** PE BEAR est:

**Définition officielle:**
"PE BEAR v2.0 - Professional Portable Executable Analysis & Manipulation Tool"

**En détail:**
- ✅ Outil d'analyse fichiers PE (Portable Executable)
- ✅ Permet modification propriétés
- ✅ Détecte protections & anomalies
- ✅ Outil éducatif & professionnel
- ✅ Open source (MIT License)
- ✅ Ligne de commande (CLI)
- ✅ En Python 3.8+

**Qui l'utilise?**
- Chercheurs sécurité
- Testeurs pénétration
- Étudiants cybersécurité
- Équipes développement
- Équipes malware analysis

---

## Q10: Pourquoi PE BEAR a été créé?

**R:** Raisons principales:

1. **Besoin:** Aucun outil gratuit complet en Python
2. **Éducation:** Enseigner internals des PE
3. **Recherche:** Faciliter reverse engineering légitime
4. **Combinaison:** Analyse + édition en une seule app
5. **Accessibilité:** Sans dépendances externes complexes

---

## Q11: Quelles sont les dépendances de PE BEAR?

**R:** Stack technique complet:

**Dépendances principales:**

\\\
pefile==2023.2.7          Parsing PE files
capstone==5.0.1           Disassembly (IDA-like)
keystone-engine==0.9.2    Assembly
unicorn==2.1.0            CPU emulation
colorama==0.4.6           Colors (Windows)
tabulate==0.9.0           Formatted tables
click==8.1.7              CLI arguments
\\\

**Développement:**

\\\
pytest==7.4.3             Unit testing
pytest-cov==4.1.0         Coverage analysis
black==23.12.0            Code formatting
pylint==3.0.3             Linting
mypy==1.7.1               Type checking
sphinx==7.2.6             Documentation
sphinx-rtd-theme==2.0.0   Doc theme
\\\

**Installation:**
\\\ash
pip install -r requirements.txt
\\\

---

## Q12: Comment fonctionne l'activation ANSI sur Windows?

**R:** Processus spécial pour couleurs dans terminal:

**Avant Windows 10:**
- Codes ANSI ne marchaient PAS
- Terminal affichait codes raw
- Aucune couleur

**Après Windows 10:**
- Support ANSI natif possible
- Via ctypes.windll.kernel32
- Activation flag: ENABLE_VIRTUAL_TERMINAL_PROCESSING

**Code:**

\\\python
import ctypes
import sys

kernel32 = ctypes.windll.kernel32
handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
mode = ctypes.c_ulong()

kernel32.GetConsoleMode(handle, ctypes.byref(mode))
mode.value |= 0x0004  # ENABLE_VIRTUAL_TERMINAL_PROCESSING

kernel32.SetConsoleMode(handle, mode)
\\\

**Résultat:**
- ✅ Couleurs affichées correctement
- ✅ Format tableau utilisable
- ✅ UX améliorée

---

## Q13: Comment le calcul d'entropie fonctionne?

**R:** Formule mathématique Shannon:

**Formule:**

\\\
Entropie = -Σ(P(byte) * log2(P(byte)))

Où:
  P(byte) = fréquence du byte / longueur totale
  Σ = somme sur tous les bytes 0-255
  log2 = logarithme base 2
\\\

**Implémentation Python:**

\\\python
def calculer_entropie(data):
    if len(data) == 0:
        return 0.0
    
    # Compter fréquences
    freq = {}
    for byte in data:
        freq[byte] = freq.get(byte, 0) + 1
    
    # Calculer entropie
    entropie = 0.0
    for count in freq.values():
        p = count / len(data)
        entropie -= p * math.log2(p)
    
    return entropie
\\\

**Interprétation:**

\\\
0-1   : Texte (très prévisible)
1-2   : Texte normal
2-4   : Données structurées
4-6   : Code exécutable
6-7   : Données comprimées
7-8   : Données chiffrées (maximum)
\\\

---

## Q14: Quelle est l'architecture du code fichier_exe.py?

**R:** Structure en 6 sections + main:

\\\
SECTION 1: CHARGEMENT/SAUVEGARDE (200 lignes)
├─ charger_fichier(chemin)
├─ sauvegarder(chemin_sortie)
└─ Validation fichiers

SECTION 2: AFFICHAGE/FORMATAGE (250 lignes)
├─ afficher_entete()
├─ afficher_tableau()
├─ afficher_succes/erreur/etc()
└─ Couleurs ANSI

SECTION 3: ANALYSE PE (400 lignes)
├─ _afficher_en_tetes()
├─ _afficher_sections()
├─ _afficher_imports()
├─ _afficher_exports()
├─ _afficher_ressources()
├─ _afficher_signature()
├─ _afficher_overlay()
└─ _afficher_tls()

SECTION 4: MENUS INTERACTIFS (300 lignes)
├─ menu_principal()
├─ menu_sections()
├─ menu_imports_exports()
├─ menu_edition()
├─ menu_injection()
└─ menu_securite()

SECTION 5: ÉDITION SPÉCIFIQUE (250 lignes)
├─ modifier_point_entree()
├─ modifier_image_base()
├─ modifier_horodatage()
├─ injecter_code()
└─ Gestion overlay

SECTION 6: UTILITAIRES (100 lignes)
├─ _human_size()
├─ _calculer_entropie()
├─ _generer_shellcode()
└─ afficher_hex_dump()

MAIN (50 lignes)
└─ Point d'entrée
\\\

**Total:** 1357 lignes de code commenté

---

## Q15: Qu'est-ce que la classe Config?

**R:** Classe statique centralisant les constantes:

\\\python
class Config:
    # Dimensions
    CONSOLE_WIDTH = 100
    TAB_SIZE = 2
    
    # Couleurs ANSI
    COLORS = {
        'red': '\\033[91m',
        'green': '\\033[92m',
        'yellow': '\\033[93m',
        'blue': '\\033[94m',
        'cyan': '\\033[96m',
        'white': '\\033[97m',
        'bold': '\\033[1m',
        'dim': '\\033[2m',
        'reset': '\\033[0m',
    }
    
    # Caractères
    CHARS = {
        'line': '═',
        'vertical': '║',
        'corner_tl': '╔',
        'corner_tr': '╗',
        ...
    }
\\\

**Usage:**

\\\python
# Utiliser une couleur
print(f"{Config.COLORS['green']}Succès{Config.COLORS['reset']}")

# Utiliser une dimension
max_width = Config.CONSOLE_WIDTH - 10
\\\

---

## Q16: Qu'est-ce que la classe PEBear?

**R:** Classe principale encapsulant toute la logique:

\\\python
class PEBear:
    def __init__(self):
        self.chemin = None           # Chemin fichier actuel
        self.pe = None               # Objet pefile.PE
        self.donnees_brutes = None   # Contenu binaire
        self.modifications = []      # Journal modifications
    
    def charger_fichier(self, chemin):
        # Charge et valide
        pass
    
    def sauvegarder(self, chemin):
        # Écrit modifications
        pass
    
    def analyser_tout(self):
        # Lance analyse complète
        pass
    
    def menu_principal(self):
        # Boucle menu
        pass
\\\

**Attributs clés:**
- self.chemin - Chemin du PE actuel
- self.pe - Objet pefile (parsing)
- self.donnees_brutes - Bytes du fichier
- self.modifications - Historique

---

## Q17: Comment les messages colorés sont générés?

**R:** Méthode standardisée avec tags:

\\\python
def afficher_succes(self, msg):
    tag = f"{Config.COLORS['green']}[OK]{Config.COLORS['reset']}"
    print(f"{tag} {msg}")
    # Affiche: [OK] message

def afficher_erreur(self, msg):
    tag = f"{Config.COLORS['red']}[ERREUR]{Config.COLORS['reset']}"
    print(f"{tag} {msg}")
    # Affiche: [ERREUR] message

def afficher_avertissement(self, msg):
    tag = f"{Config.COLORS['yellow']}[ATTENTION]{Config.COLORS['reset']}"
    print(f"{tag} {msg}")
    # Affiche: [ATTENTION] message

def afficher_info(self, msg):
    tag = f"{Config.COLORS['blue']}[INFO]{Config.COLORS['reset']}"
    print(f"{tag} {msg}")
    # Affiche: [INFO] message
\\\

**Standardisation:**
- ✓ Tags cohérents
- ✓ Couleurs consistantes
- ✓ Facile à parser

---

## Q18: Comment les tableaux sont formatés?

**R:** Utilise la libraire 	abulate:

\\\python
from tabulate import tabulate

entetes = ['Section', 'Taille', 'Droits']
lignes = [
    ['.text', '49.2 KB', 'R-X'],
    ['.data', '12.1 KB', 'RW-'],
    ['.rsrc', '234.5 KB', 'R--'],
]

tableau = tabulate(lignes, headers=entetes, tablefmt='grid')
print(tableau)
\\\

**Output:**

\\\
┌─────────────────────────┐
│ Section │ Taille  │ Droits│
├─────────────────────────┤
│ .text   │ 49.2 KB │ R-X  │
│ .data   │ 12.1 KB │ RW-  │
│ .rsrc   │ 234.5 KB│ R--  │
└─────────────────────────┘
\\\

---

## Q19: Qu'est-ce qu'un EOF marker et comment PE BEAR le gère?

**R:** EOF marker = fin du fichier

**Concept:**
- Fichier PE a taille définie
- Checksum calculé sur ces données
- Ajouter/retirer bytes = invalider checksum

**PE BEAR:**
1. Charge le fichier complètement
2. Modifie en mémoire (bytearray)
3. Recalcule checksum
4. Sauvegarde avec checksum correct
5. Fichier reste valide

---

## Q20: Pourquoi PE BEAR recalcule les checksums?

**R:** Garantir intégrité du fichier:

**Checksum = verrous de sécurité**

\\\
Avant modification:
  Fichier: DATA + CHECKSUM_VALIDE
  
Après modification manuelle:
  Fichier: DATA_MODIFIÉS + CHECKSUM_ANCIEN
  → Windows refuse ou avertit!
  
Avec PE BEAR:
  Fichier: DATA_MODIFIÉS + CHECKSUM_NOUVEAU
  → Windows accepte silencieusement
\\\

**Importance:**
- ✅ Application fonctionne après patch
- ✅ Pas d'avertissement utilisateur
- ✅ Pas de signature brisée

---

## Q21: Comment PE BEAR détecte les anomalies?

**R:** Plusieurs heuristiques:

\\\
1. ENTROPIE ANORMALE
   ├─ .text < 2.0 = possible obfuscation
   └─ .text > 7.5 = possible chiffrement

2. OVERLAY DÉTECTÉ
   ├─ Taille fichier > taille PE
   └─ Possible données cachées/malware

3. IMPORTS SUSPECTS
   ├─ CreateRemoteThread = injection
   ├─ SetWindowsHookEx = hooking
   └─ CryptEncrypt = chiffrement

4. TLS CALLBACKS
   ├─ Code avant main
   └─ Anti-debugging possible

5. SIGNATURE MANQUANTE
   ├─ Aucun certificat
   └─ Source inconnue
\\\

---

## Q22: Quelle est la taille maximale d'un PE que PE BEAR peut analyser?

**R:** Limitation pratique, pas théorique:

\\\
Fichiers < 100 MB: Chargement rapide (< 1s)
Fichiers 100-500 MB: Lent mais OK (5-10s)
Fichiers > 500 MB: Très lent (30+ secondes)

Limite système: 2-4 GB (dépend RAM)
\\\

**Raison:**
- Charge TOUT en mémoire (bytearray)
- Parse avec pefile (lent sur gros fichiers)
- Affichage peut être volumineux

---

## Q23: PE BEAR peut-il modifier des fichiers DLL?

**R:** OUI, avec les mêmes outils:

**Différences DLL vs EXE:**
- EXE = programme standalone
- DLL = library partagée
- Ambos = même format PE

**Ce qu'on peut faire:**
- ✅ Analyser DLL
- ✅ Modifier Entry Point (DLL Entry)
- ✅ Modifier ImageBase
- ✅ Modifier horodatage
- ✅ Injecter code

**Attention:**
- ⚠️ Entry Point DLL = DllMain
- ⚠️ Dépendances peuvent casser
- ⚠️ Tester en sandbox

---

## Q24: Comment PE BEAR gère les erreurs?

**R:** Stratégie complète:

\\\
1. ERREURS CRITIQUES (Rouge)
   ├─ Fichier non trouvé
   ├─ Format PE invalide
   ├─ Permission refusée
   └─ Action: Arrête + message

2. ERREURS NON-CRITIQUES (Jaune)
   ├─ Overlay vide
   ├─ Pas d'exports
   ├─ Signature invalide
   └─ Action: Continue + avertit

3. INFO (Bleu)
   ├─ Fichier chargé
   ├─ Sections trouvées
   ├─ Analysis complétée
   └─ Action: Continue + informe
\\\

**Try/Except partout:**
- Chaque opération protégée
- Pas de crash silencieux
- Messages explicites

---

## Q25: Peut-on automatiser PE BEAR par script?

**R:** Partiellement (design interactif actuel):

**Actuellement:**
- CLI interactive (menus)
- Pas d'API d'automatisation
- Pas de mode batch

**Possibilités futures:**
- Mode CLI arguments
- Import comme module Python
- API CLI standalone

**Exemple souhaité:**
\\\ash
pe-bear analyze-all notepad.exe
pe-bear modify-ep -e notepad.exe -a 0x401000
pe-bear inject-code -e notepad.exe -s shellcode.bin
\\\

---

## Q26: PE BEAR supporte-t-il les fichiers 32-bit et 64-bit?

**R:** OUI, tous les deux:

**Différences:**

\\\
32-bit (PE32):
├─ Magic: 0x010B
├─ ImageBase typique: 0x400000
├─ Adresses: 32-bit
└─ Flags: Version 3.0+

64-bit (PE32+):
├─ Magic: 0x020B
├─ ImageBase typique: 0x140000000
├─ Adresses: 64-bit
└─ Flags: Version 3.0+
\\\

**PE BEAR:**
- ✅ Détecte auto le format
- ✅ Parse structures différentes
- ✅ Gère les deux transparemment

---

## Q27: Qu'est-ce qu'un "relocation"?

**R:** Ajustement d'adresse pour ASLR:

\\\
PE chargé à 0x140000000 (ImageBase)
Code contient adresse absolue: 0x140000000 + 0x1234
  = 0x140001234

ASLR active, charge à 0x7FFF0000 (aléatoire)
Relocation doit ajouter: 0x7FFF0000 - 0x140000000
  = Offset négatif
  
Nouvelle adresse: 0x140001234 + offset
  = 0x7FFF1234
\\\

**PE BEAR:**
- Affiche nombre relocalisations
- Pas de modification directe
- Checksum tient compte des changements

---

## Q28: Comment PE BEAR valide un checksum?

**R:** Recalcul et comparaison:

\\\
1. Charger le PE
2. Lire checksum dans OPTIONAL_HEADER
3. Recalculer checksum sur les données actuelles
4. Comparer:
   ├─ Si égal: ✓ Valide
   └─ Si différent: ✗ Corrompu ou modifié
5. Afficher état
\\\

**Lors sauvegarde:**
- Recalcul automatique
- Nouvelle valeur écrite
- Fichier reste valide

---

## Q29: Peut-on patcher le code .text directement?

**R:** OUI, mais dangereux:

\\\
Injection dans .text:
1. Section R-X (Read-Execute)
2. Écrire ne devrait pas être possible
3. PE BEAR le permet (hors protections OS)
4. À l'exécution:
   ├─ Windows applique DEP (Data Execution)
   ├─ Si DEP on: Page-Fault, crash
   └─ Si DEP off: Code exécuté (dangereux!)

Solution:
1. Créer nouvelle section R-X
2. Placer code injecté là
3. Rediriger EP vers section
4. Prendre en compte relocations
\\\

**Complexité:** Élevée, risque corruption

---

## Q30: Quel est le roadmap futur de PE BEAR?

**R:** Plans d'évolution:

\\\
PE BEAR v2.0 (Actuel):
✅ Analyse complète
✅ Édition de base
✅ Détection anomalies
✅ CLI interactive

PE BEAR v3.0 (Planifié):
└─ GUI graphique (PyQt/Tkinter)
└─ Désassembly avancé (IDA-like)
└─ Émulation CPU (Unicorn)
└─ Export PDF/HTML
└─ Plugins communauté
└─ Mode batch/CLI

PE BEAR v4.0 (Visionnaire):
└─ Analyse machine learning (malware classification)
└─ Décompilation (Ghidra)
└─ Collaboration temps-réel
└─ Cloud analysis
└─ Mobile PE (rare)
\\\

---

**Dernière mise à jour:** 27 Août 2026  
**Version:** 2.0.0  
**Fiche révision complète**
