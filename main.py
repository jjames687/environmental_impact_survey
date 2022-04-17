"""
Modified version of survey from:

Programmer: Joshua Willman
Date: 2019.11.17

Trying to make a survey that can do environmental impoct surveys
"""
import csv
import os.path
import time
from tkinter import (Tk, Label, Button, Frame, Menu,
                     StringVar, Toplevel, Entry)
from tkinter import messagebox
from tkinter import ttk

# create empty lists used for each set of questions
actions_impacts = dict()
questions = ["Abiotico", "Biotico", "Socioeconomico"]


def dialogBox(title, message):
    """
    Basic function to create and display general dialog boxes.
    """
    dialog = Tk()
    dialog.wm_title(title)
    dialog.grab_set()
    dialogWidth, dialogHeight = 225, 125
    positionRight = int(dialog.winfo_screenwidth() / 2 - dialogWidth / 2)
    positionDown = int(dialog.winfo_screenheight() / 2 - dialogHeight / 2)
    dialog.geometry("{}x{}+{}+{}".format(
        dialogWidth, dialogHeight, positionRight, positionDown))
    dialog.maxsize(dialogWidth, dialogHeight)
    label = Label(dialog, text=message)
    label.pack(side="top", fill="x", pady=10)
    ok_button = ttk.Button(dialog, text="Ok", command=dialog.destroy)
    ok_button.pack(ipady=3, pady=10)
    dialog.mainloop()


def nextSurveyDialog(title, message, cmd):
    """
    Dialog box that appears before moving onto the next set of questions.
    """
    dialog = Tk()
    dialog.wm_title(title)
    dialog.grab_set()
    dialogWidth, dialogHeight = 225, 125
    positionRight = int(dialog.winfo_screenwidth() / 2 - dialogWidth / 2)
    positionDown = int(dialog.winfo_screenheight() / 2 - dialogHeight / 2)
    dialog.geometry("{}x{}+{}+{}".format(
        dialogWidth, dialogHeight, positionRight, positionDown))
    dialog.maxsize(dialogWidth, dialogHeight)
    dialog.overrideredirect(True)
    label = Label(dialog, text=message)
    label.pack(side="top", fill="x", pady=10)
    ok_button = ttk.Button(dialog, text="Begin", command=lambda: [f() for f in [cmd, dialog.destroy]])
    ok_button.pack(ipady=3, pady=10)

    dialog.protocol("WM_DELETE_WINDOW", disable_event)  # prevent user from clicking ALT + F4 to close
    dialog.mainloop()


def disable_event():
    pass


def finishedDialog(title, message):
    """
    Display the finished dialog box when user reaches the end of the survey.
    """
    dialog = Tk()
    dialog.wm_title(title)
    dialog.grab_set()
    dialogWidth, dialogHeight = 325, 150
    positionRight = int(dialog.winfo_screenwidth() / 2 - dialogWidth / 2)
    positionDown = int(dialog.winfo_screenheight() / 2 - dialogHeight / 2)
    dialog.geometry("{}x{}+{}+{}".format(
        dialogWidth, dialogHeight, positionRight, positionDown))
    dialog.maxsize(dialogWidth, dialogHeight)
    dialog.overrideredirect(True)
    label = Label(dialog, text=message)
    label.pack(side="top", fill="x", pady=10)
    ok_button = ttk.Button(dialog, text="Quit", command=quit)
    ok_button.pack(ipady=3, pady=10)

    dialog.protocol("WM_DELETE_WINDOW", disable_event)  # prevent user from clicking ALT + F4 to close
    dialog.mainloop()


def writeToFile(filename, answer_list):
    """
    Called at end of program when user selects finished button,
    write all lists to separate files.
    Parameters: filename: name for save file,
                answer_list: list containing answer from that one of the
                four sections in the survey.
    """
    headers = []
    file_exists = os.path.isfile(filename)

    with open(filename, 'a') as csvfile:
        for i in range(1, len(answer_list) + 1):
            headers.append("Q{}".format(i))
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')

        if not file_exists:
            writer.writerow(headers)  # file doesn't exist yet, write a header

        writer.writerow(answer_list)


