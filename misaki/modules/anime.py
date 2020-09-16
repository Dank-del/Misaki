import io
import json
import aiohttp
from urllib.parse import quote as urlencode
from misaki import bot
from misaki.decorator import register
from .utils.disable import disableable_dec
from .utils.message import need_args_dec, get_args_str

@register(cmds='anime')
@disableable_dec('anime')
async def anime(message): 
  query = get_args_str(message).lower() 
  headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"} 
  query = urlencode(query) 
  url = f'https://kitsu.io/api/edge/anime?filter%5Btext%5D={urlencode(query)}' 
  session = aiohttp.ClientSession() 
  async with session.get(url) as resp:
    a = await resp.json()
    if 'data' in a:
      pic = f'{a["data"][0]["attributes"]["coverImage"]["small"]}'
      info = f'{a["data"][0]["attributes"]["titles"]["en"]}\n'
      info += f'{a["data"][0]["attributes"]["titles"]["en_jp"]}\n'
      info += f'{a["data"][0]["attributes"]["titles"]["ja_jp"]}\n'
      info += f' - Rating: {a["data"][0]["attributes"]["averageRating"]}\n'
      info += f' - Release Date: {a["data"][0]["attributes"]["startDate"]}\n'
      info += f' - End Date: {a["data"][0]["attributes"]["endDate"]}\n'
      info += f' - Status: {a["data"][0]["attributes"]["status"]}\n'
      info += f' - Description: {a["data"][0]["attributes"]["description"]}\n'
      output = (f"{pic}\n{info}")
      await message.reply(output)
      return

