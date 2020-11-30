.PHONY: default_
default_: all

GCC ?= gcc

xscope_host_endpoint : xscope_io_host.c
	$(GCC) -o $@ $< -I ../xscope_file_io_device -I ${XMOS_TOOL_PATH}/include ${XMOS_TOOL_PATH}/lib/xscope_endpoint.so -std=c99

.PHONY: all
all: xscope_host_endpoint

.PHONY: clean
clean:
	rm -f xscope_host_endpoint

