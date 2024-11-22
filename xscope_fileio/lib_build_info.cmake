set(LIB_NAME xscope_fileio)
set(LIB_VERSION 1.3.1)
set(LIB_INCLUDES api .)
set(LIB_DEPENDENT_MODULES "")

find_package(Python COMPONENTS Interpreter REQUIRED)
if(DEFINED ENV{VIRTUAL_ENV} OR DEFINED ENV{CONDA_PREFIX})
    execute_process(COMMAND ${Python_EXECUTABLE} -m pip install xscope-fileio==${LIB_VERSION})
    message(STATUS "Installing xscope-fileio ${LIB_VERSION} using pip")
endif()

XMOS_REGISTER_MODULE()
