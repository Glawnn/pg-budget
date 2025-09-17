import subprocess
import sys

PACKAGES = ["pg_budget"]
TESTS = "tests"

BLACK_MAX_LINE_LENGTH = 120
FLAKE8_MAX_LINE_LENGTH = 120

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

def run(cmd):
    """Run a command, stop on error"""
    python_part = cmd[0]
    rest = cmd[1:]

    print(f"{BLUE}{python_part}{RESET} {YELLOW}{' '.join(rest)}{RESET}")

    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f"{RED}Command failed!{RESET}")
        sys.exit(result.returncode)

    print(f"{GREEN}Command succeeded! ✅{RESET}")

def lint():
    print("\n==> Running black (check only)...")
    run([sys.executable, "-m", "black", "--line-length", str(BLACK_MAX_LINE_LENGTH), "--check", *PACKAGES, TESTS])

    print("\n==> Running flake8...")
    run([sys.executable, "-m", "flake8", f"--max-line-length={FLAKE8_MAX_LINE_LENGTH}", *PACKAGES, TESTS])
    
    print("\n==> Running pylint...")
    run([sys.executable, "-m", "pylint", *PACKAGES])

def format():
    print(f"{MAGENTA}\n==> Formatting with black...{RESET}")
    run([sys.executable, "-m", "black", "--line-length", str(BLACK_MAX_LINE_LENGTH),  *PACKAGES, TESTS])

def test_unit():
    print("\n==> Running unit tests ...")
    run([sys.executable, "-m", "pytest", "-k", "unit", TESTS, "-v"])

def test_e2e():
    print("\n==> Running e2e tests...")
    run([sys.executable, "-m", "pytest", "-k", "e2e", TESTS, "-v"])

def test():
    test_unit()
    test_e2e()
