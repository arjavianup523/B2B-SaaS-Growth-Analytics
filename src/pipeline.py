import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_step(description, command):
    print("\n" + "=" * 60)
    print(description)
    print("=" * 60)

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=False
    )

    if result.returncode != 0:
        print(f"\nFAILED: {description}")
        sys.exit(result.returncode)

    print(f"\nCOMPLETED: {description}")


def main():

    print("=" * 60)
    print("B2B SAAS GROWTH ANALYTICS - AUTOMATED PIPELINE")
    print("=" * 60)

    run_step(
        "STEP 1: GENERATING RAW DATA",
        [sys.executable, "-m", "src.generate_data"]
    )

    run_step(
        "STEP 2: CLEANING DATA",
        [sys.executable, "-m", "src.clean_data"]
    )

    run_step(
        "STEP 3: LOADING DATA INTO MYSQL",
        [sys.executable, "-m", "src.load_database"]
    )

    print("\n" + "=" * 60)
    print("AUTOMATED PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()