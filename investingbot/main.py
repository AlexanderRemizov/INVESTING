"""
Investing Telegram bot.

It helps you to calculate compound interest and send the graph of it to
telegram.
"""

import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils import markdown as fmt
from investing import draw_investing
from settings import TOKEN

# Configure bot and Dispatcher for running
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message) -> None:
    """
    Respond to the user on /start with welcome message.

    Args:
        message (types.Message): message from user - /start
    """
    await message.answer(
        fmt.text(
            fmt.text(fmt.hbold('Hello, I am investing bot.')),
            fmt.text('I can calculate investment profit'),
            fmt.text('Type 4 numbers: monthly amount of investment,'),
            fmt.text('number of years, expected annual return in percentage'),
            fmt.text(' and seed money'),
            fmt.text('default seed money = monthly amount of investment.'),
            fmt.text(fmt.hbold('For example:'), '10000 10 15 50000.'),
            sep='\n',
        ),
        parse_mode='HTML',
    )


@dp.message_handler(Text(equals='Hi'))
async def cmd_hi(message: types.Message) -> None:
    """
    Responds to the user on Hi with Hi, sweetie.

    Args:
        message (types.Message): message from user - Hi
    """
    await message.answer(
        fmt.text(fmt.text(fmt.hbold('Hi, sweetie'))), parse_mode='HTML'
    )


@dp.message_handler(Text(equals='Bye'))
async def cmd_bye(message: types.Message) -> None:
    """
    Responds to the user on Bye with Okay, bye, kawai.

    Args:
        message (types.Message): message from user - Bye
    """
    await message.answer(
        fmt.text(fmt.text(fmt.hbold('Okay, bye, kawai'))), parse_mode='HTML'
    )


@dp.message_handler(content_types=['text', 'photo'])
async def cmd_main(message: types.Message) -> None:
    """
    Parse message from user and call function count_investing.

    Args:
        message (types.Message): message from user
    """
    text = message.text.split(' ')
    month_investing = int(text[0])
    count_years = int(text[1])
    percentage_return = int(text[2])
    if len(text) == 4:
        seed_money = int(text[3])
    else:
        seed_money = month_investing
    answer_message = draw_investing(
        message.from_user.id,
        month_investing,
        count_years,
        percentage_return,
        seed_money,
    )
    with open('{0}.png'.format(message.from_user.id), 'rb') as photo:
        os.remove('{0}.png'.format(message.from_user.id))
        await bot.send_photo(message.from_user.id, photo, str(answer_message))


if __name__ == '__main__':
    # start bot with skip_updates
    executor.start_polling(dp, skip_updates=True)
