cmake_minimum_required(VERSION 3.11)

# Compile for x86_64 on Mac as we can't support the M1 ARM architecture yet
set(CMAKE_OSX_ARCHITECTURES "x86_64" CACHE INTERNAL "")

project(xscope_fileio)

add_executable(xscope_host_endpoint xscope_io_host.c)

set_property(TARGET xscope_host_endpoint PROPERTY C_STANDARD 99)

target_include_directories(xscope_host_endpoint PRIVATE ../xscope_fileio
                                                        $ENV{XMOS_TOOL_PATH}/include)

find_library(XSCOPE_ENDPOINT_LIB NAMES xscope_endpoint.so xscope_endpoint.lib
                                 PATHS $ENV{XMOS_TOOL_PATH}/lib)

target_link_libraries(xscope_host_endpoint PRIVATE ${XSCOPE_ENDPOINT_LIB})
