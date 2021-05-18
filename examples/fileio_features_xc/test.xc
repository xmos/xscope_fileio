#include <platform.h>
#include <stdio.h>
#include <string.h>
#include <xscope.h>
extern "C"{
#include "xscope_io_device.h"
}
#include <assert.h>

void test(void){
    const char ref_file_name[] = "features_ref.bin";
    const char ref_array[] = "Evolution is change in the heritable characteristics of biological populations over successive generations.";

    xscope_file_t read_xscope_file = xscope_open_file(ref_file_name, "rb");
    char buffer[256] = {0};

    //Load in full ref array from disk
    size_t num_bytes = xscope_fread(&read_xscope_file, buffer, sizeof(ref_array));
    printf("Full sentence (%u): %s\n", num_bytes, buffer);

    //Seek relative to start for read
    xscope_fseek(&read_xscope_file, 10, SEEK_SET);
    printf("Should say 10: %d\n", xscope_ftell(&read_xscope_file));

    memset(buffer, 0, sizeof(buffer));
    xscope_fread(&read_xscope_file, buffer, 2);
    printf("Should say 'is': %s\n", buffer);

    //Seek relative to end for read
    xscope_fseek(&read_xscope_file, -29, SEEK_END);
    printf("Should say 79: %d\n", xscope_ftell(&read_xscope_file));
    memset(buffer, 0, sizeof(buffer));
    xscope_fread(&read_xscope_file, buffer, 4);
    printf("Should say 'over': %s\n", buffer);

    //Seek relative to current for read
    xscope_fseek(&read_xscope_file, 1, SEEK_CUR);
    printf("Should say 84: %d\n", xscope_ftell(&read_xscope_file));
    memset(buffer, 0, sizeof(buffer));
    xscope_fread(&read_xscope_file, buffer, 10);
    printf("Should say 'successive': %s\n", buffer);

    //Load in full ref again
    xscope_fseek(&read_xscope_file, 0, SEEK_SET);
    printf("Should say 0: %d\n", xscope_ftell(&read_xscope_file));
    num_bytes = xscope_fread(&read_xscope_file, buffer, sizeof(ref_array));
    printf("Full sentence (%u): %s\n", num_bytes, buffer);

    //Copy it out to dut for comparing
    const char dut_file_name[] = "features_dut.bin";
    xscope_file_t write_xscope_file = xscope_open_file(dut_file_name, "wb");
    xscope_fwrite(&write_xscope_file, buffer, sizeof(ref_array));

    //Test fseek on write file
    const char dut_mod_file_name[] = "features_dut_mod.bin";
    xscope_file_t write_xscope_fil_mod = xscope_open_file(dut_mod_file_name, "wb");
    xscope_fwrite(&write_xscope_fil_mod, buffer, sizeof(ref_array));
    xscope_fseek(&write_xscope_fil_mod, 10, SEEK_SET);  
    printf("Should say 10: %d\n", xscope_ftell(&write_xscope_fil_mod));
    xscope_fwrite(&write_xscope_fil_mod, "IS", 2);
    printf("Should say 12: %d\n", xscope_ftell(&write_xscope_fil_mod));

    xscope_close_all_files();
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