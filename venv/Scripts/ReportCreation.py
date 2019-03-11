from reportlab.pdfgen import canvas
import cStringIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Frame, PageBreak
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import reportlab.lib, reportlab.platypus
from BespokePricerDictionaries import associate_client_to_pricer_table, report_frame_creation
import os
import matplotlib.pyplot as plt
import PIL.Image
import numpy as np
import datetime as dtm


class Test(object):

    def __init__(self, dict, path, histogram, frame, name):

        self.width, self.height = letter
        self.styles = getSampleStyleSheet()
        self.dict = dict
        self.path = path
        self.hist_name = histogram
        self.report_frame = frame
        self.Report_name = name


    def run(self):

        self.doc = SimpleDocTemplate( self.Report_name,rightMargin=72,leftMargin=72, topMargin=72,bottomMargin=18)
        self.story = [Spacer(1, 2 * cm)]
        self.createLineItems()

        FirstPage = self.createDocument

        self.doc.build(self.story, onFirstPage = FirstPage)
        print "finished!"


    def createDocument(self, canvas, doc):

        self.c = canvas
        normal = self.styles['Normal']

        p = Paragraph('Bespoke Pricers Report', normal)
        p.wrapOn(self.c, self.width, self.height)
        p.drawOn(self.c, 250, 800)

        hist = Image(self.hist_name, width=380, height=380)
        hist.wrapOn(self.c, 1, 380)
        hist.drawOn(self.c, x=100,y=1)

        today_frame, monthend_frame = report_frame_creation(self.report_frame, self.path)
        freq_im_today = Image(today_frame, width=255, height=255)
        freq_im_ME = Image(monthend_frame, width=255, height=255)

        freq_im_today.wrapOn(self.c, 310,255)
        freq_im_ME.wrapOn(self.c, 310, 255)

        freq_im_today.drawOn(self.c, 1,380)
        freq_im_ME.drawOn(self.c, 305, 380)

    def createLineItems(self):

        #list of all current pricers
        table_example = associate_client_to_pricer_table(self.dict, self.path)
        table = Table(table_example.tolist(), rowHeights=0.35 * cm, colWidths=10.5 * cm)
        #table = Table(table_example.tolist())

        self.story.append(PageBreak())
        self.story.append(table)





def report_creation(path, filename, imagename, dataframe, dict):

    os.chdir(path)
    t = Test(dict,path, imagename, dataframe, filename)
    t.run()






