// Copyright 2021-2024 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.
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

