class BaseChannelCodingTool:
    """Basis-Klasse für alle Kanalcodierung-Tools mit gemeinsamen Funktionen"""

    def __init__(self):
        self.tolerance = 1e-6

    def validate_binary_string(self, binary_str, name="Binärstring", min_length=1, max_length=None):
        """Validiert Binärstring"""
        errors = []
        warnings = []

        if not binary_str:
            errors.append("FEHLER: " + name + " ist leer")
            return errors, warnings

        # Entferne Leerzeichen und Apostrophe für Toleranz
        clean_str = binary_str.replace(" ", "").replace("'", "")

        # Prüfe auf gültige Zeichen
        for c in clean_str:
            if c not in '01':
                errors.append("FEHLER: " + name + " enthält ungültige Zeichen: " + c)
                break

        # Prüfe Länge
        if len(clean_str) < min_length:
            errors.append("FEHLER: " + name + " zu kurz: " + str(len(clean_str)) + " < " + str(min_length))

        if max_length and len(clean_str) > max_length:
            errors.append("FEHLER: " + name + " zu lang: " + str(len(clean_str)) + " > " + str(max_length))

        return errors, warnings

    def validate_generator_polynomial(self, poly, name="Generatorpolynom"):
        """Validiert Generatorpolynom"""
        errors = []
        warnings = []

        # Basis-Validierung
        poly_errors, poly_warnings = self.validate_binary_string(poly, name, min_length=2)
        errors.extend(poly_errors)
        warnings.extend(poly_warnings)

        if errors:
            return errors, warnings

        clean_poly = poly.replace(" ", "").replace("'", "")
        poly_vec = self.binary_to_vector(clean_poly)

        # Muss mit 1 beginnen (höchster Koeffizient)
        if poly_vec[0] != 1:
            errors.append("FEHLER: " + name + " muss mit 1 beginnen")

        # Muss mit 1 enden (konstanter Term)
        if poly_vec[-1] != 1:
            errors.append("FEHLER: " + name + " muss mit 1 enden")

        # Grad sollte sinnvoll sein
        degree = len(poly_vec) - 1
        if degree < 1:
            errors.append("FEHLER: " + name + " Grad " + str(degree) + " < 1")
        elif degree > 20:
            warnings.append("WARNUNG: " + name + " Grad " + str(degree) + " > 20 (sehr hoch)")

        return errors, warnings

    def safe_binary_input(self, prompt, min_length=1, max_length=32):
        """Sichere Eingabe von Binärstrings"""
        while True:
            try:
                value = input(prompt).strip()
                value = value.replace(" ", "").replace("'", "")

                valid = True
                for c in value:
                    if c not in '01':
                        valid = False
                        break

                if not valid:
                    print("❌ Nur 0 und 1 erlaubt. Bitte erneut eingeben.")
                    continue

                if len(value) < min_length:
                    print("❌ Mindestens " + str(min_length) + " Bits erforderlich.")
                    continue

                if len(value) > max_length:
                    print("❌ Maximal " + str(max_length) + " Bits erlaubt.")
                    continue

                return value
            except:
                print("❌ Ungültige Eingabe. Bitte erneut eingeben.")
                continue

    def safe_int_input(self, prompt, min_val=1, max_val=100):
        """Sichere Eingabe von Ganzzahlen mit Validierung"""
        while True:
            try:
                value = int(input(prompt))
                if value < min_val:
                    print("❌ Wert " + str(value) + " < " + str(min_val) + " (Minimum).")
                    continue
                if value > max_val:
                    print("❌ Wert " + str(value) + " > " + str(max_val) + " (Maximum).")
                    continue
                return value
            except:
                print("❌ Ungültige Eingabe. Bitte eine Ganzzahl eingeben.")
                continue

    def binary_to_vector(self, binary_str):
        """Konvertiert Binärstring zu Vektor"""
        return [int(bit) for bit in binary_str]

    def vector_to_binary(self, vector):
        """Konvertiert Vektor zu Binärstring"""
        return ''.join(str(bit) for bit in vector)

    def xor_vectors(self, vec1, vec2):
        """XOR-Operation zwischen zwei Vektoren"""
        if len(vec1) != len(vec2):
            raise ValueError("Vektoren haben unterschiedliche Längen")
        result = []
        for i in range(len(vec1)):
            result.append((vec1[i] + vec2[i]) % 2)
        return result

    def hamming_distance(self, codeword1, codeword2, validate=True):
        """Berechnet Hamming-Distanz zwischen zwei Codewörtern"""
        if validate:
            errors1, _ = self.validate_binary_string(codeword1, "Codewort 1")
            errors2, _ = self.validate_binary_string(codeword2, "Codewort 2")

            if errors1 or errors2:
                print("❌ HAMMING-DISTANZ BERECHNUNG ABGEBROCHEN:")
                for error in errors1 + errors2:
                    print("   " + error)
                return None

        clean_cw1 = codeword1.replace(" ", "").replace("'", "")
        clean_cw2 = codeword2.replace(" ", "").replace("'", "")

        if len(clean_cw1) != len(clean_cw2):
            print("❌ FEHLER: Codewörter haben unterschiedliche Längen")
            return None

        vec1 = self.binary_to_vector(clean_cw1)
        vec2 = self.binary_to_vector(clean_cw2)

        distance = 0
        for i in range(len(vec1)):
            if vec1[i] != vec2[i]:
                distance += 1

        return distance


class HammingDistanceTool(BaseChannelCodingTool):
    """Tool zur Berechnung der Hamming-Distanz zwischen Codewörtern"""

    def minimum_hamming_distance(self, codewords, validate=True):
        """Bestimmt minimale Hamming-Distanz eines Codes"""
        print("\n==== MINIMALE HAMMING-DISTANZ ====")

        print("Gegebene Codewörter:")
        for i in range(len(codewords)):
            print("  CW" + str(i) + ": " + codewords[i])

        clean_codewords = []
        for cw in codewords:
            clean_codewords.append(cw.replace(" ", "").replace("'", ""))

        print("\nHamming-Distanzen zwischen allen Paaren:")
        min_distance = 999999
        min_pair = None

        distances = []
        for i in range(len(clean_codewords)):
            for j in range(i + 1, len(clean_codewords)):
                dist = self.hamming_distance(clean_codewords[i], clean_codewords[j], validate=False)
                if dist is None:
                    return None

                distances.append((i, j, dist))
                print("  d(CW" + str(i) + ", CW" + str(j) + ") = " + str(dist))

                if dist < min_distance:
                    min_distance = dist
                    min_pair = (i, j)

        print("\nMinimale Hamming-Distanz: h = " + str(min_distance))
        print("Erreicht zwischen CW" + str(min_pair[0]) + " und CW" + str(min_pair[1]))

        detectable_errors = min_distance - 1
        correctable_errors = (min_distance - 1) // 2

        print("\nFehlerkapazität:")
        print("  Erkennbare Fehler: e* = h - 1 = " + str(min_distance) + " - 1 = " + str(detectable_errors))
        print("  Korrigierbare Fehler: e = floor((h-1)/2) = " + str(correctable_errors))

        return {
            'min_distance': min_distance,
            'min_pair': min_pair,
            'detectable_errors': detectable_errors,
            'correctable_errors': correctable_errors,
            'all_distances': distances
        }

    def run(self):
        """Führt die Hamming-Distanz Berechnung durch"""
        try:
            print("\n=== HAMMING-DISTANZ BERECHNEN ===")
            n_codewords = self.safe_int_input("Anzahl Codewörter: ", min_val=2, max_val=20)

            codewords = []
            print("\nEingabe der Codewörter:")

            for i in range(n_codewords):
                while True:
                    cw = input("Codewort " + str(i + 1) + ": ").strip()
                    errors, warnings = self.validate_binary_string(cw, "Codewort " + str(i + 1))

                    if not errors:
                        clean_cw = cw.replace(" ", "").replace("'", "")
                        if codewords:
                            expected_length = len(codewords[0].replace(" ", "").replace("'", ""))
                            if len(clean_cw) != expected_length:
                                print("❌ Länge " + str(len(clean_cw)) + " ≠ " + str(expected_length) + " (erwartet).")
                                continue

                        codewords.append(cw)
                        break
                    else:
                        for error in errors:
                            print("❌ " + error)
                        print("Bitte erneut eingeben.")

            self.minimum_hamming_distance(codewords, validate=True)

        except Exception as e:
            print("❌ Fehler: " + str(e))

        input("\nDrücke Enter zum Fortfahren...")


