from tool_base import *


class HammingDistanceTool(Tool):
    def hamming_distance(self, str1, str2):
        """Berechnet die Hamming-Distanz zwischen zwei binären Strings"""
        if len(str1) != len(str2):
            raise ValueError("Die Strings müssen die gleiche Länge haben")

        # Zähle die Anzahl der unterschiedlichen Bits
        distance = sum(bit1 != bit2 for bit1, bit2 in zip(str1, str2))
        return distance

    def run(self) -> None:
        print("==== Hamming-Distanz ====")
        try:
            print("Berechnet die Hamming-Distanz zwischen zwei binären Strings")
            str1 = input("Erster binärer String: ")
            str2 = input("Zweiter binärer String: ")

            # Überprüfen, ob die Eingaben binär sind
            if not all(bit in '01' for bit in str1) or not all(bit in '01' for bit in str2):
                print("Fehler: Beide Strings müssen binär sein (nur 0 und 1 enthalten)")
            else:
                distance = self.hamming_distance(str1, str2)
                print(f"\nDie Hamming-Distanz beträgt: {distance}")
        except Exception as e:
            print("Fehler:", str(e))

        print("\nDrücke Enter, um fortzufahren...")
        input()


class SyndromeTool(Tool):
    def calculate_syndrome(self, received_word, parity_check_matrix):
        """Berechnet das Syndrom eines empfangenen Worts"""
        n = len(received_word)
        k = n - len(parity_check_matrix)

        # Berechne das Syndrom: s = H * r^T
        syndrome = []
        for row in parity_check_matrix:
            s = 0
            for i in range(n):
                s = (s + int(received_word[i]) * int(row[i])) % 2
            syndrome.append(s)

        return syndrome

    def run(self) -> None:
        print("==== Syndrom berechnen ====")
        try:
            print("Berechnet das Syndrom eines empfangenen Codeworts")
            print("Geben Sie das empfangene Codewort ein:")
            received_word = input("Empfangenes Codewort (binär): ")

            if not all(bit in '01' for bit in received_word):
                print("Fehler: Das Codewort muss binär sein (nur 0 und 1 enthalten)")
                return

            print("\nGeben Sie die Prüfmatrix H ein (Zeilen durch Kommas getrennt):")
            print("Beispiel für (7,4)-Hamming-Code: 1101000,1011100,1110010")
            parity_matrix_input = input("Prüfmatrix H: ")

            # Parsen der Prüfmatrix
            parity_check_matrix = []
            for row in parity_matrix_input.split(','):
                if not all(bit in '01' for bit in row):
                    print("Fehler: Die Prüfmatrix muss binär sein")
                    return
                parity_check_matrix.append(row)

            # Überprüfe, ob die Länge der Matrix mit dem Codewort übereinstimmt
            if any(len(row) != len(received_word) for row in parity_check_matrix):
                print("Fehler: Jede Zeile der Prüfmatrix muss die gleiche Länge wie das Codewort haben")
                return

            syndrome = self.calculate_syndrome(received_word, parity_check_matrix)

            print("\nDas Syndrom ist:", ''.join(map(str, syndrome)))

            # Überprüfe, ob das Codewort fehlerfrei ist
            if all(s == 0 for s in syndrome):
                print("Das Codewort ist fehlerfrei.")
            else:
                print("Das Codewort enthält Fehler.")

        except Exception as e:
            print("Fehler:", str(e))

        print("\nDrücke Enter, um fortzufahren...")
        input()


