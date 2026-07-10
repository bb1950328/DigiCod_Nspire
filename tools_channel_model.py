from tool_base import *
import math


class BaseChannelTool(Tool):
    """Basis-Klasse mit Validierungsfunktionen für alle Kanalmodell-Tools"""

    def __init__(self):
        self.tolerance = 0.000001

    def validate_probabilities(self, probs, name):
        """Validiert Wahrscheinlichkeitsverteilung"""
        errors = []
        warnings = []

        # Prüfe auf negative Werte und Werte > 1
        for i in range(len(probs)):
            p = probs[i]
            if p < 0:
                errors.append("FEHLER: " + name + "[" + str(i) + "] = " +
                              str(round(p, 6)) +
                              " < 0 (negative Wahrscheinlichkeit)")
            elif p > 1:
                errors.append("FEHLER: " + name + "[" + str(i) + "] = " +
                              str(round(p, 6)) +
                              " > 1 (Wahrscheinlichkeit > 1)")

        # Prüfe Summe
        total = sum(probs)
        if abs(total - 1.0) > self.tolerance:
            errors.append("FEHLER: Summe von " + name + " = " +
                          str(round(total, 6)) + " ≠ 1.0 (Abweichung: " +
                          str(round(abs(total - 1.0), 6)) + ")")
        elif abs(total - 1.0) > 0.0000000001:  # 1e-10
            warnings.append("WARNUNG: Kleine Rundungsabweichung bei " + name +
                            ": Summe = " + str(round(total, 10)))

        # Prüfe auf Null-Wahrscheinlichkeiten
        zero_count = 0
        for p in probs:
            if p == 0:
                zero_count += 1
        if zero_count > 0:
            warnings.append(
                "WARNUNG: " + name + " enthält " + str(zero_count) +
                " Null-Wahrscheinlichkeiten (kann zu log(0) führen)")

        return errors, warnings

    def validate_channel_matrix(self, channel_matrix, name):
        """Validiert Kanalmatrix P(Y|X)"""
        errors = []
        warnings = []

        if not channel_matrix:
            errors.append("FEHLER: " + name + " ist leer")
            return errors, warnings

        n_inputs = len(channel_matrix)
        n_outputs = len(channel_matrix[0]) if channel_matrix else 0

        # Prüfe Rechteck-Form
        for i in range(len(channel_matrix)):
            row = channel_matrix[i]
            if len(row) != n_outputs:
                errors.append("FEHLER: " + name + "[" + str(i) + "] hat " +
                              str(len(row)) + " Spalten, erwartet " +
                              str(n_outputs))

        if errors:  # Stoppe wenn Matrix-Form falsch
            return errors, warnings

        # Prüfe jede Zeile (muss sich zu 1 summieren)
        for i in range(len(channel_matrix)):
            row = channel_matrix[i]
            row_errors, row_warnings = self.validate_probabilities(
                row, name + "[Zeile " + str(i) + "]")
            errors.extend(row_errors)
            warnings.extend(row_warnings)

        return errors, warnings

    def safe_float_input(self, prompt, min_val, max_val):
        """Sichere Eingabe von Gleitkommazahlen mit Validierung"""
        while True:
            try:
                user_input = input(prompt +
                                   " (oder 'q' für Hauptmenü): ").strip()
                if user_input.lower() == 'q':
                    return 'q'

                value = float(user_input)
                if value < min_val:
                    print("X Wert " + str(round(value, 6)) + " < " +
                          str(round(min_val, 6)) +
                          " (Minimum). Bitte erneut eingeben.")
                    continue
                if value > max_val:
                    print("X Wert " + str(round(value, 6)) + " > " +
                          str(round(max_val, 6)) +
                          " (Maximum). Bitte erneut eingeben.")
                    continue
                return value
            except:
                print("X Ungültige Eingabe. Bitte eine Zahl eingeben.")
                continue

    def safe_int_input(self, prompt, min_val, max_val):
        """Sichere Eingabe von Ganzzahlen mit Validierung"""
        while True:
            try:
                in_str = input(prompt + " (oder 'q' für Hauptmenü): ")
                if in_str.lower() == 'q':
                    return 'q'

                in_int = int(in_str)
                if in_int < min_val:
                    print("X Wert " + str(in_int) + " < " + str(min_val) + " (Minimum). Bitte erneut eingeben.")
                    continue
                if in_int > max_val:
                    print("X Wert " + str(in_int) + " > " + str(max_val) + " (Maximum). Bitte erneut eingeben.")
                    continue
                return in_int
            except Exception as e:
                print("X Ungültige Eingabe. Bitte eine Ganzzahl eingeben. {}".format(e))
                continue

    def wait_for_continue(self):
        """Wartet auf Benutzereingabe mit Möglichkeit zurück zum Hauptmenü zu gehen"""
        user_input = input(
            "\nDrücke Enter um fortzufahren oder 'q' für Hauptmenü: ").strip(
            ).lower()
        return user_input == 'q'

    def input_probabilities_with_validation(self, name, count):
        """Eingabe von Wahrscheinlichkeiten mit automatischer Validierung"""
        print("\n" + name + " eingeben:")
        print("(Tipp: Gib die Werte so ein, dass sie sich zu 1.0 summieren)")

        while True:  # Wiederhole bis gültige Eingabe
            probs = []
            print("\nEingabe der " + str(count) + " Wahrscheinlichkeiten:")
            for i in range(count):
                prob = self.safe_float_input("P(x" + str(i) + "): ", 0.0, 1.0)
                if prob == 'q':
                    return 'q'
                probs.append(prob)

            # Validierung
            errors, warnings = self.validate_probabilities(probs, name)

            if not errors:
                if warnings:
                    print("\n!! WARNUNGEN:")
                    for warning in warnings:
                        print("   " + warning)
                    accept = input("Trotzdem fortfahren? (j/n/q): ").lower()
                    if accept == 'q':
                        return 'q'
                    if accept == 'j':
                        return probs
                    print("Bitte Werte korrigieren:")
                    continue
                print("Eingabe gültig!")
                return probs
            print("\nFEHLER gefunden:")
            for error in errors:
                print("   " + error)

            # Automatische Korrektur anbieten
            total = sum(probs)
            if abs(total - 1.0) > self.tolerance and total > 0:
                print("\nAutomatische Normalisierung möglich:")
                normalized = []
                for p in probs:
                    normalized.append(p / total)
                normalized_rounded = []
                for p in normalized:
                    normalized_rounded.append(round(p, 6))
                print("Normalisierte Werte: " + str(normalized_rounded))
                use_normalized = input(
                    "Normalisierte Werte verwenden? (j/n/q): ").lower()
                if use_normalized == 'q':
                    return 'q'
                if use_normalized == 'j':
                    return normalized
            print("Bitte Eingabe wiederholen:")
            continue

    def input_channel_matrix_with_validation(self, n_inputs, n_outputs):
        """Eingabe einer Kanalmatrix mit automatischer Validierung"""
        print("\nKanalmatrix P(Y|X) eingeben:")
        print("(Jede Zeile muss sich zu 1.0 summieren)")

        while True:  # Wiederhole bis gültige Matrix
            channel_matrix = []
            for i in range(n_inputs):
                print("\nZeile " + str(i) + " (P(Y|X=x" + str(i) + ")):")
                row = []
                for j in range(n_outputs):
                    prob = self.safe_float_input(
                        "  P(y" + str(j) + "|x" + str(i) + "): ", 0.0, 1.0)
                    if prob == 'q':
                        return 'q'
                    row.append(prob)
                channel_matrix.append(row)

            # Validierung
            errors, warnings = self.validate_channel_matrix(
                channel_matrix, "P(Y|X)")

            if not errors:
                if warnings:
                    print("\n!!  WARNUNGEN:")
                    for warning in warnings:
                        print("   " + warning)
                        return channel_matrix
                    print("Bitte Matrix korrigieren:")
                    continue
                print("Kanalmatrix gültig!")
                return channel_matrix

            print("\nFEHLER in Kanalmatrix:")
            for error in errors:
                print("   " + error)

            # Automatische Normalisierung anbieten
            can_normalize = True
            for row in channel_matrix:
                if sum(row) <= 0:
                    can_normalize = False
                    break

            if can_normalize:
                print("Automatische Zeilennormalisierung möglich:")
                normalized_matrix = []
                for i, row in enumerate(channel_matrix):
                    row_sum = sum(row)
                    normalized_row = []
                    for p in row:
                        normalized_row.append(p / row_sum)
                    normalized_matrix.append(normalized_row)
                    rounded_row = []
                    for p in normalized_row:
                        rounded_row.append(round(p, 6))
                    print("  Zeile " + str(i) + ": " + str(rounded_row))
                use_normalized = input(
                    "Normalisierte Matrix verwenden? (j/n/q): ").lower()
                if use_normalized == 'q':
                    return 'q'
                if use_normalized == 'j':
                    return normalized_matrix
            print("Bitte Matrix-Eingabe wiederholen:")
            continue

    def safe_log2(self, x):
        """Sichere log2 Berechnung für MicroPython"""
        if x <= 0:
            return 0
        try:
            return math.log(x) / math.log(2)
        except:
            return 0


