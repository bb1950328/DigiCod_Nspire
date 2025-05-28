import contextlib
import io
import sys
import traceback

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


def check_interaction(input_file: str, expected_output_file: str):
    try:
        actual_output = io.StringIO()
        sys.stdin = open("interaction/"+input_file, "r")
        with contextlib.redirect_stdout(actual_output):
            menu.select_tool(menu.TOOLS)
    finally:
        sys.stdin.close()
        sys.stdin = sys.__stdin__

    if REGENERATE_REFERENCES:
        with open("interaction/"+expected_output_file, "w") as f:
            f.write(actual_output.getvalue())
    else:
        with open("interaction/"+expected_output_file, "r") as f:
            expected_output = f.read()
        if expected_output != actual_output.getvalue():
            print("=" * 30, "EXPECTED OUTPUT", "=" * 30)
            print(expected_output)
            print("=" * 30, "ACTUAL OUTPUT", "=" * 30)
            print(actual_output.getvalue())
            print("=" * 75)
            raise ValueError("{} + {} Actual output does not match expected output".format(input_file, expected_output_file))


def test_interaction():
    files = [
        ("basic_menu_in.txt", "basic_menu_out.txt")
    ]
    fail = False
    for input_file, expected_output_file in files:
        try:
            check_interaction(input_file, expected_output_file)
        except ValueError as e:
            fail = True
    if fail:
        raise ValueError("some interaction tests failed")


def run_all_tests():
    fail = False
    for func in _get_test_functions():
        # noinspection PyBroadException
        try:
            func()
        except Exception as e:
            print(traceback.format_exc(), file=sys.stderr)
            fail = True
    if fail:
        sys.exit(1)


if __name__ == '__main__':
    run_all_tests()
