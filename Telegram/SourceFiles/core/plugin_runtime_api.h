#pragma once

#include <cstddef>
#include <filesystem>

using OvygramOutput = void (*)(void*, const char*, std::size_t) noexcept;
using OvygramSubmit = int (*)(void*, const char*, std::size_t) noexcept;
using OvygramPathChar = std::filesystem::path::value_type;

#if !defined(OVYGRAM_HOST_EXPORTS)
#define OVYGRAM_HOST_API
#elif defined(_WIN32)
#define OVYGRAM_HOST_API __declspec(dllexport)
#else
#define OVYGRAM_HOST_API __attribute__((visibility("default")))
#endif

extern "C" {
OVYGRAM_HOST_API void *OvygramCreate(
	const OvygramPathChar *python,
	const OvygramPathChar *profile,
	int disabled,
	OvygramOutput output,
	void *context) noexcept;
OVYGRAM_HOST_API int OvygramDispatch(
	void *runtime,
	const char *request,
	std::size_t length,
	OvygramOutput output,
	void *context) noexcept;
OVYGRAM_HOST_API void OvygramDestroy(void *runtime) noexcept;
OVYGRAM_HOST_API int OvygramSetClient(
	void *runtime,
	OvygramSubmit callback,
	void *context) noexcept;
OVYGRAM_HOST_API unsigned int OvygramHookMask(void *runtime) noexcept;
}

#undef OVYGRAM_HOST_API
