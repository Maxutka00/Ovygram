set(OVYGRAM_PYTHON_ROOT "" CACHE PATH "Pinned Ovygram Python bundle")
if (NOT OVYGRAM_PYTHON_ROOT)
    return()
endif()

if (NOT WIN32 OR NOT CMAKE_SIZEOF_VOID_P EQUAL 8)
    message(FATAL_ERROR "Ovygram Python requires Windows x64.")
endif()

set(plugin_python ${OVYGRAM_PYTHON_ROOT})
target_sources(Telegram PRIVATE
    SourceFiles/api/api_plugins.cpp
    SourceFiles/api/api_plugins.h
    SourceFiles/core/plugin_runtime_bridge.cpp
    SourceFiles/core/plugin_runtime_api.h
    SourceFiles/core/plugin_runtime.h
    SourceFiles/settings/sections/settings_plugins.cpp
    SourceFiles/settings/sections/settings_plugins.h
)
target_compile_definitions(Telegram PRIVATE OVYGRAM_ENABLED)

# Keep Telegram's system-only load policy for ordinary imports. The application
# loads this bridge from its private Python directory using an absolute path.
add_library(ovygram_host SHARED
    SourceFiles/core/plugin_runtime.cpp
    SourceFiles/core/plugin_runtime_exports.cpp
)
target_compile_features(ovygram_host PRIVATE cxx_std_20)
set_target_properties(ovygram_host PROPERTIES
    MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
target_include_directories(ovygram_host PRIVATE SourceFiles)
target_include_directories(ovygram_host SYSTEM PRIVATE
    "${plugin_python}/tools/include"
    "${plugin_python}/pybind11/include"
)
target_link_directories(ovygram_host PRIVATE "${plugin_python}/tools/libs")
target_link_libraries(ovygram_host PRIVATE "${plugin_python}/tools/libs/python313.lib")
target_link_options(ovygram_host PRIVATE /DEPENDENTLOADFLAG:0)
add_dependencies(Telegram ovygram_host)
add_custom_command(TARGET Telegram POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        "${plugin_python}/python" "$<TARGET_FILE_DIR:Telegram>/python"
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "$<TARGET_FILE:ovygram_host>"
        "$<TARGET_FILE_DIR:Telegram>/python/ovygram_host.dll"
    VERBATIM
)
