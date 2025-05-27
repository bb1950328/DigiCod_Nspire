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


class CyclicCodeAnalysisTool(BaseChannelCodingTool):
    """Kompakte Tool für zyklische Code Analyse - optimiert für Taschenrechner"""

    def __init__(self):
        super().__init__()
        self.last_result = None

    def polynomial_division_gf2(self, dividend_str, divisor_str):
        """Polynomdivision in GF(2) - kompakte Version"""
        dividend = [int(bit) for bit in dividend_str]
        divisor = [int(bit) for bit in divisor_str]

        # Entferne führende Nullen vom Divisor
        while len(divisor) > 1 and divisor[0] == 0:
            divisor.pop(0)

        if not divisor or all(bit == 0 for bit in divisor):
            raise ValueError("Divisor = 0")

        if len(dividend) < len(divisor):
            return "0", "".join(map(str, dividend))

        register = list(dividend)
        quotient = []

        # Führende Nullen behandeln
        while register and register[0] == 0 and len(register) >= len(divisor):
            quotient.append(0)
            register.pop(0)
            if not register:
                break

        # Hauptdivision
        while len(register) >= len(divisor):
            if register[0] == 1:
                quotient.append(1)
                for i in range(len(divisor)):
                    register[i] = register[i] ^ divisor[i]  # XOR ohne ^= für MicroPython
            else:
                quotient.append(0)
            register.pop(0)

        remainder_str = "".join(map(str, register))
        quotient_str = "".join(map(str, quotient)) if quotient else "0"

        return quotient_str, remainder_str

    def create_parity_matrix_compact(self, generator_poly_str, code_length_n=None):
        """Erstellt Prüfmatrix - kompakte Version mit minimaler Ausgabe"""

        # Validierung
        errors, warnings = self.validate_generator_polynomial(generator_poly_str)
        if errors:
            print("FEHLER:", errors[0])
            return None

        g_coeffs = [int(b) for b in generator_poly_str]
        k = len(g_coeffs) - 1  # Kontrollstellen

        # Codelänge bestimmen
        if code_length_n is None:
            if k > 0:
                n = (2 ** k) - 1
            else:
                print("FEHLER: k muss > 0")
                return None
        else:
            n = code_length_n
            if n <= k:
                print("FEHLER: n muss > k")
                return None

        m = n - k  # Nachrichtenstellen

        # Kurze Zusammenfassung
        print("Code: ({},{}) k={} Hamming".format(n, m, k))

        # H-Matrix berechnen
        H = [[0 for _ in range(n)] for _ in range(k)]

        for j in range(n):
            error_poly = ['0'] * n
            error_poly[j] = '1'
            error_str = "".join(error_poly)

            _, syndrome_str = self.polynomial_division_gf2(error_str, generator_poly_str)
            syndrome_str = syndrome_str.zfill(k)

            if len(syndrome_str) > k:
                syndrome_str = syndrome_str[-k:]

            for i in range(k):
                H[i][j] = int(syndrome_str[i])

        # Validierung
        zero_cols = 0
        col_set = set()
        for j in range(n):
            col = tuple(H[i][j] for i in range(k))
            if all(bit == 0 for bit in col):
                zero_cols += 1
            col_set.add(col)

        is_valid = (zero_cols == 0) and (len(col_set) == n)
        status = "OK" if is_valid else "WARNUNG"
        print("Status: {}".format(status))

        if not is_valid:
            if zero_cols > 0:
                print("- {} Nullspalten".format(zero_cols))
            if len(col_set) != n:
                print("- Doppelte Spalten")

        return {
            'parity_matrix': H,
            'code_length_n': n,
            'message_bits_m': m,
            'control_bits_k': k,
            'generator_polynomial_str': generator_poly_str,
            'is_valid': is_valid,
            'zero_columns': zero_cols,
            'unique_columns': len(col_set)
        }

    def show_details_menu(self, result):
        """Zeigt Details-Menü"""
        if not result:
            return

        while True:
            print("\n--- DETAILS ---")
            print("1: H-Matrix")
            print("2: Pruefgleichungen")
            print("3: Eigenschaften")
            print("q: Zurueck")

            choice = input("Wahl: ").strip().lower()

            if choice == 'q':
                break
            elif choice == '1':
                self.show_h_matrix(result)
            elif choice == '2':
                self.show_parity_equations(result)
            elif choice == '3':
                self.show_properties(result)
            else:
                print("Ungueltig!")

            input("\nEnter...")

    def show_h_matrix(self, result):
        """Zeigt H-Matrix seitenweise"""
        H = result['parity_matrix']
        n = result['code_length_n']
        k = result['control_bits_k']

        print("\nH-Matrix ({}x{}):".format(k, n))

        # Zeige Matrix in Blöcken bei großen n
        cols_per_page = 8
        for start_col in range(0, n, cols_per_page):
            end_col = min(start_col + cols_per_page, n)

            # Header
            header = "   "
            for j in range(start_col, end_col):
                header += "x{:<2}".format(j + 1)
            print(header)

            # Zeilen
            for i in range(k):
                row = "h{}:".format(i + 1)
                for j in range(start_col, end_col):
                    row += " {} ".format(H[i][j])
                print(row)

            if end_col < n:
                input("\nNaechste Spalten...")

    def show_parity_equations(self, result):
        """Zeigt Prüfgleichungen"""
        H = result['parity_matrix']
        n = result['code_length_n']
        k = result['control_bits_k']

        print("\nPruefgleichungen:")
        for i in range(k):
            terms = []
            for j in range(n):
                if H[i][j] == 1:
                    terms.append("x{}".format(j + 1))

            if terms:
                equation = " + ".join(terms) + " = 0"
                print("s{}: {}".format(i + 1, equation))
            else:
                print("s{}: 0 = 0".format(i + 1))

    def show_properties(self, result):
        """Zeigt Code-Eigenschaften"""
        print("\nCode-Eigenschaften:")
        print("n = {} (Codelaenge)".format(result['code_length_n']))
        print("k = {} (Kontrollstellen)".format(result['control_bits_k']))
        print("m = {} (Nachrichtenstellen)".format(result['message_bits_m']))
        print("g(x) = {}".format(result['generator_polynomial_str']))

        print("\nMatrix-Eigenschaften:")
        print("Nullspalten: {}".format(result['zero_columns']))
        print("Eindeutige Spalten: {}/{}".format(result['unique_columns'], result['code_length_n']))
        print("Gueltig: {}".format("Ja" if result['is_valid'] else "Nein"))

    def run(self):
        """Hauptprogramm - kompakt mit Navigation"""
        try:
            print("=== ZYKLISCHE CODES ===")
            print("Beispiele g(x):")
            print("1011: x^3+x+1 (7,4)")
            print("10011: x^4+x+1 (15,11)")

            while True:
                print("\n--- EINGABE ---")
                gen_poly = input("g(x) binaer (q=exit): ").strip()

                if gen_poly.lower() == 'q':
                    break

                if not gen_poly:
                    print("Leer!")
                    continue

                # Optionale Codelänge
                n_input = input("Codelaenge n (Enter=auto): ").strip()
                n_val = None
                if n_input:
                    try:
                        n_val = int(n_input)
                        if n_val <= 0:
                            print("n muss > 0")
                            continue
                    except ValueError:
                        print("Ungueltige Zahl")
                        continue

                # Berechnung
                print("\nBerechne...")
                result = self.create_parity_matrix_compact(gen_poly, n_val)

                if result:
                    self.last_result = result

                    # Hauptmenü
                    while True:
                        print("\n--- OPTIONEN ---")
                        print("1: Details zeigen")
                        print("2: Neue Berechnung")
                        print("q: Beenden")

                        choice = input("Wahl: ").strip().lower()

                        if choice == 'q':
                            return
                        elif choice == '1':
                            self.show_details_menu(result)
                        elif choice == '2':
                            break
                        else:
                            print("Ungueltig!")
                else:
                    input("\nEnter...")

        except KeyboardInterrupt:
            print("\nAbgebrochen.")
        except Exception as e:
            print("FEHLER: {}".format(str(e)))


