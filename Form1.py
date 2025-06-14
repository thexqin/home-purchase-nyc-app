from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.calc()
    # Any code you write here will run before the form opens.

  def calc(self):
    P = int(self.text_box_1.text) - int(self.text_box_2.text)
    self.text_box_3.text = P
    r = float(self.text_box_4.text) / 1200
    n = 360

    hoa = float(self.text_box_5.text)
    if self.radio_button_1.selected:
      tax = float(self.text_box_6.text)
    elif self.radio_button_2.selected:
      tax = float(self.text_box_6.text) / 12
    ins = float(self.text_box_8.text) / 12
    loan = (P*10000) * (r*(1+r)**n) / ((1+r)**n-1)

    C = round((loan + ins + tax + hoa), 2)
    self.text_box_7.text = C
    
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    self.calc()

  def radio_button_2_select(self, **event_args):
    """This method is called when the radio button is selected."""
    self.text_box_6.text = round(float(self.text_box_6.text)*12)

  def radio_button_1_select(self, **event_args):
    """This method is called when the radio button is selected."""
    self.text_box_6.text = round(float(self.text_box_6.text)/12)

  def slider_1_change(self, **event_args):
    """This method is called when the value of the component is changed"""
    self.text_box_1.text = self.slider_1.value
