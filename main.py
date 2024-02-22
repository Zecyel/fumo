from core.app import App
import plugins.pat.pat as pat
import plugins.kobe.kobe as kobe
import plugins.httpcat.httpcat as httpcat
import plugins.happiness.happiness as happiness

bot = App()

bot.register_plugin(pat.pat)
bot.register_plugin(kobe.kobe)
bot.register_plugin(httpcat.httpcat)
bot.register_plugin(happiness.happiness)

bot.run()