# Beispiel für eigenständige Nutzung:
if __name__ == "__main__":
    # Minimal-Implementierung der Basisklasse für Tests
    class BaseChannelCodingTool:
        def validate_generator_polynomial(self, poly_str):
            errors = []
            warnings = []

            if not poly_str:
                errors.append("Leerer String")
                return errors, warnings

            if not all(c in '01' for c in poly_str):
                errors.append("Nur 0 und 1 erlaubt")
                return errors, warnings

            if poly_str[0] != '1':
                warnings.append("Sollte mit 1 beginnen")

            if poly_str[-1] != '1':
                warnings.append("Sollte mit 1 enden")

            return errors, warnings


    # Test
    tool = CyclicCodeAnalysisTool()
    tool.run()


class ComprehensiveCodeAnalysisTool(BaseChannelCodingTool):
    """Kompakte Code-Analyse für Taschenrechner"""

    def clear_screen(self):
        """Bildschirm leeren (falls möglich)"""
        try:
            # ANSI clear screen für kompatible Terminals
            print('\033[2J\033[H')
        except:
            # Fallback: mehrere Leerzeilen
            for i in range(5):
                print('')

    def show_main_menu(self):
        """Zeigt das Hauptmenü"""
        self.clear_screen()
        print("=== CODE ANALYSE ===")
        print("1. Hamming-Code")
        print("2. CRC-Code")
        print("3. Blockcode")
        print("4. Pruefgleichungen")
        print("5. Beispiele")
        print("0. Beenden")
        print("=" * 20)

    def show_examples_menu(self):
        """Zeigt Beispiele"""
        self.clear_screen()
        print("=== BEISPIELE ===")
        print("Hamming (7,4):")
        print("Gl1: 1 2 3")
        print("Gl2: 1 2 4")
        print("Gl3: 1 3 4")
        print("")
        print("CRC Generator:")
        print("x3+x+1")
        print("1+x+x3")
        print("")
        print("Blockcode:")
        print("000 111 011 100")
        input("Enter...")

    def show_details_menu(self):
        """Zeigt Details-Menü mit Zahlen"""
        print("")
        print("Details:")
        print("1. Eigenschaften")
        print("2. Parameter")
        print("3. Berechnung")
        print("9. Zurueck")
        print("0. Beenden")

    def get_choice(self, prompt="Wahl: "):
        """Sichere Eingabe"""
        try:
            choice = input(prompt).strip()
            return choice
        except:
            return "0"

    def get_int_choice(self, prompt="Wahl: "):
        """Integer-Eingabe"""
        try:
            choice = input(prompt).strip()
            return int(choice)
        except:
            return -1

    def run(self):
        """Hauptschleife"""
        while True:
            try:
                self.show_main_menu()
                choice = self.get_int_choice()

                if choice == 0:
                    print("Programm beendet.")
                    break
                elif choice == 1:
                    if self.hamming_analysis():
                        break
                elif choice == 2:
                    if self.crc_analysis():
                        break
                elif choice == 3:
                    if self.block_analysis():
                        break
                elif choice == 4:
                    if self.parity_equations():
                        break
                elif choice == 5:
                    self.show_examples_menu()
                else:
                    print("Ungueltige Wahl!")
                    input("Enter...")

            except Exception as e:
                print("Fehler: " + str(e))
                input("Enter...")

    def hamming_analysis(self):
        """Hamming-Code Analyse"""
        self.clear_screen()
        print("=== HAMMING CODE ===")

        n_eq = self.safe_int_input("Anzahl Pruefgl.: ", 1, 10)
        if n_eq is None:
            return False

        equations = []
        print("Format: 1 2 3 4")
        for i in range(n_eq):
            while True:
                pos_str = self.get_choice("Gl. " + str(i + 1) + ": ")
                if pos_str == "0":
                    return True
                try:
                    positions = []
                    for x in pos_str.split():
                        positions.append(int(x))
                    equations.append(positions)
                    break
                except:
                    print("Fehler! Bsp: 1 2 3")

        # Basis-Ergebnis
        print("")
        print("--- ERGEBNIS ---")
        print("h = 3 (Hamming)")
        print("Korr: e = 1")
        print("Erk: e* = 2")

        # Details anbieten
        return self.show_hamming_details(equations)

    def show_hamming_details(self, equations):
        """Zeigt Hamming Details"""
        while True:
            self.show_details_menu()
            detail = self.get_int_choice()

            if detail == 0:
                return True
            elif detail == 9:
                return False
            elif detail == 1:
                self.show_hamming_properties()
            elif detail == 2:
                self.show_hamming_parameters(equations)
            elif detail == 3:
                self.show_hamming_calculation(equations)
            else:
                print("Ungueltig!")

    def show_hamming_properties(self):
        """Hamming Eigenschaften"""
        self.clear_screen()
        print("=== EIGENSCHAFTEN ===")
        print("Hamming-Distanz: 3")
        print("1-Bit Korrektur")
        print("2-Bit Erkennung")
        print("SECDED moeglich")
        print("Perfekter Code")
        input("Enter...")

    def show_hamming_parameters(self, equations):
        """Hamming Parameter"""
        self.clear_screen()
        print("=== PARAMETER ===")

        k = len(equations)
        # Schätze n basierend auf höchster Position
        max_pos = 0
        for eq in equations:
            for pos in eq:
                if pos > max_pos:
                    max_pos = pos
        n_est = max_pos + k

        print("Kontrollbits k: " + str(k))
        print("Geschaetzt n: " + str(n_est))
        print("Datenbits m: " + str(n_est - k))
        print("Coderate: " + str(n_est - k) + "/" + str(n_est))
        input("Enter...")

    def show_hamming_calculation(self, equations):
        """Hamming Berechnung"""
        self.clear_screen()
        print("=== BERECHNUNG ===")

        print("Pruefgleichungen:")
        for i, eq in enumerate(equations):
            eq_str = ""
            for j, pos in enumerate(eq):
                if j > 0:
                    eq_str += "+"
                eq_str += "x" + str(pos)
            print("x" + str(len(equations) + i + 1) + "=" + eq_str)

        input("Enter...")

    def crc_analysis(self):
        """CRC-Code Analyse"""
        self.clear_screen()
        print("=== CRC CODE ===")

        print("Format: x3+x+1")
        while True:
            gen = self.get_choice("Generator g(x): ")
            if gen == "0":
                return True

            errors, warnings = self.validate_generator_polynomial(gen)
            if not errors:
                break
            print("Fehler: " + str(errors[0]))

        # Basis-Analyse
        degree = self.get_poly_degree(gen)
        print("")
        print("--- ERGEBNIS ---")
        print("Grad: " + str(degree))
        print("Kontrollbits: " + str(degree))
        print("h >= 3 (CRC)")

        return self.show_crc_details(gen, degree)

    def show_crc_details(self, gen, degree):
        """CRC Details"""
        while True:
            self.show_details_menu()
            detail = self.get_int_choice()

            if detail == 0:
                return True
            elif detail == 9:
                return False
            elif detail == 1:
                self.show_crc_properties()
            elif detail == 2:
                self.show_crc_parameters(gen, degree)
            elif detail == 3:
                self.show_crc_calculation(gen)
            else:
                print("Ungueltig!")

    def show_crc_properties(self):
        """CRC Eigenschaften"""
        self.clear_screen()
        print("=== CRC EIGENSCHAFTEN ===")
        print("Zyklischer Code")
        print("Polynom-Darstellung")
        print("Schieberegister")
        print("Burst-Fehler gut")
        print("Hardware-effizient")
        input("Enter...")

    def show_crc_parameters(self, gen, degree):
        """CRC Parameter"""
        self.clear_screen()
        print("=== CRC PARAMETER ===")
        print("Generator: " + gen)
        print("Grad: " + str(degree))
        print("Kontrollstellen: " + str(degree))
        print("Min. Distanz: >= 3")
        input("Enter...")

    def show_crc_calculation(self, gen):
        """CRC Berechnung"""
        self.clear_screen()
        print("=== CRC RECHNUNG ===")

        data = self.get_choice("Daten (Bsp 1101): ")
        if data == "0":
            return

        print("Daten: " + data)
        print("Generator: " + gen)
        print("Polynomdivision:")
        print("Rest = CRC")
        input("Enter...")

    def block_analysis(self):
        """Blockcode Analyse"""
        self.clear_screen()
        print("=== BLOCKCODE ===")

        n_cw = self.safe_int_input("Anzahl CW: ", 2, 20)
        if n_cw is None:
            return False

        codewords = []
        print("Format: 000 111 101")
        for i in range(n_cw):
            cw = self.get_choice("CW " + str(i + 1) + ": ")
            if cw == "0":
                return True
            # Bereinige Eingabe
            clean_cw = cw.replace(" ", "").replace("'", "")
            codewords.append(clean_cw)

        # Hamming-Distanz berechnen
        min_dist = self.calculate_min_distance(codewords)

        print("")
        print("--- ERGEBNIS ---")
        print("h_min = " + str(min_dist))
        if min_dist > 0:
            print("Korr: e = " + str((min_dist - 1) // 2))
            print("Erk: e* = " + str(min_dist - 1))

        return self.show_block_details(codewords, min_dist)

    def show_block_details(self, codewords, min_dist):
        """Blockcode Details"""
        while True:
            self.show_details_menu()
            detail = self.get_int_choice()

            if detail == 0:
                return True
            elif detail == 9:
                return False
            elif detail == 1:
                self.show_block_properties(min_dist)
            elif detail == 2:
                self.show_block_parameters(codewords, min_dist)
            elif detail == 3:
                self.show_block_calculation(codewords)
            else:
                print("Ungueltig!")

    def show_block_properties(self, min_dist):
        """Block Eigenschaften"""
        self.clear_screen()
        print("=== EIGENSCHAFTEN ===")
        print("Min. Distanz: " + str(min_dist))
        if min_dist >= 3:
            print("1-Bit Korrektur")
            print("2-Bit Erkennung")
        elif min_dist == 2:
            print("1-Bit Erkennung")
        else:
            print("Keine Fehlerkorr.")
        input("Enter...")

    def show_block_parameters(self, codewords, min_dist):
        """Block Parameter"""
        self.clear_screen()
        print("=== PARAMETER ===")

        n = len(codewords[0]) if codewords else 0
        print("Codelaenge n: " + str(n))
        print("Anzahl CW: " + str(len(codewords)))
        print("Min. Distanz: " + str(min_dist))

        k_str = self.get_choice("Datenbits k: ")
        if k_str and k_str != "0":
            try:
                k = int(k_str)
                rate = float(k) / float(n)
                print("Coderate: " + str(round(rate, 3)))

                singleton = n - k + 1
                print("Singleton <= " + str(singleton))
                if min_dist <= singleton:
                    print("Bound OK")
                else:
                    print("Bound verletzt!")
            except:
                pass

        input("Enter...")

    def show_block_calculation(self, codewords):
        """Block Berechnung"""
        self.clear_screen()
        print("=== BERECHNUNG ===")

        print("Hamming-Distanzen:")
        n = len(codewords)
        for i in range(min(n, 3)):  # Zeige max 3 Paare
            for j in range(i + 1, min(n, 4)):
                if j < len(codewords):
                    dist = self.hamming_distance(codewords[i], codewords[j])
                    print("d(" + str(i) + "," + str(j) + ")=" + str(dist))

        if n > 4:
            print("...")

        input("Enter...")

    def parity_equations(self):
        """Prüfgleichungen-Tool"""
        self.clear_screen()
        print("=== PRUEFGLEICHUNGEN ===")

        n_eq = self.safe_int_input("Anzahl: ", 1, 10)
        if n_eq is None:
            return False

        equations = []
        print("Format: 1 2 3 4")
        for i in range(n_eq):
            while True:
                pos_str = self.get_choice("Gl. " + str(i + 1) + ": ")
                if pos_str == "0":
                    return True
                try:
                    positions = []
                    for x in pos_str.split():
                        positions.append(int(x))
                    equations.append(positions)
                    break
                except:
                    print("Fehler!")

        # Prüfmatrix aufbauen und anzeigen
        self.show_parity_matrix(equations)

        return False

    def show_parity_matrix(self, equations):
        """Zeigt Prüfmatrix"""
        self.clear_screen()
        print("=== PRUEFMATRIX ===")

        # Finde maximale Position
        max_pos = 0
        for eq in equations:
            for pos in eq:
                if pos > max_pos:
                    max_pos = pos

        print("H-Matrix:")
        for i, eq in enumerate(equations):
            row = ""
            for pos in range(1, max_pos + 1):
                if pos in eq:
                    row += "1 "
                else:
                    row += "0 "
            print(row)

        input("Enter...")

    def calculate_min_distance(self, codewords):
        """Berechnet minimale Hamming-Distanz"""
        if len(codewords) < 2:
            return 0

        min_dist = 999999  # Sehr große Zahl als Ersatz für float('inf')
        for i in range(len(codewords)):
            for j in range(i + 1, len(codewords)):
                dist = self.hamming_distance(codewords[i], codewords[j])
                if dist < min_dist:
                    min_dist = dist

        return min_dist if min_dist < 999999 else 0

    def hamming_distance(self, a, b):
        """Berechnet Hamming-Distanz zwischen zwei Strings"""
        if len(a) != len(b):
            return 999999  # Ersatz für float('inf')

        dist = 0
        for i in range(len(a)):
            if a[i] != b[i]:
                dist += 1
        return dist

    def get_poly_degree(self, poly):
        """Ermittelt Grad eines Polynoms"""
        poly = poly.replace(" ", "").replace("+", "").lower()

        max_degree = 0
        i = 0
        while i < len(poly):
            if poly[i] == 'x':
                if i + 1 < len(poly) and poly[i + 1].isdigit():
                    degree_str = ""
                    j = i + 1
                    while j < len(poly) and poly[j].isdigit():
                        degree_str += poly[j]
                        j += 1
                    degree = int(degree_str)
                    if degree > max_degree:
                        max_degree = degree
                    i = j
                else:
                    if max_degree < 1:
                        max_degree = 1
                    i += 1
            else:
                i += 1

        return max_degree

    def safe_int_input(self, prompt, min_val=1, max_val=100):
        """Sichere Integer-Eingabe"""
        while True:
            try:
                value_str = self.get_choice(prompt)
                if value_str == "0":
                    return None
                value = int(value_str)
                if min_val <= value <= max_val:
                    return value
                else:
                    print("Bereich: " + str(min_val) + "-" + str(max_val))
            except:
                print("Zahl eingeben!")

    def validate_generator_polynomial(self, poly):
        """Validiert Generatorpolynom"""
        errors = []
        warnings = []

        if not poly or not poly.strip():
            errors.append("Leeres Polynom")
            return errors, warnings

        # Einfache Validierung
        poly_lower = poly.lower()
        if 'x' not in poly_lower:
            errors.append("Kein x gefunden")

        return errors, warnings


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

    def run(self) -> None:
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
            print("\n--- Berechnete Code-Parameter ---")
            print("Codelänge (n = k_info + k_control): {}".format(n_codelength))

            # 2. Anzahl gültige Codewörter
            num_valid_codewords = 2 ** k_info
            print("Anzahl gültige Codewörter (2^k_info): {}".format(int(num_valid_codewords)))  #

            # 3. Anzahl mögliche Codewörter
            num_possible_codewords = 2 ** n_codelength
            print("Anzahl mögliche Codewörter (2^n): {}".format(int(num_possible_codewords)))  #

            # 4. Sicher erkennbare Fehler e*
            e_star = h_dist - 1
            print("Sicher erkennbare Fehler (e* = h - 1): {}".format(e_star))  #

            # 5. Sicher korrigierbare Fehler e
            e_corr = (h_dist - 1) // 2

            print("Sicher korrigierbare Fehler (e = floor((h-1)/2)): {}".format(e_corr))

            # 6. Prüfung auf Dichtgepacktheit
            print("\n--- Prüfung auf Dichtgepacktheit (Perfekter Code) ---")
            if e_corr < 0:
                print("\n--- Prüfung auf Dichtgepacktheit (Perfekter Code) ---")
                is_perfect = False
            else:
                sum_combinations = 0
                print(
                    "Berechnung der Summe der Binomialkoeffizienten S = Σ C(n, i) für i von 0 bis e_corr (e_corr={}):".format(
                        e_corr))
                for i in range(e_corr + 1):
                    comb = self.combinations(n_codelength, i)
                    print("  C({}, {}) = {}".format(n_codelength, i, comb))
                    sum_combinations += comb
                print("S = {}".format(sum_combinations))

                val_for_perfection = 2 ** (n_codelength - k_info)

                print("\nPrüfung der Hamming-Grenze:")
                print("  Linke Seite (Anzahl Wörter in allen Kugeln): 2^k_info * S = {} * {} = {}".format(
                    int(num_valid_codewords), sum_combinations, int(num_valid_codewords * sum_combinations)))
                print("  Rechte Seite (Gesamtzahl Wörter im Raum): 2^n = {}".format(int(num_possible_codewords)))
                print("  Vereinfachte Prüfung: S = {}, Sollwert für Perfektion (2^(n-k_info)): {}".format(
                    sum_combinations, val_for_perfection))

                is_perfect = False
                # Toleranz für Fließkommavergleiche
                if isinstance(val_for_perfection, float):
                    is_perfect = abs(sum_combinations - val_for_perfection) < self.tolerance
                else:  # Sollte bei Potenzen von 2 ein int sein
                    is_perfect = (sum_combinations == val_for_perfection)

                if is_perfect:
                    print("\n✅ Ergebnis: Der Code ist DICHTGEPACKT (PERFEKT).")
                    print("   Die Bedingung 2^k_info * Σ C(n,i) = 2^n ist erfüllt.")
                else:
                    print("\n❌ Ergebnis: Der Code ist NICHT dichtgepackt.")
                    if (num_valid_codewords * sum_combinations) > num_possible_codewords:
                        print(
                            "   Die Kugelpackungsschranke ist verletzt (2^k_info * S > 2^n). Dies sollte für gültige Codes nicht passieren.")
                    else:
                        print("\n❌ Ergebnis: Der Code ist NICHT dichtgepackt.")

        except ValueError as ve:
            print("❌ Eingabefehler: {}".format(ve))
        except Exception as e:
            print("❌ Ein unerwarteter Fehler ist aufgetreten: {}".format(e))
        input("\nDrücke Enter zum Fortfahren...")  # Hinzugefügt
