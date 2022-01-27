from tkinter import *
from tkinter.ttk import *
import threading

class TkApp(Tk):
    frame: Frame
    cnvs: Canvas
    max_values = 30

    # Values used for drawing
    canvas_width = 650
    canvas_height = 350
    incrementX = 17
    incrementY = 15
    shiftY = 50
    startY = canvas_height - shiftY
    labelStartX = 80

    def __init__(self, title, topic):
        Tk.__init__(self, title)
        self.title(title)
        self.listOfValues = []
        self.create_form_ui(topic)
        self.create_canvas()
        self.set_form_style()

    # Method for part 1 of the dynamic chart lab
    def update_values(self, new_value):
        if (len(self.listOfValues) == self.max_values):
            self.listOfValues.pop(0)
        self.listOfValues.append(new_value)
        self.redraw_lines()

    def create_form_ui(self, topic):
        self.minsize(620, 430)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Setup frame
        self.frame = Frame(self, width=620, height=430)
        self.frame['padding'] = (5, 10)
        self.frame['borderwidth'] = 10
        self.frame['relief'] = 'ridge'
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid(sticky=(W, E))

        # Title Font
        title_font = {'font': ('Helvetica', 18)}

        # Create labels
        Label(self.frame,
                text=f'Humidity Data for Past {self.max_values} Days',
                **title_font).grid(row=0, columnspan=3, pady=10)

        # Create labels for location (i.e. topic)
        loc_frame = Frame(self.frame)
        loc_frame.grid(row=1, column=0, columnspan=3)
        Label(loc_frame, text=f'Location:').grid(row=0, column=0)
        self.message_text = StringVar()
        self.message_text.set(topic)
        Label(loc_frame, textvariable=self.message_text).grid(
            row=0, column=1, sticky='W')

    def create_canvas(self):
        self.cnvs = Canvas(self.frame,
                            width=self.canvas_width,
                            height=self.canvas_height,
                            bg='#dde5b6',
                            bd=0, highlightthickness=0,
                            relief='ridge')
        self.cnvs.grid(row=2, columnspan=3)

        # Create lines and labels for graph
        startValue = 0
        self.notch_length = 20
        self.incrementY = 13

        # Create X and Y axis
        self.cnvs.create_line(self.labelStartX, self.startY-self.incrementY,
                                self.labelStartX + ((self.max_values + 1) * self.incrementX), self.startY-self.incrementY, width=1)

        self.cnvs.create_line(self.labelStartX + self.notch_length, self.startY,
                                self.labelStartX + self.notch_length, self.startY - (self.incrementY * 22), width=1)

        # Add axis labels
        self.cnvs.create_text(
            self.canvas_width / 2,  self.canvas_height - (self.shiftY - 30), anchor='nw', text='Days')

        self.cnvs.create_text(
            20,  self.canvas_height / 2, text='Humidity', anchor='nw', angle=90)

        # Create Y axis notches and labels
        for x in range(21):
            self.startY -= self.incrementY
            if x % 2 == 0:
                self.cnvs.create_line(
                    self.labelStartX, self.startY, self.labelStartX + self.notch_length, self.startY, width=1)
                self.cnvs.create_text(
                    self.labelStartX - 20, self.startY, text=str(startValue)+'%')
                startValue += 10
            else:
                self.cnvs.create_line(self.labelStartX + self.notch_length, self.startY,
                                        self.labelStartX + (self.notch_length / 2), self.startY, width=1)

        # Create X axis notches and labels
        for x in range(self.max_values):
            self.cnvs.create_line(
                self.labelStartX + self.notch_length + (self.incrementX * x), self.canvas_height - self.shiftY - self.incrementY, self.labelStartX + self.notch_length + (self.incrementX * x), self.canvas_height - self.shiftY, width=1)
            self.cnvs.create_text(
                self.labelStartX + self.notch_length + (self.incrementX * x), self.canvas_height - (self.shiftY - 10),  text=x)

        self.redraw_lines()

    def set_form_style(self):
        style = Style()
        style.theme_use('alt')
        style.configure('.',
                        font="Arial 12",
                        background='#dde5b6',
                        foreground='#463f3a')

    def redraw_lines(self):
        # Delete previously drawn lines
        self.cnvs.delete('line')

        # Values used for scaling and positioning
        first_notch_position = self.incrementY + self.shiftY
        last_notch_position = 21 * self.incrementY + self.shiftY
        height = last_notch_position - first_notch_position
        startX = self.labelStartX + self.notch_length

        # Draw lines
        for i in range(len(self.listOfValues) - 1):
            # Only draw if not bad data
            cur = self.listOfValues[i]
            next = self.listOfValues[i+1]
            if type(cur) == float:
                lineY1 = self.canvas_height - \
                    (cur / 100 *
                        height) - first_notch_position
                if type(next) == float:
                    lineY2 = self.canvas_height - \
                        (next / 100 *
                            height) - first_notch_position
                else:
                    lineY2 = lineY1
                self.cnvs.create_line(
                    (startX, lineY1), (startX + self.incrementX, lineY2), width=1, fill='red', tag='line')
            startX = startX + self.incrementX

    def initUI(self, value):
        threading.Thread(target=self.update_values, args=[
            value], daemon=True).start()
