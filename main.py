import math
from tkinter import *

import pystray
from PIL import Image
from pystray import MenuItem as item

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK = 25 * 60
SHORT_BREAK = 5 * 60
LONG_BREAK = 20 * 60
reps = 0
CHECK_MARK = '✔'
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    gui.after_cancel(timer)
    canvas.itemconfig(timer_display, text='00:00')
    global reps
    reps = 0
    title.config(text="Timer")
    checks.config(text='')


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def star_timer():
    global reps
    reps += 1
    if reps == 8:
        count_down(LONG_BREAK)
        title.config(text='Break', fg=RED)
        reps = 0
    elif reps % 2 != 0:
        count_down(WORK)
        title.config(text='Work', fg=GREEN)
    else:
        count_down(SHORT_BREAK)
        title.config(text='Break', fg=PINK)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    count_min = int(count / 60)
    count_sec = int(count % 60)
    canvas.itemconfig(timer_display, text=f"{count_min}:{count_sec:02}")
    if count > 0:
        global timer
        timer = gui.after(1000, count_down, count - 1)
    else:
        canvas.itemconfig(timer_display, text='00:00')
        work_sessions = math.ceil(reps / 2 % 4)
        checks.config(text=work_sessions * CHECK_MARK)
        gui.state(newstate='normal')
        raise_above_all()
        star_timer()


# -------------------------- UI FUNCTIONS ------------------------------ #
def raise_above_all():
    gui.attributes('-topmost', 1)
    gui.attributes('-topmost', 0)


def quit_window():
    icon.stop()
    gui.destroy()


def show_window():
    icon.stop()
    gui.after(0, gui.deiconify())


def hide_window():
    image = Image.open("Resources/depositphotos_188522596-stock-illustration-cooking-timer-mockup-realistic-style.jpg")
    menu = (item("Quit", quit_window), item('Show', show_window))
    icon = pystray.Icon('Pomodoro', image, "Pomodoro", menu)
    icon.run()
    gui.withdraw()


# ---------------------------- UI SETUP ------------------------------- #
gui = Tk()
gui.title("Pomodoro")
gui.config(width=408, height=348, padx=80, pady=30, bg=YELLOW)
gui.protocol('WM_DEL_WINDOW', hide_window)


canvas = Canvas(width=204, height=224, bg=YELLOW, highlightthickness=0)
image = PhotoImage(file="Resources/tomato.png")
canvas.create_image(102, 112, image=image)
timer_display = canvas.create_text(102, 130, text="00:00", font=(FONT_NAME, 36, "bold"), fill="white")

title = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 36, 'bold'), bg=YELLOW, highlightthickness=0)
start_bt = Button(text='Start', bg=GREEN, font=(FONT_NAME, 12, 'bold'), command=star_timer)
reset_bt = Button(text='Reset', bg=RED, font=(FONT_NAME, 12, 'bold'), command=reset_timer)
checks = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 12, 'bold'))

title.grid(column=2, row=1)
canvas.grid(column=2, row=2)
start_bt.grid(column=1, row=3)
reset_bt.grid(column=3, row=3)
checks.grid(column=2, row=4)

gui.mainloop()
