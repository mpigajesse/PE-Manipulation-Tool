# -*- coding: utf-8 -*-
"""
PE  - Analyseur et Editeur de Fichiers Portable Executable (PE)
Outil professionnel pour l'analyse et la manipulation de fichiers PE:
- exe, dll, sys, drv, etc.

Fonctionnalites principales:
  1. Analyse complete du format PE (en-tetes, sections, imports/exports)
  2. Edition des en-tetes et structures
  3. Modification des droits d'acces des sections (R/W/X)
  4. Injection de code et shellcode
  5. Gestion des overlays
  6. Controle des protections (ASLR, DEP, CFG)
  7. Journal complet des modifications

Utilisation:
  - python fichier_exe.py              (mode selection interactif)
  - python fichier_exe.py chemin.exe   (ouvre directement le fichier)

"""

import pefile
import os
import sys
import math
import hashlib
import ctypes
from datetime import datetime, timezone
from typing import Optional, List, Dict

# # ACTIVATION DES CODES ANSI SUR WINDOWS 10+
# # Sans cette activation, les couleurs ANSI ne s'affichent pas en PowerShell Windows

if sys.platform == 'win32':
    try:
        # Activer le mode ANSI sur Windows 10+
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        mode.value |= 0x0004  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
        kernel32.SetConsoleMode(handle, mode)
    except Exception:
        # Fallback pour les anciennes versions de Windows
        pass

# # CONFIGURATION GLOBALE - Parametres et constantes
# 
class Config:
    """Constantes et parametres globaux de l'application."""

    # Largeur de l'affichage en caracteres
    CONSOLE_WIDTH = 100

    # Styles de couleur ANSI pour terminal
    COLORS = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'bold': '\033[1m',
        'dim': '\033[2m',
        'reset': '\033[0m'
    }

    # Caracteres pour dessiner les boites et lignes
    CHARS = {
        'h_line': '=',        # Ligne horizontale
        'v_line': '|',        # Ligne verticale
        'corner_tl': '+',     # Coin haut gauche
        'corner_tr': '+',     # Coin haut droit
        'corner_bl': '+',     # Coin bas gauche
        'corner_br': '+',     # Coin bas droit
        'cross': '+',         # Intersection
        'dash': '-',          # Tiret court
    }


