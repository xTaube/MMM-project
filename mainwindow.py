from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np


def Is_string_ok(s_value_list):
    for s_value in s_value_list:
        dot_c = 0
        if s_value == "":
            return False
        for letter in s_value:
            if letter.isnumeric() or letter == '.':
                if letter == '.':
                    dot_c += 1
                if dot_c > 1:
                    return False
            else:
                return False
    return True


class MainWindow(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)
        loadUi("MMMProjekt.ui", self)

        self.setWindowTitle("MMM projekt")
        self.msg = self.create_msg_box()

        self.draw_plot_button.clicked.connect(self.draw_plot)
        self.R1_value_lineText.textChanged.connect(self.assign_R1_value)
        self.R2_value_lineText.textChanged.connect(self.assign_R2_value)
        self.C1_value_lineText.textChanged.connect(self.assign_C1_value)
        self.C2_value_lineText.textChanged.connect(self.assign_C2_value)
        self.R1_s = ""
        self.R2_s = ""
        self.C1_s = ""
        self.C2_s = ""

        self.Signal_comboBox.currentIndexChanged.connect(self.assign_signal)
        self.Signal = "Unit step"

    def convert_string_to_float(self):
        self.R1 = float(self.R1_s)
        self.R2 = float(self.R2_s)
        self.C1 = float(self.C1_s)
        self.C2 = float(self.C2_s)

    def create_signal(self, N, t, L, T, amp):

        if self.Signal == "Unit step":
            u = np.ones(N)
        elif self.Signal == "Sine":
            u = amp*np.sin(t/L)
        elif self.Signal == "Square":
            u = amp*np.sign(np.sin(2*np.pi * t/(T/L)))
        return u

    def draw_plot(self):
        if Is_string_ok([self.R1_s, self.R2_s, self.C1_s, self.C2_s]):
            try:
                self.convert_string_to_float()

                dt = 0.1
                T = 2*60
                N = int(T*(1/dt))
                t = np.arange(0, T, dt)
                L = 2.5
                amp = 2

                # Wygenerowanie dolnego wykresu(pobudzenie)
                u = self.create_signal(N, t, L, T, amp)
                self.MplWidget2.canvas.axes.clear()
                self.MplWidget2.canvas.axes.set_title("Impulse")
                self.MplWidget2.canvas.axes.plot(t, u)
                self.MplWidget2.canvas.draw()

                x1 = [0.0]
                x2 = [0.0]
                t1 = [0.0]
                for n in range(N):
                    dx1 = (u[n]/(self.C1*self.R1)) - (x1[n]/(self.C1*self.R1)) - (x1[n]/(self.C1*self.R2)) + (x2[n]/(self.C1*self.R2))
                    x1.append(x1[n] + dt*dx1)

                    dx2 = x1[n]/(self.C2*self.R2) - x2[n]/(self.C2*self.R2)
                    x2.append(x2[n] + dt*dx2)

                    t1.append(t[n] + dt)

                self.MplWidget1.canvas.axes.clear()
                self.MplWidget1.canvas.axes.set_title("x1(t), x2(t)")
                self.MplWidget1.canvas.axes.plot(t1, x1, label="x1(t)")
                self.MplWidget1.canvas.axes.plot(t1, x2, '--r', label="x2(t)")
                self.MplWidget1.canvas.axes.legend(loc="upper right", frameon=False)
                self.MplWidget1.canvas.axes.set_ylim([min(x1)*1.2, max(x1)*1.7])
                self.MplWidget1.canvas.draw()
            except:
                self.msg.setText("Invalid values")
                self.msg.show()
        else:
            self.msg.setText("Please pass numeric values for elements")
            self.msg.show()

    def create_msg_box(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Warning")
        msg.setIcon(QMessageBox.Warning)
        return msg

    def assign_R1_value(self):
        self.R1_s = self.R1_value_lineText.text()

    def assign_R2_value(self):
        self.R2_s = self.R2_value_lineText.text()

    def assign_C1_value(self):
        self.C1_s = self.C1_value_lineText.text()

    def assign_C2_value(self):
        self.C2_s = self.C2_value_lineText.text()

    def assign_signal(self):
        self.Signal = self.Signal_comboBox.currentText()
