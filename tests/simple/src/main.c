// Copyright 2024-2025 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <platform.h>
#include <xscope.h>
#include <xcore/assert.h>

#include "xscope_io_device.h"

void main_tile0()
{
    // create a random array in data_in
    const char filename[] = "test_file.out";
    const size_t buff_size = 256;
    uint8_t data_in[buff_size];
    uint8_t data_out[buff_size];
    for (int i = 0; i < buff_size; i++) {
        data_in[i] = rand() % 256;
    }

    // write the data to a file
    xscope_file_t fp = xscope_open_file(filename, "wb");
    xscope_fwrite(&fp, data_in, buff_size);
    xscope_fclose(&fp);

    // open the file again and read the data back and compare
    xscope_file_t fp2 = xscope_open_file(filename, "rb");
    xscope_fread(&fp2, data_out, buff_size);
    xscope_fclose(&fp2);
    for (int i = 0; i < buff_size; i++) {
        xassert(data_in[i] == data_out[i]);
    }
    printf("Data read back matches data written\n");
}

int main(){
    chanend_t xscope_chan = chanend_alloc();
    xscope_io_init(xscope_chan);
    main_tile0();
    xscope_close_all_files();
    chanend_free(xscope_chan);
    return 0;
}