# # CLASSE PRINCIPALE - PE
# 
class PE:
    """
    Classe principale pour l'analyse et la manipulation de fichiers PE.

    Attributs:
        chemin (str): Chemin du fichier PE charge
        pe (pefile.PE): Objet PE charge en memoire
        donnees_brutes (bytearray): Donnees brutes du fichier
        modifications (list): Journal des modifications effectuees
    """

    def __init__(self, chemin_fichier: Optional[str] = None):
        """
        Initialise l'analyseur PE.

        Arguments:
            chemin_fichier (str, optional): Chemin du fichier a charger
        """
        self.chemin = chemin_fichier
        self.pe = None
        self.donnees_brutes = None
        self.modifications = []

        # Charger le fichier s'il est fourni
        if chemin_fichier and os.path.exists(chemin_fichier):
            self.charger_fichier(chemin_fichier)

    # ============================================================================
    # SECTION 1: CHARGEMENT ET SAUVEGARDE DU FICHIER PE
    # ============================================================================

    def charger_fichier(self, chemin: str) -> bool:
        """
        Charge un fichier PE depuis le disque dans la memoire.

        Etapes:
        1. Verifier que le fichier existe
        2. Lire le contenu binaire complet
        3. Parser la structure PE avec pefile
        4. Enregistrer les informations de base
        5. Afficher un resume d'information

        Arguments:
            chemin (str): Chemin vers le fichier PE

        Retour:
            bool: True si charge avec succes, False sinon
        """
        try:
            # Etape 1: Verifier l'existence du fichier
            if not os.path.exists(chemin):
                self.afficher_erreur(f"Fichier introuvable: {chemin}")
                return False

            # Etape 2: Lire le contenu en tant que bytearray
            with open(chemin, "rb") as f:
                self.donnees_brutes = bytearray(f.read())

            # Etape 3: Parser avec pefile (fast_load=False pour analyse complete)
            self.pe = pefile.PE(data=self.donnees_brutes, fast_load=False)
            self.chemin = chemin
            self.modifications = []

            # Etape 4 et 5: Afficher les informations resumees
            self.afficher_succes(f"Fichier charge: {os.path.basename(chemin)}")
            self._afficher_info_resume()

            return True

        except pefile.PEFormatError as e:
            self.afficher_erreur(f"Format PE invalide: {e}")
            return False
        except Exception as e:
            self.afficher_erreur(f"Erreur lors du chargement: {e}")
            return False

    def sauvegarder(self, chemin: Optional[str] = None) -> bool:
        """
        Sauvegarde le fichier PE modifie sur le disque.

        Processus:
        1. Verifier qu'un fichier est charge
        2. Calculer le checksum correct
        3. Ecrire le fichier modifie
        4. Afficher confirmation

        Arguments:
            chemin (str, optional): Chemin de sortie (defaut: fichier_original_modified.exe)

        Retour:
            bool: True si sauvegarde reussie, False sinon
        """
        if not self.pe:
            self.afficher_erreur("Aucun fichier charge")
            return False

        try:
            # Determiner le chemin de sortie
            chemin_sortie = chemin or f"{self.chemin}_modified.exe"

            # Calculer le checksum correct du fichier modifie
            self.pe.OPTIONAL_HEADER.CheckSum = pefile.PE.calculate_checksum(
                bytes(self.pe.write())
            )

            # Ecrire le fichier
            self.pe.write(filename=chemin_sortie)

            self.afficher_succes(f"Fichier sauvegarde: {chemin_sortie}")
            self.afficher_info(f"Modifications enregistrees: {len(self.modifications)}")

            return True

        except Exception as e:
            self.afficher_erreur(f"Erreur de sauvegarde: {e}")
            return False

    # ============================================================================
    # SECTION 2: AFFICHAGE ET FORMATAGE
    # ============================================================================

    def afficher_entete(self):
        """Affiche l'en-tete principal de l'application."""
        largeur = Config.CONSOLE_WIDTH
        ligne_sup = Config.CHARS['h_line'] * largeur

        titre = "PE  - Analyseur et Editeur de Fichiers PE"
        ligne_titre = titre.center(largeur)

        print(f"\n{ligne_sup}")
        print(ligne_titre)
        print(ligne_sup)

    def afficher_section(self, titre: str):
        """
        Affiche un titre de section avec separateurs.

        Format horizontal:
        [TITRE_DE_LA_SECTION] -------- analyse details --------
        """
        largeur = Config.CONSOLE_WIDTH
        tailletitre = len(f"[{titre}]")
        espaces_restants = largeur - tailletitre - 2
        demi_esp = espaces_restants // 2

        ligne = f"[{titre}]" + " " + Config.CHARS['dash'] * demi_esp + " DETAILS " + Config.CHARS['dash'] * (demi_esp - 9)
        print(f"\n{ligne}")

    def afficher_ligne_separatrice(self):
        """Affiche une ligne de separation horizontale."""
        print(Config.CHARS['h_line'] * Config.CONSOLE_WIDTH)

    def afficher_succes(self, message: str):
        """Affiche un message de succes en vert."""
        couleur = Config.COLORS['green']
        reset = Config.COLORS['reset']
        print(f"{couleur}[OK]{reset} {message}")

    def afficher_erreur(self, message: str):
        """Affiche un message d'erreur en rouge."""
        couleur = Config.COLORS['red']
        reset = Config.COLORS['reset']
        print(f"{couleur}[ERREUR]{reset} {message}")

    def afficher_avertissement(self, message: str):
        """Affiche un message d'avertissement en jaune."""
        couleur = Config.COLORS['yellow']
        reset = Config.COLORS['reset']
        print(f"{couleur}[ATTENTION]{reset} {message}")

    def afficher_info(self, message: str):
        """Affiche une information en bleu."""
        couleur = Config.COLORS['blue']
        reset = Config.COLORS['reset']
        print(f"{couleur}[INFO]{reset} {message}")

    def afficher_tableau(self, entetes: List[str], lignes: List[List], largeurs: Optional[List[int]] = None):
        """
        Affiche un tableau horizontal formaté.

        Format:
        | Col1      | Col2      | Col3      |
        |-----------|-----------|-----------|
        | Valeur1   | Valeur2   | Valeur3   |

        Arguments:
            entetes (list): Liste des en-tetes de colonnes
            lignes (list): Liste des listes de valeurs (une par ligne)
            largeurs (list, optional): Largeurs personnalisees des colonnes
        """
        if not lignes:
            self.afficher_info("Aucune donnee a afficher")
            return

        # Calculer les largeurs des colonnes automatiquement
        if largeurs is None:
            largeurs = [len(str(h)) for h in entetes]
            for ligne in lignes:
                for i, cellule in enumerate(ligne):
                    if i < len(largeurs):
                        largeurs[i] = max(largeurs[i], len(str(cellule)))

        # Ajouter du padding
        largeurs = [l + 2 for l in largeurs]

        # Afficher l'en-tete
        sep_entete = "|"
        for i, entete in enumerate(entetes):
            sep_entete += f" {str(entete):<{largeurs[i]-1}} |"
        print(sep_entete)

        # Afficher la ligne de separation
        sep_ligne = "+"
        for l in largeurs:
            sep_ligne += Config.CHARS['dash'] * l + "+"
        print(sep_ligne)

        # Afficher les lignes de donnees
        for ligne in lignes:
            sep_donnees = "|"
            for i, cellule in enumerate(ligne):
                val = str(cellule)[:largeurs[i]-3] if len(str(cellule)) > largeurs[i]-3 else str(cellule)
                sep_donnees += f" {val:<{largeurs[i]-1}} |"
            print(sep_donnees)

    # ============================================================================
    # SECTION 3: ANALYSE DU FICHIER PE
    # ============================================================================

    def _afficher_info_resume(self):
        """Affiche un resume rapide du fichier PE charge."""
        if not self.pe:
            return

        self.afficher_info(f"Taille: {self._human_size(len(self.donnees_brutes))}")
        self.afficher_info(f"Architecture: {'64-bit (PE32+)' if self.est_64bits() else '32-bit (PE32)'}")
        self.afficher_info(f"Type: {'DLL' if self.est_dll() else 'Executable'}")

    def est_64bits(self) -> bool:
        """Retourne True si le PE est 64-bit (PE32+)."""
        return self.pe and self.pe.OPTIONAL_HEADER.Magic == 0x20B

    def est_dll(self) -> bool:
        """Retourne True si c'est une DLL (bit 0x2000 du FILE_HEADER)."""
        return self.pe and bool(self.pe.FILE_HEADER.Characteristics & 0x2000)

    def analyser_tout(self):
        """
        Effectue une analyse complete et detaillee du fichier PE.

        Ordre d'affichage:
        1. En-tetes (DOS, FILE, OPTIONAL)
        2. Sections et leurs proprietes
        3. Imports (DLL et fonctions)
        4. Exports (symboles exportes)
        5. Ressources
        6. Signature numerique
        7. Overlay et donnees supplementaires
        8. TLS Callbacks
        """
        if not self.pe:
            self.afficher_erreur("Aucun fichier charge")
            return

        self.afficher_entete()
        self.afficher_section("ANALYSE COMPLETE")
        self.afficher_ligne_separatrice()

        # Executer toutes les analyses dans l'ordre
        self._afficher_en_tetes()
        self._afficher_sections()
        self._afficher_imports()
        self._afficher_exports()
        self._afficher_ressources()
        self._afficher_signature()
        self._afficher_overlay()
        self._afficher_tls()

        self.afficher_ligne_separatrice()

    def _afficher_en_tetes(self):
        """Affiche les en-tetes DOS, FILE et OPTIONAL."""
        self.afficher_section("EN-TETES PE")

        # DOS Header
        print("\nDOS HEADER:")
        print(f"  e_magic          : {hex(self.pe.DOS_HEADER.e_magic)} {'(VALIDE)' if self.pe.DOS_HEADER.e_magic == 0x5A4D else '(INVALIDE)'}")
        print(f"  e_lfanew         : {hex(self.pe.DOS_HEADER.e_lfanew)}")

        # FILE Header
        print("\nFILE HEADER:")
        machine_type = pefile.MACHINE_TYPE.get(self.pe.FILE_HEADER.Machine, "Inconnue")
        print(f"  Machine          : {hex(self.pe.FILE_HEADER.Machine)} ({machine_type})")
        print(f"  Sections         : {self.pe.FILE_HEADER.NumberOfSections}")
        print(f"  TimeDateStamp    : {hex(self.pe.FILE_HEADER.TimeDateStamp)}")

        if self.pe.FILE_HEADER.TimeDateStamp:
            try:
                date = datetime.fromtimestamp(self.pe.FILE_HEADER.TimeDateStamp, tz=timezone.utc)
                print(f"                   -> {date.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            except:
                pass

        # OPTIONAL Header
        print("\nOPTIONAL HEADER:")
        oh = self.pe.OPTIONAL_HEADER
        pe_type = "PE32+ (64-bit)" if self.est_64bits() else "PE32 (32-bit)"
        print(f"  Magic            : {hex(oh.Magic)} ({pe_type})")
        print(f"  Entry Point      : {hex(oh.AddressOfEntryPoint)}")
        print(f"  ImageBase        : {hex(oh.ImageBase)}")
        print(f"  SizeOfImage      : {self._human_size(oh.SizeOfImage)}")
        print(f"  SizeOfCode       : {self._human_size(oh.SizeOfCode)}")

        # Protections
        dllchar = oh.DllCharacteristics
        protections = []
        if dllchar & 0x0040: protections.append("ASLR")
        if dllchar & 0x0100: protections.append("DEP")
        if dllchar & 0x0400: protections.append("No SEH")
        if dllchar & 0x4000: protections.append("CFG")
        prot_str = " + ".join(protections) if protections else "AUCUNE"
        print(f"  Protections      : {prot_str}")

    def _afficher_sections(self):
        """Affiche le tableau horizontal des sections."""
        self.afficher_section("SECTIONS DU PE")

        entetes = ["INDEX", "NOM", "VSIZE", "VADDR", "RSIZE", "OFFSET", "ENTROPIE", "R", "W", "X"]
        lignes = []

        for i, section in enumerate(self.pe.sections):
            nom = section.Name.decode("utf-8", "replace").rstrip("\x00")[:8]

            # Calculer l'entropie de la section
            data = section.get_data()
            entropie = self._calculer_entropie(data) if data else 0.0

            # Determiner les droits d'acces
            r = "OUI" if section.Characteristics & 0x40000000 else "NON"
            w = "OUI" if section.Characteristics & 0x80000000 else "NON"
            x = "OUI" if section.Characteristics & 0x20000000 else "NON"

            lignes.append([
                str(i),
                nom,
                self._human_size(section.Misc_VirtualSize),
                hex(section.VirtualAddress),
                self._human_size(section.SizeOfRawData),
                hex(section.PointerToRawData),
                f"{entropie:.2f}",
                r,
                w,
                x
            ])

        self.afficher_tableau(entetes, lignes)

    def _afficher_imports(self):
        """Affiche les DLL importees et leurs fonctions."""
        if not hasattr(self.pe, "DIRECTORY_ENTRY_IMPORT"):
            return

        self.afficher_section("IMPORTS")

        total_dll = len(self.pe.DIRECTORY_ENTRY_IMPORT) if self.pe.DIRECTORY_ENTRY_IMPORT else 0
        total_fonctions = 0

        if total_dll == 0:
            self.afficher_info("Aucun import trouve")
            return

        for entry in self.pe.DIRECTORY_ENTRY_IMPORT:
            try:
                nom_dll = entry.dll.decode("utf-8")
            except:
                nom_dll = "[Erreur lecture DLL]"

            fonctions = []
            for imp in entry.imports:
                if imp.name:
                    fonctions.append(imp.name.decode("utf-8", "replace"))
                else:
                    fonctions.append(f"[Ordinal {imp.ordinal}]")

            total_fonctions += len(fonctions)

            print(f"\n{nom_dll} ({len(fonctions)} fonctions)")
            print(Config.CHARS['dash'] * 60)

            # Afficher les fonctions par groupe de 4 (affichage horizontal)
            for i in range(0, len(fonctions), 4):
                groupe = fonctions[i:i+4]
                ligne = "  " + " | ".join(f"{f[:20]:<20}" for f in groupe)
                print(ligne)

        print(f"\nRESUME: {total_dll} DLL importees | {total_fonctions} fonctions")

    def _afficher_exports(self):
        """Affiche les symboles exportes."""
        if not hasattr(self.pe, "DIRECTORY_ENTRY_EXPORT"):
            self.afficher_info("Aucun export trouve")
            return

        self.afficher_section("EXPORTS")

        symboles = self.pe.DIRECTORY_ENTRY_EXPORT.symbols if hasattr(self.pe.DIRECTORY_ENTRY_EXPORT, 'symbols') else []

        if not symboles:
            self.afficher_info("Aucun export trouve")
            return

        entetes = ["ORDINAL", "ADRESSE", "NOM"]
        lignes = []

        for exp in symboles:
            nom = exp.name.decode("utf-8", "replace") if exp.name else "[Anonyme]"
            lignes.append([str(exp.ordinal), hex(exp.address), nom])

        self.afficher_tableau(entetes, lignes[:20])

        if len(symboles) > 20:
            self.afficher_info(f"...et {len(symboles) - 20} autres exports")

    def _afficher_ressources(self):
        """Affiche les types de ressources presentees."""
        if not hasattr(self.pe, "DIRECTORY_ENTRY_RESOURCE"):
            return

        self.afficher_section("RESSOURCES")

        types_ressources = {
            1: "Cursor", 2: "Bitmap", 3: "Icon", 4: "Menu", 5: "Dialog",
            6: "String", 7: "Font Dir", 8: "Font", 9: "Accelerator",
            10: "RCDATA", 11: "Message Table", 16: "Version", 24: "Manifest"
        }

        ressources_trouvees = []
        for res_type in self.pe.DIRECTORY_ENTRY_RESOURCE.entries:
            if res_type.id:
                nom = types_ressources.get(res_type.id, f"Type {res_type.id}")
                ressources_trouvees.append(nom)

        if ressources_trouvees:
            # Affichage horizontal: 4 ressources par ligne
            for i in range(0, len(ressources_trouvees), 4):
                groupe = ressources_trouvees[i:i+4]
                ligne = "  " + " | ".join(f"{r:<20}" for r in groupe)
                print(ligne)
        else:
            self.afficher_info("Aucune ressource trouvee")

    def _afficher_signature(self):
        """Affiche le statut de signature numerique."""
        self.afficher_section("SIGNATURE")

        idx_secu = pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]
        secu = self.pe.OPTIONAL_HEADER.DATA_DIRECTORY[idx_secu]

        if secu.VirtualAddress == 0 or secu.Size == 0:
            self.afficher_avertissement("Le fichier n'est pas signe")
        else:
            self.afficher_succes(f"Fichier signe ({self._human_size(secu.Size)})")
            print(f"  Offset: {hex(secu.VirtualAddress)}")

    def _afficher_overlay(self):
        """Affiche les informations sur l'overlay (donnees apres le PE)."""
        self.afficher_section("OVERLAY")

        try:
            debut = self.pe.get_overlay_data_start_offset()
            if debut and debut < len(self.donnees_brutes):
                overlay = self.donnees_brutes[debut:]
                entropie = self._calculer_entropie(overlay)

                print(f"\nOverlay present: OUI")
                print(f"  Offset     : {hex(debut)}")
                print(f"  Taille     : {self._human_size(len(overlay))}")
                print(f"  Entropie   : {entropie:.3f}")
                print(f"  SHA-256    : {hashlib.sha256(overlay).hexdigest()}")

                # Detecter les types d'archives courants
                signatures = {
                    b"7z\xbc\xaf": "7-Zip SFX Archive",
                    b"PK\x03\x04": "ZIP Archive",
                    b"Rar!": "RAR Archive",
                }
                for sig, desc in signatures.items():
                    if overlay.startswith(sig):
                        print(f"  Type       : {desc}")
                        break
            else:
                self.afficher_info("Aucun overlay detecte")
        except:
            self.afficher_avertissement("Impossible d'analyser l'overlay")

    def _afficher_tls(self):
        """Affiche les callbacks TLS (Thread Local Storage)."""
        if not hasattr(self.pe, "DIRECTORY_ENTRY_TLS"):
            return

        self.afficher_section("TLS CALLBACKS")

        try:
            cbs = self.pe.DIRECTORY_ENTRY_TLS.struct.AddressOfCallBacks
            if cbs:
                self.afficher_avertissement(f"TLS Callbacks present a {hex(cbs)}")
                print("  (Code execute AVANT le point d'entree)")
            else:
                self.afficher_info("Aucun TLS callback detecte")
        except:
            self.afficher_avertissement("Impossible de lire les TLS callbacks")

    # ============================================================================
    # SECTION 4: MENUS INTERACTIFS
    # ============================================================================

    def menu_principal(self):
        """
        Menu principal interactif avec format VERTICAL.

        Options:
        1. Analyser le fichier complet
        2. Gerer les sections
        3. Gerer les imports/exports
        4. Editer les proprietes (EP, ImageBase, etc.)
        5. Injecter du code
        6. Modifier les protections
        7. Voir le journal des modifications
        8. Sauvegarder le fichier
        9. Quitter
        """
        if not self.pe:
            self.afficher_erreur("Aucun fichier charge")
            return

        while True:
            self.afficher_entete()

            # Affichage du fichier ouvert avec couleur
            couleur_cyan = Config.COLORS['cyan']
            couleur_bold = Config.COLORS['bold']
            couleur_reset = Config.COLORS['reset']

            print(f"\n{couleur_cyan}{couleur_bold}Fichier actuel:{couleur_reset} {os.path.basename(self.chemin)}")
            self.afficher_ligne_separatrice()

            # Menu VERTICAL
            print("\n[MENU PRINCIPAL]")
            print()
            print("  1. Analyser le fichier complet")
            print("  2. Gerer les sections")
            print("  3. Gerer les imports/exports")
            print("  4. Editer les proprietes avancees")
            print("  5. Injection de code")
            print("  6. Modifications de securite")
            print("  7. Journal des modifications")
            print("  8. Sauvegarder le fichier")
            print("  9. Quitter")
            print()

            choix = input("Votre choix (1-9): ").strip().strip('"').strip("'")

            if choix == '1':
                self.analyser_tout()
            elif choix == '2':
                self.menu_sections()
            elif choix == '3':
                self.menu_imports_exports()
            elif choix == '4':
                self.menu_edition()
            elif choix == '5':
                self.menu_injection()
            elif choix == '6':
                self.menu_securite()
            elif choix == '7':
                self.afficher_journal()
            elif choix == '8':
                self.sauvegarder()
            elif choix == '9':
                print(f"\n{Config.COLORS['yellow']}Au revoir!{Config.COLORS['reset']}")
                break
            else:
                self.afficher_erreur("Choix invalide (1-9)")

    def menu_sections(self):
        """Menu de gestion des sections du PE - Affichage VERTICAL."""
        while True:
            self.afficher_section("GESTION DES SECTIONS")

            print("\n  1. Afficher les sections")
            print("  2. Voir details d'une section")
            print("  3. Modifier droits d'acces")
            print("  4. Exporter une section")
            print("  5. Retour au menu principal")
            print()

            choix = input("Votre choix (1-5): ").strip()

            if choix == '1':
                self._afficher_sections()
            elif choix == '2':
                self.voir_section()
            elif choix == '3':
                self.modifier_droits_section()
            elif choix == '4':
                self.exporter_section()
            elif choix == '5':
                break
            else:
                self.afficher_erreur("Choix invalide")

    def menu_imports_exports(self):
        """Menu de gestion des imports et exports - Affichage VERTICAL."""
        while True:
            self.afficher_section("IMPORTS / EXPORTS")

            print("\n  1. Afficher les imports")
            print("  2. Afficher les exports")
            print("  3. Retour au menu principal")
            print()

            choix = input("Votre choix (1-3): ").strip()

            if choix == '1':
                self._afficher_imports()
            elif choix == '2':
                self._afficher_exports()
            elif choix == '3':
                break
            else:
                self.afficher_erreur("Choix invalide")

    def menu_edition(self):
        """Menu d'edition des proprietes avancees - Affichage VERTICAL."""
        while True:
            self.afficher_section("EDITION AVANCEE")

            print("\n  1. Modifier le point d'entree (RVA)")
            print("  2. Modifier l'ImageBase")
            print("  3. Modifier l'horodatage")
            print("  4. Retour au menu principal")
            print()

            choix = input("Votre choix (1-4): ").strip()

            if choix == '1':
                self.modifier_point_entree()
            elif choix == '2':
                self.modifier_image_base()
            elif choix == '3':
                self.modifier_horodatage()
            elif choix == '4':
                break
            else:
                self.afficher_erreur("Choix invalide")

    def menu_injection(self):
        """Menu d'injection de code et shellcode - Affichage VERTICAL."""
        while True:
            self.afficher_section("INJECTION / PATCH")

            print("\n  1. Injecter du code dans une section")
            print("  2. Ajouter un overlay")
            print("  3. Extraire l'overlay")
            print("  4. Retour au menu principal")
            print()

            choix = input("Votre choix (1-4): ").strip()

            if choix == '1':
                self.injecter_code()
            elif choix == '2':
                self.ajouter_overlay()
            elif choix == '3':
                self.extraire_overlay()
            elif choix == '4':
                break
            else:
                self.afficher_erreur("Choix invalide")

    def menu_securite(self):
        """Menu de gestion des protections - Affichage VERTICAL."""
        while True:
            self.afficher_section("PROTECTIONS")

            # Afficher l'etat actuel des protections avec couleurs
            dllchar = self.pe.OPTIONAL_HEADER.DllCharacteristics
            aslr = "ACTIVE" if dllchar & 0x0040 else "INACTIVE"
            dep = "ACTIVE" if dllchar & 0x0100 else "INACTIVE"
            cfg = "ACTIVE" if dllchar & 0x4000 else "INACTIVE"

            # Colorer l'etat des protections
            aslr_couleur = Config.COLORS['green'] if dllchar & 0x0040 else Config.COLORS['red']
            dep_couleur = Config.COLORS['green'] if dllchar & 0x0100 else Config.COLORS['red']
            cfg_couleur = Config.COLORS['green'] if dllchar & 0x4000 else Config.COLORS['red']

            print(f"\nEtat des protections:")
            print(f"  {aslr_couleur}ASLR = {aslr}{Config.COLORS['reset']}")
            print(f"  {dep_couleur}DEP  = {dep}{Config.COLORS['reset']}")
            print(f"  {cfg_couleur}CFG  = {cfg}{Config.COLORS['reset']}")

            print("\n  1. Desactiver ASLR")
            print("  2. Activer ASLR")
            print("  3. Desactiver DEP")
            print("  4. Activer DEP")
            print("  5. Desactiver CFG")
            print("  6. Activer CFG")
            print("  7. Retour au menu principal")
            print()

            choix = input("Votre choix (1-7): ").strip()

            if choix == '1':
                self.pe.OPTIONAL_HEADER.DllCharacteristics &= ~0x0040
                self.afficher_succes("ASLR desactive")
                self.modifications.append("Desactivation ASLR")
            elif choix == '2':
                self.pe.OPTIONAL_HEADER.DllCharacteristics |= 0x0040
                self.afficher_succes("ASLR active")
                self.modifications.append("Activation ASLR")
            elif choix == '3':
                self.pe.OPTIONAL_HEADER.DllCharacteristics &= ~0x0100
                self.afficher_succes("DEP desactivee")
                self.modifications.append("Desactivation DEP")
            elif choix == '4':
                self.pe.OPTIONAL_HEADER.DllCharacteristics |= 0x0100
                self.afficher_succes("DEP activee")
                self.modifications.append("Activation DEP")
            elif choix == '5':
                self.pe.OPTIONAL_HEADER.DllCharacteristics &= ~0x4000
                self.afficher_succes("CFG desactive")
                self.modifications.append("Desactivation CFG")
            elif choix == '6':
                self.pe.OPTIONAL_HEADER.DllCharacteristics |= 0x4000
                self.afficher_succes("CFG active")
                self.modifications.append("Activation CFG")
            elif choix == '7':
                break
            else:
                self.afficher_erreur("Choix invalide")

    # ============================================================================
    # SECTION 5: FONCTIONS D'EDITION SPECIFIQUES
    # ============================================================================

    def voir_section(self):
        """Affiche les details complets d'une section."""
        self._afficher_sections()
        try:
            idx = int(input("\nNumero de la section a analyser: ").strip().strip('"').strip("'"))
            if 0 <= idx < len(self.pe.sections):
                section = self.pe.sections[idx]
                nom = section.Name.decode("utf-8", "replace").rstrip("\x00")

                self.afficher_section(f"DETAILS SECTION [{nom}]")

                print(f"\nNom                  : {nom}")
                print(f"Virtual Address      : {hex(section.VirtualAddress)}")
                print(f"Virtual Size         : {self._human_size(section.Misc_VirtualSize)}")
                print(f"Raw Pointer          : {hex(section.PointerToRawData)}")
                print(f"Raw Size             : {self._human_size(section.SizeOfRawData)}")

                data = section.get_data()
                entropie = self._calculer_entropie(data)
                print(f"Entropie (Shannon)   : {entropie:.3f}")
                print(f"SHA-256              : {hashlib.sha256(data).hexdigest()}")

                # Afficher un apercu hex
                print(f"\nApercu des donnees (premiers 64 octets):")
                self.afficher_hex_dump(data[:64])

        except ValueError:
            self.afficher_erreur("Numero invalide")

    def modifier_droits_section(self):
        """Modifie les droits d'acces (R/W/X) d'une section avec affichage colore."""
        self._afficher_sections()
        try:
            idx = int(input("\nNumero de la section: ").strip().strip('"').strip("'"))
            if 0 <= idx < len(self.pe.sections):
                section = self.pe.sections[idx]
                nom = section.Name.decode("utf-8", "replace").rstrip("\x00")

                couleur_cyan = Config.COLORS['cyan']
                print(f"\n{couleur_cyan}[MODIFICATION DROITS]{Config.COLORS['reset']} Section: {nom}")

                read = input("Lecture (R) activee? (o/n): ").lower() == 'o'
                write = input("Ecriture (W) activee? (o/n): ").lower() == 'o'
                execute = input("Execution (X) activee? (o/n): ").lower() == 'o'

                anciens = section.Characteristics
                section.Characteristics = 0
                if read: section.Characteristics |= 0x40000000
                if write: section.Characteristics |= 0x80000000
                if execute: section.Characteristics |= 0x20000000

                # Affichage colorise des droits
                droits_str = f"{'R' if read else '-'}{'W' if write else '-'}{'X' if execute else '-'}"
                couleur_yellow = Config.COLORS['yellow']
                couleur_green = Config.COLORS['green']
                print(f"{couleur_yellow}[NOUVEAU]{Config.COLORS['reset']} Droits: {couleur_green}{droits_str}{Config.COLORS['reset']}")

                self.afficher_succes(f"Droits de {nom} modifies avec succes")
                self.modifications.append(f"DROITS [{nom}]: 0x{anciens:08x} -> 0x{section.Characteristics:08x}")

        except ValueError:
            self.afficher_erreur("Numero invalide")

    def exporter_section(self):
        """Exporte le contenu d'une section vers un fichier."""
        self._afficher_sections()
        try:
            idx = int(input("\nNumero de section a exporter: ").strip().strip('"').strip("'"))
            if 0 <= idx < len(self.pe.sections):
                section = self.pe.sections[idx]
                nom = section.Name.decode("utf-8", "replace").rstrip("\x00")
                chemin = input("Fichier de destination: ").strip().strip('"').strip("'")

                data = section.get_data()
                with open(chemin, "wb") as f:
                    f.write(data)

                self.afficher_succes(f"Section {nom} exportee dans {chemin}")

        except ValueError:
            self.afficher_erreur("Numero invalide")
        except Exception as e:
            self.afficher_erreur(f"Erreur: {e}")

    def modifier_point_entree(self):
        """Modifie l'adresse du point d'entree (RVA) avec confirmation colorisee."""
        ancien = self.pe.OPTIONAL_HEADER.AddressOfEntryPoint

        couleur_blue = Config.COLORS['blue']
        print(f"\n{couleur_blue}[CURRENT]{Config.COLORS['reset']} Point d'entree: {hex(ancien)}")

        nouveau = input("Nouvelle RVA (hex, ex: 0x1000): ").strip().strip('"').strip("'")
        try:
            if nouveau.startswith('0x'):
                nouveau_rva = int(nouveau, 16)
            else:
                nouveau_rva = int(nouveau, 0)

            self.pe.OPTIONAL_HEADER.AddressOfEntryPoint = nouveau_rva

            # Affichage colorise du changement
            couleur_yellow = Config.COLORS['yellow']
            couleur_green = Config.COLORS['green']
            print(f"{couleur_yellow}[MODIFICATION]{Config.COLORS['reset']} {hex(ancien)} {couleur_yellow}-->{Config.COLORS['reset']} {couleur_green}{hex(nouveau_rva)}{Config.COLORS['reset']}")

            self.afficher_succes(f"Point d'entree modifie avec succes")
            self.modifications.append(f"ENTRY POINT: {hex(ancien)} -> {hex(nouveau_rva)}")

        except ValueError:
            self.afficher_erreur("RVA invalide")

    def modifier_image_base(self):
        """Modifie l'adresse de base du PE (ImageBase) avec confirmation colorisee."""
        ancien = self.pe.OPTIONAL_HEADER.ImageBase

        couleur_blue = Config.COLORS['blue']
        print(f"\n{couleur_blue}[CURRENT]{Config.COLORS['reset']} ImageBase: {hex(ancien)}")

        nouveau = input("Nouvelle ImageBase (hex): ").strip().strip('"').strip("'")
        try:
            if nouveau.startswith('0x'):
                nouvelle_base = int(nouveau, 16)
            else:
                nouvelle_base = int(nouveau, 0)

            self.pe.OPTIONAL_HEADER.ImageBase = nouvelle_base

            # Affichage colorise du changement
            couleur_yellow = Config.COLORS['yellow']
            couleur_green = Config.COLORS['green']
            print(f"{couleur_yellow}[MODIFICATION]{Config.COLORS['reset']} {hex(ancien)} {couleur_yellow}-->{Config.COLORS['reset']} {couleur_green}{hex(nouvelle_base)}{Config.COLORS['reset']}")

            self.afficher_succes(f"ImageBase modifiee avec succes")
            self.modifications.append(f"IMAGEBASE: {hex(ancien)} -> {hex(nouvelle_base)}")

        except ValueError:
            self.afficher_erreur("Adresse invalide")

    def modifier_horodatage(self):
        """Modifie la date/heure de compilation du PE avec affichage colore."""
        couleur_blue = Config.COLORS['blue']

        try:
            actuel = datetime.fromtimestamp(self.pe.FILE_HEADER.TimeDateStamp, tz=timezone.utc)
            print(f"\n{couleur_blue}[CURRENT]{Config.COLORS['reset']} Date de compilation: {actuel.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        except:
            print(f"\n{couleur_blue}[CURRENT]{Config.COLORS['reset']} Date invalide ou non definie")

        date_str = input("Nouvelle date (YYYY-MM-DD HH:MM:SS) ou 'now': ").strip().strip('"').strip("'")

        try:
            if date_str.lower() == 'now':
                nouvelle_date = datetime.now(timezone.utc)
            else:
                nouvelle_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                nouvelle_date = nouvelle_date.replace(tzinfo=timezone.utc)

            timestamp = int(nouvelle_date.timestamp())
            self.pe.FILE_HEADER.TimeDateStamp = timestamp

            # Affichage colorise
            couleur_yellow = Config.COLORS['yellow']
            couleur_green = Config.COLORS['green']
            print(f"{couleur_yellow}[MODIFICATION]{Config.COLORS['reset']} {couleur_green}{nouvelle_date.strftime('%Y-%m-%d %H:%M:%S UTC')}{Config.COLORS['reset']}")

            self.afficher_succes(f"Horodatage modifie avec succes")
            self.modifications.append(f"HORODATAGE: {nouvelle_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")

        except ValueError:
            self.afficher_erreur("Format de date invalide")

    def injecter_code(self):
        """Injecte du code (fichier ou shellcode) dans une section."""
        self.afficher_section("INJECTION DE CODE")

        print("\n  1. Fichier binaire")
        print("  2. Shellcode de test")

        choix = input("\nType a injecter (1-2): ").strip()

        if choix == '1':
            chemin = input("Chemin du fichier: ").strip().strip('"').strip("'")
            try:
                with open(chemin, "rb") as f:
                    code = f.read()
            except:
                self.afficher_erreur("Fichier introuvable")
                return
        elif choix == '2':
            code = self._generer_shellcode()
        else:
            self.afficher_erreur("Choix invalide")
            return

        self._afficher_sections()
        try:
            idx = int(input("\nNumero de section cible: ").strip().strip('"').strip("'"))
            if 0 <= idx < len(self.pe.sections):
                section = self.pe.sections[idx]
                offset = input("Offset dans la section (hex): ").strip().strip('"').strip("'")

                try:
                    if offset.startswith('0x'):
                        offset_int = int(offset, 16)
                    else:
                        offset_int = int(offset, 0)

                    pos = section.PointerToRawData + offset_int
                    self.donnees_brutes[pos:pos + len(code)] = code
                    self.afficher_succes(f"Code injecte ({len(code)} octets)")
                    self.modifications.append(f"Injection dans section {idx} a offset {hex(offset_int)}")

                except ValueError:
                    self.afficher_erreur("Offset invalide")

        except ValueError:
            self.afficher_erreur("Numero invalide")

    def ajouter_overlay(self):
        """Ajoute un fichier comme overlay (apres le PE)."""
        source = input("Fichier source: ").strip().strip('"').strip("'")

        try:
            with open(source, "rb") as f:
                data = f.read()

            self.donnees_brutes = bytearray(self.pe.write()) + data
            self.afficher_succes(f"Overlay ajoute ({self._human_size(len(data))})")
            self.modifications.append(f"Overlay: {source} ({len(data)} octets)")

        except Exception as e:
            self.afficher_erreur(f"Erreur: {e}")

    def extraire_overlay(self):
        """Extrait l'overlay vers un fichier."""
        try:
            debut = self.pe.get_overlay_data_start_offset()
            if debut is None or debut >= len(self.donnees_brutes):
                self.afficher_erreur("Aucun overlay detecte")
                return

            overlay = self.donnees_brutes[debut:]
            chemin = input("Fichier de sortie: ").strip().strip('"').strip("'") or "overlay.bin"

            with open(chemin, "wb") as f:
                f.write(overlay)

            self.afficher_succes(f"Overlay extrait dans {chemin}")

        except Exception as e:
            self.afficher_erreur(f"Erreur: {e}")

    def afficher_journal(self):
        """Affiche l'historique de toutes les modifications effectuees."""
        self.afficher_section("JOURNAL DES MODIFICATIONS")

        if not self.modifications:
            self.afficher_info("Aucune modification enregistree")
            return

        entetes = ["NUM", "MODIFICATION"]
        lignes = [[str(i+1), mod] for i, mod in enumerate(self.modifications)]
        self.afficher_tableau(entetes, lignes)

    # ============================================================================
    # SECTION 6: UTILITAIRES INTERNES
    # ============================================================================

    def _human_size(self, size: int) -> str:
        """Convertit une taille en bytes en format lisible (Ko, Mo, Go)."""
        for unite in ("B", "KB", "MB", "GB"):
            if abs(size) < 1024.0:
                return f"{size:.1f} {unite}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def _calculer_entropie(self, data: bytes) -> float:
        """
        Calcule l'entropie de Shannon d'une sequence de donnees.

        Entropie haute (proche de 8) = donnees aleatoires/compressees
        Entropie basse (proche de 0) = donnees repetitives/texte
        """
        if not data:
            return 0.0

        occurrences = [0] * 256
        for octet in data:
            occurrences[octet] += 1

        entropie = 0.0
        longueur = len(data)
        for compte in occurrences:
            if compte:
                p = compte / longueur
                entropie -= p * math.log2(p)

        return entropie

    def _generer_shellcode(self) -> bytes:
        """Genere un shellcode de test simple."""
        return b"\x90" * 32  # 32 instructions NOP (no operation)

    def afficher_hex_dump(self, data: bytes, bytes_per_line: int = 16):
        """
        Affiche les donnees en format hexadecimal lisible.

        Format:
        00000000: 48 89 e5 48 83 ec 10 48 89 7d f8 48 89 75 f0 90  H..H...H.}H.Hu..
        """
        for i in range(0, len(data), bytes_per_line):
            chunk = data[i:i + bytes_per_line]
            hex_str = " ".join(f"{b:02x}" for b in chunk)
            ascii_str = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
            print(f"  {i:08x}: {hex_str:<48} {ascii_str}")


# # FONCTION PRINCIPALE - POINT D'ENTREE DE L'APPLICATION
# 
def main():
    """
    Point d'entree principal de l'application.

    Mode d'execution:
    1. Avec argument: ouvre directement le fichier fourni
    2. Sans argument: mode selection interactif
    """
    print("=" * 100)
    print("PE  - Analyseur et Editeur de Fichiers Portable Executable".center(100))
    print("=" * 100)

    # Mode ligne de commande avec argument
    if len(sys.argv) > 1:
        fichier = sys.argv[1]
        if os.path.exists(fichier):
            pe = PE(fichier)
            pe.menu_principal()
        else:
            print(f"[ERREUR] Fichier introuvable: {fichier}")
        return

    # Mode interactif sans argument
    print("\n[MODE SELECTION DE FICHIER]")
    print("Fichiers PE detectes dans le dossier courant:\n")

    fichiers = [f for f in os.listdir(".") if f.lower().endswith((".exe", ".dll"))]

    if fichiers:
        for i, f in enumerate(fichiers, 1):
            taille = os.path.getsize(f)
            print(f"  {i}. {f:<40} ({taille:,} bytes)")

        print("\nOptions:")
        print("  - Entrez le numero du fichier (1-{})".format(len(fichiers)))
        print("  - Entrez le chemin complet d'un fichier")
        print("  - Entrez 'q' pour quitter")

        choix = input("\nVotre choix: ").strip().strip('"').strip("'")

        if choix.lower() == 'q':
            print("Au revoir!")
            return

        try:
            idx = int(choix) - 1
            if 0 <= idx < len(fichiers):
                pe = PE(fichiers[idx])
                pe.menu_principal()
            else:
                print("[ERREUR] Numero invalide")
        except ValueError:
            if os.path.exists(choix):
                pe = PE(choix)
                pe.menu_principal()
            else:
                print("[ERREUR] Fichier introuvable")
    else:
        chemin = input("\n[MODE MANUEL]\nChemin complet du fichier PE: ").strip().strip('"').strip("'")
        if chemin and os.path.exists(chemin):
            pe = PE(chemin)
            pe.menu_principal()
        else:
            print("[ERREUR] Chemin invalide")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTION] Programme arrete par l'utilisateur")
    except Exception as e:
        print(f"\n[ERREUR CRITIQUE] {e}")
        import traceback
        traceback.print_exc()
