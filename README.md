# home-purchase-nyc-app: Your NYC Home Purchase Companion 🏠

Dreaming of buying a home in the Big Apple? The "home-purchase-nyc-app" is designed to empower you with essential financial insights and property data to make informed decisions. Built with Anvil, this web application provides a user-friendly interface to calculate potential mortgage costs and access detailed property information directly from NYC's open data.

## ✨ Features

### Mortgage Calculator 💰
* **Dynamic Calculations**: Instantly calculate your estimated monthly mortgage payments, factoring in principal, interest, property taxes, homeowner's insurance, and HOA fees.
* **Flexible Tax Input**: Easily switch between annual and monthly property tax inputs.
* **Interactive Slider**: Adjust the purchase price with a convenient slider to see its immediate impact on your estimated payments.

### NYC Property Data Explorer 🏙️
* **Direct Data Access**: Query real-time property data from the City of New York's open data portal (data.cityofnewyork.us).
* **Search by Address**: Retrieve comprehensive details including PARID, Boro, Block, Lot, Year built, Zip Code, Owner, Gross Square Footage, Current Taxable Totals, Tax Class, Building Class, and more.
* **Tax Estimation**: Get an estimate of current and final property taxes based on provided assessment data and a customizable tax rate.
* **Local Database Integration**: Save and easily recall previously searched properties, with the ability to manage your search history.
* **Flexible Search**: Search for properties with or without an apartment number, perfect for both single-family homes and condominiums.

## 🚀 How It Works

The application leverages Anvil's full-stack capabilities, using Python for both the client-side UI logic and server-side data interactions.

### Mortgage Calculation (Form1)
The `Form1` module handles all mortgage-related calculations. When you input values for purchase price, down payment, interest rate, HOA fees, taxes, and insurance, the `calc` function computes the estimated monthly loan payment, adds in the other costs, and displays the total.

```python
class Form1(Form1Template):
    # ... (initialization and other methods)

    def calc(self):
        # Calculates principal (P), monthly interest rate (r), and total months (n)
        P = int(self.text_box_1.text) - int(self.text_box_2.text)
        self.text_box_3.text = P
        r = float(self.text_box_4.text) / 1200 # Annual interest rate to monthly percentage
        n = 360 # Assuming a 30-year mortgage

        # Retrieves HOA, adjusts tax for monthly calculation, and gets insurance
        hoa = float(self.text_box_5.text)
        if self.radio_button_1.selected: # Annual tax selected
            tax = float(self.text_box_6.text)
        elif self.radio_button_2.selected: # Monthly tax selected
            tax = float(self.text_box_6.text) / 12
        ins = float(self.text_box_8.text) / 12

        # Calculates loan portion of the payment (P * 10000 accounts for price scaling)
        loan = (P*10000) * (r*(1+r)**n) / ((1+r)**n-1)

        # Sums all costs and displays the rounded total
        C = round((loan + ins + tax + hoa), 2)
        self.text_box_7.text = C
```

### Property Data Retrieval (Form2)
The `Form2` module is responsible for fetching and displaying NYC property assessment data. It interacts with the NYC Open Data API and maintains a local database of previously searched properties using Anvil's built-in data tables.

```python
class Form2(Form2Template):
    # ... (initialization and other methods)

    def button_1_click(self, **event_args):
        # Constructs API request based on user input (house number, street name, apartment number)
        # Handles cases where apartment number might be excluded
        # Fetches data from data.cityofnewyork.us/resource/8y4t-faws.json
        # Parses JSON response and displays relevant property details
        # Calculates current and final tax estimates
        # Updates and refreshes the local database of searched properties
        # Includes error handling for API requests

    def check_db(self):
        # Populates a dropdown menu with previously searched properties from 'app_tables.table_db'

    def update_db(self, housenum_lo, street_name, aptno):
        # Adds new property to database or updates existing entry
```

### 🗃️ Database Schema

The `table_db` in your Anvil app stores previously searched property addresses for quick access. Its schema is as follows:

| Column Name | Type   | Description                               |
| :---------- | :----- | :---------------------------------------- |
| `housenum_lo` | String | The house number of the property.           |
| `street_name` | String | The street name of the property.          |
| `aptno`       | String | The apartment number (can be empty).      |

## 📂 File Structure

The project structure is as follows:

```
home-purchase-nyc-app/
├── Form1.py        # Contains files related to the Mortgage Calculator form
├── Form2.py        # Contains files related to the Property Data Explorer form
├── Table_db        # Anvil's built-in data tables
└── Assets          # Optional: images, CSS, etc.
```

## 🚀 Demo

Experience the "home-purchase-nyc-app" live\!

**🔗 Live Application Link:** [https://gorgeous-obedient-dirt.anvil.app/]

**📸 Screenshot:**
![Screenshot of the Home Purchase NYC App](about:sanitized)

## 🏁 Getting Started

This project is built using Anvil. To run and modify this application:

1.  **Sign up for an Anvil account:** If you don't have one, visit [anvil.works](https://anvil.works).
2.  **Clone this repository:**
    ```bash
    git clone https://github.com/your-username/home-purchase-nyc-app.git
    ```
3.  **Open in Anvil**: Create a new blank app in Anvil, then use the "Upload Anvil App" option and select the cloned directory.
4.  **Run the app**: Click the "Run" button ▶️ in the Anvil editor to see the application in action.

## 🤝 Contributing

We welcome contributions to improve this application! If you have suggestions, bug reports, or want to add new features, please feel free to:

* Open an issue 🐛
* Submit a pull request 🚀

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
