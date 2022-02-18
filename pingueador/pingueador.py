import tkinter as tk
from client.gui_app import Frame, barra_menu

def main():
    root = tk.Tk()
    root.title("EL PINGUEADOR 3000 🤖")
    root.iconbitmap("pingueador/img/mira.ico")
    root.resizable(False, False)

    barra_menu(root)

    app = Frame(root = root)
    
    app.mainloop()

if __name__ == '__main__':
    main()