class ParityMatrixTool(BaseChannelCodingTool):
    """Tool zur Erstellung einer Prüfmatrix aus Prüfgleichungen"""

    def create_parity_check_matrix(self, equations, validate=True):
        """Erstellt Prüfmatrix aus Prüfgleichungen"""
        print("\n==== PRÜFMATRIX ERSTELLEN ====")

        if validate:
            if not equations:
                print("❌ FEHLER: Keine Prüfgleichungen gegeben")
                return None

            for i in range(len(equations)):
                eq = equations[i]
                if not eq:
                    print("❌ FEHLER: Prüfgleichung " + str(i + 1) + " ist leer")
                    return None

                for pos in eq:
                    if not isinstance(pos, int) or pos <= 0:
                        print("❌ FEHLER: Ungültige Position in Gleichung " + str(i + 1))
                        return None

        print("Gegebene Prüfgleichungen:")
        max_pos = 0
        for eq in equations:
            for pos in eq:
                if pos > max_pos:
                    max_pos = pos

        for i in range(len(equations)):
            eq = equations[i]
            equation_parts = []
            for pos in eq:
                equation_parts.append("x_" + str(pos))
            equation_str = " + ".join(equation_parts)
            check_pos = max_pos + i + 1
            print("  " + equation_str + " = x_" + str(check_pos))

        n_bits = max_pos + len(equations)

        print("\nCode-Parameter:")
        print("  Codelänge: n = " + str(n_bits))
        print("  Kontrollbits: n-k = " + str(len(equations)))
        print("  Informationsbits: k = " + str(n_bits - len(equations)))
        print("  Gültige codewörter: = " + str(2 ** (n_bits - len(equations))))
        print("  Mögliche codewörter: = " + str(2 ** (n_bits)))

        H = []
        for i in range(len(equations)):
            eq = equations[i]
            row = []
            for j in range(n_bits):
                row.append(0)

            for pos in eq:
                row[pos - 1] = 1
            row[max_pos + i] = 1
            H.append(row)

        print("\nPrüfmatrix H (" + str(len(H)) + "×" + str(n_bits) + "):")
        print("      ", end="")
        for j in range(n_bits):
            print("x" + str(j + 1).rjust(2), end=" ")
        print()

        for i in range(len(H)):
            row = H[i]
            print("p" + str(i + 1) + ": ", end="")
            for val in row:
                print(" " + str(val).rjust(2), end=" ")
            print()

        return H

    def run(self):
        """Führt die Erstellung einer Prüfmatrix durch"""
        try:
            print("\n=== PRÜFMATRIX AUS PRÜFGLEICHUNGEN ===")
            n_equations = self.safe_int_input("Anzahl Prüfgleichungen: ", min_val=1, max_val=10)

            equations = []
            print("\nEingabe der Prüfgleichungen:")
            print("Positionen durch Leerzeichen getrennt eingeben")
            print("Beispiel: '1 2 3' für x₁ + x₂ + x₃ = x_check")

            for i in range(n_equations):
                while True:
                    try:
                        print("\nPrüfgleichung " + str(i + 1) + ":")
                        positions_str = input("Bit-Positionen: ").strip()

                        if not positions_str:
                            print("❌ Keine Eingabe.")
                            continue

                        positions = []
                        for x in positions_str.split():
                            positions.append(int(x))

                        valid = True
                        for pos in positions:
                            if pos <= 0:
                                valid = False
                                break

                        if not valid:
                            print("❌ Alle Positionen müssen > 0 sein.")
                            continue

                        equations.append(positions)
                        pos_strs = []
                        for pos in positions:
                            pos_strs.append("x_" + str(pos))
                        print("✅ Gleichung: " + " + ".join(pos_strs))
                        break

                    except:
                        print("❌ Ungültige Eingabe.")
                        continue

            H = self.create_parity_check_matrix(equations, validate=True)

            if H:
                calc_syndrome = input("\nFehlersyndrom berechnen? (j/n): ").lower()
                if calc_syndrome == 'j':
                    n_bits = len(H[0])
                    word = self.safe_binary_input("Wort (" + str(n_bits) + " Bits): ",
                                                  min_length=n_bits, max_length=n_bits)

                    # Hier würde das ErrorSyndromeTool verwendet werden
                    syndrome_tool = ErrorSyndromeTool()
                    syndrome_tool.calculate_error_syndrome(word, H, validate=True)

        except Exception as e:
            print("❌ Fehler: " + str(e))

        input("\nDrücke Enter zum Fortfahren...")


class ErrorSyndromeTool(BaseChannelCodingTool):
    """Tool zur Berechnung des Fehlersyndroms"""

    def calculate_error_syndrome(self, received_word, parity_check_matrix, validate=True):
        """Berechnet Fehlersyndrom"""
        print("\n==== FEHLERSYNDROM BERECHNEN ====")

        if validate:
            word_errors, _ = self.validate_binary_string(received_word, "Empfangenes Wort")

            if word_errors:
                print("❌ FEHLERSYNDROM-BERECHNUNG ABGEBROCHEN:")
                for error in word_errors:
                    print("   " + error)
                return None

        clean_word = received_word.replace(" ", "").replace("'", "")
        received_vec = self.binary_to_vector(clean_word)

        print("Empfangenes Wort: " + clean_word)

        if len(received_vec) != len(parity_check_matrix[0]):
            print("❌ FEHLER: Wortlänge stimmt nicht mit Prüfmatrix überein")
            return None

        syndrome = []
        print("\nSyndrom-Berechnung (s = H × r^T):")

        for i in range(len(parity_check_matrix)):
            row = parity_check_matrix[i]
            syndrome_bit = 0
            for j in range(len(received_vec)):
                syndrome_bit += row[j] * received_vec[j]
            syndrome_bit = syndrome_bit % 2
            syndrome.append(syndrome_bit)

            terms = []
            values = []
            for j in range(len(row)):
                if row[j] == 1:
                    terms.append("x" + str(j + 1))
                    values.append(str(received_vec[j]))

            if terms:
                equation = " + ".join(terms)
                calculation = " + ".join(values)
                print(
                    "  s" + str(i + 1) + ": " + equation + " = " + calculation + " = " + str(syndrome_bit) + " (mod 2)")
            else:
                print("  s" + str(i + 1) + ": 0 = " + str(syndrome_bit))

        syndrome_str = self.vector_to_binary(syndrome)
        print("\nFehlersyndrom: s = " + syndrome_str)

        error_detected = False
        for bit in syndrome:
            if bit != 0:
                error_detected = True
                break

        if not error_detected:
            print("✅ s = 0 → Kein Fehler erkannt")
        else:
            print("❌ s ≠ 0 → Fehler erkannt")

            syndrome_decimal = int(syndrome_str, 2)
            print("   Syndrom als Dezimalzahl: " + str(syndrome_decimal))

            if 1 <= syndrome_decimal <= len(received_vec):
                print("💡 Mögliche Fehlerposition: Bit " + str(syndrome_decimal))

                corrected_vec = received_vec[:]
                corrected_vec[syndrome_decimal - 1] = 1 - corrected_vec[syndrome_decimal - 1]
                corrected_word = self.vector_to_binary(corrected_vec)
                print("   Korrigiertes Wort: " + corrected_word)

        return {
            'syndrome': syndrome,
            'syndrome_str': syndrome_str,
            'syndrome_decimal': int(syndrome_str, 2),
            'error_detected': error_detected,
            'received_word': clean_word
        }

    def run(self):
        """Führt die Fehlersyndrom-Berechnung durch"""
        try:
            print("\n=== FEHLERSYNDROM BERECHNEN ===")

            print("Prüfmatrix H eingeben:")
            rows = self.safe_int_input("Anzahl Zeilen: ", min_val=1, max_val=10)
            cols = self.safe_int_input("Anzahl Spalten: ", min_val=1, max_val=20)

            H = []
            print("\nEingabe der Matrix (" + str(rows) + "×" + str(cols) + "):")

            for i in range(rows):
                while True:
                    row_str = input("Zeile " + str(i + 1) + ": ").strip()
                    errors, warnings = self.validate_binary_string(
                        row_str, "Zeile " + str(i + 1), min_length=cols, max_length=cols
                    )

                    if not errors:
                        clean_row = row_str.replace(" ", "").replace("'", "")
                        H.append(self.binary_to_vector(clean_row))
                        break
                    else:
                        for error in errors:
                            print("❌ " + error)
                        print("Bitte " + str(cols) + " Bits eingeben.")

            word = self.safe_binary_input("Empfangenes Wort (" + str(cols) + " Bits): ",
                                          min_length=cols, max_length=cols)

            syndrome_result = self.calculate_error_syndrome(word, H, validate=True)

            if syndrome_result:
                print("\n==== ZUSAMMENFASSUNG ====")
                print("Empfangenes Wort: " + syndrome_result['received_word'])
                print("Fehlersyndrom:    " + syndrome_result['syndrome_str'])
                if syndrome_result['error_detected']:
                    print("Fehler erkannt:   Ja")
                else:
                    print("Fehler erkannt:   Nein")

        except Exception as e:
            print("❌ Fehler: " + str(e))

        input("\nDrücke Enter zum Fortfahren...")


