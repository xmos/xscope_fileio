cmake_minimum_required(VERSION 3.21)
include($ENV{XMOS_CMAKE_PATH}/xcommon.cmake)
project(fileio_features_xc)

# sandbox
set(XMOS_SANDBOX_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../../..)

# target ans srcs
set(APP_HW_TARGET XCORE-AI-EXPLORER)
set(APP_XC_SRCS test.xc)

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