class TransinformationTool(BaseChannelTool):
    """Tool für Transinformation-Berechnung"""

    def run(self):
        print("==== Transinformation berechnen ====")
        try:
            n_input = self.safe_int_input("Anzahl der Eingangssymbole: ", 2,
                                          10)
            if n_input == 'q':
                return

            n_output = self.safe_int_input("Anzahl der Ausgangssymbole: ", 2,
                                           10)
            if n_output == 'q':
                return

            # Eingabewahrscheinlichkeiten mit Validierung
            px = self.input_probabilities_with_validation(
                "Eingabewahrscheinlichkeiten P(X)", n_input)
            if px == 'q':
                return

            # Kanalmatrix mit Validierung
            pyx = self.input_channel_matrix_with_validation(n_input, n_output)
            if pyx == 'q':
                return

            # Berechne die Ausgabewahrscheinlichkeiten p(y)
            py = []
            for j in range(n_output):
                py_j = 0
                for i in range(n_input):
                    py_j += px[i] * pyx[i][j]
                py.append(py_j)

            print("\n==== BERECHNUNGEN ====")
            py_rounded = []
            for p in py:
                py_rounded.append(round(p, 4))
            print("Ausgabewahrscheinlichkeiten P(Y): " + str(py_rounded))

            # Berechne die Entropien
            hx = 0
            for p in px:
                if p > 0:
                    hx += -p * self.safe_log2(p)

            hy = 0
            for p in py:
                if p > 0:
                    hy += -p * self.safe_log2(p)

            # Berechne H(Y|X)
            hy_given_x = 0
            for i in range(n_input):
                if px[i] > 0:
                    h_y_xi = 0
                    for j in range(n_output):
                        if pyx[i][j] > 0:
                            h_y_xi += -pyx[i][j] * self.safe_log2(pyx[i][j])
                    hy_given_x += px[i] * h_y_xi

            # Transinformation I(X;Y) = H(Y) - H(Y|X)
            transinformation = hy - hy_given_x

            print("\n==== ERGEBNISSE ====")
            print("H(X) = " + str(round(hx, 4)) + " bits")
            print("H(Y) = " + str(round(hy, 4)) + " bits")
            print("H(Y|X) = " + str(round(hy_given_x, 4)) + " bits")
            print("Transinformation I(X;Y) = " +
                  str(round(transinformation, 4)) + " bits/Symbol")

            # Plausibilitätsprüfung
            if transinformation < -self.tolerance:
                print("FEHLER: I(X;Y) = " + str(round(transinformation, 6)) +
                      " < 0 (Transinformation kann nicht negativ sein!)")
            elif transinformation < 0:
                print("!! WARNUNG: Kleine negative Abweichung korrigiert: " +
                      str(round(transinformation, 10)) + " → 0")

        except Exception as e:
            print("Fehler: " + str(e))

        if self.wait_for_continue():
            return

