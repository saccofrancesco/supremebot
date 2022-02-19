# Supreme-Bot
This is my Personal Supreme Bot for Buying Items on the Day of the Supreme Shop's Drop!

## Set Up
Download the ZIP Folder, or Clone the Repository with:
```
git clone https://github.com/TonicStark/Supreme-Bot.git
```

Then install the dependencies in a virtualenv, you can create one via `python -m venv <name of the virtualenv>`, with:
```python
pip install -r requirements.txt
```

Now you need a Chrome Driver: you can download it from this [page](https://chromedriver.chromium.org/downloads). Then put it in the folder where stands this project and you are done.

## Personalization
Now that you have set up your environment you can add Items to the `Items.json` file with this parameter sequence:

```JSON
[
    {
        "Item": "Name of the Item",
        "Style": "Color",
        "Size": "Size",
        "Type": "Category"
    }
]
```

Now you have to modify the data in the `Data.json` file to suits your needs, like that:

```JSON
[
    {
        "Name Surname": "Your Name and Surname",
        "Email": "Your E-Mail",
        "Tel": "Your Phone - Number",
        "Address": "Your Address",
        "N": "Your Civic Number",
        "City": "Your City",
        "Postal Code": "Your Postal Code",
        "Card Number": "Your Credit Card Number",
        "CVV": "Your Card's Verification Token"
    }
]
```

## Start the Bot
Now you have only to run the `main.py` file just before the drop, which is at 12:00 in Italy. You can modify the hours and minutes in the `bot.py` file, specifically:
```python
# Buy Times
self.HOUR = "12"
self.MINUTE = "00"
```
Make sure to include the items you want to buy in the list, which is in the `Item.json` file and you are good to go! The Bot will buy the items you requested within seconds! **Happy Shopping!**