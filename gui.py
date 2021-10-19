import tkinter

class OutputTable:
    def __init__(self, root: tkinter.Tk, data: list):
        for i in range(len(data)):
            for j in range(len(data[0])):
                if 0 == j:
                    self.e = tkinter.Entry(root, width=10, 
                                       font=('Arial', '16', 'bold'),
                                       justify='center')

                elif 2 == j or 5 == j:
                    self.e = tkinter.Entry(root, width=8, 
                                       font=('Arial', '16', 'bold'),
                                       justify='center')
                
                else:
                    self.e = tkinter.Entry(root, width=18, 
                                       font=('Arial', '16', 'bold'),
                                       justify='center')

                self.e.grid(row=i, column=j)
                self.e.insert(tkinter.END, data[i][j])

def create_window() -> tkinter.Tk:
    return tkinter.Tk()