class MaximumAPosterioriTool(BaseChannelTool):
    """Tool für Maximum-A-Posteriori-Entscheider"""

    def run(self):
        print("==== Maximum-A-Posteriori-Entscheider ====")
        try:
            n_input = self.safe_int_input("Anzahl der Eingangssymbole: ", 2,
                                          10)
            if n_input == 'q':
                return

            n_output = self.safe_int_input("Anzahl der Ausgangssymbole: ", 2,
                                           10)
            if n_output == 'q':
                return

            # Kanalmatrix mit Validierung
            channel_matrix = self.input_channel_matrix_with_validation(
                n_input, n_output)
            if channel_matrix == 'q':
                return

            # Eingabewahrscheinlichkeiten mit Validierung
            px = self.input_probabilities_with_validation(
                "Eingabewahrscheinlichkeiten P(X)", n_input)
            if px == 'q':
                return

            print("\n==== KANALMATRIX ====")
            print("     ", end="")
            for j in range(n_output):
                print("y" + str(j) + "      ", end="")
            print()

            for i in range(n_input):
                print("x" + str(i) + " ", end="")
                for j in range(n_output):
                    print(str(round(channel_matrix[i][j], 3)) + "   ", end="")
                print()

            print("\n==== MAP-ENTSCHEIDER-BERECHNUNG ====")
            decoder = {}

            for j in range(n_output):
                max_prob = -1
                best_input = -1

                print("\nFür y" + str(j) + ":")
                for i in range(n_input):
                    prob = channel_matrix[i][j]
                    x = px[i]
                    pxpyx = x * prob
                    print("P(x" + str(i) + ") * P(y" + str(j) + "|x" + str(i) + ") = " +
                          str(round(pxpyx, 3)))
                    if pxpyx > max_prob:
                        max_prob = pxpyx
                        best_input = i

                decoder[j] = best_input
                print("  → Wähle x" + str(best_input) + " (P = " +
                      str(round(max_prob, 3)) + ")")

            print("\n==== MAP-ENTSCHEIDER ====")
            for j in range(n_output):
                print("y" + str(j) + " → x" + str(decoder[j]))

            # Berechne Fehlerwahrscheinlichkeit falls gewünscht
            calc_error = input(
                "\nFehlerwahrscheinlichkeit berechnen? (j/n/q): ").lower()
            if calc_error in ['q', 'n']:
                return
            # Eingabewahrscheinlichkeiten mit Validierung
            px = self.input_probabilities_with_validation(
                "Eingabewahrscheinlichkeiten P(X)", n_input)
            if px == 'q':
                return

            # Berechne Fehlerwahrscheinlichkeit
            total_error_prob = 0
            print("\n==== FEHLERWAHRSCHEINLICHKEITS-BERECHNUNG ====")

            for i in range(n_input):
                for j in range(n_output):
                    decision = decoder[j]
                    is_error = decision != i
                    prob_contribution = px[i] * channel_matrix[i][j]

                    if is_error:
                        total_error_prob += prob_contribution
                        error_indicator = "✗"
                    else:
                        error_indicator = "✓"

                    print("P(x" + str(i) + ") * P(y" + str(j) + "|x" + str(i) +
                          ") = " + str(round(px[i], 3)) + " * " +
                          str(round(channel_matrix[i][j], 3)) + " = " +
                          str(round(prob_contribution, 4)) + " [y" + str(j) +
                          "→x" + str(decision) + "] " + error_indicator)

            print("\nGesamtfehlerwahrscheinlichkeit: P(Fehler) = " +
                  str(round(total_error_prob, 4)))

        except Exception as e:
            print("X Fehler: " + str(e))

        if self.wait_for_continue():
            return

