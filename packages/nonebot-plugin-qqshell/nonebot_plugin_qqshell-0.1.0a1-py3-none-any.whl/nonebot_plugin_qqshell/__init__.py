from nonebot import require
require("nonebot_plugin_htmlrender")

from nonebot.plugin import PluginMetadata

from .config import Config
from .handler import shell_handler

__plugin_meta__ = PluginMetadata(
    name="QQShell 是一个类 WebSSH、XShell 的运行在机器人的 SSH Shell，在 QQ 中自由运行你的命令吧",
    description=(
        "QQShell 能执行任何你所能想到的服务器命令\n"
        "   >shell cd /\n"
        "   >shell pwd\n"
        "   >shell su\n"
    ),
    usage=">shell <你的指令>",
    config=Config,
    homepage="https://github.com/yejue/nonebot-plugin-qqshell.git",
    type="application",
    supported_adapters={"~onebot.v11"}
)
