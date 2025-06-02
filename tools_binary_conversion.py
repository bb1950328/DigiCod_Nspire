from tool_base import Tool


class BinaryConverter(Tool):
    def run(self):
        while True:
            print("=== BINÄR KONVERTER ===")
            print("1) -> Dezimal")
            print("2) -> Hexadezimal")
            print("3) -> Oktal")
            print("4) -> Zweierkomplement")
            print("5) -> Float")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice in ['1', '2', '3', '4', '5']:
                self._convert_from_binary(choice)
            else:
                print("Ungültige Eingabe!")
            print()

    def _convert_from_binary(self, choice):
        binary = input("Binärzahl (z.B. 1010): ").strip()
        if not binary or not all(c in '01' for c in binary):
            print("Fehler: Ungültige Binärzahl!")
            input("Enter zum Fortfahren...")
            return

        try:
            if choice == '1':  # Zu Dezimal
                decimal = int(binary, 2)
                print("Dezimal: {}".format(decimal))

            elif choice == '2':  # Zu Hex
                decimal = int(binary, 2)
                print("Hex: {:X}".format(decimal))

            elif choice == '3':  # Zu Oktal
                decimal = int(binary, 2)
                print("Oktal: {:o}".format(decimal))

            elif choice == '4':  # Zweierkomplement
                if binary[0] == '1':
                    # Negativ: Bits invertieren und +1
                    inverted = ''.join('1' if b == '0' else '0' for b in binary)
                    decimal = -(int(inverted, 2) + 1)
                else:
                    decimal = int(binary, 2)
                print("2er-Kompl.: {}".format(decimal))

            elif choice == '5':  # Float
                print("Binär als Float-Bits:")
                if len(binary) == 32:
                    sign = binary[0]
                    exp = binary[1:9]
                    mant = binary[9:]
                    print("S:{} E:{} M:{}".format(sign, exp, mant))
                else:
                    print("32 Bit benötigt!")

        except Exception as e:
            print("Fehler bei Konvertierung!")

        input("Enter zum Fortfahren...")


class DecimalConverter(Tool):
    def run(self):
        while True:
            print("=== DEZIMAL KONVERTER ===")
            print("1) -> Binär")
            print("2) -> Hexadezimal")
            print("3) -> Oktal")
            print("4) -> Zweierkomplement")
            print("5) -> Exzess")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice in ['1', '2', '3', '4', '5']:
                self._convert_from_decimal(choice)
            else:
                print("Ungültige Eingabe!")
            print()

    def _convert_from_decimal(self, choice):
        try:
            decimal = int(input("Dezimalzahl (z.B. 42): "))

            if choice == '1':  # Zu Binär
                binary = bin(decimal)[2:] if decimal >= 0 else bin(decimal)[3:]
                print("Binär: {}".format(binary))

            elif choice == '2':  # Zu Hex
                print("Hex: {:X}".format(abs(decimal)))

            elif choice == '3':  # Zu Oktal
                print("Oktal: {:o}".format(abs(decimal)))

            elif choice == '4':  # Zweierkomplement
                bits = int(input("Bit-Anzahl (z.B. 8): "))
                if decimal >= 0:
                    binary = format(decimal, '0{}b'.format(bits))
                else:
                    # 2er-Komplement berechnen
                    positive = abs(decimal)
                    max_val = 2 ** bits
                    twos_comp = max_val - positive
                    binary = format(twos_comp, '0{}b'.format(bits))
                print("2er-Kompl.: {}".format(binary))

            elif choice == '5':  # Exzess
                bias = int(input("Bias (z.B. 127): "))
                excess_val = decimal + bias
                if excess_val >= 0:
                    print("Exzess: {}".format(excess_val))
                else:
                    print("Fehler: Negative Exzess-Zahl!")

        except ValueError:
            print("Fehler: Ungültige Eingabe!")

        input("Enter zum Fortfahren...")