class CRCCheckTool(Tool):
    def crc_check(self, message, poly, crc):
        """Überprüft eine CRC-Prüfsumme"""
        # Kombiniere Nachricht und CRC
        combined = message + crc

        # Führe Polynomdivision durch
        return self.polynomial_division(combined, poly) == '0' * (len(poly) - 1)

    def polynomial_division(self, dividend, divisor):
        """Führt eine Polynomdivision im GF(2) durch"""
        # Konvertiere in Binärlisten
        dividend = list(map(int, dividend))
        divisor = list(map(int, divisor))

        # Führe die Polynomdivision durch
        for i in range(len(dividend) - len(divisor) + 1):
            if dividend[i] == 1:
                for j in range(len(divisor)):
                    dividend[i + j] ^= divisor[j]

        # Gib den Rest zurück
        remainder = ''.join(map(str, dividend[-(len(divisor) - 1):]))
        return remainder

    def run(self) -> None:
        print("==== CRC prüfen ====")
        try:
            print("Überprüft, ob eine Nachricht mit CRC-Prüfsumme fehlerfrei ist")

            message = input("Nachricht (binär): ")
            if not all(bit in '01' for bit in message):
                print("Fehler: Die Nachricht muss binär sein (nur 0 und 1 enthalten)")
                return

            poly = input("Generator-Polynom (binär, z.B. 1011 für x³+x+1): ")
            if not all(bit in '01' for bit in poly) or poly[0] != '1':
                print("Fehler: Das Generator-Polynom muss binär sein und mit 1 beginnen")
                return

            crc = input("CRC-Prüfsumme (binär): ")
            if not all(bit in '01' for bit in crc):
                print("Fehler: Die CRC-Prüfsumme muss binär sein")
                return

            if len(crc) != len(poly) - 1:
                print(f"Warnung: Die CRC-Prüfsumme sollte {len(poly) - 1} Bits lang sein")

            result = self.crc_check(message, poly, crc)

            if result:
                print("\nDie CRC-Prüfung ist ERFOLGREICH: keine Fehler erkannt")
            else:
                print("\nDie CRC-Prüfung ist FEHLGESCHLAGEN: Übertragungsfehler erkannt")

        except Exception as e:
            print("Fehler:", str(e))

        print("\nDrücke Enter, um fortzufahren...")
        input()


class CRCCalculationTool(Tool):
    def calculate_crc(self, message, poly):
        """Berechnet eine CRC-Prüfsumme"""
        # Füge (len(poly) - 1) Nullen ans Ende der Nachricht an
        padded_message = message + '0' * (len(poly) - 1)

        # Führe Polynomdivision durch
        remainder = self.polynomial_division(padded_message, poly)

        return remainder

    def polynomial_division(self, dividend, divisor):
        """Führt eine Polynomdivision im GF(2) durch"""
        # Konvertiere in Binärlisten
        dividend = list(map(int, dividend))
        divisor = list(map(int, divisor))

        # Führe die Polynomdivision durch
        for i in range(len(dividend) - len(divisor) + 1):
            if dividend[i] == 1:
                for j in range(len(divisor)):
                    dividend[i + j] ^= divisor[j]

        # Gib den Rest zurück
        remainder = ''.join(map(str, dividend[-(len(divisor) - 1):]))
        return remainder

    def run(self) -> None:
        print("==== CRC berechnen ====")
        try:
            print("Berechnet eine CRC-Prüfsumme für eine Nachricht")

            message = input("Nachricht (binär): ")
            if not all(bit in '01' for bit in message):
                print("Fehler: Die Nachricht muss binär sein (nur 0 und 1 enthalten)")
                return

            poly = input("Generator-Polynom (binär, z.B. 1011 für x³+x+1): ")
            if not all(bit in '01' for bit in poly) or poly[0] != '1':
                print("Fehler: Das Generator-Polynom muss binär sein und mit 1 beginnen")
                return

            crc = self.calculate_crc(message, poly)

            print(f"\nCRC-Prüfsumme: {crc}")
            print(f"Vollständiger kodierter Bitstrom: {message + crc}")

            # Zeige die polynom-Notation
            degree = len(poly) - 1
            poly_terms = []
            for i, bit in enumerate(poly):
                if bit == '1':
                    power = degree - i
                    if power == 0:
                        poly_terms.append("1")
                    elif power == 1:
                        poly_terms.append("x")
                    else:
                        poly_terms.append(f"x^{power}")

            poly_notation = " + ".join(poly_terms)
            print(f"Generator-Polynom: {poly_notation}")

        except Exception as e:
            print("Fehler:", str(e))

        print("\nDrücke Enter, um fortzufahren...")
        input()