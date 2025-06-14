from ._anvil_designer import Form2Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.http
import json

class Form2(Form2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.URL = 'https://data.cityofnewyork.us/resource/8y4t-faws.json'
    self.check_db()

  def check_db(self):
    results = app_tables.table_db.search()
    items = []
    
    for row in results:
      items.append(f"{row['housenum_lo']}, {row['street_name']}, {row['aptno']}")
      
    self.dropdown_menu_1.items = items
    self.dropdown_menu_1.selected_value = self.dropdown_menu_1.items[0]

  def update_db(self, housenum_lo, street_name, aptno):
    row = app_tables.table_db.get(housenum_lo=housenum_lo)

    if row is None:
      app_tables.table_db.add_row(housenum_lo=housenum_lo,
                                  street_name=street_name,
                                  aptno=aptno)
    else:
      row.update(housenum_lo=housenum_lo,
                 street_name=street_name,
                 aptno=aptno)
    
  def button_1_click(self, **event_args):
    '''This method is called when the component is clicked.'''
    housenum_lo = self.text_box_1.text
    street_name = self.text_box_2.text.upper()
    aptno = self.text_box_6.text.upper()

    try:
      if self.checkbox_1.checked:
        resp = anvil.http.request(f'{self.URL}?housenum_lo={housenum_lo}&street_name={street_name}',
                               json=True)
      else:
        resp = anvil.http.request(f'{self.URL}?housenum_lo={housenum_lo}&street_name={street_name}&aptno={aptno}',
                                  json=True)

      json_data = resp[-1]

      parid = json_data.get('parid')
      boro = json_data.get('boro')
      block = json_data.get('block')
      lot = json_data.get('lot')
      year = json_data.get('year')
      zip_code = json_data.get('zip_code')
      owner = json_data.get('owner')
      gross_sqft = json_data.get('gross_sqft')
      curtxbtot = int(json_data.get('curtxbtot'))
      curtxbextot = int(json_data.get('curtxbextot'))
      curtaxclass = json_data.get('curtaxclass')
      bldg_class = json_data.get('bldg_class')
      appt_date = json_data.get('appt_date')
      extracrdt = json_data.get('extracrdt')

      if appt_date is not None:
        appt_date = appt_date[:10]
      if extracrdt is not None:
        extracrdt = extracrdt[:10]
      
      self.text_1.text = (
        f'PARID: {parid}\n'
        f'BORO: {boro}\n'
        f'BLOCK: {block}\n'
        f'LOT: {lot}\n'
        f'YEAR: {year}\n'
        f'ZIPCODE: {zip_code}\n'
        f'APT: {aptno}\n'
        f'OWNER: {owner}\n'
        f'SQFT: {gross_sqft}\n'
        f'CUR TXB TOT: {curtxbtot}\n'
        f'CUR TXB EX TOT: {curtxbextot}\n'
        f'CUR TAX CLASS: {curtaxclass}\n'
        f'BLDG CLASS: {bldg_class}\n'
        f'APPT DT: {appt_date}\n'
        f'EXTRACR DT: {extracrdt}'
      )
      
      # current tax
      
      curval = curtxbtot - curtxbextot
      self.text_box_3.text = curval

      curtax = curval * float(self.text_box_4.text)

      self.text_box_5.text = curtax

      # final tax
      finaltax = curtxbtot * float(self.text_box_4.text)
      
      self.text_box_7.text = finaltax
      
      # update db
      self.update_db(housenum_lo, street_name, aptno)
      self.check_db()
      
    except anvil.http.HttpError as e:
      alert(f'Error {e.status}')
    except Exception as e:
      alert(e)

  def dropdown_menu_1_change(self, **event_args):
    """This method is called when an item is selected"""
    arg = self.dropdown_menu_1.selected_value.split(',')

    self.text_box_1.text = arg[0].strip()
    self.text_box_2.text = arg[1].strip()
    self.text_box_6.text = arg[2].strip()

    if arg[2].strip() == '':
      self.text_box_6.enabled = False
      self.checkbox_1.checked = True
    else:
      self.text_box_6.enabled = True
      self.checkbox_1.checked = False

  def checkbox_1_change(self, **event_args):
    """This method is called when the component is checked or unchecked"""
    if self.checkbox_1.checked:
      self.text_box_6.text = ''
      self.text_box_6.enabled = False
    else:
      self.text_box_6.enabled = True
