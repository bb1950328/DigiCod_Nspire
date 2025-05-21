from tool_base import *


class ConvolutionalEncodeTool(Tool):
    def get_convolution_output(self, input_bits, generator_polynomials):
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

    def run(self) -> None:
        print("==== Codierung mit Faltungscode ====")
        try:
            input_bits = input("Eingabe-Bits: ")
            if not all(bit in '01' for bit in input_bits):
                print("Fehler: Die Eingabe muss binär sein (nur 0 und 1 enthalten)")
                print("\nDrücke Enter, um fortzufahren...")
                input()
                return

            n_polys = int(input("Anzahl der Generatorpolynome: "))
            if n_polys <= 0:
                print("Fehler: Die Anzahl der Polynome muss positiv sein")
                print("\nDrücke Enter, um fortzufahren...")
                input()
                return

            generator_polynomials = []
            for i in range(n_polys):
                poly = input("Generatorpolynom {} (Bitfolge): ".format(i + 1))
                if not all(bit in '01' for bit in poly):
                    print("Fehler: Das Generatorpolynom {} muss binär sein".format(i + 1))
                    print("\nDrücke Enter, um fortzufahren...")
                    input()
                    return
                generator_polynomials.append(poly)

            output = self.get_convolution_output(input_bits, generator_polynomials)
            output_str = ''.join(str(bit) for bit in output)
            print("\nKodierte Ausgabe: {}".format(output_str))

            # Gruppiere die Ausgabe je nach Anzahl der Polynome
            grouped = []
            for i in range(0, len(output), n_polys):
                grouped.append(output_str[i:i + n_polys])

            print("Gruppiert:", ' '.join(grouped))
        except Exception as e:
            print("Fehler: {}".format(str(e)))

        print("\nDrücke Enter, um fortzufahren...")
        input()


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