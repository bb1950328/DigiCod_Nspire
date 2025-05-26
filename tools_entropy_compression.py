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
        return {sym: code for sym, code in nodes[0][1:]}

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
            for sym, code in huffman_code.items():
                print("{}: {}".format(sym, code))

            # Calculate average code length
            avg_length = sum(len(code) * freq for (sym, code), freq in zip(huffman_code.items(), freqs)) / sum(freqs)
            print("\nDurchschnittliche Codewortlänge: {:.6f} bits/Symbol".format(avg_length))

        except Exception as e:
            print("Fehler: {}".format(str(e)))

        print("\nDrücke Enter, um fortzufahren...")
        input()


class RLETool(Tool):
    def run_length_encode(self, data):
        """Führt eine Lauflängenkodierung der Eingabedaten durch"""
        if not data:
            return []

        encoded = []
        count = 1
        current = data[0]

        for i in range(1, len(data)):
            if data[i] == current:
                count += 1
            else:
                encoded.append((current, count))
                current = data[i]
                count = 1

        # Füge das letzte Element hinzu
        encoded.append((current, count))
        return encoded

    def run_length_decode(self, encoded_data):
        """Dekodiert eine lauflängenkodierte Sequenz"""
        decoded = []
        for symbol, count in encoded_data:
            decoded.extend([symbol] * count)
        return decoded

    def run(self) -> None:
        print("==== Lauflängenkodierung (RLE) ====")
        try:
            inp_type = input("Eingabetyp (text/binär): ").strip().lower()

            if inp_type == "text":
                inp_data = input("Geben Sie den zu kodierenden Text ein: ")
                original_data = list(inp_data)
            elif inp_type == "binär" or inp_type == "binär":
                inp_data = input("Geben Sie die Binärsequenz ein (nur 0 und 1): ")
                if not all(bit in "01" for bit in inp_data):
                    raise ValueError("Binärsequenz darf nur 0 und 1 enthalten")
                original_data = list(inp_data)
            else:
                raise ValueError("Ungültiger Eingabetyp. Bitte 'text' oder 'binär' eingeben.")

            encoded = self.run_length_encode(original_data)

            print("\nEingabe:")
            print("".join(original_data))

            print("\nLauflängenkodiert:")
            if inp_type == "text":
                for symbol, count in encoded:
                    print("{}:{}".format(symbol, count), end=" ")
            else:
                for symbol, count in encoded:
                    print("{}×{}".format(symbol, count), end=" ")

            # Berechne Kompressionsrate
            original_size = len(original_data)
            # Bei binärer Eingabe müssen wir abschätzen, wie viele Bits pro Paar benötigt werden
            if inp_type == "binär" or inp_type == "binär":
                # Ein Bit für das Symbol und log2(max_count) Bits für die Anzahl
                max_count = max(count for _, count in encoded)
                bits_for_count = max(1, math.ceil(math.log2(max_count)))
                encoded_size = len(encoded) * (1 + bits_for_count)
            else:
                # Grobe Abschätzung: 8 Bits pro Zeichen + Bits für die Anzahl
                encoded_size = sum(8 + math.ceil(math.log2(max(1, count))) for _, count in encoded)

            compression_ratio = original_size / encoded_size if encoded_size > 0 else float('inf')

            print("\n\nKompressionsrate: {:.2f}".format(compression_ratio))
            print("Original: {} Einheiten".format(original_size))
            print("Kodiert: ~ {} Einheiten".format(encoded_size))

            # Dekodiere zur Überprüfung
            decoded = self.run_length_decode(encoded)
            if decoded == original_data:
                print("\nÜberprüfung: Die Dekodierung stimmt mit der Originaleingabe überein.")
            else:
                print("\nWarnung: Die Dekodierung stimmt nicht mit der Originaleingabe überein!")

        except Exception as e:
            print("Fehler: {}".format(str(e)))

        print("\nDrücke Enter, um fortzufahren...")
        input()


