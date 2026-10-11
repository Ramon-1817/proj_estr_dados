# ARQUIVO PRINCIPAL DO PROJETO

import tkinter as tk

# IMPORTAÇÃO DA INTERFACE

from interface.gancho import AppOrdenacaoComGancho

def main():

    janela = tk.Tk()
    AppOrdenacaoComGancho(janela)
    janela.mainloop()

if __name__ == "__main__":
    main()