class CRCCalculationTool(BaseChannelCodingTool):
    """Tool zur CRC-Berechnung"""

    def polynomial_division_gf2(self, dividend, divisor, validate=True):
        """Polynomdivision in GF(2)"""
        print("\n==== POLYNOMDIVISION IN GF(2) ====")

        if isinstance(dividend, str):
            dividend_str = dividend.replace(" ", "").replace("'", "")
            dividend = self.binary_to_vector(dividend_str)
        else:
            dividend_str = self.vector_to_binary(dividend)

        if isinstance(divisor, str):
            divisor_str = divisor.replace(" ", "").replace("'", "")
            divisor = self.binary_to_vector(divisor_str)
        else:
            divisor_str = self.vector_to_binary(divisor)

        print("Dividend:  " + dividend_str)
        print("Divisor:   " + divisor_str)

        while len(dividend) > 1 and dividend[0] == 0:
            dividend = dividend[1:]
        while len(divisor) > 1 and divisor[0] == 0:
            divisor = divisor[1:]

        if len(dividend) < len(divisor):
            print("\nSpezialfall: Dividend-Grad < Divisor-Grad")
            print("Quotient: 0")
            print("Rest:     " + self.vector_to_binary(dividend))
            return [0], dividend

        quotient = []
        remainder = dividend[:]

        print("\nDivisions-Schritte:")
        step = 1

        while len(remainder) >= len(divisor):
            has_ones = False
            for bit in remainder:
                if bit == 1:
                    has_ones = True
                    break
            if not has_ones:
                break

            while len(remainder) > 1 and remainder[0] == 0:
                remainder = remainder[1:]

            if len(remainder) < len(divisor):
                break

            quotient.append(1)

            print("Schritt " + str(step) + ":")
            print("  " + self.vector_to_binary(remainder))

            for i in range(len(divisor)):
                if i < len(remainder):
                    remainder[i] = (remainder[i] + divisor[i]) % 2

            print("  " + self.vector_to_binary(divisor))
            print("  " + "-" * len(dividend_str))
            print("  " + self.vector_to_binary(remainder))
            print()

            if remainder and remainder[0] == 0:
                remainder = remainder[1:]

            step += 1

        if not quotient:
            quotient = [0]
        if not remainder:
            remainder = [0]

        quotient_str = self.vector_to_binary(quotient)
        remainder_str = self.vector_to_binary(remainder)

        print("Ergebnis:")
        print("  Quotient: " + quotient_str)
        print("  Rest:     " + remainder_str)

        return quotient, remainder

    def crc_calculation(self, data, generator_poly, validate=True):
        """CRC-Berechnung"""
        print("\n==== CRC-BERECHNUNG ====")

        if validate:
            data_errors, _ = self.validate_binary_string(data, "Datenbits")
            poly_errors, _ = self.validate_generator_polynomial(generator_poly, "Generatorpolynom")

            if data_errors or poly_errors:
                print("❌ CRC-BERECHNUNG ABGEBROCHEN:")
                for error in data_errors + poly_errors:
                    print("   " + error)
                return None, None

        clean_data = data.replace(" ", "").replace("'", "")
        clean_poly = generator_poly.replace(" ", "").replace("'", "")

        data_vec = self.binary_to_vector(clean_data)
        poly_vec = self.binary_to_vector(clean_poly)

        print("Datenbits:        " + clean_data)
        print("Generatorpolynom: " + clean_poly)

        degree = len(poly_vec) - 1
        print("Polynom-Grad:     " + str(degree))
        print("Kontrollstellen:  " + str(degree))

        extended_data = data_vec[:]
        for i in range(degree):
            extended_data.append(0)

        print("Erweiterte Daten: " + self.vector_to_binary(extended_data))

        quotient, remainder = self.polynomial_division_gf2(extended_data, poly_vec, validate=False)

        while len(remainder) < degree:
            remainder = [0] + remainder

        crc_codeword = data_vec + remainder
        print("\nCRC-Codewort: " + self.vector_to_binary(crc_codeword))
        print("  Datenteil:   " + clean_data)
        print("  CRC-Teil:    " + self.vector_to_binary(remainder))

        return crc_codeword, remainder

    def run(self):
        """Führt die CRC-Berechnung durch"""
        try:
            print("\n=== CRC-BERECHNUNG ===")

            while True:
                data = input("Datenbits: ").strip()
                errors, warnings = self.validate_binary_string(data, "Datenbits")
                if not errors:
                    break
                for error in errors:
                    print("❌ " + error)

            while True:
                generator = input("Generatorpolynom: ").strip()
                errors, warnings = self.validate_generator_polynomial(generator)
                if not errors:
                    break
                for error in errors:
                    print("❌ " + error)

            result = self.crc_calculation(data, generator, validate=True)
            codeword = result[0] if result else None
            remainder = result[1] if result else None

            if codeword:
                print("\n==== ERGEBNIS ====")
                print("Original-Daten:  " + data)
                print("CRC-Codewort:    " + self.vector_to_binary(codeword))
                print("CRC-Prüfbits:    " + self.vector_to_binary(remainder))

        except Exception as e:
            print("❌ Fehler: " + str(e))

        input("\nDrücke Enter zum Fortfahren...")