class LZW(Tool):

    def lzw_encode(self, data, initial_dict=None):  # ← 'self' hinzugefügt
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

    def lzw_decode(self, encoded_data, initial_dict=None):  # ← 'self' hinzugefügt
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

    def print_encoding_steps(self, data, initial_dict=None):  # ← 'self' hinzugefügt
        """
        Zeigt die Schritte der LZW-Kodierung mit optionalem Anfangswörterbuch
        """
        # Initialisiere Wörterbuch
        if initial_dict is None:
            # Automatisch alle eindeutigen Zeichen aus der Eingabe verwenden
            unique_chars = sorted(set(data))
            dictionary = {char: i for i, char in enumerate(unique_chars)}
            print("Automatisches Wörterbuch für Zeichen: {}".format(unique_chars))
        elif isinstance(initial_dict, list):
            dictionary = {char: i for i, char in enumerate(initial_dict)}
            print("Anfangswörterbuch aus Liste: {}".format(initial_dict))
        elif isinstance(initial_dict, dict):
            dictionary = initial_dict.copy()
            print("Vorgegebenes Wörterbuch: {}".format(initial_dict))
        else:
            raise ValueError("initial_dict muss None, Liste oder Dictionary sein")

        print("Eingabe: {}".format(data))
        print("Startwörterbuch: {}".format(dictionary))
        print("\nKodierungsschritte:")
        print("Buffer | Erkannte Zeichenfolge (Index) | Neuer Eintrag")
        print("-" * 60)

        result = []
        current_string = ""
        buffer_pos = 0

        for i, char in enumerate(data):
            buffer = data[buffer_pos:i + 1]
            new_string = current_string + char

            if new_string in dictionary:
                current_string = new_string
            else:
                # Ausgabe
                index = dictionary[current_string] if current_string else None
                if index is not None:
                    result.append(index)
                    next_entry_index = len(dictionary)
                    print("{}   | {} ({}){}| → {}: {}".format(
                        buffer.ljust(6),
                        current_string,
                        index,
                        ' ' * (20 - len(current_string) - len(str(index))),
                        next_entry_index,
                        new_string
                    ))
                    dictionary[new_string] = next_entry_index

                current_string = char
                buffer_pos = i

        # Letzter Eintrag
        if current_string:
            index = dictionary[current_string]
            result.append(index)
            print("{}   | {} ({})".format(data[buffer_pos:].ljust(6), current_string, index))

        print("\nKodierte Nachricht: {}".format(' '.join(map(str, result))))

        # Zeige finales Wörterbuch
        print("\nFinales Wörterbuch:")
        for key, value in sorted(dictionary.items(), key=lambda x: x[1]):
            print("Index {}: '{}'".format(value, key))

        return result, dictionary

    def create_initial_dict_from_input(self):
        """
        Hilfsfunktion um Anfangswörterbuch vom Benutzer zu erstellen
        """
        print("\n==== Anfangswörterbuch wählen ====")
        print("1. Automatisch aus Eingabe")
        print("2. Ziffern 0-9 (Standard)")
        print("3. Buchstaben A-Z")
        print("4. Kleinbuchstaben a-z")
        print("5. Benutzerdefiniert")

        choice = input("Wähle eine Option (1-5): ").strip()
        print("Gewählte Option: {}".format(choice))  # Debug-Ausgabe

        if choice == "1":
            print("→ Automatische Erkennung gewählt")
            return None  # Automatische Erkennung
        elif choice == "2":
            print("→ Ziffern 0-9 gewählt")
            return [str(i) for i in range(10)]
        elif choice == "3":
            print("→ Buchstaben A-Z gewählt")
            return [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        elif choice == "4":
            print("→ Kleinbuchstaben a-z gewählt")
            return [chr(i) for i in range(ord('a'), ord('z') + 1)]
        elif choice == "5":
            print("→ Benutzerdefiniert gewählt")
            chars_input = input("Zeichen eingeben (ohne Leerzeichen, z.B. 'abcd123'): ").strip()
            if chars_input:
                custom_dict = list(chars_input)
                print("Benutzerdefiniertes Wörterbuch: {}".format(custom_dict))
                return custom_dict
            else:
                print("Keine Eingabe - verwende Standard (Ziffern 0-9)")
                return [str(i) for i in range(10)]
        else:
            print("Ungültige Eingabe '{}' - verwende Standard (Ziffern 0-9)".format(choice))
            return [str(i) for i in range(10)]  # Default

    def run(self) -> None:
        """
        Hauptmenü für LZW-Funktionen
        """
        print("==== Lempel-Ziv-Welch (LZW) ====")
        print("1. Dekodieren")
        print("2. Kodieren")
        print("0. Exit")

        subchoice = input("\nWähle eine Option: ")
        # DEBUG: Zeige was tatsächlich eingegeben wurde
        print("DEBUG: Eingabe roh: '{}'".format(repr(subchoice)))
        print("DEBUG: Eingabe Länge: {}".format(len(subchoice)))

        # Robust behandeln
        subchoice = str(subchoice).strip()
        print("DEBUG: Nach strip(): '{}'".format(repr(subchoice)))

        # Explizite Vergleiche mit Debug
        print("DEBUG: subchoice == '1'? {}".format(subchoice == "1"))
        print("DEBUG: subchoice == '2'? {}".format(subchoice == "2"))
        print("DEBUG: subchoice == '0'? {}".format(subchoice == "0"))


        if  subchoice == "1":
            # Dekodieren
            try:
                print("Eingabe (LZW-Codes durch Leerzeichen getrennt):")
                print("Beispiel: 1 2 3 10 12 11 13")
                data_str = input().strip()

                if not data_str:
                    print("Keine Eingabe erhalten!")
                    return

                encoded_data = list(map(int, data_str.split()))
                print("Codes erhalten: {}".format(encoded_data))

                initial_dict = self.create_initial_dict_from_input()
                print("Dekodierungs-Wörterbuch: {}".format(initial_dict))

                result = self.lzw_decode(encoded_data, initial_dict)
                print("\nDekodiert: '{}'".format(result))
                print("Anzahl Codes eingegeben: {}".format(len(encoded_data)))
                print("Anzahl Zeichen dekodiert: {}".format(len(result)))

                # Zeige Dekodierungs-Wörterbuch
                if initial_dict is None:
                    print("WARNUNG: Automatisches Wörterbuch bei Dekodierung nicht möglich!")
                    print("Verwende Standard: Ziffern 0-9")
                else:
                    print("Verwendetes Dekodierungs-Wörterbuch:")
                    for i, char in enumerate(initial_dict):
                        print("  {}: '{}'".format(i, char))

            except Exception as e:
                print("Fehler: {}".format(str(e)))
                import traceback
                traceback.print_exc()

        elif subchoice == "2":
            # Schritt-für-Schritt Anzeige
            try:
                data = input("Eingabe (codewort zum kodieren): ")
                print("Eingabe erhalten: '{}'".format(data))

                initial_dict = self.create_initial_dict_from_input()
                print("Gewähltes Wörterbuch für Schritt-Anzeige: {}".format(initial_dict))

                print("\n{}".format('=' * 60))
                result, final_dict = self.print_encoding_steps(data, initial_dict)
                print("{}".format('=' * 60))

                # Test der Dekodierung
                decoded = self.lzw_decode(result, initial_dict)
                print("\nVerifikation:")
                print("Original:   '{}'".format(data))
                print("Dekodiert:  '{}'".format(decoded))
                print("Korrekt:    {}".format('✓' if data == decoded else '✗'))

                # Kompressionsrate
                if result:
                    # Berechne Bits für Original
                    if initial_dict is None:
                        alphabet_size = len(set(data))
                        print("Automatisches Alphabet: {} (Größe: {})".format(sorted(set(data)), alphabet_size))
                    elif isinstance(initial_dict, list):
                        alphabet_size = len(initial_dict)
                        print("Verwendetes Alphabet: {} (Größe: {})".format(initial_dict, alphabet_size))
                    else:
                        alphabet_size = len(initial_dict)
                        print("Dictionary-Alphabet (Größe: {})".format(alphabet_size))

                    bits_per_char = max(1, alphabet_size.bit_length())
                    original_bits = len(data) * bits_per_char

                    # Berechne Bits für komprimierte Version
                    max_index = max(result) if result else 0
                    bits_per_code = max(bits_per_char, max_index.bit_length())
                    compressed_bits = len(result) * bits_per_code

                    compression_ratio = (1 - compressed_bits / original_bits) * 100 if original_bits > 0 else 0

                    print("\nKompression:")
                    print("Alphabet-Größe: {} (benötigt {} Bit pro Zeichen)".format(alphabet_size, bits_per_char))
                    print("Original: {} Bits ({} Zeichen × {} Bit)".format(original_bits, len(data), bits_per_char))
                    print(
                        "Komprimiert: {} Bits ({} Codes × {} Bit)".format(compressed_bits, len(result), bits_per_code))
                    print("Kompressionsrate: {:.1f}%".format(compression_ratio))



            except Exception as e:
                print("Fehler: {}".format(str(e)))
                import traceback
                traceback.print_exc()

        else:
            print("Ungültige Option gewählt!")

        print("\nDrücke Enter, um fortzufahren...")
        input()

