import math  # Add this at the top of the file

class Tool(object):
    # abstract
    def run(self) -> None:
        raise NotImplementedError(f"{self.__class__.__name__} must implement run()")

class BaseConversionTool(Tool):

    def run(self) -> None:
        print("Tool Basisumwandlung....")

class EntropyTool(Tool):
    def run(self) -> None:
        print("==== Entropie berechnen ====")
        try:
            n = int(input("Anzahl der Symbole: "))
            probs = []
            for i in range(n):
                p = float(input(f"Wahrscheinlichkeit für Symbol {i + 1}: "))
                probs.append(p)

            result = -sum(p1 * math.log2(p1) for p1 in probs if p1 > 0)
            print(f"\nEntropie: {result:.6f} bits/Symbol")
        except Exception as e:
            print(f"Fehler: {str(e)}")
            
        # Pause functionality from icth_tool.py
        print("\nDrücke Enter, um fortzufahren...")
        input()

class ToolNode(object):
    def __init__(self, nr: int, name: str) -> None:
        self.nr = nr
        self.name = name

class ToolGroup(ToolNode):
    def __init__(self, nr: int, name: str, tools: list[ToolNode]) -> None:
        super().__init__(nr, name)
        self.tools = tools

class ToolEntry(ToolNode):
    def __init__(self, nr: int, name: str, cls) -> None:
        super().__init__(nr, name)
        self.cls = cls

TOOLS = [
    ToolGroup(1, "Informationstheorie", [
        ToolEntry(1, "Entropie berechnen", EntropyTool),
        ToolEntry(2, "Basisumwandlung", BaseConversionTool),
    ]),
]

def find_tool_by_path(path: list[int], tools: list[ToolNode]) -> ToolEntry | ToolGroup | None:
    current_tools = tools
    current = None
    for p in path:
        current = next((t for t in current_tools if t.nr == p), None)
        if current is None:
            return None
        if isinstance(current, ToolGroup):
            current_tools = current.tools
    return current


def select_tool(tools: list[ToolNode]) -> None:
    path: list[int] = []

    while True:
        node = find_tool_by_path(path, tools) if path else None
        current_tools = tools if not path else node.tools if isinstance(node, ToolGroup) else []

        print()
        print("# Hauptmenu" if not path else f"# {'.'.join(map(str, path))} {node.name if node else ''}")
        for t in current_tools:
            print(f"{t.nr} {t.name}")

        input_str = input("Nr: ").strip()

        if input_str == "":
            if path:
                path.pop()  # Go up one level
                continue
            else:
                return  # Exit menu

        try:
            parts = list(map(int, input_str.split(".")))
            full_path = parts if "." in input_str else path + parts

            result = find_tool_by_path(full_path, tools)
            if isinstance(result, ToolEntry):
                print()
                instance = result.cls()
                instance.run()
            elif isinstance(result, ToolGroup):
                path = full_path
            else:
                print("Ungültige Eingabe.")
        except ValueError:
            print("Bitte eine gültige Nummer oder Pfad eingeben (z.B. 1 oder 1.2).")


def main():
    select_tool(TOOLS)

if __name__ == "__main__":
    main()