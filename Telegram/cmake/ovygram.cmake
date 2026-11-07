set(OVYGRAM_PYTHON_ROOT "" CACHE PATH "Pinned Ovygram Python bundle")
option(OVYGRAM_SYSTEM_PYTHON "Link the system Python instead of the bundled one (Linux)." OFF)
if (NOT OVYGRAM_PYTHON_ROOT)
    return()
endif()

if (NOT (WIN32 OR LINUX) OR NOT CMAKE_SIZEOF_VOID_P EQUAL 8)
    message(FATAL_ERROR "Ovygram Python requires Windows or Linux x64.")
endif()

if (OVYGRAM_SYSTEM_PYTHON AND NOT LINUX)
    message(FATAL_ERROR "OVYGRAM_SYSTEM_PYTHON is supported only on Linux.")
endif()

set(plugin_python ${OVYGRAM_PYTHON_ROOT})

target_sources(Telegram PRIVATE
    SourceFiles/api/api_plugins.cpp
    SourceFiles/api/api_plugins.h
    SourceFiles/core/plugin_runtime_bridge.cpp
    SourceFiles/core/plugin_runtime_api.h
    SourceFiles/core/plugin_runtime.h
    SourceFiles/ovygram/chat_bars.h
    SourceFiles/ovygram/chat_decorations.cpp
    SourceFiles/ovygram/chat_list_filter.cpp
    SourceFiles/ovygram/chat_list_filter.h
    SourceFiles/ovygram/chat_decorations.h
    SourceFiles/ovygram/message_decorations.cpp
    SourceFiles/ovygram/message_decorations.h
    SourceFiles/ovygram/plugin_elements.cpp
    SourceFiles/ovygram/plugin_elements.h
    SourceFiles/ovygram/plugin_menus.cpp
    SourceFiles/ovygram/plugin_menus.h
    SourceFiles/ovygram/plugin_paint.cpp
    SourceFiles/ovygram/plugin_paint.h
    SourceFiles/ovygram/plugin_section.cpp
    SourceFiles/ovygram/plugin_section.h
    SourceFiles/ovygram/plugin_ui.cpp
    SourceFiles/ovygram/plugin_widgets.cpp
    SourceFiles/ovygram/plugin_widgets.h
    SourceFiles/ovygram/plugin_ui.h
    SourceFiles/settings/sections/settings_plugins.cpp
    SourceFiles/settings/sections/settings_plugins.h
)
target_compile_definitions(Telegram PRIVATE OVYGRAM_ENABLED)
target_link_libraries(Telegram PRIVATE ${CMAKE_DL_LIBS})

# Keep Telegram's system-only load policy for ordinary imports. The application
# loads this bridge from its private Python directory using an absolute path.
add_library(ovygram_host SHARED
    SourceFiles/core/plugin_runtime.cpp
    SourceFiles/core/plugin_runtime_exports.cpp
)
target_compile_features(ovygram_host PRIVATE cxx_std_20)
# The host shares class names with the bridge in Telegram, so on Linux only the
# C API may be exported, or the dynamic linker could bind them to each other.
set_target_properties(ovygram_host PROPERTIES
    PREFIX ""
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN ON
    MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
target_include_directories(ovygram_host PRIVATE SourceFiles)
target_include_directories(ovygram_host SYSTEM PRIVATE
    "${plugin_python}/pybind11/include"
)

if (OVYGRAM_SYSTEM_PYTHON)
    find_package(Python3 3.13 REQUIRED COMPONENTS Development.Embed)
    target_compile_definitions(ovygram_host PRIVATE OVYGRAM_SYSTEM_PYTHON)
    target_link_libraries(ovygram_host PRIVATE Python3::Python)
else()
    if (WIN32)
        set(plugin_python_library python313.lib)
    else()
        set(plugin_python_library libpython3.13.so)
    endif()
    target_include_directories(ovygram_host SYSTEM PRIVATE
        "${plugin_python}/tools/include"
    )
    target_link_directories(ovygram_host PRIVATE "${plugin_python}/tools/libs")
    target_link_libraries(ovygram_host PRIVATE "${plugin_python}/tools/libs/${plugin_python_library}")

    if (WIN32)
        target_link_options(ovygram_host PRIVATE /DEPENDENTLOADFLAG:0)
    else()
        set_target_properties(ovygram_host PROPERTIES
            BUILD_WITH_INSTALL_RPATH ON
            INSTALL_RPATH "$ORIGIN")
    endif()
endif()

add_dependencies(Telegram ovygram_host)
add_custom_command(TARGET Telegram POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        "${plugin_python}/python" "$<TARGET_FILE_DIR:Telegram>/python"
    # The bundle holds the SDK from the time it was staged; use the current one.
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        "${CMAKE_CURRENT_SOURCE_DIR}/PluginSDK" "$<TARGET_FILE_DIR:Telegram>/python/sdk"
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "$<TARGET_FILE:ovygram_host>"
        "$<TARGET_FILE_DIR:Telegram>/python/$<TARGET_FILE_NAME:ovygram_host>"
    VERBATIM
)
