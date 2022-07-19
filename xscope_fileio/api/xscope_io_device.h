// Copyright (c) 2020, XMOS Ltd, All rights reserved
#ifndef XSCOPE_IO_DEVICE_H_
#define XSCOPE_IO_DEVICE_H_

#ifdef __XC__
#define chanend_t chanend
#else
#include <xcore/chanend.h>
#endif

#include <stddef.h>
#include <stdint.h>
#include "xscope_io_common.h"

typedef struct{
    char filename[MAX_FILENAME_LEN + 1];
    xscope_file_mode_t mode;
    unsigned index;
} xscope_file_t;

#ifdef __XC__
extern "C"{
#endif

/******************************************************************************
 * xscope_io_init
 *
 * This opens the input and output files on the host and also initialises the
 * channel end for use later when reading data from host to device.
 * This must be called before attempting to read or write.
 *
 * @param   xscope_end is the app side channel end connected xscope_host_data()
 *          task in the top level application.
 * @return  void
 ******************************************************************************/
void xscope_io_init(chanend_t xscope_end);

/******************************************************************************
 * xscope_fileio_is_initialized
 *
 * This returns the status of the host xscope fileio connection
 *
 * @return  1 if initialized, else 0
 ******************************************************************************/
unsigned xscope_fileio_is_initialized(void);

/******************************************************************************
 * xscope_open_files
 *
 * This opens the input and output files on the host and also initialises the
 * channel end for use later when reading data from host to device.
 * This must be called before attempting to read or write.
 *
 * @param   read_file_name to open on host
 * @param   write_file_name to open on host
 * @return  an initialised xscope_file_handle
 ******************************************************************************/
xscope_file_t xscope_open_file(const char* filename, char* attributes);

/******************************************************************************
 * xscope_fread   NOTE MAXIMUM n_bytes_to_read of 64kB on Linux, bugzillaid=18528
 *
 * Reads a number of bytes into the buffer provided by the application.
 * It sends a command to the host app which responds with an upload of the
 * requested data from the file. Each read is contiguous from the previous read
 *
 * @param   handle of file to operate on
 * @param   buffer that will be written the file read
 * @param   n_bytes_to_read
 * @return  number of bytes actually read. Will be zero if EOF already hit.
 ******************************************************************************/
size_t xscope_fread(xscope_file_t *xscope_io_handle, uint8_t *buffer, size_t n_bytes_to_read);

/******************************************************************************
 * xscope_fwrite
 *
 * Writes a number of bytes from the buffer provided by the application.
 *
 * @param   handle of file to operate on
 * @param   buffer that will be read and sent to be written on the host
 * @param   n_bytes_to_write
 * @return  void
 ******************************************************************************/
void xscope_fwrite(xscope_file_t *xscope_io_handle, uint8_t *buffer, size_t n_bytes_to_write);

/******************************************************************************
 * xscope_seek SEEK_SET, SEEK_CUR or SEEK_END. Note no error checking yet!!
 *
 * Sets the file position of the stream to the given offset
 *
 * @param   handle of file to operate on
 * @param   offset in bytes
 * @param   whence - SEEK_SET, SEEK_CUR or SEEK_END
 * @return  void
 ******************************************************************************/
void xscope_fseek(xscope_file_t *xscope_io_handle, int offset, int whence);

/******************************************************************************
 * xscope_ftell
 *
 * Obtain the file position of the stream
 *
 * @param   handle of file to operate on
 * @return  void
 ******************************************************************************/
int xscope_ftell(xscope_file_t *xscope_file);


/******************************************************************************
 * xscope_close_all_files
 *
 * Closes all files on the host.
 * This must be called at the end of device application as it also signals
 * terminate to the host app.
 *
 * @return  void
 ******************************************************************************/
void xscope_close_all_files(void);

#ifdef __XC__
}
#endif

#endif
