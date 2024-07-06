from classes import database, interface

if __name__ == '__main__':
    db = database.Database()
    gui = interface.ConsoleGUI(db)
    gui.main_menu()