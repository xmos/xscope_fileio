#include <platform.h>
#include <xs1.h>
#include <xscope.h>

extern "C" {
void main_tile0(chanend);
}

int main (void)
{
  chan xscope_chan;
  par
  {
    xscope_host_data(xscope_chan);
    on tile[0]: main_tile0(xscope_chan);
  }
  return 0;
}

