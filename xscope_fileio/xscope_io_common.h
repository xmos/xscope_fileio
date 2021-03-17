// Copyright (c) 2020, XMOS Ltd, All rights reserved
#ifndef XSCOPE_IO_COMMON_H_
#define XSCOPE_IO_COMMON_H_

#define MAX_XSCOPE_SIZE_BYTES   256
#define END_MARKER_STRING       "finally_the_end!!" //17 * 8 = 136 bits of unlikely data 
#define END_MARKER_LEN          (sizeof(END_MARKER_STRING) - 1)
#define MAX_FILENAME_LEN        64
#define MAX_FILES_OPEN          32

typedef enum{
    XSCOPE_IO_READ_BINARY=0,
    XSCOPE_IO_READ_TEXT,
    XSCOPE_IO_WRITE_BINARY,
    XSCOPE_IO_WRITE_TEXT,
} xscope_file_mode_t;

enum{
    XSCOPE_ID_OPEN_FILE     = 0,
    XSCOPE_ID_READ_BYTES    = 1,
    XSCOPE_ID_WRITE_SETUP   = 2,
    XSCOPE_ID_WRITE_BYTES   = 3,
    XSCOPE_ID_SEEK          = 4,
    XSCOPE_ID_TELL          = 5,
    XSCOPE_ID_HOST_QUIT     = 6, 
};

#endif