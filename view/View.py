from Tkinter import *

'''
View.
'''
class View():
    
    def __init__(self):
        # root window
        root = Tk()
        Button(root, text="Hello!").pack()
        root.update()
        self.inputs(root)
        root.wait_window(self.top)
    
    def hello(self):
        # create a window.
        root = Tk()
        # create a label that is a child of the root.
        w = Label(root, text="Hello, world!")
        # size label and make visible.
        w.pack()
        # keep window open until exed out.
        root.mainloop()
        
    def inputs(self, parent):
        self.top = Toplevel(parent)

        Label(self.top, text="Value").pack()

        self.e = Entry(self.top)
        self.e.pack(padx=5)

        b = Button(self.top, text="OK", command=self.ok)
        b.pack(pady=5)
        
    def ok(self):

        print "value is", self.e.get()

        self.top.destroy()
        
        
        