class MaximumLikelihoodTool(BaseChannelTool):
    """Tool für Maximum-Likelihood-Entscheider"""

    def run(self):
        print("==== Maximum-Likelihood-Entscheider ====")
        try:
            n_input = self.safe_int_input("Anzahl der Eingangssymbole: ", 2,
                                          10)
            if n_input == 'q':
                return

            n_output = self.safe_int_input("Anzahl der Ausgangssymbole: ", 2,
                                           10)
            if n_output == 'q':
                return

            # Kanalmatrix mit Validierung
            channel_matrix = self.input_channel_matrix_with_validation(
                n_input, n_output)
            if channel_matrix == 'q':
                return

            print("\n==== KANALMATRIX ====")
            print("     ", end="")
            for j in range(n_output):
                print("y" + str(j) + "      ", end="")
            print()

            for i in range(n_input):
                print("x" + str(i) + " ", end="")
                for j in range(n_output):
                    print(str(round(channel_matrix[i][j], 3)) + "   ", end="")
                print()

            # ML-Entscheider: Für jedes yj, wähle xi mit höchstem P(yj|xi)
            print("\n==== ML-ENTSCHEIDER-BERECHNUNG ====")
            decoder = {}

            for j in range(n_output):
                max_prob = -1
                best_input = -1

                print("\nFür y" + str(j) + ":")
                for i in range(n_input):
                    prob = channel_matrix[i][j]
                    print("  P(y" + str(j) + "|x" + str(i) + ") = " +
                          str(round(prob, 3)))
                    if prob > max_prob:
                        max_prob = prob
                        best_input = i

                decoder[j] = best_input
                print("  → Wähle x" + str(best_input) + " (P = " +
                      str(round(max_prob, 3)) + ")")

            print("\n==== ML-ENTSCHEIDER ====")
            for j in range(n_output):
                print("y" + str(j) + " → x" + str(decoder[j]))

            # Berechne Fehlerwahrscheinlichkeit falls gewünscht
            calc_error = input(
                "\nFehlerwahrscheinlichkeit berechnen? (j/n/q): ").lower()
            if calc_error in ['q', 'n']:
                return
            # Eingabewahrscheinlichkeiten mit Validierung
            px = self.input_probabilities_with_validation(
                "Eingabewahrscheinlichkeiten P(X)", n_input)
            if px == 'q':
                return

            # Berechne Fehlerwahrscheinlichkeit
            total_error_prob = 0
            print("\n==== FEHLERWAHRSCHEINLICHKEITS-BERECHNUNG ====")

            for i in range(n_input):
                for j in range(n_output):
                    decision = decoder[j]
                    is_error = decision != i
                    prob_contribution = px[i] * channel_matrix[i][j]

                    if is_error:
                        total_error_prob += prob_contribution
                        error_indicator = "✗"
                    else:
                        error_indicator = "✓"

                    print("P(x" + str(i) + ") * P(y" + str(j) + "|x" + str(i) +
                          ") = " + str(round(px[i], 3)) + " * " +
                          str(round(channel_matrix[i][j], 3)) + " = " +
                          str(round(prob_contribution, 4)) + " [y" + str(j) +
                          "→x" + str(decision) + "] " + error_indicator)

            print("\nGesamtfehlerwahrscheinlichkeit: P(Fehler) = " +
                  str(round(total_error_prob, 4)))

        except Exception as e:
            print("X Fehler: " + str(e))

        if self.wait_for_continue():
            return


class EntropyCalculationTool(BaseChannelTool):
    """Tool zur Entropie-Berechnung"""

    def run(self):
        print("==== Entropie berechnen ====")
        try:
            n = self.safe_int_input("Anzahl Symbole: ", 2, 20)
            if n == 'q':
                return

            # Wahrscheinlichkeiten mit Validierung eingeben
            probs = self.input_probabilities_with_validation(
                "Symbolwahrscheinlichkeiten", n)
            if probs == 'q':
                return

            print("\n==== ENTROPIE-BERECHNUNG ====")
            print("H(X) = -∑ p(xi) * log₂(p(xi))")
            print()

            entropy = 0
            for i, p in enumerate(probs):
                if p > 0:
                    log_val = self.safe_log2(p)
                    contribution = -p * log_val
                    entropy += contribution
                    print("i=" + str(i) + ": p(x" + str(i) + ") = " +
                          str(round(p, 4)) + ", log₂(" + str(round(p, 4)) +
                          ") = " + str(round(log_val, 4)))
                    print("      Beitrag: -" + str(round(p, 4)) + " * " +
                          str(round(log_val, 4)) + " = " +
                          str(round(contribution, 4)))
                else:
                    print("i=" + str(i) + ": p(x" + str(i) + ") = " +
                          str(round(p, 4)) + ", log₂(" + str(round(p, 4)) +
                          ") = undefined (→ 0)")

            print("\nH(X) = " + str(round(entropy, 4)) + " bits")

            # Zusätzliche Informationen
            max_entropy = self.safe_log2(n)
            print("Maximale Entropie (Gleichverteilung): " +
                  str(round(max_entropy, 4)) + " bits")
            if entropy < max_entropy:
                redundancy = max_entropy - entropy
                print("Redundanz: " + str(round(redundancy, 4)) + " bits")

        except Exception as e:
            print("X Fehler: " + str(e))

        if self.wait_for_continue():
            return


