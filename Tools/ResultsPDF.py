from fpdf import FPDF
import Constants
from datetime import datetime


class ResultsPDF(FPDF):

    def header(self):
        title = "Results of Test Run"
        # Arial bold 15
        self.set_font('Arial', size=15)
        # Calculate width of title and position
        w =  170
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(48, 62, 88)
        self.set_fill_color(92, 116, 144)
        self.set_text_color(255, 255, 255)
        # Thickness of frame (1 mm)
        self.set_line_width(0.7)
        # Title
        self.cell(w, 16, title, 1, 1, 'C', 1)
        self.image('GUI/img/Apyno_logo_big.png', 25, 12, 13, 13)
        # Line break
        self.ln(10)
        self.draw_lines()

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def draw_lines(self):
        self.line(20, 25, 20, self.h - 30)
        self.line(190, 25, 190, self.h - 30)
        self.line(20, self.h - 30, 190, self.h-30)

    def draw_report_data(self, path):
        self.set_font("Arial", size=8)
        self.set_left_margin(30)
        self.set_text_color(0)
        self.cell(0, 0, "Date: " + str(datetime.now())[:-15])
        self.ln(5)
        self.cell(0, 0, "Time: " + str(datetime.now())[11:-7])
        self.ln(5)
        self.cell(0, 0, "Module: " + str(path))
        self.ln(10)

    def simple_table(self, spacing=2):
        data = [['First Name', 'Last Name', 'email', 'zip'],
                ['Mike', 'Driscoll', 'mike@somewhere.com', '55555'],
                ['John', 'Doe', 'jdoe@doe.com', '12345'],
                ['Nina', 'Ma', 'inane@where.com', '54321']
                ]
        self.set_draw_color(255, 255, 255)
        self.set_fill_color(92, 116, 144)
        self.set_text_color(255, 255, 255)
        self.set_left_margin(30)
        col_width = self.w / 7.5
        row_height = self.font_size
        for row in data:
            for item in row:

                self.cell(col_width, (row_height * spacing),
                          txt=item, border=1, fill=1,)
            self.ln(row_height * spacing)



