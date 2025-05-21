
class Tool(object):
    NAME = "?"

    # abstract
    def run(self) -> None:
        raise NotImplementedError(f"{self.__class__.__name__} must implement run()")

class BaseConversionTool(Tool):
    NAME = "Basisumwandlung"

    def run(self) -> None:
        print("Basisumwandlung....")

TOOLS = [
    BaseConversionTool,
]


def show_tool_menu():
    global tool, tool_num
    for i, tool in enumerate(TOOLS):
        print(f"{i}: {tool.NAME}")
    tool_nr_str = input("Tool: ")
    try:
        return int(tool_nr_str)
    except ValueError:
        return None


if __name__ == '__main__':
    while True:
        tool_num = show_tool_menu()

        if tool_num is not None:
            tool_cls = TOOLS[tool_num]
            tool = tool_cls()
            tool.run()
        else:
            break