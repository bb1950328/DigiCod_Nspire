from tool_base import *
import math

class KeyGenerationTool(Tool):
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

    def gcd(self, a, b):
        """Berechnet den größten gemeinsamen Teiler"""
        while b:
            a, b = b, a % b
        return a

    def mod_inverse(self, e, phi):
        """Berechnet das multiplikative Inverse von e modulo phi"""
        # Erweiterter Euklidischer Algorithmus
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            else:
                gcd, x, y = extended_gcd(b % a, a)
                return gcd, y - (b // a) * x, x

        g, x, y = extended_gcd(e, phi)
        if g != 1:
            raise Exception('Modular inverse does not exist')
        else:
            return x % phi

    def generate_keypair(self, p, q):
        """Generiert ein RSA-Schlüsselpaar"""
        # Berechne n = p * q
        n = p * q
        
        # Berechne φ(n) = (p - 1) * (q - 1)
        phi = (p - 1) * (q - 1)
        
        # Wähle e mit 1 < e < φ(n) und ggT(e, φ(n)) = 1
        e = 65537  # Standardwert für e
        
        # Stelle sicher, dass e und phi teilerfremd sind
        if self.gcd(e, phi) != 1:
            raise ValueError("e und φ(n) sind nicht teilerfremd")
        
        # Berechne d mit d * e ≡ 1 (mod φ(n))
        d = self.mod_inverse(e, phi)
        
        # Öffentlicher Schlüssel: (e, n)
        # Privater Schlüssel: (d, n)
        return (e, n), (d, n)

    def run(self) -> None:
        print("==== RSA-Schlüsselpaar erzeugen ====")
        try:
            # Lese Primzahlen p und q ein
            p = int(input("Erste Primzahl p: "))
            if not self.is_prime(p):
                print("Warnung: Die eingegebene Zahl ist keine Primzahl!")
            
            q = int(input("Zweite Primzahl q: "))
            if not self.is_prime(q):
                print("Warnung: Die eingegebene Zahl ist keine Primzahl!")
            
            if p == q:
                print("Warnung: p und q sollten unterschiedliche Primzahlen sein.")
            
            # Generiere das Schlüsselpaar
            public_key, private_key = self.generate_keypair(p, q)
            
            print("\nÖffentlicher Schlüssel (e, n):")
            print("e =", public_key[0])
            print("n =", public_key[1])
            
            print("\nPrivater Schlüssel (d, n):")
            print("d =", private_key[0])
            print("n =", private_key[1])
            
            print("\nSchlüsselparameter:")
            print("p =", p)
            print("q =", q)
            print("φ(n) =", (p-1)*(q-1))
            
        except Exception as e:
            print("Fehler:", str(e))
        
        print("\nDrücke Enter, um fortzufahren...")
        input()


class EncryptionTool(Tool):
    def encrypt(self, message, public_key):
        """Verschlüsselt eine Nachricht mit dem öffentlichen Schlüssel"""
        e, n = public_key
        
        # Konvertiere jeden Buchstaben in eine Zahl und verschlüssele
        encrypted = []
        for char in message:
            # Konvertiere in einen Zahlenwert (ASCII)
            m = ord(char)
            
            # Überprüfe, ob der Wert kleiner als n ist
            if m >= n:
                raise ValueError("Nachricht zu groß für Modul n={}. Zeichen '{}' mit Wert {} überschreitet das Limit.".format(n, char, m))
            
            # Verschlüssele: c = m^e mod n
            c = pow(m, e, n)
            encrypted.append(c)
            
        return encrypted

    def run(self) -> None:
        print("==== RSA-Verschlüsselung ====")
        try:
            message = input("Nachricht zum Verschlüsseln: ")
            
            e = int(input("Öffentlicher Exponent e: "))
            n = int(input("Modul n: "))
            
            public_key = (e, n)
            
            # Verschlüssele die Nachricht
            encrypted = self.encrypt(message, public_key)
            
            print("\nVerschlüsselte Nachricht (als Zahlen):")
            print(encrypted)
            
            print("\nVerschlüsselte Nachricht (durch Kommas getrennt):")
            print(",".join(map(str, encrypted)))
            
        except Exception as e:
            print("Fehler:", str(e))
        
        print("\nDrücke Enter, um fortzufahren...")
        input()


class DecryptionTool(Tool):
    def decrypt(self, encrypted, private_key):
        """Entschlüsselt eine verschlüsselte Nachricht mit dem privaten Schlüssel"""
        d, n = private_key
        
        # Entschlüssele jede Zahl und konvertiere zurück zu einem Zeichen
        decrypted = ""
        for c in encrypted:
            # Entschlüssele: m = c^d mod n
            m = pow(c, d, n)
            
            # Konvertiere zurück zu einem Zeichen
            char = chr(m)
            decrypted += char
            
        return decrypted

    def run(self) -> None:
        print("==== RSA-Entschlüsselung ====")
        try:
            # Lese verschlüsselte Nachricht ein
            encrypted_input = input("Verschlüsselte Nachricht (durch Kommas getrennte Zahlen): ")
            encrypted = list(map(int, encrypted_input.split(",")))
            
            d = int(input("Privater Exponent d: "))
            n = int(input("Modul n: "))
            
            private_key = (d, n)
            
            # Entschlüssele die Nachricht
            decrypted = self.decrypt(encrypted, private_key)
            
            print("\nEntschlüsselte Nachricht:")
            print(decrypted)
            
        except Exception as e:
            print("Fehler:", str(e))
        
        print("\nDrücke Enter, um fortzufahren...")
        input()


def conditional_entropy_yx(pxy, px):
    """
    Berechnet die bedingte Entropie H(Y|X)
    """
    h_yx = 0.0

    # Berechne P(Y|X) aus P(X,Y) und P(X)
    for i in range(len(px)):
        if px[i] == 0:
            continue

        for j in range(len(pxy[i])):
            if pxy[i][j] > 0:
                # P(Y|X) = P(X,Y) / P(X)
                p_y_given_x = pxy[i][j] / px[i]
                h_yx -= pxy[i][j] * math.log2(p_y_given_x)

    return h_yx