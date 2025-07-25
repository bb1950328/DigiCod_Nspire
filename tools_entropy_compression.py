from tool_base import *
import math


class EntropyTool(Tool):
    def entropy(self, probs):
        """Berechnet die Entropie einer Wahrscheinlichkeitsverteilung"""
        return -sum(p * math.log2(p) for p in probs if p > 0)

    def run(self) -> None:
        print("==== Entropie berechnen ====")
        try:
            n = int(input("Anzahl der Symbole: "))
            if n <= 0:
                raise ValueError("Die Anzahl der Symbole muss positiv sein")
            probs = []
            for i in range(n):
                p = float(input("Wahrscheinlichkeit für Symbol {}: ".format(i + 1)))
                probs.append(p)

            result = self.entropy(probs)
            print("\nEntropie: {:.6f} bits/Symbol".format(result))
        except Exception as e:
            print("Fehler: {}".format(str(e)))

        print("\nDrücke Enter, um fortzufahren...")
        input()


class RedundanzTool(Tool):
    def entropy(self, probs):
        """Berechnet die Entropie einer Wahrscheinlichkeitsverteilung"""
        return -sum(p * math.log2(p) for p in probs if p > 0)

    def redundanz(self, probs, codewortlängen):
        """Berechnet die Redundanz eines Codes"""
        h = self.entropy(probs)
        l = sum(p * l for p, l in zip(probs, codewortlängen))
        return l - h  # RC = L - H(X)

    def run(self) -> None:
        print("==== Redundanz berechnen ====")
        try:
            n = int(input("Anzahl der Symbole: "))
            probs = []
            lengths = []
            for i in range(n):
                p = float(input("Wahrscheinlichkeit für Symbol {}: ".format(i + 1)))
                probs.append(p)
                l = float(input("Codewortlänge für Symbol {}: ".format(i + 1)))
                lengths.append(l)

            result = self.redundanz(probs, lengths)
            print("\nRedundanz: {:.6f} bits/Symbol".format(result))
        except Exception as e:
            print("Fehler: {}".format(str(e)))

        print("\nDrücke Enter, um fortzufahren...")
        input()


class HuffmanTool(Tool):
    def huffman_coding(self, symbols, frequencies):
        """Erstellt einen Huffman-Code basierend auf Symbolen und Frequenzen"""
        # Einfache Implementierung für die Prüfung
        nodes = [[freq, [sym, ""]] for sym, freq in zip(symbols, frequencies)]

        while len(nodes) > 1:
            # Sortiere nach Frequenz
            nodes.sort(key=lambda x: x[0])
            # Nimm die zwei kleinsten Knoten
            lo = nodes.pop(0)
            hi = nodes.pop(0)

            # Füge "0" zu allen Codes im lo Knoten hinzu
            for pair in lo[1:]:
                pair[1] = "0" + pair[1]
            # Füge "1" zu allen Codes im hi Knoten hinzu
            for pair in hi[1:]:
                pair[1] = "1" + pair[1]

            # Erstelle neuen Knoten mit Summe der Frequenzen
            nodes.append([lo[0] + hi[0]] + lo[1:] + hi[1:])

        # Extrahiere Codes in ein Dictionary
        result = [(sym, code) for sym, code in nodes[0][1:]]
        result.sort(key=lambda t: symbols.index(t[0]))
        return result

    def run(self) -> None:
        print("==== Huffman-Code erstellen ====")
        try:
            n = int(input("Anzahl der Symbole: "))
            symbols = []
            freqs = []
            for i in range(n):
                s = input("Symbol {}: ".format(i + 1))
                symbols.append(s)
                f = float(input("Häufigkeit für Symbol {}: ".format(i + 1)))
                freqs.append(f)

            huffman_code = self.huffman_coding(symbols, freqs)
            print("\nHuffman-Code:")
            for sym, code in huffman_code:
                print("{}: {}".format(sym, code))

            # Calculate average code length
            avg_length = sum(len(code) * freq for (sym, code), freq in zip(huffman_code, freqs))
            print("\nDurchschnittliche Codewortlänge: {:.6f} bits/Symbol".format(avg_length))

        except Exception as e:
            print("Fehler: {}".format(str(e)))

        print("\nDrücke Enter, um fortzufahren...")
        input()


