from os import environ
import aiohttp
from pyrogram import Client, filters
import time
import cloudscraper
from urllib.parse import urlparse
from bs4 import BeautifulSoup

API_ID = 2054877
API_HASH = '4227c1e45e462209a3dcc67ada88a44f'
BOT_TOKEN = '1861652521:AAHsirFvvZD0bTwkYgXC_vK3KiMv4WVHMSE'

API_KEY = environ.get('API_KEY', '5fd20df0c4db85798dd4f5ff3d03e3606a94f98b')

bot = Client('gplink bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**𝗛𝗘𝗟𝗟𝗢🎈{message.chat.first_name}!**\n\n"
        "hey dude i am upgraded version .support multiple links")


@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    link  =  f"{message.text}"
    try:
        link = link.split()
        for i in a:
            if 'https' in i :
              url = i
                
        short_link = await gplinks_bypass(url)
        await message.reply(f'Here is your👉{short_link} , quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def gplinks_bypass(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    res = client.head(url)
    header_loc = res.headers['location']
    param = header_loc.split('postid=')[-1]
    req_url = f'{p.scheme}://{p.netloc}/{param}'

    p = urlparse(header_loc)
    ref_url = f'{p.scheme}://{p.netloc}/'

    h = { 'referer': ref_url }
    res = client.get(req_url, headers=h, allow_redirects=False)

    bs4 = BeautifulSoup(res.content, 'html.parser')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'referer': ref_url,
        'x-requested-with': 'XMLHttpRequest',
    }
    time.sleep(10)
    res = client.post(final_url, headers=h, data=data)
    try:
        return res.json()['url'].replace('\/','/')
    except: return 'Something went wrong :('



bot.run()
