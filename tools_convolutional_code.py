from tool_base import *


class ConvolutionalEncodeTool(Tool):
    def get_convolution_output(self, input_bits, generator_polynomials, add_tail_bits=True, output_order="g1_first"):
        """
        Berechnet die Ausgabe eines Faltungscodierers

        add_tail_bits: Füge Nullen hinzu um Register zu leeren
        output_order: "g1_first" oder "g2_first" für Ausgabe-Reihenfolge
        """
        # Konvertiere String-Eingabe in Liste von Integers
        if isinstance(input_bits, str):
            input_bits = [int(bit) for bit in input_bits]

        # Konvertiere Generator-Polynome zu Listen von Integers
        g_polys = []
        for poly in generator_polynomials:
            if isinstance(poly, str):
                g_polys.append([int(bit) for bit in poly])
            else:
                g_polys.append(poly)

        # Bestimme das Gedächtnis (maximale Länge - 1)
        max_len = max(len(p) for p in g_polys)
        memory = max_len - 1

        # Füge Tail-Bits hinzu wenn gewünscht
        if add_tail_bits:
            input_sequence = input_bits + [0] * memory
            print("Tail-Bits hinzugefuegt: " + str([0] * memory))
        else:
            input_sequence = input_bits

        # Schieberegister: [s0, s1, s2, ...] wobei s0 das neueste Bit ist
        shift_register = [0] * max_len

        output = []

        print("Debug: Schritt-fuer-Schritt Berechnung")
        print("Generatorpolynome: " + str(g_polys))
        print("Gedaechtnis m = " + str(memory))
        print("")

        for step, input_bit in enumerate(input_sequence):
            # Schiebe alle Bits nach rechts und füge neues Bit links ein
            shift_register = [input_bit] + shift_register[:-1]

            print("Schritt " + str(step + 1) + ": Eingabe=" + str(input_bit))
            print("Schieberegister: " + str(shift_register))

            # Berechne Ausgabe für jedes Generatorpolynom
            step_output = []
            for poly_idx, poly in enumerate(g_polys):
                # XOR aller relevanten Bits
                output_bit = 0
                calculation_parts = []

                for i in range(len(poly)):
                    if poly[i] == 1:  # Nur wenn Polynom-Bit gesetzt ist
                        if i < len(shift_register):
                            output_bit ^= shift_register[i]
                            calculation_parts.append("s" + str(i) + "(" + str(shift_register[i]) + ")")

                step_output.append(output_bit)
                print("g" + str(poly_idx + 1) + " " + str(poly) + ": " +
                      " XOR ".join(calculation_parts) + " = " + str(output_bit))

            # Ausgabe-Reihenfolge bestimmen
            if output_order == "g2_first" and len(step_output) >= 2:
                step_output = [step_output[1], step_output[0]] + step_output[2:]

            output.extend(step_output)
            print("Ausgabe: " + str(step_output))
            print("")

        return output

    def test_known_example(self):
        """Testet mit einem bekannten Beispiel aus der Literatur"""
        print("=== BEKANNTES BEISPIEL ===")
        print("g1 = [1,1,1], g2 = [1,0,1]")
        print("Eingabe: [1,0,1]")

        result = self.get_convolution_output([1, 0, 1], [[1, 1, 1], [1, 0, 1]], add_tail_bits=True)
        print("Ergebnis: " + str(result))
        print("")

    def run(self):
        """Hauptfunktion für die Faltungscodierung"""
        print("==== Codierung mit Faltungscode ====")
        try:
            input_bits = input("Eingabe-Bits: ")
            if not all(bit in '01' for bit in input_bits):
                print("Fehler: Die Eingabe muss binaer sein (nur 0 und 1)")
                input("Enter...")
                return

            n_polys = int(input("Anzahl der Generatorpolynome: "))
            if n_polys <= 0:
                print("Fehler: Anzahl muss positiv sein")
                input("Enter...")
                return

            generator_polynomials = []
            for i in range(n_polys):
                poly = input("Generatorpolynom " + str(i + 1) + " (Bitfolge): ")
                if not all(bit in '01' for bit in poly):
                    print("Fehler: Generatorpolynom muss binaer sein")
                    input("Enter...")
                    return
                generator_polynomials.append(poly)

            # Optionen abfragen
            print("")
            tail_choice = input("Tail-Bits hinzufuegen? (j/n): ")
            add_tail = tail_choice.lower() == 'j' or tail_choice.lower() == 'y'

            order_choice = input("Ausgabe-Reihenfolge (1=g1 zuerst, 2=g2 zuerst): ")
            output_order = "g2_first" if order_choice == "2" else "g1_first"

            print("")
            output = self.get_convolution_output(input_bits, generator_polynomials,
                                                 add_tail_bits=add_tail,
                                                 output_order=output_order)

            # Erstelle die finale Ausgabe
            output_str = ''.join(str(bit) for bit in output)
            print("=== ERGEBNIS ===")
            print("Kodierte Ausgabe: " + output_str)

            # Gruppiere die Ausgabe je nach Anzahl der Polynome
            grouped = []
            for i in range(0, len(output), n_polys):
                group = output_str[i:i + n_polys]
                grouped.append(group)

            print("Gruppiert: " + ' '.join(grouped))

            # Alternative Darstellung
            if n_polys == 2:
                print("")
                print("Alternative Gruppierung:")
                g1_bits = []
                g2_bits = []
                for i in range(0, len(output), 2):
                    if output_order == "g1_first":
                        g1_bits.append(str(output[i]))
                        if i + 1 < len(output):
                            g2_bits.append(str(output[i + 1]))
                    else:
                        g2_bits.append(str(output[i]))
                        if i + 1 < len(output):
                            g1_bits.append(str(output[i + 1]))

                print("g1: " + ''.join(g1_bits))
                print("g2: " + ''.join(g2_bits))

        except Exception as e:
            print("Fehler: " + str(e))

        input("Enter...")


