from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from .utils.alphador import Alphador

periods = ["<b>1 день</b>", "<b>7 дней</b>", "<b>30 дней</b>"]

#text="🔎Сканирование"
async def scan_info(message: types.Message):
    await message.answer(f"👛Просто отправьте мне адрес криптокошелька(начинающегося с 0х) и я вышлю вам всю доступную информацию за 1, 7 и 30 дней")

#Text(startswith="0x")
async def scan(message: types.Message):
    message_edit = await message.answer("🔄Загрузка...")
    alphador = Alphador()
    await alphador.login()
    info = await alphador.wallet_analyze_full(message.text)
    await alphador.close()
    for i, period in enumerate(info):
        if not period.get("trades"): continue
        growth = [trade.get('roi') for trade in period.get('trades') if trade.get('roi')]
        growth = sum(growth) // len(growth) if growth else 0
        amount = [trade.get('trades')[-1].get('amount') for trade in period.get('trades')]
        amount = sum(amount) // len(amount) if amount else 0
        transaction = "".join(
            f"""{f'🟢' if transaction.get('pnl') > 0 else '🔴'}<b>{transaction.get('symbol')}</b>\n<b>PnL:</b> <code>{transaction.get('pnl')}$</code> <b>ROI:</b> <code>{transaction.get('roi')}%</code> <b>Trades:</b> <code>{len(transaction.get('trades'))}</code>\n""" 
            for transaction in period.get('trades')
        )
        await message.answer(f"{periods[i]}\n<b>rPnL:</b> <code>${period.get('totalPnl', 0)}</code>\n<b>uPnL:</b> <code>${period.get('totalUnrealizedProfit', 0)}</code>\n<b>Winrate:</b> <code>{period.get('tradeSuccessRatio', 0)}%</code>\n<b>ROI:</b> <code>{period.get('totalRoi', 0)}%</code>\n<b>Growth:</b> <code>{growth}%</code>\n<b>Trading Volume:</b> <code>${period.get('totalVolume')}</code>\n<b>Gas Fees:</b> <code>${period.get('totalGasUsd')}</code>\n<b>Gas per transaction:</b> <code>${period.get('totalGasUsd') // period.get('totalTrades', 1)}</code>\n<b>Total Trades:</b> <code>{period.get('totalTrades')}</code>\n<b>Total transactions:</b> <code>{period.get('totalTrades') // len(period.get('trades'))}</code>\n<b>Total tokens:</b> <code>{len(period.get('trades'))}</code>\n<b>Amount USD:</b> <code>${amount}</code>\n\n{transaction}")
    await message_edit.delete()

def register(dp: Dispatcher):
    dp.register_message_handler(scan_info, text="🔎Сканирование")
    dp.register_message_handler(scan, Text(startswith="0x"))