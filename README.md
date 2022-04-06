# PCGameAnalysis
Allows the user to get data from Steam regarding games sold on that platform

#PLEASE NOTE THAT THE WISHLIST AND REVENUE NUMBERS ARE ESTIMATIONS



This script was made with python, which you can get here: https://www.python.org/downloads/

To use it you will need to install some libraries, to do so, use this command in your terminal after installing python

```pip install pandas openpyxl```

Once those libraries are installed, simply type ```python3 ./PCGameAnalysis.py``` to run it


Once you've done that, you will be prompted by a text menu looking like this:
![Screenshot from 2022-04-06 19-30-21](https://user-images.githubusercontent.com/103136664/162033728-af5c2525-2c38-420e-89ef-eb6006490df1.png)

By choosing "1", you will be able to get data from Steam regarding the games or publishers of your choice

By choosing "2", you will be able to get data from Steam regarding games similar to the game of your choice

Here's a list of the data that this script will retrieve:
```
Game title
Tags
Number of followers
Wishlist estimations (Using Simon Carless' numbers from this article: https://newsletter.gamediscover.co/p/deep-dive-how-steam-followers-and)
Revenue estimations (Using the Boxleiter method)
Positive reviews percentage, and the resulting rating (Both recent and general reviews/rating)
Release date
Days since the game got released
How many players are playing that game when you started this script

```

##Known issues

Here are some issues that are there and might be fixed in the future, but aren't that important

The tags are listed first instead of the game's name
Empty spaces are replaced by %20 in the tags' name

