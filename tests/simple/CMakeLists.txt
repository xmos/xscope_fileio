cmake_minimum_required(VERSION 3.23)
include($ENV{XMOS_CMAKE_PATH}/xcommon.cmake)
project(test_simple)

# sandbox
set(XMOS_SANDBOX_DIR ${CMAKE_CURRENT_LIST_DIR}/../../..)
message("XMOS_SANDBOX_DIR: ${XMOS_SANDBOX_DIR}")

# target
if(CMAKE_C_COMPILER_VERSION VERSION_EQUAL "3.6.0") # XS3 (XTC 15.3.1)
set(APP_HW_TARGET XK-EVK-XU316)
else() # vx4
set(APP_HW_TARGET XK-EVK-XU416)
endif()

# flags
set(APP_COMPILER_FLAGS
  -Os
  -g
  -report
  -Wall
  -fxscope
)

#deps
set(APP_DEPENDENT_MODULES  xscope_fileio)

XMOS_REGISTER_APP()
