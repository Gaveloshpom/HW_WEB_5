import platform

import sys
import aiohttp
import asyncio
import datetime
import logging


async def main(ccy, date=datetime.datetime.today().strftime("%d.%m.%Y")):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?date={date}') as response:
                if response.status == 200:
                    response_result = await response.json()
                    r = response_result["exchangeRate"]
                    res = {}
                    for ell in ccy:
                        exchange, *_ = list(filter(lambda el: el["currency"] == ell, r))
                        purchase_sale = {
                                    date: {
                                         ell: {
                                            "purchase": exchange['purchaseRate'],
                                            "sale": exchange['saleRate']
                                           }
                                      }
                                 }
                        res.update(purchase_sale)
                    return res
                else:
                    logging.error(f"Error : {response.status}")
        except aiohttp.ClientConnectionError as e:
            logging.error(f"Connection error to server: {e}")


async def start():
    res = list()
    # ccy = list()
    # ccy.append(sys.argv[1])     #Мало брати вказані валюти для обробки, функціонал не дороблений
    # archive_days = int(sys.argv[2])
    archive_days = int(sys.argv[2])
    ccy = ["EUR", "USD"]
    if archive_days <= 10:
        for i in range(archive_days):
            day = datetime.datetime.today() - datetime.timedelta(i)
            r = asyncio.create_task(main(ccy, day.strftime("%d.%m.%Y")))
            res.append(r)
        print(await asyncio.gather(*res))
    else:
        print("Max amount of days is 10!")

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(start())
