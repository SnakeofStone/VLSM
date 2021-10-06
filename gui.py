import tkinter

class OutputTable:
    def __init__(self, root, data):
        self.window = tkinter.Entry(root)

        for i in range(len(data)):
            for j in range(len(data[0])):
                self.e = tkinter.Entry(root, width=20, 
                                       font=('Arial', '16', 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(tkinter.END, data[i][j])

def create_window() -> tkinter.Tk:
    return tkinter.Tk()