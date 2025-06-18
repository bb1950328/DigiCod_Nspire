from tool_base import Tool


class ProbabilityCalculator(Tool):
    def run(self):
        while True:
            print("=== WAHRSCHEINLICHKEIT ===")
            print("1) Grundlagen")
            print("2) Kombinatorik")
            print("3) Binomial")
            print("4) Lotto")
            print("5) Bitfehler")
            print("6) Würfel/Münze")
            print("7) Urnen")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice == '1':
                BasicProbability().run()
            elif choice == '2':
                Combinatorics().run()
            elif choice == '3':
                BinomialCalculator().run()
            elif choice == '4':
                LottoCalculator().run()
            elif choice == '5':
                BitErrorCalculator().run()
            elif choice == '6':
                DiceCalculator().run()
            elif choice == '7':
                UrnCalculator().run()
            else:
                print("Ungültig!")
            print()


class BasicProbability(Tool):
    def run(self):
        while True:
            print("=== GRUNDLAGEN ===")
            print("1) P(A oder B)")
            print("2) P(A und B)")
            print("3) P(nicht A)")
            print("4) P(A|B)")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice == '1':
                self._or_probability()
            elif choice == '2':
                self._and_probability()
            elif choice == '3':
                self._not_probability()
            elif choice == '4':
                self._conditional_probability()

    def _or_probability(self):
        try:
            print("P(A oder B)")
            p_a = float(input("P(A): "))
            p_b = float(input("P(B): "))

            indep = input("Unabhängig? (j/n): ").strip().lower()

            if indep == 'j':
                p_ab = p_a * p_b
                result = p_a + p_b - p_ab
            else:
                p_ab = float(input("P(A∩B): "))
                result = p_a + p_b - p_ab

            print("P(A∪B) = {:.4f}".format(result))

        except ValueError:
            print("Fehler!")

        input("Enter...")

    def _and_probability(self):
        try:
            print("P(A und B)")
            p_a = float(input("P(A): "))

            indep = input("Unabhängig? (j/n): ").strip().lower()

            if indep == 'j':
                p_b = float(input("P(B): "))
                result = p_a * p_b
            else:
                p_b_given_a = float(input("P(B|A): "))
                result = p_a * p_b_given_a

            print("P(A∩B) = {:.4f}".format(result))

        except ValueError:
            print("Fehler!")

        input("Enter...")

    def _not_probability(self):
        try:
            p_a = float(input("P(A): "))
            result = 1 - p_a
            print("P(Ā) = {:.4f}".format(result))
        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _conditional_probability(self):
        try:
            print("P(A|B)")
            p_ab = float(input("P(A∩B): "))
            p_b = float(input("P(B): "))
            if p_b == 0:
                print("P(B) = 0!")
            else:
                result = p_ab / p_b
                print("P(A|B) = {:.4f}".format(result))
        except ValueError:
            print("Fehler!")
        input("Enter...")


