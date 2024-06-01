import flet as ft

from libresvip.core.compat import as_file
from libresvip.core.constants import res_dir

from .ui import Application


def main() -> None:
    with as_file(res_dir) as assets_dir:
        ft.app(target=Application, assets_dir=assets_dir)


if __name__ == "__main__":
    main()
