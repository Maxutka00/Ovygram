#define OVYGRAM_HOST_EXPORTS
#include "core/plugin_runtime_api.h"
#undef OVYGRAM_HOST_EXPORTS
#include "core/plugin_runtime.h"

#include <cstring>
#include <stdexcept>

extern "C" void *OvygramCreate(
	const wchar_t *python,
	const wchar_t *profile,
	int disabled,
	OvygramOutput output,
	void *context) noexcept {
	try {
		return new Core::PluginRuntime(python, profile, disabled != 0);
	} catch (const std::exception &error) {
		output(context, error.what(), std::strlen(error.what()));
		return nullptr;
	} catch (...) {
		return nullptr;
	}
}

extern "C" int OvygramDispatch(
	void *runtime,
	const char *request,
	std::size_t length,
	OvygramOutput output,
	void *context) noexcept {
	try {
		const auto result = static_cast<Core::PluginRuntime*>(runtime)->dispatch(
			std::string(request, length));
		output(context, result.data(), result.size());
		return 1;
	} catch (const std::exception &error) {
		output(context, error.what(), std::strlen(error.what()));
		return 0;
	} catch (...) {
		return 0;
	}
}

extern "C" void OvygramDestroy(void *runtime) noexcept {
	delete static_cast<Core::PluginRuntime*>(runtime);
}

extern "C" int OvygramSetClient(
		void *runtime,
		OvygramSubmit callback,
		void *context) noexcept {
	try {
		if (callback) {
			static_cast<Core::PluginRuntime*>(runtime)->setClient(
				[=](const std::string &request) {
					if (!callback(context, request.data(), request.size())) {
						throw std::runtime_error("Desktop client is unavailable.");
					}
				});
		} else {
			static_cast<Core::PluginRuntime*>(runtime)->setClient({});
		}
		return 1;
	} catch (...) {
		return 0;
	}
}

extern "C" unsigned int OvygramHookMask(void *runtime) noexcept {
	try {
		return static_cast<Core::PluginRuntime*>(runtime)->hookMask();
	} catch (...) {
		return 0;
	}
}