class CRCCheckTool(BaseChannelCodingTool):
    """Tool zur CRC-Prüfung"""

    def polynomial_division_gf2(self, dividend, divisor, validate=True):
        """Polynomdivision in GF(2) - vereinfachte Version für CRC-Check"""
        if isinstance(dividend, str):
            dividend_str = dividend.replace(" ", "").replace("'", "")
            dividend = self.binary_to_vector(dividend_str)
        else:
            dividend_str = self.vector_to_binary(dividend)

        if isinstance(divisor, str):
            divisor_str = divisor.replace(" ", "").replace("'", "")
            divisor = self.binary_to_vector(divisor_str)
        else:
            divisor_str = self.vector_to_binary(divisor)

        while len(dividend) > 1 and dividend[0] == 0:
            dividend = dividend[1:]
        while len(divisor) > 1 and divisor[0] == 0:
            divisor = divisor[1:]

        if len(dividend) < len(divisor):
            return [0], dividend

        quotient = []
        remainder = dividend[:]

        while len(remainder) >= len(divisor):
            has_ones = False
            for bit in remainder:
                if bit == 1:
                    has_ones = True
                    break
            if not has_ones:
                break

            while len(remainder) > 1 and remainder[0] == 0:
                remainder = remainder[1:]

            if len(remainder) < len(divisor):
                break

            quotient.append(1)

            for i in range(len(divisor)):
                if i < len(remainder):
                    remainder[i] = (remainder[i] + divisor[i]) % 2

            if remainder and remainder[0] == 0:
                remainder = remainder[1:]

        if not quotient:
            quotient = [0]
        if not remainder:
            remainder = [0]

        return quotient, remainder

    def crc_check(self, received_word, generator_poly, validate=True):
        """CRC-Prüfung eines empfangenen Wortes"""
        print("\n==== CRC-PRÜFUNG ====")

        if validate:
            word_errors, _ = self.validate_binary_string(received_word, "Empfangenes Wort")
            poly_errors, _ = self.validate_generator_polynomial(generator_poly, "Generatorpolynom")

            if word_errors or poly_errors:
                print("❌ CRC-PRÜFUNG ABGEBROCHEN:")
                for error in word_errors + poly_errors:
                    print("   " + error)
                return None

        if isinstance(received_word, str):
            clean_word = received_word.replace(" ", "").replace("'", "")
            received_vec = self.binary_to_vector(clean_word)
        else:
            received_vec = received_word
            clean_word = self.vector_to_binary(received_vec)

        if isinstance(generator_poly, str):
            clean_poly = generator_poly.replace(" ", "").replace("'", "")
            poly_vec = self.binary_to_vector(clean_poly)
        else:
            poly_vec = generator_poly
            clean_poly = self.vector_to_binary(poly_vec)

        print("Empfangenes Wort: " + clean_word)
        print("Generatorpolynom: " + clean_poly)

        quotient, remainder = self.polynomial_division_gf2(received_vec, poly_vec, validate=False)

        all_zero = True
        for bit in remainder:
            if bit != 0:
                all_zero = False
                break

        if all_zero:
            print("✅ Rest = 0 → Kein Fehler erkannt")
            return True
        else:
            remainder_str = self.vector_to_binary(remainder)
            print("❌ Rest = " + remainder_str + " ≠ 0 → Fehler erkannt")
            return False

    def run(self):
        """Führt die CRC-Prüfung durch"""
        try:
            print("\n=== CRC-PRÜFUNG ===")

            while True:
                received = input("Empfangenes Wort: ").strip()
                errors, warnings = self.validate_binary_string(received, "Empfangenes Wort")
                if not errors:
                    break
                for error in errors:
                    print("❌ " + error)

            while True:
                generator = input("Generatorpolynom: ").strip()
                errors, warnings = self.validate_generator_polynomial(generator)
                if not errors:
                    break
                for error in errors:
                    print("❌ " + error)

            is_valid = self.crc_check(received, generator, validate=True)

            if is_valid is not None:
                print("\n==== ERGEBNIS ====")
                print("Empfangenes Wort: " + received)
                if is_valid:
                    print("Status: ✅ GÜLTIG")
                else:
                    print("Status: ❌ FEHLERHAFT")

        except Exception as e:
            print("❌ Fehler: " + str(e))

        input("\nDrücke Enter zum Fortfahren...")


class PolynomialDivisionTool(BaseChannelCodingTool):
    """Tool für Polynomdivision in GF(2)"""

    def polynomial_division_gf2(self, dividend, divisor, validate=True):
        """Polynomdivision in GF(2)"""
        print("\n==== POLYNOMDIVISION IN GF(2) ====")

        if isinstance(dividend, str):
            dividend_str = dividend.replace(" ", "").replace("'", "")
            dividend = self.binary_to_vector(dividend_str)
        else:
            dividend_str = self.vector_to_binary(dividend)

        if isinstance(divisor, str):
            divisor_str = divisor.replace(" ", "").replace("'", "")
            divisor = self.binary_to_vector(divisor_str)
        else:
            divisor_str = self.vector_to_binary(divisor)

        print("Dividend:  " + dividend_str)
        print("Divisor:   " + divisor_str)

        while len(dividend) > 1 and dividend[0] == 0:
            dividend = dividend[1:]
        while len(divisor) > 1 and divisor[0] == 0:
            divisor = divisor[1:]

        if len(dividend) < len(divisor):
            print("\nSpezialfall: Dividend-Grad < Divisor-Grad")
            print("Quotient: 0")
            print("Rest:     " + self.vector_to_binary(dividend))
            return [0], dividend

        quotient = []
        remainder = dividend[:]

        print("\nDivisions-Schritte:")
        step = 1

        while len(remainder) >= len(divisor):
            has_ones = False
            for bit in remainder:
                if bit == 1:
                    has_ones = True
                    break
            if not has_ones:
                break

            while len(remainder) > 1 and remainder[0] == 0:
                remainder = remainder[1:]

            if len(remainder) < len(divisor):
                break

            quotient.append(1)

            print("Schritt " + str(step) + ":")
            print("  " + self.vector_to_binary(remainder))

            for i in range(len(divisor)):
                if i < len(remainder):
                    remainder[i] = (remainder[i] + divisor[i]) % 2

            print("  " + self.vector_to_binary(divisor))
            print("  " + "-" * len(dividend_str))
            print("  " + self.vector_to_binary(remainder))
            print()

            if remainder and remainder[0] == 0:
                remainder = remainder[1:]

            step += 1

        if not quotient:
            quotient = [0]
        if not remainder:
            remainder = [0]

        quotient_str = self.vector_to_binary(quotient)
        remainder_str = self.vector_to_binary(remainder)

        print("Ergebnis:")
        print("  Quotient: " + quotient_str)
        print("  Rest:     " + remainder_str)

        return quotient, remainder

    def run(self):
        """Führt die Polynomdivision durch"""
        try:
            print("\n=== POLYNOMDIVISION IN GF(2) ===")

            while True:
                dividend = input("Dividend: ").strip()
                errors, _ = self.validate_binary_string(dividend, "Dividend")
                if not errors:
                    break
                for error in errors:
                    print("❌ " + error)

            while True:
                divisor = input("Divisor: ").strip()
                errors, _ = self.validate_binary_string(divisor, "Divisor", min_length=2)
                if not errors:
                    break
                for error in errors:
                    print("❌ " + error)

            quotient, remainder = self.polynomial_division_gf2(dividend, divisor, validate=True)

        except Exception as e:
            print("❌ Fehler: " + str(e))

        input("\nDrücke Enter zum Fortfahren...")


import math


class BaseChannelCodingTool:
    """Basisklasse für Kanalcodierungs-Tools (simuliert für Kontext)."""

    def __init__(self):
        pass

    def validate_generator_polynomial(self, generator_poly_str):
        """
        Validiert das Generatorpolynom.
        Gibt eine Liste von Fehlern und Warnungen zurück.
        """
        errors = []
        warnings = []
        if not generator_poly_str:
            errors.append("Generatorpolynom darf nicht leer sein.")
            return errors, warnings

        if not all(c in '01' for c in generator_poly_str):
            errors.append("Generatorpolynom darf nur '0' und '1' enthalten.")

        if generator_poly_str.startswith('0') and len(generator_poly_str) > 1:
            warnings.append("Generatorpolynom beginnt mit '0'. Dies ist unüblich.")

        if len(generator_poly_str) < 2:
            errors.append("Generatorpolynom muss mindestens Grad 1 haben (z.B. '11').")

        return errors, warnings


