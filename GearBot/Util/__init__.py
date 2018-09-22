import importlib

from database import DatabaseConnector
from . import Configuration, Converters, GearbotLogging, Pages, Permissioncheckers, Utils, VersionInfo, Confirmation, \
    HelpGenerator, Emoji, InfractionUtils, Archive, Translator, DocUtils, GlobalHandlers, JumboGenerator

components = [
    Configuration,
    DatabaseConnector,
    Converters,
    GearbotLogging,
    Permissioncheckers,
    Utils,
    VersionInfo,
    Emoji,
    Confirmation,
    HelpGenerator,
    Pages,
    InfractionUtils,
    Archive,
    Translator,
    DocUtils,
    GlobalHandlers,
    JumboGenerator
]

async def reload(bot):
    log_cache = GearbotLogging.LOG_CACHE
    for c in components:
        importlib.reload(c)
    prepDatabase(bot)
    await readyBot(bot)
    GearbotLogging.LOG_CACHE = log_cache

async def readyBot(bot):
    await Configuration.on_ready(bot)
    Emoji.on_ready(bot)
    Confirmation.on_ready(bot)
    Pages.on_ready(bot)
    Utils.on_ready(bot)
    Translator.on_ready(bot)
    bot.data = {
        "forced_exits": set(),
        "unbans": set(),
        "message_deletes": set()
    }
    await GearbotLogging.onReady(bot, Configuration.get_master_var("BOT_LOG_CHANNEL"))

def prepDatabase(bot):
    GearbotLogging.info("Connecting to the database.")
    DatabaseConnector.init()
    bot.database_connection = DatabaseConnector.connection
    GearbotLogging.info("Database connection established.")