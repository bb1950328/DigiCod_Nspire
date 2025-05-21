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


class LZ78Tool(Tool):
    def lz78_encode(self, data):
        """Implementiert LZ78-Kompression für eine Zeichenfolge"""
        dictionary = {"": 0}  # Leerer String hat Index 0
        result = []
        w = ""

        for c in data:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                # Ausgabe: (Index von w, nächstes Zeichen c)
                result.append((dictionary[w], c))
                # Füge wc zum Dictionary hinzu
                dictionary[wc] = len(dictionary)
                w = ""

        # Füge verbleibende Zeichen hinzu, falls vorhanden
        if w:
            result.append((dictionary[w], ""))

        return result, dictionary

    def lz78_decode(self, encoded_data, dictionary_size):
        """Dekodiert LZ78-komprimierte Daten"""
        # Erstelle ein inverses Dictionary mit Indizes als Schlüssel
        dictionary = {0: ""}
        result = []

        for index, char in encoded_data:
            if index in dictionary:
                w = dictionary[index]
                if char:  # Falls char nicht leer ist
                    word = w + char
                else:
                    word = w
                result.append(word)
                dictionary[len(dictionary)] = word
            else:
                # Dieser Fall sollte theoretisch nicht eintreten
                print("Warnung: Ungültiger Index {} im kodierten Datenstrom.".format(index))

        return "".join(result)

    def run(self) -> None:
        print("==== Lempel-Ziv LZ78 ====")
        try:
            input_text = input("Geben Sie den zu komprimierenden Text ein: ")

            # Kodieren
            encoded_data, dictionary = self.lz78_encode(input_text)

            # Ausgabe des Kodierungsergebnisses
            print("\nEingabetext: {}".format(input_text))
            print("\nKodiertes Ergebnis:")
            for index, char in encoded_data:
                print("({}, '{}')".format(index, char), end=" ")

            # Dictionary-Größe und Kompressionsrate berechnen
            original_size = len(input_text) * 8  # Annahme: 8 Bits pro Zeichen

            # Berechne die ungefähre Größe des kodierten Ergebnisses in Bits
            max_index = max(index for index, _ in encoded_data) if encoded_data else 0
            bits_for_index = max(1, math.ceil(math.log2(max_index + 1))) if max_index > 0 else 1

            # 8 Bits für jeden Zeichencode + bits_for_index für den Index
            encoded_size = sum(bits_for_index + (8 if char else 0) for _, char in encoded_data)

            print("\n\nDictionary-Größe: {} Einträge".format(len(dictionary)))
            print("Original: ~{} Bits (8 Bits pro Zeichen)".format(original_size))
            print("Kodiert: ~{} Bits".format(encoded_size))

            compression_ratio = original_size / encoded_size if encoded_size > 0 else float('inf')
            print("Kompressionsrate: {:.2f}".format(compression_ratio))

            # Dekodieren zur Überprüfung
            decoded_text = self.lz78_decode(encoded_data, len(dictionary))

            if decoded_text == input_text:
                print("\nÜberprüfung: Die Dekodierung stimmt mit der Originaleingabe überein.")
            else:
                print("\nWarnung: Die Dekodierung stimmt nicht mit der Originaleingabe überein!")
                print("Dekodiert: {}".format(decoded_text))

        except Exception as e:
            print("Fehler: {}".format(str(e)))

        print("\nDrücke Enter, um fortzufahren...")
        input()


