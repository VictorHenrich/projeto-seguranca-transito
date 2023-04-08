from typing import Union, Optional
from pathlib import Path
import sys

import src


SRC_PATH: Path = Path(list(src.__path__)[0])


class TestUtil:
    @classmethod
    def load_modules(cls, path: Union[str, Path] = SRC_PATH) -> None:
        parent_path: Path = Path(path)

        if not parent_path.exists():
            return

        sys.path.append(str(parent_path))

        for child_path in Path(parent_path).iterdir():
            if child_path.is_dir():
                cls.load_modules(child_path)

            sys.path.append(str(child_path))
