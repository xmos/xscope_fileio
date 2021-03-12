#include <platform.h>
#include <stdio.h>
#include <string.h>
#include <xscope.h>
#include <xcore/assert.h>
#include <xcore/hwtimer.h>
#include "xscope_io_device.h"

#include <assert.h>

#define IN_FILE_NAME    "ref.bin"
#define OUT_FILE_NAME   "dut.bin"

float ticks_to_KBPS(unsigned ticks, unsigned num_bytes){
    const float ticks_per_second = 100000000;
    float kb = (float)num_bytes / 1000;
    float time_s = (float) ticks / ticks_per_second;

    return kb/time_s;
}

void do_test(void){
    xscope_file_t read_xscope_file = xscope_open_file(IN_FILE_NAME, "rb");
    xscope_file_t write_xscope_file = xscope_open_file(OUT_FILE_NAME, "wb");

    uint8_t buffer[256*1024] = {0};

    xscope_fseek(0, SEEK_END, &read_xscope_file);
    unsigned fsize = xscope_ftell(&read_xscope_file);
    xscope_fseek(0, SEEK_SET, &read_xscope_file);
    printf("Input file size kB: %d\n", fsize / 1000);

    unsigned read_total_time = 0;
    unsigned write_total_time = 0;


    //Load in full ref array from disk
    size_t num_bytes = 0;
    do{
        unsigned t0 = get_reference_time();
        num_bytes = xscope_fread(buffer, sizeof(buffer), &read_xscope_file);
        unsigned t1 = get_reference_time();
        read_total_time += t1 - t0;

        unsigned t2 = get_reference_time();
        xscope_fwrite(buffer, num_bytes, &write_xscope_file);
        unsigned t3 = get_reference_time();
        write_total_time += t3 - t2;
    } while(num_bytes > 0);
       




    printf("Throughput KBPS Read: %f, Write: %f\n", ticks_to_KBPS(read_total_time, fsize), ticks_to_KBPS(write_total_time, fsize));
}

void main_tile0(chanend_t xscope_chan)
{
    xscope_io_init(xscope_chan);
    do_test();
    xscope_close_files();
}
