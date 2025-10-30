import pkgutil
import importlib
import inspect
import telegram.mods as handlers_package
from telegram.core.bot.handler import Handler, CallbackHandler

def load_handlers(bot):
    handlers = []

    def walk_modules(package):
        for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
            module = importlib.import_module(module_name)

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and (
                    (issubclass(obj, Handler) and obj is not Handler) or
                    (issubclass(obj, CallbackHandler) and obj is not CallbackHandler)
                ):
                    handler_instance = obj(bot)
                    handlers.append(handler_instance)

                    class_name = handler_instance.__class__.__name__

                    # فقط اگر دقیقا subclass از Handler هست
                    if isinstance(handler_instance, Handler):
                        bot.message_handler(func=handler_instance.check)(handler_instance.handle)
                        print(f"✅ Registered MessageHandler: {class_name}")

                    # فقط اگر دقیقا subclass از CallbackHandler هست
                    if isinstance(handler_instance, CallbackHandler):
                        bot.callback_query_handler(func=handler_instance.callback_check)(handler_instance.handle)
                        print(f"✅ Registered CallbackHandler: {class_name}")

            if is_pkg:
                subpackage = importlib.import_module(module_name)
                walk_modules(subpackage)

    walk_modules(handlers_package)
    return handlers
