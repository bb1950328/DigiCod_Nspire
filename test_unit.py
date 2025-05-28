import sys

import menu
import tool_base

REGENERATE_REFERENCES = False


def _get_test_functions():
    return [obj for name, obj in globals().items() if callable(obj) and name.startswith("test_")]


def test_a():
    print("test_a")


def test_b():
    print("test_b")


def check_tool_list(tools: list, path: str):
    encountered_nrs = set()
    for to in tools:
        subpath = path + ("." if len(path) > 0 else "") + str(to.nr)
        if to.nr in encountered_nrs:
            raise ValueError("Tool {} \"{}\" has duplicate number {}".format(subpath, to.name, to.nr))
        encountered_nrs.add(to.nr)

        if isinstance(to, tool_base.ToolEntry):
            if not issubclass(to.cls, tool_base.Tool):
                raise ValueError("Tool {} \"{}\" must inherit from tool_base.Tool".format(subpath, to.name))
        elif isinstance(to, tool_base.ToolGroup):
            check_tool_list(to.tools, subpath)


def test_tools():
    check_tool_list(menu.TOOLS, "")


def run_all_tests():
    fail = False
    for func in _get_test_functions():
        # noinspection PyBroadException
        try:
            func()
        except Exception as e:
            sys.print_exception(e)
            fail = True
    if fail:
        sys.exit(1)


if __name__ == '__main__':
    run_all_tests()