class Combinatorics(Tool):
    def run(self):
        while True:
            print("=== KOMBINATORIK ===")
            print("1) Fakultät n!")
            print("2) 4 Varianten")
            print("3) Kombination C(n,k)")
            print("4) Typ bestimmen")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice == '1':
                self._factorial()
            elif choice == '2':
                self._four_variants()
            elif choice == '3':
                self._combination()
            elif choice == '4':
                self._determine_type()

    def _factorial(self):
        try:
            n = int(input("n: "))
            if n < 0:
                print("n ≥ 0!")
            else:
                result = self._calc_factorial(n)
                print("{}! = {}".format(n, result))
        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _four_variants(self):
        print("=== 4 VARIANTEN ===")
        print("1) Geordnet + Wiederholung")
        print("2) Geordnet + ohne Wdh")
        print("3) Ungeordnet + Wiederholung")
        print("4) Ungeordnet + ohne Wdh")

        var = input("Variante: ").strip()
        if var not in ['1', '2', '3', '4']:
            print("1-4!")
            input("Enter...")
            return

        try:
            n = int(input("n: "))
            k = int(input("k: "))

            if var == '1':
                # n^k
                result = n ** k
                print("N = {}^{} = {}".format(n, k, result))

            elif var == '2':
                # n!/(n-k)!
                if k > n:
                    print("k ≤ n!")
                    input("Enter...")
                    return
                result = self._calc_factorial(n) // self._calc_factorial(n - k)
                print("N = {}!/{}! = {}".format(n, n - k, result))

            elif var == '3':
                # (n+k-1)!/(k!(n-1)!)
                result = (self._calc_factorial(n + k - 1) //
                          (self._calc_factorial(k) * self._calc_factorial(n - 1)))
                print("N = C({},{}) = {}".format(n + k - 1, k, result))

            elif var == '4':
                # C(n,k)
                if k > n:
                    print("k ≤ n!")
                    input("Enter...")
                    return
                result = (self._calc_factorial(n) //
                          (self._calc_factorial(k) * self._calc_factorial(n - k)))
                print("N = C({},{}) = {}".format(n, k, result))

        except ValueError:
            print("Fehler!")

        input("Enter...")

    def _combination(self):
        try:
            n = int(input("n: "))
            k = int(input("k: "))

            if k > n or n < 0 or k < 0:
                print("0 ≤ k ≤ n!")
            else:
                result = self._calc_combination(n, k)
                print("C({},{}) = {}".format(n, k, result))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _determine_type(self):
        try:
            print("Typ bestimmen")
            print("Reihenfolge wichtig? (j/n)")
            ordered = input("> ").strip().lower() == 'j'
            print("Wiederholung möglich? (j/n)")
            replacement = input("> ").strip().lower() == 'j'

            n = int(input("n: "))
            k = int(input("k: "))

            if ordered and replacement:
                result = n ** k
                print("Typ 1: N = {}^{} = {}".format(n, k, result))
            elif ordered and not replacement:
                if k > n:
                    print("k ≤ n!")
                    input("Enter...")
                    return
                result = self._calc_factorial(n) // self._calc_factorial(n - k)
                print("Typ 2: N = {}!/{}! = {}".format(n, n - k, result))
            elif not ordered and replacement:
                result = (self._calc_factorial(n + k - 1) //
                          (self._calc_factorial(k) * self._calc_factorial(n - 1)))
                print("Typ 3: N = C({},{}) = {}".format(n + k - 1, k, result))
            else:
                if k > n:
                    print("k ≤ n!")
                    input("Enter...")
                    return
                result = self._calc_combination(n, k)
                print("Typ 4: N = C({},{}) = {}".format(n, k, result))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _calc_factorial(self, n):
        if n <= 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def _calc_combination(self, n, k):
        if k > n or k < 0:
            return 0
        if k == 0 or k == n:
            return 1
        if k > n - k:
            k = n - k
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        return result


class BinomialCalculator(Tool):
    def run(self):
        while True:
            print("=== BINOMIAL ===")
            print("1) P(X = k)  # Exakt k Erfolge")
            print("2) P(X ≤ k)  # Höchstens k Erfolge")
            print("3) P(X ≥ k) # Mindestens k Erfolge")
            print("4) E(X) & Var(X) # Erwartung & Varianz")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice == '1':
                self._exact_prob()
            elif choice == '2':
                self._cumulative_up()
            elif choice == '3':
                self._cumulative_down()
            elif choice == '4':
                self._expectation()

    def _exact_prob(self):
        try:
            n = int(input("n: "))
            k = int(input("k: "))
            p = float(input("p: "))

            if k > n or n < 0 or k < 0 or p < 0 or p > 1:
                print("Parameter ungültig!")
            else:
                prob = self._binomial_prob(n, k, p)
                print("P(X={}) = {:.6f}".format(k, prob))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _cumulative_up(self):
        try:
            n = int(input("n: "))
            k = int(input("k: "))
            p = float(input("p: "))

            if k > n or n < 0 or k < 0 or p < 0 or p > 1:
                print("Parameter ungültig!")
            else:
                total_prob = 0
                for i in range(k + 1):
                    total_prob += self._binomial_prob(n, i, p)
                print("P(X≤{}) = {:.6f}".format(k, total_prob))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _cumulative_down(self):
        try:
            n = int(input("n: "))
            k = int(input("k: "))
            p = float(input("p: "))

            if k > n or n < 0 or k < 0 or p < 0 or p > 1:
                print("Parameter ungültig!")
            else:
                prob_less = 0
                for i in range(k):
                    prob_less += self._binomial_prob(n, i, p)
                prob = 1 - prob_less
                print("P(X≥{}) = {:.6f}".format(k, prob))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _expectation(self):
        try:
            n = int(input("n: "))
            p = float(input("p: "))

            if n < 0 or p < 0 or p > 1:
                print("Parameter ungültig!")
            else:
                expectation = n * p
                variance = n * p * (1 - p)
                print("E(X) = {:.3f}".format(expectation))
                print("Var(X) = {:.3f}".format(variance))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _binomial_prob(self, n, k, p):
        if k > n or k < 0:
            return 0
        binomial_coeff = self._combination(n, k)
        return binomial_coeff * (p ** k) * ((1 - p) ** (n - k))

    def _combination(self, n, k):
        if k > n or k < 0:
            return 0
        if k == 0 or k == n:
            return 1
        if k > n - k:
            k = n - k
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        return result


