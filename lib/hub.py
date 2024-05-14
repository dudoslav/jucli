import click

@click.group()
@click.option(
    "--endpoint",
    "-e",
    help = "Endpoint of JupyterHub",
    type = click.UNPROCESSED,
    callback = validate_url,
    envvar = "JUCLI_ENDPOINT",
)
@click.pass_context
def hub(ctx, **kwargs) -> None:
    """
    Set common options for JupyterHub commands
    """
    ctx.obj["options"] <<= Options(
        **kwargs,
    )


@hub.command()
@click.pass_context
@make_async
async def version(ctx) -> None:
    """
    Print version of JupyterHub instance
    """
    assert_value(ctx.obj["options"].address, "Address must be set")

    async with JupyterHubClient(ctx.obj["options"]) as client:
        click.echo(await client.version())


@hub.command()
@click.pass_context
@make_async
async def info(ctx) -> None:
    """
    Print info of JupyterHub instance
    """
    assert_value(ctx.obj["options"].address, "Address must be set")

    async with JupyterHubClient(ctx.obj["options"]) as client:
        click.echo(await client.info())

@hub.command()
@click.pass_context
@click.argument("user_name")
@click.argument("data", required = False)
@make_async
async def start(ctx, user_name, data) -> None:
    """
    Start JupyterServer on JupyterHub
    """
    async with JupyterHubClient(ctx.obj["options"]) as client:
        await client.start_server(user_name, data)


@hub.command()
@click.argument("user_name")
@click.pass_context
@make_async
async def stop(ctx, user_name) -> None:
    """
    Stop JupyterServer on JupyterHub
    """
    async with JupyterHubClient(ctx.obj["options"]) as client:
        await client.stop_server(user_name)

