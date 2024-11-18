cmake_minimum_required(VERSION 3.21)
project(xscope_fileio)

# Set build type to Release if not set
set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build." FORCE)

# Add executable and set C standard
add_executable(xscope_host_endpoint xscope_io_host.c)
set_property(TARGET xscope_host_endpoint PROPERTY C_STANDARD 99)

# Set the output directory to the same directory as the CMake file
set_target_properties(xscope_host_endpoint PROPERTIES
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}"
)

# Include directories
target_include_directories(
  xscope_host_endpoint 
  PRIVATE ../xscope_fileio $ENV{XMOS_TOOL_PATH}/include
)

# Find the xscope endpoint library
find_library(
  XSCOPE_ENDPOINT_LIB
  NAMES xscope_endpoint.so xscope_endpoint.lib
  PATHS $ENV{XMOS_TOOL_PATH}/lib
)

# Check if the library was found and link it
if (XSCOPE_ENDPOINT_LIB)
  target_link_libraries(xscope_host_endpoint PRIVATE ${XSCOPE_ENDPOINT_LIB})
  message(STATUS "Found xscope endpoint library: ${XSCOPE_ENDPOINT_LIB}")
else ()
  message(FATAL_ERROR "xscope endpoint library not found in XMOS_TOOL_PATH/lib.")
endif ()
