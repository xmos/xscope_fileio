cmake_minimum_required(VERSION 3.23)
include($ENV{XMOS_CMAKE_PATH}/xcommon.cmake)
project(fileio_test)

# sandbox
set(XMOS_SANDBOX_DIR ${CMAKE_CURRENT_LIST_DIR}/../../..)

# target ans srcs
set(APP_HW_TARGET XCORE-AI-EXPLORER)

# flags
set(APP_COMPILER_FLAGS
  -Os
  -g
  -report
  -Wall
  -fxscope
  -Wno-xcore-fptrgroup
)

# deps
set(APP_DEPENDENT_MODULES  xscope_fileio)

XMOS_REGISTER_APP()
