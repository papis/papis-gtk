import gui.app
import papis.database

def main():
    gui.app.Gui(
        documents=papis.database.get().query_dict(dict(author='einstein'))
    )
