import PyPDF2  # GET THE TEXT FROM THE PDF
import pyttsx3  # PYTHON LIBRARY FOR TEXT TO SPEECH, IT DOESNT HAVE A WAY TO STOP THE VOICE
from tkinter import Tk, Label, Entry, Button, filedialog, LabelFrame, Text, END, StringVar, Radiobutton, LEFT, \
    messagebox
from os import environ, remove

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame  # LIBRARY FOR PLAY, PAUSE, AND RESUME THE AUDIO

BACKGROUND_COLOR = "#E1F7F5"
doc = None
num_entry1 = None
num_entry2 = None
info = None
# SET THE VOICE ENGINE
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# PUT THE AVAILABLE VOICES INSIDE A DIC
lis_voices = [x.id[66:-5] for x in voices]
dic_voices = {x: lis_voices.index(x) for x in lis_voices}


# DELETA WAV AUDIO
def delete_audio():
    try:
        pygame.mixer.quit()
        remove('pdf_temporal_audio.wav')
    except FileNotFoundError:
        pass


def refresh_program():
    global info
    path_entry.delete(0, END)
    num_entry1.delete(0, END)
    num_entry2.delete(0, END)
    info.grid_forget()
    delete_audio()


# GET PDF
def get_pdf():
    global num_entry1
    global num_entry2
    global doc
    global info
    try:
        # GET PDF
        pdf_path = filedialog.askopenfile().name
        doc = PyPDF2.PdfReader(pdf_path)
        # SHOW THE DOC INFO
        info = LabelFrame(window, text="PDF Info", font=('Century Gothic', 10), background=BACKGROUND_COLOR,
                          fg="#1E0342")
        info.grid(column=0, columnspan=2, row=3)
        nump = len(doc.pages)
        name = doc.metadata.title
        pag = Label(info, text=f"Numbers of Pages in total: {nump}", font=('Century Gothic', 8),
                    background=BACKGROUND_COLOR, fg="#1E0342")
        pag.pack()
        name = Label(info, text=f"File Name: {name}", font=('Century Gothic', 8), background=BACKGROUND_COLOR,
                     fg="#1E0342")
        name.pack()
        read_buton = Button(text="🔊 Read", font=("Century Gothic", 8), width=10, background="#0E46A3", fg="white",
                            activebackground="#9AC8CD", activeforeground="#1E0342",
                            command=lambda: read_pdf(int(v.get())))
        read_buton.grid(column=2, row=3)
        stop_read_buton = Button(text="⚠️ Stop", font=("Century Gothic", 8), width=10, background="#1E0342", fg="white",
                                 activebackground="#0E46A3", activeforeground="#1E0342", command=stop)
        stop_read_buton.grid(column=2, row=4)
        pause_buton = Button(text="⏸ Pause", font=("Century Gothic", 8), width=10, background="#0E46A3", fg="white",
                             activebackground="#9AC8CD", activeforeground="#1E0342", command=pause)
        pause_buton.grid(column=3, row=3)
        unpause_buton = Button(text="⏭ Continue", font=("Century Gothic", 8), width=10, background="#0E46A3",
                               fg="white",
                               activebackground="#9AC8CD", activeforeground="#1E0342", command=unpause)
        unpause_buton.grid(column=6, row=3)
        refresh_doc = Button(text="↻ Refresh", font=("Century Gothic", 8), width=10, background="#0E46A3",
                             fg="white",
                             activebackground="#9AC8CD", activeforeground="#1E0342", command=refresh_program)
        refresh_doc.grid(column=3, row=4)
        num_page = LabelFrame(window, text="Select page (max5)", font=('Century Gothic', 10),
                              background=BACKGROUND_COLOR,
                              fg="#1E0342", pady=5)
        num_page.grid(column=0, columnspan=2, row=4)
        num_label1 = Label(num_page, text="From", font=('Century Gothic', 9), background=BACKGROUND_COLOR)
        num_label1.grid(column=0, row=5)
        num_entry1 = Entry(num_page, width=5)
        num_entry1.grid(column=1, row=5)
        num_label2 = Label(num_page, text="To", font=('Century Gothic', 9), background=BACKGROUND_COLOR)
        num_label2.grid(column=0, row=6)
        num_entry2 = Entry(num_page, width=5)
        num_entry2.grid(column=1, row=6)
        return path_entry.insert(0, pdf_path), doc
    except AttributeError:
        pass


