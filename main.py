from core.app import App
import plugins.pat.pat as pat
import plugins.kobe.kobe as kobe
import plugins.httpcat.httpcat as httpcat
import plugins.happiness.happiness as happiness
import plugins.battle.battle as battle
import plugins.mahjong.mahjong as mahjong
import plugins.answer.answer as answer
# import plugins.stopwatch.stopwatch as stopwatch
import plugins.guess_npc.guess_npc as guess_npc

bot = App()

bot.register_plugin(pat.pat)
bot.register_plugin(kobe.kobe)
bot.register_plugin(httpcat.httpcat)
bot.register_plugin(happiness.happiness)
bot.register_plugin(battle.battle)
bot.register_plugin(mahjong.mahjong)
bot.register_plugin(answer.answer)
# bot.register_plugin(stopwatch.stopwatch)
bot.register_plugin(guess_npc.guess_npc)

bot.run()