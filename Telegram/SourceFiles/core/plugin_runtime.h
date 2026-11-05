#pragma once

#include <filesystem>
#include <functional>
#include <memory>
#include <string>

namespace Core {

class PluginRuntime final {
public:
	PluginRuntime(
		const std::filesystem::path &python,
		const std::filesystem::path &profile,
		bool disabled);
	~PluginRuntime();

	[[nodiscard]] std::string dispatch(const std::string &request);
	void setClient(std::function<void(const std::string&)> callback);
	[[nodiscard]] unsigned int hookMask() const;

private:
	struct Private;
	std::unique_ptr<Private> _private;
};

} // namespace Core
