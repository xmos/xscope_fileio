cmake_minimum_required(VERSION 3.21)
include($ENV{XMOS_CMAKE_PATH}/xcommon.cmake)
project(fileio_test)

# sandbox
set(XMOS_SANDBOX_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../../..)
message(STATUS "XMOS_SANDBOX_DIR: ${XMOS_SANDBOX_DIR}")

# target ans srcs
set(APP_HW_TARGET XCORE-AI-EXPLORER)
set(APP_XC_SRCS main.xc)
set(APP_C_SRCS test.c)

# flags
set(APP_COMPILER_FLAGS
  -Os
  -g
  -report
  -Wall
  -fxscope
  -Wno-xcore-fptrgroup
)
set(APP_XSCOPE_SRCS config.xscope)
set(APP_DEPENDENT_MODULES  xscope_fileio)
XMOS_REGISTER_APP()
