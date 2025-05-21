class Tool(object):
    # abstract
    def run(self) -> None:
        raise NotImplementedError("{} must implement run()".format(self.__class__.__name__))


class PlaceholderTool(Tool):
    def __init__(self, name):
        self.name = name

    def run(self) -> None:
        print("==== {} ====".format(self.name))
        print("Functionality for {} not yet implemented".format(self.name))
        print("\nDrücke Enter, um fortzufahren...")
        input()

class ToolNode(object):
    def __init__(self, nr: int, name: str) -> None:
        self.nr = nr
        self.name = name

class ToolGroup(ToolNode):
    def __init__(self, nr: int, name: str, tools: list) -> None:
        super().__init__(nr, name)
        self.tools = tools

class ToolEntry(ToolNode):
    def __init__(self, nr: int, name: str, cls) -> None:
        super().__init__(nr, name)
        self.cls = cls
