from pathlib import Path
import sys
from typing import Optional
import src


def load_modules(p: Optional[Path] = None) -> None:
    path: Path = p or Path(list(src.__path__)[0])

    if not path.exists():
        return

    sys.path.append(str(path))

    if path.is_dir():
        for child_path in path.iterdir():
            if child_path.is_dir():
                load_modules(child_path)

            sys.path.append(str(child_path))


load_modules()

import src.main
