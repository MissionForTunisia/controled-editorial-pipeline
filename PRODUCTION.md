# MANIFESTE DE PRODUCTION CONTRÔLÉE

Projet : `QUELLE SOCIÉTÉ APRÈS L’IA ?`

## Sources de vérité

| Rôle | Source | Autorité |
|---|---|---|
| CONTENT_SOURCE | `QUELLE SOCIÉTÉ APRÈS LIA  -draft.pdf` (73 p.) | seule autorité éditoriale (fond) |
| VISUAL_SOURCE | `tets2.pdf` (49 p., A5) | référence de direction artistique uniquement |
| PROCESS_SOURCE | README.md de ce dépôt | workflow : extraction → DA → composition → compilation → inspection → correction |

## Métadonnées finales

* FINAL_TITLE : `QUELLE SOCIÉTÉ APRÈS L’IA ?`
* SUBTITLE : `Travail, intelligence, pouvoir et société à l’ère de l’intelligence artificielle`
* AUTHOR CREDIT : `S. Noussair & GLM 5.1`
* DESIGN CREDIT : `S. Dhafer & Prism`
* BOOK TYPE : `Essai prospectif contemporain`

## Audit de la source de contenu (SOURCE A)

* p. 1–9 : matériel de production (ÉTAPE 0, architecture, estimations, CHECKPOINT 0) → **non publié**
* p. 10–64 : manuscrit lisible par le lecteur (Préface → Bibliographie) → **publié intégralement**
  * blocs de production interleavés à retirer : têtes `ÉTAPE n`, `CHECKPOINT n` (résumés, estimations de mots, « J’attends votre instruction »)
* p. 65–69 : CHECKPOINT 6 + ÉTAPE 7 (audit) → **non publié** (note toutefois 6 corrections à appliquer)
* p. 70–73 : ÉTAPE 8 — **corrections finales définies par l’auteur**, à appliquer lors de la transcription :
  1. fusion des balises `Fait : / Hypothèse : / Observation : / Interprétation :` dans la prose
  2. variation de la formulation répétée de la thèse (rareté → abondance), chap. 3 et 6
  3. analogie archiviste / stagiaire ajoutée au chapitre 4
  4. paragraphe de transition « pendant systémique » ajouté en fin du chapitre 9
  5. ancrages d’actualité : Hollywood 2023 (chap. 7), robocalls 2024 (chap. 12)
  6. étude OpenAI 2023 citée au chap. 7 + entrée Eloundou et al. (2023) en bibliographie

## Cartographie structurelle (publiée)

Cover → Page de titre → Épigraphe → Préface courte → Table des matières →
Introduction (Le matin ordinaire) →
Partie I (ch. 1–3) → Partie II (ch. 4–6) → Partie III (ch. 7–10) → Partie IV (ch. 11–13) → Partie V (ch. 14–15) →
Conclusion (L’après n’est pas un endroit) → Dix questions pour demain → Épilogue (L’humain après l’IA) →
Bibliographie sélective et commentée.

## Direction artistique (dérivée de SOURCE B, palette imposée)

* Navy `#0A1128`, cyan lumineux `#00D9FF`, cyan secondaire `#00B4D8`, indigo `#4361EE`, typo blanche sur fond sombre.
* Intercalaires de partie : pleine page navy, grille fine, constellation minimale, accent cyan.
* Ouvertures de chapitre : grand numéro pâle, titre navy, filet cyan.
* Boîtes : `aiquote` (citation, filet/cadre cyan fin), `conceptbox` (concepts du manuscrit), `scenariobox` (scénarios A/B/C, traitement égal).
* A5, pdfLaTeX, babel[french], T1, microtype, lmodern + sourcesanspro.

## Portes de validation

A. CONTENU — toutes les sections présentes, aucun bloc de production fugitif, corrections d’auteur appliquées.
B. ÉDITORIAL — typographie française (guillemets, espaces insécables, apostrophes), hiérarchie des titres, artéfacts d’extraction corrigés.
C. LATEX — `pdflatex -interaction=nonstopmode -halt-on-error` ×3 passes, TOC/bookmarks résolus.
D. LOGS — zéro erreur ; revue des overfull/underfull, warnings fancyhdr/TikZ/références.
E. VISUEL — rendu PNG et inspection : couverture, titre, épigraphe, TdM, intercalaires, ouvertures de chapitre, prose, boîtes, conclusion, questions, épilogue, bibliographie, dernière page.

## Artefacts

* Livrable final : `QUELLE_SOCIETE_APRES_L_IA_FINAL.pdf`
* Sources : `book/main.tex`, `book/design/`, `book/content/`
* QA : rendus sous `qa/` (non versionnés à l’infini, jeu de contrôle conservé)
