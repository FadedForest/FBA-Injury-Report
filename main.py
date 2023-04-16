import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import discord
from table2ascii import table2ascii as t2a, PresetStyle
from table2ascii import Alignment, table2ascii
from flask import Flask
from threading import Thread
#Stays Online
app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
#Bot Token
my_secret = os.environ['discord_code']
#Website Scrapping
url= "https://www.fba-wiki.net/index.php/2023_Disabled_List"

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

injury_table = soup.find('table', id='Long_Term')

# Obtain every title of columns with tag <th>
headers = []
for i in injury_table.find_all('th'):
 title = i.text
 headers.append(title)

mydata = pd.DataFrame(columns=headers)

# Create a for loop to fill mydata
for j in injury_table.find_all('tr')[1:]:
 row_data = j.find_all('td')
 row = [i.text for i in row_data]
 length = len(mydata)
 mydata.loc[length] = row

new_list = mydata.replace('\n',' ', regex=True)

table=new_list.values.tolist()

output=t2a(
  header=headers,
  body=table,
  alignments=[Alignment.LEFT, Alignment.CENTER, Alignment.CENTER, Alignment.CENTER, Alignment.RIGHT],
  style=PresetStyle.markdown
)

#Day2Day

d2d_table = soup.find('table', id='Day2Day')

# Obtain every title of columns with tag <th>
d2dheaders = []
for i in d2d_table.find_all('th'):
 title = i.text
 d2dheaders.append(title)

d2dmydata = pd.DataFrame(columns=d2dheaders)

# Create a for loop to fill mydata
for j in d2d_table.find_all('tr')[1:]:
 row_data = j.find_all('td')
 row = [i.text for i in row_data]
 length = len(d2dmydata)
 d2dmydata.loc[length] = row

d2dnew_list = d2dmydata.replace('\n',' ', regex=True)

d2dtable=d2dnew_list.values.tolist()

d2doutput=t2a(
  header=d2dheaders,
  body=d2dtable,
  alignments=[Alignment.LEFT, Alignment.CENTER, Alignment.CENTER, Alignment.CENTER, Alignment.RIGHT],
  style=PresetStyle.markdown
)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$injur') or message.content.startswith('$Injur'):
        await message.channel.send("**Injured**"f"```\n{output}\n```")
        await message.channel.send("**Day-to-Day**"f"```\n{d2doutput}\n```")

client.run(my_secret)