class BinarySymmetricChannelTool(BaseChannelTool):
    """Tool für binären symmetrischen Kanal (BSC)"""

    def run(self):
        print("==== Binärer symmetrischer Kanal (BSC) ====")
        try:
            error_prob = self.safe_float_input("Fehlerwahrscheinlichkeit ε: ",
                                               0.0, 0.5)
            if error_prob == 'q':
                return

            # Validierung für BSC
            if error_prob > 0.5:
                print(
                    "!! WARNUNG: ε > 0.5 führt zu schlechterem Kanal als Raten!"
                )

            # Kanalmatrix
            channel_matrix = [[1 - error_prob, error_prob],
                              [error_prob, 1 - error_prob]]

            print("\n==== KANALMATRIX P(Y|X) ====")
            print("     y0      y1")
            print("x0   " + str(round(1 - error_prob, 3)) + "   " +
                  str(round(error_prob, 3)))
            print("x1   " + str(round(error_prob, 3)) + "   " +
                  str(round(1 - error_prob, 3)))

            # Eingabeverteilung
            equal_input = input(
                "\nGleichverteilte Eingabe verwenden? (j/n/q): ").lower()
            if equal_input == 'q':
                return
            if equal_input == 'n':
                input_probs = self.input_probabilities_with_validation(
                    "Eingabewahrscheinlichkeiten P(X)", 2)
                if input_probs == 'q':
                    return
            else:
                input_probs = [0.5, 0.5]
                print("Verwende gleichverteilte Eingabe: P(X) = [0.5, 0.5]")

            # Ausgabewahrscheinlichkeiten
            py0 = input_probs[0] * (1 -
                                    error_prob) + input_probs[1] * error_prob
            py1 = 1 - py0
            output_probs = [py0, py1]

            print("\n==== WAHRSCHEINLICHKEITEN ====")
            input_rounded = []
            for p in input_probs:
                input_rounded.append(round(p, 4))
            output_rounded = []
            for p in output_probs:
                output_rounded.append(round(p, 4))
            print("Eingabe P(X):  " + str(input_rounded))
            print("Ausgabe P(Y):  " + str(output_rounded))

            # Entropien
            hx = 0
            for p in input_probs:
                if p > 0:
                    hx += -p * self.safe_log2(p)

            hy = 0
            for p in output_probs:
                if p > 0:
                    hy += -p * self.safe_log2(p)

            if error_prob in [0, 1]:
                hy_given_x = 0
            else:
                hy_given_x = -error_prob * self.safe_log2(error_prob) - (
                    1 - error_prob) * self.safe_log2(1 - error_prob)

            mutual_info = hy - hy_given_x

            # Kanalkapazität
            if error_prob == 0:
                capacity = 1
            elif error_prob == 0.5:
                capacity = 0
            else:
                h_error = -error_prob * self.safe_log2(error_prob) - (
                    1 - error_prob) * self.safe_log2(1 - error_prob)
                capacity = 1 - h_error

            print("\n==== ENTROPIEN ====")
            print("H(X) = " + str(round(hx, 4)) + " bit")
            print("H(Y) = " + str(round(hy, 4)) + " bit")
            print("H(Y|X) = " + str(round(hy_given_x, 4)) + " bit")
            print("I(X;Y) = " + str(round(mutual_info, 4)) + " bit")
            print("\n==== KANALKAPAZITÄT ====")
            print("C = 1 - H(ε) = " + str(round(capacity, 4)) + " bit/Symbol")

            # Übertragungszeit berechnen
            calc_time = input(
                "\nÜbertragungszeit berechnen? (j/n/q): ").lower()
            if calc_time == 'q':
                return
            if calc_time == 'j':
                data_size = self.safe_int_input("Datenmenge (Bit): ", 1,
                                                1000000000)
                if data_size == 'q':
                    return

                channel_rate = self.safe_int_input("Kanalrate (bit/s): ", 1,
                                                   1000000000)
                if channel_rate == 'q':
                    return

                effective_rate = channel_rate * mutual_info
                if effective_rate > 0:
                    transmission_time = data_size / effective_rate
                    print("\n==== ÜBERTRAGUNGSZEIT ====")
                    print("Effektive Datenrate: " + str(channel_rate) + " × " +
                          str(round(mutual_info, 4)) + " = " +
                          str(round(effective_rate, 2)) + " bit/s")
                    print("Übertragungszeit: " + str(data_size) + " / " +
                          str(round(effective_rate, 2)) + " = " +
                          str(round(transmission_time, 2)) + " s")
                else:
                    print(
                        "X Effektive Datenrate = 0, keine Übertragung möglich!"
                    )

        except Exception as e:
            print("Fehler: " + str(e))

        if self.wait_for_continue():
            return


