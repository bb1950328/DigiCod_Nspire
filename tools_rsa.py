from tool_base import *
import math

class RSA(Tool):
    def __init__(self):
        self.results = {}

    def is_prime(self, n):
        """Einfacher Primzahltest"""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def factorize_n(self, n):
        """Faktorisiert n in p und q (für kleine Zahlen)"""
        for p in range(2, int(math.sqrt(n)) + 1):
            if n % p == 0:
                q = n // p
                if self.is_prime(p) and self.is_prime(q):
                    return p, q
        return None, None

    def extended_gcd_table(self, a, b):
        """
        Erweiterte euklidische Algorithmus mit detaillierter Tabelle
        Gibt Tabelle für Prüfungsdarstellung zurück
        """
        print("\n==== Erweiterter Euklidischer Algorithmus: {} und {} ====".format(a, b))

        # Tabellenkopf
        print("{:<8} {:<8} {:<8} {:<8} {:<8} {:<8}".format('a', 'b', 'q', 'r', 'x', 'y'))
        print("-" * 50)

        # Initialisierung
        table = []
        old_r, r = a, b
        old_s, s = 1, 0
        old_t, t = 0, 1

        # Erste Zeile
        table.append([a, b, 0, a, 1, 0])
        print("{:<8} {:<8} {:<8} {:<8} {:<8} {:<8}".format(a, b, 0, a, 1, 0))

        while r != 0:
            q_val = old_r // r  # q is already used as a variable name for a prime factor
            new_r = old_r - q_val * r
            old_r, r = r, new_r
            new_s = old_s - q_val * s
            old_s, s = s, new_s
            new_t = old_t - q_val * t
            old_t, t = t, new_t

            # Use original r for table display before it's updated
            table.append([old_r, r, q_val, old_r - q_val * r, old_s, old_t]) # r was already new_r here
            print("{:<8} {:<8} {:<8} {:<8} {:<8} {:<8}".format(r if r != new_r else old_r, new_r, q_val, new_r, old_s, old_t))


        gcd = old_r
        x, y = old_s, old_t

        print("\nErgebnis: ggT({}, {}) = {}".format(a, b, gcd))
        print("Koeffizienten: {} * {} + {} * {} = {}".format(a, x, b, y, gcd))
        print("Verifikation: {} * {} + {} * {} = {}".format(a, x, b, y, a * x + b * y))

        # Modulares Inverses falls ggT = 1
        if gcd == 1:
            mod_inv = x % b if x % b >= 0 else (x % b + b) # ensure positive result
            print("Modulares Inverses von {} mod {} = {}".format(a, b, mod_inv))
            print("Verifikation: {} * {} mod {} = {}".format(a, mod_inv, b, (a * mod_inv) % b))
            return gcd, x, y, mod_inv

        return gcd, x, y, None

    def mod_exp_table(self, base, exponent, modulus):
        """
        Modulare Exponentiation mit Zwischenschritten
        """
        print("\n==== Modulare Exponentiation: {}^{} mod {} ====".format(base, exponent, modulus))

        if exponent == 0:
            return 1

        # Binärdarstellung des Exponenten
        binary = bin(exponent)[2:]
        print("Exponent {} in binär: {}".format(exponent, binary))

        result = 1
        base_power = base % modulus

        print("\n{:<4} {:<10} {:<15} {:<15}".format('Bit', 'Potenz', 'Zwischenergebnis', 'Neues Ergebnis'))
        print("-" * 55)

        for i, bit in enumerate(reversed(binary)):
            if bit == '1':
                new_result = (result * base_power) % modulus
                print("{:<4} {}^{:<9} {} * {:<12} {}".format(bit, base, 2 ** i, result, base_power, new_result))
                result = new_result
            else:
                print("{:<4} {}^{:<9} {:<12} {}".format(bit, base, 2 ** i, '(ignoriert)', result))

            if i < len(binary) - 1:
                base_power = (base_power * base_power) % modulus

        print("\nErgebnis: {}^{} mod {} = {}".format(base, exponent, modulus, result))
        return result

    def comprehensive_rsa_analysis(self, **kwargs):
        """
        Umfassende RSA-Analyse basierend auf verfügbaren Parametern

        Mögliche Parameter:
        - p, q: Primzahlen
        - n: Modul (wird faktorisiert wenn p,q fehlen)
        - e: Öffentlicher Exponent
        - d: Privater Exponent
        - phi: Euler-Funktion (wird berechnet wenn nicht gegeben)
        - m: Klartext (zum Verschlüsseln)
        - c: Chiffretext (zum Entschlüsseln)
        """
        print("=" * 60)
        print("UMFASSENDE RSA-ANALYSE")
        print("=" * 60)

        # Parameter extrahieren
        p_param = kwargs.get('p') # Renamed to avoid conflict with loop variable p
        q_param = kwargs.get('q') # Renamed to avoid conflict with loop variable q
        n = kwargs.get('n')
        e = kwargs.get('e')
        d = kwargs.get('d')
        phi = kwargs.get('phi')
        m = kwargs.get('m')
        c = kwargs.get('c')

        print("\n1. GEGEBENE PARAMETER:")
        for param, value in kwargs.items():
            if value is not None:
                print("   {} = {}".format(param, value))

        # Schritt 1: Bestimme p und q
        print("\n2. PRIMZAHLEN p UND q:")
        if p_param is not None and q_param is not None:
            print("   Gegeben: p = {}, q = {}".format(p_param, q_param))
            # Verifikation
            if not self.is_prime(p_param):
                print("   WARNUNG: p = {} ist keine Primzahl!".format(p_param))
            if not self.is_prime(q_param):
                print("   WARNUNG: q = {} ist keine Primzahl!".format(q_param))
        elif n is not None:
            print("   Faktorisierung von n = {}:".format(n))
            p_param, q_param = self.factorize_n(n)
            if p_param and q_param:
                print("   Gefunden: p = {}, q = {}".format(p_param, q_param))
                print("   Verifikation: {} * {} = {}".format(p_param, q_param, p_param * q_param))
            else:
                print("   FEHLER: Konnte n = {} nicht faktorisieren!".format(n))
                return
        else:
            print("   FEHLER: Weder (p,q) noch n gegeben!")
            return

        # Schritt 2: Berechne n
        print("\n3. MODUL n:")
        if n is None:
            n = p_param * q_param
            print("   Berechnet: n = p * q = {} * {} = {}".format(p_param, q_param, n))
        else:
            print("   Gegeben: n = {}".format(n))
            if p_param and q_param and p_param * q_param != n:
                print("   WARNUNG: p * q = {} != n = {}".format(p_param * q_param, n))

        # Schritt 3: Berechne φ(n)
        print("\n4. EULER-FUNKTION φ(n):")
        if phi is None:
            phi = (p_param - 1) * (q_param - 1)
            print("   Berechnet: φ(n) = (p-1) * (q-1) = ({}-1) * ({}-1) = {} * {} = {}".format(p_param, q_param, p_param - 1, q_param - 1, phi))
        else:
            print("   Gegeben: φ(n) = {}".format(phi))
            expected_phi = (p_param - 1) * (q_param - 1)
            if phi != expected_phi:
                print("   WARNUNG: Erwartet φ(n) = {}, aber φ(n) = {} gegeben".format(expected_phi, phi))

        # Schritt 4: Bestimme e und d
        print("\n5. ÖFFENTLICHER UND PRIVATER EXPONENT:")

        if e is not None and d is None:
            print("   Gegeben: e = {}".format(e))
            print("   Berechne d mit erweitertem euklidischem Algorithmus:")

            # Prüfe ob ggT(e, φ(n)) = 1
            gcd_val = math.gcd(e, phi)
            if gcd_val != 1:
                print("   FEHLER: ggT(e, φ(n)) = ggT({}, {}) = {} != 1".format(e, phi, gcd_val))
                print("   e und φ(n) sind nicht teilerfremd!")
                return

            gcd_val, x_val, y_val, d = self.extended_gcd_table(e, phi) # Renamed x, y to avoid conflict

        elif d is not None and e is None:
            print("   Gegeben: d = {}".format(d))
            print("   HINWEIS: e kann nicht eindeutig aus d berechnet werden")
            print("   Standardwert e = 65537 wird angenommen (falls nicht anders spezifiziert)")
            e = 65537
            if math.gcd(e, phi) != 1:
                # Suche ein passendes e
                for test_e in [3, 5, 17, 257, 65537]:
                    if math.gcd(test_e, phi) == 1:
                        e = test_e
                        break
            print("   Verwende: e = {}".format(e))

        elif e is not None and d is not None:
            print("   Gegeben: e = {}, d = {}".format(e, d))
            # Verifikation
            verification = (e * d) % phi
            print("   Verifikation: e * d mod φ(n) = {} * {} mod {} = {}".format(e, d, phi, verification))
            if verification != 1:
                print("   WARNUNG: e * d mod φ(n) = {} != 1".format(verification))

        else:
            print("   Weder e noch d gegeben. Verwende Standard e = 65537")
            e = 65537
            if math.gcd(e, phi) != 1:
                for test_e in [3, 5, 17, 257]:
                    if math.gcd(test_e, phi) == 1:
                        e = test_e
                        break
            print("   Gewählt: e = {}".format(e))
            gcd_val, x_val, y_val, d = self.extended_gcd_table(e, phi) # Renamed x, y

        # Schritt 5: Zusammenfassung der Schlüssel
        print("\n6. SCHLÜSSEL:")
        print("   Öffentlicher Schlüssel:  (e, n) = ({}, {})".format(e, n))
        print("   Privater Schlüssel:      (d, n) = ({}, {})".format(d, n))

        # Schritt 6: Verschlüsselung (falls m gegeben)
        if m is not None:
            print("\n7. VERSCHLÜSSELUNG von m = {}:".format(m))
            if m >= n:
                print("   FEHLER: m = {} >= n = {}".format(m, n))
                print("   Die Nachricht ist zu groß für den Modul!")
            else:
                c_calculated = self.mod_exp_table(m, e, n)
                if c is not None and c != c_calculated:
                    print("   WARNUNG: Berechnetes c = {}, aber c = {} gegeben".format(c_calculated, c))
                c = c_calculated

        # Schritt 7: Entschlüsselung (falls c gegeben)
        if c is not None:
            print("\n8. ENTSCHLÜSSELUNG von c = {}:".format(c))
            m_calculated = self.mod_exp_table(c, d, n)
            if m is not None and m != m_calculated:
                print("   WARNUNG: Berechnetes m = {}, aber m = {} gegeben".format(m_calculated, m))
            m = m_calculated

        # Schritt 8: Vollständige Verifikation
        print("\n9. VOLLSTÄNDIGE VERIFIKATION:")
        if m is not None and c is not None:
            # Ver- und Entschlüsselung testen
            c_verify = pow(m, e, n)
            m_verify = pow(c, d, n)

            print("   Original → Verschlüsselt → Entschlüsselt:")
            print("   {} → {} → {}".format(m, c_verify, m_verify))

            if c_verify == c and m_verify == m:
                print("   ✓ Verifikation erfolgreich!")
            else:
                print("   ✗ Verifikation fehlgeschlagen!")

        # Zusammenfassung aller Ergebnisse
        print("\n10. ZUSAMMENFASSUNG ALLER PARAMETER:")
        print("    p = {}".format(p_param))
        print("    q = {}".format(q_param))
        print("    n = {}".format(n))
        print("    φ(n) = {}".format(phi))
        print("    e = {}".format(e))
        print("    d = {}".format(d))
        if m is not None:
            print("    m = {}".format(m))
        if c is not None:
            print("    c = {}".format(c))

        return {
            'p': p_param, 'q': q_param, 'n': n, 'phi': phi,
            'e': e, 'd': d, 'm': m, 'c': c
        }


    def run(self) -> None:
        """Umfassendes RSA-Menü für Prüfungen"""
        global current_menu
        current_menu = "rsa_comprehensive"

        while current_menu == "rsa_comprehensive":
            print("==== UMFASSENDE RSA-ANALYSE ====")
            print("Gib alle verfügbaren Parameter ein. Alles andere wird berechnet.")
            print()

            rsa = RSA()
            params = {}

            # Parameter einlesen
            print("Parameter eingeben (Enter für 'nicht verfügbar'):")

            # Primzahlen
            p_input = input("Primzahl p: ").strip()
            if p_input:
                params['p'] = int(p_input)

            q_input = input("Primzahl q: ").strip()
            if q_input:
                params['q'] = int(q_input)

            # Modul
            if 'p' not in params or 'q' not in params:
                n_input = input("Modul n: ").strip()
                if n_input:
                    params['n'] = int(n_input)

            # Exponenten
            e_input = input("Öffentlicher Exponent e: ").strip()
            if e_input:
                params['e'] = int(e_input)

            d_input = input("Privater Exponent d: ").strip()
            if d_input:
                params['d'] = int(d_input)

            # Euler-Funktion (normalerweise nicht gegeben, aber möglich)
            phi_input = input("φ(n) (normalerweise leer): ").strip()
            if phi_input:
                params['phi'] = int(phi_input)

            # Nachrichten
            m_input = input("Klartext m (zum Verschlüsseln): ").strip()
            if m_input:
                params['m'] = int(m_input)

            c_input = input("Chiffretext c (zum Entschlüsseln): ").strip()
            if c_input:
                params['c'] = int(c_input)

            # Analyse durchführen
            try:
                results = rsa.comprehensive_rsa_analysis(**params)

                print("\n" + "=" * 60)
                print("ANALYSE ABGESCHLOSSEN")
                print("=" * 60)

            except Exception as e:
                print("\nFEHLER bei der Analyse: {}".format(str(e)))
                import traceback
                traceback.print_exc()

            print("\nOptionen:")
            print("1. Neue Analyse")
            print("2. Nur erweiterten euklidischen Algorithmus")
            print("3. Nur modulare Exponentiation")
            print("0. Zurück zum Hauptmenü")

            choice = input("\nWähle eine Option: ")

            if choice == "1":
                continue
            elif choice == "2":
                try:
                    a_val = int(input("Erste Zahl a: ")) # Renamed a to avoid conflict
                    b_val = int(input("Zweite Zahl b: ")) # Renamed b to avoid conflict
                    rsa.extended_gcd_table(a_val, b_val)
                except Exception as e:
                    print("Fehler: {}".format(e))
                input("\nDrücke Enter zum Fortfahren...")
            elif choice == "3":
                try:
                    base = int(input("Basis: "))
                    exponent = int(input("Exponent: "))
                    modulus = int(input("Modul: "))
                    rsa.mod_exp_table(base, exponent, modulus)
                except Exception as e:
                    print("Fehler: {}".format(e))
                input("\nDrücke Enter zum Fortfahren...")
            elif choice == "0":
                current_menu = "main"