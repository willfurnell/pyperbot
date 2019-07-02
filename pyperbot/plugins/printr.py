from pyperbot.wrappers import plugin, unload, onload, command

from escpos.printer import Network


@plugin
class Printr:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.printer = self.config.get("printer")
        self.p = None

    @onload
    def onload(self):
        self.p = Network(self.printer)
        print("printer loaded")

    @unload
    def unload(self):
        self.p = None

    @command("print")
    def printr(self, msg):
        self.p.text(msg.text)
        self.p.cut()
        return msg.reply(text="Printed!")
