from typer import Typer, Argument, Option


app = Typer()


@app.command()
def about() -> None:
    print("Krabby is a Python library for text processing.")


@app.command()
def md5sum(
    file: str = Argument(..., help="The file to calculate the MD5 hash of."),
    batch_size: int = Option(1024, help="The batch size to read the file in."),
) -> None:
    from .krabby import md5sum as _md5sum
    print(_md5sum(file, batch_size))


def main() -> None:
    app()


if __name__ == "__main__":
    main()