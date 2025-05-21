from tool_base import Tool


class BinToDec(Tool):
    def run(self) -> None:
        print("==== Binär zu Dezimal ====")
        bin_str = input("Gib eine Binärzahl ein: ")
        try:
            decimal = int(bin_str, 2)
            print("Dezimal: {}".format(decimal))
        except ValueError:
            print("Ungültige Binärzahl!")
        print("\nDrücke Enter, um fortzufahren...")
        input()


class DecToBin(Tool):
    def run(self) -> None:
        print("==== Dezimal zu Binär ====")
        try:
            decimal = int(input("Gib eine Dezimalzahl ein: "))
            binary = bin(decimal)[2:]  # Remove '0b' prefix
            print("Binär: {}".format(binary))
        except ValueError:
            print("Ungültige Dezimalzahl!")
        print("\nDrücke Enter, um fortzufahren...")
        input()


class HexToBin(Tool):
    def run(self) -> None:
        print("==== Hexadezimal zu Binär ====")
        hex_str = input("Gib eine Hexadezimalzahl ein: ")
        try:
            decimal = int(hex_str, 16)
            binary = bin(decimal)[2:]  # Remove '0b' prefix
            print("Binär: {}".format(binary))
        except ValueError:
            print("Ungültige Hexadezimalzahl!")
        print("\nDrücke Enter, um fortzufahren...")
        input()


class TwosComplementToDecimal(Tool):
    def run(self) -> None:
        print("==== Zweierkomplement zu Dezimal ====")
        bin_str = input("Gib eine Binärzahl im Zweierkomplement ein: ")
        try:
            # Check if the first bit is 1 (negative number)
            if bin_str[0] == '1':
                # Invert all bits
                inverted = ''.join('1' if bit == '0' else '0' for bit in bin_str)
                # Add 1 to get two's complement
                decimal = -1 * (int(inverted, 2) + 1)
            else:
                decimal = int(bin_str, 2)
            print("Dezimal: {}".format(decimal))
        except ValueError:
            print("Ungültige Binärzahl!")
        except IndexError:
            print("Leere Eingabe!")
        print("\nDrücke Enter, um fortzufahren...")
        input()


class DecimalToTwosComplement(Tool):
    def run(self) -> None:
        print("==== Dezimal zu Zweierkomplement ====")
        try:
            decimal = int(input("Gib eine Dezimalzahl ein: "))
            bits = int(input("Gib die Anzahl an Bits ein: "))

            if decimal >= 0:
                # For positive numbers, just convert to binary
                binary = bin(decimal)[2:].zfill(bits)
            else:
                # For negative numbers, calculate two's complement
                # First, get absolute value and convert to binary
                abs_binary = bin(abs(decimal))[2:].zfill(bits)
                # Invert all bits
                inverted = ''.join('1' if bit == '0' else '0' for bit in abs_binary)
                # Add 1 to get two's complement
                binary = bin(int(inverted, 2) + 1)[2:].zfill(bits)

            print("Zweierkomplement ({} Bit): {}".format(bits, binary[-bits:]))
        except ValueError:
            print("Ungültige Eingabe!")
        print("\nDrücke Enter, um fortzufahren...")
        input()


class FloatToBin(Tool):
    def run(self) -> None:
        print("==== Gleitkommazahl zu Binär ====")
        try:
            float_val = float(input("Gib eine Gleitkommazahl ein: "))
            # Simple implementation for binary fraction conversion
            int_part = int(float_val)
            frac_part = float_val - int_part

            # Convert integer part to binary
            int_binary = bin(int_part)[2:]

            # Convert fractional part to binary (limited precision)
            frac_binary = ""
            precision = 10  # Adjust as needed
            for _ in range(precision):
                frac_part *= 2
                bit = int(frac_part)
                frac_binary += str(bit)
                frac_part -= bit
                if frac_part == 0:
                    break

            print("Binär: {}.{}".format(int_binary, frac_binary))
        except ValueError:
            print("Ungültige Eingabe!")
        print("\nDrücke Enter, um fortzufahren...")
        input()


