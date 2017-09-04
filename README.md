# PriceWatcher
Whenever it's time to get tickets back home, it's always a struggle to find the cheapest fare. Checking the website every now and then is cumbersome so I decided to develop a simple script that watches the wizzair website for price changes.

Everything is deployed on heroku, uses postgres to store current lowest price and is being run every 10 minutes. Should it detect a change, it'd send an email to me and a text to inform about the change so I can act accordingly.

If it helps you in any way, then it'd be splendid. Do as you wish with it!