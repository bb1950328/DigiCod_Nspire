import tools_entropy_compression
import tools_rsa
import tool_base
import tools_channel_coding
import tools_convolutional_code
import channel_model
import tools_binary_conversion



TOOLS = [
    tool_base.ToolGroup(1, "Entropie und Kompression", [
        tool_base.ToolEntry(1, "Entropie berechnen", tools_entropy_compression.EntropyTool),
        tool_base.ToolEntry(2, "Redundanz berechnen", tools_entropy_compression.RedundanzTool),
        tool_base.ToolEntry(3, "Huffman-Code erstellen", tools_entropy_compression.HuffmanTool),
        tool_base.ToolEntry(4, "Lauflängenkodierung (RLE)", tools_entropy_compression.RLETool),
        tool_base.ToolEntry(5, "Lempel-Ziv LZW", tools_entropy_compression.LZW),
        tool_base.ToolEntry(6, "Vollständige Analyse", tools_entropy_compression.InfoAnalyseTool),
    ]),

    tool_base.ToolGroup(2, "RSA", [
        tool_base.ToolEntry(1, "RSA", tools_rsa.RSA),
    ]),

    tool_base.ToolGroup(3, "Kanalcodierung", [
        tool_base.ToolEntry(1, "Blockcode: Analyse",tools_channel_coding.ComprehensiveCodeAnalysisTool),
        tool_base.ToolEntry(2, "Blockcode: Eigenschaften",tools_channel_coding.CodePropertiesAnalysisTool),
        tool_base.ToolEntry(3, "Prüfmatrix H:", tools_channel_coding.ParityMatrixTool),
        tool_base.ToolEntry(4, "Zyklischer Code: g(x) zu Matrix",tools_channel_coding.CyclicCodeAnalysisTool),
        tool_base.ToolEntry(5, "CRC: Prüfbits mit g(x) berechnen & Codewort erstellen",tools_channel_coding.CRCCalculationTool),
        tool_base.ToolEntry(6, "CRC: Empfangenes Wort mit g(x) prüfen", tools_channel_coding.CRCCheckTool),
        tool_base.ToolEntry(7, "Polynomdivision", tools_channel_coding.PolynomialDivisionTool),
        tool_base.ToolEntry(8, "Hamming-Distanz berechnen", tools_channel_coding.HammingDistanceTool),
        tool_base.ToolEntry(9, "Code-Parameter & Dichtgepacktheit",tools_channel_coding.CodeParametersAndBoundsTool),  # Neuer/Angepasster Eintrag

    ]),

    tool_base.ToolGroup(4, "Faltungscode", [
        tool_base.ToolEntry(1, "Faltungskodierung", tools_convolutional_code.ConvolutionalEncodeTool),
        tool_base.ToolEntry(2, "Viterbi-Dekodierung", tools_convolutional_code.ViterbiDecodeTool),
    ]),

    tool_base.ToolGroup(5, "Kanalmodell", [
        tool_base.ToolEntry(1, "Transinformation", channel_model.TransinformationTool),
        tool_base.ToolEntry(2, "Maximum-Likelihood", channel_model.MaximumLikelihoodTool),
        tool_base.ToolEntry(3, "Entropie berechnen", channel_model.EntropyCalculationTool),
        tool_base.ToolEntry(4, "Binärer symmetrischer Kanal", channel_model.BinarySymmetricChannelTool),
        tool_base.ToolEntry(5, "Kanalmatrix bestimmen", channel_model.ChannelMatrixDeterminationTool),
        tool_base.ToolEntry(6, "Kanaltyp analysieren", channel_model.ChannelTypeAnalysisTool),
        tool_base.ToolEntry(7, "Vollständige Kanalanalyse", channel_model.ComprehensiveChannelAnalysisTool),
    ]),

    tool_base.ToolGroup(6, "Umrechnungen", [
        tool_base.ToolEntry(1, "Binär", tools_binary_conversion.BinaryConverter),
        tool_base.ToolEntry(2, "Dezimal", tools_binary_conversion.DecimalConverter),
        tool_base.ToolEntry(3, "Hexadezimal", tools_binary_conversion.HexConverter),
        tool_base.ToolEntry(4, "2er-Komplement", tools_binary_conversion.TwosComplementConverter),
        tool_base.ToolEntry(5, "Fixkommazahl", tools_binary_conversion.FixedPointConverter),
        tool_base.ToolEntry(6, "Float", tools_binary_conversion.FloatConverter),
        tool_base.ToolEntry(7, "Exzess", tools_binary_conversion.ExcessConverter),
        tool_base.ToolEntry(8, "Oktal", tools_binary_conversion.OctalConverter),
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
