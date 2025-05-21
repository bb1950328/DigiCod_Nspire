import tools_entropy_compression
import tools_rsa
import tool_base
import tools_channel_coding
import tools_convolutional_code
import channel_model


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
        tool_base.ToolEntry(1, "Faltungskodierung", tools_convolutional_code.ConvolutionalEncodeTool),
        tool_base.ToolEntry(2, "Viterbi-Dekodierung", tools_convolutional_code.ViterbiDecodeTool),
    ]),
    
    tool_base.ToolGroup(5, "Kanalmodell", [
        tool_base.ToolEntry(1, "Transinformation", channel_model.TransinformationTool),
        tool_base.ToolEntry(2, "Maximum-Likelihood", channel_model.MaximumLikelihoodTool),
    ]),
    
    tool_base.ToolGroup(6, "Binärumrechnung", [
        tool_base.ToolEntry(1, "Binär ↔ Dezimal", lambda: tool_base.PlaceholderTool("Binär ↔ Dezimal")),
        tool_base.ToolEntry(2, "Hexadezimal → Binär", lambda: tool_base.PlaceholderTool("Hexadezimal → Binär")),
        tool_base.ToolEntry(3, "2er-Komplement ↔ Dezimal", lambda: tool_base.PlaceholderTool("2er-Komplement ↔ Dezimal")),
        tool_base.ToolEntry(4, "Float → Binär", lambda: tool_base.PlaceholderTool("Float → Binär")),
        tool_base.ToolEntry(5, "IEEE-754 analysieren", lambda: tool_base.PlaceholderTool("IEEE-754 analysieren")),
    ]),
]