class LottoCalculator(Tool):
    def run(self):
        while True:
            print("=== LOTTO ===")
            print("1) 6 aus 49")
            print("2) k aus n")
            print("3) k Richtige")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice == '1':
                self._lotto_6_49()
            elif choice == '2':
                self._custom_lotto()
            elif choice == '3':
                self._k_correct()

    def _lotto_6_49(self):
        total = self._combination(49, 6)
        print("6 aus 49:")
        print("Gesamt: {}".format(total))
        print("6 Richtige: 1:{}".format(total))

        if input("Alle? (a): ") == 'a':
            for k in range(3, 7):
                favorable = self._combination(6, k) * self._combination(43, 6 - k)
                print("{} Richtige: {}:{}".format(k, favorable, total))
        input("Enter...")

    def _custom_lotto(self):
        try:
            n = int(input("n (gesamt): "))
            k = int(input("k (ziehen): "))

            if k > n:
                print("k ≤ n!")
            else:
                total = self._combination(n, k)
                print("Gesamt: {}".format(total))
                print("Alle richtig: 1:{}".format(total))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _k_correct(self):
        try:
            n = int(input("n (gesamt): "))
            k = int(input("k (ziehen): "))
            r = int(input("r (richtige): "))

            if r > k or k > n:
                print("r ≤ k ≤ n!")
            else:
                favorable = self._combination(k, r) * self._combination(n - k, k - r)
                total = self._combination(n, k)
                prob = favorable / total
                print("{} Richtige:".format(r))
                print("P = {:.6f}".format(prob))
                print("1:{:.0f}".format(total / favorable if favorable > 0 else 0))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _combination(self, n, k):
        if k > n or k < 0:
            return 0
        if k == 0 or k == n:
            return 1
        if k > n - k:
            k = n - k
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        return result


class BitErrorCalculator(Tool):
    def run(self):
        while True:
            print("=== BITFEHLER ===")
            print("1) Block fehlerfrei")
            print("2) Max k Fehler")
            print("3) Genau k Fehler")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice == '1':
                self._error_free()
            elif choice == '2':
                self._max_errors()
            elif choice == '3':
                self._exact_errors()

    def _error_free(self):
        try:
            p_error = float(input("Bitfehler-P: "))
            n_bits = int(input("Block-Bits: "))

            prob = (1 - p_error) ** n_bits
            print("P(fehlerfrei) = {:.6f}".format(prob))
            print("P(fehlerhaft) = {:.6f}".format(1 - prob))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _max_errors(self):
        try:
            p_error = float(input("Bitfehler-P: "))
            n_bits = int(input("Block-Bits: "))
            k_max = int(input("Max Fehler: "))

            total_prob = 0
            for k in range(k_max + 1):
                prob_k = self._binomial_prob(n_bits, k, p_error)
                total_prob += prob_k

            print("P(≤{}) = {:.6f}".format(k_max, total_prob))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _exact_errors(self):
        try:
            p_error = float(input("Bitfehler-P: "))
            n_bits = int(input("Block-Bits: "))
            k = int(input("Genau k Fehler: "))

            prob = self._binomial_prob(n_bits, k, p_error)
            print("P({}) = {:.6f}".format(k, prob))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _binomial_prob(self, n, k, p):
        if k > n or k < 0:
            return 0
        binomial_coeff = self._combination(n, k)
        return binomial_coeff * (p ** k) * ((1 - p) ** (n - k))

    def _combination(self, n, k):
        if k > n or k < 0:
            return 0
        if k == 0 or k == n:
            return 1
        if k > n - k:
            k = n - k
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        return result