class otherPopUpDialog(object):
    """
    Class for 'other' selections in General Question class.
    When user selects 'other' option, they are able to input 
    their answer into an Entry widget.

    self.value: the value of Entry widget.
    """

    def __init__(self, master, text):
        top = self.top = Toplevel(master)
        self.text = text
        top.wm_title("Other Answers")
        top.grab_set()
        dialogWidth, dialogHeight = 200, 150
        positionRight = int(top.winfo_screenwidth() / 2 - dialogWidth / 2)
        positionDown = int(top.winfo_screenheight() / 2 - dialogHeight / 2)
        top.geometry("{}x{}+{}+{}".format(
            dialogWidth, dialogHeight, positionRight, positionDown))
        self.label = Label(top, text=self.text)
        self.label.pack(ipady=5)
        self.enter = Entry(top)
        self.enter.pack(ipady=5)
        self.ok_button = Button(top, text="Ok", command=self.cleanup)
        self.ok_button.pack(ipady=5)

    def cleanup(self):
        """
        Get input from Entry widget and close dialog.
        """
        self.value = self.enter.get()
        self.top.destroy()


class Survey(Tk):
    """
    Main class, define the container which will contain all the frames.
    """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # call closing protocol to create dialog box to ask 
        # if user if they want to quit or not.
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # title for the whole survey
        Tk.wm_title(self, "Environmental Impact Survey")

        # Create container Frame to hold all other classes, 
        # which are the different parts of the survey.
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create menu bar
        menubar = Menu(container)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        Tk.config(self, menu=menubar)

        # create empty dictionary for the different frames (the different classes)
        self.frames = {}

        for fr in (StartPage, Construccion, Apertura, Adecuacion, Descapote, Vias_transporte, Disposicion, Arranque,
                   Cargue, Ventilacion, Drenajes, Esteriles_escombros, Cierre, Levantamiento, EndScreen):
            frame = fr(container, self)
            self.frames[fr] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def on_closing(self):
        """
        Display dialog box before quitting.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def show_frame(self, cont):
        """
        Used to display a frame.
        """
        frame = self.frames[cont]
        frame.tkraise()  # bring a frame to the "top"


class StartPage(Frame):
    """
    First page that user will see.
    Explains the rules and any extra information the user may need 
    before beginning the survey.
    User can either click one of the two buttons, Begin Survey or Quit.
    """

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        # set up start page window
        self.configure(bg="#EFF3F6")
        start_label = Label(self, text="Environmental Impact", font=("Verdana", 16),
                            borderwidth=2, relief="ridge")
        start_label.pack(pady=10, padx=10, ipadx=5, ipady=3)

        # add labels and buttons to window
        info_text = "Using this tool to complete the survey:\nFor each action in the plan, you will decide if it has" \
                    " an impact.\nThen you will decide if the impact is positive or negative.\nFinally, the assesment" \
                    "of the impact will be completed.\nThere are 3 phases of action in the plan.\nThere are 12 total" \
                    " actions to assess for 26 impacts.\n\nAfter each section, a small window will notify you."
        info_label = Label(self, text=info_text, font=("Verdana", 12),
                           borderwidth=2, relief="ridge")
        info_label.pack(pady=10, padx=10, ipadx=20, ipady=3)

        purpose_text = "The purpose of this questionaire is to make it \nto fill out impact surveys."
        purpose_text = Label(self, text=purpose_text, font=("Verdana", 12),
                             borderwidth=2, relief="ridge")
        purpose_text.pack(pady=10, padx=10, ipadx=5, ipady=3)

        start_button = ttk.Button(self, text="Begin Survey",
                                  command=lambda: controller.show_frame(Construccion))
        start_button.pack(ipadx=10, ipady=15, pady=15)

        quit_button = ttk.Button(self, text="Quit", command=self.on_closing)
        quit_button.pack(ipady=3, pady=10)

    def on_closing(self):
        """
        Display dialog box before quitting.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.controller.destroy()


