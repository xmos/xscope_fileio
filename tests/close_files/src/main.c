// Copyright 2024-2025 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.
#include <platform.h>
#include <stdio.h>
#include <string.h>
#include <xscope.h>
#include <xcore/assert.h>
#include <xcore/hwtimer.h>
#include "xscope_io_device.h"


// This test will open and close some files in different order.
// then it will reclose all files.
static
void test_close_unordered(chanend_t xscope_chan)
{
    xscope_file_t fp[5];

    // open and close some files
    fp[0] = xscope_open_file("output/fp0.out", "wb");
    fp[1] = xscope_open_file("output/fp1.out", "wb");
    fp[2] = xscope_open_file("output/fp2.out", "wb");
    xscope_fclose(&fp[0]);
    fp[3] = xscope_open_file("output/fp3.out", "wb");
    xscope_fclose(&fp[2]);
    fp[4] = xscope_open_file("output/fp4.out", "wb");    
    xscope_fclose(&fp[1]);

    // close all files
    for (int i = 0; i < 5; i++) {
        xscope_fclose(&fp[i]);
    }
}


// This test will create a large number of files (N_FILES) and write some data to them.
// It will reuse the same file pointer.
static
void test_open_close_continously(chanend_t xscope_chan){
    
    const unsigned N_FILES = 240;       // number of files that will be created

    const unsigned BUFF_SIZE = 1024;    // size of data buffer to write to each file
    uint8_t data[BUFF_SIZE] = {0};

    for (unsigned file_n = 0; file_n < N_FILES; file_n++){
        char filename[24];
        snprintf(filename, 24, "output/file_%d.out", file_n);
        printf("%s\n", filename);

        xscope_file_t fp = xscope_open_file(filename, "wb");
        data[0] = file_n; // first index of data is the file number
        xscope_fwrite(&fp, data, BUFF_SIZE);
        xscope_fclose(&fp);
    }

}


// This test will open a file that was previously closed, and write some data to it.
// The idea is to ensure that we can open and close reusing the same file pointer
// and change the data to write to the file.
static
void test_open_a_closed_file(chanend_t xscope_chan){
    const char *filename = "output/test_open_a_closed_file.out";
    const unsigned BUFF_SIZE = 1024;    // size of data buffer to write to each file
    uint8_t data[BUFF_SIZE] = {0};

    // create a file and write some data to it
    xscope_file_t fp = xscope_open_file(filename, "wb");
    memset(data, 0, BUFF_SIZE);
    xscope_fwrite(&fp, data, BUFF_SIZE);
    xscope_fclose(&fp);

    xscope_open_file(filename, "wb");
    memset(data, 1, BUFF_SIZE);
    xscope_fwrite(&fp, data, BUFF_SIZE);
    xscope_fclose(&fp);
}


void main_tile0(chanend_t xscope_chan)
{
    test_close_unordered(xscope_chan);
    test_open_close_continously(xscope_chan);
    test_open_a_closed_file(xscope_chan);
}

int main(){
    chanend_t xscope_chan = chanend_alloc();
    xscope_io_init(xscope_chan);
    main_tile0(xscope_chan);
    xscope_close_all_files();
    chanend_free(xscope_chan);
    return 0;
}
