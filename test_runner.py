from tests.dynamic.runner import run_suite
import sys

sys.path.append("dlls/")

if __name__ == "__main__":
    from comm import comm

    subclass = comm(0, 1)
    run_suite(subclass)
