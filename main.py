import tkinter as tk
import random
from tkinter import StringVar, END

# Basic UI
window = tk.Tk()
window.geometry('750x450')
window.title('Typing Speed Test')
window.minsize(750, 450)
window.maxsize(750, 450)

start_label = tk.Label(text='Test Instructions', font=('Times New Roman', 20, 'bold', 'underline'))
instructions = tk.Label(
    text='This is a test of your typing speed. Once you press start, you will be directed to a new page.'
         '\nYou will see a paragraph that you will need to type out in the entry box below.'
         '\nOnly when the entry box is pressed will the timer of 60 seconds begin.'
         '\nType one word at a time, and press the spacebar to submit the word.'
         '\nThe entry box will clear automatically for you to type the next word.'
         '\nYou can track the letters you typed correctly by looking at the colours of the letters as you type.'
         '\n(Green signifies correct, while red signifies wrong.)'
         '\nYou are allowed to re-type the letter with no penalty.'
         '\nThe test will end when all words are typed out, or when the timer runs out.'
         '\nA summary of your results will be shown to you at the end.'
         '\nBest of Luck!', font=('Times New Roman', 15), pady=20)
start_label.pack(pady=(90, 0))
instructions.pack()


def start():
    start_label.destroy()
    start_button.destroy()
    instructions.destroy()


start_button = tk.Button(text='Start Test', command=start)
start_button.pack(pady=(0, 78))

# Reference Para
with open("words.txt") as file:
    test_para = file.read()

paragraph = test_para
listed_para = list(paragraph)


def convert(string):
    li = list(string.split(" "))
    return li


title = tk.Label(text='Typing Speed Test', font=('Times New Roman', 20, 'bold'), pady=10)
title.pack()
listed_words = convert(paragraph)

text = tk.Text(font=('Times New Roman', 16), height=15)
text.pack()
text.insert(tk.END, paragraph)
text.config(state='disabled')


# Colour code along the way
def check_input(*args):
    user_word = list(user_input.get())

    # Clear all tags in the Text widget
    text.tag_delete("correct")
    text.tag_delete("incorrect")

    for i, char in enumerate(user_word):
        if char == listed_para[i]:
            text.tag_add("correct", f"1.{i}")
        else:
            text.tag_add("incorrect", f"1.{i}")

    # Configure tags to set the color
    text.tag_config("correct", foreground="green")
    text.tag_config("incorrect", foreground="red")


# Entry box for user to input answer/Gets input when enter is hit
var = StringVar()
user_input = tk.Entry(window, textvariable=var, foreground='grey')
user_input.insert(0, 'Type here...')

# Create timer for 1 minute
initial = 60
time = 60
timer_label = tk.Label(text=f"Time Remaining: {initial}", font=('Times New Roman', 20, 'bold'))

times_up = False
time_left = 60


def timer(count):
    timer_label.config(text=f"Time Remaining: {count}")
    if count > 0:
        window.after(1000, timer, count - 1)
        global time
        time = time - 1
        global time_left
        time_left = time
        if time == 0:
            global times_up
            times_up = True


def on_entry_click(event):
    if user_input.get() == "Type here...":
        user_input.delete(0, tk.END)
        user_input.configure(foreground="black")
        timer(60)


def on_focus_out(event):
    if user_input.get() == "":
        user_input.insert(0, "Type here...")
        user_input.configure(foreground="grey")


user_input.pack(pady=15)
timer_label.pack()
user_input.bind("<FocusIn>", on_entry_click)
user_input.bind("<FocusOut>", on_focus_out)
var.trace('w', check_input)

word_wrong = 0
word_right = 0
words_typed = []
words_removed = []
total_typed = []


def sent_input(event):
    global word_right
    global word_wrong
    global paragraph
    global listed_para
    global total_typed

    word_sent = user_input.get()  # Gets the word the user typed
    if word_sent.strip() != 'Type here...':
        if word_sent.strip():
            if " " not in word_sent.strip():
                text.config(state='normal')
                if word_sent == f"{listed_words[0]} " or word_sent != f"{listed_words[0]} ":
                    text.tag_add('correct', 1.0, f'1.{len(listed_words[0])}')
                    listed_words.remove(listed_words[0])
                    paragraph = " ".join(listed_words)
                    listed_para = list(paragraph)

                    try:
                        words_typed.append(word_sent)
                        total_typed.append(f"{listed_words[0]} ")
                        words_removed.append(f"{listed_words[0]} ")

                    except IndexError:
                        print('error')

                    finally:
                        for word in words_typed:
                            if word in words_removed:
                                word_right += 1
                                words_typed.remove(word)
                                words_removed.remove(word)

                    text.delete("1.0", END)
                    text.insert(tk.END, paragraph)
                    text.config(state='disabled')

                    # End game
                    if listed_words == [] or times_up:
                        text.destroy()
                        user_input.destroy()
                        timer_label.destroy()
                        total_rights = word_right + 1
                        if 40 <= total_rights <= 60:
                            standard = 'AVERAGE'
                        elif total_rights >= 80:
                            standard = 'ABOVE AVERAGE'
                        else:
                            standard = 'UNDER AVERAGE'
                        percentage = (word_right + 1) / len(total_typed) * 100
                        rounded = round(percentage, 1)
                        wrongs = len(total_typed) - (word_right + 1)
                        if wrongs == 0:
                            outro = tk.Label(
                                text=f' In general, your WPM is {word_right + 1} word(s) per minute. That is {standard}! '
                                     f'\nIn technicalities, you typed a total of {len(total_typed)} word(s), and all were right!'
                                     f'\nThis gives you an accuracy of {rounded}%!',
                                font=('Times New Roman', 20, 'bold', 'italic'), borderwidth=1, relief="solid")
                            outro.place(x=60, y=200)
                            time_left_label = tk.Label(text=f"Time Remaining: {time_left} seconds",
                                                       font=('Times New Roman', 20, 'bold', 'italic'))
                            time_left_label.pack(pady=(60, 0))
                        elif wrongs < 0:
                            actual = len(total_typed) + 1
                            percentage = (word_right + 1) / actual * 100
                            rounded = round(percentage, 1)
                            outro = tk.Label(
                                text=f' In general, your WPM is {word_right + 1} word(s) per minute. That is {standard}! '
                                     f'\nIn technicalities, you typed a total of {actual} word(s), and all were right!'
                                     f'\nThis gives you an accuracy of {rounded}%!',
                                font=('Times New Roman', 20, 'bold', 'italic'), borderwidth=1, relief="solid")
                            outro.place(x=60, y=200)
                            time_left_label = tk.Label(text=f"Time Remaining: {time_left} seconds",
                                                       font=('Times New Roman', 20, 'bold', 'italic'))
                            time_left_label.pack(pady=(60, 0))

                        else:
                            outro = tk.Label(
                                text=f' In general, your WPM is {word_right + 1} word(s) per minute. That is {standard}! '
                                     f'\nIn technicalities, you typed a total of {len(total_typed)} word(s), but '
                                     f'{len(total_typed) - (word_right + 1)} was/were wrong. '
                                     f'\nThis gives you an accuracy of {rounded}%!',
                                font=('Times New Roman', 20, 'bold', 'italic'), borderwidth=1, relief="solid")
                            outro.place(x=60, y=200)
                            time_left_label = tk.Label(text=f"Time Remaining: {time_left} seconds", font=('Times New Roman', 20, 'bold', 'italic'))
                            time_left_label.pack(pady=(60, 0))

                user_input.delete(0, 'end')


window.bind('<space>', sent_input)

window.mainloop()
