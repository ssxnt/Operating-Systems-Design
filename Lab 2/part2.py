# Lab 2 (part 2)
# student name: Sant Sumetpong
# student number: 24821563

from __future__ import annotations  # helps with type hints
from tkinter import *


# do not import any more modules

# do not change the skeleton of the program. Only add code where it is requested.
class ComplexNumber:

    def __init__(self, real: float, imag: float) -> None:
        self.real = real
        self.imag = imag

    def add(self, new: ComplexNumber) -> ComplexNumber:
        """
           adds this' complex number by new complex number
           returns the result as a complex number (type ComplexNumber)
        """
        a = self.real + new.real
        b = self.imag + new.imag
        return ComplexNumber(a, b)

    def subtract(self, new: ComplexNumber) -> ComplexNumber:
        """
           subtracts this' complex number by new complex number
           returns the result as a complex number (type ComplexNumber)
        """
        a = self.real - new.real
        b = self.imag - new.imag
        return ComplexNumber(a, b)

    def multiply(self, new: ComplexNumber) -> ComplexNumber:
        """
           multiplies this' complex number by new complex number
           returns the result as a complex number (type ComplexNumber)
        """
        a = self.real * new.real - self.imag * new.imag
        b = self.real * new.imag + self.imag * new.real
        return ComplexNumber(a, b)

    def divide(self, new: ComplexNumber) -> ComplexNumber:
        """
           divides 'this' complex number by new complex number
           returns the result as a complex number (type ComplexNumber)
        """
        if not new.real and not new.imag:
            return ComplexNumber(float('NaN'), float('NaN'))
        else:
            denom = new.real ** 2 + new.imag ** 2
            a = (self.real * new.real + self.imag * new.imag) / denom
            b = (self.imag * new.real + self.real * new.imag) / denom
            if a != a or b != b:  # if a or b is NaN, return because NaN cant be converted to int type (I tried it)
                return ComplexNumber(a, b)
            aMantissa = a - int(a)
            bMantissa = b - int(b)
            if not aMantissa or not bMantissa:  # if the mantissa is .0, then just truncate it; else, keep as is
                if not aMantissa and not bMantissa:  # this makes it easier to read (better UI/UX)
                    return ComplexNumber(int(a), int(b))
                elif not aMantissa:
                    return ComplexNumber(int(a), b)
                else:
                    return ComplexNumber(a, int(b))
            return ComplexNumber(a, b)

    def toString(self) -> str:
        """
            returns a string representation of 'this' complex number
        """
        if self.real != self.real and self.imag != self.imag:  # to check manually if number is "NaN"
            return "NaN"
        if not self.real and not self.imag:  # if zero return zero
            return '0'
        if not self.imag:
            return str(self.real)
        elif not self.real:
            if self.imag == 1:  # if 1 or -1 ignore the 1 or -1 before the i
                return 'i'
            elif self.imag == -1:
                return '-i'
            return str(self.imag) + 'i'
        else:
            if self.imag > 0:
                if self.imag == 1:  # check if the complex part is neg or pos and adjust accordingly
                    return str(self.real) + " + i"
                return str(self.real) + " + " + str(self.imag) + 'i'
            else:
                if self.imag == -1:
                    return str(self.real) + " - i"
                return str(self.real) + " - " + str(-self.imag) + 'i'


class GUI:
    """
        this class implements the GUI for our program
        use as is.
        The add, subtract, multiply and divide methods invoke the corresponding
        methods from the ComplexNumber class to calculate the result to display.
    """

    def __init__(self):
        """
            The initializer creates the main window, label and entry widgets,
            and starts the GUI mainloop.
        """
        window = Tk()
        window.title("Complex Numbers")
        window.geometry("250x190")  # arbitrary chosen to make the window bigger

        # Labels and entries for the first complex number
        frame1 = Frame(window)
        frame1.grid(row=1, column=1, pady=10)
        Label(frame1, text="Complex Number 1:").pack(side=LEFT)
        self.com1Re = StringVar()
        Entry(frame1, width=5, textvariable=self.com1Re,
              justify=RIGHT, font=('Calibri 13')).pack(side=LEFT)
        Label(frame1, text="+").pack(side=LEFT)
        self.com1Im = StringVar()
        Entry(frame1, width=5, textvariable=self.com1Im,
              justify=RIGHT, font=('Calibri 13')).pack(side=LEFT)
        Label(frame1, text="i").pack(side=LEFT)

        # Labels and entries for the second complex number
        frame2 = Frame(window)
        frame2.grid(row=3, column=1, pady=10)
        Label(frame2, text="Complex Number 2:").pack(side=LEFT)
        self.com2Re = StringVar()
        Entry(frame2, width=5, textvariable=self.com2Re,
              justify=RIGHT, font=('Calibri 13')).pack(side=LEFT)
        Label(frame2, text="+").pack(side=LEFT)
        self.com2Im = StringVar()
        Entry(frame2, width=5, textvariable=self.com2Im,
              justify=RIGHT, font=('Calibri 13')).pack(side=LEFT)
        Label(frame2, text="i").pack(side=LEFT)

        # Labels and entries for the result complex number
        # an entry widget is used as the output here
        frame3 = Frame(window)
        frame3.grid(row=4, column=1, pady=10)
        Label(frame3, text="Result:     ").pack(side=LEFT)
        self.result = StringVar()
        Entry(frame3, width=10, textvariable=self.result,
              justify=RIGHT, font=('Calibri 13')).pack(side=LEFT)

        # Buttons for add, subtract, multiply and divide
        frame4 = Frame(window)  # Create and add a frame to window
        frame4.grid(row=5, column=1, pady=5, sticky=E)
        Button(frame4, text="Add", command=self.add).pack(
            side=LEFT)
        Button(frame4, text="Subtract",
               command=self.subtract).pack(side=LEFT)
        Button(frame4, text="Multiply",
               command=self.multiply).pack(side=LEFT)
        Button(frame4, text="Divide",
               command=self.divide).pack(side=LEFT)

        mainloop()

    def add(self):
        (com1, com2) = self.getBothComplex()
        result = com1.add(com2)
        self.result.set(result.toString())

    def subtract(self):
        (com1, com2) = self.getBothComplex()
        result = com1.subtract(com2)
        self.result.set(result.toString())

    def multiply(self):
        (com1, com2) = self.getBothComplex()
        result = com1.multiply(com2)
        self.result.set(result.toString())

    def divide(self):
        (com1, com2) = self.getBothComplex()
        result = com1.divide(com2)
        self.result.set(result.toString())

    def getBothComplex(self):
        """ Helper method used by add, subtract, multiply and divide methods """
        try:
            real1 = eval(self.com1Re.get())
            imag1 = eval(self.com1Im.get())
            com1 = ComplexNumber(real1, imag1)

            real2 = eval(self.com2Re.get())
            imag2 = eval(self.com2Im.get())
            com2 = ComplexNumber(real2, imag2)
            return (com1, com2)
        except:
            return (ComplexNumber(float('NaN'), float('NaN')), ComplexNumber(float('NaN'), float('NaN')))
            # if an entry value is missing, cause NaN


if __name__ == "__main__": GUI()