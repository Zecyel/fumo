from core.app import App
from plugins.pat.pat import pat
from plugins.kobe.kobe import kobe
from plugins.httpcat.httpcat import httpcat
from plugins.httpdog.httpdog import httpdog
from plugins.happiness.happiness import happiness
from plugins.battle.battle import battle
from plugins.mahjong.mahjong import mahjong
from plugins.answer.answer import answer
from plugins.stopwatch.stopwatch import stopwatch
from plugins.guess_npc.guess_npc import guess_npc
from plugins.tingpai.tingpai import tingpai
from plugins.coin.coin import coin
from plugins.pray.pray import pray
from plugins.repeat.repeat import repeat
from plugins.score.score import score

bot = App()

bot.register_plugin(pat)
bot.register_plugin(kobe)
bot.register_plugin(httpcat)
bot.register_plugin(httpdog)
bot.register_plugin(happiness)
# bot.register_plugin(battle)
bot.register_plugin(mahjong)
bot.register_plugin(answer)
bot.register_plugin(stopwatch)
bot.register_plugin(guess_npc)
bot.register_plugin(tingpai)
bot.register_plugin(coin)
bot.register_plugin(pray)
bot.register_plugin(repeat)
bot.register_plugin(score)

bot.run()