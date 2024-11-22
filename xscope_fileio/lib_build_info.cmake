function(install_if_not_installed lib_name lib_version)
    find_package(Python COMPONENTS Interpreter REQUIRED)
    if(DEFINED ENV{VIRTUAL_ENV} OR DEFINED ENV{CONDA_PREFIX})
        execute_process(
            COMMAND ${Python_EXECUTABLE} -c "import pkg_resources; pkg_resources.require('${lib_name}==${lib_version}')"
            RESULT_VARIABLE pkg_check_result
            OUTPUT_QUIET
            ERROR_QUIET
        )
        if(NOT pkg_check_result EQUAL 0)
            execute_process(COMMAND ${Python_EXECUTABLE} -m pip install ${lib_name}==${lib_version} COMMAND_ERROR_IS_FATAL ANY)
            message(STATUS "Installing ${lib_name} ${lib_version} using pip")
        else()
            message(STATUS "${lib_name} ${lib_version} is already installed")
        endif()
    endif()
endfunction()

set(LIB_NAME xscope_fileio)
set(LIB_VERSION 1.3.0)
set(LIB_INCLUDES api .)
set(LIB_DEPENDENT_MODULES "")
install_if_not_installed(${LIB_NAME} ${LIB_VERSION})
XMOS_REGISTER_MODULE()
