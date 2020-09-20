# module to find anime info from kitsu.io by t.me/dank_as_fuck ( misaki@eagleunion.tk)

import aiohttp
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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
  query.replace('', '%20') 
  url = f'https://kitsu.io/api/edge/anime?filter%5Btext%5D={urlencode(query)}' 
  session = aiohttp.ClientSession() 
  async with session.get(url) as resp:
    a = await resp.json()
    if 'data' in a.keys():
      data = a["data"][0]
      pic = f'{data["attributes"]["coverImage"]["original"] if data["attributes"].get("coverImage", "") else ""}'
      id = f'{a["data"][0]["id"]}'
      info = f'{data["attributes"]["titles"]["en_jp"]}\n'
      info += f'{data["attributes"]["titles"]["ja_jp"]}\n'
      info += f' * Rating: {data["attributes"]["averageRating"]}\n'
      info += f' * Release Date: {data["attributes"]["startDate"]}\n'
      info += f' * End Date: {data["attributes"]["endDate"]}\n'
      info += f' * Status: {data["attributes"]["status"]}\n'
      info += f' * Description: {data["attributes"]["description"]}\n'
      aurl = f'kitsu.io/anime/'+id
      if len(info) > 1024:
        info = info[0:500] + "...."
      link_btn = InlineKeyboardMarkup()
      link_btn.insert(InlineKeyboardButton("Read more", url=aurl))
      if pic:
         await message.reply_photo(pic, caption=info, reply_markup=link_btn)
      else:
         await message.reply_text(info, reply_markup=link_btn)
