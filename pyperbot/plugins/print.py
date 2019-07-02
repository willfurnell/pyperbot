from pyperbot.wrappers import plugin, unload, onload, command

from escpos.printer import Network


@plugin
class printr:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.printer = None

    @onload
    def onload(self):
        self.printer = Network(self.config.get('printer'))

    @unload
    def unload(self):
        self.printer = None

    @command("print")
    def printr(self, msg):
        self.printer.text(msg.text)
        self.printer.cut()
        return msg.reply(text="Printed!")

