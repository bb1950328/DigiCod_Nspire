"""
ICTh Prüfungstool für TI nspire CX II
Dieses Tool enthält nützliche Funktionen für die ICTh-Prüfung.
"""

import math

# Globale Variablen für Rückkehr zum Hauptmenü
main_menu_active = True
current_menu = "main"


#####################
# Hilfsfunktionen #
#####################

def clear_screen():
    """Löscht den Bildschirm"""
    print("\n" * 10)


def pause():
    """Pausiert das Programm bis Benutzer eine Taste drückt"""
    input("\nDrücke Enter zum Fortfahren...")


#####################
# Entropie und Kompression #
#####################

def entropy(probs):
    """Berechnet die Entropie für gegebene Wahrscheinlichkeiten"""
    h = 0
    for p in probs:
        if p > 0:  # Vermeidet log(0)
            h -= p * math.log2(p)
    return h


def redundanz(probs, codewortlängen):
    """Berechnet die Redundanz eines Codes"""
    h = entropy(probs)
    l = sum(p * l for p, l in zip(probs, codewortlängen))
    return l - h  # RC = L - H(X)


def huffman_coding(symbols, frequencies):
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


def rle_encode(data):
    """Komprimiert Bitfolgen mit Lauflängenkodierung"""
    if not data:
        return ""

    encoding = ""
    prev_char = data[0]
    count = 1

    for char in data[1:]:
        if char == prev_char:
            count += 1
        else:
            encoding += str(count)
            prev_char = char
            count = 1

    encoding += str(count)
    return encoding


def rle_decode(data, start_with="1"):
    """Dekomprimiert RLE-Daten zurück in Binärformat"""
    result = ""
    current_char = start_with

    for count in data:
        result += current_char * int(count)
        # Wechsle zwischen '0' und '1'
        current_char = '1' if current_char == '0' else '0'

    return result


def lz78_encode(data):
    """
    LZ78 Kompressionsalgorithmus
    Gibt Sequenz von (Index, Zeichen)-Paaren zurück
    """
    result = []
    dictionary = {"": 0}  # Leere Zeichenfolge hat Index 0
    current_phrase = ""

    i = 0
    while i < len(data):
        current_char = data[i]
        potential_phrase = current_phrase + current_char

        if potential_phrase in dictionary:
            # Erweitere aktuelle Phrase
            current_phrase = potential_phrase
        else:
            # Ausgabe: (Index der aktuellen Phrase, nächstes Zeichen)
            result.append((dictionary[current_phrase], current_char))

            # Füge neue Phrase zum Wörterbuch hinzu
            dictionary[potential_phrase] = len(dictionary)

            # Beginne neue Phrase
            current_phrase = ""

        i += 1

    # Behandle die letzte Phrase, falls nicht leer
    if current_phrase:
        result.append((dictionary[current_phrase], ""))

    return result


def lz78_decode(encoded_data):
    """
    LZ78 Dekompressionsalgorithmus
    Dekomprimiert eine Liste von (Index, Zeichen)-Paaren
    """
    result = ""
    dictionary = [""]  # Index 0 ist leere Zeichenfolge

    for index, char in encoded_data:
        # Rekonstruiere die Phrase aus dem Wörterbuch
        if index < len(dictionary):
            phrase = dictionary[index] + char
        else:
            # Spezialfall: Wenn ein Index verwendet wird, der noch nicht im Wörterbuch ist
            phrase = dictionary[-1] + dictionary[-1][0]

        # Füge dekodierte Phrase zum Ergebnis hinzu
        result += phrase

        # Aktualisiere das Wörterbuch
        dictionary.append(phrase)

    return result


def lz77_encode(data, window_size=7, lookahead_size=4):
    """
    Vereinfachte LZ77 Kompression mit fixen Fenstergröße und Vorschau
    Gibt Triple (Offset, Länge, nächstes Zeichen) zurück
    """
    result = []
    i = 0

    while i < len(data):
        # Suche nach der längsten übereinstimmenden Sequenz im Fenster
        best_length = 0
        best_offset = 0

        # Bestimme das aktuelle Fenster und den Vorschau-Puffer
        start = max(0, i - window_size)
        window = data[start:i]
        lookahead = data[i:min(i + lookahead_size, len(data))]

        # Finde die längste Übereinstimmung
        for j in range(1, len(window) + 1):
            pattern = window[-j:]
            match_length = 0

            while (match_length < len(lookahead) and
                   match_length < j and
                   lookahead[match_length] == pattern[match_length]):
                match_length += 1

            if match_length > best_length:
                best_length = match_length
                best_offset = j

        # Nächstes Zeichen nach der Übereinstimmung oder erstes Zeichen
        next_char = lookahead[best_length] if best_length < len(lookahead) else ""

        # Ausgabe: (Offset, Länge, nächstes Zeichen)
        result.append((best_offset, best_length, next_char))

        # Gehe um die Länge der Übereinstimmung + 1 vorwärts
        i += best_length + 1

    return result


def lz77_decode(encoded_data):
    """
    Dekomprimiert LZ77-kodierte Daten (Offset, Länge, nächstes Zeichen)
    """
    result = ""

    for offset, length, next_char in encoded_data:
        # Füge übereinstimmende Sequenz hinzu
        if offset > 0 and length > 0:
            start = len(result) - offset
            for i in range(length):
                result += result[start + i]

        # Füge nächstes Zeichen hinzu
        if next_char:
            result += next_char

    return result


#####################
# Verschlüsselung (RSA) #
#####################

def mod_exp(base, exponent, modulus):
    """Effiziente modulare Exponentiation"""
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result


def extended_gcd(a, b):
    """Berechnet ggt(a,b) und Koeffizienten x,y mit ax + by = ggt(a,b)"""
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


def mod_inverse(e, phi):
    """Berechnet d = e^(-1) mod phi"""
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise Exception('Modulares Inverses existiert nicht')
    else:
        return x % phi


def rsa_key_gen(p, q, e=None):
    """Generiert RSA-Schlüssel"""
    n = p * q
    phi = (p - 1) * (q - 1)

    # Wenn kein e angegeben wurde, wähle ein Standardwert (üblich: 65537)
    if e is None:
        e = 65537

    # Überprüfe, ob e und phi teilerfremd sind
    if math.gcd(e, phi) != 1:
        raise ValueError("e und phi müssen teilerfremd sein")

    # Berechne privaten Schlüssel d
    d = mod_inverse(e, phi)

    return (e, n), (d, n)  # (public_key, private_key)


def rsa_encrypt(message, public_key):
    """Verschlüsselt eine Nachricht mit RSA"""
    e, n = public_key
    return mod_exp(message, e, n)


def rsa_decrypt(ciphertext, private_key):
    """Entschlüsselt eine Nachricht mit RSA"""
    d, n = private_key
    return mod_exp(ciphertext, d, n)


#####################
# Kanalcodierung #
#####################

def hamming_distance(str1, str2):
    """Berechnet Hamming-Distanz zwischen zwei Binärstrings"""
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))


def syndrome(received, parity_matrix):
    """Berechnet Fehlersyndrom für einen empfangenen Codevektor"""
    # Implementierung der Matrix-Multiplikation
    n_rows = len(parity_matrix)
    result = [0] * n_rows

    for i in range(n_rows):
        for j in range(len(received)):
            result[i] = (result[i] + int(received[j]) * parity_matrix[i][j]) % 2

    return ''.join(str(bit) for bit in result)


def mod2div(dividend, divisor):
    """Durchführung der Polynomdivision im GF(2)"""
    # Kopiere die Bits des Dividenden
    result = list(dividend)

    # Anzahl der Bits, die verarbeitet werden sollen
    pick_len = len(divisor)

    # Durchlaufe bis zur Ende des Dividenden
    for i in range(len(dividend) - pick_len + 1):
        if result[i] == '1':
            # XOR-Operation mit dem Divisor
            for j in range(pick_len):
                result[i + j] = str(int(result[i + j]) ^ int(divisor[j]))

    # Der Rest ist das Fehlersyndrom
    return ''.join(result[-(pick_len - 1):])


def crc_check(message, generator, n_check_bits):
    """Prüft, ob die Nachricht mit CRC fehlerfrei ist"""
    # Teile die Nachricht in Daten und Prüfbits
    data = message[:-n_check_bits]
    check_bits = message[-n_check_bits:]

    # Berechne die Prüfbits neu
    computed_check = crc_compute(data, generator, n_check_bits)

    # Vergleiche
    return check_bits == computed_check


def crc_compute(data, generator, n_check_bits):
    """Berechnet die CRC-Prüfbits für gegebene Daten"""
    # Füge n Nullen hinzu
    extended_data = data + '0' * n_check_bits

    # Polynomdivision
    remainder = mod2div(extended_data, generator)

    return remainder


