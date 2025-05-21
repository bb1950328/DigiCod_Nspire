from tool_base import *


class TransinformationTool(Tool):
    def calculate_transinformation(self, px, pyx):
        """Berechnet die Transinformation eines Kanals"""
        import math

        # Anzahl der Eingangs- und Ausgangssymbole
        n_input = len(px)
        n_output = len(pyx[0])

        # Berechne die Ausgabewahrscheinlichkeiten p(y)
        py = [0] * n_output
        for j in range(n_output):
            for i in range(n_input):
                py[j] += px[i] * pyx[i][j]

        # Berechne die gemeinsame Wahrscheinlichkeit p(x,y)
        pxy = []
        for i in range(n_input):
            row = []
            for j in range(n_output):
                row.append(px[i] * pyx[i][j])
            pxy.append(row)

        # Berechne die Entropien H(X), H(Y) und H(X,Y)
        hx = -sum(p * math.log2(p) if p > 0 else 0 for p in px)
        hy = -sum(p * math.log2(p) if p > 0 else 0 for p in py)

        hxy = 0
        for i in range(n_input):
            for j in range(n_output):
                p = pxy[i][j]
                if p > 0:
                    hxy -= p * math.log2(p)

        # Berechne die Transinformation I(X;Y) = H(X) + H(Y) - H(X,Y)
        transinformation = hx + hy - hxy

        return transinformation

    def run(self) -> None:
        print("==== Transinformation berechnen ====")
        try:
            n_input = int(input("Anzahl der Eingangssymbole: "))
            n_output = int(input("Anzahl der Ausgangssymbole: "))

            print("\nEingabewahrscheinlichkeiten p(x):")
            px = []
            for i in range(n_input):
                p = float(input("p(x{}): ".format(i)))
                px.append(p)

            print("\nKanalmatrix p(y|x):")
            pyx = []
            for i in range(n_input):
                row = []
                print("Für x{}:".format(i))
                for j in range(n_output):
                    p = float(input("p(y{}|x{}): ".format(j, i)))
                    row.append(p)
                pyx.append(row)

            result = self.calculate_transinformation(px, pyx)
            print("\nTransinformation: {:.6f} bits/Symbol".format(result))
        except Exception as e:
            print("Fehler: {}".format(str(e)))

        print("\nDrücke Enter, um fortzufahren...")
        input()


class MaximumLikelihoodTool(Tool):
    def maximum_likelihood(self, channel_matrix):
        """Implementiert die Maximum-Likelihood-Decodierung für einen Kanal"""
        n_input = len(channel_matrix)
        n_output = len(channel_matrix[0])

        # Für jedes Ausgangssymbol bestimme das wahrscheinlichste Eingangssymbol
        decoder = []
        for j in range(n_output):
            max_prob = -1
            best_i = 0
            for i in range(n_input):
                if channel_matrix[i][j] > max_prob:
                    max_prob = channel_matrix[i][j]
                    best_i = i
            decoder.append(best_i)

        return decoder

    def run(self) -> None:
        print("==== Maximum-Likelihood-Decodierung ====")
        try:
            n_input = int(input("Anzahl der Eingangssymbole: "))
            n_output = int(input("Anzahl der Ausgangssymbole: "))

            print("\nKanalmatrix p(y|x):")
            channel_matrix = []
            for i in range(n_input):
                row = []
                print("Für x{}:".format(i))
                for j in range(n_output):
                    p = float(input("p(y{}|x{}): ".format(j, i)))
                    row.append(p)
                channel_matrix.append(row)

            decoder = self.maximum_likelihood(channel_matrix)

            print("\nMaximum-Likelihood-Dekodierung:")
            for j in range(n_output):
                print("y{} → x{}".format(j, decoder[j]))
        except Exception as e:
            print("Fehler: {}".format(str(e)))

        print("\nDrücke Enter, um fortzufahren...")
        input()