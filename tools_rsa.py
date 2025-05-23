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
        print(f"\n==== Erweiterter Euklidischer Algorithmus: {a} und {b} ====")

        # Tabellenkopf
        print(f"{'a':<8} {'b':<8} {'q':<8} {'r':<8} {'x':<8} {'y':<8}")
        print("-" * 50)

        # Initialisierung
        table = []
        old_r, r = a, b
        old_s, s = 1, 0
        old_t, t = 0, 1

        # Erste Zeile
        table.append([a, b, 0, a, 1, 0])
        print(f"{a:<8} {b:<8} {0:<8} {a:<8} {1:<8} {0:<8}")

        while r != 0:
            q = old_r // r
            old_r, r = r, old_r - q * r
            old_s, s = s, old_s - q * s
            old_t, t = t, old_t - q * t

            table.append([old_r, r, q, old_r - q * r, old_s, old_t])
            print(f"{old_r:<8} {r:<8} {q:<8} {old_r - q * r:<8} {old_s:<8} {old_t:<8}")

        gcd = old_r
        x, y = old_s, old_t

        print(f"\nErgebnis: ggT({a}, {b}) = {gcd}")
        print(f"Koeffizienten: {a} * {x} + {b} * {y} = {gcd}")
        print(f"Verifikation: {a} * {x} + {b} * {y} = {a * x + b * y}")

        # Modulares Inverses falls ggT = 1
        if gcd == 1:
            mod_inv = x % b if x % b > 0 else x % b + b
            print(f"Modulares Inverses von {a} mod {b} = {mod_inv}")
            print(f"Verifikation: {a} * {mod_inv} mod {b} = {(a * mod_inv) % b}")
            return gcd, x, y, mod_inv

        return gcd, x, y, None

    def mod_exp_table(self, base, exponent, modulus):
        """
        Modulare Exponentiation mit Zwischenschritten
        """
        print(f"\n==== Modulare Exponentiation: {base}^{exponent} mod {modulus} ====")

        if exponent == 0:
            return 1

        # Binärdarstellung des Exponenten
        binary = bin(exponent)[2:]
        print(f"Exponent {exponent} in binär: {binary}")

        result = 1
        base_power = base % modulus

        print(f"\n{'Bit':<4} {'Potenz':<10} {'Zwischenergebnis':<15} {'Neues Ergebnis':<15}")
        print("-" * 55)

        for i, bit in enumerate(reversed(binary)):
            if bit == '1':
                new_result = (result * base_power) % modulus
                print(f"{bit:<4} {base}^{2 ** i:<9} {result} * {base_power:<12} {new_result}")
                result = new_result
            else:
                print(f"{bit:<4} {base}^{2 ** i:<9} {'(ignoriert)':<12} {result}")

            if i < len(binary) - 1:
                base_power = (base_power * base_power) % modulus

        print(f"\nErgebnis: {base}^{exponent} mod {modulus} = {result}")
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
        p = kwargs.get('p')
        q = kwargs.get('q')
        n = kwargs.get('n')
        e = kwargs.get('e')
        d = kwargs.get('d')
        phi = kwargs.get('phi')
        m = kwargs.get('m')
        c = kwargs.get('c')

        print("\n1. GEGEBENE PARAMETER:")
        for param, value in kwargs.items():
            if value is not None:
                print(f"   {param} = {value}")

        # Schritt 1: Bestimme p und q
        print("\n2. PRIMZAHLEN p UND q:")
        if p is not None and q is not None:
            print(f"   Gegeben: p = {p}, q = {q}")
            # Verifikation
            if not self.is_prime(p):
                print(f"   WARNUNG: p = {p} ist keine Primzahl!")
            if not self.is_prime(q):
                print(f"   WARNUNG: q = {q} ist keine Primzahl!")
        elif n is not None:
            print(f"   Faktorisierung von n = {n}:")
            p, q = self.factorize_n(n)
            if p and q:
                print(f"   Gefunden: p = {p}, q = {q}")
                print(f"   Verifikation: {p} * {q} = {p * q}")
            else:
                print(f"   FEHLER: Konnte n = {n} nicht faktorisieren!")
                return
        else:
            print("   FEHLER: Weder (p,q) noch n gegeben!")
            return

        # Schritt 2: Berechne n
        print("\n3. MODUL n:")
        if n is None:
            n = p * q
            print(f"   Berechnet: n = p * q = {p} * {q} = {n}")
        else:
            print(f"   Gegeben: n = {n}")
            if p and q and p * q != n:
                print(f"   WARNUNG: p * q = {p * q} ≠ n = {n}")

        # Schritt 3: Berechne φ(n)
        print("\n4. EULER-FUNKTION φ(n):")
        if phi is None:
            phi = (p - 1) * (q - 1)
            print(f"   Berechnet: φ(n) = (p-1) * (q-1) = ({p}-1) * ({q}-1) = {p - 1} * {q - 1} = {phi}")
        else:
            print(f"   Gegeben: φ(n) = {phi}")
            expected_phi = (p - 1) * (q - 1)
            if phi != expected_phi:
                print(f"   WARNUNG: Erwartet φ(n) = {expected_phi}, aber φ(n) = {phi} gegeben")

        # Schritt 4: Bestimme e und d
        print("\n5. ÖFFENTLICHER UND PRIVATER EXPONENT:")

        if e is not None and d is None:
            print(f"   Gegeben: e = {e}")
            print(f"   Berechne d mit erweitertem euklidischem Algorithmus:")

            # Prüfe ob ggT(e, φ(n)) = 1
            gcd_val = math.gcd(e, phi)
            if gcd_val != 1:
                print(f"   FEHLER: ggT(e, φ(n)) = ggT({e}, {phi}) = {gcd_val} ≠ 1")
                print(f"   e und φ(n) sind nicht teilerfremd!")
                return

            gcd_val, x, y, d = self.extended_gcd_table(e, phi)

        elif d is not None and e is None:
            print(f"   Gegeben: d = {d}")
            print("   HINWEIS: e kann nicht eindeutig aus d berechnet werden")
            print("   Standardwert e = 65537 wird angenommen (falls nicht anders spezifiziert)")
            e = 65537
            if math.gcd(e, phi) != 1:
                # Suche ein passendes e
                for test_e in [3, 5, 17, 257, 65537]:
                    if math.gcd(test_e, phi) == 1:
                        e = test_e
                        break
            print(f"   Verwende: e = {e}")

        elif e is not None and d is not None:
            print(f"   Gegeben: e = {e}, d = {d}")
            # Verifikation
            verification = (e * d) % phi
            print(f"   Verifikation: e * d mod φ(n) = {e} * {d} mod {phi} = {verification}")
            if verification != 1:
                print(f"   WARNUNG: e * d mod φ(n) = {verification} ≠ 1")

        else:
            print("   Weder e noch d gegeben. Verwende Standard e = 65537")
            e = 65537
            if math.gcd(e, phi) != 1:
                for test_e in [3, 5, 17, 257]:
                    if math.gcd(test_e, phi) == 1:
                        e = test_e
                        break
            print(f"   Gewählt: e = {e}")
            gcd_val, x, y, d = self.extended_gcd_table(e, phi)

        # Schritt 5: Zusammenfassung der Schlüssel
        print("\n6. SCHLÜSSEL:")
        print(f"   Öffentlicher Schlüssel:  (e, n) = ({e}, {n})")
        print(f"   Privater Schlüssel:      (d, n) = ({d}, {n})")

        # Schritt 6: Verschlüsselung (falls m gegeben)
        if m is not None:
            print(f"\n7. VERSCHLÜSSELUNG von m = {m}:")
            if m >= n:
                print(f"   FEHLER: m = {m} ≥ n = {n}")
                print("   Die Nachricht ist zu groß für den Modul!")
            else:
                c_calculated = self.mod_exp_table(m, e, n)
                if c is not None and c != c_calculated:
                    print(f"   WARNUNG: Berechnetes c = {c_calculated}, aber c = {c} gegeben")
                c = c_calculated

        # Schritt 7: Entschlüsselung (falls c gegeben)
        if c is not None:
            print(f"\n8. ENTSCHLÜSSELUNG von c = {c}:")
            m_calculated = self.mod_exp_table(c, d, n)
            if m is not None and m != m_calculated:
                print(f"   WARNUNG: Berechnetes m = {m_calculated}, aber m = {m} gegeben")
            m = m_calculated

        # Schritt 8: Vollständige Verifikation
        print(f"\n9. VOLLSTÄNDIGE VERIFIKATION:")
        if m is not None and c is not None:
            # Ver- und Entschlüsselung testen
            c_verify = pow(m, e, n)
            m_verify = pow(c, d, n)

            print(f"   Original → Verschlüsselt → Entschlüsselt:")
            print(f"   {m} → {c_verify} → {m_verify}")

            if c_verify == c and m_verify == m:
                print("   ✓ Verifikation erfolgreich!")
            else:
                print("   ✗ Verifikation fehlgeschlagen!")

        # Zusammenfassung aller Ergebnisse
        print(f"\n10. ZUSAMMENFASSUNG ALLER PARAMETER:")
        print(f"    p = {p}")
        print(f"    q = {q}")
        print(f"    n = {n}")
        print(f"    φ(n) = {phi}")
        print(f"    e = {e}")
        print(f"    d = {d}")
        if m is not None:
            print(f"    m = {m}")
        if c is not None:
            print(f"    c = {c}")

        return {
            'p': p, 'q': q, 'n': n, 'phi': phi,
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
                print(f"\nFEHLER bei der Analyse: {str(e)}")
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
                    a = int(input("Erste Zahl a: "))
                    b = int(input("Zweite Zahl b: "))
                    rsa.extended_gcd_table(a, b)
                except Exception as e:
                    print(f"Fehler: {e}")
                input("\nDrücke Enter zum Fortfahren...")
            elif choice == "3":
                try:
                    base = int(input("Basis: "))
                    exponent = int(input("Exponent: "))
                    modulus = int(input("Modul: "))
                    rsa.mod_exp_table(base, exponent, modulus)
                except Exception as e:
                    print(f"Fehler: {e}")
                input("\nDrücke Enter zum Fortfahren...")
            elif choice == "0":
                current_menu = "main"