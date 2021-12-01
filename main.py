# Importing Libraries
from bot import Bot
from datetime import datetime
import time

# Defining the main program
bot = Bot()
if __name__ == "__main__":
    while True:
        now = datetime.now()
        h = now.strftime("%H")
        m = now.strftime("%M")
        print(h, ":", m)
        time.sleep(1)
        if h == bot.HOUR and m == bot.MINUTE:
            bot.open_supreme_shop()
            bot.ItemIterator()
            bot.add_to_basket()
            bot.go_checkout()
            bot.Pay()