class AnalyzeIEEE754(Tool):
    def run(self) -> None:
        print("==== IEEE-754 Analyse ====")
        try:
            choice = input("Möchtest du (1) eine Dezimalzahl in IEEE-754 umwandeln oder "
                           "(2) eine IEEE-754 Repräsentation analysieren? ")

            if choice == "1":
                float_val = float(input("Gib eine Gleitkommazahl ein: "))
                # Convert to IEEE-754 (32-bit single precision) manually
                ieee_bin = self._float_to_ieee754_bin(float_val)

                sign = ieee_bin[0]
                exponent = ieee_bin[1:9]
                mantissa = ieee_bin[9:]

                print("IEEE-754 (32-bit):")
                print("Sign bit: {}".format(sign))
                print("Exponent: {} (bias 127, value: {})".format(exponent, int(exponent, 2) - 127))
                print("Mantissa: {}".format(mantissa))
                print("Vollständige Repräsentation: {}".format(ieee_bin))

            elif choice == "2":
                ieee_bin = input("Gib die IEEE-754 Binärrepräsentation ein (32 Bit): ").zfill(32)

                if len(ieee_bin) != 32:
                    print("Die Eingabe muss 32 Bit lang sein!")
                else:
                    sign = int(ieee_bin[0])
                    exponent = int(ieee_bin[1:9], 2) - 127
                    mantissa_bits = ieee_bin[9:]

                    # Convert to decimal
                    float_val = self._ieee754_bin_to_float(ieee_bin)

                    print("Sign: {}".format('negativ' if sign else 'positiv'))
                    print("Exponent: {} (unbiased)".format(exponent))
                    print("Mantissa: 1.{}".format(mantissa_bits))
                    print("Dezimalwert: {}".format(float_val))
            else:
                print("Ungültige Auswahl!")

        except ValueError:
            print("Ungültige Eingabe!")
        print("\nDrücke Enter, um fortzufahren...")
        input()

    def _float_to_ieee754_bin(self, f):
        """Convert a float to IEEE-754 binary representation (32-bit)"""
        if f == 0:
            return '0' + '0' * 8 + '0' * 23  # Zero

        # Handle sign
        sign = '1' if f < 0 else '0'
        f = abs(f)

        # Special cases
        if f == float('inf'):
            return sign + '1' * 8 + '0' * 23  # Infinity

        # Convert to binary (separate integer and fraction parts)
        int_part = int(f)
        frac_part = f - int_part

        # Convert integer part to binary
        int_bin = ''
        if int_part == 0:
            int_bin = '0'
        else:
            while int_part > 0:
                int_bin = str(int_part % 2) + int_bin
                int_part //= 2

        # Convert fraction part to binary
        frac_bin = ''
        for _ in range(150):  # Precision limit, should be enough for 32-bit float
            frac_part *= 2
            bit = int(frac_part)
            frac_bin += str(bit)
            frac_part -= bit
            if frac_part == 0:
                break

        # Combine binary parts and normalize
        binary = int_bin + '.' + frac_bin

        # Find leading 1 position to determine exponent
        if int_bin != '0':
            # 1.xxx * 2^exponent
            exponent = len(int_bin) - 1
            normalized = int_bin + frac_bin
            implicit_leading_one = normalized[0]  # This should always be '1'
            significand = (normalized[1:24 + 1] + '0' * 23)[:23]
        else:
            # 0.xxx needs to find first 1
            exponent = 0
            for bit in frac_bin:
                if bit == '1':
                    break
                exponent -= 1

            # Adjust for normalization: 0.00...1xxx -> 1.xxx
            normalized = frac_bin[-exponent:]
            if normalized:  # If we found a '1'
                significand = (normalized[1:24] + '0' * 23)[:23]
            else:  # Very small number, treat as 0
                return sign + '0' * 8 + '0' * 23

        # Add bias to exponent
        biased_exp = exponent + 127

        # Check for subnormal or overflow
        if biased_exp <= 0:  # Subnormal
            return sign + '0' * 8 + '0' * 23  # Simplified to zero
        if biased_exp >= 255:  # Overflow
            return sign + '1' * 8 + '0' * 23  # Infinity

        # Convert exponent to binary
        exp_bin = '0' * (8 - len(bin(biased_exp)[2:])) + bin(biased_exp)[2:]

        # Return IEEE 754 representation
        return sign + exp_bin + significand

    def _ieee754_bin_to_float(self, ieee_bin):
        """Convert IEEE-754 binary representation (32-bit) to float"""
        sign_bit = int(ieee_bin[0])
        exp_bits = ieee_bin[1:9]
        frac_bits = ieee_bin[9:]

        # Parse components
        sign = -1 if sign_bit else 1
        exponent = int(exp_bits, 2)

        # Special cases
        if exponent == 0:
            if int(frac_bits, 2) == 0:
                return 0.0 * sign  # Zero with correct sign
            else:
                # Subnormal number
                fraction = 0.0
                for i, bit in enumerate(frac_bits):
                    if bit == '1':
                        fraction += 2 ** -(i + 1)
                return sign * fraction * (2 ** -126)
        elif exponent == 255:
            if int(frac_bits, 2) == 0:
                return float('inf') * sign  # Infinity
            else:
                return float('nan')  # NaN

        # Normal case
        fraction = 1.0  # Implicit leading 1
        for i, bit in enumerate(frac_bits):
            if bit == '1':
                fraction += 2 ** -(i + 1)

        # Compute final value
        unbiased_exp = exponent - 127
        return sign * fraction * (2 ** unbiased_exp)