class ViterbiDecodeTool(Tool):
    def viterbi_simplified(self, received_bits, trellis, block_size):
        """
        Vereinfachte Viterbi-Decodierung für einen Faltungscode

        Parameters:
        - received_bits: Liste der empfangenen Bits
        - trellis: Liste von Tupeln (state, (output_bits), next_state)
        - block_size: Anzahl der Ausgangsbits pro Block (typischerweise 2 für Rate 1/2)

        Returns:
        - Decodierte Bitsequenz
        """
        num_states = max(t[0] for t in trellis) + 1  # Anzahl der Zustände im Trellis

        # Initialisiere Pfad-Metriken (akkumulierte Hamming-Distanz)
        path_metrics = [float('inf')] * num_states
        path_metrics[0] = 0  # Starte im Zustand 0

        # Initialisiere Survivor-Pfade
        survivors = [[] for _ in range(num_states)]

        # Gruppiere empfangene Bits in Blöcke
        received_blocks = [received_bits[i:i + block_size] for i in range(0, len(received_bits), block_size)]

        # Durchlaufe jeden Block der empfangenen Bits
        for block in received_blocks:
            new_metrics = [float('inf')] * num_states
            new_survivors = [[] for _ in range(num_states)]

            # Überprüfe alle möglichen Übergänge
            for prev_state, (out0, out1), next_state in trellis:
                output = [out0, out1]  # Ausgabe für diesen Übergang

                # Berechne Hamming-Distanz zwischen Empfangener Ausgabe und Erwartetem
                distance = sum(1 for r, e in zip(block, output) if r != e)

                # Updatee Pfadmetrik für diesen Übergang
                new_path_metric = path_metrics[prev_state] + distance

                # Wenn dieser Pfad besser ist, aktualisiere
                if new_path_metric < new_metrics[next_state]:
                    new_metrics[next_state] = new_path_metric

                    # Bestimme, welches Eingabebit zu diesem Übergang führt
                    input_bit = 1 if (prev_state == 0 and next_state == 1) or (prev_state == 1 and next_state == 1) else 0

                    # Aktualisiere den Survivor-Pfad
                    new_survivors[next_state] = survivors[prev_state] + [input_bit]

            # Aktualisiere Metriken und Survivor-Pfade für den nächsten Durchlauf
            path_metrics = new_metrics
            survivors = new_survivors

        # Wähle den Pfad mit der niedrigsten Metrik
        best_path_idx = path_metrics.index(min(path_metrics))
        return survivors[best_path_idx]

    def run(self) -> None:
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
            if not all(bit in '01' for bit in received_bits):
                print("Fehler: Die empfangenen Bits müssen binär sein (nur 0 und 1 enthalten)")
                print("\nDrücke Enter, um fortzufahren...")
                input()
                return

            # Prüfe, ob die Länge der empfangenen Bits gerade ist (für Block-Größe 2)
            if len(received_bits) % 2 != 0:
                print("Fehler: Die Anzahl der empfangenen Bits muss gerade sein (für Block-Größe 2)")
                print("\nDrücke Enter, um fortzufahren...")
                input()
                return

            # Vereinfachtes Trellis für ein Beispiel
            trellis = [
                (0, (0, 0), 0),  # Von Zustand 0 mit Input 0 -> Zustand 0, Ausgabe 00
                (0, (1, 1), 1),  # Von Zustand 0 mit Input 1 -> Zustand 1, Ausgabe 11
                (1, (1, 0), 0),  # Von Zustand 1 mit Input 0 -> Zustand 0, Ausgabe 10
                (1, (0, 1), 1)  # Von Zustand 1 mit Input 1 -> Zustand 1, Ausgabe 01
            ]

            received_bits_list = [int(bit) for bit in received_bits]
            decoded = self.viterbi_simplified(received_bits_list, trellis, 2)
            print("\nDekodiert: {}".format(''.join(str(bit) for bit in decoded)))
        except Exception as e:
            print("Fehler: {}".format(str(e)))

        print("\nDrücke Enter, um fortzufahren...")
        input()