class RLETool(Tool):
    def rle_encode(self, data):
        if len(data) == 0:
            return [], 0
        encoded = []
        prev = data[0]
        count = 1
        for i in range(1, len(data)):
            if data[i] == prev:
                count += 1
            else:
                encoded.append((prev, count))
                prev = data[i]
                count = 1
        encoded.append((prev, count))
        return encoded, len(encoded)

    def rle_decode(self, encoded):
        output = ''
        for sym, cnt in encoded:
            output += sym * cnt
        return output

    def menu(self):
        print("==== Lauflängenkodierung (RLE) ====")
        print("Eingabetyp wählen:")
        print("1: Text")
        print("2: Binär (nur 0 und 1)")
        print("3: Beenden")
        print("Option (1–3):")

    def run(self) -> None:
        while True:
            self.menu()
            try:
                choice = int(input())
            except:
                print("Ungültige Eingabe.")
                continue

            if choice == 3:
                print("Beendet.")
                break
            elif choice not in [1, 2]:
                print("Nur 1, 2 oder 3 erlaubt.")
                continue

            print("Geben Sie den zu kodierenden Text ein:")
            s = input().strip()

            if choice == 2:
                valid = True
                for c in s:
                    if c not in '01':
                        print("Nur 0 und 1 erlaubt für binär.")
                        valid = False
                        break
                if not valid:
                    continue

            encoded, n_units = self.rle_encode(s)
            print("Eingabe:")
            print(s)

            print("Lauflängenkodiert:")
            output_str = ""
            for sym, cnt in encoded:
                if cnt == 1:
                    output_str += sym
                else:
                    output_str += sym + str(cnt)
            print(output_str)

            original_len = len(s)
            encoded_len = len(output_str)
            rate = round(encoded_len / original_len, 5)
            print("Kompressionsrate:", rate)
            print("Original:", original_len, "Einheiten")
            print("Kodiert:", encoded_len, "Einheiten")

            decoded = self.rle_decode(encoded)
            print("Überprüfung:", end=' ')
            if decoded == s:
                print("Dekodierung stimmt mit Original überein.")
            else:
                print("Fehler in der Dekodierung!")

            print("Drücke Enter zum Fortfahren...")
            input()  # Wartet auf Enter