class CyclicCodeAnalysisTool(BaseChannelCodingTool):
    """Tool für zyklische Code Analyse - Implementierung nach Übung 11"""

    def __init__(self):
        super().__init__()

    def polynomial_division_gf2(self, dividend_str, divisor_str):
        """
        Führt eine Polynomdivision in GF(2) durch.
        Beide Eingaben sind Binärstrings (MSB zuerst).
        Gibt (Quotient, Rest) als Binärstrings zurück.
        Diese Methode implementiert das Verfahren der schrittweisen XOR-Operationen,
        analog zur "schnellen Mehrfachaddition" bzw. Standard-Polynomdivision für Syndrome.
        """

        dividend = [int(bit) for bit in dividend_str]
        divisor = [int(bit) for bit in divisor_str]

        # Entferne führende Nullen vom Divisor, falls vorhanden (sollte nicht der Fall sein für g(x))
        while len(divisor) > 1 and divisor[0] == 0:
            divisor.pop(0)

        if not divisor or all(bit == 0 for bit in divisor):
            raise ValueError("Divisor darf nicht Null sein.")

        if len(dividend) < len(divisor):
            return "0", "".join(map(str, dividend))

        register = list(dividend)
        quotient = []

        # Anfängliche Ausrichtung und führende Nullen im Quotienten
        lead_zeros = 0
        while register and register[0] == 0 and len(register) >= len(divisor):
            quotient.append(0)
            register.pop(0)
            if not register:  # Fall: Dividend war komplett 0
                break

        # Haupt-Divisionsschleife
        # Solange der Grad des Registers >= Grad des Divisors ist
        while len(register) >= len(divisor):
            if register[0] == 1:  # Wenn das führende Bit 1 ist, XOR durchführen
                quotient.append(1)
                for i in range(len(divisor)):
                    register[i] ^= divisor[i]
            else:  # Wenn das führende Bit 0 ist, einfach shiften
                quotient.append(0)

            # Register shiften (führende Null entfernen)
            register.pop(0)

            # Zusätzliche Nullen im Quotienten für die verbleibenden Bits des Dividenden,
            # wenn das Register kleiner als der Divisor wird, bevor alle Bits verarbeitet wurden.
            if len(register) < len(divisor) and len(register) < (len(dividend_str) - len(quotient)):
                quotient.extend([0] * ((len(dividend_str) - len(quotient)) - len(register)))

        # Der Rest ist, was im Register übrig bleibt
        remainder_str = "".join(map(str, register))
        # Quotient formatieren
        quotient_str = "".join(map(str, quotient)) if quotient else "0"

        # Sicherstellen, dass der Rest die korrekte Länge hat (Grad < Grad des Divisors)
        # Normalerweise sollte der Rest kürzer sein als der Divisor.
        # Für Syndrome ist die Länge des Rests = Grad des Generatorpolynoms

        return quotient_str, remainder_str

    def create_parity_matrix_from_generator(self, generator_poly_str, code_length_n=None):
        """
        Erstellt die Prüfmatrix (H) für einen zyklischen Code, basierend auf dem Generatorpolynom g(x).
        Die Methode folgt den Prinzipien aus Übung 11, Aufgaben 5.2 und 5.3:
        1. Für jede Fehlerposition i wird ein Fehlervektor e_i(x) (Polynom x^i oder entsprechendes Bitmuster) erstellt.
        2. Das Syndrom s_i(x) für diesen Fehler wird durch Polynomdivision e_i(x) mod g(x) berechnet[cite: 1585].
           Der Rest dieser Division ist das Syndrom.
        3. Die Koeffizienten des Syndroms s_i(x) bilden die i-te Spalte der Prüfmatrix H[cite: 1586].
        Die Matrix wird live berechnet und nicht aus einem Speicher geladen.
        """
        print("\n==== BERECHNUNG DER PRÜFMATRIX H (ZYKLISCHER CODE) ====")
        print("Methode nach Übung 11, Aufgabe 5.2 & 5.3: Syndrome durch Polynomdivision")

        errors, warnings = self.validate_generator_polynomial(generator_poly_str)
        if errors:
            for error in errors: print(f"❌ FEHLER: {error}")
            return None
        for warning in warnings: print(f"⚠️ WARNUNG: {warning}")

        g_coeffs = [int(b) for b in generator_poly_str]

        # Grad des Generatorpolynoms k (Anzahl der Kontrollstellen)
        # g(x) = g_k * x^k + ... + g_1 * x^1 + g_0 * x^0. g_k ist immer 1.
        # Länge von g_coeffs ist k+1. Grad k ist len(g_coeffs) - 1.
        num_control_bits_k = len(g_coeffs) - 1
        print(f"Generatorpolynom g(x): {generator_poly_str}")
        print(f"Grad des Generatorpolynoms (Anzahl Kontrollstellen): k = {num_control_bits_k}")

        # Bestimme Codelänge n
        # Für einen (zyklischen) Hamming-Code, erzeugt von einem primitiven Polynom vom Grad k,
        # ist n = 2^k - 1.
        if code_length_n is None:
            # Annahme für Hamming-Codes wenn n nicht spezifiziert
            if num_control_bits_k > 0:  # Verhindert Endlosschleife oder Fehler bei k=0
                n = (2 ** num_control_bits_k) - 1
            else:  # Sollte durch Validierung abgefangen werden
                print("❌ FEHLER: Grad des Generatorpolynoms muss > 0 sein.")
                return None
            print(f"Codelänge (angenommen für Hamming-Code): n = 2^k - 1 = {n}")
        else:
            n = code_length_n
            if n <= num_control_bits_k:
                print(f"❌ FEHLER: Codelänge n ({n}) muss größer sein als Grad k ({num_control_bits_k}).")
                return None
            print(f"Codelänge (gegeben): n = {n}")

        num_message_bits_m = n - num_control_bits_k
        print(f"Anzahl Nachrichtenstellen: m = n - k = {num_message_bits_m}")

        if n <= 0 or num_message_bits_m <= 0:
            print(f"❌ FEHLER: Ungültige Code-Parameter (n={n}, m={num_message_bits_m}, k={num_control_bits_k}).")
            return None

        # Initialisiere Prüfmatrix H (k Zeilen, n Spalten)
        H = [[0 for _ in range(n)] for _ in range(num_control_bits_k)]

        print("\n--- Berechnung der Spalten der Prüfmatrix H durch Syndrome ---")
        # Die Spalten von H sind die Syndrome der Fehlervektoren x^i (für i von n-1 bis 0)
        # Fehlervektor x^i bedeutet eine '1' an der (i+1)-ten Bitposition von rechts (LSB ist x^0)
        # oder (n-i)-ten Position von links (MSB ist x^(n-1))
        for j in range(n):  # j repräsentiert die Fehlerposition von links (0 bis n-1)
            # Dies entspricht dem Fehlerpolynom e(x) = x^(n-1-j)
            error_poly_str = ['0'] * n
            error_poly_str[j] = '1'  # Fehler an der j-ten Stelle (0-indexed von links)
            error_poly_str = "".join(error_poly_str)

            # Das Syndrom ist der Rest der Division e(x) / g(x)
            _, syndrome_str = self.polynomial_division_gf2(error_poly_str, generator_poly_str)

            # Sicherstellen, dass das Syndrom k_check_bits lang ist (mit führenden Nullen auffüllen)
            syndrome_str = syndrome_str.zfill(num_control_bits_k)

            if len(syndrome_str) > num_control_bits_k:  # Sollte nicht passieren wenn division korrekt ist
                syndrome_str = syndrome_str[-num_control_bits_k:]

            print(
                f"  Fehler an Position x_{j + 1} (Polynom x^{n - 1 - j}): e_{j + 1}(x) = {error_poly_str}, Syndrom s_{j + 1}(x) = {syndrome_str}")

            # Das Syndrom (als k-Bit Vektor) ist die (j+1)-te Spalte von H
            for i in range(num_control_bits_k):
                H[i][j] = int(syndrome_str[i])

        print("\n--- Resultierende Prüfmatrix H ---")
        header = "    " + " ".join([f"x{i + 1:<2}" for i in range(n)])
        print(header)
        print("    " + "-" * (len(header) - 4))
        for i, row in enumerate(H):
            row_str = "h{:<2}: ".format(i + 1) + " ".join([f"{bit:<2}" for bit in row])
            print(row_str)

        # Formatiere als Prüfgleichungen
        print("\nPrüfgleichungen (s_i = sum(H_ij * x_j) = 0):")
        for i in range(num_control_bits_k):
            terms = []
            for j in range(n):
                if H[i][j] == 1:
                    terms.append(f"x{j + 1}")
            if terms:
                equation = " + ".join(terms) + " = 0"
                print(f"s{i + 1}: {equation}")
            else:
                print(f"s{i + 1}: 0 = 0")  # Sollte nicht vorkommen für sinnvolle H

        self._verify_H_matrix_properties(H, generator_poly_str, n, num_control_bits_k)

        return {
            'parity_matrix': H,
            'code_length_n': n,
            'message_bits_m': num_message_bits_m,
            'control_bits_k': num_control_bits_k,
            'generator_polynomial_str': generator_poly_str
        }

    def _verify_H_matrix_properties(self, H, generator_str, n, k_ctrl_bits):
        """Überprüft allgemeine Eigenschaften der generierten H-Matrix."""
        print("\n--- Verifikation der H-Matrix Eigenschaften ---")

        if not H or not H[0] or k_ctrl_bits <= 0:  # Zusätzliche Prüfung für k_ctrl_bits
            print("❌ Leere oder ungültige H-Matrix / Kontrollbit-Anzahl zur Verifikation übergeben.")
            return

        # Prüfe auf Nullspalten
        zero_columns_found = 0
        # Stelle sicher, dass n der tatsächlichen Spaltenanzahl von H entspricht
        actual_n = len(H[0]) if H else 0
        if actual_n != n:
            print(
                f"⚠️ Warnung: Erwartete Spaltenanzahl n={n} stimmt nicht mit tatsächlicher Spaltenanzahl {actual_n} der Matrix H überein.")
            # Fahre fort mit actual_n für die Prüfungen, aber dies deutet auf ein Problem hin

        # Verwende die tatsächliche Anzahl der Spalten in der generierten Matrix H für die Schleife
        for j in range(actual_n):
            # Stelle sicher, dass k_ctrl_bits der tatsächlichen Zeilenanzahl von H entspricht
            actual_k = len(H)
            if actual_k != k_ctrl_bits:
                print(
                    f"⚠️ Warnung: Erwartete Zeilenanzahl k_ctrl_bits={k_ctrl_bits} stimmt nicht mit tatsächlicher Zeilenanzahl {actual_k} der Matrix H überein.")
                # Fahre fort mit actual_k für die Prüfungen

            is_zero_column = all(H[i][j] == 0 for i in range(actual_k))
            if is_zero_column:
                zero_columns_found += 1

        if zero_columns_found == 0:
            print("✅ Korrekt: Keine Nullspalten in H.")
        else:
            print(
                f"❌ Warnung: {zero_columns_found} Nullspalten in H gefunden. (Ungültig für Hamming-Codes und fehlererkennende Codes)")

        # Prüfe auf eindeutige Spalten (wichtig für Hamming-Codes zur 1-Bit-Fehlerkorrektur)
        columns_as_tuples = []
        if actual_n > 0 and len(H) == k_ctrl_bits:  # Nutze actual_k (len(H))
            for j in range(actual_n):  # Nutze actual_n
                col = tuple(H[i][j] for i in range(k_ctrl_bits))  # Nutze k_ctrl_bits (sollte len(H) sein)
                columns_as_tuples.append(col)

            if len(set(columns_as_tuples)) == actual_n:  # Vergleiche mit actual_n
                print("✅ Korrekt: Alle Spalten in H sind eindeutig.")
            else:
                column_counts = {}
                for col_tuple in columns_as_tuples:
                    column_counts[col_tuple] = column_counts.get(col_tuple, 0) + 1

                duplicate_columns = {col: count for col, count in column_counts.items() if count > 1}
                if duplicate_columns:
                    print(
                        f"❌ Warnung: Es gibt {len(duplicate_columns)} verschiedene Spaltenmuster, die mehrfach vorkommen:")
                    for col_tuple, count in duplicate_columns.items():
                        col_str = "".join(map(str, col_tuple))
                        print(f"    - Spaltenmuster ({col_str}) kommt {count}-mal vor.")
                else:
                    print("❌ Warnung: Es gibt doppelte Spalten in H, aber Details konnten nicht ermittelt werden.")
        elif k_ctrl_bits > 0:  # Nur wenn k_ctrl_bits > 0 ist, sonst ist H leer und die obige Bedingung nicht erfüllt
            print("ℹ️ Prüfung auf eindeutige Spalten übersprungen aufgrund von Matrix-Dimensionen oder Parametern.")

    def run(self):
        """Führt die zyklische Code Analyse durch."""
        try:
            print("\n=== ZYKLISCHE CODE ANALYSE NACH ÜBUNG 11 ===")
            print("Die Prüfmatrix H wird live berechnet, indem Syndrome für Einzelfehlerpositionen")
            print("mittels Polynomdivision (e_i(x) mod g(x)) bestimmt werden[cite: 1585, 1586].")
            print("\nBeispiele für Generatorpolynome g(x):")
            print("  '1011'    (für x³ + x + 1 -> (7,4) Hamming Code)")
            print("  '1101'    (für x³ + x² + 1)")
            print("  '10011'   (für x⁴ + x + 1 -> (15,11) Hamming Code)")

            while True:
                generator_poly_input = input("\nGeneratorpolynom g(x) als Binärstring eingeben (z.B. 1011): ").strip()
                if generator_poly_input:
                    break
                print("❌ Eingabe darf nicht leer sein.")


            code_length_input_str = input("Spezifische totale Codelänge m+k eingeben? (Standard: 2^k-1 für Hamming): ").strip()
            code_length_n_arg = None
            if code_length_input_str:
                try:
                    code_length_n_arg = int(code_length_input_str)
                    if code_length_n_arg <= 0:
                        print("⚠️ Ungültige Codelänge, Standard wird verwendet.")
                        code_length_n_arg = None
                except ValueError:
                    print("⚠️ Ungültige Eingabe für Codelänge, Standard wird verwendet.")

            result = self.create_parity_matrix_from_generator(generator_poly_input, code_length_n=code_length_n_arg)

            if result:
                pass

        except KeyboardInterrupt:
            print("\n❌ Analyse abgebrochen.")
        except Exception as e:
            print(f"❌ Ein unerwarteter Fehler ist aufgetreten: {e}")

        input("\nDrücken Sie Enter zum Beenden...")



