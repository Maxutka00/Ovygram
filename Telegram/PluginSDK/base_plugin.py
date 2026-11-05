"""Plugin lifecycle and persistent settings for Ovygram."""


class BasePlugin:
    def on_plugin_load(self):
        pass

    def on_plugin_unload(self):
        pass

    def create_settings(self):
        return []

    def get_setting(self, key, default=None):
        return self._desktop_context.get(key, default)

    def set_setting(self, key, value):
        self._desktop_context.set(key, value)

    def get_account_setting(self, account_id, key, default=None):
        return self._desktop_context.get(key, default, account_id)

    def set_account_setting(self, account_id, key, value):
        self._desktop_context.set(key, value, account_id)

    def log(self, message):
        self._desktop_context.log(str(message))

    def subscribe(self, event, callback, priority=0):
        return self._desktop_context.manager.runtime.register(
            self._desktop_context, event, callback, priority)

    def add_hook(self, point, callback, priority=0, request=None):
        return self._desktop_context.manager.runtime.register(
            self._desktop_context, point, callback, priority, request)

    def run_async(self, coroutine):
        return self._desktop_context.manager.runtime.schedule(self._desktop_context, coroutine)
