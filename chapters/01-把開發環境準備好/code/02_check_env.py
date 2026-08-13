"""確認程式跑在專案自己的虛擬環境裡，而不是系統的 Python。"""

import sys
from pathlib import Path


def env_info() -> dict[str, str]:
    """回傳目前的 Python 版本與直譯器位置。"""
    return {
        "version": sys.version.split()[0],
        "executable": sys.executable,
        "in_venv": str(Path(sys.executable).parent.parent.name == ".venv"),
    }


if __name__ == "__main__":
    for key, value in env_info().items():
        print(f"{key}: {value}")
