# PE BEAR - Questions & Réponses (FAQ)

## Questions Fréquemment Posées

---

## Q1: Qu'est-ce qu'un fichier PE (Portable Executable)?

**R:** Un PE est le format exécutable standard sous Windows. Il contient:
- **DOS Header** - Compatibilité avec MS-DOS 2.0
- **PE Signature** - Identificateur "PE\0\0"
- **FILE Header** - Infos générales (architecture, sections)
- **OPTIONAL Header** - Infos d'exécution (entry point, ImageBase)
- **Sections** - Code, données, ressources, relocations
- **Ressources** - Icônes, chaînes, dialogues

**Format:** Binaire structuré, éditable avec outils hex ou parsers

---

## Q2: Qu'est-ce que l'entropie Shannon en cybersécurité?

**R:** L'entropie mesure le "bruit" d'une section:

`
Entropie = -Σ(P(byte) * log2(P(byte)))
`

**Interprétation:**
- **0-1** - Texte clair, très prévisible
- **1-2** - Texte normal, données
- **4-5** - Code exécutable moyen
- **6-7** - Données compressées/obfusquées
- **7-8** - Chiffrement, compression maximale

**Utilisation:** Détecter des payloads cachés dans le code

---

## Q3: Comment modifier un Point d'Entrée (Entry Point)?

**R:** Étapes:

1. Charger le PE
2. Afficher l'EP actuel (adresse RVA hexadécimale)
3. Choisir une nouvelle adresse (doit pointer du code valide)
4. Sauvegarder et vérifier dans un débogueur

**Attention:** 
- Une adresse invalide = crash au démarrage
- À utiliser en testing/reverse engineering uniquement

---

## Q4: Qu'est-ce qu'ImageBase?

**R:** L'adresse mémoire préférée pour charger le PE. Typiquement:
- **0x400000** - Applications 32-bit
- **0x140000000** - Applications 64-bit

**ASLR (Address Space Layout Randomization):**
- Désactiver ImageBase fixe = adresse aléatoire à chaque lancement
- Protection moderne pour prévenir les exploits

---

## Q5: Qu'est-ce qu'une section ".text"?

**R:** Contient le code machine exécutable. Propriétés:
- **Droits:** R-X (Lecture + Exécution)
- **Entropie:** Généralement 5-7 (code variable)
- **Autres sections:** .data (données), .rsrc (ressources), .reloc (relocations)

---

## Q6: Qu'est-ce qu'un overlay?

**R:** Données après le dernier secteur PE mappé. Utilisations:
- Données cachées supplémentaires
- Ressources comprimées
- **Malware:** Pour cacher du code supplémentaire

**Détection:** Comparer la taille fichier vs taille PE déclarée

---

## Q7: Qu'est-ce qu'un TLS Callback?

**R:** Fonction appelée AVANT le point d'entrée principal. Utilisation légitime:
- Protection anti-debugging
- Initialisation spécialisée

**Malware:** Pour exécuter du code de contrôle avant même que le main s'exécute

---

## Q8: Qu'est-ce que la signature numérique?

**R:** Certificat vérifiant l'authenticité du PE:
- **Signé:** Éditeur connu, traçable
- **Non signé:** Inconnu, risqué
- **Révoqué:** Signature compromise

**Marque:** Affiche l'éditeur dans les propriétés Windows

---

## Q9: Comment les imports/exports fonctionnent?

**R:** 
- **Imports:** Fonctions que ce PE utilise d'autres DLL
  - Exemple: KERNEL32.CreateFileA → Créer un fichier
  
- **Exports:** Fonctions que ce PE offre à d'autres
  - Exemple: DLL graphique expose DrawPixel()

**Table d'adresses:** Résolue au chargement par le système

---

## Q10: Qu'est-ce qu'une relocation?

**R:** Adresse nécessitant ajustement si le PE charge à une adresse différente.

**ASLR active:** Toutes les adresses absolues sont relocalisées
**ASLR inactif:** ImageBase fixe = pas de relocalisation

---

## Q11: Peut-on patcher un PE sans le corrompre?

**R:** Oui, si:
- ✅ Les sections restent alignées
- ✅ Les tailles ne changent pas (ou shrink)
- ✅ Le checksum est recalculé
- ✅ Les relocations sont mises à jour

**Notre outil:** Recalcule automatiquement

---

## Q12: Qu'est-ce que DEP (Data Execution Prevention)?

**R:** Protection Windows interdisant l'exécution depuis le heap/stack.

**Usage:**
- **Activé (vert)** - Sécurisé, recommandé
- **Désactivé (rouge)** - Vulnérable, testing uniquement

**Flag PE:** DLLCHARACTERISTICS_NX_COMPAT (0x0100)

---

## Q13: Qu'est-ce que CFG (Control Flow Guard)?

**R:** Protection avancée contre les exploits de redirection d'exécution.

**Support:**
- Windows 8.1+
- Compilateurs MSVC récents
- **Flag PE:** 0x4000

---