class ChannelMatrixDeterminationTool(BaseChannelTool):
    """Tool zur Bestimmung der Kanalmatrix aus Wahrscheinlichkeiten"""

    def run(self):
        print("==== Kanalmatrix aus Wahrscheinlichkeiten bestimmen ====")
        try:
            n_inputs = self.safe_int_input("Anzahl Eingänge: ", 2, 10)
            if n_inputs == 'q':
                return

            n_outputs = self.safe_int_input("Anzahl Ausgänge: ", 2, 10)
            if n_outputs == 'q':
                return

            # Eingabewahrscheinlichkeiten mit Validierung
            input_probs = self.input_probabilities_with_validation(
                "Eingabewahrscheinlichkeiten P(X)", n_inputs)
            if input_probs == 'q':
                return

            # Ausgabewahrscheinlichkeiten mit Validierung
            output_probs = self.input_probabilities_with_validation(
                "Ausgangswahrscheinlichkeiten P(Y)", n_outputs)
            if output_probs == 'q':
                return

            print("\n==== GEGEBENE DATEN ====")
            input_rounded = []
            for p in input_probs:
                input_rounded.append(round(p, 4))
            output_rounded = []
            for p in output_probs:
                output_rounded.append(round(p, 4))
            print("P(X) = " + str(input_rounded))
            print("P(Y) = " + str(output_rounded))

            if len(input_probs) == 2 and len(output_probs) == 2:
                # Binärer symmetrischer Kanal
                print("\n==== BINÄRER SYMMETRISCHER KANAL (BSC) ====")
                print("Annahme: P(Y|X) = [[1-ε, ε], [ε, 1-ε]]")

                p_x0, p_x1 = input_probs[0], input_probs[1]
                p_y0, p_y1 = output_probs[0], output_probs[1]

                print("\nGleichungssystem:")
                print("P(y0) = P(x0)*(1-ε) + P(x1)*ε = " + str(round(p_y0, 4)))
                print("P(y1) = P(x0)*ε + P(x1)*(1-ε) = " + str(round(p_y1, 4)))

                # Löse nach ε auf
                if abs(p_x0 - p_x1) > self.tolerance:
                    epsilon = (p_x0 - p_y0) / (p_x0 - p_x1)

                    # Validiere ε
                    if epsilon < 0 or epsilon > 1:
                        print("X FEHLER: Berechnetes ε = " +
                              str(round(epsilon, 4)) +
                              " nicht im gültigen Bereich [0, 1]")
                        print(
                            "Die gegebenen Wahrscheinlichkeiten sind nicht mit einem BSC konsistent!"
                        )
                        if self.wait_for_continue():
                            return
                        return

                    print("\n==== LÖSUNG ====")
                    print("ε = (P(x0) - P(y0)) / (P(x0) - P(x1))")
                    print("ε = (" + str(round(p_x0, 4)) + " - " +
                          str(round(p_y0, 4)) + ") / (" + str(round(p_x0, 4)) +
                          " - " + str(round(p_x1, 4)) + ") = " +
                          str(round(epsilon, 4)))

                    channel_matrix = [[1 - epsilon, epsilon],
                                      [epsilon, 1 - epsilon]]

                    print("\nKanalmatrix P(Y|X):")
                    print("     y0      y1")
                    print("x0   " + str(round(1 - epsilon, 3)) + "   " +
                          str(round(epsilon, 3)))
                    print("x1   " + str(round(epsilon, 3)) + "   " +
                          str(round(1 - epsilon, 3)))

                    # Verifikation
                    calc_y0 = input_probs[0] * (
                        1 - epsilon) + input_probs[1] * epsilon
                    calc_y1 = input_probs[0] * epsilon + input_probs[1] * (
                        1 - epsilon)

                    # Prüfe Abweichung
                    error_y0 = abs(calc_y0 - p_y0)
                    error_y1 = abs(calc_y1 - p_y1)
                    if error_y0 < self.tolerance and error_y1 < self.tolerance:
                        print("Verifikation erfolgreich!")
                    else:
                        print("\n==== VERIFIKATION ====")
                        print("P(Y) berechnet = [" + str(round(calc_y0, 4)) +
                              ", " + str(round(calc_y1, 4)) + "]")
                        print("P(Y) gegeben   = [" + str(round(p_y0, 4)) + ", " +
                              str(round(p_y1, 4)) + "]")
                        print("!! Abweichungen: Δy0=" +
                              str(round(error_y0, 6)) + ", Δy1=" +
                              str(round(error_y1, 6)))

                    # Vollständige Analyse anbieten
                    full_analysis = input(
                        "\nVollständige BSC-Analyse durchführen? (j/n/q): "
                    ).lower()
                    if full_analysis == 'q':
                        return
                    if full_analysis == 'j':
                        print("\n--- Automatische BSC-Analyse mit ε = " +
                              str(round(epsilon, 4)) + " ---")

                else:
                    print(
                        "FEHLER: P(x0) = P(x1), kann ε nicht eindeutig bestimmen"
                    )
            else:
                print("\n==== ALLGEMEINER KANAL ====")
                print("Allgemeine Kanalmatrix-Bestimmung für n×m Kanäle:")
                print("P(Y) = P(X)ᵀ * P(Y|X)")
                print(
                    "Dieses System ist unterbestimmt - zusätzliche Annahmen erforderlich."
                )
                print("Implementierung für allgemeine Fälle nicht verfügbar.")

        except Exception as e:
            print("Fehler: " + str(e))

        if self.wait_for_continue():
            return


