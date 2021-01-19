import discord
import os
import requests
import json
import re
from keep_alive import keep_alive

client = discord.Client()

def get_summoner_id(region, name):
  riot_api_key = os.getenv('RIOT_API_TOKEN')
  response = requests.get(f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={riot_api_key}')
  json_data = json.loads(response.text)
  encrypted_id = json_data['id']
  return encrypted_id

def get_summoner_stats(region, name):
  riot_api_key = os.getenv('RIOT_API_TOKEN')
  region = region.upper()
  regions = {
    'BR': 'BR1',
    'EUNE': 'EUN1',
    'EUW': 'EUW1',
    'LAN': 'LA1',
    'LAS': 'LA2',
    'NA': 'NA1',
    'OCE': 'OCE1',
    'RU': 'RU1',
    'TR': 'TR1',
    'JP': 'JP1'
  }
  region_cdn = regions[region].lower()
  summoner_id = get_summoner_id(region_cdn, name)
  response = requests.get(f'https://{region_cdn}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={riot_api_key}')
  json_data = json.loads(response.text)
  if len(json_data) != 0:
    json_data = json_data[0]
    tier = json_data['tier']
    rank =  json_data['rank']
    summonerName = json_data['summonerName']
    leaguePoints = json_data['leaguePoints']
    wins =  json_data['wins']
    losses = json_data['losses']
    message = f'>>> Invocador:            `{summonerName}` \n'
    message += f'Liga:                      `{tier} {rank}` \n'
    message += f'Puntos de liga:    `{leaguePoints}` \n'
    message += f'🏆    `{wins}`    |    ❌    `{losses}`'
  else:
    message = 'Esta invocador no tiene liga ¯\_(ツ)_/¯'
  return message
# print(get_summoner_stats('las', 'pride is my sin'))

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

def get_covid_data(country):
  response = requests.get(f'https://covid19.mathdro.id/api/countries/{country}')
  json_data = json.loads(response.text)
  confirmed = json_data['confirmed']['value']
  recovered = json_data['recovered']['value']
  deaths = json_data['deaths']['value']
  message = f'>>> Confirmados: `{confirmed}` \nRecuperados: `{recovered}` \nMuertos: `{deaths}`'
  return message
# print(get_covid_data('chile'))

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!perkin lol'):
    region = message.content.split()[2]
    name = message.content[16:]
    await message.channel.send(get_summoner_stats(region, name))
  elif message.content.startswith('!perkin signo'):
    signo = message.content.split()[-1]
    await message.channel.send(get_astrological_sign(signo))
  elif message.content.startswith('!perkin clima'):
    lugar = message.content[13:]
    await message.channel.send(get_weather(lugar))
  elif message.content.startswith('!perkin saldo bip'):
    numero = message.content[16:]
    await message.channel.send(bip_balance(numero))
  elif message.content.startswith('!perkin inspirame'):
    await message.channel.send(inspirational_quote())
  elif message.content.startswith('!perkin precio'):
    indicador = message.content.split()[-1]
    await message.channel.send(get_economic_indicator(indicador))
  elif message.content.startswith('!perkin covid'):
    country = message.content.split()[-1]
    await message.channel.send(get_covid_data(country))
  elif message.content.startswith('!perkin saluda'):
    author_name = message.author
    await message.channel.send(f'Hola {author_name}!')
  elif message.content.startswith('!perkin help'):
    command_list = '```lol [región] [nombre] \n' 
    command_list += 'signo [nombre]\n' 
    command_list += 'clima [lugar] \t NOTA= Sea muy específico \n' 
    command_list += 'saldo bip [N° tarjeta] \n' 
    command_list += 'inspirame \n' 
    command_list += 'precio [indicador] \t NOTA= parametro indicadores muestra lista\n' 
    command_list += 'covid [país] \n' 
    command_list += 'saluda```'
    await message.channel.send(f'Lista de comandos: {command_list}')

keep_alive()
client.run(os.getenv('DISCORD_TOKEN'))