class LZW(Tool):

    def lzw_encode(self, data, initial_dict=None):
        """
        LZW Kompressionsalgorithmus mit optionalem Anfangswörterbuch
        """
        # Initialisiere Wörterbuch
        if initial_dict is None:
            # Automatisch alle eindeutigen Zeichen aus der Eingabe verwenden
            unique_chars = sorted(set(data))
            dictionary = {char: i for i, char in enumerate(unique_chars)}
        elif isinstance(initial_dict, list):
            # Liste von Zeichen -> Dictionary erstellen
            dictionary = {char: i for i, char in enumerate(initial_dict)}
        elif isinstance(initial_dict, dict):
            # Dictionary direkt verwenden
            dictionary = initial_dict.copy()
        else:
            raise ValueError("initial_dict muss None, Liste oder Dictionary sein")

        result = []
        current_string = ""

        for char in data:
            # Versuche die Zeichenfolge zu erweitern
            new_string = current_string + char

            if new_string in dictionary:
                # Zeichenfolge ist im Wörterbuch, erweitere weiter
                current_string = new_string
            else:
                # Zeichenfolge nicht im Wörterbuch
                # Gib Index der aktuellen Zeichenfolge aus
                result.append(dictionary[current_string])

                # Füge neue Zeichenfolge zum Wörterbuch hinzu
                dictionary[new_string] = len(dictionary)

                # Beginne mit dem aktuellen Zeichen
                current_string = char

        # Gib den Index der letzten Zeichenfolge aus
        if current_string:
            result.append(dictionary[current_string])

        return result, dictionary

    def lzw_decode(self, encoded_data, initial_dict=None):
        """
        LZW Dekompressionsalgorithmus mit optionalem Anfangswörterbuch
        """
        # Initialisiere Wörterbuch
        if initial_dict is None:
            # Standard: Ziffern 0-9
            dictionary = {i: str(i) for i in range(10)}
        elif isinstance(initial_dict, list):
            # Liste von Zeichen -> Dictionary erstellen
            dictionary = {i: char for i, char in enumerate(initial_dict)}
        elif isinstance(initial_dict, dict):
            # Dictionary umkehren (char->index zu index->char)
            dictionary = {v: k for k, v in initial_dict.items()}
        else:
            raise ValueError("initial_dict muss None, Liste oder Dictionary sein")

        result = ""

        if not encoded_data:
            return result

        # Erstes Symbol
        old_code = encoded_data[0]
        result += dictionary[old_code]

        for i in range(1, len(encoded_data)):
            new_code = encoded_data[i]

            if new_code in dictionary:
                # Code ist im Wörterbuch
                string = dictionary[new_code]
            else:
                # Code ist nicht im Wörterbuch (sollte der nächste sein)
                string = dictionary[old_code] + dictionary[old_code][0]

            result += string

            # Füge neue Zeichenfolge zum Wörterbuch hinzu
            dictionary[len(dictionary)] = dictionary[old_code] + string[0]

            old_code = new_code

        return result

    def encode_compact(self, data, initial_dict=None):
        """
        Kompakte LZW-Kodierung - zeigt nur das Ergebnis
        """
        try:
            result, dictionary = self.lzw_encode(data, initial_dict)
            print("Eingabe: {}".format(data))
            print("Kodiert: {}".format(' '.join(map(str, result))))
            return result, dictionary
        except Exception as e:
            print("FEHLER: {}".format(str(e)))
            return None, None

    def show_encoding_steps(self, data, dictionary):
        """
        Zeigt detaillierte Kodierungsschritte (auf Anfrage)
        """
        print("\n=== KODIERUNGSSCHRITTE ===")

        # Hilfsfunktion für Formatierung
        def pad_left(text, width):
            text = str(text)
            if len(text) >= width:
                return text
            return text + ' ' * (width - len(text))

        result = []
        current_string = ""
        step = 1

        # Zeige Startwörterbuch
        print("Start-Wörterbuch:")
        for key, value in sorted(dictionary.items(), key=lambda x: x[1]):
            print("  {}: '{}'".format(value, key))

        print("\nSchritte:")

        for char in data:
            new_string = current_string + char

            if new_string in dictionary:
                current_string = new_string
            else:
                # Ausgabe für aktuellen Schritt
                if current_string:
                    index = dictionary[current_string]
                    result.append(index)
                    next_index = len(dictionary)

                    print("{}. '{}' -> {} | Neu: {}='{}'".format(
                        step, current_string, index, next_index, new_string
                    ))

                    dictionary[new_string] = next_index
                    step += 1

                current_string = char

        # Letzter Schritt
        if current_string:
            index = dictionary[current_string]
            result.append(index)
            print("{}. '{}' -> {}".format(step, current_string, index))

        print("\nErgebnis: {}".format(' '.join(map(str, result))))
        return result

    def show_final_dictionary(self, dictionary):
        """
        Zeigt das finale Wörterbuch (auf Anfrage)
        """
        print("\n=== FINALES WÖRTERBUCH ===")
        for key, value in sorted(dictionary.items(), key=lambda x: x[1]):
            print("{}: '{}'".format(value, key))

    def create_initial_dict_from_input(self):
        """
        Hilfsfunktion um Anfangswörterbuch vom Benutzer zu erstellen
        """
        print("\nWörterbuch wählen:")
        print("1=Auto 2=0-9 3=A-Z 4=a-z 5=Custom")

        choice = input("Option: ").strip()

        if choice == "1":
            return None  # Automatische Erkennung
        elif choice == "2":
            return [str(i) for i in range(10)]
        elif choice == "3":
            return [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        elif choice == "4":
            return [chr(i) for i in range(ord('a'), ord('z') + 1)]
        elif choice == "5":
            chars_input = input("Zeichen eingeben: ").strip()
            if chars_input:
                return list(chars_input)
            else:
                return [str(i) for i in range(10)]
        else:
            return [str(i) for i in range(10)]  # Default

    def run(self) -> None:
        """
        Hauptmenü für LZW-Funktionen
        """
        print("=== LZW ===")
        print("1=Dekodieren 2=Kodieren 0=Exit")

        subchoice = input("Option: ").strip()

        if subchoice == "1":
            # Dekodieren
            try:
                print("LZW-Codes (Leerzeichen getrennt):")
                data_str = input().strip()

                if not data_str:
                    print("Keine Eingabe!")
                    return

                encoded_data = list(map(int, data_str.split()))
                initial_dict = self.create_initial_dict_from_input()

                result = self.lzw_decode(encoded_data, initial_dict)
                print("Dekodiert: '{}'".format(result))

                # Optional: Details zeigen
                show_details = input("Details zeigen? (j/n): ").strip().lower()
                if show_details == 'j':
                    print("Codes: {}".format(len(encoded_data)))
                    print("Zeichen: {}".format(len(result)))

            except Exception as e:
                print("FEHLER: {}".format(str(e)))

        elif subchoice == "2":
            # Kodieren
            try:
                data = input("Text zum kodieren: ").strip()
                if not data:
                    print("Keine Eingabe!")
                    return

                initial_dict = self.create_initial_dict_from_input()

                # Kompakte Kodierung
                result, final_dict = self.encode_compact(data, initial_dict)

                if result is not None:
                    # Optionale Details
                    print("\nDetails zeigen?")
                    print("1=Schritte 2=Wörterbuch 3=Beide 0=Nein")
                    detail_choice = input("Option: ").strip()

                    if detail_choice == "1":
                        # Neue Kodierung für Schritte (da Dictionary verändert wurde)
                        temp_result = self.show_encoding_steps(data,
                                                               initial_dict.copy() if isinstance(initial_dict, dict)
                                                               else ({char: i for i, char in
                                                                      enumerate(initial_dict)} if initial_dict
                                                                     else {char: i for i, char in
                                                                           enumerate(sorted(set(data)))}))
                    elif detail_choice == "2":
                        self.show_final_dictionary(final_dict)
                    elif detail_choice == "3":
                        # Beide zeigen
                        temp_result = self.show_encoding_steps(data,
                                                               initial_dict.copy() if isinstance(initial_dict, dict)
                                                               else ({char: i for i, char in
                                                                      enumerate(initial_dict)} if initial_dict
                                                                     else {char: i for i, char in
                                                                           enumerate(sorted(set(data)))}))
                        self.show_final_dictionary(final_dict)

                    # Verifikation
                    decoded = self.lzw_decode(result, initial_dict)
                    if data != decoded:
                        print("WARNUNG: Verifikation fehlgeschlagen!")
                        print("Original: '{}'".format(data))
                        print("Dekodiert: '{}'".format(decoded))

            except Exception as e:
                print("FEHLER: {}".format(str(e)))

        else:
            print("Ungültige Option!")

        print("\nEnter für weiter...")
        input()


class InfoAnalyseTool(Tool):
    def __init__(self):
        self.symbols = []
        self.probs = []
        self.codes = []
        self.results = {}

    def clear_screen(self):
        """Simuliert clear screen für bessere Übersicht"""
        print("\n" * 5)

    def input_data(self):
        """Eingabe der Grunddaten"""
        print("=== Daten eingeben ===")
        try:
            n = int(input("Anzahl Symbole: "))
            if n <= 0:
                raise ValueError("Muss > 0 sein")

            self.symbols = []
            self.probs = []

            for i in range(n):
                sym = input("Symbol {}: ".format(i + 1))
                prob = float(input("P({}): ".format(sym)))
                if prob <= 0 or prob > 1:
                    raise ValueError("P muss 0 < P <= 1")
                self.symbols.append(sym)
                self.probs.append(prob)

            # Prüfe Summe
            total = sum(self.probs)
            if abs(total - 1.0) > 0.001:
                print("WARNUNG: Summe = {:.3f}".format(total))

            return True
        except Exception as e:
            print("Fehler: {}".format(str(e)))
            return False

    def calculate_all(self):
        """Berechnet alle wichtigen Werte"""
        if not self.probs:
            return False

        # Entropie
        h = -sum(p * math.log(p, 2) for p in self.probs if p > 0)

        # Redundanz Quelle
        n = len(self.symbols)
        h0 = math.log(n, 2)
        rq = h0 - h

        # Speichere Ergebnisse
        self.results = {
            'entropy': h,
            'h0': h0,
            'redundanz_quelle': rq,
            'n_symbols': n
        }

        return True

    def create_huffman(self):
        """Erstellt Huffman-Code"""
        if len(self.symbols) <= 1:
            return {"codes": {self.symbols[0]: "0"}, "avg_len": 1.0}

        # Nodes: [freq, symbol_or_list]
        nodes = [[p, s] for s, p in zip(self.symbols, self.probs)]

        while len(nodes) > 1:
            nodes.sort(key=lambda x: x[0])
            left = nodes.pop(0)
            right = nodes.pop(0)

            merged = [left[0] + right[0], [left, right]]
            nodes.append(merged)

        # Codes extrahieren
        codes = {}

        def assign_codes(node, code=""):
            if isinstance(node[1], str):  # Blatt
                codes[node[1]] = code if code else "0"
            else:  # Innerer Knoten
                assign_codes(node[1][0], code + "0")
                assign_codes(node[1][1], code + "1")

        assign_codes(nodes[0])

        # Mittlere Länge
        avg_len = sum(len(codes[s]) * p for s, p in zip(self.symbols, self.probs))

        return {"codes": codes, "avg_len": avg_len}

    def show_summary(self):
        """Zeigt Zusammenfassung"""
        if not self.results:
            print("Keine Daten!")
            return

        print("=== ZUSAMMENFASSUNG ===")
        print("Symbole: {}".format(len(self.symbols)))
        print("H(X): {:.3f} bit".format(self.results['entropy']))
        print("RQ: {:.3f} bit".format(self.results['redundanz_quelle']))

        # Huffman berechnen
        huff = self.create_huffman()
        rc_huff = huff['avg_len'] - self.results['entropy']
        print("L_Huff: {:.3f} bit".format(huff['avg_len']))
        print("RC_Huff: {:.3f} bit".format(rc_huff))

    def show_entropy_details(self):
        """Details zur Entropie"""
        print("=== ENTROPIE DETAILS ===")
        print("H(X) = -sum(p*log2(p))")
        print("")
        total = 0
        for s, p in zip(self.symbols, self.probs):
            term = -p * math.log(p, 2)
            total += term
            print("{}: {:.3f}*{:.3f}={:.3f}".format(s, p, math.log(p, 2), term))
        print("Sum: {:.6f} bit".format(total))

    def show_redundanz_details(self):
        """Details zur Redundanz"""
        print("=== REDUNDANZ DETAILS ===")
        print("H0 = log2(n) = {:.3f}".format(self.results['h0']))
        print("H(X) = {:.3f}".format(self.results['entropy']))
        print("RQ = H0-H(X) = {:.3f}".format(self.results['redundanz_quelle']))

    def show_huffman_details(self):
        """Details zum Huffman-Code"""
        print("=== HUFFMAN DETAILS ===")
        huff = self.create_huffman()

        for s in self.symbols:
            code = huff['codes'].get(s, "?")
            print("{}: {}".format(s, code))

        print("")
        print("Mittlere Länge:")
        total = 0
        for s, p in zip(self.symbols, self.probs):
            code_len = len(huff['codes'].get(s, ""))
            term = p * code_len
            total += term
            print("{}: {:.3f}*{}={:.3f}".format(s, p, code_len, term))
        print("L = {:.6f} bit".format(total))

    def encode_message(self):
        """Nachricht codieren"""
        if not self.symbols:
            print("Keine Daten!")
            return

        msg = input("Nachricht: ")
        huff = self.create_huffman()

        encoded = ""
        for char in msg:
            if char in huff['codes']:
                encoded += huff['codes'][char]
            else:
                print("Zeichen '{}' unbekannt!".format(char))
                return

        print("Codiert: {}".format(encoded))
        print("Länge: {} bit".format(len(encoded)))
        orig_len = len(msg) * math.ceil(math.log(len(self.symbols), 2))
        print("Original: {} bit".format(orig_len))
        if orig_len > 0:
            comp = len(encoded) / float(orig_len)
            print("Kompression: {:.1%}".format(comp))

    def run(self):
        """Hauptmenü"""
        while True:
            self.clear_screen()
            print("=== INFO ANALYSE ===")
            if self.symbols:
                print("Daten: {} Symbole".format(len(self.symbols)))
                print("")
                print("1) Zusammenfassung")
                print("2) Entropie Details")
                print("3) Redundanz Details")
                print("4) Huffman Details")
                print("5) Nachricht codieren")
                print("6) Neue Daten")
            else:
                print("Keine Daten vorhanden")
                print("")
                print("1) Daten eingeben")

            print("q) Beenden")
            print("")

            choice = input("Wahl: ").strip().lower()

            if choice == 'q':
                break
            elif choice == '1':
                if self.symbols:
                    self.show_summary()
                else:
                    if self.input_data():
                        self.calculate_all()
                        self.show_summary()
            elif choice == '2' and self.symbols:
                self.show_entropy_details()
            elif choice == '3' and self.symbols:
                self.show_redundanz_details()
            elif choice == '4' and self.symbols:
                self.show_huffman_details()
            elif choice == '5' and self.symbols:
                self.encode_message()
            elif choice == '6' and self.symbols:
                if self.input_data():
                    self.calculate_all()
            else:
                print("Ungültige Eingabe!")

            if choice != 'q':
                input("\nEnter zum Fortfahren...")

