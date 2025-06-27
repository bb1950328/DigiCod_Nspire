from tool_base import *
import math

class RSA(Tool):
    def __init__(self):
        self.results = {}

    def gcd(self, a, b):
        """Euklidischer Algorithmus zur Berechnung des größten gemeinsamen Teilers (ggT)"""
        while b:
            a, b = b, a % b
        return abs(a) # ggT ist immer positiv

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
        r_old, r_new = a, b # umbenannt von old_r, r um Klarheit zu schaffen
        s_old, s_new = 1, 0 # umbenannt von old_s, s
        t_old, t_new = 0, 1 # umbenannt von old_t, t

        # Erste Zeile in der Logik, wie sie oft handschriftlich gemacht wird
        # Die "erste" Zeile der Tabelle (a=a, b=b, q=_, r=a, x=1, y=0) und
        # die "zweite" Zeile (a=a, b=b, q=_, r=b, x=0, y=1) sind implizit in den Startwerten

        if b == 0: # Sonderfall, wenn b direkt 0 ist
            print("{:<8} {:<8} {:<8} {:<8} {:<8} {:<8}".format(a, b, '-', a, 1, 0))
            gcd_val = a
            x_val = 1
            y_val = 0
            print("\nErgebnis: ggT({}, {}) = {}".format(a, b, gcd_val))
            print("Koeffizienten: {} * {} + {} * {} = {}".format(a, x_val, b, y_val, gcd_val))
            print("Verifikation: {} * {} + {} * {} = {}".format(a, x_val, b, y_val, a * x_val + b * y_val))
            mod_inv = None
            if gcd_val == 1 and b != 0: # b ist hier 0, also kein mod_inv für b
                 pass # Modulares Inverses nicht sinnvoll hier
            return gcd_val, x_val, y_val, mod_inv

        # Tabelle beginnt mit der ersten Iteration des Algorithmus
        while r_new != 0:
            q_val = r_old // r_new
            r_temp = r_old - q_val * r_new # temporärer neuer Rest
            s_temp = s_old - q_val * s_new # temporärer neuer s
            t_temp = t_old - q_val * t_new # temporärer neuer t

            # Zeile für die Tabelle ausgeben
            # Wir zeigen r_old, r_new, den Quotienten q_val, den Rest r_temp,
            # und die Koeffizienten s_old und t_old, die zu r_old gehören
            print("{:<8} {:<8} {:<8} {:<8} {:<8} {:<8}".format(r_old, r_new, q_val, r_temp, s_old, t_old))
            table.append([r_old, r_new, q_val, r_temp, s_old, t_old])

            r_old, r_new = r_new, r_temp
            s_old, s_new = s_new, s_temp
            t_old, t_new = t_new, t_temp

        # Letzte Zeile mit r_new = 0
        print("{:<8} {:<8} {:<8} {:<8} {:<8} {:<8}".format(r_old, r_new, '-', '-', s_old, t_old))
        table.append([r_old, r_new, '-', '-', s_old, t_old])


        gcd_val = r_old
        x_val = s_old
        y_val = t_old

        print("\nErgebnis: ggT({}, {}) = {}".format(a, b, gcd_val))
        # Die Koeffizienten x und y beziehen sich auf die ursprünglichen a und b:
        # a*x + b*y = ggT(a,b)
        # Im Algorithmus sind das s_old (für a) und t_old (für b), wenn r_old der ggT ist.
        # Es ist wichtig zu beachten, wie x und y in Bezug auf die Eingaben a und b interpretiert werden.
        # In der Standardform des erweiterten Euklidischen Algorithmus sind die finalen s und t die Koeffizienten
        # für die ursprünglichen a und b.
        # Wenn wir `a_orig * x + b_orig * y = gcd` wollen, dann sind `x = s_old` und `y = t_old` (wenn `r_old` der gcd ist).
        # Jedoch, die gebräuchlichere Darstellung ist, dass `x` der Koeffizient von `a` ist.

        # Korrekte Zuordnung der Koeffizienten prüfen:
        # Am Ende gilt: gcd = r_old = a * s_old + b * t_old (wenn b die Rolle des zweiten Parameters übernimmt)
        # oder gcd = r_old = a_orig * x_final + b_orig * y_final
        # Die Variablen 'x' und 'y' aus der Vorlesung sind hier s_old und t_old.

        print("Koeffizienten: {} * {} + {} * {} = {}".format(a, x_val, b, y_val, gcd_val))
        print("Verifikation: {} * {} + {} * {} = {}".format(a, x_val, b, y_val, a * x_val + b * y_val))

        mod_inv = None
        # Modulares Inverses d = e^-1 mod phi  => e*d === 1 (mod phi)
        # Hier suchen wir a^-1 mod b, also x_val mod b.
        if gcd_val == 1:
            mod_inv = x_val % b
            # Sicherstellen, dass das Ergebnis positiv ist, falls b negativ ist oder x_val negativ
            if mod_inv < 0:
                mod_inv += b
            print("Modulares Inverses von {} mod {} = {}".format(a, b, mod_inv))
            print("Verifikation: ({} * {}) mod {} = {}".format(a, mod_inv, b, (a * mod_inv) % b))


        return gcd_val, x_val, y_val, mod_inv


    def mod_exp_table(self, base, exponent, modulus):
        """
        Modulare Exponentiation mit Zwischenschritten (Square-and-Multiply von rechts nach links)
        """
        print("\n==== Modulare Exponentiation: {}^{} mod {} ====".format(base, exponent, modulus))

        if modulus == 1:
            print("\nErgebnis: {}^{} mod {} = 0".format(base, exponent, modulus))
            return 0
        if exponent == 0:
            print("\nErgebnis: {}^{} mod {} = 1".format(base, exponent, modulus))
            return 1

        # Binärdarstellung des Exponenten
        binary_exponent = bin(exponent)[2:]
        print("Exponent {} in binär: {}".format(exponent, binary_exponent))

        result = 1
        # Basis ^ (2^i) mod Modul
        # Wir iterieren durch die Bits des Exponenten von rechts nach links (least significant to most significant)
        print("\n{:<6} | {:<15} | {:<18} | {:<15}".format('Bit (i)', 'Basis^(2^i) mod M', 'Altes Ergebnis * B^{2^i}', 'Neues Ergebnis'))
        print("-" * 65)

        current_power_of_base = base % modulus # Entspricht base^(2^0)

        for i, bit in enumerate(reversed(binary_exponent)):
            op_str = ""
            if bit == '1':
                old_res_for_print = result
                result = (result * current_power_of_base) % modulus
                op_str = "{} * {} = {} ".format(old_res_for_print, current_power_of_base, old_res_for_print * current_power_of_base)
                print("{:<6} | {:<15} | {:<18} | {:<15}".format(
                    str(i) + " (" + bit + ")",
                    current_power_of_base,
                    op_str + "mod {} -> {}".format(modulus, result) if op_str else "(ignoriert)",
                    result
                ))
            else:
                 print("{:<6} | {:<15} | {:<18} | {:<15}".format(
                    str(i) + " (" + bit + ")",
                    current_power_of_base,
                    "(ignoriert)",
                    result
                ))
            # Nächste Potenz der Basis vorbereiten für den nächsten Bit
            if i < len(binary_exponent) - 1: # Nicht für den letzten Schritt
                current_power_of_base = (current_power_of_base * current_power_of_base) % modulus


        print("\nErgebnis: {}^{} mod {} = {}".format(base, exponent, modulus, result))
        return result

    def comprehensive_rsa_analysis(self, **kwargs):
        """
        Umfassende RSA-Analyse basierend auf verfügbaren Parametern
        """
        print("=" * 60)
        print("UMFASSENDE RSA-ANALYSE")
        print("=" * 60)

        p_param = kwargs.get('p')
        q_param = kwargs.get('q')
        n = kwargs.get('n')
        e = kwargs.get('e')
        d = kwargs.get('d')
        phi = kwargs.get('phi')
        m = kwargs.get('m')
        c = kwargs.get('c')

        # Lokale Variablen für berechnete Werte, um None zu vermeiden wenn nicht berechnet
        calculated_p, calculated_q, calculated_n, calculated_phi, calculated_e, calculated_d = None, None, None, None, None, None
        original_m, original_c = m, c # Speichere ursprüngliche m und c Werte

        print("\n1. GEGEBENE PARAMETER:")
        has_params = False
        for param_name, value in kwargs.items():
            if value is not None:
                print("   {} = {}".format(param_name, value))
                has_params = True
        if not has_params:
            print("   Keine Parameter gegeben.")


        print("\n2. PRIMZAHLEN p UND q:")
        if p_param is not None and q_param is not None:
            print("   Gegeben: p = {}, q = {}".format(p_param, q_param))
            if not self.is_prime(p_param): print("   WARNUNG: p = {} ist keine Primzahl!".format(p_param))
            if not self.is_prime(q_param): print("   WARNUNG: q = {} ist keine Primzahl!".format(q_param))
            calculated_p, calculated_q = p_param, q_param
        elif n is not None:
            print("   Faktorisierung von n = {}:".format(n))
            fact_p, fact_q = self.factorize_n(n)
            if fact_p and fact_q:
                print("   Gefunden: p = {}, q = {}".format(fact_p, fact_q))
                print("   Verifikation: {} * {} = {}".format(fact_p, fact_q, fact_p * fact_q))
                calculated_p, calculated_q = fact_p, fact_q
            else:
                print("   FEHLER: Konnte n = {} nicht faktorisieren! Berechnung wird abgebrochen.".format(n))
                return
        else:
            print("   FEHLER: Weder (p,q) noch n gegeben! Berechnung für p,q,n,phi nicht möglich.")
            # Weiter versuchen, falls e,d,c oder m gegeben sind und Aktionen isoliert möglich sind

        if calculated_p and calculated_q:
            print("\n3. MODUL n:")
            if n is None:
                calculated_n = calculated_p * calculated_q
                print("   Berechnet: n = p * q = {} * {} = {}".format(calculated_p, calculated_q, calculated_n))
            else:
                calculated_n = n
                print("   Gegeben: n = {}".format(n))
                if calculated_p * calculated_q != n:
                    print("   WARNUNG: p * q = {} * {} = {} != n = {}".format(calculated_p, calculated_q, calculated_p * calculated_q, n))

            print("\n4. EULER-FUNKTION φ(n):")
            if phi is None:
                calculated_phi = (calculated_p - 1) * (calculated_q - 1)
                print("   Berechnet: φ(n) = (p-1) * (q-1) = ({}-1) * ({}-1) = {} * {} = {}".format(
                    calculated_p, calculated_q, calculated_p - 1, calculated_q - 1, calculated_phi))
            else:
                calculated_phi = phi
                print("   Gegeben: φ(n) = {}".format(phi))
                expected_phi = (calculated_p - 1) * (calculated_q - 1)
                if phi != expected_phi:
                    print("   WARNUNG: Erwartet φ(n) = {}, aber φ(n) = {} gegeben".format(expected_phi, phi))
        else: # Fall, wo p,q nicht bestimmt werden konnten
            if n is not None: calculated_n = n
            if phi is not None: calculated_phi = phi


        print("\n5. ÖFFENTLICHER UND PRIVATER EXPONENT:")
        # Fall 1: e ist gegeben, d soll berechnet werden
        if e is not None and calculated_phi is not None: # d kann nur berechnet werden, wenn phi bekannt ist
            calculated_e = e
            print("   Gegeben: e = {}".format(e))
            if d is None: # d soll berechnet werden
                print("   Berechne d mit erweitertem euklidischem Algorithmus (e * d = 1 mod φ(n)):")
                gcd_val, x_val, _, mod_inv_d = self.extended_gcd_table(e, calculated_phi)
                if gcd_val != 1:
                    print("   FEHLER: ggT(e, φ(n)) = ggT({}, {}) = {} != 1".format(e, calculated_phi, gcd_val))
                    print("   e und φ(n) sind nicht teilerfremd! d kann nicht berechnet werden.")
                elif mod_inv_d is not None:
                    calculated_d = mod_inv_d
                    print("   Berechnet: d = {} (aus e^-1 mod φ(n))".format(calculated_d))
                else:
                    print("   FEHLER: d konnte nicht aus e und φ(n) berechnet werden.")
            else: # d war auch gegeben
                calculated_d = d
                print("   Gegeben: d = {}".format(d))
                # Verifikation wenn beide gegeben
                verification = (calculated_e * calculated_d) % calculated_phi
                print("   Verifikation: e * d mod φ(n) = {} * {} mod {} = {}".format(calculated_e, calculated_d, calculated_phi, verification))
                if verification != 1:
                    print("   WARNUNG: e * d mod φ(n) = {} != 1. Die Schlüssel sind nicht konsistent!".format(verification))

        # Fall 2: d ist gegeben, e soll berechnet werden (oder Standard e)
        elif d is not None and calculated_phi is not None: # e kann nur berechnet werden, wenn phi bekannt ist
            calculated_d = d
            print("   Gegeben: d = {}".format(d))
            if e is None: # e soll berechnet werden
                print("   Berechne e mit erweitertem euklidischem Algorithmus (d * e = 1 mod φ(n)):")
                gcd_val, x_val, _, mod_inv_e = self.extended_gcd_table(d, calculated_phi) # d ist 'a', phi ist 'b'
                if gcd_val != 1:
                    print("   FEHLER: ggT(d, φ(n)) = ggT({}, {}) = {} != 1".format(d, calculated_phi, gcd_val))
                    print("   d und φ(n) sind nicht teilerfremd! e kann nicht berechnet werden.")
                elif mod_inv_e is not None:
                    calculated_e = mod_inv_e
                    print("   Berechnet: e = {} (aus d^-1 mod φ(n))".format(calculated_e))
                else:
                    print("   FEHLER: e konnte nicht aus d und φ(n) berechnet werden.")
            # else: e war auch gegeben, schon oben behandelt

        # Fall 3: Weder e noch d gegeben, aber phi ist bekannt -> wähle Standard e
        elif e is None and d is None and calculated_phi is not None:
            print("   Weder e noch d gegeben. Versuche Standard e = 65537.")
            potential_e = 65537
            if self.gcd(potential_e, calculated_phi) == 1:
                calculated_e = potential_e
                print("   Gewählt: e = {}".format(calculated_e))
                print("   Berechne d mit erweitertem euklidischem Algorithmus (e * d = 1 mod φ(n)):")
                gcd_val, x_val, _, mod_inv_d = self.extended_gcd_table(calculated_e, calculated_phi)
                if gcd_val == 1 and mod_inv_d is not None:
                    calculated_d = mod_inv_d
                    print("   Berechnet: d = {} (aus e^-1 mod φ(n))".format(calculated_d))
                else:
                    print("   FEHLER: Konnte d nicht für e={} und φ(n)={} berechnen.".format(calculated_e, calculated_phi))
            else:
                print("   Standard e = 65537 ist nicht teilerfremd zu φ(n) = {}. Überspringe e,d Berechnung.".format(calculated_phi))
        elif e is not None: # e gegeben, aber phi nicht
            calculated_e = e
            print("   Gegeben: e = {}".format(e))
            if d is not None:
                calculated_d = d
                print("   Gegeben: d = {}".format(d))
                if calculated_phi is None:
                    print("   WARNUNG: φ(n) unbekannt, e*d mod φ(n) kann nicht verifiziert werden.")
            else:
                print("   HINWEIS: d nicht gegeben und φ(n) unbekannt, d kann nicht berechnet werden.")

        elif d is not None: # d gegeben, aber phi nicht
            calculated_d = d
            print("   Gegeben: d = {}".format(d))
            print("   HINWEIS: e nicht gegeben und φ(n) unbekannt, e kann nicht berechnet werden.")


        print("\n6. SCHLÜSSEL:")
        if calculated_e is not None and calculated_n is not None:
            print("   Öffentlicher Schlüssel:  (e, n) = ({}, {})".format(calculated_e, calculated_n))
        else:
            print("   Öffentlicher Schlüssel:  (e, n) = (Unbekannt, {})".format(calculated_n if calculated_n else "Unbekannt"))

        if calculated_d is not None and calculated_n is not None:
            print("   Privater Schlüssel:      (d, n) = ({}, {})".format(calculated_d, calculated_n))
        else:
            print("   Privater Schlüssel:      (d, n) = (Unbekannt, {})".format(calculated_n if calculated_n else "Unbekannt"))


        # Schritt 6: Verschlüsselung (falls m gegeben)
        calculated_c = c # Initialisiere mit gegebenem c (falls vorhanden)
        if original_m is not None: # Verwende original_m für die Entscheidung zur Verschlüsselung
            print("\n7. VERSCHLÜSSELUNG von m = {}:".format(original_m))
            if calculated_e is None or calculated_n is None:
                print("   FEHLER: e oder n sind unbekannt. Verschlüsselung nicht möglich.")
            elif original_m >= calculated_n:
                print("   FEHLER: m = {} >= n = {}. Die Nachricht ist zu groß!".format(original_m, calculated_n))
            else:
                encrypted_val = self.mod_exp_table(original_m, calculated_e, calculated_n)
                print("   Verschlüsselt: c = m^e mod n = {}^{} mod {} = {}".format(original_m, calculated_e, calculated_n, encrypted_val))
                if calculated_c is not None and calculated_c != encrypted_val: # Wenn c auch gegeben war
                    print("   WARNUNG: Berechnetes c = {} unterscheidet sich von gegebenem c = {}".format(encrypted_val, calculated_c))
                calculated_c = encrypted_val # Aktualisiere c mit dem neu berechneten Wert

        # Schritt 7: Entschlüsselung (falls c gegeben)
        calculated_m = m # Initialisiere mit gegebenem m (falls vorhanden)
        # Nutze calculated_c, da dieser Wert ggf. gerade verschlüsselt wurde.
        # Wenn original_c gegeben war und keine Verschlüsselung stattfand, ist calculated_c = original_c
        if calculated_c is not None:
            print("\n8. ENTSCHLÜSSELUNG von c = {}:".format(calculated_c))
            if calculated_d is None or calculated_n is None:
                print("   FEHLER: d oder n sind unbekannt. Entschlüsselung nicht möglich.")
            else:
                decrypted_val = self.mod_exp_table(calculated_c, calculated_d, calculated_n)
                print("   Entschlüsselt: m' = c^d mod n = {}^{} mod {} = {}".format(calculated_c, calculated_d, calculated_n, decrypted_val))
                if original_m is not None and original_m != decrypted_val:
                     print("   WARNUNG: Entschlüsseltes m' = {} unterscheidet sich von ursprünglichem m = {}".format(decrypted_val, original_m))
                calculated_m = decrypted_val # Aktualisiere m mit dem neu berechneten Wert
        elif original_c is not None: # c war ursprünglich gegeben, aber Entschlüsselung nicht möglich
             print("\n8. ENTSCHLÜSSELUNG von c = {}:".format(original_c))
             print("   FEHLER: Entschlüsselung nicht möglich (d oder n fehlen).")


        # Schritt 8: Vollständige Verifikation (nur wenn m und c am Ende Werte haben)
        print("\n9. VOLLSTÄNDIGE VERIFIKATION (falls möglich):")
        if original_m is not None and calculated_e is not None and calculated_d is not None and calculated_n is not None:
            # Ver- und Entschlüsselung testen mit original_m
            c_verify = pow(original_m, calculated_e, calculated_n)
            m_verify = pow(c_verify, calculated_d, calculated_n)

            print("   Original m = {} → Verschlüsselt c' = {} → Entschlüsselt m'' = {}".format(original_m, c_verify, m_verify))

            if m_verify == original_m:
                print("   ✓ Verifikation m -> c' -> m'' erfolgreich!")
            else:
                print("   ✗ Verifikation m -> c' -> m'' fehlgeschlagen!")

            if calculated_c is not None: # Wenn ein c-Wert (gegeben oder berechnet) existiert
                m_verify_from_c = pow(calculated_c, calculated_d, calculated_n)
                print("   Gegebenes/Berechnetes c = {} → Entschlüsselt m''' = {}".format(calculated_c, m_verify_from_c))
                if original_m is not None and m_verify_from_c == original_m:
                    print("   ✓ Entschlüsselung von c zu original m erfolgreich!")
                elif calculated_m is not None and m_verify_from_c == calculated_m and original_m is None: # Kein original_m zum Vergleich
                    print("   ✓ Entschlüsselung von c zu berechnetem m erfolgreich!")
                elif original_m is not None:
                    print("   ✗ Entschlüsselung von c zu original m fehlgeschlagen!")


        # Zusammenfassung aller Ergebnisse
        print("\n10. ZUSAMMENFASSUNG ALLER (potenziell berechneten) PARAMETER:")
        print("    p = {}".format(calculated_p if calculated_p is not None else "Unbekannt/Nicht gegeben"))
        print("    q = {}".format(calculated_q if calculated_q is not None else "Unbekannt/Nicht gegeben"))
        print("    n = {}".format(calculated_n if calculated_n is not None else "Unbekannt/Nicht gegeben"))
        print("    φ(n) = {}".format(calculated_phi if calculated_phi is not None else "Unbekannt/Nicht gegeben"))
        print("    e = {}".format(calculated_e if calculated_e is not None else "Unbekannt/Nicht gegeben"))
        print("    d = {}".format(calculated_d if calculated_d is not None else "Unbekannt/Nicht gegeben"))
        if original_m is not None: # Zeige das ursprüngliche m, falls vorhanden
            print("    Ursprüngliches m = {}".format(original_m))
        if calculated_m is not None and calculated_m != original_m : # Zeige berechnetes m, falls es anders ist oder original_m nicht da war
            print("    Berechnetes/Entschlüsseltes m = {}".format(calculated_m))
        elif calculated_m is not None and original_m is None:
            print("    Entschlüsseltes m = {}".format(calculated_m))

        if original_c is not None:
            print("    Ursprüngliches c = {}".format(original_c))
        if calculated_c is not None and calculated_c != original_c:
            print("    Berechnetes/Verschlüsseltes c = {}".format(calculated_c))
        elif calculated_c is not None and original_c is None:
            print("    Verschlüsseltes c = {}".format(calculated_c))
        input("\nDrücke Enter zum Fortfahren...")

        return {
            'p': calculated_p, 'q': calculated_q, 'n': calculated_n, 'phi': calculated_phi,
            'e': calculated_e, 'd': calculated_d,
            'm_original': original_m, 'c_original': original_c,
            'm_final': calculated_m, 'c_final': calculated_c
        }

    def euler_phi(self, n):
        """
        Berechnet den Wert der Eulerschen Phi-Funktion (Totient-Funktion) für n.
        Die Funktion gibt die Anzahl der Zahlen zurück, die zu n teilerfremd sind und kleiner oder gleich n sind.
        """
        if n <= 0:
            return 0

        if n == 1:
            return 1

        # Berechnung über die Primfaktorzerlegung (effizient)
        result = n

        # Primfaktorzerlegung
        temp_n = n

        # Prüfe auf Teiler 2
        if temp_n % 2 == 0:
            result = result * (1 - 1 / 2)
            while temp_n % 2 == 0:
                temp_n //= 2

        # Prüfe auf ungerade Teiler
        i = 3
        while i * i <= temp_n:
            if temp_n % i == 0:
                result = result * (1 - 1 / i)
                while temp_n % i == 0:
                    temp_n //= i
            i += 2

        # Falls temp_n > 1 ist, dann ist es eine Primzahl
        if temp_n > 1:
            result = result * (1 - 1 / temp_n)

        return int(result)

    def run(self) -> None:
        """Umfassendes RSA-Menü für Prüfungen"""
        global current_menu # Annahme: current_menu ist eine globale Variable für die Menüsteuerung
        current_menu = "rsa_comprehensive"

        while current_menu == "rsa_comprehensive":
            print("\n" + "=" * 30)
            print("UMFASSENDE RSA-ANALYSE")
            print("=" * 30)
            print("Gib alle verfügbaren Parameter ein. Fehlende Werte werden berechnet.")
            print("Lasse Eingaben leer, wenn der Parameter nicht bekannt ist.")
            print()

            # rsa = RSA() # Instanz wird bereits als self übergeben
            params = {}

            # Parameter einlesen
            print("Parameter eingeben (Enter für 'nicht verfügbar'):")

            p_input = input("Primzahl p: ").strip()
            if p_input: params['p'] = int(p_input)

            q_input = input("Primzahl q: ").strip()
            if q_input: params['q'] = int(q_input)

            if 'p' not in params or 'q' not in params: # Nur nach n fragen, wenn p oder q fehlt
                n_input = input("Modul n (Produkt von p und q): ").strip()
                if n_input: params['n'] = int(n_input)

            e_input = input("Öffentlicher Exponent e: ").strip()
            if e_input: params['e'] = int(e_input)

            # Nur nach d fragen, wenn e nicht zur Berechnung von d genutzt werden kann (oder umgekehrt)
            # Oder wenn phi nicht bekannt ist.
            # Besser ist es, immer zu fragen und die Logik in comprehensive_rsa_analysis zu haben.
            d_input = input("Privater Exponent d: ").strip()
            if d_input: params['d'] = int(d_input)

            phi_input = input("φ(n) (Euler'sche Phi-Funktion, (p-1)*(q-1)): ").strip()
            if phi_input: params['phi'] = int(phi_input)

            m_input = input("Klartext m (Zahl zum Verschlüsseln): ").strip()
            if m_input: params['m'] = int(m_input)

            c_input = input("Chiffretext c (Zahl zum Entschlüsseln): ").strip()
            if c_input: params['c'] = int(c_input)

            # Analyse durchführen
            try:
                # self ist die Instanz der RSA-Klasse
                results = self.comprehensive_rsa_analysis(**params)
                print("\n" + "=" * 60)
                print("ANALYSE ABGESCHLOSSEN")
                print("=" * 60)

            except Exception as e:
                print("\nFEHLER bei der Analyse: {}".format(str(e)))
                # In MicroPython ist traceback möglicherweise nicht voll verfügbar
                # import traceback
                # traceback.print_exc() # Kann viel Output erzeugen

            print("\nOptionen:")
            print("1. Neue RSA Analyse")
            print("2. Nur erweiterten euklidischen Algorithmus")
            print("3. Nur modulare Exponentiation")
            print("4. Nur Eulerische Phi-Funktion")
            print("0. Zurück zum Hauptmenü")

            choice = input("Wähle eine Option: ").strip()

            if choice == "1":
                continue
            elif choice == "2":
                try:
                    a_val = int(input("Euklidischer Algorithmus - Erste Zahl a: "))
                    b_val = int(input("Euklidischer Algorithmus - Zweite Zahl b: "))
                    self.extended_gcd_table(a_val, b_val)
                except ValueError:
                    print("Ungültige Eingabe. Bitte Zahlen eingeben.")
                except Exception as e_inner:
                    print("Fehler im Euklid. Alg.: {}".format(e_inner))
                input("\nDrücke Enter zum Fortfahren...")
            elif choice == "3":
                try:
                    base = int(input("Modulare Exponentiation - Basis: "))
                    exponent = int(input("Modulare Exponentiation - Exponent: "))
                    modulus = int(input("Modulare Exponentiation - Modul: "))
                    self.mod_exp_table(base, exponent, modulus)
                except ValueError:
                    print("Ungültige Eingabe. Bitte Zahlen eingeben.")
                except Exception as e_inner:
                    print("Fehler in mod. Exp.: {}".format(e_inner))
                input("\nDrücke Enter zum Fortfahren...")
            elif choice == "4":
                try:
                    n = int(input("n für phi(n) eingeben: "))
                    result = self.euler_phi(n)
                    print(f"φ({n}) = {result}")
                except ValueError:
                    print("Ungültige Eingabe. Bitte eine Zahl eingeben.")
                except Exception as e_inner:
                    print("Fehler in Euler-Phi: {}".format(e_inner))
            elif choice == "0":
                current_menu = "main" # Signalisiert der Hauptschleife (ausserhalb dieser Methode) zu wechseln
                break # Verlässt die while-Schleife dieser Methode
            else:
                print("Ungültige Auswahl.")
                input("\nDrücke Enter zum Fortfahren...")