class SystematicEncodingTool(BaseChannelCodingTool):
    """Tool für systematische Codierung"""

    def polynomial_division_gf2(self, dividend, divisor, validate=True):
        """Vereinfachte Polynomdivision für systematische Codierung"""
        if isinstance(dividend, str):
            dividend_str = dividend.replace(" ", "").replace("'", "")
            dividend = self.binary_to_vector(dividend_str)

        if isinstance(divisor, str):
            divisor_str = divisor.replace(" ", "").replace("'", "")
            divisor = self.binary_to_vector(divisor_str)

        while len(dividend) > 1 and dividend[0] == 0:
            dividend = dividend[1:]
        while len(divisor) > 1 and divisor[0] == 0:
            divisor = divisor[1:]

        if len(dividend) < len(divisor):
            return [0], dividend

        quotient = []
        remainder = dividend[:]

        while len(remainder) >= len(divisor):
            has_ones = False
            for bit in remainder:
                if bit == 1:
                    has_ones = True
                    break
            if not has_ones:
                break

            while len(remainder) > 1 and remainder[0] == 0:
                remainder = remainder[1:]

            if len(remainder) < len(divisor):
                break

            quotient.append(1)

            for i in range(len(divisor)):
                if i < len(remainder):
                    remainder[i] = (remainder[i] + divisor[i]) % 2

            if remainder and remainder[0] == 0:
                remainder = remainder[1:]

        if not quotient:
            quotient = [0]
        if not remainder:
            remainder = [0]

        return quotient, remainder

    def systematic_encoding(self, message, generator_poly, validate=True):
        """Systematische Codierung"""
        print("\n==== SYSTEMATISCHE CODIERUNG ====")

        if validate:
            msg_errors, _ = self.validate_binary_string(message, "Nachrichtenbits")
            poly_errors, _ = self.validate_generator_polynomial(generator_poly, "Generatorpolynom")

            if msg_errors or poly_errors:
                print("❌ SYSTEMATISCHE CODIERUNG ABGEBROCHEN:")
                for error in msg_errors + poly_errors:
                    print("   " + error)
                return None

        clean_message = message.replace(" ", "").replace("'", "")
        clean_poly = generator_poly.replace(" ", "").replace("'", "")

        message_vec = self.binary_to_vector(clean_message)
        poly_vec = self.binary_to_vector(clean_poly)

        print("Nachricht:        " + clean_message)
        print("Generatorpolynom: " + clean_poly)

        degree = len(poly_vec) - 1
        print("Polynom-Grad:     " + str(degree))

        shifted_message = message_vec[:]
        for i in range(degree):
            shifted_message.append(0)

        print("Verschobene Nachricht: " + self.vector_to_binary(shifted_message))

        quotient, remainder = self.polynomial_division_gf2(shifted_message, poly_vec, validate=False)

        while len(remainder) < degree:
            remainder = [0] + remainder

        codeword = message_vec + remainder
        print("\nSystematisches Codewort: " + self.vector_to_binary(codeword))
        print("  Nachrichtenteil: " + clean_message)
        print("  Kontrollbits:    " + self.vector_to_binary(remainder))

        return codeword

    def run(self):
        """Führt die systematische Codierung durch"""
        try:
            print("\n=== SYSTEMATISCHE CODIERUNG ===")

            while True:
                message = input("Nachrichtenbits: ").strip()
                errors, warnings = self.validate_binary_string(message, "Nachrichtenbits")
                if not errors:
                    break
                for error in errors:
                    print("❌ " + error)

            while True:
                generator = input("Generatorpolynom: ").strip()
                errors, warnings = self.validate_generator_polynomial(generator)
                if not errors:
                    break
                for error in errors:
                    print("❌ " + error)

            codeword = self.systematic_encoding(message, generator, validate=True)

            if codeword:
                print("\n=== VERIFIKATION ===")
                crc_check_tool = CRCCheckTool()
                crc_check_tool.crc_check(codeword, generator, validate=False)

        except Exception as e:
            print("❌ Fehler: " + str(e))

        input("\nDrücke Enter zum Fortfahren...")


