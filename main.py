import math

from entropy_compression_tools import *
from rsa_tools import KeyGenerationTool, EncryptionTool, DecryptionTool


TOOLS = [
    ToolGroup(1, "Entropie und Kompression", [
        ToolEntry(1, "Entropie berechnen", EntropyTool),
        ToolEntry(2, "Redundanz berechnen", RedundanzTool),
        ToolEntry(3, "Huffman-Code erstellen", HuffmanTool),
        ToolEntry(4, "Lauflängenkodierung (RLE)", RLETool),
        ToolEntry(5, "Lempel-Ziv LZ78", LZ78Tool),
        ToolEntry(6, "Lempel-Ziv LZ77", LZ77Tool),
    ]),
    
    ToolGroup(2, "RSA", [
        ToolEntry(1, "Schlüsselpaar erzeugen", KeyGenerationTool),
        ToolEntry(2, "Verschlüsseln", EncryptionTool),
        ToolEntry(3, "Entschlüsseln", DecryptionTool),
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