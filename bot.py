import json
import discord
import requests
import random
import re
from app import start_server

def random_quote():
    # not in quote mode
    positive = random.choice(settings['positive_words'])
    if not settings['quote_mode']:
        return positive
    # quote mode
    response = requests.get('https://zenquotes.io/api/random/')
    if response.status_code >= 400:
        return positive
    content = json.loads(response.text)[0]
    return f'{positive}\n{content["q"]}\n\t- {content["a"]}'

settings = {
    'trigger': '(:',
    'quote_mode': True,
    'quiet_mode': False,
    'counter_words': ['not', "don't", "dont"],
    'negative_words': ['depressed', 'depression', 'sad', 'bad', 'kms', 'no', 'angry', 'die'],
    'positive_words': ['Be happy like me, Happy Bot! XD', 'You have summoned me, Happy Bot! XD'],
}

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} is ready to spread some positivity!')

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return
    # toggle quiet mode
    if message.content == '):':
        settings['quiet_mode'] = not settings['quiet_mode']
        if settings['quiet_mode']:
            await message.channel.send('ok ill be quiet')
        else:
            await message.channel.send('HELLO XD')
        return
    # turn off quote mode
    if message.content == settings['trigger']:
        settings['quote_mode'] = False
        await message.channel.send(random_quote())
        return
    # turn on quote mode
    if message.content.lower() == f"{settings['trigger']} quote":
        settings['quote_mode'] = True
        await message.channel.send(random_quote())
        return
    
    # check messages for negative words
    parsed_messages = res.sub(r'[^\w\s]', '', message.content).split(' ')
    sent = False
    for index, word in enumerate(parsed_messages):
        if sent:
            break
        if word.word in settings['negative_words']:
            if index > 0 and parsed_messages[index - 1].lower() in settings['counter_words']:
                continue
            if not settings['quiet_mode']:
                await message.channel.send(random_quote())
                sent = True


# run bot
start_server()
with open('token', 'r') as f:
    lines = f.readlines()
client.run(lines[0])

# TODO: implement persistence?
