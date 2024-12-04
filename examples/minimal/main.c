#include <platform.h>
#include <xcore/chanend.h>

#include <xscope_io_device.h>

int main(){
    chanend_t xscope_chan = chanend_alloc();
    xscope_io_init(xscope_chan);
    xscope_io_check_version();
    xscope_close_all_files();
    chanend_free(xscope_chan);
    return 0;
}
