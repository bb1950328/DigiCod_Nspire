import math

class Tool(object):
    # abstract
    def run(self) -> None:
        raise NotImplementedError("{} must implement run()".format(self.__class__.__name__))

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

class PlaceholderTool(Tool):
    def __init__(self, name):
        self.name = name

    def run(self) -> None:
        print("==== {} ====".format(self.name))
        print("Functionality for {} not yet implemented".format(self.name))
        print("\nDrücke Enter, um fortzufahren...")
        input()

class ToolNode(object):
    def __init__(self, nr: int, name: str) -> None:
        self.nr = nr
        self.name = name

class ToolGroup(ToolNode):
    def __init__(self, nr: int, name: str, tools: list) -> None:
        super().__init__(nr, name)
        self.tools = tools

class ToolEntry(ToolNode):
    def __init__(self, nr: int, name: str, cls) -> None:
        super().__init__(nr, name)
        self.cls = cls

TOOLS = [
    ToolGroup(1, "Entropie und Kompression", [
        ToolEntry(1, "Entropie berechnen", EntropyTool),
        ToolEntry(2, "Redundanz berechnen", RedundanzTool),
        ToolEntry(3, "Huffman-Code erstellen", HuffmanTool),
        ToolEntry(4, "Lauflängenkodierung (RLE)", RLETool),
        ToolEntry(5, "Lempel-Ziv LZ78", lambda: PlaceholderTool("Lempel-Ziv LZ78")),
        ToolEntry(6, "Lempel-Ziv LZ77", lambda: PlaceholderTool("Lempel-Ziv LZ77")),
    ]),
    
    # Rest of the TOOLS list remains unchanged
    ToolGroup(2, "RSA", [
        ToolEntry(1, "Schlüsselpaar erzeugen", lambda: PlaceholderTool("Schlüsselpaar erzeugen")),
        ToolEntry(2, "Verschlüsseln", lambda: PlaceholderTool("Verschlüsseln")),
        ToolEntry(3, "Entschlüsseln", lambda: PlaceholderTool("Entschlüsseln")),
    ]),
    
    ToolGroup(3, "Kanalcodierung", [
        ToolEntry(1, "Hamming-Distanz", lambda: PlaceholderTool("Hamming-Distanz")),
        ToolEntry(2, "Syndrom berechnen", lambda: PlaceholderTool("Syndrom berechnen")),
        ToolEntry(3, "CRC prüfen", lambda: PlaceholderTool("CRC prüfen")),
        ToolEntry(4, "CRC berechnen", lambda: PlaceholderTool("CRC berechnen")),
    ]),
    
    ToolGroup(4, "Faltungscode", [
        ToolEntry(1, "Faltungskodierung", lambda: PlaceholderTool("Faltungskodierung")),
        ToolEntry(2, "Viterbi-Dekodierung", lambda: PlaceholderTool("Viterbi-Dekodierung")),
    ]),
    
    ToolGroup(5, "Kanalmodell", [
        ToolEntry(1, "Transinformation", lambda: PlaceholderTool("Transinformation")),
        ToolEntry(2, "Maximum-Likelihood", lambda: PlaceholderTool("Maximum-Likelihood")),
    ]),
    
    ToolGroup(6, "Binärumrechnung", [
        ToolEntry(1, "Binär ↔ Dezimal", lambda: PlaceholderTool("Binär ↔ Dezimal")),
        ToolEntry(2, "Hexadezimal → Binär", lambda: PlaceholderTool("Hexadezimal → Binär")),
        ToolEntry(3, "2er-Komplement ↔ Dezimal", lambda: PlaceholderTool("2er-Komplement ↔ Dezimal")),
        ToolEntry(4, "Float → Binär", lambda: PlaceholderTool("Float → Binär")),
        ToolEntry(5, "IEEE-754 analysieren", lambda: PlaceholderTool("IEEE-754 analysieren")),
    ]),
]

def find_tool_by_path(path: list, tools: list):
    current_tools = tools
    current = None
    for p in path:
        try:
            current = next((t for t in current_tools if t.nr == p))
        except StopIteration:
            current = None
        if current is None:
            return None
        if isinstance(current, ToolGroup):
            current_tools = current.tools
    return current


def select_tool(tools) -> None:
    path = []

    while True:
        node = find_tool_by_path(path, tools) if path else None
        current_tools = tools if not path else node.tools if isinstance(node, ToolGroup) else []

        print()
        print("# Hauptmenü" if not path else "# {} {}".format(".".join(map(str, path)), node.name if node else ''))
        for t in current_tools:
            print("{} {}".format(t.nr, t.name))

        input_str = input("Nr: ").strip()

        if input_str == "":
            if path:
                path.pop()  # Go up one level
                continue
            else:
                return  # Exit menu

        try:
            parts = list(map(int, input_str.split(".")))
            full_path = parts if "." in input_str else path + parts

            result = find_tool_by_path(full_path, tools)
            if isinstance(result, ToolEntry):
                print()
                instance = result.cls()
                instance.run()
            elif isinstance(result, ToolGroup):
                path = full_path
            else:
                print("Ungültige Eingabe.")
        except ValueError:
            print("Bitte eine gültige Nummer oder Pfad eingeben (z.B. 1 oder 1.2).")


def main():
    select_tool(TOOLS)

main()