def change_voice(value):
    engine.setProperty('voice', voices[value].id)


def read_pdf(value):
    global doc
    global num_entry1
    global num_entry2
    # READ THE PDF VOICE, AND SAVE IT AS A .WAV SO THAT WE CAN PASS IT TO PYGAME
    change_voice(value)
    y = len(doc.pages)
    try:
        pag = range(int(num_entry1.get()) - 1, int(num_entry2.get()))
        page_text = []
        for x in pag:
            page_text.append(doc.pages[x].extract_text())
        engine.save_to_file(page_text, 'pdf_temporal_audio.wav')
        engine.runAndWait()
        pygame.init()
        pygame.mixer_music.load('pdf_temporal_audio.wav')
        pygame.mixer_music.play()
    except ValueError:
        messagebox.showinfo(title="Pages not found", message="Please choose a range of pages."
                                                             "Ex: - 1 / 1 or 1 / ....")
    except IndexError:
        messagebox.showinfo(title="Pages not found", message="Range of pages does not exist!")


def read_txt(value):
    global doc
    # READ TXT
    engine.setProperty('voice', voices[value].id)
    txt = tex_entry.get(index1=1.0, index2=END)
    engine.say(txt)
    engine.runAndWait()


def stop():
    pygame.mixer_music.fadeout(3)


def pause():
    pygame.mixer_music.pause()


def unpause():
    pygame.mixer_music.unpause()


# GUI LAYOUT
window = Tk()
window.config(height=600, width=700, pady=40, padx=50, background=BACKGROUND_COLOR)
window.grid_propagate(False)  # It doesn't change size with the content
# TITLE
h1 = Label(window, text='PDF Reader', font=('Century Gothic', 20), border=0, background=BACKGROUND_COLOR, fg="#1E0342",
           justify='center')
h1.grid(column=1, columnspan=3, row=0)
# CHANGE VOICE
label_frame_format = LabelFrame(text='Change voice', font=('Century Gothic', 8), border=0, background=BACKGROUND_COLOR,
                                fg="#1E0342")
label_frame_format.grid(row=9, column=2, columnspan=6)
v = StringVar(value="0")
for (text, value) in dic_voices.items():
    Radiobutton(label_frame_format, text=text, variable=v, value=value, font=('Century Gothic', 8), border=0,
                background=BACKGROUND_COLOR, fg="#1E0342").pack(side=LEFT, ipady=2)

# UPLOAD PDF
h2 = Label(text="Upload your PDF: ", font=('Century Gothic', 10), border=0, background=BACKGROUND_COLOR, fg="#1E0342")
h2.grid(column=0, row=1)
path_entry = Entry(font=("Century Gothic", 10), width=50)
path_entry.grid(column=1, row=1, columnspan=3)
spacer1 = Label(text="  ", border=0, background=BACKGROUND_COLOR, fg="#1E0342")
spacer1.grid(row=1, column=5)
btnFind = Button(text="Search", font=("Century Gothic", 8), width=10, background="#0E46A3", fg="white",
                 activebackground="#9AC8CD", activeforeground="#1E0342", command=get_pdf)  # GET PDF
btnFind.grid(row=1, column=6)
# TITLE2
h2 = Label(window, text='TEXT Reader', font=('Century Gothic', 20), border=0, background=BACKGROUND_COLOR, fg="#1E0342",
           justify='center', pady=10)
h2.grid(column=1, columnspan=3, row=5)
tex_entry = Text(font=("Century Gothic", 10), width=70, height=10)
tex_entry.grid(column=0, columnspan=7, row=6)
spacer2 = Label(text="  ", border=0, background=BACKGROUND_COLOR, fg="#1E0342")
spacer2.grid(row=7, column=0)
read_buton2 = Button(text="🔊 Read", font=("Century Gothic", 8), width=10, background="#0E46A3", fg="white",
                     activebackground="#9AC8CD", activeforeground="#1E0342", command=lambda: read_txt(int(v.get())),
                     padx=10)
read_buton2.grid(column=2, row=8)

window.mainloop()
# QUIT THE PLAYER AND REMOVE THE WAV FROM THE FILE
delete_audio()
