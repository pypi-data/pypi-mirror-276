#!/usr/bin/python3
from tkinter import *
from tkinter import font
from collections import OrderedDict
# File: PyCount.py
# Mission: Graphically tally categorized clicks.
# Record if [Okay] or [Cancel] was selected.

# Source:
# https://github.com/soft9000/Blog9000

class ClickCounter:
    ''' Tally button clicks. Reset to lask known on error.'''
    def __init__(self, a_counter):
        self.counter = a_counter
        self.label = None
        self.button = None
        self.last = 0

    def on_click(self):
        name = 'Unknown.'
        if self.button:
            name = self.button.cget('text')
        if self.label:
            try:
                self.last = int(self.label.get())
                self.last += 1
            except:
                print('Value Error. [', name, '] ',
                      self.label.get(),
                      f'reset to ({self.last})',
                      file=sys.stderr)
        self.label.delete(0,'end')
        self.label.insert(0, str(self.last))
        

class Counter:
    '''Graphically exchange a dictionary of count-clicks with a user. Dictionary keys match fields requested. Font, size, and label allignment can be selected upon construction as per Tkinter definition.

G.U.I Usage:
===========
from Prompter9000.PyCount import *
params = {"Hits":0, "Miss":0, "Other":10}
Counter.edit(params)

NOTE: Dictionary results will be returned ONLY IF the data was changed. Otherwise an empty dictionary will be returned.

Console Usage:
=============    
python PyCount.py "{'Hits':0, 'Miss':0, 'Other':10}

NOTES: Please encode your dictionary as a single str(dict()) parameter when using the CLI. Results will be returned as a dictionary of strings. A __btn_ok key is added and will be `True` if [Okay] was selected, else is `False` if user pressed [Cancel].
'''
    def __init__(self, a_dict, font_size=16, font_name='TkFixedFont', align='e'):
        '''
        Initialize fileds. Optional horizontal alignments
        are n, s, [e], w ... Tk's `sticky` grid options.
        '''
        self._font_default_size = font_size
        self._font_default_name = font_name
        self._align = align 
        self._data = OrderedDict(a_dict)
        self._dict = OrderedDict()
        self._isOk = None
        self.last_row = None
        self.tk = None

    def _okay(self):
        self._isOk = True
        self.tk.quit()

    def _cancel(self):
        self._isOk = False
        self.tk.quit()

    def as_bool(self, _input:str)->bool:
        ''' Read boolean from the string input.
        Returns True if input is either 'yes', 'true', or '1'
        '''
        if _input:
            _input = _input.lower()
            if  (_input[0] == 'y') or \
                (_input[0] == 't') or \
                (_input[0] == '1'):
                    return True
        return False

    def _convert(self, row, field, value):
        ''' Attempt to convert + assign a string value
            back to a row's input type. Default is to 
            simply assign value as-passed. 
            Return False on error.
        '''
        if not isinstance(row, dict):
            return False
        try:
            target = row[field]
            if isinstance(target, bool):
                row[field] = self.as_bool(value)
            elif isinstance(target, int):
                row[field] = int(value)
            elif isinstance(target, float):
                row[field] = float(value)
            else:
                row[field] = value
            return True
        except:
            return False
        
    @staticmethod
    def begin(fields, title="Counter",
             font_size=16, font_name='TkFixedFont',
             align='e'):
        ''' Create the frame, add the title, as well as the input fields.'''
        self = Counter(fields, font_size, font_name, align)
        self.tk = Tk()

        if title:
            self.tk.title(title)
        self._font_default = font.nametofont(self._font_default_name)
        self._font_default.configure(size=self._font_default_size)
        self._font_default.configure(weight=font.NORMAL)
        self._font_bold = font.nametofont(self._font_default_name)
        self._font_bold.configure(size=self._font_default_size)
        self._font_bold.configure(weight=font.BOLD)

        self.last_row = 0
        # zFields (A Label, plus an Entry, in a grid layout)
        for ref in self._data:
            instance = ClickCounter(self)
            a_prompt = str(ref) + ": "
            obj = Button(master=self.tk,
                        text=a_prompt,
                        font=self._font_bold,
                        command=instance.on_click) # click activation
            obj.grid(row=self.last_row, column=0,
                     padx=4, sticky=self._align)

            instance.button = obj # click identification

            a_value = self._data[ref]
            if not a_value:
                a_value = '0'
            try:
                instance.last = int(a_value) # click reset
            except:
                instance.last = 0 # meh
            obj = Entry(master=self.tk, bd=5,
                        font=self._font_default)
            obj.insert(0, a_value)
            obj.grid(row=self.last_row, column=1)

            instance.label = obj # click identification

            self._dict[ref]=obj
            self.last_row += 1
        return self

    @staticmethod
    def end(prompter):
        ''' Add the closing buttons, center, and pack the Frame.'''
        if prompter.last_row is None:
            return False
        if isinstance(prompter, Counter) is False:
            return False
        # zButtons (A Frame in the grid, plus the properly-centered pair of buttons)
        bottom = Frame(prompter.tk)
        bottom.grid(row=prompter.last_row, columnspan=2)
        btn = Button(bottom, text="Okay",
                     command=prompter._okay,
                     font=prompter._font_bold)
        btn.pack(side=LEFT, pady=12)

        btn = Button(bottom, text="Cancel",
                     command=prompter._cancel,
                     font=prompter._font_bold)
        btn.pack(side=RIGHT, padx=10)

        # zCenter (Close enough to make no odds?)
        width = prompter.tk.winfo_screenwidth()
        height = prompter.tk.winfo_screenheight()
        x = (width - prompter.tk.winfo_reqwidth()) / 2
        y = (height - prompter.tk.winfo_reqheight()) / 2
        prompter.tk.geometry("+%d+%d" % (x, y))
        return True

    def show(self):
        ''' Display the dialog - extract the results.'''
        from collections import OrderedDict
        self.tk.mainloop()
        try:
            if not self._isOk:
                return dict()
            self._data['__conv_ok'] = True # New!
            for tag in self._dict.keys():
                value = (self._dict[tag]).get()
                if not self._convert(self._data, tag, value):
                    self._data['__conv_ok']  = False
                    self._data[tag] = value    # gigo
            return dict(self._data)
        finally:
            try:
                self.tk.destroy()
                # self.tk = None
            except:
                pass

    @staticmethod
    def edit(fields, title="Input",
             font_size=16, font_name='TkFixedFont',
             align='e'):
        ''' Basic mission statement completed. '''
        self = Counter.begin(fields, title,
                              font_size,
                              font_name,
                              align)
        if Counter.end(self) is False:
            raise Exception("AddButtons: Unexpected Error.")
        return self.show()


if __name__ == "__main__":
    import sys
    import os
    cmd_name = sys.argv[0]
    if cmd_name.find('\\'):
        cmd_name = cmd_name.split('\\')[-1]
    if cmd_name.find('/'):
        cmd_name = cmd_name.split('/')[-1]
    
    sz = len(sys.argv)
    params = {"Hits":0, "Miss":0, "Other":10}
    if sz > 2:
        print("Input: One stringified dictionary as a parameter, please.")
        print(f"Example: \"{str(params)}\"")
        print("\t(i.e: surrounding quotations are os-required)")
        quit()
    elif sz == 2:
        data = sys.argv[1:][0]
        params = eval(data)

    results = Counter.edit(params, title=cmd_name)
    if not results:
        params['__btn_ok'] = False
        print(params)
    else:
        results['__btn_ok'] = True
        print(dict(results))
    print()
