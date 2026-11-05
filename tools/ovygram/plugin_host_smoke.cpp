#include "core/plugin_runtime.h"

#include <iostream>
#include <string_view>

int wmain(int argc, wchar_t **argv) {
	if (argc != 3) {
		return 2;
	}
	try {
		const auto python = std::filesystem::path(argv[0]).parent_path() / L"python";
		auto host = Core::PluginRuntime(python, argv[1], std::wstring_view(argv[2]) == L"disabled");
		for (auto line = std::string(); std::getline(std::cin, line);) {
			std::cout << host.dispatch(line) << std::endl;
		}
	} catch (const std::exception &error) {
		std::cerr << error.what() << std::endl;
		return 1;
	}
	return 0;
}
