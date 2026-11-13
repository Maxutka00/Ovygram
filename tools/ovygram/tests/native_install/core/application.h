#pragma once

namespace Core {
class PluginRuntime;
class Application {
public:
	PluginRuntime *pluginRuntime();
};
Application &App();
} // namespace Core
