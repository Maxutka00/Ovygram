#include <pybind11/embed.h>

#include "core/plugin_runtime.h"

#include <mutex>
#include <stdexcept>

namespace Core {
namespace {

namespace py = pybind11;

struct NativeClient {
	std::mutex mutex;
	std::function<void(const std::string&)> submit;

};

std::mutex NativeClientMutex;
std::weak_ptr<NativeClient> ActiveNativeClient;

PYBIND11_EMBEDDED_MODULE(_ovygram_native, module) {
	module.def("submit", [](const std::string &request) {
		auto client = std::shared_ptr<NativeClient>();
		{
			const auto lock = std::lock_guard(NativeClientMutex);
			client = ActiveNativeClient.lock();
		}
		if (!client) {
			throw std::runtime_error("Desktop client has stopped.");
		}
		const auto lock = std::lock_guard(client->mutex);
		if (!client->submit) {
			throw std::runtime_error("Desktop client is unavailable.");
		}
		client->submit(request);
	});
}

void CheckStatus(PyStatus status) {
	if (PyStatus_Exception(status)) {
		throw std::runtime_error(status.err_msg ? status.err_msg : "Python initialization failed");
	}
}

void InitializePython(const std::filesystem::path &directory) {
	if (!std::filesystem::is_regular_file(directory / L"python313.zip")
		|| !std::filesystem::is_regular_file(directory / L"sdk/ovygram_runtime.py")) {
		throw std::runtime_error("Bundled Python or Plugin SDK is missing.");
	}
	PyConfig config;
	PyConfig_InitIsolatedConfig(&config);
	config.install_signal_handlers = 0;
	config.configure_c_stdio = 0;
	config.site_import = 0;
	config.write_bytecode = 0;
	config.module_search_paths_set = 1;
	try {
		CheckStatus(PyConfig_SetString(&config, &config.home, directory.c_str()));
		const auto executable = directory / L"python.exe";
		CheckStatus(PyConfig_SetString(&config, &config.executable, executable.c_str()));
		for (const auto *name : { L"python313.zip", L".", L"sdk" }) {
			const auto path = directory / name;
			CheckStatus(PyWideStringList_Append(&config.module_search_paths, path.c_str()));
		}
	} catch (...) {
		PyConfig_Clear(&config);
		throw;
	}
	py::initialize_interpreter(&config, 0, nullptr, false);
}

} // namespace

struct PluginRuntime::Private {
	py::object manager;
	PyThreadState *threadState = nullptr;
	std::shared_ptr<NativeClient> client = std::make_shared<NativeClient>();

};

PluginRuntime::PluginRuntime(
	const std::filesystem::path &python,
	const std::filesystem::path &profile,
	bool disabled)
: _private(std::make_unique<Private>()) {
	if (Py_IsInitialized()) {
		throw std::logic_error("Ovygram requires one Python interpreter.");
	}
	auto failure = std::string();
	try {
		InitializePython(python);
		{
			const auto lock = std::lock_guard(NativeClientMutex);
			ActiveNativeClient = _private->client;
		}
		_private->manager = py::module_::import("ovygram_runtime")
			.attr("Manager")(profile.wstring(), disabled);
		_private->threadState = PyEval_SaveThread();
	} catch (const std::exception &error) {
		failure = error.what();
		_private.reset();
	}
	if (!_private) {
		if (Py_IsInitialized()) {
			py::finalize_interpreter();
		}
		throw std::runtime_error(failure);
	}
}

PluginRuntime::~PluginRuntime() {
	setClient({});
	PyEval_RestoreThread(_private->threadState);
	auto finalize = false;
	try {
		_private->manager.attr("shutdown")();
		finalize = py::len(py::module_::import("threading").attr("enumerate")()) == 1;
	} catch (const std::exception &) {
		// The Python side leaves the crash marker when shutdown is incomplete.
	}
	_private.reset();
	if (finalize) {
		py::finalize_interpreter();
	} else {
		// A plugin can own unmanaged threads. The process is already exiting.
		PyEval_SaveThread();
	}
}

void PluginRuntime::setClient(
		std::function<void(const std::string&)> callback) {
	const auto ready = bool(callback);
	{
		const auto lock = std::lock_guard(_private->client->mutex);
		_private->client->submit = std::move(callback);
	}
	if (ready) {
		const auto lock = py::gil_scoped_acquire();
		_private->manager.attr("runtime").attr("ready").attr("set")();
	}
}

std::string PluginRuntime::dispatch(const std::string &request) {
	const auto lock = py::gil_scoped_acquire();
	try {
		return _private->manager.attr("dispatch")(request).cast<std::string>();
	} catch (const std::exception &error) {
		throw std::runtime_error(error.what());
	}
}

unsigned int PluginRuntime::hookMask() const {
	const auto lock = py::gil_scoped_acquire();
	return _private->manager.attr("runtime").attr("hook_mask").cast<unsigned int>();
}

} // namespace Core
