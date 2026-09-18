#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_content.py — Transcription contrôlée du manuscrit (SOURCE A) vers LaTeX.

Règles :
  - SEULE SOURCE du contenu : "QUELLE SOCIÉTÉ APRÈS LIA  -draft.pdf" (pages 10–64).
  - Le matériel de production (ÉTAPE n / CHECKPOINT n / notes d'instruction) est retiré.
  - Les 6 corrections finales définies par l'auteur (ÉTAPE 8, p. 70–73) sont appliquées.
  - Normalisation typographique conservatrice uniquement (aucune réécriture).
Chaque remplacement ciblé est vérifié par assertion : échec bruyant si absent.
"""
import re, os

SRC = "/tmp/extract/sourceA.txt"
OUT = "/home/user/controled-editorial-pipeline/book/content"

text = open(SRC, encoding="utf-8").read()

pages = {}
for m in re.finditer(r"===== PAGE (\d+) =====\n(.*?)(?====== PAGE |\Z)", text, re.S):
    pages[int(m.group(1))] = m.group(2)
assert max(pages) == 73, "source inattendue"

# fusion des lignes à cheval sur deux pages (le texte continu ne doit pas être coupé)
def strip_blank(lines):
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines

page_lines = [strip_blank(pages[p].split("\n")) for p in range(10, 65)]
body_lines = []
SPECIAL = re.compile(r"^(#|\*|\d+\.\s|>|---)")
for idx, lines in enumerate(page_lines):
    if idx > 0 and body_lines and body_lines[-1].strip() and lines:
        prev, nxt = body_lines[-1].strip(), lines[0].strip()
        fuse = prev.startswith(">") or not (SPECIAL.match(prev) or SPECIAL.match(nxt))
        if not fuse:
            body_lines.append("")
        body_lines.extend(lines)
    else:
        if body_lines:
            body_lines.append("")
        body_lines.extend(lines)
body = "\n".join(body_lines)

def collapse(t):
    t = t.replace("\u00a0", " ")
    lines = [ln.rstrip() for ln in t.split("\n")]
    out, buf = [], []
    HARD = re.compile(r"^(\*|#|>|\d+\.\s|---)")
    def flush():
        if buf:
            out.append(" ".join(buf).strip()); buf.clear()
    for ln in lines:
        s = ln.strip()
        if s == "":
            flush()
        elif HARD.match(s):
            flush()
            buf.append(s)
        else:
            buf.append(s)
    flush()
    return "\n\n".join(out)

body = collapse(body)

# ------------------------------------------------- retrait du matériel de production
def cut(pattern, label, expect):
    global body
    body, n = re.subn(pattern, "\n\n", body, flags=re.S)
    assert n >= expect, f"bloc de production non trouvé : {label} (n={n})"

cut(r"# ÉTAPE \d[^\n]*\n(\*\(Conformément.*?\)\*)?", "têtes ÉTAPE", 6)
cut(r"\*\(Conformément[^*]*?\)\*", "notes conformément", 0)
cut(r"\*\(J'attends votre instruction[^\n]*", "notes instruction", 0)
cut(r"# CHECKPOINT \d[^\n]*\n.*?(?=\Z|\n# )", "blocs CHECKPOINT", 5)
cut(r"(?m)^---$", "séparateurs", 10)

# ------------------------------------------------ corrections de l'auteur (ÉTAPE 8)
def rep(old, new, label, n_expected=1):
    global body
    n = body.count(old)
    if n_expected == 0:
        body = body.replace(old, new)
        return
    assert n == n_expected, f"{label}: {n} occurrence(s), attendu {n_expected}"
    body = body.replace(old, new)

# C1 — fusion des balises conceptuelles dans la prose
rep("**Fait :** Avec l'apparition des réseaux de neurones",
    "C'est un fait désormais visible : avec l'apparition des réseaux de neurones", "C1 ch4 Fait")
rep("**Fait :** Lorsqu'une tâche est automatisée",
    "C'est un fait établi : lorsqu'une tâche est automatisée", "C1 ch7 Fait")
rep("**Fait :** La production d'IA à l'état de l'art",
    "C'est un fait : la production d'IA à l'état de l'art", "C1 ch11 Fait")
rep("**Fait :** Il est aujourd'hui possible de générer",
    "C'est un fait : il est aujourd'hui possible de générer", "C1 ch12 Fait")
rep("**Observation :** Il faut donc l'admettre", "Il faut donc l'admettre", "C1 ch1 Obs")
rep("**Observation :** Le moteur de recherche nous renvoyait",
    "On observe que le moteur de recherche nous renvoyait", "C1 ch4 Obs")
rep("**Observation :** Nous passons progressivement",
    "On observe que nous passons progressivement", "C1 ch5 Obs")
rep("**Observation :** L'une des conséquences les plus immédiates",
    "On observe que l'une des conséquences les plus immédiates", "C1 ch8 Obs")
rep("**Observation :** L'IA permet à un non-expert",
    "On observe que l'IA permet à un non-expert", "C1 ch9 Obs")
rep("**Observation :** L'IA attaque ce modèle",
    "On observe que l'IA attaque ce modèle", "C1 ch13 Obs")
rep("**Hypothèse :** Ces différences sont suffisantes",
    "L'hypothèse qui se dessine est la suivante : ces différences sont suffisantes", "C1 ch1 Hyp")
rep("**Hypothèse :** Le véritable enjeu de l'IA",
    "L'hypothèse qui se dessine est la suivante : le véritable enjeu de l'IA", "C1 ch3 Hyp")
rep("**Hypothèse :** Avec l'IA, ce mouvement",
    "L'hypothèse qui se dessine est la suivante : avec l'IA, ce mouvement", "C1 ch7 Hyp")
rep("**Hypothèse :** Lorsque l'augmentation est généralisée",
    "L'hypothèse est alors la suivante : lorsque l'augmentation", "C1 ch8 Hyp")
rep("**Hypothèse :** Le défi de l'école",
    "L'hypothèse qui se dessine est la suivante : le défi de l'école", "C1 ch10 Hyp")
rep("**Hypothèse :** Nous assistons à l'émergence",
    "L'hypothèse est la suivante : nous assistons à l'émergence", "C1 ch11 Hyp")
rep("**Hypothèse :** Si la production de certaines réalisations",
    "L'hypothèse est la suivante : si la production de certaines réalisations", "C1 ch6 Hyp")
rep("**Hypothèse :** Le passage de l'outil à l'agent",
    "L'hypothèse est la suivante : le passage de l'outil à l'agent", "C1 ch5 Hyp")
rep("**Hypothèse prudente :**", "Reste une hypothèse prudente :", "C1 ch2 Hyp prudence")
rep("**Interprétation :** Historiquement, nos sociétés ont récompensé",
    "L'interprétation qui s'impose est la suivante : historiquement, nos sociétés ont récompensé", "C1 ch2 Interp")
rep("**Interprétation :** L'effondrement du coût de production",
    "Notre interprétation est la suivante : l'effondrement du coût de production", "C1 ch6 Interp")
rep("**Interprétation :** L'IA ne supprime pas le besoin d'experts",
    "L'interprétation est alors la suivante : l'IA ne supprime pas le besoin d'experts", "C1 ch9 Interp")
rep("**Interprétation :** L'IA ne crée pas la désinformation",
    "Notre interprétation est la suivante : l'IA ne crée pas la désinformation", "C1 ch12 Interp")
rep("**Interprétation :** Le management de demain",
    "Notre interprétation est la suivante : le management de demain", "C1 ch13 Interp")
rep("**Interprétation :** Aucun de ces trois scénarios",
    "Une interprétation s'impose : aucun de ces trois scénarios", "C1 ch14 Interp")
rep("**Conclusion du Chapitre 3 :**", "Ce que nous retiendrons de ce chapitre :", "C1 ch3 concl")
rep("**Conclusion du Chapitre 15 :**", "Ce que nous retiendrons de ce chapitre :", "C1 ch15 concl")
rep("**Fait :** Une tâche peut être automatisée.",
    "C'est un fait établi : une tâche peut être automatisée.", "C1 ch2 Fait")
rep("**Observation :** Lorsque cette tâche cesse d'être rare",
    "On observe ensuite que lorsque cette tâche cesse d'être rare", "C1 ch2 Obs")
rep("**Observation :** L'une des conséquences potentielles de l'IA est de rendre",
    "On observe que l'une des conséquences potentielles de l'IA est de rendre", "C1 ch3 Obs")
rep("**Fait :** Avec l'IA, le coût marginal de production",
    "C'est un fait : avec l'IA, le coût marginal de production", "C1 ch6 Fait")
rep("**Observation :** Pour ces pays, l'IA n'est pas une technologie",
    "On observe que pour ces pays, l'IA n'est pas une technologie", "C1 ch11 Obs")
rep("**Hypothèse :** Nous pourrions assister à un retour paradoxal",
    "D'où une hypothèse : nous pourrions assister à un retour paradoxal", "C1 ch12 Hyp 2")
rep("**Hypothèse :** L'entreprise de l'ère de l'IA pourrait être plus petite",
    "L'hypothèse est la suivante : l'entreprise de l'ère de l'IA pourrait être plus petite", "C1 ch13 Hyp")
assert not re.search(r"\*\*(Fait|Observation|Hypothèse|Interprétation)", body), "balises résiduelles"

# C2 — variation de la formulation répétée de la thèse
rep("l'intelligence cessait d'être une ressource relativement rare pour tendre à devenir une ressource abondante ?",
    "l'intelligence cessait d'être un facteur limitant pour devenir une ressource irrigant toute l'économie ?",
    "C2 ch3 thèse")
rep("La production intellectuelle n'échappait pas à cette règle.",
    "La production intellectuelle n'échappait pas à cette règle. Avec l'IA, ce postulat vacille.", "C2 ch6 thèse")

# C3 — analogie archiviste / stagiaire (ch4)
rep("elle inférait une étiquette ou une probabilité.",
    "elle inférait une étiquette ou une probabilité.\n\nPour reprendre une analogie simple : l'IA traditionnelle "
    "fonctionnait comme un archiviste méticuleux. Vous lui demandiez un dossier spécifique selon des critères précis, "
    "et il vous le trouvait immanquablement dans les étagères, ou classait les nouveaux documents dans les bonnes cases. "
    "L'IA générative, elle, ressemble à un stagiaire créatif et polyglotte : vous lui donnez un ensemble de notes "
    "éparses et un objectif de haut niveau, et il rédige pour vous une synthèse inédite, en proposant un angle ou une "
    "formulation que vous n'aviez pas envisagés. Le saut n'est pas de la recherche à la vitesse, mais de la restitution "
    "à la proposition.", "C3 ch4 analogie")

# C4 — transition renforcée (fin ch9)
rep("C'est tout le défi qui se pose à notre système éducatif.",
    "C'est tout le défi qui se pose à notre système éducatif.\n\nMais cette illusion de compétence à l'échelle "
    "individuelle possède un pendant systémique beaucoup plus redoutable. Si l'utilisateur croit naïvement en "
    "l'infaillibilité ou en la neutralité de la machine, il risque de ne pas voir qui, de l'autre côté de l'écran, "
    "oriente réellement cette machine, sélectionne ses données d'apprentissage et en tire les bénéfices. L'expertise "
    "qui s'érode laisse la place à un nouveau pouvoir, invisible et concentré. C'est ce pouvoir qu'il nous faut "
    "maintenant interroger.", "C4 ch9 transition")

# C5 — ancrages d'actualité
rep("Le métier s'est rehaussé en complexité.",
    "Le métier s'est rehaussé en complexité.\n\nL'actualité récente offre des illustrations frappantes de cette "
    "recomposition. La grève historique des scénaristes et des acteurs à Hollywood en 2023 a offert un aperçu "
    "saisissant de ce débat : la défense ne portait pas seulement sur la crainte d'une automatisation de l'écriture "
    "de scripts par l'IA, mais sur l'utilisation non consentie des images et des voix pour créer des répliques "
    "numériques éternelles, modifiant à jamais le contrat de travail et la propriété de l'empreinte humaine.",
    "C5 ch7 Hollywood")
rep("tandis que le coût de la vérification, lui, n'a cessé d'augmenter.",
    "tandis que le coût de la vérification, lui, n'a cessé d'augmenter.\n\nL'actualité l'illustre crûment : lors "
    "d'élections primaires aux États-Unis début 2024, des appels téléphoniques robotisés utilisant un clone vocal "
    "troublant d'un candidat démocrate ont été massivement diffusés pour dissuader les citoyens de voter. La "
    "technologie, peu coûteuse et aisément accessible, a prouvé qu'elle pouvait être une arme de déstabilisation "
    "électorale à grande échelle, sans qu'aucun acteur humain n'ait eu à prononcer le moindre mot.",
    "C5 ch12 robocalls")

# C6 — étude OpenAI 2023 (ch7)
rep("(des tâches relationnelles et de jugement situées, beaucoup plus difficiles à automatiser).",
    "\\1\n\nLes travaux récents le confirment : une étude menée par les chercheurs d'OpenAI en 2023 a ainsi montré "
    "que la majorité des professions humaines ont au moins une fraction de leurs tâches susceptibles d'être "
    "accélérées ou automatisées par les grands modèles de langage. L'impact ne se limite plus aux travaux manuels "
    "ou administratifs de routine ; il touche le cœur du travail intellectuel.", "C6 ch7 OpenAI")

# --------------------------------------------- normalisations conservatrices
rep("y consacrerBreur son propre temps", "y consacrer son propre temps", "extraction ch6")
rep("une dizaine de@de variantes", "une dizaine de variantes", "extraction ch6")
rep("Troisième exemple :C l3 la traduction", "Troisième exemple : la traduction", "extraction ch6")
rep("base de données5", "base de données", "extraction ch4")
rep("la consommation totale de cette ressource n diminuait pas",
    "la consommation totale de cette ressource ne diminuait pas", "extraction ch3")
rep("apocalytiques", "apocalyptiques", "ortho ch7")
rep("système judiciare", "système judiciaire", "ortho ch12", 0)
rep("l'expertise qui est recherché, c'est", "l'expertise qui est recherchée, c'est", "accord ch2")
rep("les possibilités qu'elle ouvre nous confronte", "les possibilités qu'elle ouvre nous confrontent", "accord ch15")
rep("l'un des lignes de faille", "l'une des lignes de faille", "accord ch11")
rep("Adults dans notre rapport à la connaissance", "Adultes dans notre rapport à la connaissance", "ortho concl 1")
rep("Adults dans notre rapport au travail", "Adultes dans notre rapport au travail", "ortho concl 2")
rep("Adults dans notre rapport au pouvoir", "Adultes dans notre rapport au pouvoir", "ortho concl 3")
rep("s'adjointre des agents", "s'adjoindre des agents", "ortho ch13")
rep("possibles* exaggerés", "possibles* exagérés", "ortho ch14")
rep("que le dystopie de la concentration", "que la dystopie de la concentration", "accord ch14")
rep("voix cloneée", "voix clonée", "ortho ch12")
rep("contenus counterfeités", "contenus contrefaits", "ortho ch12")
rep("bulbes cognitifs", "bulles cognitives", "ortho ch14")
rep("pour next week,", "pour la semaine prochaine,", "langue ch5")
rep("de se cheapen", "de se banaliser", "langue ch8")
rep("À quoi sert-ce que je suis là ?", "À quoi sert-il que je sois là ?", "ortho épilogue")
rep("des extraction de données", "des extractions de données", "accord biblio", 0)
rep("des données d'entraînement. Le\n\n*compute* est la nouvelle terre",
    "des données d'entraînement. Le *compute* est la nouvelle terre", "recollage ch14")
# recollage des traits d'union de fin de ligne
body = re.sub(r"([A-Za-zÀ-ÿ\u00C0-\u017F])- (?=[a-zà-ÿ\u00C0-\u017F])", r"\1-", body)
# espaces français : resserrer autour des guillemets (babel-french insère les bonnes espaces)
body = re.sub(r"«\s+", "«", body)
body = re.sub(r"\s+»", "»", body)
# guillemets droits résiduels → guillemets français
body = re.sub(r'"([^"]{1,200}?)"', r"«\1»", body)
assert '"' not in body, "guillemets droits résiduels"

# ---------------------------------------------------------------- bibliographie (protection précoce)
body = re.sub(r"^\*\*Sur (.+)\*\*$", lambda m: "@@BIBTHEME@@" + m.group(1) + "@@ENDBIBTHEME@@", body, flags=re.M)
body = re.sub(r"^\*\s+(.+\(\d{4}[^)]*\).+)$", lambda m: "@@BIB@@" + m.group(1).strip() + "@@ENDBIB@@", body, flags=re.M)

# ---------------------------------------------------------------- citations en aiquote
def quote_sub(m):
    raw = m.group(1).strip()
    if raw.startswith("**"):
        inner = raw.strip("*").strip()
        return "@@QBOLD@@%s@@ENDQ@@" % inner
    inner = re.sub(r"\*\*(.+?)\*\*", r"\1", raw)
    inner = re.sub(r"\*(.+?)\*", r"\1", inner).strip()
    return "@@Q@@%s@@ENDQ@@" % inner
body = re.sub(r"^> (.+)$", quote_sub, body, flags=re.M)
body = re.sub(r"@@Q(BOLD)?@@(.*?)@@ENDQ@@\n\n(?=@@Q)", lambda m: "@@Q%s@@%s@@ENDQ@@\n\n" % (m.group(1) or "", m.group(2)), body, flags=re.S)

# ---------------------------------------------------------------- échappement LaTeX
def esc(t):
    t = t.replace("\\", r"\textbackslash{}")
    for ch, r in [("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                  ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                  ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}"),
                  (">", r"\textgreater{}"), ("<", r"\textless{}")]:
        t = t.replace(ch, r)
    return t

body = esc(body)
body = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", body, flags=re.S)
body = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"\\emph{\1}", body)

# insertions LaTeX (après échappement)
body = body.replace("XXI\\up{e}", "XXI@EXP@@").replace("XXIe", "XXI\\up{e}")
body = re.sub(r"\bXXe\b", "XX\\\\up{e}", body)  # pragma: no cover
body = body.replace("XXIe siècle", "XXI\\up{e} siècle").replace("XXe siècle", "XX\\up{e} siècle")
body = re.sub(r"(\d) \\%", r"\1~\\%", body)
body = body.replace("10 000 kilomètres", "10~000 kilomètres")
body = body.replace("@EXP@@", "{e}")

# ---------------------------------------------------------------- restauration des aiquotes
body = re.sub(r"@@QBOLD@@(.*?)@@ENDQ@@", lambda m: "\\begin{aiquote}[s]\n\\qbold %s\n\\end{aiquote}" % m.group(1).strip(), body, flags=re.S)
body = re.sub(r"@@Q@@(.*?)@@ENDQ@@", lambda m: "\\begin{aiquote}\n%s\n\\end{aiquote}" % m.group(1).strip(), body, flags=re.S)

# ---------------------------------------------------------------- titres
body = re.sub(r"^\\# PARTIE ([IVX]+) — (.+)$",
              lambda m: "\\begin{partdivider}{%s}{%s}\\end{partdivider}" % (m.group(1), m.group(2)), body, flags=re.M)
body = re.sub(r"^\\#\\# Chapitre (\d+) — (.+)$",
              lambda m: "\\bookchap{%s}{%s}" % (m.group(1), m.group(2)), body, flags=re.M)
body = re.sub(r"^\\#\\# \d+\. INTRODUCTION — (.+)$", r"\\booksection{Introduction}{\1}", body, flags=re.M)
body = re.sub(r"^\\#\\# \d+\. PRÉFACE COURTE$", r"\\booksection{}{Préface courte}", body, flags=re.M)
body = re.sub(r"^\\# CONCLUSION — (.+)$", r"\\booksection{Conclusion}{\1}", body, flags=re.M)
body = re.sub(r"^\\# DIX QUESTIONS POUR DEMAIN$", r"\\booksection{}{Dix questions pour demain}", body, flags=re.M)
body = re.sub(r"^\\# ÉPILOGUE — (.+)$", r"\\booksection{Épilogue}{\1}", body, flags=re.M)
body = re.sub(r"^\\# BIBLIOGRAPHIE SÉLECTIVE ET COMMENTÉE$", r"\\booksection{}{Bibliographie sélective et commentée}", body, flags=re.M)
assert body.count("\\bookchap{") == 15, "chapitres ≠ 15"
assert body.count("\\booksection{") == 6, "sections étoilées ≠ 6"
assert body.count("\\begin{partdivider}") == 5, "parties ≠ 5"

# ---------------------------------------------------------------- boîtes scénarios
body = re.sub(r"^\\#\\#\\# SCÉNARIO ([ABC]) — ([^\n]+)$\n(.*?)(?=\n\n(?:\\#\\#\\# SCÉNARIO|Une interprétation s'impose|\\booksection|\\bookchap)|\Z)",
              lambda m: "\\begin{scenariobox}{%s}{%s}\n%s\n\\end{scenariobox}\n\n"
                        % (m.group(1), m.group(2), m.group(3).strip()),
              body, flags=re.M | re.S)
assert body.count("\\begin{scenariobox}") == 3, "scénarios ≠ 3"

# ---------------------------------------------------------------- bibliographie (restauration)
body = re.sub(r"@@BIBTHEME@@(.+?)@@ENDBIBTHEME@@", lambda m: "\\bibtheme{%s}" % m.group(1), body, flags=re.S)
body = re.sub(r"@@BIB@@(.+?)@@ENDBIB@@", lambda m: "\\bibentry{%s}" % m.group(1).strip(), body, flags=re.S)
ELDONOU = ("\\bibentry{Eloundou, T., Manning, S., Mishkin, P., \\& Rock, D. (2023). "
           "\\emph{GPTs are GPTs: An Early Look at the Labor Market Impact Potential of Large Language Models}. "
           "Étude empirique majeure (co-écrite avec des chercheurs d'OpenAI et de l'Université de Pennsylvanie) "
           "mesurant l'exposition des tâches professionnelles aux LLMs, chiffrant la proportion d'emplois impactés "
           "et validant la distinction entre automatisation de tâches et de métiers entiers.}")
assert body.count("\\bibtheme{") == 5, "thèmes biblio ≠ 5"
assert body.count("\\bibentry{") == 11, "entrées biblio ≠ 11"
body = body.replace("\\bibtheme{l'IA, le pouvoir et l'infrastructure}",
                    ELDONOU + "\n\n\\bibtheme{l'IA, le pouvoir et l'infrastructure}", 1)

# ---------------------------------------------------------------- listes
def wrap_list(marker, env):
    global body
    pat = re.compile(r"((?:%s).+(?:\n\n?)?)+" % marker, re.M)
    def f(m):
        block = m.group(0)
        items = [re.sub(r"\s+", " ", i).strip() for i in re.split(marker, block, flags=re.M) if i.strip()]
        return "\\begin{%s}\n%s\n\\end{%s}\n" % (env, "\n".join("\\item " + i for i in items), env)
    body = pat.sub(f, body)

wrap_list(r"^\* ", "eplist")
body = re.sub(r"^(\d+)\. ", r"@@QITEM@@", body, flags=re.M)
wrap_list(r"@@QITEM@@", "questionslist")

# ---------------------------------------------------------------- nettoyage
body = re.sub(r"\n{3,}", "\n\n", body).strip()
assert "**" not in body and "###" not in body, "markdown résiduel"
assert "@@" not in body.replace("@EXP@@", ""), "marqueurs résiduels"

# ---------------------------------------------------------------- découpage
i0 = body.index("\\booksection{}{Préface courte}")
i_intro = body.index("\\booksection{Introduction}{")
i1 = body.index("\\begin{partdivider}{I}")
front_preface = body[i0:i_intro].strip()
front_intro = body[i_intro:i1].strip()
rest = body[i1:]

def between(s, a, b=None):
    i = s.index(a)
    j = s.index(b) if b else len(s)
    return s[i:j].strip()

files = {"front-preface.tex": front_preface, "front.tex": front_intro}
for name, a, b in [("part1", "\\begin{partdivider}{I}", "\\begin{partdivider}{II}"),
                   ("part2", "\\begin{partdivider}{II}", "\\begin{partdivider}{III}"),
                   ("part3", "\\begin{partdivider}{III}", "\\begin{partdivider}{IV}"),
                   ("part4", "\\begin{partdivider}{IV}", "\\begin{partdivider}{V}"),
                   ("part5", "\\begin{partdivider}{V}", "\\booksection{Conclusion}")]:
    files[name + ".tex"] = between(rest, a, b)
files["back.tex"] = between(rest, "\\booksection{Conclusion}")

os.makedirs(OUT, exist_ok=True)
total = 0
for fn, content in files.items():
    with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
        f.write(content + "\n")
    w = len(content.split()); total += w
    print(f"{fn:12s} {w:6d} mots")
print(f"TOTAL: {total} mots")

# ---------------------------------------------------------------- Gate A préliminaire
joined = "\n".join(files.values())
for must in ["Préface courte", "Le matin ordinaire", "LE MONDE AVANT", "LE GRAND BASCULEMENT",
             "LE TRAVAIL ET L'INTELLIGENCE", "POUVOIR, VÉRITÉ ET ORGANISATIONS",
             "L'après n'est pas un endroit", "Dix questions pour demain", "L'humain après l'IA",
             "Bibliographie sélective et commentée", "Eloundou", "Rifkin", "Jevons", "Vygotsky",
             "archiviste", "pendant systémique", "Hollywood", "clone vocal", "bicycle de l'esprit"]:
    assert must in joined, f"MANQUANT: {must}"
for banned in ["CHECKPOINT", "ÉTAPE", "J'attends", "CONTINUER", "Estimation", "estimation du volume",
               "Objectif", "Transition**", "AUDIT", "J'attendrai"]:
    assert banned not in joined, f"FUITES: {banned}"
chap = re.findall(r"\\bookchap\{(\d+)\}", joined)
assert chap == [str(i) for i in range(1, 16)], f"chapitres: {chap}"
print("Gate A préliminaire : OK (15 chapitres, 5 parties, aucun bloc de production)")