class ShiftRegisterTool(BaseChannelCodingTool):
    """Tool für Schieberegister-Simulation"""

    def shift_register_simulation(self, generator_poly, input_data, validate=True):
        """Simulation eines rückgekoppelten Schieberegisters"""
        print("\n==== SCHIEBEREGISTER-SIMULATION ====")

        if validate:
            data_errors, _ = self.validate_binary_string(input_data, "Eingangsdaten")
            poly_errors, _ = self.validate_generator_polynomial(generator_poly, "Generatorpolynom")

            if data_errors or poly_errors:
                print("❌ SCHIEBEREGISTER-SIMULATION ABGEBROCHEN:")
                for error in data_errors + poly_errors:
                    print("   " + error)
                return None, None

        clean_poly = generator_poly.replace(" ", "").replace("'", "")
        clean_data = input_data.replace(" ", "").replace("'", "")

        poly_vec = self.binary_to_vector(clean_poly)
        data_vec = self.binary_to_vector(clean_data)

        print("Generatorpolynom: " + clean_poly)
        print("Eingangsdaten:    " + clean_data)

        degree = len(poly_vec) - 1

        feedback_positions = []
        for i in range(1, len(poly_vec)):
            if poly_vec[i] == 1:
                pos = len(poly_vec) - 1 - i
                feedback_positions.append(pos)

        print("Rückkopplungspositionen: " + str(feedback_positions))

        register = []
        for i in range(degree):
            register.append(0)

        output = []

        extended_input = data_vec[:]
        for i in range(degree):
            extended_input.append(0)

        print("\nSchieberegister-Simulation:")
        print("Schritt | Eingabe | Register  | Rückkopplung | Ausgabe")
        print("--------|---------|-----------|--------------|--------")

        for step in range(len(extended_input)):
            input_bit = extended_input[step]

            feedback = 0
            for pos in feedback_positions:
                if pos < len(register):
                    feedback = (feedback + register[pos]) % 2

            new_bit = (input_bit + feedback) % 2

            output_bit = register[-1] if register else 0
            output.append(output_bit)

            new_register = [new_bit]
            for i in range(len(register) - 1):
                new_register.append(register[i])
            register = new_register

            register_str = self.vector_to_binary(register)
            print("   " + str(step).rjust(2) + "   |    " + str(input_bit) + "    |  " +
                  register_str + "  |      " + str(feedback) + "       |    " + str(output_bit))

        remainder = register[:]

        print("\nAusgabesequenz: " + self.vector_to_binary(output))
        print("Register-Rest:  " + self.vector_to_binary(remainder))

        return output, remainder

    def run(self):
        """Führt die Schieberegister-Simulation durch"""
        try:
            print("\n=== SCHIEBEREGISTER-SIMULATION ===")

            while True:
                generator = input("Generatorpolynom: ").strip()
                errors, warnings = self.validate_generator_polynomial(generator)
                if not errors:
                    break
                for error in errors:
                    print("❌ " + error)

            while True:
                data = input("Eingangsdaten: ").strip()
                errors, warnings = self.validate_binary_string(data, "Eingangsdaten")
                if not errors:
                    break
                for error in errors:
                    print("❌ " + error)

            output, remainder = self.shift_register_simulation(generator, data, validate=True)

        except Exception as e:
            print("❌ Fehler: " + str(e))

        input("\nDrücke Enter zum Fortfahren...")


class ComprehensiveCodeAnalysisTool(BaseChannelCodingTool):
    """Tool für vollständige Code-Analyse"""

    def run(self):
        """Führt eine vollständige Code-Analyse durch"""
        try:
            print("\n=== VOLLSTÄNDIGE CODE-ANALYSE ===")
            print("1. Hamming-Code")
            print("2. CRC-Code")
            print("3. Allgemeiner Blockcode")

            code_choice = input("Code-Typ wählen: ")

            if code_choice == "1":
                print("\nPrüfgleichungen eingeben:")
                n_eq = self.safe_int_input("Anzahl Prüfgleichungen: ", min_val=1, max_val=10)
                print("\nBeispieleingabe: 1 2 3 4 6 7 8 ")

                equations = []
                for i in range(n_eq):
                    while True:
                        try:
                            pos_str = input("Prüfgleichung " + str(i + 1) + " (Positionen): ")
                            positions = []
                            for x in pos_str.split():
                                positions.append(int(x))
                            equations.append(positions)
                            break
                        except:
                            print("❌ Ungültige Eingabe.")

                # Verwende ParityMatrixTool
                matrix_tool = ParityMatrixTool()
                H = matrix_tool.create_parity_check_matrix(equations, validate=True)

                if H:
                    print("\nHamming-Code Eigenschaften:")
                    print("  Hamming-Distanz: h = 3")
                    print("  Korrigierbare Fehler: e = 1")
                    print("  Erkennbare Fehler: e* = 2")

            elif code_choice == "2":
                while True:
                    generator = input("Generatorpolynom: ").strip()
                    errors, warnings = self.validate_generator_polynomial(generator)
                    if not errors:
                        break
                    for error in errors:
                        print("❌ " + error)

                # Code-Eigenschaften analysieren
                analysis_tool = CyclicCodeAnalysisTool()
                analysis = analysis_tool.cyclic_code_analysis(generator, validate=True)

                data_input = input("Datenbits (Enter für nur Analyse): ").strip()
                if data_input:
                    crc_tool = CRCCalculationTool()
                    result = crc_tool.crc_calculation(data_input, generator, validate=True)

                    if result:
                        shift_tool = ShiftRegisterTool()
                        output, reg_remainder = shift_tool.shift_register_simulation(
                            generator, data_input, validate=True)

            elif code_choice == "3":
                n_cw = self.safe_int_input("Anzahl Codewörter: ", min_val=2, max_val=20)

                codewords = []
                for i in range(n_cw):
                    cw = input("Codewort " + str(i + 1) + ": ").strip()
                    codewords.append(cw)

                # Analysiere mit HammingDistanceTool
                hamming_tool = HammingDistanceTool()
                result = hamming_tool.minimum_hamming_distance(codewords, validate=True)

                if result:
                    n = len(codewords[0].replace(" ", "").replace("'", "")) if codewords else None
                    k_input = input("Anzahl Nachrichtenbits k (Enter für unbekannt): ").strip()
                    k = int(k_input) if k_input else None

                    if n and k:
                        print("\nCode-Parameter:")
                        print("  Codelänge: n = " + str(n))
                        print("  Nachrichtenbits: k = " + str(k))
                        print("  Kontrollbits: n-k = " + str(n - k))
                        print("  Coderate: R = k/n = " + str(k) + "/" + str(n) + " = " + str(round(k / n, 3)))

                        singleton_bound = n - k + 1
                        print("  Singleton-Bound: d ≤ n-k+1 = " + str(singleton_bound))

                        if result['min_distance'] == singleton_bound:
                            print("  ✅ Code erfüllt Singleton-Bound mit Gleichheit (MDS-Code)")
                        elif result['min_distance'] < singleton_bound:
                            print("  ✅ Code erfüllt Singleton-Bound")
                        else:
                            print("  ❌ Code verletzt Singleton-Bound (Fehler in Berechnung?)")
            else:
                print("❌ Ungültige Auswahl!")

        except Exception as e:
            print("❌ Fehler: " + str(e))

        input("\nDrücke Enter zum Fortfahren...")


