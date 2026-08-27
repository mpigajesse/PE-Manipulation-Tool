# PE BEAR - Exemples Détaillés & Cas d'Usage

## 📚 Table des matières

1. [Cas Simples](#cas-simples)
2. [Cas Intermédiaires](#cas-intermédiaires)
3. [Cas Avancés](#cas-avancés)
4. [Malware Analysis](#malware-analysis)
5. [Débugguage & Patching](#débugguage--patching)

---

## Cas Simples

### Cas 1: Analyser un Exécutable Basique

**Objectif:** Examiner un simple Hello World.exe

**Étapes:**

\\\
1. Lancer PE BEAR
   $ python fichier_exe.py

2. Demande de fichier
   > Entrer chemin: C:\Windows\System32\notepad.exe

3. Attendre chargement
   [OK] Fichier chargé avec succès

4. Menu principal
   1) Analyser tout
   ...
   > Choix: 1

5. Résultats:
   ├─ DOS Header affiché
   ├─ FILE Header affiché
   ├─ OPTIONAL Header affiché
   ├─ Sections listées
   ├─ Imports affichés
   ├─ Exports affichés
   └─ Signature vérifiée
\\\

**À Observer:**

\\\
DOS Header:
  e_magic: 0x5A4D (MZ)
  e_lfanew: 0x00000090
  
FILE Header:
  Machine: Intel 386 (0x014C)
  NumberOfSections: 6
  Timestamp: 2024-01-15 10:30:45
  
OPTIONAL Header:
  Magic: PE32+ (0x020B)
  AddressOfEntryPoint: 0x00001234
  ImageBase: 0x0000000140000000
  
Sections:
  .text   : 0x1234 (49.2 KB) | R-X | Entropie: 6.2
  .data   : 0x2345 (12.1 KB) | R-- | Entropie: 2.1
  .rsrc   : 0x3456 (234.5 KB)| R-- | Entropie: 7.8
\\\

**Interprétation:**

- ✅ Exécutable Windows légitime (e_magic valide)
- ✅ 64-bit (Magic 020B)
- ✅ Protections modernes (ASLR, DEP, CFG activés)
- ✅ Sections normales (.text, .data, .rsrc)
- ✅ Entropie section .text: 6.2 = code normal
- ⚠️ Entropie .rsrc: 7.8 = données comprimées (normal pour ressources)

---

### Cas 2: Vérifier les Droits des Sections

**Objectif:** Vérifier les permissions R/W/X

**Procédure:**

\\\
Menu: 2) Gestion sections
      3) Voir droits sections

Affichage:
┌─────────────────────────────────┐
│ Section    │ Droits │ Flags     │
├─────────────────────────────────┤
│ .text      │ R-X    │ 0x60000020│
│ .data      │ RW-    │ 0xC0000040│
│ .rsrc      │ R--    │ 0x40000040│
│ .reloc     │ R--    │ 0x40000040│
└─────────────────────────────────┘

Légende:
  R = Lecture (Read)
  W = Écriture (Write)
  X = Exécution (Execute)
  - = Non permis
\\\

**Analyse:**

\\\
✅ .text: R-X
   └─ Correct! Code exécutable, non-modifiable

✅ .data: RW-
   └─ Correct! Données modifiables, non-exécutables

✅ .rsrc: R--
   └─ Correct! Ressources lecture seule

⚠️ .reloc: R--
   └─ Correct! Relocalisations non-exécutables
\\\

---

**Dernière mise à jour:** 27 Août 2026  
**Version:** 2.0.0