#####################
# Faltungscodes #
#####################
def calculate_error_syndrome(position, generator, codeword_length):
    """
    Berechnet das Syndrom für eine spezifische Fehlerstelle bei zyklischen Codes

    Args:
        position (int): Position des Fehlers (Exponent von x^position)
        generator (str): Generator-Polynom in Binärdarstellung
        codeword_length (int): Länge des Codeworts

    Returns:
        tuple: (polynomial_form, binary_form) des Syndroms
    """
    # Erzeuge ein Fehler-Polynom x^position
    error_polynomial = ['0'] * codeword_length
    error_polynomial[position] = '1'
    error_polynomial_str = ''.join(error_polynomial)

    # Berechne das Syndrom durch Polynomdivision
    syndrome = mod2div(error_polynomial_str, generator)

    # Auffüllen mit führenden Nullen falls nötig
    syndrome_bits = len(generator) - 1
    syndrome = syndrome.zfill(syndrome_bits)

    # Binäre Form des Syndroms
    binary_form = [int(bit) for bit in syndrome]

    # Polynomiale Form des Syndroms erstellen
    polynomial_form = ""
    for i in range(syndrome_bits):
        if syndrome[i] == '1':
            if syndrome_bits - i - 1 == 0:
                term = "1"
            elif syndrome_bits - i - 1 == 1:
                term = "x"
            else:
                term = f"x^{syndrome_bits - i - 1}"

            if polynomial_form:
                polynomial_form += " + " + term
            else:
                polynomial_form = term

    if not polynomial_form:
        polynomial_form = "0"

    return polynomial_form, binary_form


def create_syndrome_table_for_cyclic_code(generator, codeword_length=None):
    """
    Erstellt eine Tabelle mit Syndromen für jede Fehlerstelle in einem zyklischen Code

    Args:
        generator (str): Generator-Polynom in Binärdarstellung
        codeword_length (int, optional): Länge des Codeworts

    Returns:
        dict: Tabelle mit Fehlerstellen und zugehörigen Syndromen
    """
    # Berechne die Codewortlänge wenn nicht angegeben
    if codeword_length is None:
        codeword_length = 2 ** (len(generator) - 1) - 1

    # Tabelle für Fehlerstellen und Syndrome
    syndrome_table = {}

    # Für jede mögliche Fehlerposition
    for position in range(codeword_length):
        error_term = f"x^{position}" if position > 1 else ("x" if position == 1 else "1")
        poly_syndrome, bin_syndrome = calculate_error_syndrome(position, generator, codeword_length)
        syndrome_table[error_term] = (poly_syndrome, bin_syndrome)

    return syndrome_table

def get_convolution_output(input_bits, generator_polynomials):
    """Berechnet die Ausgabe eines Faltungscodierers für eine gegebene Eingabe"""
    # Konvertiere String-Eingabe in Liste von Integers
    if isinstance(input_bits, str):
        input_bits = [int(bit) for bit in input_bits]

    # Konvertiere Generator-Polynome zu Listen von Integers, falls nötig
    g_polys = []
    for poly in generator_polynomials:
        if isinstance(poly, str):
            g_polys.append([int(bit) for bit in poly])
        else:
            g_polys.append(poly)

    output = []
    # Bestimme die maximale Länge der Generatorpolynome für das Schieberegister
    max_len = max(len(p) for p in g_polys)
    state = [0] * (max_len - 1)  # Schieberegister

    for bit in input_bits:
        # Aktualisiere Schieberegister
        state = [bit] + state[:-1]

        # Berechne Ausgabe für jedes Generatorpolynom
        for poly in g_polys:
            # XOR der relevanten Bits (Faltung)
            out_bit = 0
            for i in range(min(len(poly), len(state) + 1)):
                if i == 0:
                    out_bit ^= bit * poly[i]  # Aktuelles Bit
                else:
                    if i - 1 < len(state):
                        out_bit ^= state[i - 1] * poly[i]
            output.append(out_bit)

    return output


def viterbi_simplified(received_bits, trellis, num_states):
    """Vereinfachte Viterbi-Dekodierung für kleine Faltungscodes"""
    # Initialisiere Metriken und Pfade
    metrics = [float('inf')] * num_states
    metrics[0] = 0  # Startknoten
    paths = [[] for _ in range(num_states)]

    # Verarbeite Bipaare (bei Rate 1/2)
    for i in range(0, len(received_bits), 2):
        received_pair = received_bits[i:i + 2]

        new_metrics = [float('inf')] * num_states
        new_paths = [[] for _ in range(num_states)]

        for state in range(num_states):
            for prev_state, output, next_state in trellis:
                if next_state == state:
                    # Hamming-Distanz zum empfangenen Paar
                    distance = sum(a != b for a, b in zip(output, received_pair))
                    metric = metrics[prev_state] + distance

                    if metric < new_metrics[state]:
                        new_metrics[state] = metric
                        new_paths[state] = paths[prev_state] + [prev_state >> 1]

        metrics = new_metrics
        paths = new_paths

    # Finde den Pfad mit der besten Metrik
    best_state = metrics.index(min(metrics))
    return paths[best_state]


#####################
# Kanalmodell #
#####################

def transinformation(px, pyx):
    """Berechnet die Transinformation T = H(Y) - H(Y|X)"""
    # Berechne p(y)
    py = [sum(px[i] * pyx[i][j] for i in range(len(px))) for j in range(len(pyx[0]))]

    # Berechne H(Y)
    hy = -sum(p * math.log2(p) for p in py if p > 0)

    # Berechne H(Y|X)
    hyx = 0
    for i in range(len(px)):
        for j in range(len(pyx[0])):
            if pyx[i][j] > 0 and px[i] > 0:
                hyx -= px[i] * pyx[i][j] * math.log2(pyx[i][j])

    return hy - hyx


def maximum_likelihood(channel_matrix):
    """Implementiert das Maximum-Likelihood-Verfahren zur Kanaldecodierung"""
    decoder = []
    for j in range(len(channel_matrix[0])):  # Für jede Spalte
        # Finde das Maximum in dieser Spalte
        max_prob = -1
        max_index = -1
        for i in range(len(channel_matrix)):
            if channel_matrix[i][j] > max_prob:
                max_prob = channel_matrix[i][j]
                max_index = i
        decoder.append(max_index)
    return decoder


#####################
# Binärzahlen und Darstellung #
#####################

def bin_to_dec(bin_str):
    """Wandelt einen Binärstring in eine Dezimalzahl um"""
    return int(bin_str, 2)


def dec_to_bin(dec_num, width=None):
    """Wandelt eine Dezimalzahl in einen Binärstring um"""
    bin_str = bin(dec_num)[2:]  # [2:] entfernt "0b" Präfix
    if width:
        bin_str = bin_str.zfill(width)
    return bin_str


def hex_to_bin(hex_str, width=None):
    """Wandelt einen Hexstring in einen Binärstring um"""
    bin_str = bin(int(hex_str, 16))[2:]
    if width:
        bin_str = bin_str.zfill(width)
    return bin_str


def twos_complement_to_decimal(bits):
    """Wandelt Zweierkomplement-Darstellung in Dezimalzahl um"""
    if bits[0] == '0':
        # Positive Zahl
        return int(bits, 2)
    else:
        # Negative Zahl: Invertiere und addiere 1
        inverted = ''.join('1' if bit == '0' else '0' for bit in bits)
        return -1 * (int(inverted, 2) + 1)


def decimal_to_twos_complement(n, bits):
    """Wandelt Dezimalzahl in Zweierkomplement mit n Bits um"""
    if n >= 0:
        binary = bin(n)[2:].zfill(bits)
        return binary[-bits:]
    else:
        binary = bin((1 << bits) + n)[2:]
        return binary[-bits:]


def float_to_bin(num):
    """Wandelt float in binäre IEEE 754 Darstellung um"""
    import struct
    packed = struct.pack('!f', num)
    integer = int.from_bytes(packed, 'big')
    return bin(integer)[2:].zfill(32)


def analyze_ieee754(bits):
    """Analysiert eine IEEE 754 Binärdarstellung"""
    sign = int(bits[0], 2)

    # Single precision
    exponent = int(bits[1:9], 2)
    mantissa = int('1' + bits[9:], 2) / (2 ** 23)

    # Berechne den tatsächlichen Wert
    if exponent == 0:
        # Denormalisierte Zahl
        return (-1) ** sign * (2 ** -126) * (mantissa - 1)
    elif exponent == 255:
        if mantissa == 1.0:
            return float('-inf') if sign else float('inf')
        else:
            return float('nan')
    else:
        # Normalisierte Zahl
        return (-1) ** sign * (2 ** (exponent - 127)) * mantissa


