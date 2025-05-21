import tools_entropy_compression
import tools_rsa
import tool_base
import tools_channel_coding


TOOLS = [
    tool_base.ToolGroup(1, "Entropie und Kompression", [
        tool_base.ToolEntry(1, "Entropie berechnen", tools_entropy_compression.EntropyTool),
        tool_base.ToolEntry(2, "Redundanz berechnen", tools_entropy_compression.RedundanzTool),
        tool_base.ToolEntry(3, "Huffman-Code erstellen", tools_entropy_compression.HuffmanTool),
        tool_base.ToolEntry(4, "Lauflängenkodierung (RLE)", tools_entropy_compression.RLETool),
        tool_base.ToolEntry(5, "Lempel-Ziv LZ78", tools_entropy_compression.LZ78Tool),
        tool_base.ToolEntry(6, "Lempel-Ziv LZ77", tools_entropy_compression.LZ77Tool),
    ]),
    
    tool_base.ToolGroup(2, "RSA", [
        tool_base.ToolEntry(1, "Schlüsselpaar erzeugen", tools_rsa.KeyGenerationTool),
        tool_base.ToolEntry(2, "Verschlüsseln", tools_rsa.EncryptionTool),
        tool_base.ToolEntry(3, "Entschlüsseln", tools_rsa.DecryptionTool),
    ]),
    
    tool_base.ToolGroup(3, "Kanalcodierung", [
        tool_base.ToolEntry(1, "Hamming-Distanz", tools_channel_coding.HammingDistanceTool),
        tool_base.ToolEntry(2, "Syndrom berechnen", tools_channel_coding.SyndromeTool),
        tool_base.ToolEntry(3, "CRC prüfen", tools_channel_coding.CRCCheckTool),
        tool_base.ToolEntry(4, "CRC berechnen", tools_channel_coding.CRCCalculationTool),
    ]),
    
    tool_base.ToolGroup(4, "Faltungscode", [
        tool_base.ToolEntry(1, "Faltungskodierung", lambda: tool_base.PlaceholderTool("Faltungskodierung")),
        tool_base.ToolEntry(2, "Viterbi-Dekodierung", lambda: tool_base.PlaceholderTool("Viterbi-Dekodierung")),
    ]),
    
    tool_base.ToolGroup(5, "Kanalmodell", [
        tool_base.ToolEntry(1, "Transinformation", lambda: tool_base.PlaceholderTool("Transinformation")),
        tool_base.ToolEntry(2, "Maximum-Likelihood", lambda: tool_base.PlaceholderTool("Maximum-Likelihood")),
    ]),
    
    tool_base.ToolGroup(6, "Binärumrechnung", [
        tool_base.ToolEntry(1, "Binär ↔ Dezimal", lambda: tool_base.PlaceholderTool("Binär ↔ Dezimal")),
        tool_base.ToolEntry(2, "Hexadezimal → Binär", lambda: tool_base.PlaceholderTool("Hexadezimal → Binär")),
        tool_base.ToolEntry(3, "2er-Komplement ↔ Dezimal", lambda: tool_base.PlaceholderTool("2er-Komplement ↔ Dezimal")),
        tool_base.ToolEntry(4, "Float → Binär", lambda: tool_base.PlaceholderTool("Float → Binär")),
        tool_base.ToolEntry(5, "IEEE-754 analysieren", lambda: tool_base.PlaceholderTool("IEEE-754 analysieren")),
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
        if isinstance(current, tool_base.ToolGroup):
            current_tools = current.tools
    return current


def select_tool(tools) -> None:
    path = []

    while True:
        node = find_tool_by_path(path, tools) if path else None
        current_tools = tools if not path else node.tools if isinstance(node, tool_base.ToolGroup) else []

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
            if isinstance(result, tool_base.ToolEntry):
                print()
                instance = result.cls()
                instance.run()
            elif isinstance(result, tool_base.ToolGroup):
                path = full_path
            else:
                print("Ungültige Eingabe.")
        except ValueError:
            print("Bitte eine gültige Nummer oder Pfad eingeben (z.B. 1 oder 1.2).")


def main():
    select_tool(TOOLS)

main()