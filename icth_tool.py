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
                data = input("Daten (Bitfolge): ")
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
        print("7. Beenden")

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
            print("Beenden des Programms...")
            break
        else:
            print("Ungültige Eingabe!")
            pause()


# Starte das Programm
if __name__ == "__main__":
    main_menu()