class DiceCalculator(Tool):
    def run(self):
        while True:
            print("=== WÜRFEL/MÜNZE ===")
            print("1) Münzwurf")
            print("2) Würfel")
            print("3) n Versuche")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice == '1':
                self._coin_flip()
            elif choice == '2':
                self._dice()
            elif choice == '3':
                self._multiple_attempts()

    def _coin_flip(self):
        try:
            n = int(input("Würfe: "))
            k = int(input("Kopf: "))

            prob = self._binomial_prob(n, k, 0.5)
            print("P({} Kopf) = {:.6f}".format(k, prob))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _dice(self):
        try:
            sides = int(input("Seiten: ") or "6")
            target = int(input("Ziel: "))

            if target < 1 or target > sides:
                print("1-{}!".format(sides))
            else:
                prob = 1.0 / sides
                print("P({}) = {:.6f}".format(target, prob))
                print("= 1/{}".format(sides))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _multiple_attempts(self):
        try:
            p_single = float(input("Einzel-P: "))
            n_attempts = int(input("Versuche: "))

            p_all_fail = (1 - p_single) ** n_attempts
            p_at_least_one = 1 - p_all_fail

            print("P(≥1) = {:.6f}".format(p_at_least_one))
            print("P(0) = {:.6f}".format(p_all_fail))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _binomial_prob(self, n, k, p):
        if k > n or k < 0:
            return 0
        binomial_coeff = self._combination(n, k)
        return binomial_coeff * (p ** k) * ((1 - p) ** (n - k))

    def _combination(self, n, k):
        if k > n or k < 0:
            return 0
        if k == 0 or k == n:
            return 1
        if k > n - k:
            k = n - k
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        return result


class UrnCalculator(Tool):
    def run(self):
        while True:
            print("=== URNEN ===")
            print("1) Eine Urne")
            print("2) Zwei Urnen")
            print("3) Ohne Zurücklegen")
            print("q) Zurück")

            choice = input("Wahl: ").strip().lower()
            if choice == 'q':
                break

            if choice == '1':
                self._single_urn()
            elif choice == '2':
                self._two_urns()
            elif choice == '3':
                self._without_replacement()

    def _single_urn(self):
        try:
            total = int(input("Gesamt: "))
            favorable = int(input("Günstige: "))

            if favorable > total:
                print("Günstige ≤ Gesamt!")
            else:
                prob = favorable / total
                print("P = {:.6f}".format(prob))
                print("= {}/{}".format(favorable, total))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _two_urns(self):
        try:
            print("Urne 1:")
            total1 = int(input("Gesamt: "))
            fav1 = int(input("Günstige: "))

            print("Urne 2:")
            total2 = int(input("Gesamt: "))
            fav2 = int(input("Günstige: "))

            p_urn = float(input("P(Urne wählen) [0.5]: ") or "0.5")

            p1 = fav1 / total1
            p2 = fav2 / total2
            total_prob = p_urn * p1 + (1 - p_urn) * p2

            print("P(günstig) = {:.6f}".format(total_prob))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _without_replacement(self):
        try:
            total = int(input("Gesamt: "))
            favorable = int(input("Günstige: "))
            draws = int(input("Ziehungen: "))
            successes = int(input("Erfolge: "))

            # Hypergeometrisch
            prob = self._hypergeometric_prob(total, favorable, draws, successes)
            print("P({} Erfolge) = {:.6f}".format(successes, prob))

        except ValueError:
            print("Fehler!")
        input("Enter...")

    def _hypergeometric_prob(self, N, K, n, k):
        if k > K or k > n or (n - k) > (N - K):
            return 0

        numerator = self._combination(K, k) * self._combination(N - K, n - k)
        denominator = self._combination(N, n)

        if denominator == 0:
            return 0

        return numerator / denominator

    def _combination(self, n, k):
        if k > n or k < 0:
            return 0
        if k == 0 or k == n:
            return 1
        if k > n - k:
            k = n - k
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        return result
