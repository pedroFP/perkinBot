import discord
import os
import requests
import json
import re

client = discord.Client()

def get_astrological_sign(sign):
  sign_name = sign.lower()
  response = requests.get('https://api.xor.cl/tyaas/')
  json_data = json.loads(response.text)
  sign_data = json_data['horoscopo'][sign_name]
  message = ''
  for key, value in sign_data.items():
    words = re.findall('.[^A-Z]*', key)
    title = ' '.join(map(str, words)).capitalize()
    message += '{0}: {1} \n'.format(title, value)
  return message
# print(get_astrological_sign('tauro'))

def get_weather(location):
  response = requests.get(f'http://es.wttr.in/{location.lower()}?m&format=%l %t %C! %c')
  message = "Clima en: " + response.text
  return message.title()
# print(get_weather('ñuñoa, santiago, chile'))

def bip_balance(number):
  response = requests.get(f'https://api.xor.cl/bip/?n={number}')
  json_data = json.loads(response.text)
  balance = json_data['saldoBip']
  balanceDate = json_data['fechaSaldo']
  message = f'Tu saldo es: `{balance}` \nFecha de saldo: `{balanceDate}`'
  return message
# print(bip_balance(22532227))

def inspirational_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)[0]
  quote = json_data['q']
  author = json_data['a']
  message = f'> {quote} \n - {author}'
  return message
# print(inspirational_quote())

def get_economic_indicator(indicator):
  indicator = indicator.lower()
  response = requests.get('https://mindicador.cl/api')
  json_data = json.loads(response.text)
  if indicator == 'indicadores':
    message = list(json_data.keys())[3:]
  else:
    indicator_data = json_data[indicator]
    name = indicator_data['nombre']
    value = str(indicator_data['valor'])
    currency = indicator_data['unidad_medida']
    message = f'```{name}: $ {value} {currency}```'
  return message
# print(get_economic_indicator('dolar'))

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!perkin signo'):
    signo = message.content.split()[-1]
    await message.channel.send(get_astrological_sign(signo))

  if message.content.startswith('!perkin clima'):
    lugar = message.content[13:]
    await message.channel.send(get_weather(lugar))

  if message.content.startswith('!perkin saldo bip'):
    numero = message.content[16:]
    await message.channel.send(bip_balance(numero))

  if message.content.startswith('!perkin inspirame'):
    await message.channel.send(inspirational_quote())

  if message.content.startswith('!perkin precio'):
    indicador = message.content.split()[-1]
    await message.channel.send(get_economic_indicator(indicador))

  if message.content.startswith('!perkin saluda'):
    author_name = message.author.split('#')[0]
    await message.channel.send(f'Hola {author_name}!')

client.run(os.getenv('DISCORD_TOKEN'))