class ChannelTypeAnalysisTool(BaseChannelTool):
    """Tool zur Analyse von Kanaleigenschaften"""

    def run(self):
        print("==== Kanaltyp-Analyse ====")
        try:
            n_inputs = self.safe_int_input("Anzahl Eingänge: ", 2, 10)
            if n_inputs == 'q':
                return

            n_outputs = self.safe_int_input("Anzahl Ausgänge: ", 2, 10)
            if n_outputs == 'q':
                return

            # Kanalmatrix mit Validierung eingeben
            channel_matrix = self.input_channel_matrix_with_validation(
                n_inputs, n_outputs)
            if channel_matrix == 'q':
                return

            print("\n==== KANALMATRIX ====")
            print("     ", end="")
            for j in range(n_outputs):
                print("y" + str(j) + "      ", end="")
            print()

            for i in range(n_inputs):
                print("x" + str(i) + " ", end="")
                for j in range(n_outputs):
                    print(str(round(channel_matrix[i][j], 3)) + "   ", end="")
                print()

            # Kanaleigenschaften analysieren
            print("\n==== KANALEIGENSCHAFTEN-ANALYSE ====")

            # Deterministisch: Jede Zeile hat genau eine 1
            is_deterministic = True
            deterministic_details = []
            for i in range(n_inputs):
                count_ones = 0
                ones_positions = []
                for j in range(n_outputs):
                    if abs(channel_matrix[i][j] - 1.0) < self.tolerance:
                        count_ones += 1
                        ones_positions.append(j)
                deterministic_details.append((count_ones, ones_positions))
                if count_ones != 1:
                    is_deterministic = False

            # Verlustfrei: Jede Spalte hat höchstens eine 1
            is_lossless = True
            lossless_details = []
            for j in range(n_outputs):
                count_ones = 0
                ones_positions = []
                for i in range(n_inputs):
                    if abs(channel_matrix[i][j] - 1.0) < self.tolerance:
                        count_ones += 1
                        ones_positions.append(i)
                lossless_details.append((count_ones, ones_positions))
                if count_ones > 1:
                    is_lossless = False

            # Symmetrisch (für binäre Kanäle)
            is_symmetric = False
            if n_inputs == 2 and n_outputs == 2:
                if (abs(channel_matrix[0][0] - channel_matrix[1][1])
                        < self.tolerance
                        and abs(channel_matrix[0][1] - channel_matrix[1][0])
                        < self.tolerance):
                    is_symmetric = True

            # Vollständig gestört: alle Einträge gleich
            is_completely_disturbed = True
            expected_value = 1.0 / n_outputs
            for i in range(n_inputs):
                for j in range(n_outputs):
                    if abs(channel_matrix[i][j] -
                           expected_value) > self.tolerance:
                        is_completely_disturbed = False
                        break
                if not is_completely_disturbed:
                    break

            # Ergebnisse anzeigen
            print("Deterministisch:           " +
                  ("✓" if is_deterministic else "✗"))
            if not is_deterministic:
                for i in range(len(deterministic_details)):
                    count, positions = deterministic_details[i]
                    if count != 1:
                        print("  Zeile " + str(i) + ": " + str(count) +
                              " Einsen bei " + str(positions))

            print("Verlustfrei (lossless):    " +
                  ("✓" if is_lossless else "✗"))
            if not is_lossless:
                for j in range(len(lossless_details)):
                    count, positions = lossless_details[j]
                    if count > 1:
                        print("  Spalte " + str(j) + ": " + str(count) +
                              " Einsen bei " + str(positions))

            print("Symmetrisch (binär):       " +
                  ("✓" if is_symmetric else "✗"))
            print("Vollständig gestört:       " +
                  ("✓" if is_completely_disturbed else "✗"))
            print("Nicht gestört:             " +
                  ("✓" if (is_deterministic and is_lossless) else "✗"))

            # Zusätzliche Informationen
            print("\n==== INTERPRETATION ====")
            if is_deterministic and is_lossless:
                print(
                    "Perfekter Kanal: Keine Informationsverluste, bijektive Abbildung"
                )
            elif is_deterministic:
                print(
                    "Deterministischer Kanal: Eindeutige Zuordnung, aber möglicherweise nicht umkehrbar"
                )
            elif is_lossless:
                print(
                    "Verlustfreier Kanal: Alle Eingaben am Ausgang unterscheidbar"
                )
            elif is_completely_disturbed:
                print(
                    "Vollständig gestörter Kanal: Keine Information übertragbar"
                )

            if is_symmetric and n_inputs == 2:
                epsilon = channel_matrix[0][1]
                print("Binärer symmetrischer Kanal mit ε = " +
                      str(round(epsilon, 4)))

            # Kanalkapazität für spezielle Fälle
            if is_completely_disturbed:
                print("Kanalkapazität C = 0 (keine Information übertragbar)")
            elif is_deterministic and is_lossless:
                capacity = self.safe_log2(n_inputs)
                print("Kanalkapazität C = log₂(" + str(n_inputs) + ") = " +
                      str(round(capacity, 4)) + " bit/Symbol")

        except Exception as e:
            print("X Fehler: " + str(e))

        if self.wait_for_continue():
            return


