#include "core/plugin_runtime.h"

#include <iostream>

#ifdef _WIN32
int wmain(int argc, wchar_t **argv) {
#else
int main(int argc, char **argv) {
#endif
	if (argc != 3) {
		return 2;
	}
	try {
		const auto python = std::filesystem::path(argv[0]).parent_path() / L"python";
		const auto disabled = (std::filesystem::path(argv[2]) == L"disabled");
		auto host = Core::PluginRuntime(python, argv[1], disabled);
		for (auto line = std::string(); std::getline(std::cin, line);) {
			std::cout << host.dispatch(line) << std::endl;
		}
	} catch (const std::exception &error) {
		std::cerr << error.what() << std::endl;
		return 1;
	}
	return 0;
}
