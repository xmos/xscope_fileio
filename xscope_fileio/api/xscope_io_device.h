// Copyright 2020-2024 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.
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

/**
 * @defgroup xscope_fileio_device     Doxygen group for XScope file I/O device API
 */


/**
 * @brief Structure representing an XScope file
 * @ingroup xscope_fileio_device
 */
typedef struct {
    char filename[MAX_FILENAME_LEN + 1]; /**< Name of the file */
    xscope_file_mode_t mode; /**< Mode of the file (read or write) */
    unsigned index; /**< Index of the file */
} xscope_file_t;

#ifdef __XC__
extern "C" {
#endif


/**
 * @brief initialises XScope I/O
 *
 * This function opens the input and output files on the host and also initialises
 * the channel end for use later when reading data from host to device. This must
 * be called before attempting to read or write.
 *
 * @param xscope_end The app side channel end connected to xscope_host_data() task
 *                  in the top-level application.
 * @return void
 * @ingroup xscope_fileio_device
 */
void xscope_io_init(chanend_t xscope_end);

/**
 * @brief Checks if the XScope file I/O is initialized
 *
 * @return 1 if initialized, else 0
 */
unsigned xscope_fileio_is_initialized(void);

/**
 * @brief Opens an XScope file
 *
 * This opens the input and output files on the host and also initialises the
 * channel end for use later when reading data from host to device.
 * This must be called before attempting to read or write.
 *
 * @param filename The name of the file to open on the host
 * @param attributes The attributes of the file
 * @return An initialized xscope_file_t structure
 * @ingroup xscope_fileio_device
 */
xscope_file_t xscope_open_file(const char *filename, char *attributes);

/**
 * @brief Reads data from an XScope file
 *
 * Reads a number of bytes into the buffer provided by the application.
 * It sends a command to the host app which responds with an upload of the
 * requested data from the file. Each read is contiguous from the previous read.
 *
 * @param xscope_io_handle Handle of the file to operate on
 * @param buffer Buffer that will be written with the file read
 * @param n_bytes_to_read Number of bytes to read
 * @return Number of bytes actually read. Will be zero if EOF already hit.
 * @ingroup xscope_fileio_device
 */
size_t xscope_fread(xscope_file_t *xscope_io_handle, uint8_t *buffer, size_t n_bytes_to_read);

/**
 * @brief Writes data to an XScope file
 *
 * Writes a number of bytes from the buffer provided by the application.
 *
 * @param xscope_io_handle Handle of the file to operate on
 * @param buffer Buffer that will be read and sent to be written on the host
 * @param n_bytes_to_write Number of bytes to write
 * @return void
 * @ingroup xscope_fileio_device
 */
void xscope_fwrite(xscope_file_t *xscope_io_handle, uint8_t *buffer, size_t n_bytes_to_write);

/**
 * @brief Sets the file position of an XScope file
 *
 * Sets the file position of the stream to the given offset.
 *
 * @param xscope_io_handle Handle of the file to operate on
 * @param offset Offset in bytes
 * @param whence SEEK_SET, SEEK_CUR, or SEEK_END
 * @return void
 * @ingroup xscope_fileio_device
 */
void xscope_fseek(xscope_file_t *xscope_io_handle, int offset, int whence);

/**
 * @brief Obtains the file position of an XScope file
 *
 * @param xscope_file Handle of the file to operate on
 * @return Current file position
 * @ingroup xscope_fileio_device
 */
int xscope_ftell(xscope_file_t *xscope_file);

/**
 * @brief Closes all XScope files on the host
 *
 * This must be called at the end of the device application as it also signals
 * termination to the host app.
 *
 * @return void
 * @ingroup xscope_fileio_device
 */
void xscope_close_all_files(void);

/**
 * @brief Closes a single XScope file on the host
 *
 * It can be called at any time to close a file.
 * Note: xscope_close_all_files() must still be called
 * at the end of the device application.
 *
 * @param xscope_file Handle of the file to operate on
 * @return void
 * @ingroup xscope_fileio_device
 */
void xscope_fclose(xscope_file_t *xscope_file);

#ifdef __XC__
}
#endif

#endif
