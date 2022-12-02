
# Check income in Cardano wallets

It is a simple project made in python that seeks to solve the income check when you have several wallets.

The idea is to place the wallets that we want to monitor in the excel file, first see the balance of each one and then check every hour if there were any changes. It only considers the income, when realizing an income, it sends a message to the indicated telegram group.

Check balances every 5 seconds so as not to spam the server and then check all wallets again every hour to check for changes


## Dependencies and imports

`import os`
`import json`
`from time import sleep`
`import pandas as pd`
`import requests`
`from pathlib import Path`
`import datetime`
## Variables

To run this script you need to set the following variables:

`bot_token` : This identifier is provided to us by Telegram when generating a bot

`chat_id` : This identifier is provided to us by Telegram, it identifies the group to which the message will be sent

## To run

We need a file called wallets.xlsx with the wallets to check. In this repository there is an example file.

Having that, it only remains to execute the script


```bash

  python3 aviso_ingresos_cardano.py
```
    
## Author
Twitter
- [@Ramiro_P_](https://twitter.com/Ramiro_P_)

Github
- [@DeployRama](https://github.com/deployRama) 