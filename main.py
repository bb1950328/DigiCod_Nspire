import math

class Tool(object):
    # abstract
    def run(self) -> None:
        raise NotImplementedError(f"{self.__class__.__name__} must implement run()")

class EntropyTool(Tool):
    def run(self) -> None:
        print("==== Entropie berechnen ====")
        try:
            n = int(input("Anzahl der Symbole: "))
            probs = []
            for i in range(n):
                p = float(input(f"Wahrscheinlichkeit für Symbol {i + 1}: "))
                probs.append(p)

            result = -sum(p * math.log2(p) for p in probs if p > 0)
            print(f"\nEntropie: {result:.6f} bits/Symbol")
        except Exception as e:
            print(f"Fehler: {str(e)}")
            
        print("\nDrücke Enter, um fortzufahren...")
        input()

class PlaceholderTool(Tool):
    def __init__(self, name):
        self.name = name

    def run(self) -> None:
        print(f"==== {self.name} ====")
        print(f"Functionality for {self.name} not yet implemented")
        print("\nDrücke Enter, um fortzufahren...")
        input()

class ToolNode(object):
    def __init__(self, nr: int, name: str) -> None:
        self.nr = nr
        self.name = name

class ToolGroup(ToolNode):
    def __init__(self, nr: int, name: str, tools: list[ToolNode]) -> None:
        super().__init__(nr, name)
        self.tools = tools

class ToolEntry(ToolNode):
    def __init__(self, nr: int, name: str, cls) -> None:
        super().__init__(nr, name)
        self.cls = cls

TOOLS = [
    ToolGroup(1, "Entropie und Kompression", [
        ToolEntry(1, "Entropie berechnen", EntropyTool),
        ToolEntry(2, "Redundanz berechnen", lambda: PlaceholderTool("Redundanz berechnen")),
        ToolEntry(3, "Huffman-Code erstellen", lambda: PlaceholderTool("Huffman-Code erstellen")),
        ToolEntry(4, "Lauflängenkodierung (RLE)", lambda: PlaceholderTool("Lauflängenkodierung (RLE)")),
        ToolEntry(5, "Lempel-Ziv LZ78", lambda: PlaceholderTool("Lempel-Ziv LZ78")),
        ToolEntry(6, "Lempel-Ziv LZ77", lambda: PlaceholderTool("Lempel-Ziv LZ77")),
    ]),
    
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

def find_tool_by_path(path: list[int], tools: list[ToolNode]) -> ToolEntry | ToolGroup | None:
    current_tools = tools
    current = None
    for p in path:
        current = next((t for t in current_tools if t.nr == p), None)
        if current is None:
            return None
        if isinstance(current, ToolGroup):
            current_tools = current.tools
    return current


def select_tool(tools: list[ToolNode]) -> None:
    path: list[int] = []

    while True:
        node = find_tool_by_path(path, tools) if path else None
        current_tools = tools if not path else node.tools if isinstance(node, ToolGroup) else []

        print()
        print("# Hauptmenü" if not path else f"# {'.'.join(map(str, path))} {node.name if node else ''}")
        for t in current_tools:
            print(f"{t.nr} {t.name}")

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

if __name__ == "__main__":
    main()