class CodePropertiesAnalysisTool(BaseChannelCodingTool):
    """Tool für Code-Eigenschaften Analyse"""

    def code_properties_analysis(self, **kwargs):
        """Analysiert Eigenschaften eines Codes umfassend"""
        print("\n==== CODE-EIGENSCHAFTEN ANALYSE ====")

        results = {}
        validate = kwargs.get('validate', True)

        # Hamming-Distanz Analysis
        codewords = kwargs.get('codewords')
        if codewords:
            print("1. HAMMING-DISTANZ ANALYSE:")
            hamming_tool = HammingDistanceTool()
            hamming_result = hamming_tool.minimum_hamming_distance(codewords, validate=validate)
            if hamming_result:
                results['hamming_analysis'] = hamming_result

                d = hamming_result['min_distance']
                print("\nCode-Klassifikation basierend auf d = " + str(d) + ":")

                if d == 1:
                    print("  → Keine Fehlerkorrektur (nur Informationsübertragung)")
                elif d == 2:
                    print("  → Single-Error-Detection (SED)")
                elif d == 3:
                    print("  → Single-Error-Correction (SEC)")
                elif d == 4:
                    print("  → Single-Error-Correction + Double-Error-Detection (SECDED)")
                else:
                    t = (d - 1) // 2
                    print("  → " + str(t) + "-Error-Correction Code")

        # Generator-Polynom Analyse
        generator_poly = kwargs.get('generator_poly')
        if generator_poly:
            print("2. GENERATOR-POLYNOM ANALYSE:")
            cyclic_tool = CyclicCodeAnalysisTool()
            poly_analysis = cyclic_tool.cyclic_code_analysis(generator_poly, validate=validate)
            results['polynomial_analysis'] = poly_analysis

        return results

    def run(self):
        """Führt die Code-Eigenschaften Analyse durch"""
        try:
            print("\n=== CODE-EIGENSCHAFTEN ANALYSIEREN ===")
            print("1. Codewörter analysieren")
            print("2. Generatorpolynom analysieren")
            print("3. Beides")

            choice = input("Auswahl: ").strip()

            codewords = None
            generator_poly = None

            if choice in ["1", "3"]:
                n_cw = self.safe_int_input("Anzahl Codewörter: ", min_val=2, max_val=20)
                codewords = []
                for i in range(n_cw):
                    cw = input("Codewort " + str(i + 1) + ": ").strip()
                    codewords.append(cw)

            if choice in ["2", "3"]:
                while True:
                    generator_poly = input("Generatorpolynom: ").strip()
                    errors, warnings = self.validate_generator_polynomial(generator_poly)
                    if not errors:
                        break
                    for error in errors:
                        print("❌ " + error)

            # Führe Analyse durch
            results = self.code_properties_analysis(
                codewords=codewords,
                generator_poly=generator_poly,
                validate=True
            )

            print("\n==== ANALYSE ABGESCHLOSSEN ====")
            if results:
                print("Ergebnisse wurden erfolgreich berechnet.")
            else:
                print("Keine Ergebnisse verfügbar.")

        except Exception as e:
            print("❌ Fehler: " + str(e))

        input("\nDrücke Enter zum Fortfahren...")


class CodeParametersAndBoundsTool(BaseChannelCodingTool):
    """
    Werkzeug zur Berechnung von Code-Parametern, Fehlererkennungs/-korrektur-
    Fähigkeiten und zur Prüfung auf Dichtgepacktheit (Perfekter Code).
    Nimmt Nachrichtenstellen, Kontrollstellen und Hammingdistanz als Eingabe.
    """

    def factorial(self, num):
        """Berechnet die Fakultät einer Zahl (für MicroPython)."""
        if num < 0:
            # Dieser Fall sollte durch Eingabevalidierung von e verhindert werden
            return 0  # Oder Fehler werfen
        if num == 0:
            return 1
        res = 1
        for i in range(1, num + 1):
            res *= i
        return res

    def combinations(self, n_items, k_items):
        """Berechnet den Binomialkoeffizienten C(n, k) (für MicroPython)."""
        if k_items < 0 or k_items > n_items:
            return 0
        if k_items == 0 or k_items == n_items:
            return 1
        if k_items > n_items // 2:  # Optimierung: C(n, k) == C(n, n-k)
            k_items = n_items - k_items

        res = 1
        for i in range(k_items):
            res = res * (n_items - i) // (i + 1)
        return res

    def run(self):
        """Führt die Berechnungen und Prüfungen durch."""
        print("\n=== CODE-PARAMETER, FEHLERKAPAZITÄT & DICHTGEPACKTHEIT PRÜFEN ===")
        try:
            k_info = self.safe_int_input("Anzahl Nachrichtenstellen (k bzw. m): ", min_val=1, max_val=100)
            k_control = self.safe_int_input("Anzahl Kontrollstellen (r bzw. Prüfstellen): ", min_val=1, max_val=100)
            h_dist = self.safe_int_input("Minimale Hamming-Distanz (h): ", min_val=1, max_val=(k_info + k_control))

            # 1. Codelänge n
            n_codelength = k_info + k_control
            print(f"\n--- Berechnete Code-Parameter ---")
            print(f"Codelänge (n = k_info + k_control): {n_codelength}")

            # 2. Anzahl gültige Codewörter
            num_valid_codewords = 2 ** k_info
            print(f"Anzahl gültige Codewörter (2^k_info): {int(num_valid_codewords)}")  # [cite: 264]

            # 3. Anzahl mögliche Codewörter
            num_possible_codewords = 2 ** n_codelength
            print(f"Anzahl mögliche Codewörter (2^n): {int(num_possible_codewords)}")  # [cite: 264]

            # 4. Sicher erkennbare Fehler e*
            e_star = h_dist - 1
            print(f"Sicher erkennbare Fehler (e* = h - 1): {e_star}")  # [cite: 264]

            # 5. Sicher korrigierbare Fehler e
            e_corr = (h_dist - 1) // 2

            print(f"Sicher korrigierbare Fehler (e = floor((h-1)/2)): {e_corr}")  # [cite: 264]

            # 6. Prüfung auf Dichtgepacktheit
            print(f"\n--- Prüfung auf Dichtgepacktheit (Perfekter Code) ---")
            if e_corr < 0:
                print(
                    "Hinweis: Mit e < 0 ist keine Fehlerkorrektur möglich, Prüfung auf Dichtgepacktheit nicht sinnvoll für e < 0.")
                is_perfect = False
            else:
                sum_combinations = 0
                print(
                    f"Berechnung der Summe der Binomialkoeffizienten S = Σ C(n, i) für i von 0 bis e_corr (e_corr={e_corr}):")
                for i in range(e_corr + 1):
                    comb = self.combinations(n_codelength, i)
                    print(f"  C({n_codelength}, {i}) = {comb}")
                    sum_combinations += comb
                print(f"S = {sum_combinations}")


                val_for_perfection = 2 ** (n_codelength - k_info)

                print(f"\nPrüfung der Hamming-Grenze:")
                print(
                    f"  Linke Seite (Anzahl Wörter in allen Kugeln): 2^k_info * S = {int(num_valid_codewords)} * {sum_combinations} = {int(num_valid_codewords * sum_combinations)}")
                print(f"  Rechte Seite (Gesamtzahl Wörter im Raum): 2^n = {int(num_possible_codewords)}")
                print(
                    f"  Vereinfachte Prüfung: S = {sum_combinations}, Sollwert für Perfektion (2^(n-k_info)): {val_for_perfection}")

                is_perfect = False
                # Toleranz für Fließkommavergleiche
                if isinstance(val_for_perfection, float):
                    is_perfect = abs(sum_combinations - val_for_perfection) < self.tolerance
                else:  # Sollte bei Potenzen von 2 ein int sein
                    is_perfect = (sum_combinations == val_for_perfection)

                if is_perfect:
                    print(f"\n✅ Ergebnis: Der Code ist DICHTGEPACKT (PERFEKT).")
                    print(f"   Die Bedingung 2^k_info * Σ C(n,i) = 2^n ist erfüllt.")
                else:
                    print(f"\n❌ Ergebnis: Der Code ist NICHT dichtgepackt.")
                    if (num_valid_codewords * sum_combinations) > num_possible_codewords:
                        print(
                            "   Die Kugelpackungsschranke ist verletzt (2^k_info * S > 2^n). Dies sollte für gültige Codes nicht passieren.")
                    else:
                        print("   Die Kugelpackungsschranke ist nicht mit Gleichheit erfüllt (2^k_info * S < 2^n).")

        except ValueError as ve:
            print(f"❌ Eingabefehler: {ve}")
        except Exception as e:
            print(f"❌ Ein unerwarteter Fehler ist aufgetreten: {e}")

        input("\nDrücke Enter zum Fortfahren...")  # Hinzugefügt