#####################
# Menüfunktionen #
#####################

def entropie_menu():
    global current_menu
    current_menu = "entropie"

    while current_menu == "entropie":
        clear_screen()
        print("==== Entropie und Kompression ====")
        print("1. Entropie berechnen")
        print("2. Redundanz berechnen")
        print("3. Huffman-Code erstellen")
        print("4. Lauflängenkodierung (RLE)")
        print("5. Lempel-Ziv LZ78")
        print("6. Lempel-Ziv LZ77")
        print("0. Zurück zum Hauptmenü")

        choice = input("\nWähle eine Option: ")

        if choice == "1":
            # Entropie berechnen
            clear_screen()
            print("==== Entropie berechnen ====")
            try:
                n = int(input("Anzahl der Symbole: "))
                probs = []
                for i in range(n):
                    p = float(input(f"Wahrscheinlichkeit für Symbol {i + 1}: "))
                    probs.append(p)

                result = entropy(probs)
                print(f"\nEntropie: {result:.6f} bits/Symbol")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "2":
            # Redundanz berechnen
            clear_screen()
            print("==== Redundanz berechnen ====")
            try:
                n = int(input("Anzahl der Symbole: "))
                probs = []
                lengths = []
                for i in range(n):
                    p = float(input(f"Wahrscheinlichkeit für Symbol {i + 1}: "))
                    l = float(input(f"Codewortlänge für Symbol {i + 1}: "))
                    probs.append(p)
                    lengths.append(l)

                result = redundanz(probs, lengths)
                print(f"\nRedundanz: {result:.6f} bits/Symbol")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "3":
            # Huffman-Code erstellen
            clear_screen()
            print("==== Huffman-Code erstellen ====")
            try:
                n = int(input("Anzahl der Symbole: "))
                symbols = []
                freqs = []
                for i in range(n):
                    s = input(f"Symbol {i + 1}: ")
                    f = float(input(f"Wahrscheinlichkeit für Symbol {s}: "))
                    symbols.append(s)
                    freqs.append(f)

                huffman_code = huffman_coding(symbols, freqs)
                print("\nHuffman-Code:")
                for sym, code in huffman_code.items():
                    print(f"{sym}: {code}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "4":
            # Lauflängenkodierung
            clear_screen()
            print("==== Lauflängenkodierung (RLE) ====")
            print("1. Kodieren")
            print("2. Dekodieren")
            subchoice = input("\nWähle eine Option: ")

            if subchoice == "1":
                try:
                    data = input("Eingabe (Bitfolge): ")
                    result = rle_encode(data)
                    print(f"\nRLE-Kodiert: {result}")
                except Exception as e:
                    print(f"Fehler: {str(e)}")

            elif subchoice == "2":
                try:
                    data = input("Eingabe (RLE-Kodiert): ")
                    start = input("Startet mit ('0' oder '1', Default '1'): ") or "1"
                    result = rle_decode(data, start)
                    print(f"\nDekodiert: {result}")
                except Exception as e:
                    print(f"Fehler: {str(e)}")

            pause()

        elif choice == "5":
            # Lempel-Ziv LZ78
            clear_screen()
            print("==== Lempel-Ziv LZ78 ====")
            print("1. Kodieren")
            print("2. Dekodieren")
            subchoice = input("\nWähle eine Option: ")

            if subchoice == "1":
                try:
                    data = input("Eingabe: ")
                    result = lz78_encode(data)
                    print("\nLZ78-Kodiert:")
                    for idx, char in result:
                        print(f"({idx}, '{char}')", end=" ")
                    print()
                except Exception as e:
                    print(f"Fehler: {str(e)}")

            elif subchoice == "2":
                try:
                    print("Eingabe LZ78-Kodiert (Format: idx1,char1 idx2,char2 ...):")
                    data_str = input()
                    pairs = data_str.split()
                    encoded_data = []
                    for pair in pairs:
                        idx, char = pair.strip("()").split(",")
                        encoded_data.append((int(idx), char.strip("'")))

                    result = lz78_decode(encoded_data)
                    print(f"\nDekodiert: {result}")
                except Exception as e:
                    print(f"Fehler: {str(e)}")

            pause()

        elif choice == "6":
            # Lempel-Ziv LZ77
            clear_screen()
            print("==== Lempel-Ziv LZ77 ====")
            print("1. Kodieren")
            print("2. Dekodieren")
            subchoice = input("\nWähle eine Option: ")

            if subchoice == "1":
                try:
                    data = input("Eingabe: ")
                    window = int(input("Fenstergröße (Standard: 7): ") or "7")
                    lookahead = int(input("Vorschau-Größe (Standard: 4): ") or "4")

                    result = lz77_encode(data, window, lookahead)
                    print("\nLZ77-Kodiert:")
                    for offset, length, char in result:
                        print(f"({offset}, {length}, '{char}')", end=" ")
                    print()
                except Exception as e:
                    print(f"Fehler: {str(e)}")

            elif subchoice == "2":
                try:
                    print("Eingabe LZ77-Kodiert (Format: offset1,length1,char1 offset2,length2,char2 ...):")
                    data_str = input()
                    triplets = data_str.split()
                    encoded_data = []
                    for triplet in triplets:
                        offset, length, char = triplet.strip("()").split(",")
                        encoded_data.append((int(offset), int(length), char.strip("'")))

                    result = lz77_decode(encoded_data)
                    print(f"\nDekodiert: {result}")
                except Exception as e:
                    print(f"Fehler: {str(e)}")

            pause()

        elif choice == "0":
            current_menu = "main"


def rsa_menu():
    global current_menu
    current_menu = "rsa"

    while current_menu == "rsa":
        clear_screen()
        print("==== RSA Verschlüsselung ====")
        print("1. RSA Schlüssel generieren")
        print("2. RSA verschlüsseln")
        print("3. RSA entschlüsseln")
        print("4. Modulares Inverses berechnen")
        print("5. Erweiterter Euklidischer Algorithmus")
        print("0. Zurück zum Hauptmenü")

        choice = input("\nWähle eine Option: ")

        if choice == "1":
            # RSA Schlüssel generieren
            clear_screen()
            print("==== RSA Schlüssel generieren ====")
            try:
                p = int(input("Primzahl p: "))
                q = int(input("Primzahl q: "))
                e_input = input("Öffentlicher Exponent e (leer für Standard): ")

                if e_input:
                    e = int(e_input)
                    public_key, private_key = rsa_key_gen(p, q, e)
                else:
                    public_key, private_key = rsa_key_gen(p, q)

                print("\nÖffentlicher Schlüssel (e, n):", public_key)
                print("Privater Schlüssel (d, n):", private_key)
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "2":
            # RSA verschlüsseln
            clear_screen()
            print("==== RSA verschlüsseln ====")
            try:
                message = int(input("Nachricht (als Zahl): "))
                e = int(input("Öffentlicher Exponent e: "))
                n = int(input("Modulus n: "))

                ciphertext = rsa_encrypt(message, (e, n))
                print(f"\nVerschlüsselt: {ciphertext}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "3":
            # RSA entschlüsseln
            clear_screen()
            print("==== RSA entschlüsseln ====")
            try:
                ciphertext = int(input("Chiffretext (als Zahl): "))
                d = int(input("Privater Exponent d: "))
                n = int(input("Modulus n: "))

                plaintext = rsa_decrypt(ciphertext, (d, n))
                print(f"\nEntschlüsselt: {plaintext}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "4":
            # Modulares Inverses
            clear_screen()
            print("==== Modulares Inverses berechnen ====")
            try:
                a = int(input("Zahl a: "))
                m = int(input("Modulus m: "))

                inverse = mod_inverse(a, m)
                print(f"\nModulares Inverses von {a} mod {m}: {inverse}")
                print(f"Überprüfung: {a} * {inverse} mod {m} = {(a * inverse) % m}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "5":
            # Erweiterter Euklidischer Algorithmus
            clear_screen()
            print("==== Erweiterter Euklidischer Algorithmus ====")
            try:
                a = int(input("Zahl a: "))
                b = int(input("Zahl b: "))

                gcd, x, y = extended_gcd(a, b)
                print(f"\nggT({a}, {b}) = {gcd}")
                print(f"Koeffizienten x, y: {x}, {y}")
                print(f"Überprüfung: {a}*{x} + {b}*{y} = {a * x + b * y}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "0":
            current_menu = "main"


def kanal_menu():
    global current_menu
    current_menu = "kanal"

    while current_menu == "kanal":
        clear_screen()
        print("==== Kanalcodierung ====")
        print("1. Hamming-Distanz berechnen")
        print("2. CRC berechnen")
        print("3. CRC prüfen")
        print("4. Fehlersyndrom berechnen")
        print("0. Zurück zum Hauptmenü")

        choice = input("\nWähle eine Option: ")

        if choice == "1":
            # Hamming-Distanz
            clear_screen()
            print("==== Hamming-Distanz berechnen ====")
            try:
                str1 = input("Erste Bitfolge: ")
                str2 = input("Zweite Bitfolge: ")

                if len(str1) != len(str2):
                    print("Fehler: Die Bitfolgen müssen gleich lang sein!")
                else:
                    distance = hamming_distance(str1, str2)
                    print(f"\nHamming-Distanz: {distance}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "2":
            # CRC berechnen
            clear_screen()
            print("==== CRC berechnen ====")
            try:
                data = input("Daten (Term standart: 11): ")
                generator = input("Generator-Polynom (Bitfolge): ")
                n_check_bits = len(generator) - 1

                check_bits = crc_compute(data, generator, n_check_bits)
                print(f"\nCRC-Prüfbits: {check_bits}")
                print(f"Vollständiges Codewort: {data + check_bits}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "3":
            # CRC prüfen
            clear_screen()
            print("==== CRC prüfen ====")
            try:
                message = input("Vollständige Nachricht mit CRC (Bitfolge): ")
                generator = input("Generator-Polynom (Bitfolge): ")
                n_check_bits = len(generator) - 1

                is_valid = crc_check(message, generator, n_check_bits)
                if is_valid:
                    print("\nNachricht ist fehlerfrei!")
                else:
                    print("\nNachricht enthält Fehler!")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "4":
            # Fehlersyndrom
            clear_screen()
            print("==== Fehlersyndrom berechnen ====")
            try:
                received = input("Empfangener Codevektor (Bitfolge): ")
                n_rows = int(input("Anzahl der Zeilen in der Prüfmatrix: "))
                n_cols = int(input("Anzahl der Spalten in der Prüfmatrix: "))

                print(f"\nGib die Prüfmatrix ({n_rows}x{n_cols}) ein:")
                parity_matrix = []
                for i in range(n_rows):
                    row = input(f"Zeile {i + 1}: ")
                    parity_matrix.append([int(bit) for bit in row])

                synd = syndrome(received, parity_matrix)
                print(f"\nFehlersyndrom: {synd}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "0":
            current_menu = "main"


def faltungscode_menu():
    global current_menu
    current_menu = "faltung"

    while current_menu == "faltung":
        clear_screen()
        print("==== Faltungscodes ====")
        print("1. Codierung mit Faltungscode")
        print("2. Viterbi-Decodierung (vereinfacht)")
        print("0. Zurück zum Hauptmenü")

        choice = input("\nWähle eine Option: ")

        if choice == "1":
            # Faltungscode Codierung
            clear_screen()
            print("==== Codierung mit Faltungscode ====")
            try:
                input_bits = input("Eingabe-Bits: ")
                n_polys = int(input("Anzahl der Generatorpolynome: "))

                generator_polynomials = []
                for i in range(n_polys):
                    poly = input(f"Generatorpolynom {i + 1} (Bitfolge): ")
                    generator_polynomials.append(poly)

                output = get_convolution_output(input_bits, generator_polynomials)
                output_str = ''.join(str(bit) for bit in output)
                print(f"\nKodierte Ausgabe: {output_str}")

                # Gruppiere die Ausgabe je nach Anzahl der Polynome
                grouped = []
                for i in range(0, len(output), n_polys):
                    grouped.append(output_str[i:i + n_polys])

                print("Gruppiert:", ' '.join(grouped))
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "2":
            # Viterbi-Decodierung
            clear_screen()
            print("==== Viterbi-Decodierung (vereinfacht) ====")
            print("Diese Funktion erfordert vorbereitete Trellis-Daten.")
            print("Für komplexe Faltungscodes ist manuelle Berechnung empfohlen.")

            try:
                # Vereinfachtes Beispiel mit einem 2-Zuständigen Codierer
                print("\nEinfaches Beispiel mit einem (2,1,2) Faltungscode:")
                print("Zustände: 00, 01")
                print("Trellis-Übergänge: (vorheriger Zustand, Ausgabe, nächster Zustand)")
                print("(0, 00, 0), (0, 11, 1), (1, 10, 0), (1, 01, 1)")

                received_bits = input("\nEmpfangene Bits: ")

                # Vereinfachtes Trellis für ein Beispiel
                trellis = [
                    (0, (0, 0), 0),  # Von Zustand 0 mit Input 0 -> Zustand 0, Ausgabe 00
                    (0, (1, 1), 1),  # Von Zustand 0 mit Input 1 -> Zustand 1, Ausgabe 11
                    (1, (1, 0), 0),  # Von Zustand 1 mit Input 0 -> Zustand 0, Ausgabe 10
                    (1, (0, 1), 1)  # Von Zustand 1 mit Input 1 -> Zustand 1, Ausgabe 01
                ]

                decoded = viterbi_simplified([int(bit) for bit in received_bits], trellis, 2)
                print(f"\nDekodiert: {''.join(str(bit) for bit in decoded)}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "0":
            current_menu = "main"


def kanalmodell_menu():
    global current_menu
    current_menu = "kanalmodell"

    while current_menu == "kanalmodell":
        clear_screen()
        print("==== Kanalmodell ====")
        print("1. Transinformation berechnen")
        print("2. Maximum-Likelihood-Decodierung")
        print("0. Zurück zum Hauptmenü")

        choice = input("\nWähle eine Option: ")

        if choice == "1":
            # Transinformation
            clear_screen()
            print("==== Transinformation berechnen ====")
            try:
                n_input = int(input("Anzahl der Eingangssymbole: "))
                n_output = int(input("Anzahl der Ausgangssymbole: "))

                print("\nEingabewahrscheinlichkeiten p(x):")
                px = []
                for i in range(n_input):
                    p = float(input(f"p(x{i}): "))
                    px.append(p)

                print("\nKanalmatrix p(y|x):")
                pyx = []
                for i in range(n_input):
                    row = []
                    print(f"Für x{i}:")
                    for j in range(n_output):
                        p = float(input(f"p(y{j}|x{i}): "))
                        row.append(p)
                    pyx.append(row)

                result = transinformation(px, pyx)
                print(f"\nTransinformation: {result:.6f} bits/Symbol")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "2":
            # Maximum-Likelihood
            clear_screen()
            print("==== Maximum-Likelihood-Decodierung ====")
            try:
                n_input = int(input("Anzahl der Eingangssymbole: "))
                n_output = int(input("Anzahl der Ausgangssymbole: "))

                print("\nKanalmatrix p(y|x):")
                channel_matrix = []
                for i in range(n_input):
                    row = []
                    print(f"Für x{i}:")
                    for j in range(n_output):
                        p = float(input(f"p(y{j}|x{i}): "))
                        row.append(p)
                    channel_matrix.append(row)

                decoder = maximum_likelihood(channel_matrix)

                print("\nMaximum-Likelihood-Dekodierung:")
                for j in range(n_output):
                    print(f"y{j} → x{decoder[j]}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "0":
            current_menu = "main"


def binär_menu():
    global current_menu
    current_menu = "binär"

    while current_menu == "binär":
        clear_screen()
        print("==== Binärzahlen und Darstellung ====")
        print("1. Binär → Dezimal")
        print("2. Dezimal → Binär")
        print("3. Hexadezimal → Binär")
        print("4. Zweierkomplement → Dezimal")
        print("5. Dezimal → Zweierkomplement")
        print("6. Float → IEEE 754 Binär")
        print("7. IEEE 754 Binär → Float")
        print("0. Zurück zum Hauptmenü")

        choice = input("\nWähle eine Option: ")

        if choice == "1":
            # Binär → Dezimal
            clear_screen()
            print("==== Binär → Dezimal ====")
            try:
                bin_str = input("Binärzahl: ")
                result = bin_to_dec(bin_str)
                print(f"\nDezimal: {result}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "2":
            # Dezimal → Binär
            clear_screen()
            print("==== Dezimal → Binär ====")
            try:
                dec_num = int(input("Dezimalzahl: "))
                width = input("Anzahl Bits (optional): ")

                if width:
                    result = dec_to_bin(dec_num, int(width))
                else:
                    result = dec_to_bin(dec_num)

                print(f"\nBinär: {result}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "3":
            # Hexadezimal → Binär
            clear_screen()
            print("==== Hexadezimal → Binär ====")
            try:
                hex_str = input("Hexadezimalzahl: ")
                width = input("Anzahl Bits (optional): ")

                if width:
                    result = hex_to_bin(hex_str, int(width))
                else:
                    result = hex_to_bin(hex_str)

                print(f"\nBinär: {result}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "4":
            # Zweierkomplement → Dezimal
            clear_screen()
            print("==== Zweierkomplement → Dezimal ====")
            try:
                bits = input("Zweierkomplement-Binärzahl: ")
                result = twos_complement_to_decimal(bits)
                print(f"\nDezimal: {result}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "5":
            # Dezimal → Zweierkomplement
            clear_screen()
            print("==== Dezimal → Zweierkomplement ====")
            try:
                n = int(input("Dezimalzahl: "))
                bits = int(input("Anzahl Bits: "))

                result = decimal_to_twos_complement(n, bits)
                print(f"\nZweierkomplement: {result}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "6":
            # Float → IEEE 754
            clear_screen()
            print("==== Float → IEEE 754 Binär ====")
            try:
                num = float(input("Gleitkommazahl: "))
                result = float_to_bin(num)

                # Teile das Ergebnis in Vorzeichen, Exponent und Mantisse
                sign = result[0]
                exponent = result[1:9]
                mantissa = result[9:]

                print(f"\nIEEE 754 Single Precision:")
                print(f"Vorzeichen: {sign}")
                print(f"Exponent: {exponent}")
                print(f"Mantisse: {mantissa}")
                print(f"Vollständig: {result}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "7":
            # IEEE 754 → Float
            clear_screen()
            print("==== IEEE 754 Binär → Float ====")
            try:
                bits = input("IEEE 754 Binärdarstellung: ")

                # Stelle sicher, dass es 32 Bit sind
                if len(bits) != 32:
                    bits = bits.zfill(32)

                result = analyze_ieee754(bits)

                # Teile das Ergebnis in Vorzeichen, Exponent und Mantisse
                sign = bits[0]
                exponent = bits[1:9]
                mantissa = bits[9:]

                print(f"\nVorzeichen: {sign}")
                print(f"Exponent: {exponent} (Dezimal: {int(exponent, 2)})")
                print(f"Mantisse: {mantissa}")
                print(f"Dezimalwert: {result}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "0":
            current_menu = "main"


def polynomial_division_for_syndrome(message, generator):
    """
    Berechnet das Syndrom für eine Fehlerstelle mittels Polynomdivision

    Args:
        message (str): Empfangenes Codewort oder Nachricht
        generator (str): Generator-Polynom (Bitfolge)

    Returns:
        str: Syndrom (Rest der Polynomdivision)
    """
    # Polynomdivision durchführen
    remainder = mod2div(message, generator)
    return remainder


def fast_multiple_addition(generator, codeword, show_steps=False):
    """
    Führt schnelle Mehrfachaddition durch, um Codewort zu prüfen

    Args:
        generator (str): Generator-Polynom (Bitfolge)
        codeword (str): Zu prüfendes Codewort
        show_steps (bool): Berechnungsschritte anzeigen

    Returns:
        tuple: (is_valid, result) oder (is_valid, steps, result) wenn show_steps=True
    """
    # Kopie des Codeworts für Berechnung
    result = list(codeword)
    steps = [codeword] if show_steps else None

    # Finde Positionen mit '1' im Codewort
    ones_positions = [i for i, bit in enumerate(codeword) if bit == '1']

    # Entferne führende Nullen im Generator
    gen = generator
    while gen.startswith('0') and len(gen) > 1:
        gen = gen[1:]

    # Für jede Position mit einer '1', addiere den Generator (XOR)
    for pos in ones_positions:
        # Überspringe Positionen, die über die Codewortlänge hinausgehen würden
        if pos > len(codeword) - len(gen):
            continue

        # Generator an dieser Position anwenden
        for j in range(len(gen)):
            if pos + j < len(result) and gen[j] == '1':
                # XOR-Operation: 1^1=0, 0^0=0, 1^0=1, 0^1=1
                result[pos + j] = '1' if result[pos + j] != '1' else '0'

        # Diesen Schritt aufzeichnen, falls gewünscht
        if show_steps:
            steps.append(''.join(result))

    # Codewort ist gültig, wenn das Ergebnis nur aus Nullen besteht
    is_valid = all(bit == '0' for bit in result)

    # Passende Ergebnisse zurückgeben
    if show_steps:
        return is_valid, steps, ''.join(result)
    else:
        return is_valid, ''.join(result)


def generate_cyclic_codewords(generator, message_length):
    """
    Generiert gültige Codeworte für einen zyklischen Code

    Args:
        generator (str): Generator-Polynom (Bitfolge)
        message_length (int): Länge des Nachrichtenanteils

    Returns:
        list: Liste der gültigen Codeworte
    """
    # Anzahl der Kontrollbits = Grad des Generator-Polynoms
    check_bits = len(generator) - 1

    # Gesamtlänge des Codeworts
    codeword_length = message_length + check_bits

    # Liste für gültige Codeworte
    codewords = []

    # Generiere alle möglichen Nachrichtenmuster
    for i in range(2 ** message_length):
        # In Binärdarstellung umwandeln und mit führenden Nullen auffüllen
        message = bin(i)[2:].zfill(message_length)

        # Kontrollbits mit CRC-ähnlicher Methode berechnen
        padded_message = message + '0' * check_bits
        remainder = mod2div(padded_message, generator)

        # Vollständiges Codewort erstellen
        codeword = message + remainder

        codewords.append(codeword)

    return codewords


def create_parity_matrix_from_generator(generator):
    """
    Erstellt eine Prüfmatrix für einen zyklischen Code

    Args:
        generator (str): Generator-Polynom (Bitfolge)

    Returns:
        list: Prüfmatrix als Liste von Zeilen
    """
    # Generator-Polynom bereinigen
    generator = generator.lstrip('0')
    if not generator:
        generator = '0'

    # Anzahl der Kontrollbits = Grad des Generator-Polynoms
    r = len(generator) - 1

    # Für einen Standard-zyklischen Code ist die Codewortlänge 2^r - 1
    n = 2 ** r - 1

    # Prüfmatrix initialisieren
    H = []

    # Bei zyklischen Codes ist jede Zeile von H eine zyklische Verschiebung der vorherigen
    for i in range(r):
        row = [0] * n

        # Für die erste Zeile verwende das Generator-Polynom
        if i == 0:
            for j in range(len(generator)):
                if j < n:
                    row[j] = int(generator[j])
        else:
            # Für nachfolgende Zeilen verwende eine zyklische Verschiebung
            prev_row = H[i - 1]
            # Zyklische Verschiebung nach rechts
            row = [prev_row[-1]] + prev_row[:-1]

        H.append(row)

    return H


def zyklischer_code_menu():
    global current_menu
    current_menu = "zyklisch"

    while current_menu == "zyklisch":
        clear_screen()
        print("==== Zyklische Codes ====")
        print("1. Polynomdivision für Syndromberechnung")
        print("2. Schnelle Mehrfachaddition")
        print("3. Zyklische Codeworte generieren")
        print("4. Syndromtabelle für zyklischen Code erstellen")
        print("0. Zurück zum Hauptmenü")

        choice = input("\nWähle eine Option: ")

        if choice == "1":
            # Polynomdivision für Syndrom
            clear_screen()
            print("==== Polynomdivision für Syndrom ====")
            try:
                message = input("Nachricht oder empfangenes Codewort: ")
                generator = input("Generator-Polynom (Bitfolge): ")

                syndrome = polynomial_division_for_syndrome(message, generator)
                print(f"\nSyndrom: {syndrome}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "2":
            # Schnelle Mehrfachaddition
            clear_screen()
            print("==== Schnelle Mehrfachaddition ====")
            try:
                generator = input("Generator-Polynom (Bitfolge): ")
                codeword = input("Codewort (Bitfolge): ")
                show_steps = input("Berechnungsschritte anzeigen? (j/n): ").lower() == 'j'

                if show_steps:
                    is_valid, steps, result = fast_multiple_addition(generator, codeword, True)

                    print("\nBerechnungsschritte:")
                    for i, step in enumerate(steps):
                        if i == 0:
                            print(f"Codewort: {step}")
                        else:
                            print(f"Schritt {i}: {step}")
                else:
                    is_valid, result = fast_multiple_addition(generator, codeword, False)

                print(f"\nErgebnis: {result}")
                if is_valid:
                    print("Das Codewort ist gültig!")
                else:
                    print("Das Codewort enthält Fehler!")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "3":
            # Zyklische Codeworte generieren
            clear_screen()
            print("==== Zyklische Codeworte generieren ====")
            try:
                generator = input("Generator-Polynom (Bitfolge): ")
                message_length = int(input("Nachrichtenlänge: "))

                codewords = generate_cyclic_codewords(generator, message_length)

                print(f"\nAnzahl der gültigen Codeworte: {len(codewords)}")
                print("\nEinige Beispiel-Codeworte:")
                for i in range(min(10, len(codewords))):
                    print(codewords[i])

                if len(codewords) > 10:
                    print("...")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "4":
            # Syndromtabelle erstellen
            clear_screen()
            print("==== Syndromtabelle für zyklischen Code erstellen ====")
            try:
                generator = input("Generator-Polynom (Bitfolge): ")
                codeword_length = input("Codewortlänge (Optional, leer für 2^r-1): ")

                if codeword_length:
                    codeword_length = int(codeword_length)
                    syndrome_table = create_syndrome_table_for_cyclic_code(generator, codeword_length)
                else:
                    syndrome_table = create_syndrome_table_for_cyclic_code(generator)

                print("\nSyndromtabelle für Fehlerstellen:")
                print(f"{'Fehler':<8} {'Syndrom':<15} {'Binär'}")
                print("-" * 40)

                for error_term, (poly_form, bin_form) in syndrome_table.items():
                    bin_str = f"[{' '.join(str(bit) for bit in bin_form)}]"
                    print(f"{error_term:<8} {poly_form:<15} {bin_str}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "0":
            current_menu = "main"


def polynomial_menu():
    global current_menu
    current_menu = "polynomial"

    while current_menu == "polynomial":
        clear_screen()
        print("==== Polynomprüfung ====")
        print("1. Prüfen ob Polynom reduzibel/irreduzibel ist")
        print("2. Prüfen ob Polynom primitiv ist")
        print("3. Elemente des Erweiterungsfelds generieren")
        print("0. Zurück zum Hauptmenü")

        choice = input("\nWähle eine Option: ")

        if choice == "1":
            # Irreduzibilitätsprüfung
            clear_screen()
            print("==== Polynom auf Irreduzibilität prüfen ====")
            try:
                poly_str = input("Polynom (höchste Potenz zuerst, z.B. 1101 für x³+x²+1): ")
                poly = [int(bit) for bit in poly_str]

                # Entferne führende Nullen
                while poly and poly[0] == 0:
                    poly = poly[1:]

                if not poly:
                    print("\nUngültiges Polynom (leer).")
                else:
                    result = is_irreducible_polynomial(poly)

                    # Zeige Polynom in Standardnotation
                    poly_terms = []
                    degree = len(poly) - 1
                    for i, coeff in enumerate(poly):
                        if coeff == 1:
                            power = degree - i
                            if power == 0:
                                poly_terms.append("1")
                            elif power == 1:
                                poly_terms.append("x")
                            else:
                                poly_terms.append(f"x^{power}")

                    poly_notation = " + ".join(poly_terms)

                    print(f"\nPolynom: {poly_notation}")
                    if result:
                        print("Das Polynom ist irreduzibel.")
                    else:
                        print("Das Polynom ist reduzibel (faktorisierbar).")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "2":
            # Primitivitätsprüfung
            clear_screen()
            print("==== Polynom auf Primitivität prüfen ====")
            print("Hinweis: Diese Berechnung kann für Polynome mit Grad > 4 sehr lange dauern.")
            try:
                poly_str = input("Polynom (höchste Potenz zuerst, z.B. 1101 für x³+x²+1): ")
                poly = [int(bit) for bit in poly_str]

                # Entferne führende Nullen
                while poly and poly[0] == 0:
                    poly = poly[1:]

                if not poly:
                    print("\nUngültiges Polynom (leer).")
                else:
                    degree = len(poly) - 1

                    if degree > 4:
                        confirm = input(
                            f"Das Polynom hat Grad {degree}, was eine lange Berechnung erfordert. Fortfahren? (j/n): ")
                        if confirm.lower() != 'j':
                            raise Exception("Berechnung abgebrochen")

                    result = is_primitive_polynomial(poly)

                    # Zeige Polynom in Standardnotation
                    poly_terms = []
                    for i, coeff in enumerate(poly):
                        if coeff == 1:
                            power = degree - i
                            if power == 0:
                                poly_terms.append("1")
                            elif power == 1:
                                poly_terms.append("x")
                            else:
                                poly_terms.append(f"x^{power}")

                    poly_notation = " + ".join(poly_terms)

                    print(f"\nPolynom: {poly_notation}")
                    if result:
                        print("Das Polynom ist primitiv.")
                    else:
                        print("Das Polynom ist NICHT primitiv.")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "3":
            # Erweiterungsfeld-Elemente
            clear_screen()
            print("==== Erweiterungsfeld-Elemente generieren ====")
            print("Hinweis: Diese Funktion ist für Felder mit Grad ≤ 4 optimiert.")
            try:
                poly_str = input("Primitives Polynom (höchste Potenz zuerst, z.B. 1101 für x³+x²+1): ")
                poly = [int(bit) for bit in poly_str]

                # Entferne führende Nullen
                while poly and poly[0] == 0:
                    poly = poly[1:]

                if not poly:
                    print("\nUngültiges Polynom (leer).")
                else:
                    degree = len(poly) - 1
                    max_elements = 2 ** degree - 1

                    if degree > 4:
                        confirm = input(
                            f"Das Polynom erzeugt ein Feld GF(2^{degree}) mit {max_elements} Elementen. Anzahl der anzuzeigenden Elemente eingeben (max {max_elements}): ")
                        limit = int(confirm) if confirm else max_elements
                    else:
                        limit = max_elements

                    elements = generate_extension_field_elements(poly, min(limit, max_elements))

                    print(f"\nElemente des Erweiterungsfelds GF(2^{degree}):")
                    for i, element in enumerate(elements):
                        # Binärdarstellung
                        bin_repr = ''.join(str(bit) for bit in element)

                        # Polynomdarstellung
                        poly_terms = []
                        for j, bit in enumerate(element):
                            if bit == 1:
                                power = degree - 1 - j
                                if power == 0:
                                    poly_terms.append("1")
                                elif power == 1:
                                    poly_terms.append("x")
                                else:
                                    poly_terms.append(f"x^{power}")

                        poly_repr = " + ".join(poly_terms) if poly_terms else "0"

                        # Kompakte Darstellung für α-Potenz
                        if i == 0:
                            alpha_repr = "1"
                        else:
                            alpha_repr = f"α^{i}"

                        print(f"{alpha_repr:>6} = {poly_repr:>12} = {bin_repr}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "0":
            current_menu = "main"


#####################
# Quellen mit Gedächtnis #
#####################

def compute_stationary_distribution(transition_matrix):
    """
    Berechnet näherungsweise die stationäre Verteilung einer Markov-Kette
    Verwendet Potenzmethode statt Matrixinversion (MicroPython-kompatibel)
    """
    n = len(transition_matrix)
    # Starte mit Gleichverteilung
    pi = [1.0 / n] * n

    # Iteration der Potenzmethode
    for _ in range(50):  # 50 Iterationen für Konvergenz
        new_pi = [0] * n
        for j in range(n):
            for i in range(n):
                new_pi[j] += pi[i] * transition_matrix[i][j]

        # Normalisiere
        total = sum(new_pi)
        pi = [p / total for p in new_pi]

    return pi


def joint_probability(px, pyx):
    """
    Berechnet die gemeinsame Wahrscheinlichkeit P(X,Y) aus P(X) und P(Y|X)
    """
    pxy = []
    for i in range(len(px)):
        row = []
        for j in range(len(pyx[i])):
            p = px[i] * pyx[i][j]
            row.append(p)
        pxy.append(row)

    return pxy


def marginal_probability_y(pxy):
    """
    Berechnet die Randwahrscheinlichkeiten P(Y) aus P(X,Y)
    """
    if not pxy:
        return []

    n_y = len(pxy[0])
    py = [0] * n_y

    for i in range(len(pxy)):
        for j in range(n_y):
            py[j] += pxy[i][j]

    return py


def conditional_entropy_yx(pxy, px):
    """
    Berechnet die bedingte Entropie H(Y|X)
    """
    h_yx = 0.0

    # Berechne P(Y|X) aus P(X,Y) und P(X)
    for i in range(len(px)):
        if px[i] == 0:
            continue

        for j in range(len(pxy[i])):
            if pxy[i][j] > 0:
                # P(Y|X) = P(X,Y) / P(X)
                p_y_given_x = pxy[i][j] / px[i]
                h_yx -= pxy[i][j] * math.log2(p_y_given_x)

    return h_yx


def entropy_with_memory(transition_matrix):
    """
    Berechnet die Entropie einer Quelle mit Gedächtnis (Markov-Quelle)
    """
    # Berechne stationäre Verteilung
    pi = compute_stationary_distribution(transition_matrix)

    # Berechne bedingte Entropie H(X_t+1 | X_t)
    h_cond = 0.0
    for i in range(len(pi)):
        for j in range(len(transition_matrix[i])):
            if pi[i] > 0 and transition_matrix[i][j] > 0:
                h_cond -= pi[i] * transition_matrix[i][j] * math.log2(transition_matrix[i][j])

    # Berechne Entropie der stationären Verteilung H(X)
    h_stationary = 0.0
    for p in pi:
        if p > 0:
            h_stationary -= p * math.log2(p)

    return {
        "stationary_distribution": pi,
        "conditional_entropy": h_cond,
        "stationary_entropy": h_stationary,
        "entropy_rate": h_cond
    }


#####################
# Menü-Funktionen #
#####################

def markov_menu():
    global current_menu
    current_menu = "markov"

    while current_menu == "markov":
        clear_screen()
        print("==== Markov-Quellen und Gedächtnis ====")
        print("1. Verbundwahrscheinlichkeiten berechnen")
        print("2. Bedingte Entropie berechnen")
        print("3. Entropie für Quellen mit Gedächtnis")
        print("0. Zurück zum Hauptmenü")

        choice = input("\nWähle eine Option: ")

        if choice == "1":
            # Verbundwahrscheinlichkeiten
            clear_screen()
            print("==== Verbundwahrscheinlichkeiten ====")
            try:
                n_x = int(input("Anzahl der X-Symbole: "))
                n_y = int(input("Anzahl der Y-Symbole: "))

                print("\nP(X) Wahrscheinlichkeiten:")
                px = []
                for i in range(n_x):
                    p = float(input(f"P(X={i + 1}): "))
                    px.append(p)

                print("\nBedingte Wahrscheinlichkeiten P(Y|X):")
                pyx = []
                for i in range(n_x):
                    print(f"Für X={i + 1}:")
                    row = []
                    for j in range(n_y):
                        p = float(input(f"P(Y={j + 1}|X={i + 1}): "))
                        row.append(p)
                    pyx.append(row)

                # Berechne Verbundwahrscheinlichkeiten
                pxy = joint_probability(px, pyx)

                # Berechne Randwahrscheinlichkeiten für Y
                py = marginal_probability_y(pxy)

                print("\nVerbundwahrscheinlichkeiten P(X,Y):")
                for i in range(n_x):
                    for j in range(n_y):
                        print(f"P(X={i + 1},Y={j + 1}) = {pxy[i][j]:.6f}")

                print("\nRandwahrscheinlichkeiten P(Y):")
                for j in range(n_y):
                    print(f"P(Y={j + 1}) = {py[j]:.6f}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "2":
            # Bedingte Entropie
            clear_screen()
            print("==== Bedingte Entropie ====")
            try:
                n_x = int(input("Anzahl der X-Symbole: "))
                n_y = int(input("Anzahl der Y-Symbole: "))

                print("\nP(X) Wahrscheinlichkeiten:")
                px = []
                for i in range(n_x):
                    p = float(input(f"P(X={i + 1}): "))
                    px.append(p)

                print("\nVerbundwahrscheinlichkeiten P(X,Y):")
                pxy = []
                for i in range(n_x):
                    print(f"Für X={i + 1}:")
                    row = []
                    for j in range(n_y):
                        p = float(input(f"P(X={i + 1},Y={j + 1}): "))
                        row.append(p)
                    pxy.append(row)

                # Berechne bedingte Entropie
                h_yx = conditional_entropy_yx(pxy, px)

                print(f"\nBedingte Entropie H(Y|X) = {h_yx:.6f} bits")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "3":
            # Entropie mit Gedächtnis
            clear_screen()
            print("==== Entropie für Quellen mit Gedächtnis ====")
            try:
                n = int(input("Anzahl der Zustände: "))

                print("\nÜbergangsmatrix eingeben:")
                transition_matrix = []
                for i in range(n):
                    print(f"Für Zustand {i + 1}:")
                    row = []
                    for j in range(n):
                        p = float(input(f"P(Zustand {j + 1}|Zustand {i + 1}): "))
                        row.append(p)
                    transition_matrix.append(row)

                # Berechne Entropie
                result = entropy_with_memory(transition_matrix)

                print("\nErgebnisse:")
                print("Stationäre Verteilung:")
                for i, p in enumerate(result["stationary_distribution"]):
                    print(f"π_{i + 1} = {p:.6f}")

                print(f"\nStationäre Entropie H(X) = {result['stationary_entropy']:.6f} bits")
                print(f"Bedingte Entropie H(X_t+1|X_t) = {result['conditional_entropy']:.6f} bits")
                print(f"Entropierate = {result['entropy_rate']:.6f} bits pro Symbol")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "0":
            current_menu = "main"


#####################
# Blockcode-Eigenschaften #
#####################

def factorial(n):
    """Einfache Fakultätsberechnung für MicroPython"""
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def binomial(n, k):
    """Binomialkoeffizient ohne math.comb für MicroPython"""
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1

    # Berechne n! / (k! * (n-k)!)
    return factorial(n) // (factorial(k) * factorial(n - k))


def is_densely_packed(n, k, d):
    """
    Prüft, ob ein Blockcode dichtgepackt ist
    """
    # Berechne die Anzahl der Codewörter (2^k)
    num_codewords = 2 ** k

    # Anzahl der Bits, die korrigiert werden können
    t = (d - 1) // 2

    # Berechne die Anzahl der Wörter innerhalb der Korrekturkugel
    sphere_size = 0
    for i in range(t + 1):
        # Anzahl der möglichen Positionen für i Fehler
        sphere_size += binomial(n, i)

    # Ein Code ist dichtgepackt, wenn:
    total_words = 2 ** n
    packed_size = num_codewords * sphere_size

    return total_words == packed_size


def create_hamming_parity_matrix(r):
    """
    Erzeugt eine Prüfmatrix für einen Hamming-Code
    """
    n = 2 ** r - 1  # Länge des Hamming-Codes

    # Initialisiere die Prüfmatrix mit Nullen
    H = [[0 for _ in range(n)] for _ in range(r)]

    # Fülle die Prüfmatrix
    for j in range(n):
        # j+1 als r-bit Binärdarstellung
        col_idx = j + 1
        binary = bin(col_idx)[2:].zfill(r)
        binary = binary[-r:]  # Nimm nur die letzten r Bits

        for i in range(r):
            H[i][j] = int(binary[r - i - 1])  # Richtiger Index für Hamming-Code

    return H


#####################
# Polynomprüfung #
#####################

def polynomial_division_gf2(dividend, divisor):
    """
    Polynomiale Division im GF(2)

    Argumente:
        dividend, divisor: Listen mit Koeffizienten, höchste Potenz zuerst
    Rückgabe:
        (quotient, remainder): Tupel mit Ergebnispolynomen
    """
    # Entferne führende Nullen
    while len(dividend) > 0 and dividend[0] == 0:
        dividend = dividend[1:]
    while len(divisor) > 0 and divisor[0] == 0:
        divisor = divisor[1:]

    if not divisor:
        raise ValueError("Division durch Null")

    if not dividend:
        return [0], [0]

    if len(dividend) < len(divisor):
        return [0], dividend.copy()

    quotient = [0] * (len(dividend) - len(divisor) + 1)
    remainder = dividend.copy()

    for i in range(len(quotient)):
        if remainder[i] == 1:
            quotient[i] = 1
            for j in range(len(divisor)):
                remainder[i + j] = (remainder[i + j] + divisor[j]) % 2

    # Entferne führende Nullen im Rest
    while len(remainder) > 0 and remainder[0] == 0:
        remainder = remainder[1:]

    # Falls Rest leer ist, setze ihn auf [0]
    if not remainder:
        remainder = [0]

    return quotient, remainder


def is_irreducible_polynomial(poly):
    """
    Prüft, ob ein Polynom irreduzibel ist im GF(2)

    Argument:
        poly: Liste mit Koeffizienten, höchste Potenz zuerst
    Rückgabe:
        bool: True wenn irreduzibel, False sonst
    """
    # Entferne führende Nullen
    while poly and poly[0] == 0:
        poly = poly[1:]

    if not poly or len(poly) <= 1:
        return False  # Konstante oder leeres Polynom

    degree = len(poly) - 1

    # Brute-Force-Methode: Prüfe alle möglichen Faktoren bis Grad degree//2
    for d in range(1, degree // 2 + 1):
        # Generiere alle möglichen Polynome vom Grad d
        for coeffs in generate_all_polynomials(d):
            # Füge eine 1 für den höchsten Koeffizienten hinzu
            test_poly = [1] + coeffs

            # Prüfe ob test_poly ein Teiler ist
            _, remainder = polynomial_division_gf2(poly, test_poly)

            if remainder == [0]:
                return False  # Gefunden: test_poly ist ein Teiler

    return True


def generate_all_polynomials(degree):
    """
    Generiert alle möglichen Polynome vom Grad < degree im GF(2)

    Argument:
        degree: Maximaler Grad
    Rückgabe:
        Liste aller möglichen Polynomkoeffizienten (ohne höchsten Koeffizienten)
    """
    result = []

    # 2^degree mögliche Kombinationen
    for i in range(2 ** degree):
        # Konvertiere i in Binärdarstellung
        binary = bin(i)[2:].zfill(degree)
        coeffs = [int(bit) for bit in binary]
        result.append(coeffs)

    return result


def is_primitive_polynomial(poly):
    """
    Prüft, ob ein Polynom primitiv ist im GF(2)
    Ein primitives Polynom muss:
    1. Irreduzibel sein
    2. Die Periode 2^degree - 1 haben

    Argument:
        poly: Liste mit Koeffizienten, höchste Potenz zuerst
    Rückgabe:
        bool: True wenn primitiv, False sonst
    """
    # Entferne führende Nullen
    while poly and poly[0] == 0:
        poly = poly[1:]

    if not poly or len(poly) <= 1:
        return False  # Konstante oder leeres Polynom

    # Prüfe auf Irreduzibilität
    if not is_irreducible_polynomial(poly):
        return False

    degree = len(poly) - 1
    period = 2 ** degree - 1

    # Für sehr kleine Grade können wir eine direkte Prüfung durchführen
    if degree <= 4:  # Für größere Grade wird die Berechnung zu aufwändig
        # Prüfe, ob das Polynom eine maximale Periode hat
        x = [0] * (degree + 1)
        x[degree - 1] = 1  # x entspricht x^1

        state = x.copy()
        seen_states = [state.copy()]

        for _ in range(period):
            # Berechne x * state mod poly
            state = multiply_polynomials_gf2(x, state)
            state = polynomial_mod_gf2(state, poly)

            # Prüfe, ob dieser Zustand bereits gesehen wurde
            if state in seen_states and state != [0] * degree + [1]:
                return False

            seen_states.append(state.copy())

        # Wenn wir alle Zustände durchlaufen haben, ist das Polynom primitiv
        return True

    # Für größere Grade: approximiere über bekannte Eigenschaften
    # (Dies ist eine Vereinfachung - für eine genaue Prüfung sind umfangreichere Berechnungen nötig)
    return is_irreducible_polynomial(poly)


def multiply_polynomials_gf2(a, b):
    """
    Multipliziert zwei Polynome im GF(2)

    Argumente:
        a, b: Listen mit Koeffizienten, höchste Potenz zuerst
    Rückgabe:
        Liste mit Koeffizienten des Produkts
    """
    if not a or not b:
        return [0]

    result = [0] * (len(a) + len(b) - 1)

    for i in range(len(a)):
        for j in range(len(b)):
            if a[i] and b[j]:
                result[i + j] = (result[i + j] + 1) % 2

    return result


def polynomial_mod_gf2(poly, modulus):
    """
    Berechnet poly mod modulus im GF(2)

    Argumente:
        poly, modulus: Listen mit Koeffizienten, höchste Potenz zuerst
    Rückgabe:
        Liste mit Koeffizienten des Rests
    """
    _, remainder = polynomial_division_gf2(poly, modulus)
    return remainder


def generate_extension_field_elements(poly, max_elements=None):
    """
    Generiert Elemente des Erweiterungsfelds GF(2^m) mit dem gegebenen Polynom

    Argumente:
        poly: Primitives Polynom als Liste mit Koeffizienten, höchste Potenz zuerst
        max_elements: Maximale Anzahl zu generierender Elemente (für große Felder)
    Rückgabe:
        Liste der generierten Elemente
    """
    degree = len(poly) - 1
    if not max_elements:
        max_elements = 2 ** degree - 1

    # Initialisiere mit α^1 (entspricht x)
    alpha = [0] * degree
    alpha[degree - 2] = 1  # x entspricht der Basis im Erweiterungsfeld

    elements = [[1] + [0] * (degree - 1)]  # Starte mit 1 (α^0)
    elements.append(alpha.copy())  # Füge α^1 hinzu

    # Berechne α^i für i = 2 bis max_elements
    for i in range(2, max_elements + 1):
        # α^i = α^(i-1) * α
        next_power = [0] * (2 * degree - 1)  # Produkt hat Grad 2*degree-2

        # Multiplikation: alpha^(i-1) * alpha
        for j in range(degree):
            if elements[-1][j] == 1:
                for k in range(degree):
                    if alpha[k] == 1:
                        next_power[j + k] = (next_power[j + k] + 1) % 2

        # Reduktion modulo des primitiven Polynoms
        result = [0] * degree

        # Kopiere die niedrigen Koeffizienten direkt
        for j in range(degree):
            result[j] = next_power[j]

        # Reduziere die höheren Koeffizienten
        for j in range(degree, len(next_power)):
            if next_power[j] == 1:
                # Subtrahiere x^(j-degree) * primitives_polynom
                for k in range(len(poly)):
                    if poly[k] == 1:
                        idx = j - degree + k
                        if idx < len(result):
                            result[idx] = (result[idx] + 1) % 2

        elements.append(result)

    return elements

def blockcode_menu():
    global current_menu
    current_menu = "blockcode"

    while current_menu == "blockcode":
        clear_screen()
        print("==== Blockcode-Eigenschaften ====")
        print("1. Prüfen ob Code dichtgepackt ist")
        print("2. Hamming-Prüfmatrix generieren")
        print("0. Zurück zum Hauptmenü")

        choice = input("\nWähle eine Option: ")

        if choice == "1":
            # Dichtgepackt prüfen
            clear_screen()
            print("==== Prüfen ob Code dichtgepackt ist ====")
            try:
                n = int(input("Codewortlänge n: "))
                k = int(input("Anzahl Informationsbits k: "))
                d = int(input("Minimale Hamming-Distanz d: "))

                result = is_densely_packed(n, k, d)

                if result:
                    print(f"\nDer ({n},{k},{d})-Code ist dichtgepackt!")
                else:
                    print(f"\nDer ({n},{k},{d})-Code ist NICHT dichtgepackt.")

                # Zeige Berechnungsdetails
                num_codewords = 2 ** k
                t = (d - 1) // 2

                sphere_size = 0
                for i in range(t + 1):
                    sphere_size += binomial(n, i)

                total_words = 2 ** n
                packed_size = num_codewords * sphere_size

                print(f"\nAnzahl der Codewörter: 2^{k} = {num_codewords}")
                print(f"Korrigierbare Fehler: t = ({d}-1)/2 = {t}")
                print(f"Größe der Korrekturkugel: {sphere_size}")
                print(f"Anzahl aller Wörter: 2^{n} = {total_words}")
                print(f"Codewörter * Kugel: {num_codewords} * {sphere_size} = {packed_size}")
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "2":
            # Hamming-Prüfmatrix
            clear_screen()
            print("==== Hamming-Prüfmatrix generieren ====")
            try:
                r = int(input("Anzahl der Prüfbits r: "))

                H = create_hamming_parity_matrix(r)
                n = 2 ** r - 1

                print(f"\nPrüfmatrix für ({n},{n - r},{3})-Hamming-Code:")
                for i in range(r):
                    print(' '.join(str(bit) for bit in H[i]))
            except Exception as e:
                print(f"Fehler: {str(e)}")
            pause()

        elif choice == "0":
            current_menu = "main"


def main_menu():
    global current_menu
    current_menu = "main"

    while True:
        clear_screen()
        print("==== ICTh Prüfungstool ====")
        print("1. Entropie und Kompression")
        print("2. RSA Verschlüsselung")
        print("3. Kanalcodierung")
        print("4. Faltungscodes")
        print("5. Kanalmodell")
        print("6. Binärzahlen und Darstellung")
        print("7. Zyklische Codes")
        print("8. Markov-Quellen und Gedächtnis")  # Neue Option
        print("9. Blockcode-Eigenschaften")       # Neue Option
        print("10. Polynomprüfung")               # Neue Option
        print("0. Beenden")

        choice = input("\nWähle eine Option: ")

        if choice == "1":
            entropie_menu()
        elif choice == "2":
            rsa_menu()
        elif choice == "3":
            kanal_menu()
        elif choice == "4":
            faltungscode_menu()
        elif choice == "5":
            kanalmodell_menu()
        elif choice == "6":
            binär_menu()
        elif choice == "7":
            zyklischer_code_menu()
        elif choice == "8":
            markov_menu()  # Neues Menü
        elif choice == "9":
            blockcode_menu()  # Neues Menü
        elif choice == "10":
            polynomial_menu()  # Neues Menü
        elif choice == "0":
            print("Beenden des Programms...")
            break
        else:
            print("Ungültige Eingabe!")
            pause()
# Starte das Programm
if __name__ == "__main__":
    main_menu()