import typer

default_kwargs = {
    "no_args_is_help": True,
    "add_completion": False,
    "context_settings": {"help_option_names": ["-h", "--help"]},
}


app = typer.Typer(help="ibis-bench", **default_kwargs)


@app.command()
def hello():
    """
    say hello
    """
    print("hello")


@app.command()
def there():
    """
    say there
    """
    print("there")


if __name__ == "__main__":
    typer.run(app)