class Construccion(Frame):
    """
    Class that displays questions for Fase 1
    Construccion campamento y oficinas
    """
    construccion = dict()
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global actions_impacts
        global questions
        # Create header label
        ttk.Label(self, text="Construccion campamento y oficinas", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.questions = questions

        # set index in questions list 
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes 
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=('Verdana', 16))
        self.question_label.pack(padx=20, pady=10)

        Label(self, text="Impact", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Negative", "No Impact", "Positive"]

        scale = [("-1", -1), ("0", 0), ("1", 1)]

        self.impact = StringVar()
        self.impact.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.impact, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        Label(self, text="Intensidad", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.intensidad = StringVar()
        self.intensidad.set(0)  # initialize

        # Frame to contain text 
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.intensidad, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Set up labels and checkboxes
        self.question_label.pack(anchor='w', padx=20, pady=10)
        Label(self, text="Extension", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.extension = StringVar()
        self.extension.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.extension, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer0 = self.impact.get()
        answer1 = self.intensidad.get()
        answer2 = self.extension.get()
        if answer0 != '0' and answer1 == '0':
            dialogBox("No Value Given: Intensidad",
                      "You did not select an answer.\nPlease try again.")
        elif answer0 != '0' and answer2 == '0':
            dialogBox("No Value Given: Extension",
                      "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index + 1
            self.construccion[variable] = total_impact
            actions_impacts[Construccion] = self.construccion
            print(self.construccion)
            print(actions_impacts)
            next_survey_text = "End of Part 1."
            nextSurveyDialog("Next Survey", next_survey_text,
                             lambda: self.controller.show_frame(Apertura))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index
            self.construccion[variable] = total_impact

            self.impact.set(0)
            self.extension.set(0)  # reset value for next question
            self.intensidad.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class Apertura(Frame):
    """
    Class that displays questions for Fase 1
    Apertura Bocaminas
    """
    apertura = dict()
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global actions_impacts
        global questions
        # Create header label
        ttk.Label(self, text="Apertura y perforación bocaminas", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.questions = questions

        # set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=('Verdana', 16))
        self.question_label.pack(padx=20, pady=10)

        Label(self, text="Impact", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Negative", "No Impact", "Positive"]

        scale = [("-1", -1), ("0", 0), ("1", 1)]

        self.impact = StringVar()
        self.impact.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.impact, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        Label(self, text="Intensidad", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.intensidad = StringVar()
        self.intensidad.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.intensidad, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Set up labels and checkboxes
        self.question_label.pack(anchor='w', padx=20, pady=10)
        Label(self, text="Extension", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.extension = StringVar()
        self.extension.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.extension, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer0 = self.impact.get()
        answer1 = self.intensidad.get()
        answer2 = self.extension.get()
        if answer0 != '0' and answer1 == '0':
            dialogBox("No Value Given: Intensidad",
                      "You did not select an answer.\nPlease try again.")
        elif answer0 != '0' and answer2 == '0':
            dialogBox("No Value Given: Extension",
                      "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index + 1
            self.apertura[variable] = total_impact
            actions_impacts[Apertura] = self.apertura
            print(self.apertura)
            print(actions_impacts)
            next_survey_text = "End of Part 2."
            nextSurveyDialog("Next Survey", next_survey_text,
                             lambda: self.controller.show_frame(Adecuacion))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index
            self.apertura[variable] = total_impact

            self.impact.set(0)
            self.extension.set(0)  # reset value for next question
            self.intensidad.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class Adecuacion(Frame):
    """
    Class that displays questions for Fase 1
    Adecuacion del sistema de acceso y sostenimiento
    """
    adecuacion = dict()
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global actions_impacts
        global questions
        # Create header label
        ttk.Label(self, text="Adecuacion del sistema de acceso y sostenimiento", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.questions = questions

        # set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=('Verdana', 16))
        self.question_label.pack(padx=20, pady=10)

        Label(self, text="Impact", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Negative", "No Impact", "Positive"]

        scale = [("-1", -1), ("0", 0), ("1", 1)]

        self.impact = StringVar()
        self.impact.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.impact, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        Label(self, text="Intensidad", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.intensidad = StringVar()
        self.intensidad.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.intensidad, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Set up labels and checkboxes
        self.question_label.pack(anchor='w', padx=20, pady=10)
        Label(self, text="Extension", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.extension = StringVar()
        self.extension.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.extension, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer0 = self.impact.get()
        answer1 = self.intensidad.get()
        answer2 = self.extension.get()
        if answer0 != '0' and answer1 == '0':
            dialogBox("No Value Given: Intensidad",
                      "You did not select an answer.\nPlease try again.")
        elif answer0 != '0' and answer2 == '0':
            dialogBox("No Value Given: Extension",
                      "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index + 1
            self.adecuacion[variable] = total_impact
            actions_impacts[Adecuacion] = self.adecuacion
            print(self.adecuacion)
            print(actions_impacts)
            next_survey_text = "End of Part 3."
            nextSurveyDialog("Next Survey", next_survey_text,
                             lambda: self.controller.show_frame(Descapote))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index
            self.adecuacion[variable] = total_impact

            self.impact.set(0)
            self.extension.set(0)  # reset value for next question
            self.intensidad.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class Descapote(Frame):
    """
    Class that displays questions for Fase 1
    Descapote y remotion capa vegetal
    """
    descapote = dict()
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global actions_impacts
        global questions
        # Create header label
        ttk.Label(self, text="Descapote y remotion capa vegetal", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.questions = questions

        # set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=('Verdana', 16))
        self.question_label.pack(padx=20, pady=10)

        Label(self, text="Impact", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Negative", "No Impact", "Positive"]

        scale = [("-1", -1), ("0", 0), ("1", 1)]

        self.impact = StringVar()
        self.impact.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.impact, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        Label(self, text="Intensidad", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.intensidad = StringVar()
        self.intensidad.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.intensidad, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Set up labels and checkboxes
        self.question_label.pack(anchor='w', padx=20, pady=10)
        Label(self, text="Extension", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.extension = StringVar()
        self.extension.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.extension, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer0 = self.impact.get()
        answer1 = self.intensidad.get()
        answer2 = self.extension.get()
        if answer0 != '0' and answer1 == '0':
            dialogBox("No Value Given: Intensidad",
                      "You did not select an answer.\nPlease try again.")
        elif answer0 != '0' and answer2 == '0':
            dialogBox("No Value Given: Extension",
                      "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index + 1
            self.descapote[variable] = total_impact
            actions_impacts[Descapote] = self.descapote
            print(self.descapote)
            print(actions_impacts)
            next_survey_text = "End of Part 4."
            nextSurveyDialog("Next Survey", next_survey_text,
                             lambda: self.controller.show_frame(Vias_transporte))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index
            self.descapote[variable] = total_impact

            self.impact.set(0)
            self.extension.set(0)  # reset value for next question
            self.intensidad.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class Vias_transporte(Frame):
    """
    Class that displays questions for Fase 1
    Adecuacion de vias de transporte
    """
    vias_transporte = dict()
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global actions_impacts
        global questions
        # Create header label
        ttk.Label(self, text="Adecuacion de vias de transporte", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.questions = questions

        # set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=('Verdana', 16))
        self.question_label.pack(padx=20, pady=10)

        Label(self, text="Impact", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Negative", "No Impact", "Positive"]

        scale = [("-1", -1), ("0", 0), ("1", 1)]

        self.impact = StringVar()
        self.impact.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.impact, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        Label(self, text="Intensidad", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.intensidad = StringVar()
        self.intensidad.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.intensidad, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Set up labels and checkboxes
        self.question_label.pack(anchor='w', padx=20, pady=10)
        Label(self, text="Extension", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.extension = StringVar()
        self.extension.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.extension, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer0 = self.impact.get()
        answer1 = self.intensidad.get()
        answer2 = self.extension.get()
        if answer0 != '0' and answer1 == '0':
            dialogBox("No Value Given: Intensidad",
                      "You did not select an answer.\nPlease try again.")
        elif answer0 != '0' and answer2 == '0':
            dialogBox("No Value Given: Extension",
                      "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index + 1
            self.vias_transporte[variable] = total_impact
            actions_impacts[Vias_transporte] = self.vias_transporte
            print(self.vias_transporte)
            print(actions_impacts)
            next_survey_text = "End of Part 5."
            nextSurveyDialog("Next Survey", next_survey_text,
                             lambda: self.controller.show_frame(Disposicion))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index
            self.vias_transporte[variable] = total_impact

            self.impact.set(0)
            self.extension.set(0)  # reset value for next question
            self.intensidad.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class Disposicion(Frame):
    """
    Class that displays questions for Fase 1
    Disposicion escombros y material removido
    """
    disposicion = dict()
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global actions_impacts
        global questions
        # Create header label
        ttk.Label(self, text="Disposicion escombros y material removido", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.questions = questions

        # set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=('Verdana', 16))
        self.question_label.pack(padx=20, pady=10)

        Label(self, text="Impact", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Negative", "No Impact", "Positive"]

        scale = [("-1", -1), ("0", 0), ("1", 1)]

        self.impact = StringVar()
        self.impact.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.impact, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        Label(self, text="Intensidad", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.intensidad = StringVar()
        self.intensidad.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.intensidad, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Set up labels and checkboxes
        self.question_label.pack(anchor='w', padx=20, pady=10)
        Label(self, text="Extension", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.extension = StringVar()
        self.extension.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.extension, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer0 = self.impact.get()
        answer1 = self.intensidad.get()
        answer2 = self.extension.get()
        if answer0 != '0' and answer1 == '0':
            dialogBox("No Value Given: Intensidad",
                      "You did not select an answer.\nPlease try again.")
        elif answer0 != '0' and answer2 == '0':
            dialogBox("No Value Given: Extension",
                      "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index + 1
            self.disposicion[variable] = total_impact
            actions_impacts[Disposicion] = self.disposicion
            print(self.disposicion)
            print(actions_impacts)
            next_survey_text = "End of Part 6."
            nextSurveyDialog("Next Survey", next_survey_text,
                             lambda: self.controller.show_frame(Arranque))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index
            self.disposicion[variable] = total_impact

            self.impact.set(0)
            self.extension.set(0)  # reset value for next question
            self.intensidad.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class Arranque(Frame):
    """
    Class that displays questions for Fase 1
    Arranque y extracción
    """
    arranque = dict()

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global actions_impacts
        global questions
        # Create header label
        ttk.Label(self, text="Arranque y extracción", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.questions = questions

        # set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=('Verdana', 16))
        self.question_label.pack(padx=20, pady=10)

        Label(self, text="Impact", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Negative", "No Impact", "Positive"]

        scale = [("-1", -1), ("0", 0), ("1", 1)]

        self.impact = StringVar()
        self.impact.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.impact, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        Label(self, text="Intensidad", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.intensidad = StringVar()
        self.intensidad.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.intensidad, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Set up labels and checkboxes
        self.question_label.pack(anchor='w', padx=20, pady=10)
        Label(self, text="Extension", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.extension = StringVar()
        self.extension.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.extension, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer0 = self.impact.get()
        answer1 = self.intensidad.get()
        answer2 = self.extension.get()
        if answer0 != '0' and answer1 == '0':
            dialogBox("No Value Given: Intensidad",
                      "You did not select an answer.\nPlease try again.")
        elif answer0 != '0' and answer2 == '0':
            dialogBox("No Value Given: Extension",
                      "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            total_impact = 0
            total_impact = 3 * (int(self.intensidad.get())) + 2 * (int(self.extension.get()))
            total_impact = int(self.impact.get()) * total_impact
            variable = self.index + 1
            self.arranque[variable] = total_impact
            actions_impacts[Arranque] = self.arranque
            print(self.arranque)
            print(actions_impacts)
            next_survey_text = "End of Part 7."
            nextSurveyDialog("Next Survey", next_survey_text,
                             lambda: self.controller.show_frame(Cargue))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            total_impact = 0
            total_impact = 3 * (int(self.intensidad.get())) + 2 * (int(self.extension.get()))
            total_impact = int(self.impact.get()) * total_impact
            variable = self.index
            self.arranque[variable] = total_impact

            self.impact.set(0)
            self.extension.set(0)  # reset value for next question
            self.intensidad.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class Cargue(Frame):
    """
    Class that displays questions for Fase 1
    Cargue y transporte
    """
    cargue = dict()
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global actions_impacts
        global questions
        # Create header label
        ttk.Label(self, text="Cargue y transporte", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.questions = questions

        # set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=('Verdana', 16))
        self.question_label.pack(padx=20, pady=10)

        Label(self, text="Impact", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Negative", "No Impact", "Positive"]

        scale = [("-1", -1), ("0", 0), ("1", 1)]

        self.impact = StringVar()
        self.impact.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.impact, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        Label(self, text="Intensidad", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.intensidad = StringVar()
        self.intensidad.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.intensidad, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Set up labels and checkboxes
        self.question_label.pack(anchor='w', padx=20, pady=10)
        Label(self, text="Extension", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.extension = StringVar()
        self.extension.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.extension, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer0 = self.impact.get()
        answer1 = self.intensidad.get()
        answer2 = self.extension.get()
        if answer0 != '0' and answer1 == '0':
            dialogBox("No Value Given: Intensidad",
                      "You did not select an answer.\nPlease try again.")
        elif answer0 != '0' and answer2 == '0':
            dialogBox("No Value Given: Extension",
                      "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index + 1
            self.cargue[variable] = total_impact
            actions_impacts[Cargue] = self.cargue
            print(self.cargue)
            print(actions_impacts)
            next_survey_text = "End of Part 8."
            nextSurveyDialog("Next Survey", next_survey_text,
                             lambda: self.controller.show_frame(Ventilacion))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index
            self.cargue[variable] = total_impact

            self.impact.set(0)
            self.extension.set(0)  # reset value for next question
            self.intensidad.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class Ventilacion(Frame):
    """
    Class that displays questions for Fase 1
    Ventilacion
    """
    ventilacion = dict()
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global actions_impacts
        global questions
        # Create header label
        ttk.Label(self, text="Ventilacion ", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.questions = questions

        # set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=('Verdana', 16))
        self.question_label.pack(padx=20, pady=10)

        Label(self, text="Impact", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Negative", "No Impact", "Positive"]

        scale = [("-1", -1), ("0", 0), ("1", 1)]

        self.impact = StringVar()
        self.impact.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.impact, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        Label(self, text="Intensidad", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.intensidad = StringVar()
        self.intensidad.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.intensidad, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Set up labels and checkboxes
        self.question_label.pack(anchor='w', padx=20, pady=10)
        Label(self, text="Extension", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.extension = StringVar()
        self.extension.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.extension, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer0 = self.impact.get()
        answer1 = self.intensidad.get()
        answer2 = self.extension.get()
        if answer0 != '0' and answer1 == '0':
            dialogBox("No Value Given: Intensidad",
                      "You did not select an answer.\nPlease try again.")
        elif answer0 != '0' and answer2 == '0':
            dialogBox("No Value Given: Extension",
                      "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index + 1
            self.ventilacion[variable] = total_impact
            actions_impacts[Ventilacion] = self.ventilacion
            print(self.ventilacion)
            print(actions_impacts)
            next_survey_text = "End of Part 9."
            nextSurveyDialog("Next Survey", next_survey_text,
                             lambda: self.controller.show_frame(Drenajes))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index
            self.ventilacion[variable] = total_impact

            self.impact.set(0)
            self.extension.set(0)  # reset value for next question
            self.intensidad.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class Drenajes(Frame):
    """
    Class that displays questions for Fase 1
    Drenajes y manejo de aguas
    """
    drenajes = dict()
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global actions_impacts
        global questions
        # Create header label
        ttk.Label(self, text="Drenajes y manejo de aguas", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.questions = questions

        # set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=('Verdana', 16))
        self.question_label.pack(padx=20, pady=10)

        Label(self, text="Impact", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Negative", "No Impact", "Positive"]

        scale = [("-1", -1), ("0", 0), ("1", 1)]

        self.impact = StringVar()
        self.impact.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.impact, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        Label(self, text="Intensidad", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.intensidad = StringVar()
        self.intensidad.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.intensidad, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Set up labels and checkboxes
        self.question_label.pack(anchor='w', padx=20, pady=10)
        Label(self, text="Extension", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.extension = StringVar()
        self.extension.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.extension, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer0 = self.impact.get()
        answer1 = self.intensidad.get()
        answer2 = self.extension.get()
        if answer0 != '0' and answer1 == '0':
            dialogBox("No Value Given: Intensidad",
                      "You did not select an answer.\nPlease try again.")
        elif answer0 != '0' and answer2 == '0':
            dialogBox("No Value Given: Extension",
                      "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index + 1
            self.drenajes[variable] = total_impact
            actions_impacts[Drenajes] = self.drenajes
            print(self.drenajes)
            print(actions_impacts)
            next_survey_text = "End of Part 10."
            nextSurveyDialog("Next Survey", next_survey_text,
                             lambda: self.controller.show_frame(Esteriles_escombros))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index
            self.drenajes[variable] = total_impact

            self.impact.set(0)
            self.extension.set(0)  # reset value for next question
            self.intensidad.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class Esteriles_escombros(Frame):
    """
    Class that displays questions for Fase 1
    Disposicion de estériles y escombros
    """
    esteriles_escombros = dict()
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global actions_impacts
        global questions
        # Create header label
        ttk.Label(self, text="Disposicion de estériles y escombros", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.questions = questions

        # set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=('Verdana', 16))
        self.question_label.pack(padx=20, pady=10)

        Label(self, text="Impact", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Negative", "No Impact", "Positive"]

        scale = [("-1", -1), ("0", 0), ("1", 1)]

        self.impact = StringVar()
        self.impact.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.impact, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        Label(self, text="Intensidad", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.intensidad = StringVar()
        self.intensidad.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.intensidad, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Set up labels and checkboxes
        self.question_label.pack(anchor='w', padx=20, pady=10)
        Label(self, text="Extension", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.extension = StringVar()
        self.extension.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.extension, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer0 = self.impact.get()
        answer1 = self.intensidad.get()
        answer2 = self.extension.get()
        if answer0 != '0' and answer1 == '0':
            dialogBox("No Value Given: Intensidad",
                      "You did not select an answer.\nPlease try again.")
        elif answer0 != '0' and answer2 == '0':
            dialogBox("No Value Given: Extension",
                      "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index + 1
            self.esteriles_escombros[variable] = total_impact
            actions_impacts[Esteriles_escombros] = self.esteriles_escombros
            print(self.esteriles_escombros)
            print(actions_impacts)
            next_survey_text = "End of Part 11."
            nextSurveyDialog("Next Survey", next_survey_text,
                             lambda: self.controller.show_frame(Cierre))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index
            self.esteriles_escombros[variable] = total_impact

            self.impact.set(0)
            self.extension.set(0)  # reset value for next question
            self.intensidad.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class Cierre(Frame):
    """
    Class that displays questions for Fase 1
    Cierre de bocaminas
    """
    cierre = dict()

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global actions_impacts
        global questions
        # Create header label
        ttk.Label(self, text="Cierre de bocaminas", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.questions = questions

        # set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=('Verdana', 16))
        self.question_label.pack(padx=20, pady=10)

        Label(self, text="Impact", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Negative", "No Impact", "Positive"]

        scale = [("-1", -1), ("0", 0), ("1", 1)]

        self.impact = StringVar()
        self.impact.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.impact, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        Label(self, text="Intensidad", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.intensidad = StringVar()
        self.intensidad.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.intensidad, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Set up labels and checkboxes
        self.question_label.pack(anchor='w', padx=20, pady=10)
        Label(self, text="Extension", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.extension = StringVar()
        self.extension.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.extension, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer0 = self.impact.get()
        answer1 = self.intensidad.get()
        answer2 = self.extension.get()
        if answer0 != '0' and answer1 == '0':
            dialogBox("No Value Given: Intensidad",
                      "You did not select an answer.\nPlease try again.")
        elif answer0 != '0' and answer2 == '0':
            dialogBox("No Value Given: Extension",
                      "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            total_impact = 0
            total_impact = 3 * (int(self.intensidad.get())) + 2 * (int(self.extension.get()))
            total_impact = int(self.impact.get()) * total_impact
            variable = self.index + 1
            self.cierre[variable] = total_impact
            actions_impacts[Cierre] = self.cierre
            print(self.cierre)
            print(actions_impacts)
            next_survey_text = "End of Part 12."
            nextSurveyDialog("Next Survey", next_survey_text,
                             lambda: self.controller.show_frame(Levantamiento))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            total_impact = 0
            total_impact = 3 * (int(self.intensidad.get())) + 2 * (int(self.extension.get()))
            total_impact = int(self.impact.get()) * total_impact
            variable = self.index
            self.cierre[variable] = total_impact

            self.impact.set(0)
            self.extension.set(0)  # reset value for next question
            self.intensidad.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class Levantamiento(Frame):
    """
    Class that displays questions for Fase 1
    Levantamiento infraestructura
    """
    levantamiento = dict()
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global actions_impacts
        global questions
        # Create header label
        ttk.Label(self, text="Levantamiento infraestructura", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.questions = questions

        # set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=('Verdana', 16))
        self.question_label.pack(padx=20, pady=10)

        Label(self, text="Impact", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Negative", "No Impact", "Positive"]

        scale = [("-1", -1), ("0", 0), ("1", 1)]

        self.impact = StringVar()
        self.impact.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.impact, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        Label(self, text="Intensidad", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.intensidad = StringVar()
        self.intensidad.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.intensidad, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Set up labels and checkboxes
        self.question_label.pack(anchor='w', padx=20, pady=10)
        Label(self, text="Extension", font=('Verdana', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Baja", "Media", "Alta", "Muy Alta", "Total"]

        scale = [("1", 1), ("2", 2), ("4", 4), ("8", 8), ("12", 12)]

        self.extension = StringVar()
        self.extension.set(0)  # initialize

        # Frame to contain text
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text,
                                variable=self.extension, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer0 = self.impact.get()
        answer1 = self.intensidad.get()
        answer2 = self.extension.get()
        if answer0 != '0' and answer1 == '0':
            dialogBox("No Value Given: Intensidad",
                      "You did not select an answer.\nPlease try again.")
        elif answer0 != '0' and answer2 == '0':
            dialogBox("No Value Given: Extension",
                      "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index + 1
            self.levantamiento[variable] = total_impact
            actions_impacts[Levantamiento] = self.levantamiento
            print(self.levantamiento)
            print(actions_impacts)
            next_survey_text = "End of Part 13."
            nextSurveyDialog("Next Survey", next_survey_text,
                             lambda: self.controller.show_frame(EndScreen))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            total_impact = 0
            total_impact = 3*(int(self.intensidad.get())) + 2*(int(self.extension.get()))
            total_impact = int(self.impact.get())*total_impact
            variable = self.index
            self.levantamiento[variable] = total_impact

            self.impact.set(0)
            self.extension.set(0)  # reset value for next question
            self.intensidad.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class EndScreen(Frame):
    """
    Displays expenses at game question from General questions.
    """

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global general_answers_list

        # Create header label
        ttk.Label(self, text="End Screen", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.question = "The evaluation is now finished. Click continue to write the file."

        # Set up labels and listbox
        self.question_label = Label(self, text="10. {}".format(self.question), font=('Verdana', 16))
        self.question_label.pack(anchor='w', padx=20, pady=10)


        enter_button = ttk.Button(self, text="Continue", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        end diologue
        '''

        self.writeToFile()
        finished_text = "You have reached the end of the survey.\n"
        finishedDialog("Finished Survey", finished_text)

    def writeToFile(self):
        """
        When user selects finished button, writes each filename with corresponding 
        answer list to separate files.
        """
        # list of names and answer lists
        filenames = ['answers.csv']

        answers_lists = [actions_impacts]

        for filename, answers in zip(filenames, answers_lists):
            writeToFile(filename, answers)



# Run program
if __name__ == "__main__":
    app = Survey()
    app.mainloop()
