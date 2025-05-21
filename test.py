import sys


def _get_test_functions():
    return [obj for name, obj in globals().items() if callable(obj) and name.startswith("test_")]

def test_a():
    print("test_a")

def test_b():
    print("test_b")


if __name__ == '__main__':
    fail = False
    for func in _get_test_functions():
        try:
            func()
        except Exception as e:
            sys.print_exception(e)
            fail = True
    if fail:
        sys.exit(1)
