TARGET_FLAG ?= -target=XCORE-AI-EXPLORER
TARGET_EXEC ?= fileio_test.xe

XCC ?= xcc

SRCS := main.xc test.c ../../xscope_fileio/src/xscope_io_device.c
INC_DIRS += $(dir $(SRCS)) ../../xscope_fileio/api ../../xscope_fileio
INC_FLAGS := $(addprefix -I,$(INC_DIRS))

BUILD_DIR := build
OBJS := $(SRCS:%=$(BUILD_DIR)/%.o)
DEPS := $(OBJS:.o=.d)

CFLAGS := -c $(INC_FLAGS) $(TARGET_FLAG) -Os -g
XCFLAGS := $(CFLAGS)

$(TARGET_EXEC): $(OBJS) config.xscope
# 	@echo "**HELLO LINKER**"
	$(XCC) $(TARGET_FLAG) -o $@ $^ -report

# c source
$(BUILD_DIR)/%.c.o: %.c
	$(MKDIR_P) $(dir $@)
# 	@echo "**HELLO C**"
	$(XCC) $(CFLAGS) -c $< -o $@

# xc source
$(BUILD_DIR)/%.xc.o: %.xc
	$(MKDIR_P) $(dir $@)
# 	@echo "**HELLO XC**"
	$(XCC) $(XCFLAGS) -c $< -o $@

# asm source
$(BUILD_DIR)/%.S.o: %.S
	$(MKDIR_P) $(dir $@)
# 	@echo "**HELLO ASM**"
	$(XCC) $(ASMFLAGS) -c $< -o $@

.PHONY: clean

clean:
	$(RM) -r build
	$(RM) $(TARGET_EXEC)

-include $(DEPS)

MKDIR_P ?= mkdir -p