## Q14: Comment détecter les ressources?

**R:** Types courants:
- **RT_ICON (3)** - Icônes
- **RT_DIALOG (5)** - Dialogues UI
- **RT_STRING (6)** - Chaînes de texte
- **RT_BITMAP (2)** - Bitmaps
- **RT_VERSION (16)** - Infos version

**Malware:** Ressources anormales = comportement suspect

---

## Q15: Qu'est-ce qu'une relocalisation par base?

**R:** Ajustement global de toutes les adresses absolues.

`
Nouvelle_adresse = Ancienne_adresse + (ImageBase_reel - ImageBase_ideal)
`

**Automatique:** À chaque chargement si ASLR actif

---

## Q16: Comment calcule-t-on SHA-256 d'une section?

**R:** 
1. Lire les données brutes de la section
2. Appliquer l'algorithme SHA-256
3. Afficher en hexadécimal

**Usage:** Vérifier l'intégrité d'une section lors des modifications

---

## Q17: Qu'est-ce qu'une relocalisation d'importation?

**R:** Adresse d'une fonction importée qui nécessite une relocalisation.

**Processus:**
1. PE charge à adresse X
2. Calcule offset = X - ImageBase
3. Applique offset à chaque relocalisation d'import
4. Fonction importée resolue à adresse correcte

---

## Q18: Peut-on injecter du code dans le .text?

**R:** ⚠️ Risky mais possible:
- ✅ Injecter dans .text (exécutable)
- ✅ Modifier l'Entry Point pour sauter au code injecté
- ❌ Ne pas le faire sans faire sauter vers le vrai main après

**Séquence:**
1. Injecter shellcode dans .text
2. Changer EP vers shellcode
3. Shellcode fait JMP vers le vrai main
4. Contrôle rétabli

---

## Q19: Qu'est-ce que la subsomption de code?

**R:** Technique d'optimisation où du code petit s'insère dans un espace libre.

**Dans PE BEAR:** "Espace libre" entre sections = optimal pour injection

---

## Q20: Comment bypasser les protections?

**R:** ⚠️ **Pour testing seulement (dans un sandbox!)**

**Techniques légitime:**
- Désactiver DEP (DLLCHARACTERISTICS_NX_COMPAT)
- Désactiver ASLR (DLL_DYNAMIC_BASE)
- Désactiver CFG
- Tester dans un environnement isolé

**À NE JAMAIS faire:**
- Modifier les exécutables système
- Désactiver sur des serveurs production
- Bypasser pour distribuer des malwares

---

## Q21: Qu'est-ce qu'une IAT (Import Address Table)?

**R:** Table contenant les adresses des fonctions importées.

**Processus:**
1. Loader charge les DLL
2. Résout les symboles
3. Remplit l'IAT avec les adresses
4. Code utilise l'IAT pour appeler les fonctions

**Sécurité:** IAT hooks = détection par antivirus

---

## Q22: Comment détecter des malwares?

**R:** Signes suspects:

1. **Entropie élevée** dans les sections (chiffrement?)
2. **Overlay non vide** (données cachées?)
3. **Signatures nulles** (non signé = suspect)
4. **Imports anormaux** (CreateRemoteThread, SetWindowsHookEx?)
5. **TLS callbacks** (code avant main)
6. **Section suspecte** (.packed, .upx, .aspack)

---

## Q23: Qu'est-ce qu'UPX (Ultimate Packer)?

**R:** Compresseur de PE courant. Signe:

`
Sections: .upx0, .upx1
Entropie: Élevée (données comprimées)
`

**Légitime:** Réduction de taille
**Malware:** Obfusquer le code

---

## Q24: Comment fonctionne l'obfuscation PE?

**R:** Techniques:

1. **Packing** - Compresser le code (UPX, ASPack)
2. **Cryptage** - Chiffrer les sections
3. **Code splitting** - Éparpiller le code
4. **Junk code** - Ajouter du code inutile
5. **Redirection** - Modifier les imports

**Détection:** Entropie haute + signature basse

---

## Q25: Peut-on défaire du code packé?

**R:** ⚠️ Technique avancée:

**Unpacking (décompression):**
1. Laisser le packer décompresser en mémoire
2. Dumper la mémoire avec un debugger
3. Analyser le code décompressé

**Légalité:** Dépend du contexte (reverse engineering légal vs. malware)

---

## Dépannage

### Problème: "Impossible de charger le fichier"

**Solutions:**
- Vérifier que le fichier existe
- Vérifier les permissions (lecture)
- Vérifier que c'est un vrai PE (e_magic = "MZ")

### Problème: "Entropie incorrecte"

**Solutions:**
- Vérifier la taille de la section
- Vérifier les données brutes
- Recalculer si corrompu

### Problème: "Erreur de sauvegarde"

**Solutions:**
- Vérifier l'espace disque
- Vérifier les permissions (écriture)
- Fermer les éditeurs hex ouverts sur le fichier

---

**Dernière mise à jour:** 27 Août 2026  
**Version:** 2.0.0
