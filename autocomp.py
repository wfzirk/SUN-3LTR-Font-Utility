# https://stackoverflow.com/questions/47839813/python-tkinter-autocomplete-combobox-with-like-search


import tkinter as tk

from csv import reader
from bfConfig import *

class AutoComplete(tk.Frame):

    def __init__(self, master, alias_var, dictList=None):
    
        self.master = master
        self.dictList = dictList
        self.alias_var = alias_var
        self.entry = tk.Entry(self.master, textvariable = self.alias_var, width=32)
        self.entry.pack(expand=True, fill=tk.X )

        self.entry.bind('<KeyRelease>', self.on_keyrelease)
        #self.entry.bind('<Leave>', self.on_keyrelease)      # on mouse leave widget
        self.listbox = tk.Listbox(self.master)   #, width = max_width)
        self.listbox.pack(side=tk.LEFT, expand=True, fill=tk.BOTH )

        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        scrollbar = tk.Scrollbar(self.master)

        scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH)
        
        scrollbar.config(command = self.listbox.yview)
        
        if self.dictList:
            self.listbox_update(self.dictList)
   
    
    def on_keyrelease(self, event):
        
        # get text from entry
        value = event.widget.get()
        value = value.strip().lower()
        
        # get data from list
        if value == '':
            data = self.dictList
        else:
            data = []
            for item in self.dictList:
                if value in item.lower():
                    data.append(item)                

        # update data in listbox
        self.listbox_update(data)
        
        
    def listbox_update(self, data):
        #print('---------data',data)
        # delete previous data
        self.listbox.delete(0, 'end')

        # put new data
        for item in data:
            #print(item)
            self.listbox.insert('end', item)


    def on_select(self, event):
        # display element selected on list
        #print('(event) previous:', event.widget.get('active'))
        #print('(event)  current:', event.widget.get(event.widget.curselection()))
        sel = event.widget.get(event.widget.curselection()).split(' ')[0]
        print('---', sel)
        self.alias_var.set(sel)


if __name__ == "__main__":

    
    test_list = ('apple', 'banana', 'Cranberry', 'dogwood', 'alpha', 'Acorn', 'Anise', 'Strawberry' )

    root = tk.Tk()
    root.width=420
     
    entry = AutoComplete(root)
    entry.width=420
    #entry.grid(row=0, column=0)

    #entry = autocomp(root, test_list)

    root.mainloop()