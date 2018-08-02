import gui.app
import papis.database
import click
import papis.cli

@click.command()
@click.help_option('-h', '--help')
@papis.cli.query_option()
def main(query):
    gui.app.Gui(
        documents=papis.database.get().query(query)
    )