class LZ77Tool(Tool):
    def find_longest_match(self, data, cursor, window_size, lookahead_size):
        """Findet die längste Übereinstimmung im Suchfenster"""
        end_of_buffer = min(cursor + lookahead_size, len(data))

        # Falls wir am Ende der Daten angekommen sind
        if cursor >= len(data):
            return 0, 0, ""

        # Berechne die Suche im Fenster
        search_start = max(0, cursor - window_size)
        search_window = data[search_start:cursor]
        lookahead = data[cursor:end_of_buffer]

        match_length = 0
        match_offset = 0
        next_char = ""

        # Länge 0, wenn keine Übereinstimmung gefunden
        if not lookahead:
            return match_offset, match_length, next_char

        # Der Fall, wenn keine Übereinstimmung gefunden wird
        next_char = lookahead[0]

        # Suche nach Übereinstimmungen
        for i in range(len(search_window), 0, -1):
            pattern = search_window[i - 1:]
            length = 0

            # Finde die längste Übereinstimmung
            for j in range(min(len(pattern), len(lookahead))):
                if pattern[j] != lookahead[j]:
                    break
                length += 1

            # Wenn wir eine längere Übereinstimmung gefunden haben
            if length > match_length:
                match_length = length
                match_offset = len(search_window) - i + 1

        # Nur wenn wir mindestens ein Zeichen kodieren
        if match_length > 0:
            if cursor + match_length < len(data):
                next_char = data[cursor + match_length]
            else:
                next_char = ""

        return match_offset, match_length, next_char

    def lz77_encode(self, data, window_size=10, lookahead_size=5):
        """Implementiert LZ77-Kompression"""
        result = []
        cursor = 0

        while cursor < len(data):
            offset, length, next_char = self.find_longest_match(data, cursor, window_size, lookahead_size)
            result.append((offset, length, next_char))
            cursor += length + 1  # +1 wegen des zusätzlichen Zeichens

        return result

    def lz77_decode(self, encoded_data):
        """Dekodiert LZ77-komprimierte Daten"""
        result = []

        for offset, length, next_char in encoded_data:
            # Hole bereits dekodierte Zeichen aus dem "Fenster"
            if offset > 0 and length > 0:
                start = len(result) - offset
                for i in range(length):
                    if start + i >= 0 and start + i < len(result):
                        result.append(result[start + i])
                    else:
                        # This handles repetitions that exceed the available window
                        # For example, when we need to repeat 'A' 3 times but only have
                        # one 'A' in the window, we keep appending 'A' as we decode
                        if result:
                            result.append(result[-1])

            # Füge das nächste Zeichen hinzu, wenn es existiert
            if next_char:
                result.append(next_char)

        return "".join(result)

    def run(self) -> None:
        print("==== Lempel-Ziv LZ77 ====")
        try:
            input_text = input("Geben Sie den zu komprimierenden Text ein: ")
            window_size = int(input("Fenstergröße (Standard: 10): ") or "10")
            lookahead_size = int(input("Vorschaugröße (Standard: 5): ") or "5")

            # Kodieren
            encoded_data = self.lz77_encode(input_text, window_size, lookahead_size)

            # Ausgabe des Kodierungsergebnisses
            print("\nEingabetext: {}".format(input_text))
            print("\nKodiertes Ergebnis (Offset, Länge, Nächstes Zeichen):")
            for offset, length, next_char in encoded_data:
                print("({}, {}, '{}')".format(offset, length, next_char), end=" ")

            # Berechne Kompressionsrate
            original_size = len(input_text) * 8  # Annahme: 8 Bits pro Zeichen

            # Berechne die ungefähre Größe des kodierten Ergebnisses in Bits
            bits_for_offset = math.ceil(math.log2(window_size + 1)) if window_size > 0 else 1
            bits_for_length = math.ceil(math.log2(lookahead_size + 1)) if lookahead_size > 0 else 1

            # bits_for_offset + bits_for_length + 8 Bits für das nächste Zeichen
            encoded_size = sum(bits_for_offset + bits_for_length + (8 if char else 0) for _, _, char in encoded_data)

            print("\n\nOriginal: ~{} Bits (8 Bits pro Zeichen)".format(original_size))
            print("Kodiert: ~{} Bits".format(encoded_size))

            compression_ratio = original_size / encoded_size if encoded_size > 0 else float('inf')
            print("Kompressionsrate: {:.2f}".format(compression_ratio))

            # Dekodieren zur Überprüfung
            decoded_text = self.lz77_decode(encoded_data)

            if decoded_text == input_text:
                print("\nÜberprüfung: Die Dekodierung stimmt mit der Originaleingabe überein.")
            else:
                print("\nWarnung: Die Dekodierung stimmt nicht mit der Originaleingabe überein!")
                print("Dekodiert: {}".format(decoded_text))

        except Exception as e:
            print("Fehler: {}".format(str(e)))

        print("\nDrücke Enter, um fortzufahren...")
        input()
