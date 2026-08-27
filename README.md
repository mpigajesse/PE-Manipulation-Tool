# PE  - Analyseur et Editeur de Fichiers PE

## Description

**PE ** est un outil professionnel complet pour l'analyse et la manipulation de fichiers **Portable Executable (PE)** sous Windows.

Conçu pour le reverse engineering, l'analyse de malwares et l'édition binaire, PE  offre une interface intuitive et colorisée.

## Fonctionnalités

✅ Analyse complète (en-têtes, sections, imports, exports)  
✅ Édition avancée (point d'entrée, ImageBase, horodatage)  
✅ Injection de code et shellcode  
✅ Gestion des protections (ASLR, DEP, CFG)  
✅ Gestion des sections (R/W/X, export, entropie)  
✅ Journal complet des modifications  
✅ Interface colorisée (codes ANSI)  
✅ Tableaux professionels  

## Installation

```bash
cd E:\PE
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Utilisation

```bash
# Mode interactif
python fichier_exe.py

# Mode direct
python fichier_exe.py "C:\Path\To\File.exe"
```

## Menu principal

```
[MENU PRINCIPAL]

  1. Analyser le fichier complet
  2. Gerer les sections
  3. Gerer les imports/exports
  4. Editer les proprietes avancees
  5. Injection de code
  6. Modifications de securite
  7. Journal des modifications
  8. Sauvegarder le fichier
  9. Quitter
```

## Codes couleur

- [OK] - Succès (vert)
- [ERREUR] - Erreur (rouge)
- [ATTENTION] - Avertissement (jaune)
- [INFO] - Information (bleu)

## Architecture

- Activation ANSI (Windows 10+)
- Config (Constantes)
- PE (Classe principale)
  - Section 1: Chargement/Sauvegarde
  - Section 2: Affichage/Formatage
  - Section 3: Analyse PE
  - Section 4: Menus interactifs
  - Section 5: Édition spécifique
  - Section 6: Utilitaires
- main() (Point d'entrée)

## Caractéristiques

### Analyse
- En-têtes DOS, FILE, OPTIONAL
- Sections avec entropie et SHA-256
- Imports/exports détaillés
- Ressources, signature, overlay
- TLS callbacks

### Édition
- Point d'entrée (RVA)
- ImageBase
- Horodatage
- Droits sections

### Injection
- Code binaire
- Shellcode
- Overlay

### Protections
- ASLR
- DEP
- CFG

## Licence

MIT License

## 📝 Auteur

**Jesse Mpiga-Odoumba**
- Développeur Full-Stack & Ingénieur IA & Big Data
- Spécialiste Cybersécurité & Cryptographie
- Email: jesse.mpiga@a-ct.ma
- GitHub: [github.com/mpigajesse](https://github.com/mpigajesse)

---

PE BEAR Project v2.0.0  
Reverse engineering professionnel  
Windows 10+ support  

**Date:** 27 Août 2026  
**Status:** Production ✅
