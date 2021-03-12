#include <platform.h>
#include <stdio.h>
#include <string.h>
#include <xscope.h>
extern "C"{
#include "xscope_io_device.h"
}
#include <assert.h>

void test(void){
    const char ref_file_name[] = "ref.bin";
    const char ref_array[] = "Evolution is change in the heritable characteristics of biological populations over successive generations.";

    xscope_file_t read_xscope_file = xscope_open_file(ref_file_name, "rb");
    char buffer[256] = {0};

    //Load in full ref array from disk
    size_t num_bytes = xscope_fread(buffer, sizeof(ref_array), &read_xscope_file);
    printf("Full sentence (%u): %s\n", num_bytes, buffer);

    //Seek relative to start for read
    xscope_fseek(10, SEEK_SET, &read_xscope_file);
    memset(buffer, 0, sizeof(buffer));
    xscope_fread(buffer, 2, &read_xscope_file);
    printf("Should say 'is': %s\n", buffer);

    //Seek relative to end for read
    xscope_fseek(-29, SEEK_END, &read_xscope_file);
    memset(buffer, 0, sizeof(buffer));
    xscope_fread(buffer, 4, &read_xscope_file);
    printf("Should say 'over': %s\n", buffer);

    //Seek relative to current for read
    xscope_fseek(1, SEEK_CUR, &read_xscope_file);
    memset(buffer, 0, sizeof(buffer));
    xscope_fread(buffer, 10, &read_xscope_file);
    printf("Should say 'successive': %s\n", buffer);

    //Load in full ref again
    xscope_fseek(0, SEEK_SET, &read_xscope_file);
    num_bytes = xscope_fread(buffer, sizeof(ref_array), &read_xscope_file);
    printf("Full sentence (%u): %s\n", num_bytes, buffer);

    //Copy it out to dut for comparing
    const char dut_file_name[] = "dut.bin";
    xscope_file_t write_xscope_file = xscope_open_file(dut_file_name, "wb");
    xscope_fwrite(buffer, sizeof(ref_array), &write_xscope_file);

    //Test fseek on write file
    const char dut_mod_file_name[] = "dut_mod.bin";
    xscope_file_t write_xscope_fil_mod = xscope_open_file(dut_mod_file_name, "wb");
    xscope_fwrite(buffer, sizeof(ref_array), &write_xscope_fil_mod);
    xscope_fseek(10, SEEK_SET, &write_xscope_fil_mod);
    xscope_fwrite("IS ", 3, &write_xscope_fil_mod);

    xscope_close_files();
}

int main(void){
    chan xscope_chan;
    par{
        xscope_host_data(xscope_chan);
        on tile[0]:{
                xscope_io_init(xscope_chan);
                test();
        }
    }
    return 0;
}