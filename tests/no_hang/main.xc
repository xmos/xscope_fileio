#include <platform.h>
#include <xs1.h>
#include "xscope_io_device.h"


extern "C" {
void main_tile0(void);
}

int main (void)
{
    chan xscope_chan;
    par
    {
        xscope_host_data(xscope_chan);
        on tile[0]: {
            xscope_io_init(xscope_chan);
            main_tile0();
            xscope_close_all_files();
        }
    }
return 0;
}

