# ------------------------------------------------------------
#  Informationstheorie‑Trainer für TI‑Nspire CX II T (MicroPython)
#  – Fragen/Antworten offline nach Schlagworten durchsuchen –
# ------------------------------------------------------------

from tool_base import *

try:
    import urandom as random
except ImportError:
    import random


class InformationTheory(Tool):
    def __init__(self):
        self.PAGE_SIZE = 5
        self.QUESTION_DB = [
            {
                "id": 2,
                "q": "Im 5er-System ist die Basis 5 und es sind nur die Ziffern 0 bis 5 erlaubt.",
                "a": "False",
                "topic": "Zahlensysteme",
                "tags": [
                    "Zahlensystem",
                    "Basis",
                    "Fünfersystem",
                    "Ziffern"
                ]
            },
            {
                "id": 3,
                "q": "Welche Aussagen zur Exzesscodierung sind korrekt?",
                "a": [
                    "Exzesscodierung verschiebt den Nullpunkt in den positiven Bereich.",
                    "Exzess-127 erlaubt Darstellung von –127 bis 128."
                ],
                "topic": "Codierungen",
                "tags": [
                    "Exzesscodierung",
                    "Nullpunkt",
                    "Exzess-127",
                    "Darstellungsbereich"
                ]
            },
            {
                "id": 4,
                "q": "In einer Exzesscodierung wird der Bias zur darzustellenden Zahl addiert, um den Binärcode zu erhalten.",
                "a": "True",
                "topic": "Codierungen",
                "tags": [
                    "Exzesscodierung",
                    "Bias",
                    "Binärcode",
                    "Addieren"
                ]
            },
            {
                "id": 5,
                "q": "Welche Aussagen zu Gleitkommazahlen nach IEEE‑754 sind korrekt?",
                "a": [
                    "Das Vorzeichenbit 1 bedeutet negative Zahl.",
                    "Der Exponent wird im Exzessformat gespeichert."
                ],
                "topic": "Gleitkommazahlen",
                "tags": [
                    "Gleitkommazahl",
                    "IEEE-754",
                    "Vorzeichenbit",
                    "Exzessformat"
                ]
            },
            {
                "id": 6,
                "q": "Ordnen Sie die Booleschen Operationen den logischen Bedeutungen zu.",
                "a": [
                    "Disjunktion → OR",
                    "Konjunktion → AND",
                    "Entweder-Oder (ausschließliches Oder) → XOR",
                    "Negation → NOT"
                ],
                "topic": "Boolesche Algebra",
                "tags": [
                    "Boolesche_Operation",
                    "OR_AND_XOR_NOT",
                    "Zuordnung",
                    "Logik"
                ]
            },
            {
                "id": 7,
                "q": "Information ist …",
                "a": "relevant und nicht redundant",
                "topic": "Informationstheorie",
                "tags": [
                    "Information",
                    "Relevanz",
                    "Redundanz",
                    "Definition"
                ]
            },
            {
                "id": 8,
                "q": "Die Auftrittswahrscheinlichkeiten der Zeichen einer Quelle haben keinen Einfluss auf den …",
                "a": "Entscheidungsgehalt der Quelle.",
                "topic": "Informationstheorie",
                "tags": [
                    "Entscheidungsgehalt",
                    "Wahrscheinlichkeit",
                    "Quelle",
                    "Einfluss"
                ]
            },
            {
                "id": 9,
                "q": "Je seltener ein Zeichen einer Quelle, desto grösser ist sein …",
                "a": "Informationsgehalt.",
                "topic": "Informationstheorie",
                "tags": [
                    "Informationsgehalt",
                    "Seltenheit",
                    "Quelle",
                    "Probabilität"
                ]
            },
            {
                "id": 10,
                "q": "Wann ist die Entropie einer binären Quelle maximal?",
                "a": [
                    "Die Entropie beträgt 1 bit pro Symbol.",
                    "Die Unsicherheit über das nächste Symbol ist am grössten.",
                    "Die beiden Symbole treten mit gleicher Wahrscheinlichkeit auf.",
                    "Es ist nicht vorhersagbar, welches Symbol als nächstes kommt."
                ],
                "topic": "Informationstheorie",
                "tags": [
                    "Entropie",
                    "Binärquelle",
                    "Maximal",
                    "Gleichverteilung"
                ]
            },
            {
                "id": 11,
                "q": "Die Huffman‑Codierung berücksichtigt nicht …",
                "a": "die Historie der Zeichen.",
                "topic": "Kompression",
                "tags": [
                    "Huffman",
                    "Historie",
                    "Quelle",
                    "Kompression"
                ]
            },
            {
                "id": 12,
                "q": "Welche Aussagen treffen auf LZ77 zu?",
                "a": [
                    "Verwendet ein Sliding Window",
                    "Erkennt wiederkehrende Phrasen"
                ],
                "topic": "Kompression",
                "tags": [
                    "LZ77",
                    "Sliding_Window",
                    "Phrasen",
                    "Kompression"
                ]
            },
            {
                "id": 13,
                "q": "Welche Aussagen zur Datenkomprimierung sind korrekt?",
                "a": [
                    "Eine hohe Entropie erschwert Kompression",
                    "Kompression reduziert Redundanz"
                ],
                "topic": "Kompression",
                "tags": [
                    "Kompression",
                    "Entropie",
                    "Redundanz",
                    "Aussagen"
                ]
            },
            {
                "id": 14,
                "q": "Welche Aussagen über die mittlere Codewortlänge in einer Huffman‑Codierung sind korrekt?",
                "a": [
                    "Sie ist niemals kleiner als die Entropie.",
                    "Sie kann größer als die Entropie sein."
                ],
                "topic": "Kompression",
                "tags": [
                    "Huffman",
                    "mittlere_Codewortlänge",
                    "Entropie",
                    "Vergleich"
                ]
            },
            {
                "id": 15,
                "q": "Was bedeutet es, wenn ein Code die Präfixeigenschaft besitzt?",
                "a": [
                    "Kein Codewort ist der Anfang eines anderen Codeworts.",
                    "Die Zeichenfolge ist eindeutig dekodierbar, auch ohne Trennzeichen."
                ],
                "topic": "Codierungen",
                "tags": [
                    "Präfixcode",
                    "Dekodierbarkeit",
                    "Codewort",
                    "Eigenschaft"
                ]
            },
            {
                "id": 16,
                "q": "Ein nach Lempel‑Ziv codierter Code kann …",
                "a": "grösser sein als der Originalcode.",
                "topic": "Kompression",
                "tags": [
                    "Lempel_Ziv",
                    "Codegrösse",
                    "Kompression",
                    "Vergleich"
                ]
            },
            {
                "id": 17,
                "q": "Die mittlere Codewortlänge ist abhängig …",
                "a": "von den Auftrittswahrscheinlichkeiten der Zeichen und der Codierung der Quelle.",
                "topic": "Kompression",
                "tags": [
                    "Codewortlänge",
                    "Wahrscheinlichkeit",
                    "Codierung",
                    "Quelle"
                ]
            },
            {
                "id": 18,
                "q": "Beim RSA‑Verschlüsselungsverfahren wird angenommen, dass …",
                "a": "die Faktorisierung grosser Zahlen in Primzahlen aufwändig ist.",
                "topic": "Kryptographie",
                "tags": [
                    "RSA",
                    "Faktorisierung",
                    "Primzahlen",
                    "Schwierigkeit"
                ]
            },
            {
                "id": 19,
                "q": "Ein wesentliches Problem bei symmetrischen Verschlüsselungsverfahren mit vielen Teilnehmern ist die Länge des Schlüssels.",
                "a": "False",
                "topic": "Kryptographie",
                "tags": [
                    "Symmetrische_Verschlüsselung",
                    "Teilnehmer",
                    "Schlüsselverwaltung",
                    "Problem"
                ]
            },
            {
                "id": 20,
                "q": "Der Euklidische Algorithmus wird in der RSA‑Verschlüsselung verwendet, um die Primfaktoren zu berechnen.",
                "a": "False",
                "topic": "Kryptographie",
                "tags": [
                    "Euclid",
                    "RSA",
                    "Primfaktoren",
                    "Fehlaussage"
                ]
            },
            {
                "id": 21,
                "q": "Ein Code ist dichtgepackt, wenn …",
                "a": "sich alle gültigen und ungültigen Codeworte in einer Korrigierkugel befinden.",
                "topic": "Codetheorie",
                "tags": [
                    "Dichtgepackt",
                    "Korrigierkugel",
                    "Codewort",
                    "Eigenschaft"
                ]
            },
            {
                "id": 22,
                "q": "Welche Aussagen zum CRC sind korrekt?",
                "a": [
                    "CRC nutzt Polynomdivision.",
                    "Das Ergebnis ist eine Prüfsumme."
                ],
                "topic": "Fehlererkennung",
                "tags": [
                    "CRC",
                    "Polynomdivision",
                    "Prüfsumme",
                    "Fehlererkennung"
                ]
            },
            {
                "id": 23,
                "q": "Ein Faltungscode speichert vergangene Eingaben mit Hilfe von … . Zum optimalen Decodieren wird oft der …-Algorithmus eingesetzt.",
                "a": [
                    "Schieberegister",
                    "Viterbi-Algorithmus"
                ],
                "topic": "Fehlerkorrektur",
                "tags": [
                    "Faltungscode",
                    "Schieberegister",
                    "Viterbi",
                    "Decodierung"
                ]
            },
            {
                "id": 24,
                "q": "Das Shannon'sche Codierungstheorem besagt, dass jede Quellensprache mit einer Entropie H mit einer durchschnittlichen Codewortlänge L codiert werden kann, wobei L ≥ H.",
                "a": "True",
                "topic": "Informationstheorie",
                "tags": [
                    "Shannon",
                    "Codierungstheorem",
                    "Entropie",
                    "Codewortlänge"
                ]
            },
            {
                "id": 25,
                "q": "Wie viele verschiedene ganze Zahlen können im 8‑Bit‑Zweierkomplement dargestellt werden?",
                "a": "256 (von –128 bis +127)",
                "topic": "Stellenwertsystem",
                "tags": ["Stellenwertsystem", "Zweierkomplement", "Bitbreite", "Zahlenbereich"]
            },
            {
                "id": 26,
                "q": "Wandle die Dezimalzahl 45 in eine 8‑Bit‑Dualzahl um.",
                "a": "00101101₂",
                "topic": "Stellenwertsystem",
                "tags": ["Stellenwertsystem", "Umrechnung", "Dualsystem", "Beispiel"]
            },
            {
                "id": 27,
                "q": "Welche Aussage ist korrekt? A) Das Oktalsystem hat die Basis 8 und Ziffern 0–7. B) Das Oktalsystem hat die Basis 16 und Ziffern 0–F.",
                "a": "A",
                "topic": "Stellenwertsystem",
                "tags": ["Stellenwertsystem", "Oktalsystem", "Basis", "Wahr/Falsch"]
            },
            {
                "id": 28,
                "q": "Gib das Einerkomplement (b‑1) der Binärzahl 01011010 an.",
                "a": "10100101",
                "topic": "Stellenwertsystem",
                "tags": ["Komplement", "Einerkomplement", "Binärzahl", "Invertieren"]
            },
            {
                "id": 29,
                "q": "Berechne 13 ⋅ 11 als Unsigned‑Multiplikation im Binärsystem (Ergebnis in Binär).",
                "a": "100011 (dezimal = 143)",
                "topic": "Stellenwertsystem",
                "tags": ["Multiplikation", "Unsigned", "Dualsystem", "Beispiel"]
            },
            {
                "id": 30,
                "q": "Eine 16‑Bit‑Fixkommazahl verwendet 4 Nachkommabits. Welcher absolute Rundungsfehler kann maximal auftreten?",
                "a": "2⁻⁴ = 0,0625 dezimal",
                "topic": "Stellenwertsystem",
                "tags": ["Fixkommazahl", "Rundungsfehler", "Nachkommastellen", "Grenze"]
            },
            {
                "id": 31,
                "q": "Welcher Polynomterm entspricht dem Codewort 10101 im GF(2)?",
                "a": "u⁴ + u² + u⁰",
                "topic": "Interpretation eines Codewortes",
                "tags": ["Codewort", "Polynomdarstellung", "GF(2)", "Mapping"]
            },
            {
                "id": 32,
                "q": "True/False: Das Skalarprodukt zweier Codewort‑Vektoren in ℤ₂ liefert eine Paritätsprüfung.",
                "a": "True",
                "topic": "Interpretation eines Codewortes",
                "tags": ["Codewort", "Vektor", "Parität", "Bool"]
            },
            {
                "id": 33,
                "q": "Nenne zwei gleichwertige Darstellungen des Codeworts 1001 ausserhalb der Polynomdarstellung.",
                "a": [
                    "(1,0,0,1)ᵀ als Vektor",
                    "9₁₀ als Ganzzahl"
                ],
                "topic": "Interpretation eines Codewortes",
                "tags": ["Codewort", "Darstellung", "Vektor", "Dezimal"]
            },
            {
                "id": 34,
                "q": "Welche Eigenschaft fehlt, wenn (ℤ, ⋅) *keine* Gruppe ist? Wähle: A) Assoziativität B) Neutrales Element C) Inverses Element D) Abgeschlossenheit",
                "a": "C (für Multiplikation in ℤ existiert nicht zu jedem Element ein multiplikatives Inverses)",
                "topic": "Gruppe‑Ring‑Körper",
                "tags": ["AlgebraischeStrukturen", "Gruppe", "InversesElement", "MultipleChoice"]
            },
            {
                "id": 35,
                "q": "Ordne zu: (i) Gruppe, (ii) Ring, (iii) Körper — Welches benötigt zwei Operationen, von denen die zweite eine abelsche Gruppe auf allen Nicht‑Null‑Elementen bildet?",
                "a": "(iii) Körper",
                "topic": "Gruppe‑Ring‑Körper",
                "tags": ["AlgebraischeStrukturen", "Körper", "Definition", "Zuordnung"]
            },
            {
                "id": 36,
                "q": "True/False: In jedem endlichen Körper GF(pⁿ) gilt die Multiplikation kommutativ.",
                "a": "True",
                "topic": "Gruppe‑Ring‑Körper",
                "tags": ["GaloisFeld", "Kommutativität", "Bool", "Eigenschaft"]
            },
            {
                "id": 37,
                "q": "Ein Erzeuger 'a' erzeugt eine zyklische Gruppe der Ordnung 8. Wie viele verschiedene Potenzen von 'a' existieren, bevor sich der Zyklus wiederholt?",
                "a": "8 (a⁰ … a⁷)",
                "topic": "Gruppe‑Ring‑Körper",
                "tags": ["ZyklischeGruppe", "Ordnung", "Generator", "Exponentiation"]
            },
            {
                "id": 38,
                "q": "Welche der folgenden Booleschen Funktionen ist *funktional vollständig*? A) XOR allein B) NAND allein C) NOR + AND",
                "a": "B) NAND allein",
                "topic": "Boolesche Algebra",
                "tags": ["BoolAlgebra", "FunktionalVollständig", "NAND", "MC"]
            },
            {
                "id": 39,
                "q": "Gib die kanonische disjunktive Normalform (KDNF) für die Funktion f(A,B) = ¬A ∧ B an.",
                "a": "f(A,B) = ¬A ∧ B (bereits KDNF, da beide Variablen enthalten)",
                "topic": "Boolesche Algebra",
                "tags": ["KDNF", "Normalform", "Logikfunktion", "Beispiel"]
            },
            {
                "id": 40,
                "q": "Ein Halbaddierer liefert SUM = A ⊕ B und CARRY = A ∧ B. Welches Ergebnis (SUM,CARRY) ergibt sich für A = 1, B = 1?",
                "a": "(0,1)",
                "topic": "Boolesche Algebra",
                "tags": ["Halbaddierer", "XOR", "AND", "Beispiel"]
            },
            {
                "id": 41,
                "q": "Wähle alle wahren Aussagen zum Volladdierer: 1) hat 3 Eingänge 2) kann zwei 1‑Bit‑Zahlen addieren 3) benötigt XOR‑ und AND‑Gatter 4) erzeugt 2 Ausgangsbits",
                "a": ["1", "3", "4"],
                "topic": "Boolesche Algebra",
                "tags": ["Volladdierer", "Mehrfachantwort", "Eigenschaften", "Gatter"]
            },
            {
                "id": 42,
                "q": "True/False: Die NAND‑Verknüpfung kann jede andere Boolesche Funktion realisieren.",
                "a": "True",
                "topic": "Boolesche Algebra",
                "tags": ["NAND", "FunktionaleVollständigkeit", "Bool"]
            },
            {
                "id": 43,
                "q": "Ein fairer Würfel wird zweimal geworfen. Wie gross ist die Anzahl möglicher Ergebnisse Ω?",
                "a": "36",
                "topic": "Wahrscheinlichkeit",
                "tags": ["Laplace", "Ergebnisraum", "Würfel", "Kombinatorik"]
            },
            {
                "id": 44,
                "q": "Berechne die Wahrscheinlichkeit, bei 5 Bit genau 2 Fehler zu erhalten, wenn p = 0,1 die Fehlerrate pro Bit ist.",
                "a": "P = C(5,2)·0,1²·0,9³ ≈ 0,0729",
                "topic": "Wahrscheinlichkeit",
                "tags": ["Binomialverteilung", "Fehlerwahrscheinlichkeit", "Berechnung", "Beispiel"]
            },
            {
                "id": 45,
                "q": "Ordne zu: Kombination ohne Reihenfolge und ohne Zurücklegen. Formel? A) nPk B) nCk C) n^k",
                "a": "B) nCk = n! / (k!(n−k)!)",
                "topic": "Wahrscheinlichkeit",
                "tags": ["Kombinatorik", "Binomialkoeffizient", "Formel", "Zuordnung"]
            },
            {
                "id": 46,
                "q": "True/False: Für stochastisch unabhängige Ereignisse A und B gilt P(A∩B) = P(A)·P(B).",
                "a": "True",
                "topic": "Wahrscheinlichkeit",
                "tags": ["Unabhängigkeit", "Multiplikationsregel", "Bool"]
            },
            {
                "id": 47,
                "q": "Aus einem Urnenspiel werden 3 Kugeln *mit Zurücklegen* gezogen. Wie viele verschiedene geordneten Ergebnisse sind möglich, wenn die Urne 5 Kugel­farben enthält?",
                "a": "5³ = 125",
                "topic": "Wahrscheinlichkeit",
                "tags": ["Kombinatorik", "Zurücklegen", "Geordnet", "Urne"]
            },
            {
                "id": 48,
                "q": "Berechne den Entscheidungsgehalt H₀ für eine Quelle mit 8 verschiedenen Symbolen.",
                "a": "H₀ = log₂(8) = 3 bit",
                "topic": "Informationstheorie",
                "tags": ["Informationstheorie", "Entscheidungsgehalt", "Log2", "Beispiel"]
            },
            {
                "id": 49,
                "q": "Gib die Formel für den Informationsgehalt I(xₖ) eines Zeichens mit Wahrscheinlichkeit p(xₖ) an.",
                "a": "I(xₖ) = log₂(1 / p(xₖ)) bit",
                "topic": "Informationstheorie",
                "tags": ["Informationstheorie", "Informationsgehalt", "Formel", "Wahrscheinlichkeit"]
            },
            {
                "id": 50,
                "q": "Wie gross ist die Entropie einer binären Quelle, wenn p(0) = 0.5?",
                "a": "H = 1.000 bit",
                "topic": "Informationstheorie",
                "tags": ["Informationstheorie", "Entropie", "Binärquelle", "Beispiel"]
            },
            {
                "id": 51,
                "q": "Wann erreicht die Entropie einer Quelle ihr Maximum?",
                "a": [
                    "Alle Symbole treten mit gleicher Wahrscheinlichkeit auf.",
                    "Die Unsicherheit über das nächste Symbol ist am grössten."
                ],
                "topic": "Informationstheorie",
                "tags": ["Informationstheorie", "Maximale_Entropie", "Gleichverteilung", "Unsicherheit"]
            },
            {
                "id": 52,
                "q": "Eine Quelle hat Entscheidungsgehalt 4 bit und Entropie 2.75 bit. Wie gross ist die absolute Redundanz?",
                "a": "R_Q,absolut = 4 − 2.75 = 1.25 bit",
                "topic": "Informationstheorie",
                "tags": ["Informationstheorie", "Redundanz", "Absolut", "Berechnung"]
            },
            {
                "id": 53,
                "q": "Formuliere das Shannon'sche Codierungstheorem als Ungleichung.",
                "a": "H(X) ≤ L ≤ H(X) + 1",
                "topic": "Informationstheorie",
                "tags": ["Informationstheorie", "Shannon", "Codierungstheorem", "Ungleichung"]
            },
            {
                "id": 54,
                "q": "Was bedeutet Präfixeigenschaft bei Codes kurz erklärt?",
                "a": "Kein Codewort ist der Anfang eines anderen Codeworts → eindeutige Dekodierung ohne Trennzeichen",
                "topic": "Informationstheorie",
                "tags": ["Informationstheorie", "Präfixeigenschaft", "Dekodierung", "Code"]
            },
            {
                "id": 55,
                "q": "Nenne zwei Kenngrössen, die bei einer Quelle mit Gedächtnis zusätzlich zur Entropie betrachtet werden.",
                "a": ["Verbundentropie H(X,Y)", "Bedingte Entropie H(Y|X)"],
                "topic": "Informationstheorie",
                "tags": ["Informationstheorie", "Quelle_mit_Gedächtnis", "Verbundentropie", "Bedingte_Entropie"]
            },
            {
                "id": 56,
                "q": "Die Zeichenkette 'AAAAABBBCCDAA' wird mit RLE komprimiert. Wie viele Zeichen hat das komprimierte Ergebnis?",
                "a": "9",
                "topic": "Kompression",
                "tags": ["Kompression", "RLE", "Lauflängen", "Beispiel"]
            },
            {
                "id": 57,
                "q": "Welche zwei Hauptstrukturen verwendet der LZ77‑Algorithmus?",
                "a": ["Search Buffer (Textfenster)", "Look‑ahead Buffer"],
                "topic": "Kompression",
                "tags": ["Kompression", "LZ77", "SearchBuffer", "LookAhead"]
            },
            {
                "id": 58,
                "q": "True/False: Beim LZW‑Verfahren startet das Wörterbuch meist mit den Einträgen 0–255 für Byte‑Werte.",
                "a": "True",
                "topic": "Kompression",
                "tags": ["Kompression", "LZW", "Wörterbuch", "Bool"]
            },
            {
                "id": 59,
                "q": "Ordne die Reihenfolge einer Kombinationskompression richtig zu: Huffman → Lempel‑Ziv oder Lempel‑Ziv → Huffman?",
                "a": "Lempel‑Ziv zuerst, anschliessend Huffman",
                "topic": "Kompression",
                "tags": ["Kompression", "Kombination", "LZ", "Huffman"]
            },
            {
                "id": 60,
                "q": "Welche Aussage ist korrekt? A) Hohe Entropie erleichtert Kompression. B) Hohe Entropie erschwert Kompression.",
                "a": "B",
                "topic": "Kompression",
                "tags": ["Kompression", "Entropie", "Schwierigkeit", "MultipleChoice"]
            },
            {
                "id": 61,
                "q": "Welche beiden Eigenschaften treffen auf die mittlere Codewortlänge eines Huffman‑Codes zu?",
                "a": [
                    "Nie kleiner als die Entropie.",
                    "Kann grösser als die Entropie sein."
                ],
                "topic": "Kompression",
                "tags": ["Kompression", "Huffman", "Codewortlänge", "Eigenschaften"]
            },
            {
                "id": 62,
                "q": "Warum besitzt ein optimaler Huffman‑Code zwangsläufig die Präfixeigenschaft?",
                "a": "Der Binärbaum endet nur an Blättern; damit ist kein Codewort Präfix eines anderen.",
                "topic": "Kompression",
                "tags": ["Kompression", "Huffman", "Präfix", "Begründung"]
            },
            {
                "id": 63,
                "q": "Beim bitbasierten RLE wird das erste Run‑Length‑Symbol häufig vorangestellt. Was muss der Dekoder dabei wissen?",
                "a": "Ob die Folge mit einer 0 oder 1 startet.",
                "topic": "Kompression",
                "tags": ["Kompression", "RLE", "Startbit", "Dekodierung"]
            },
            {
                "id": 64,
                "q": "Gib die RSA‑Verschlüsselungsfunktion an (Klartext m, öffentlicher Exponent e, Modulus N).",
                "a": "c = m^e mod N",
                "topic": "Kryptologie",
                "tags": ["Kryptologie", "RSA", "Verschlüsselung", "Formel"]
            },
            {
                "id": 65,
                "q": "Welche Bedingung muss für die Schlüssel‑Exponenten e und d in RSA gelten?",
                "a": "e · d ≡ 1 (mod φ(N))",
                "topic": "Kryptologie",
                "tags": ["Kryptologie", "RSA", "Schlüsselbedingung", "Totient"]
            },
            {
                "id": 66,
                "q": "Berechne φ(n) für die Primzahlen p = 11 und q = 7.",
                "a": "φ(n) = (p−1)(q−1) = 10·6 = 60",
                "topic": "Kryptologie",
                "tags": ["Kryptologie", "Eulerfunktion", "Totient", "Beispiel"]
            },
            {
                "id": 67,
                "q": "True/False: Die Sicherheit von RSA basiert darauf, dass das Faktorisieren grosser Zahlen in Primzahlen aufwändig ist.",
                "a": "True",
                "topic": "Kryptologie",
                "tags": ["Kryptologie", "RSA", "Faktorisierung", "Bool"]
            },
            {
                "id": 68,
                "q": "Ein wesentliches Problem bei symmetrischen Verschlüsselungsverfahren mit vielen Teilnehmern ist die Länge des Schlüssels.",
                "a": "False",
                "topic": "Kryptologie",
                "tags": ["Kryptologie", "Symmetrisch", "Schlüsselverwaltung", "Bool"]
            },
            {
                "id": 69,
                "q": "Der Euklidische Algorithmus wird in RSA benutzt, um das multiplikative Inverse von e zu bestimmen, nicht um die Primfaktoren zu berechnen.",
                "a": "True",
                "topic": "Kryptologie",
                "tags": ["Kryptologie", "Euklidischer_Algorithmus", "Inverse", "Bool"]
            },
            {
                "id": 70,
                "q": "Welche beiden Schritte sind nötig, um einen RSA‑Privat­schlüssel (d) aus (p,q,e) zu berechnen?",
                "a": [
                    "φ(N) = (p−1)(q−1) bestimmen.",
                    "Multiplikatives Inverses d von e modulo φ(N) mittels erweitertem Euklid finden."
                ],
                "topic": "Kryptologie",
                "tags": ["Kryptologie", "RSA", "Privatschlüssel", "Berechnung"]
            },
            {
                "id": 71,
                "q": "Was kennzeichnet einen symmetrischen Kanal bezüglich seiner Fehlerwahrscheinlichkeit?",
                "a": "Fehlerwahrscheinlichkeit ist unabhängig von der Symbolverteilung der Quelle.",
                "topic": "Kanalmodell",
                "tags": ["Kanalmodell", "Symmetrischer_Kanal", "Fehlerwahrscheinlichkeit", "Eigenschaft"]
            },
            {
                "id": 72,
                "q": "Definiere Äquivokation H(X|Y) in einem digitalen Kanal in einem Satz.",
                "a": "Ungewissheit über das gesendete Symbol X bei bekanntem Empfangssymbol Y.",
                "topic": "Kanalmodell",
                "tags": ["Kanalmodell", "Äquivokation", "Definition", "Unsicherheit"]
            },
            {
                "id": 73,
                "q": "Formel für die Transinformation T eines Kanals angeben.",
                "a": "T = H(X) − H(X|Y) = H(Y) − H(Y|X)",
                "topic": "Kanalmodell",
                "tags": ["Kanalmodell", "Transinformation", "Formel", "Informationfluss"]
            },
            {
                "id": 74,
                "q": "Bei welcher quadratischen Kanalmatrix liegt ein vollständig gestörter (rein zufälliger) Kanal vor?",
                "a": "Alle Einträge gleich, z.B. 0.25 in jeder Zelle einer 4×4‑Matrix",
                "topic": "Kanalmodell",
                "tags": ["Kanalmodell", "Gestörter_Kanal", "Matrix", "Beispiel"]
            },
            {
                "id": 75,
                "q": "Wie lautet die Formel für die maximale Anzahl *sicher erkennbarer* Fehler e* in Abhängigkeit von der Hammingdistanz h?",
                "a": "e* = h − 1",
                "topic": "Fehlerkorrektur",
                "tags": ["Fehlerkorrektur", "Hammingdistanz", "Erkennbare_Fehler", "Formel"]
            },
            {
                "id": 76,
                "q": "Wie viele Fehler kann ein Code mit Hammingdistanz h = 3 sicher korrigieren?",
                "a": "⌊(h−1)/2⌋ = 1",
                "topic": "Fehlerkorrektur",
                "tags": ["Fehlerkorrektur", "Hammingdistanz", "Korrigierbare_Fehler", "Beispiel"]
            },
            {
                "id": 77,
                "q": "True/False: Für einen (n,k)‑Hammingcode gilt n = 2^k − 1.",
                "a": "True",
                "topic": "Fehlerkorrektur",
                "tags": ["Fehlerkorrektur", "Hammingcode", "Blockcode", "Bool"]
            },
            {
                "id": 78,
                "q": "Welche zwei Grössen bestimmt man beim CRC‑Verfahren mittels Polynomdivision?",
                "a": ["Generatorpolynom G(x)", "Prüfsumme (Rest)"],
                "topic": "Fehlerkorrektur",
                "tags": ["Fehlerkorrektur", "CRC", "Polynomdivision", "Prüfsumme"]
            },
            {
                "id": 79,
                "q": "Der Grad des Generatorpolynoms im CRC entspricht ___ .",
                "a": "der Anzahl Kontrollstellen (Prüfbits)",
                "topic": "Fehlerkorrektur",
                "tags": ["Fehlerkorrektur", "CRC", "Generatorgrad", "Kontrollstellen"]
            },
            {
                "id": 80,
                "q": "Ein Faltungscode wird als Tupel (a, e, s) angegeben. Wofür stehen a, e und s?",
                "a": [
                    "a: Anzahl Ausgänge pro Zeitintervall",
                    "e: Anzahl Eingänge pro Zeitintervall",
                    "s: Anzahl Speicherplätze (Shiftregister‑Stufen)"
                ],
                "topic": "Fehlerkorrektur",
                "tags": ["Fehlerkorrektur", "Faltungscode", "Parameter", "Definition"]
            },
            {
                "id": 81,
                "q": "Zum optimalen Decodieren eines Faltungscodes wird häufig welcher Algorithmus eingesetzt?",
                "a": "Viterbi‑Algorithmus",
                "topic": "Fehlerkorrektur",
                "tags": ["Fehlerkorrektur", "Viterbi", "Faltungscode", "Decodierung"]
            },
            {
                "id": 82,
                "q": "Formuliere die Bedingung für einen dichtgepackten Code bezogen auf Korrigierkugeln.",
                "a": "Alle gültigen Codewörter plus die dazugehörigen Korrigierkugeln füllen den gesamten Code­raum lückenlos aus.",
                "topic": "Fehlerkorrektur",
                "tags": ["Fehlerkorrektur", "Dichtgepackt", "Korrigierkugel", "Coderaum"]
            },
            {
                "id": 83,
                "q": "Was ist das Fehlersyndrom eines empfangenen Codeworts kurz erklärt?",
                "a": "Rest der Division durch das Generatorpolynom bzw. Paritätsprüfung, zeigt das Fehler­muster an.",
                "topic": "Fehlerkorrektur",
                "tags": ["Fehlerkorrektur", "Fehlersyndrom", "Rest", "Generatorpolynom"]
            },
            {
                "id": 84,
                "q": "Gib die allgemeine Formel für den darstellbaren Zahlenbereich eines n‑Bit‑Zweierkomplement‑Systems an.",
                "a": "von −2^{n−1} bis +2^{n−1}−1",
                "topic": "Stellenwertsystem",
                "tags": ["Stellenwertsystem", "Zweierkomplement", "Formel", "Bitbreite"]
            },
            {
                "id": 85,
                "q": "Beschreibe das Standardverfahren, um eine Dezimalzahl in ein beliebiges Basissystem b (b≥2) umzuwandeln.",
                "a": [
                    "Wiederholtes Teilen der Zahl durch Basis b",
                    "Aufschreiben der Reste in umgekehrter Reihenfolge"
                ],
                "topic": "Stellenwertsystem",
                "tags": ["Stellenwertsystem", "Umrechnung", "Algorithmus", "Basiswechsel"]
            },
            {
                "id": 86,
                "q": "Formuliere die allgemeine Berechnung eines Exzess‑Codes mit k Bits.",
                "a": "Code = Wert + Bias, wobei Bias = 2^{k−1}−1",
                "topic": "Codierungen",
                "tags": ["Exzesscodierung", "Bias", "Formel", "k-Bit"]
            },
            {
                "id": 87,
                "q": "Nenne zwei Bedingungen, damit ein Code eindeutig dekodierbar ist.",
                "a": [
                    "Präfixfreiheit (kein Codewort ist Präfix eines anderen)",
                    "Endliche Präfixe enden an Codewortgrenzen (keine Mehrdeutigkeit)"
                ],
                "topic": "Codierungen",
                "tags": ["EindeutigeDekodierung", "Präfix", "KraftMcMillan", "Codeeigenschaft"]
            },
            {
                "id": 88,
                "q": "Wie sind die Bits im IEEE‑754 Single‑Precision‑Format aufgeteilt?",
                "a": "1 Sign‑Bit, 8 Exponent‑Bits, 23 Mantissa‑Bits (mit verborgenem führenden 1‑Bit)",
                "topic": "Gleitkommazahlen",
                "tags": ["IEEE-754", "SinglePrecision", "Bitaufteilung", "Standard"]
            },
            {
                "id": 89,
                "q": "Gib die allgemeine Formel zur Berechnung des Wertes einer normalisierten IEEE‑754‑Gleitkommazahl an.",
                "a": "Wert = (−1)^s · 1.f · 2^{e−Bias}",
                "topic": "Gleitkommazahlen",
                "tags": ["IEEE-754", "Formel", "Normalisiert", "Bias"]
            },
            {
                "id": 90,
                "q": "Schreibe die beiden De‑Morgan‑Gesetze in Boolescher Algebra auf.",
                "a": [
                    "¬(A ∧ B) = ¬A ∨ ¬B",
                    "¬(A ∨ B) = ¬A ∧ ¬B"
                ],
                "topic": "Boolesche Algebra",
                "tags": ["DeMorgan", "Gesetze", "Negation", "Logik"]
            },
            {
                "id": 91,
                "q": "Wann gilt eine Menge von Booleschen Operationen als funktional vollständig?",
                "a": "Wenn sich jede Boolesche Funktion ausschließlich mit Operationen aus dieser Menge ausdrücken lässt.",
                "topic": "Boolesche Algebra",
                "tags": ["FunktionaleVollständigkeit", "Definition", "BoolAlgebra", "Operationen"]
            },
            {
                "id": 92,
                "q": "Gib die allgemeine Formel für die Entropie H(X) einer Quelle mit Symbolwahrscheinlichkeiten pᵢ an.",
                "a": "H(X) = −∑ pᵢ·log₂(pᵢ)",
                "topic": "Informationstheorie",
                "tags": ["Entropie", "Formel", "Informationstheorie", "p_i"]
            },
            {
                "id": 93,
                "q": "Was unterscheidet absolute von relativer Redundanz einer Quelle?",
                "a": [
                    "Absolute Redundanz: R_abs = H₀ − H (bit/symbol)",
                    "Relative Redundanz: r = R_abs / H₀ (dimensionslos)"
                ],
                "topic": "Informationstheorie",
                "tags": ["Redundanz", "Absolut", "Relativ", "Definition"]
            },
            {
                "id": 94,
                "q": "Vergleiche verlustfreie und verlustbehaftete Datenkompression in einem Satz.",
                "a": "Verlustfreie Kompression erlaubt exakte Rekonstruktion der Originaldaten, verlustbehaftete spart mehr Speicher durch akzeptierten Informationsverlust.",
                "topic": "Kompression",
                "tags": ["Verlustfrei", "Verlustbehaftet", "Definition", "Vergleich"]
            },
            {
                "id": 95,
                "q": "Nenne zwei typische Kriterien zur Bewertung der Effektivität eines Kompressionsverfahrens.",
                "a": ["Kompressionsrate", "Kodier‑/Dekodier‑Geschwindigkeit"],
                "topic": "Kompression",
                "tags": ["Kompression", "Kriterium", "Rate", "Performance"]
            },
            {
                "id": 96,
                "q": "Fasse die Hauptunterschiede zwischen symmetrischer und asymmetrischer Verschlüsselung zusammen.",
                "a": [
                    "Symmetrisch: gleicher Schlüssel zum Ver‑ und Entschlüsseln, sehr schnell, Schlüsselverteilung problematisch.",
                    "Asymmetrisch: Schlüssel‑Paar (öffentlich/privat), langsamer, erleichtert Verteilung und digitale Signaturen."
                ],
                "topic": "Kryptologie",
                "tags": ["Symmetrisch", "Asymmetrisch", "Vergleich", "Verschlüsselung"]
            },
            {
                "id": 97,
                "q": "Welche drei Sicherheitsziele werden in der Kryptographie häufig genannt?",
                "a": ["Vertraulichkeit", "Integrität", "Authentizität"],
                "topic": "Kryptologie",
                "tags": ["CIA", "Sicherheitsziele", "Grundlagen", "Kryptographie"]
            },
            {
                "id": 98,
                "q": "Definiere Kanalkapazität C in einem Satz und gib die zugehörige Formel an.",
                "a": "C = max_{p(x)} I(X;Y) – die maximale Transinformation über alle Eingabeverteilungen.",
                "topic": "Kanalmodell",
                "tags": ["Kanalkapazität", "Definition", "Formel", "Transinformation"]
            },
            {
                "id": 99,
                "q": "Was versteht man unter dem Begriff 'Gedächtnisloser Kanal'?",
                "a": "Fehler/Übertragungswahrscheinlichkeiten hängen nur vom aktuellen Symbol ab, nicht von vorangegangenen.",
                "topic": "Kanalmodell",
                "tags": ["Gedächtnislos", "Kanal", "Definition", "Eigenschaft"]
            },
            {
                "id": 100,
                "q": "Gib die Beziehung zwischen Codewortlänge n, Informationsbits k und Paritätsbits r in einem Blockcode an.",
                "a": "n = k + r",
                "topic": "Fehlerkorrektur",
                "tags": ["Blockcode", "n_k_r", "Formel", "Paritätsbits"]
            },
            {
                "id": 101,
                "q": "Formuliere die allgemeine Gleichung für die maximal korrigierbaren Fehler t in Abhängigkeit von der Mindest‑Hammingdistanz d_min.",
                "a": "t = ⌊(d_min − 1) / 2⌋",
                "topic": "Fehlerkorrektur",
                "tags": ["Fehlerkorrektur", "Hammingdistanz", "t", "Formel"]
            },
            {
                "id": 102,
                "q": "Gib die allgemeine Formel der Binomialverteilung P(X=k) an.",
                "a": "P(X=k) = C(n,k)·p^k·(1−p)^{n−k}",
                "topic": "Wahrscheinlichkeit",
                "tags": ["Binomialverteilung", "Formel", "P(X=k)", "n_k"]
            },
            {
                "id": 103,
                "q": "Was bedeutet der Begriff 'stochastische Unabhängigkeit' zweier Ereignisse kurz erklärt?",
                "a": "Das Eintreten von A beeinflusst nicht die Wahrscheinlichkeit von B: P(A∩B)=P(A)·P(B).",
                "topic": "Wahrscheinlichkeit",
                "tags": ["Unabhängigkeit", "Definition", "Multiplikationssatz", "Wahrscheinlichkeit"]
            },
            {
                "id": 104,
                "q": "Definiere eine abelsche Gruppe in Stichpunkten.",
                "a": [
                    "Assoziativität",
                    "Neutrales Element",
                    "Inverses Element",
                    "Kommutativität"
                ],
                "topic": "Gruppe‑Ring‑Körper",
                "tags": ["AbelscheGruppe", "Eigenschaften", "Definition", "Algebra"]
            },
            {
                "id": 105,
                "q": "Beschreibe, wie ein k‑Bit‑Codewort in ein Polynom in GF(2) umgewandelt wird.",
                "a": "Bit i wird Koeffizient des Terms u^i; höchstwertiges Bit → höchster Grad.",
                "topic": "Interpretation eines Codewortes",
                "tags": ["Polynomdarstellung", "GF(2)", "Mapping", "Codewort"]
            },
            {
                "id": 106,
                "q": "Was ist ein Nibble und wie viele verschiedene Werte kann es darstellen?",
                "a": "Ein Nibble umfasst 4 Bits und kann 2⁴ = 16 Werte (0–15) darstellen.",
                "topic": "Stellenwertsystem",
                "tags": ["Nibble", "4Bit", "Wertebereich", "Definition"]
            },
            {
                "id": 107,
                "q": "Welche Formel bestimmt die Anzahl benötigter Bits n, um z verschiedene Adressen eindeutig zu kodieren?",
                "a": "2^{n−1} < z ≤ 2^{n}",
                "topic": "Stellenwertsystem",
                "tags": ["Adressierungsformel", "Bitbedarf", "Log2", "Formel"]
            },
            {
                "id": 108,
                "q": "Nenne zwei Vorteile und zwei Nachteile des Binärsystems im Vergleich zum Hexadezimalsystem.",
                "a": [
                    "Vorteile Binär: einfache Hardware‑Realisierung, robuste Zustands­unterscheidung.",
                    "Nachteile Binär: lange Darstellung, schwer lesbar für Menschen.",
                    "Vorteile Hex: kompakte Darstellung, leichte Umrechnung 4 Bit ↔ 1 Hex‑Digit.",
                    "Nachteile Hex: zusätzliche Zeichen A‑F, Umwandlung für Maschine nötig."
                ],
                "topic": "Stellenwertsystem",
                "tags": ["Binär_vs_Hex", "Vor_Nachteile", "Vergleich", "Darstellung"]
            },
            {
                "id": 109,
                "q": "Wie viele Ergebnis‑Bits benötigt man maximal bei der Multiplikation zweier n‑Bit‑Zahlen?",
                "a": "2 n Bits",
                "topic": "Computerarithmetik",
                "tags": ["Multiplikation", "Bitbreite", "n-Bit", "Ergebnis"]
            },
            {
                "id": 110,
                "q": "Welche vier Normalformen werden in der Aussagenlogik unterschieden?",
                "a": [
                    "Negationsnormalform (NNF)",
                    "Disjunktive Normalform (DNF)",
                    "Konjunktive Normalform (KNF)",
                    "Kanonische disjunktive Normalform (KDNF)"
                ],
                "topic": "Boolesche Algebra",
                "tags": ["Normalformen", "NNF", "DNF", "KNF"]
            },
            {
                "id": 111,
                "q": "Was besagt die Potenz‑2‑Regel beim Karnaugh‑Diagramm?",
                "a": "Es dürfen nur Felder‑Gruppen in Größen von 1, 2, 4, 8, … (Potenzen von 2) gebildet werden.",
                "topic": "Boolesche Algebra",
                "tags": ["KV-Diagramm", "Potenz2Regel", "Karnaugh", "Minimierung"]
            },
            {
                "id": 112,
                "q": "Was ist Coderedundanz R_C und wie berechnet sie sich?",
                "a": "R_C = L − H(X) (Differenz zwischen mittlerer Codewortlänge und Entropie)",
                "topic": "Informationstheorie",
                "tags": ["Coderedundanz", "R_C", "Definition", "Formel"]
            },
            {
                "id": 113,
                "q": "Welche Aussage beschreibt eine Quelle mit Entropie H = 0?",
                "a": "Das nächste Symbol ist vollständig vorhersagbar; keine Unsicherheit vorhanden.",
                "topic": "Informationstheorie",
                "tags": ["Entropie0", "Vorhersagbarkeit", "Unsicherheit", "Grenzfall"]
            },
            {
                "id": 114,
                "q": "Nenne zwei Kenngrößen, die bei einer Quelle MIT Gedächtnis kleiner sind als bei einer gedächtnislosen Quelle.",
                "a": ["Entropie H(X)", "Transinformationbedarf pro Symbol"],
                "topic": "Informationstheorie",
                "tags": ["Quelle_mit_Gedächtnis", "Entropie", "Kenngrößen", "Vergleich"]
            },
            {
                "id": 115,
                "q": "Wann kann RLE die Datenlänge vergrössern?",
                "a": "Bei hochgradig zufälligen Daten ohne lange Wiederholungssequenzen.",
                "topic": "Kompression",
                "tags": ["RLE", "Negativfall", "Zufallsdaten", "Länge"]
            },
            {
                "id": 116,
                "q": "Warum liegt die Huffman‑Kompression nahe an der theoretischen Entropie, wenn die Symbolhäufigkeiten stark unterschiedlich sind?",
                "a": "Häufige Symbole erhalten kurze Codewörter, seltene bekommen längere → mittlere Codewortlänge nähert sich H.",
                "topic": "Kompression",
                "tags": ["Huffman", "UngleicheWahrscheinlichkeit", "Effizienz", "Entropienähe"]
            },
            {
                "id": 117,
                "q": "Wie viele Schlüssel werden bei N Teilnehmern in einem reinen symmetrischen System benötigt?",
                "a": "N(N−1)/2",
                "topic": "Kryptologie",
                "tags": ["Symmetrisch", "Schlüsselanzahl", "Formel", "N-Teilnehmer"]
            },
            {
                "id": 118,
                "q": "Nenne einen Grund, weshalb RSA für große Datenmengen meist in Kombination mit symmetrischer Verschlüsselung eingesetzt wird.",
                "a": "RSA ist deutlich langsamer; daher wird meist nur ein symmetrischer Sitzungsschlüssel per RSA übertragen.",
                "topic": "Kryptologie",
                "tags": ["Hybridverfahren", "Performance", "RSA", "Symmetrisch"]
            },
            {
                "id": 119,
                "q": "Welche Bedingung muss für die Nachricht m in RSA erfüllt sein, bevor sie mit dem öffentlichen Schlüssel verschlüsselt wird?",
                "a": "m < n (dem RSA‑Modulus)",
                "topic": "Kryptologie",
                "tags": ["RSA", "Nachrichtenbedingung", "m<n", "Korrektheit"]
            },
            {
                "id": 120,
                "q": "Wie lautet die Bedingung 2^k ≥ n + 1 bei Hamming‑Codes bezogen auf n, k und ihre Bedeutung?",
                "a": "Sie stellt sicher, dass k Paritätsbits in einem (n,k)‑Code alle n + 1 möglichen Syndromwerte abbilden.",
                "topic": "Fehlerkorrektur",
                "tags": ["Hammingcode", "Paritätsbits", "Syndrom", "Bedingung"]
            },
            {
                "id": 121,
                "q": "Was ist der Unterschied zwischen erkannter und korrigierter Fehleranzahl (e* vs. e) bei Blockcodes?",
                "a": "Erkannte Fehler e* = h−1, korrigierbare Fehler e = ⌊(h−1)/2⌋.",
                "topic": "Fehlerkorrektur",
                "tags": ["Blockcode", "e*", "e", "Hammingdistanz"]
            },
            {
                "id": 122,
                "q": "Wie beeinflusst eine niedrige Code‑Rate R = k/n die Redundanz und Fehlerkorrekturleistung eines Faltungscodes?",
                "a": "Je kleiner R, desto mehr Redundanz und desto höher die potenzielle Fehlerkorrekturleistung, aber geringere Effizienz.",
                "topic": "Fehlerkorrektur",
                "tags": ["Faltungscode", "CodeRate", "Redundanz", "Leistung"]
            },
            {
                "id": 123,
                "q": "Was ist die Additionsregel der Wahrscheinlichkeiten für zwei Ereignisse A und B?",
                "a": "P(A∪B) = P(A) + P(B) − P(A∩B)",
                "topic": "Wahrscheinlichkeit",
                "tags": ["Additionssatz", "Wahrscheinlichkeit", "AUB", "Formel"]
            },
            {
                "id": 124,
                "q": "Welcher Wert ist beim Werfen eines fairen Würfels wahrscheinlicher: eine bestimmte Zahl oder die Menge aller geraden Zahlen?",
                "a": "Die Menge aller geraden Zahlen (P = 3/6) ist wahrscheinlicher als eine einzelne Zahl (P = 1/6).",
                "topic": "Wahrscheinlichkeit",
                "tags": ["Würfel", "Vergleich", "GeradeZahlen", "Einzelereignis"]
            },
            {
                "id": 125,
                "q": "Nenne ein Beispiel für einen Ring, der kein Körper ist, und begründe kurz.",
                "a": "Die ganzen Zahlen ℤ: keine multiplikativen Inversen für alle Nicht‑Null‑Elemente.",
                "topic": "Gruppe‑Ring‑Körper",
                "tags": ["Ring", "KeinKörper", "Beispiel", "Eigenschaft"]
            },
            {
                "id": 126,
                "q": "Wie prüft man mit einem Skalarprodukt in ℤ₂, ob ein Codewort gerade oder ungerade Parität besitzt?",
                "a": "Alle Bits mit 1 multiplizieren (AND) und aufsummieren mod 2; Ergebnis 0 → gerade, 1 → ungerade.",
                "topic": "Interpretation eines Codewortes",
                "tags": ["Paritätsprüfung", "Skalarprodukt", "Z2", "GeradeUngerade"]
            },
            {
                "id": 127,
                "q": "Welche Aussage beschreibt den Zusammenhang zwischen Symbolwahrscheinlichkeit p(x) und Informationsgehalt I(x) korrekt?  \nA) I(x) sinkt, wenn p(x) sinkt  \nB) I(x) steigt, wenn p(x) sinkt  \nC) I(x) ist unabhängig von p(x)",
                "a": "B",
                "topic": "Informationstheorie",
                "tags": ["Informationsgehalt", "Wahrscheinlichkeit", "Zusammenhang", "MultipleChoice"]
            },
            {
                "id": 128,
                "q": "True/False: Wenn alle Symbole einer Quelle die gleiche Wahrscheinlichkeit besitzen, ist der Informationsgehalt jedes Symbols identisch.",
                "a": "True",
                "topic": "Informationstheorie",
                "tags": ["Gleichverteilung", "Informationsgehalt", "Bool", "Eigenschaft"]
            },
            {
                "id": 129,
                "q": "Ordne zu:  \n1) Entropie einer Quelle  \n2) Entscheidungsgehalt H₀  \nTrifft zu …  \na) basiert ausschliesslich auf der Anzahl möglicher Symbole  \nb) berücksichtigt deren Wahrscheinlichkeiten",
                "a": ["1 → b", "2 → a"],
                "topic": "Informationstheorie",
                "tags": ["Entropie", "Entscheidungsgehalt", "Zuordnung", "Definition"]
            },
            {
                "id": 130,
                "q": "Welche Quelle ist besser komprimierbar?  \nA) Quelle A: ein Symbol tritt mit 98 % Wahrscheinlichkeit auf, die restlichen 2 % verteilen sich auf vier Symbole  \nB) Quelle B: fünf Symbole treten jeweils mit 20 % Wahrscheinlichkeit auf",
                "a": "A",
                "topic": "Kompression",
                "tags": ["Kompressierbarkeit", "Wahrscheinlichkeit", "Häufigkeit", "MultipleChoice"]
            },
            {
                "id": 131,
                "q": "Nenne zwei Gründe, warum seltene Symbole in einem Huffman‑Code längere Codewörter erhalten.",
                "a": [
                    "Sie tragen weniger zur Gesamtwahrscheinlichkeit bei.",
                    "Längere Codewörter erhöhen die Differenzierung zu häufigen Symbolen und sichern Präfixfreiheit."
                ],
                "topic": "Kompression",
                "tags": ["Huffman", "SelteneSymbole", "CodewortLänge", "Begründung"]
            },
            {
                "id": 132,
                "q": "True/False: Eine Quelle mit Entropie H = 0 hat immer Redundanz R = 0.",
                "a": "False",
                "topic": "Informationstheorie",
                "tags": ["Entropie0", "Redundanz", "Bool", "Quelleneigenschaft"]
            },
            {
                "id": 133,
                "q": "Welche Auswirkung hat das Hinzufügen eines sehr seltenen Symbols (p ≈ 0) auf die Entropie einer ansonsten unveränderten Quelle?",
                "a": "Die Entropie steigt leicht, weil zusätzliche Unsicherheit eingeführt wird.",
                "topic": "Informationstheorie",
                "tags": ["SeltenesSymbol", "Entropie", "Einfluss", "Quelle"]
            },
            {
                "id": 134,
                "q": "Erkläre in einem Satz, wann die *relative* Redundanz einer Quelle Null ist.",
                "a": "Wenn ihre Entropie H gleich dem Entscheidungsgehalt H₀ ist (keine vermeidbare Redundanz).",
                "topic": "Informationstheorie",
                "tags": ["RelativeRedundanz", "Null", "Bedingung", "Definition"]
            },
            {
                "id": 135,
                "q": "Vergleiche die Auswirkungen einer Quelle *mit Gedächtnis* im Gegensatz zu einer gedächtnislosen Quelle auf die Entropie pro Symbol.",
                "a": "Eine Quelle mit Gedächtnis weist meist geringere Entropie pro Symbol auf, da vergangene Symbole Information über kommende liefern.",
                "topic": "Informationstheorie",
                "tags": ["QuelleMitGedächtnis", "Entropie", "Vergleich", "Eigenschaft"]
            },
            {
                "id": 136,
                "q": "Welche Eigenschaft einer Quellencodierung wird verbessert, wenn man die tatsächlichen Symbolwahrscheinlichkeiten korrekt erfasst und nutzt?",
                "a": "Die mittlere Codewortlänge nähert sich der Entropie an und reduziert die Coderedundanz.",
                "topic": "Kompression",
                "tags": ["Coderedundanz", "Symbolwahrscheinlichkeit", "CodeEffizienz", "Eigenschaft"]
            }
        ]

    def _pause(self):
        """Warte auf Enter-Eingabe"""
        input('\n<Enter> drücken …')

    def _wrap(self, text, width=35):
        """Zeile weich umbrechen (einfach)."""
        out, line = [], ''
        for word in text.split():
            if len(line) + len(word) + 1 > width:
                out.append(line)
                line = word
            else:
                line = line + (' ' if line else '') + word
        if line:
            out.append(line)
        return out

    def _show_paged(self, items, fn_render):
        """Seitenweise Anzeige mit Navigation"""
        page = 0
        while True:
            start = page * self.PAGE_SIZE
            if start >= len(items):
                print('\nKein weiterer Eintrag.')
                break

            end = min(start + self.PAGE_SIZE, len(items))
            print('\n----- Seite', page + 1, '/',
                  ((len(items) - 1) // self.PAGE_SIZE) + 1, '-----')
            for idx in range(start, end):
                try:
                    line = fn_render(idx, items[idx])
                except TypeError:
                    line = fn_render(items[idx])
                print(line)

            btn = input("[N]ext / [P]rev / Nummer / [V]iew / [Q]uit: ").strip().lower()

            if btn == 'n':
                page += 1
            elif btn == 'p' and page > 0:
                page -= 1
            elif btn == 'v':
                for idx in range(start, end):
                    self.view_question(items[idx])
            elif btn.isdigit():
                sel = int(btn)
                q_hit = next((q for q in items if q['id'] == sel), None)
                if q_hit:
                    self.view_question(q_hit)
                else:
                    print('Keine Frage mit dieser Nummer in der Liste.')
            else:
                break

    def view_question(self, qdict):
        """Einzelne Frage mit Antwort anzeigen"""
        print('\n=== Frage', qdict['id'], '===')
        for line in self._wrap(qdict['q']):
            print(line)
        print('\n--- Lösung ---')
        if isinstance(qdict['a'], list):
            for ans in qdict['a']:
                print('-', ans)
        else:
            print(qdict['a'])
        self._pause()

    def browse_db(self):
        """Alle Fragen durchblättern"""
        self._show_paged(self.QUESTION_DB,
                         lambda i, q: "%2d. %s" % (q['id'], q['q'][:38] + ('…' if len(q['q']) > 38 else '')))

    def search_db(self):
        """Suche nach Begriffen"""
        key = input('\nSuchbegriff: ').strip().lower()
        hits = [q for q in self.QUESTION_DB
                if key in q['q'].lower() or any(key in t.lower() for t in q['tags'])]

        if not hits:
            print('Keine Treffer.')
            self._pause()
            return

        if len(hits) == 1:
            self.view_question(hits[0])
            return

        self._show_paged(hits,
                         lambda i, q: "%2d. %s" % (q['id'], q['q'][:38] + ('…' if len(q['q']) > 38 else '')))

    def list_by_topic(self):
        """Topics seitenweise anzeigen, dann Fragen des gewählten Topics."""
        topics = sorted(set(q['topic'] for q in self.QUESTION_DB))
        page = 0

        while True:
            start = page * self.PAGE_SIZE
            if start >= len(topics):
                print('\nKein weiterer Eintrag.')
                break

            end = min(start + self.PAGE_SIZE, len(topics))
            print('\n--- Topics Seite', page + 1, '/',
                  ((len(topics) - 1) // self.PAGE_SIZE) + 1, '---')
            for idx in range(start, end):
                print("%2d. %s" % (idx + 1, topics[idx]))

            cmd = input("[N]ext / [P]rev / Nummer / [Q]uit: ").strip().lower()

            if cmd == 'n':
                page += 1
            elif cmd == 'p' and page > 0:
                page -= 1
            elif cmd.isdigit():
                sel = int(cmd) - 1
                if 0 <= sel < len(topics):
                    topic = topics[sel]
                    hits = [q for q in self.QUESTION_DB if q['topic'] == topic]
                    self._show_paged(
                        hits,
                        lambda i, q: "%2d. %s" % (
                            q['id'], q['q'][:38] + ('…' if len(q['q']) > 38 else '')
                        )
                    )
            else:
                break

    def quiz_random(self):
        """Zufällige Quiz-Frage"""
        q = random.choice(self.QUESTION_DB)
        print('\n** QUIZ **')
        for line in self._wrap(q['q']):
            print(line)
        input('\nDeine Antwort (Enter zeigt Lösung)…')
        self.view_question(q)

    def statistics(self):
        """Zeige Statistiken zur Datenbank"""
        total_questions = len(self.QUESTION_DB)
        topics = set(q['topic'] for q in self.QUESTION_DB)
        all_tags = []
        for q in self.QUESTION_DB:
            all_tags.extend(q['tags'])
        unique_tags = set(all_tags)

        print('\n=== STATISTIKEN ===')
        print('Anzahl Fragen: {}'.format(total_questions))
        print('Anzahl Topics: {}'.format(len(topics)))
        print('Anzahl verschiedener Tags: {}'.format(len(unique_tags)))

        print('\n--- Topics ---')
        for topic in sorted(topics):
            count = len([q for q in self.QUESTION_DB if q['topic'] == topic])
            print('{}: {} Fragen'.format(topic, count))

        self._pause()

    def run(self) -> None:
        """Hauptmenü für den Informationstheorie-Trainer"""
        global current_menu
        current_menu = "information_theory"

        while current_menu == "information_theory":
            print('\n' + '=' * 40)
            print('INFORMATIONSTHEORIE-TRAINER')
            print('=' * 40)
            print('1. Alle Fragen durchblättern')
            print('2. Suche nach Begriffen')
            print('3. Nach Topic filtern')
            print('4. Quiz (Zufallsfrage)')
            print('5. Statistiken anzeigen')
            print('0. Zurück zum Hauptmenü')

            choice = input('Wähle eine Option: ').strip()

            try:
                if choice == '1':
                    self.browse_db()
                elif choice == '2':
                    self.search_db()
                elif choice == '3':
                    self.list_by_topic()
                elif choice == '4':
                    self.quiz_random()
                elif choice == '5':
                    current_menu = "main"
                    break
                elif choice == '6':
                    self.statistics()
                elif choice == '0':
                    current_menu = "main"
                    break
                else:
                    print('Ungültige Auswahl.')
                    self._pause()
            except Exception as e:
                print('Fehler: {}'.format(str(e)))
                self._pause()