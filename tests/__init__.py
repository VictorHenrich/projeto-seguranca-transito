from typing import Optional
from pathlib import Path
import sys
import src


SRC_PATH: Path = Path(list(src.__path__)[0])


def load_modules(child_path: Optional[Path] = None):
    parent_path: Path = Path(child_path or SRC_PATH)

    if not parent_path.exists():
        return

    sys.path.append(str(parent_path))

    for child_path in Path(parent_path).iterdir():
        if child_path.is_dir():
            load_modules(child_path)

        sys.path.append(str(child_path))

    import src.main


load_modules()