class ComprehensiveChannelAnalysisTool(BaseChannelTool):
    """Kompakte Kanalanalyse für Taschenrechner"""

    def run(self):
        print("=== Kanalanalyse ===")
        try:
            # Eingabe der Parameter
            n_inputs = self.safe_int_input("Eingaenge: ", 2, 10)
            if n_inputs == 'q':
                return

            n_outputs = self.safe_int_input("Ausgaenge: ", 2, 10)
            if n_outputs == 'q':
                return

            channel_matrix = self.input_channel_matrix_with_validation(
                n_inputs, n_outputs)
            if channel_matrix == 'q':
                return

            input_probs = self.input_probabilities_with_validation(
                "P(X)", n_inputs)
            if input_probs == 'q':
                return

            # Berechnungen durchführen
            results = self.calculate_all_results(n_inputs, n_outputs,
                                                 channel_matrix, input_probs)
            if results is None:
                return

            # Hauptmenü anzeigen
            self.show_main_menu(results, n_inputs, n_outputs, channel_matrix,
                                input_probs)

        except Exception as e:
            print("Fehler: " + str(e))
            self.wait_for_continue()

    def calculate_all_results(self, n_inputs, n_outputs, channel_matrix,
                              input_probs):
        """Alle Berechnungen durchführen"""
        try:
            # 1. Ausgabewahrscheinlichkeiten
            py = []
            for j in range(n_outputs):
                py_j = 0
                for i in range(n_inputs):
                    py_j += input_probs[i] * channel_matrix[i][j]
                py.append(py_j)

            # Validierung
            py_errors, py_warnings = self.validate_probabilities(py, "P(Y)")
            if py_errors:
                print("FEHLER P(Y):")
                for error in py_errors:
                    print(error)
                self.wait_for_continue()
                return None

            # 2. Entropien
            hx = self.calculate_entropy(input_probs)
            hy = self.calculate_entropy(py)

            # H(Y|X)
            hy_given_x = 0
            for i in range(n_inputs):
                if input_probs[i] > 0:
                    h_y_xi = 0
                    for j in range(n_outputs):
                        if channel_matrix[i][j] > 0:
                            h_y_xi += -channel_matrix[i][j] * self.safe_log2(
                                channel_matrix[i][j])
                    hy_given_x += input_probs[i] * h_y_xi

            hx_given_y = hx - (hy - hy_given_x)
            mutual_info = hy - hy_given_x

            # Plausibilitätsprüfung
            if mutual_info < -self.tolerance:
                print("FEHLER: I(X;Y) < 0!")
                print("I(X;Y) = " + str(round(mutual_info, 6)))
                self.wait_for_continue()
                return None

            # 3. ML-Entscheider
            decoder = {}
            for j in range(n_outputs):
                max_prob = -1
                best_input = -1
                for i in range(n_inputs):
                    prob = channel_matrix[i][j]
                    if prob > max_prob:
                        max_prob = prob
                        best_input = i
                decoder[j] = best_input

            # 4. Fehlerwahrscheinlichkeit
            total_error_prob = 0
            error_details = []
            for i in range(n_inputs):
                for j in range(n_outputs):
                    decision = decoder[j]
                    if decision != i:
                        prob_contribution = input_probs[i] * channel_matrix[i][
                            j]
                        total_error_prob += prob_contribution
                        error_details.append(
                            (i, j, decoder[j], prob_contribution))

            return {
                'py': py,
                'hx': hx,
                'hy': hy,
                'hy_given_x': hy_given_x,
                'hx_given_y': hx_given_y,
                'mutual_info': mutual_info,
                'decoder': decoder,
                'error_prob': total_error_prob,
                'error_details': error_details
            }

        except Exception as e:
            print("Berechnungsfehler: " + str(e))
            return None

    def calculate_entropy(self, probs):
        """Entropie berechnen"""
        h = 0
        for p in probs:
            if p > 0:
                h += -p * self.safe_log2(p)
        return h

    def show_main_menu(self, results, n_inputs, n_outputs, channel_matrix,
                       input_probs):
        """Hauptmenü mit Zusammenfassung"""
        while True:
            print("\n=== ERGEBNISSE ===")
            print("I(X;Y) = " + str(round(results['mutual_info'], 4)) + " bit")
            print("P(Fehler) = " + str(round(results['error_prob'], 4)))

            if results['mutual_info'] > 0 and results['hx'] > 0:
                efficiency = (results['mutual_info'] / results['hx']) * 100
                print("Effizienz = " + str(round(efficiency, 1)) + "%")

            print("\nDetails anzeigen:")
            print("1) P(Y) - Ausgabewahrsch.")
            print("2) Entropien")
            print("3) ML-Entscheider")
            print("4) Fehleranalyse")
            print("5) Uebertragungszeit")
            print("q) Zurueck")

            choice = input("Wahl: ").lower()

            if choice == 'q':
                return
            if choice == '1':
                self.show_output_probabilities(results['py'], n_outputs)
            elif choice == '2':
                self.show_entropies(results)
            elif choice == '3':
                self.show_decoder(results['decoder'], channel_matrix, n_inputs,
                                  n_outputs)
            elif choice == '4':
                self.show_error_analysis(results['error_details'],
                                         results['error_prob'])
            elif choice == '5':
                self.show_transmission_time(results['mutual_info'])

    def show_output_probabilities(self, py, n_outputs):
        """Ausgabewahrscheinlichkeiten anzeigen"""
        print("\n=== P(Y) ===")
        for j in range(n_outputs):
            print("P(y" + str(j) + ") = " + str(round(py[j], 4)))

        print("\nSumme = " + str(round(sum(py), 4)))
        input("Enter...")

    def show_entropies(self, results):
        """Entropien anzeigen"""
        print("\n=== ENTROPIEN ===")
        print("H(X) = " + str(round(results['hx'], 4)) + " bit")
        print("H(Y) = " + str(round(results['hy'], 4)) + " bit")
        print("H(Y|X) = " + str(round(results['hy_given_x'], 4)) + " bit")
        print("H(X|Y) = " + str(round(results['hx_given_y'], 4)) + " bit")
        print("I(X;Y) = " + str(round(results['mutual_info'], 4)) + " bit")
        input("Enter...")

    def show_decoder(self, decoder, channel_matrix, n_inputs, n_outputs):
        """ML-Entscheider anzeigen"""
        print("\n=== ML-ENTSCHEIDER ===")
        for j in range(n_outputs):
            best_input = decoder[j]
            best_prob = channel_matrix[best_input][j]
            print("y" + str(j) + " -> x" + str(best_input) + " (P=" +
                  str(round(best_prob, 3)) + ")")
        input("Enter...")

    def show_error_analysis(self, error_details, total_error_prob):
        """Fehleranalyse anzeigen"""
        print("\n=== FEHLERANALYSE ===")
        print("Gesamt: P(Fehler) = " + str(round(total_error_prob, 4)))

        if len(error_details) > 0:
            print("\nFehlerhafte Pfade:")
            for i, j, decision, prob in error_details:
                if prob > 0.001:  # Nur relevante Fehler anzeigen
                    print("x" + str(i) + "->y" + str(j) + "->x" +
                          str(decision) + ": " + str(round(prob, 4)))
        else:
            print("Keine Fehler!")
        input("Enter...")

    def show_transmission_time(self, mutual_info):
        """Übertragungszeit berechnen"""
        print("\n=== UEBERTRAGUNG ===")

        data_size = self.safe_int_input("Datenmenge (Bit): ", 1, 1000000000)
        if data_size == 'q':
            return

        channel_rate = self.safe_int_input("Kanalrate (bit/s): ", 1,
                                           1000000000)
        if channel_rate == 'q':
            return

        effective_rate = channel_rate * mutual_info
        if effective_rate > 0:
            transmission_time = data_size / effective_rate
            print("\nEffektive Rate:")
            print(
                str(channel_rate) + " x " + str(round(mutual_info, 4)) +
                " = " + str(round(effective_rate, 2)) + " bit/s")
            print("\nZeit: " + str(round(transmission_time, 2)) + " s")

            if transmission_time >= 60:
                minutes = transmission_time / 60
                print("    = " + str(round(minutes, 2)) + " min")
                if minutes >= 60:
                    hours = minutes / 60
                    print("    = " + str(round(hours, 2)) + " h")
        else:
            print("Keine Uebertragung moeglich!")

        input("Enter...")

    def wait_for_continue(self):
        """Warten auf Benutzereingabe"""
        response = input("Enter oder q: ").lower()
        return response == 'q'