class HexConverter(Tool):
    def run(self):
        while True:
            print("=== HEX KONVERTER ===")
            print("1) -> Dezimal")
            print("2) -> Binär")
            print("3) -> Oktal")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice in ['1', '2', '3']:
                self._convert_from_hex(choice)
            else:
                print("Ungültige Eingabe!")
            print()

    def _convert_from_hex(self, choice):
        hex_str = input("Hex ohne 0x (z.B. A3F): ").strip().upper()
        try:
            decimal = int(hex_str, 16)

            if choice == '1':  # Zu Dezimal
                print("Dezimal: {}".format(decimal))

            elif choice == '2':  # Zu Binär
                binary = bin(decimal)[2:]
                print("Binär: {}".format(binary))
                show_details = input("Details? (d/Enter): ").strip().lower()
                if show_details == 'd':
                    # Zeige gruppierte Darstellung
                    padded = binary.zfill((len(binary) + 3) // 4 * 4)
                    groups = [padded[i:i + 4] for i in range(0, len(padded), 4)]
                    print("Gruppiert: {}".format(" ".join(groups)))

            elif choice == '3':  # Zu Oktal
                print("Oktal: {:o}".format(decimal))

        except ValueError:
            print("Fehler: Ungültige Hex-Zahl!")

        input("Enter zum Fortfahren...")


class OctalConverter(Tool):
    def run(self):
        while True:
            print("=== OKTAL KONVERTER ===")
            print("1) -> Dezimal")
            print("2) -> Binär")
            print("3) -> Hexadezimal")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice in ['1', '2', '3']:
                self._convert_from_octal(choice)
            else:
                print("Ungültige Eingabe!")
            print()

    def _convert_from_octal(self, choice):
        octal_str = input("Oktalzahl (z.B. 157): ").strip()
        try:
            decimal = int(octal_str, 8)

            if choice == '1':  # Zu Dezimal
                print("Dezimal: {}".format(decimal))

            elif choice == '2':  # Zu Binär
                binary = bin(decimal)[2:]
                print("Binär: {}".format(binary))

            elif choice == '3':  # Zu Hex
                print("Hex: {:X}".format(decimal))

        except ValueError:
            print("Fehler: Ungültige Oktal-Zahl!")

        input("Enter zum Fortfahren...")


class FixedPointConverter(Tool):
    def run(self):
        while True:
            print("=== FIXKOMMA KONVERTER ===")
            print("1) Dezimal -> Fixkomma")
            print("2) Fixkomma -> Dezimal")
            print("3) Rechnen mit Fixkomma")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice in ['1', '2', '3']:
                self._handle_fixed_point(choice)
            else:
                print("Ungültige Eingabe!")
            print()

    def _handle_fixed_point(self, choice):
        try:
            if choice == '1':  # Dezimal zu Fixkomma
                decimal = float(input("Dezimalzahl (z.B. 5.25): "))
                total_bits = int(input("Gesamt-Bits (z.B. 16): "))
                frac_bits = int(input("Nachkomma-Bits (z.B. 8): "))

                scale = 2 ** frac_bits
                fixed_int = int(decimal * scale)
                binary = format(fixed_int & ((1 << total_bits) - 1), '0{}b'.format(total_bits))

                print("Fixkomma: {}".format(binary))
                print("Skalierung: 2^{}".format(frac_bits))

                show_details = input("Details? (d/Enter): ").strip().lower()
                if show_details == 'd':
                    # Rekonstruierte Zahl zeigen
                    reconstructed = self._fixed_to_decimal(binary, frac_bits)
                    print("Rekonstruiert: {}".format(reconstructed))
                    print("Differenz: {}".format(abs(decimal - reconstructed)))

            elif choice == '2':  # Fixkomma zu Dezimal
                binary = input("Fixkomma-Binär (z.B. 0101010000000000): ").strip()
                frac_bits = int(input("Nachkomma-Bits (z.B. 8): "))

                decimal = self._fixed_to_decimal(binary, frac_bits)
                print("Dezimal: {}".format(decimal))

            elif choice == '3':  # Rechnen
                print("Addition/Subtraktion:")
                a = input("Fixkomma A (z.B. 0101000000000000): ").strip()
                b = input("Fixkomma B (z.B. 0010000000000000): ").strip()
                op = input("Operation (+/-): ").strip()

                val_a = int(a, 2)
                val_b = int(b, 2)

                if op == '+':
                    result = val_a + val_b
                elif op == '-':
                    result = val_a - val_b
                else:
                    print("Unbekannte Operation!")
                    input("Enter zum Fortfahren...")
                    return

                bits = max(len(a), len(b))
                result_bin = format(result & ((1 << bits) - 1), '0{}b'.format(bits))
                print("Ergebnis: {}".format(result_bin))

        except ValueError:
            print("Fehler: Ungültige Eingabe!")

        input("Enter zum Fortfahren...")

    def _fixed_to_decimal(self, binary, frac_bits):
        """Konvertiert Fixkomma-Binär zu Dezimal"""
        if binary[0] == '1' and len(binary) > 1:
            # Negative Zahl (2er-Komplement)
            inverted = ''.join('1' if b == '0' else '0' for b in binary)
            fixed_int = -(int(inverted, 2) + 1)
        else:
            fixed_int = int(binary, 2)

        return fixed_int / (2 ** frac_bits)


class FloatConverter(Tool):
    def run(self):
        while True:
            print("=== FLOAT KONVERTER ===")
            print("1) Dezimal -> IEEE-754")
            print("2) IEEE-754 -> Dezimal")
            print("3) Float-Addition")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice in ['1', '2', '3']:
                self._handle_float(choice)
            else:
                print("Ungültige Eingabe!")
            print()

    def _handle_float(self, choice):
        try:
            if choice == '1':  # Dezimal zu IEEE-754
                decimal = float(input("Dezimalzahl (z.B. 3.14): "))
                ieee = self._float_to_ieee754(decimal)
                print("IEEE-754: {}".format(ieee))

                show_details = input("Details? (d/Enter): ").strip().lower()
                if show_details == 'd':
                    sign = ieee[0]
                    exp = ieee[1:9]
                    mant = ieee[9:]
                    print("Sign: {}".format(sign))
                    print("Exp: {} ({})".format(exp, int(exp, 2) - 127))
                    print("Mant: {}".format(mant))

                    # Rekonstruierte Zahl zeigen
                    reconstructed = self._ieee754_to_float(ieee)
                    print("Rekonstruiert: {}".format(reconstructed))
                    print("Differenz: {}".format(abs(decimal - reconstructed)))

            elif choice == '2':  # IEEE-754 zu Dezimal
                ieee = input("IEEE-754 32bit (z.B. 01000000010010010000111111011011): ").strip()
                if len(ieee) != 32:
                    print("Fehler: 32 Bit benötigt!")
                    input("Enter zum Fortfahren...")
                    return

                decimal = self._ieee754_to_float(ieee)
                print("Dezimal: {}".format(decimal))

            elif choice == '3':  # Addition
                print("Float-Addition (vereinfacht):")
                a = float(input("Zahl A (z.B. 2.5): "))
                b = float(input("Zahl B (z.B. 3.14): "))
                result = a + b
                print("A + B = {}".format(result))

                show_details = input("IEEE Details? (d/Enter): ").strip().lower()
                if show_details == 'd':
                    ieee_a = self._float_to_ieee754(a)
                    ieee_b = self._float_to_ieee754(b)
                    ieee_r = self._float_to_ieee754(result)
                    print("A: {}".format(ieee_a))
                    print("B: {}".format(ieee_b))
                    print("R: {}".format(ieee_r))

        except ValueError:
            print("Fehler: Ungültige Eingabe!")

        input("Enter zum Fortfahren...")

    def _float_to_ieee754(self, f):
        """Vereinfachte IEEE-754 Konvertierung"""
        if f == 0:
            return '0' * 32

        sign = '1' if f < 0 else '0'
        f = abs(f)

        # Sehr vereinfachte Implementierung
        # Für Prüfungszwecke ausreichend
        try:
            # Nutze eingebaute float-zu-bits Konvertierung wo möglich
            import struct
            bits = struct.unpack('>I', struct.pack('>f', f if sign == '0' else -f))[0]
            return format(bits, '032b')
        except:
            # Fallback für MicroPython
            return '0' * 32  # Platzhalter

    def _ieee754_to_float(self, ieee):
        """Vereinfachte IEEE-754 Dekodierung"""
        try:
            sign = int(ieee[0])
            exp_bits = ieee[1:9]
            mant_bits = ieee[9:]

            exp = int(exp_bits, 2) - 127

            # Vereinfachte Berechnung
            mant_val = 1.0  # Implizite 1
            for i, bit in enumerate(mant_bits):
                if bit == '1':
                    mant_val += 2 ** -(i + 1)

            result = mant_val * (2 ** exp)
            return -result if sign else result

        except:
            return 0.0


class ExcessConverter(Tool):
    def run(self):
        while True:
            print("=== EXZESS KONVERTER ===")
            print("1) Dezimal -> Exzess")
            print("2) Exzess -> Dezimal")
            print("3) Exzess-Binär -> Dezimal")
            print("4) Dezimal -> Exzess-Binär")
            print("5) Exzess-Rechnung")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice in ['1', '2', '3', '4', '5']:
                self._handle_excess(choice)
            else:
                print("Ungültige Eingabe!")
            print()

    def _handle_excess(self, choice):
        try:
            if choice == '1':  # Dezimal zu Exzess
                decimal = int(input("Dezimalzahl (z.B. -10): "))
                bias = int(input("Bias (z.B. 127): "))

                excess_val = decimal + bias
                print("Exzess-Wert: {}".format(excess_val))

            elif choice == '2':  # Exzess zu Dezimal
                excess_val = int(input("Exzess-Wert (z.B. 117): "))
                bias = int(input("Bias (z.B. 127): "))

                decimal = excess_val - bias
                print("Dezimal: {}".format(decimal))

            elif choice == '3':  # Exzess-Binär zu Dezimal
                binary = input("Exzess-Binär (z.B. 01110101): ").strip()
                bias = int(input("Bias (z.B. 127): "))

                excess_val = int(binary, 2)
                decimal = excess_val - bias
                print("Exzess-Wert: {}".format(excess_val))
                print("Dezimal: {}".format(decimal))

            elif choice == '4':  # Dezimal zu Exzess-Binär
                decimal = int(input("Dezimalzahl (z.B. -10): "))
                bias = int(input("Bias (z.B. 127): "))
                bits = int(input("Bit-Anzahl (z.B. 8): "))

                excess_val = decimal + bias
                if excess_val < 0 or excess_val >= 2 ** bits:
                    print("Fehler: Außerhalb des Bereichs!")
                    input("Enter zum Fortfahren...")
                    return

                binary = format(excess_val, '0{}b'.format(bits))
                print("Exzess-Wert: {}".format(excess_val))
                print("Exzess-Binär: {}".format(binary))

            elif choice == '5':  # Rechnung
                print("Exzess-Addition:")
                print("ACHTUNG: Bias 2x abziehen!")

                a_bin = input("Exzess A (z.B. 10000001): ").strip()
                b_bin = input("Exzess B (z.B. 10000010): ").strip()
                bias = int(input("Bias (z.B. 127): "))

                a_val = int(a_bin, 2)
                b_val = int(b_bin, 2)

                # Addition und Bias-Korrektur
                sum_val = a_val + b_val
                corrected = sum_val - bias

                bits = max(len(a_bin), len(b_bin))
                result_bin = format(corrected, '0{}b'.format(bits))

                print("Summe: {}".format(sum_val))
                print("Korrigiert: {}".format(corrected))
                print("Binär: {}".format(result_bin))

        except ValueError:
            print("Fehler: Ungültige Eingabe!")

        input("Enter zum Fortfahren...")


class TwosComplementConverter(Tool):
    def run(self):
        while True:
            print("=== ZWEIERKOMPLEMENT ===")
            print("1) Dezimal -> 2er-Kompl.")
            print("2) 2er-Kompl. -> Dezimal")
            print("3) Addition/Subtraktion")
            print("4) Multiplikation")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice in ['1', '2', '3', '4']:
                self._handle_twos_complement(choice)
            else:
                print("Ungültige Eingabe!")
            print()

    def _handle_twos_complement(self, choice):
        try:
            if choice == '1':  # Dezimal zu 2er-Komplement
                decimal = int(input("Dezimalzahl (z.B. -5): "))
                bits = int(input("Bit-Anzahl (z.B. 8): "))

                if decimal >= 0:
                    binary = format(decimal, '0{}b'.format(bits))
                else:
                    # 2er-Komplement berechnen
                    positive = abs(decimal)
                    max_val = 2 ** bits
                    twos_comp = max_val - positive
                    binary = format(twos_comp, '0{}b'.format(bits))

                print("2er-Kompl.: {}".format(binary))

            elif choice == '2':  # 2er-Komplement zu Dezimal
                binary = input("2er-Kompl. (z.B. 11111011): ").strip()

                decimal = self._twos_comp_to_decimal(binary)
                print("Dezimal: {}".format(decimal))

            elif choice == '3':  # Addition/Subtraktion
                a = input("2er-Kompl. A (z.B. 11111100): ").strip()
                b = input("2er-Kompl. B (z.B. 00000011): ").strip()
                op = input("Operation (+/-): ").strip()

                # Zu Dezimal konvertieren
                dec_a = self._twos_comp_to_decimal(a)
                dec_b = self._twos_comp_to_decimal(b)

                if op == '+':
                    result_dec = dec_a + dec_b
                elif op == '-':
                    result_dec = dec_a - dec_b
                else:
                    print("Unbekannte Operation!")
                    input("Enter zum Fortfahren...")
                    return

                # Zurück zu 2er-Komplement
                bits = max(len(a), len(b))
                result_bin = self._decimal_to_twos_comp(result_dec, bits)

                print("Ergebnis: {}".format(result_bin))
                print("Dezimal: {}".format(result_dec))

            elif choice == '4':  # Multiplikation
                a = input("2er-Kompl. A (z.B. 1100): ").strip()
                b = input("2er-Kompl. B (z.B. 0011): ").strip()

                # Zu Dezimal konvertieren
                dec_a = self._twos_comp_to_decimal(a)
                dec_b = self._twos_comp_to_decimal(b)

                result_dec = dec_a * dec_b

                # Zurück zu 2er-Komplement (doppelte Bitanzahl für Produkt)
                bits = len(a) + len(b)
                result_bin = self._decimal_to_twos_comp(result_dec, bits)

                print("Produkt: {}".format(result_bin))
                print("Dezimal: {}".format(result_dec))
                print("Bit-Länge: {}".format(bits))

                show_details = input("Schritte zeigen? (d/Enter): ").strip().lower()
                if show_details == 'd':
                    print("A = {} = {}".format(a, dec_a))
                    print("B = {} = {}".format(b, dec_b))
                    print("A x B = {} x {} = {}".format(dec_a, dec_b, result_dec))

                    # Zeige auch das ursprüngliche Bit-Format
                    orig_bits = max(len(a), len(b))
                    truncated = result_bin[-orig_bits:] if len(result_bin) > orig_bits else result_bin
                    print("Gekürzt auf {} Bit: {}".format(orig_bits, truncated))

        except ValueError:
            print("Fehler: Ungültige Eingabe!")

        input("Enter zum Fortfahren...")

    def _twos_comp_to_decimal(self, binary):
        if binary[0] == '1':
            inverted = ''.join('1' if b == '0' else '0' for b in binary)
            return -(int(inverted, 2) + 1)
        else:
            return int(binary, 2)

    def _decimal_to_twos_comp(self, decimal, bits):
        if decimal >= 0:
            return format(decimal, '0{}b'.format(bits))
        else:
            max_val = 2 ** bits
            twos_comp = max_val + decimal  # decimal ist negativ
            return format(twos_comp, '0{}b'.format(bits))