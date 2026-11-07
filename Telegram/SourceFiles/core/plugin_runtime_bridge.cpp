#include "core/plugin_runtime.h"
#include "core/plugin_runtime_api.h"

#ifdef _WIN32
#include <Windows.h>
#else
#include <dlfcn.h>
#endif

#include <mutex>
#include <stdexcept>

namespace Core {
namespace {

#ifdef _WIN32
using Library = HMODULE;
constexpr auto kHostFile = L"ovygram_host.dll";

[[nodiscard]] Library LoadHost(const std::filesystem::path &host) {
	const auto result = LoadLibraryExW(
		host.c_str(),
		nullptr,
		LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR | LOAD_LIBRARY_SEARCH_SYSTEM32);
	if (!result) {
		throw std::runtime_error("Python host DLL failed to load: " + std::to_string(GetLastError()));
	}
	return result;
}

[[nodiscard]] void *ResolveHost(Library library, const char *name) {
	return reinterpret_cast<void*>(GetProcAddress(library, name));
}

void UnloadHost(Library library) {
	FreeLibrary(library);
}
#else
using Library = void*;
constexpr auto kHostFile = "ovygram_host.so";

[[nodiscard]] Library LoadHost(const std::filesystem::path &host) {
	// CPython extension modules do not link libpython on Linux, they expect
	// its symbols in the global scope, so RTLD_GLOBAL is required here.
	const auto result = dlopen(host.c_str(), RTLD_NOW | RTLD_GLOBAL);
	if (!result) {
		throw std::runtime_error(std::string("Python host failed to load: ") + dlerror());
	}
	return result;
}

[[nodiscard]] void *ResolveHost(Library library, const char *name) {
	return dlsym(library, name);
}

void UnloadHost(Library library) {
	dlclose(library);
}
#endif

struct Output {
	std::string text;
	bool copied = false;
};

void CopyOutput(void *context, const char *data, std::size_t length) noexcept {
	const auto output = static_cast<Output*>(context);
	try {
		output->text.assign(data, length);
		output->copied = true;
	} catch (...) {
	}
}

} // namespace

struct PluginRuntime::Private {
	Library library = nullptr;
	void *runtime = nullptr;
	decltype(&OvygramDispatch) dispatch = nullptr;
	decltype(&OvygramDestroy) destroy = nullptr;
	decltype(&OvygramSetClient) setClient = nullptr;
	decltype(&OvygramHookMask) hookMask = nullptr;
	std::mutex mutex;
	std::function<void(const std::string&)> client;

	static int Submit(void *context, const char *data, std::size_t length) noexcept;

	~Private() {
		if (runtime) {
			destroy(runtime);
			// Keep the host mapped until exit. A plugin may have unmanaged threads.
		} else if (library) {
			UnloadHost(library);
		}
	}

};

int PluginRuntime::Private::Submit(
		void *context,
		const char *data,
		std::size_t length) noexcept {
	try {
		const auto self = static_cast<Private*>(context);
		const auto lock = std::lock_guard(self->mutex);
		if (!self->client) {
			return 0;
		}
		self->client(std::string(data, length));
		return 1;
	} catch (...) {
		return 0;
	}
}

PluginRuntime::PluginRuntime(
	const std::filesystem::path &python,
	const std::filesystem::path &profile,
	bool disabled)
: _private(std::make_unique<Private>()) {
	_private->library = LoadHost(std::filesystem::absolute(python / kHostFile));
	const auto resolve = [&](const char *name) {
		const auto address = ResolveHost(_private->library, name);
		if (!address) {
			throw std::runtime_error(std::string("Missing Python host export: ") + name);
		}
		return address;
	};
	const auto create = reinterpret_cast<decltype(&OvygramCreate)>(
		resolve("OvygramCreate"));
	_private->dispatch = reinterpret_cast<decltype(&OvygramDispatch)>(
		resolve("OvygramDispatch"));
	_private->destroy = reinterpret_cast<decltype(&OvygramDestroy)>(
		resolve("OvygramDestroy"));
	_private->setClient = reinterpret_cast<decltype(&OvygramSetClient)>(
		resolve("OvygramSetClient"));
	_private->hookMask = reinterpret_cast<decltype(&OvygramHookMask)>(
		resolve("OvygramHookMask"));
	auto result = Output();
	// Python keeps these in sys.path and data paths, which must not depend
	// on the current directory.
	const auto pythonPath = std::filesystem::absolute(python).lexically_normal();
	const auto profilePath = std::filesystem::absolute(profile).lexically_normal();
	_private->runtime = create(
		pythonPath.c_str(),
		profilePath.c_str(),
		disabled,
		CopyOutput,
		&result);
	if (!_private->runtime) {
		throw std::runtime_error(result.copied ? result.text : "Python host initialization failed.");
	}
}

PluginRuntime::~PluginRuntime() {
	setClient({});
}

void PluginRuntime::setClient(
		std::function<void(const std::string&)> callback) {
	const auto ready = bool(callback);
	{
		const auto lock = std::lock_guard(_private->mutex);
		_private->client = std::move(callback);
	}
	if (!_private->setClient(
			_private->runtime,
			ready ? Private::Submit : nullptr,
			_private.get())) {
		throw std::runtime_error("Desktop client callback setup failed.");
	}
}

std::string PluginRuntime::dispatch(const std::string &request) {
	auto result = Output();
	if (!_private->dispatch(
		_private->runtime, request.data(), request.size(), CopyOutput, &result)) {
		throw std::runtime_error(result.copied ? result.text : "Python host request failed.");
	}
	if (!result.copied) {
		throw std::bad_alloc();
	}
	return std::move(result.text);
}

unsigned int PluginRuntime::hookMask() const {
	return _private->hookMask(_private->runtime);
}

} // namespace Core
