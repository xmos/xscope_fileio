// Copyright 2020-2024 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.
#include "xscope_io_device.h"
#include <xcore/chanend.h>
#include <xcore/hwtimer.h>
#include <xcore/select.h>
#include <xcore/assert.h>
#include <xcore/lock.h>

#include <string.h>
#include <xscope.h>
#include <stdio.h>

#define VERBOSE                 0

//Global chanend so we don't need to keep passing it in for read operations
chanend_t c_xscope = 0;
uint8_t available_files[MAX_FILES_OPEN] = {0}; // 0 = available, 1 = in use
lock_t file_access_lock;
volatile unsigned xscope_io_init_flag = 0;

__attribute__((weak))
void xscope_fileio_lock_alloc(void) {
    file_access_lock = lock_alloc();
    xassert(file_access_lock != 0);
}

__attribute__((weak))
void xscope_fileio_lock_acquire(void) {
    lock_acquire(file_access_lock);
}

__attribute__((weak))
void xscope_fileio_lock_release(void) {
    lock_release(file_access_lock);
}


static int get_available_file_idx(){
    for (unsigned idx = 0; idx < MAX_FILES_OPEN; idx++){
        if (available_files[idx] == 0){
            available_files[idx] = 1;
            if(VERBOSE){printf("Allocated file index: %u\n", idx);}
            return idx;
        }
    }
    return -1;
}
static inline void reset_available_file_idx(unsigned idx){
    available_files[idx] = 0;
}

static void xscope_io_check_version(){
    char packet[XSCOPE_IO_VERSION_LEN];
    snprintf(packet, XSCOPE_IO_VERSION_LEN, "%s", XSCOPE_IO_VERSION);
    xscope_bytes(XSCOPE_ID_CHECK_VERSION, XSCOPE_IO_VERSION_LEN, (const unsigned char *)packet);
}

unsigned xscope_fileio_is_initialized(void) {
    return xscope_io_init_flag;
}

void xscope_io_init(chanend_t xscope_end){
    xscope_fileio_lock_alloc();
    xscope_mode_lossless();
    c_xscope = xscope_end;
    xscope_connect_data_from_host(c_xscope);
    xscope_io_check_version();
    xscope_io_init_flag = 1;
}

xscope_file_t xscope_open_file(const char* filename, char* attributes){
    /* Wait until xscope_fileio is initialized */
    while(xscope_fileio_is_initialized() == 0) {
        delay_ticks(1);
    }
    xscope_fileio_lock_acquire();
    xscope_file_t xscope_file;
    strcpy(xscope_file.filename, filename);
    char packet[1 + MAX_FILENAME_LEN + 1];
    unsigned length = 1 + 1 + strlen(xscope_file.filename) + 1;
    xassert(length <= 1 + 1 + MAX_FILENAME_LEN + 1);
    
    if(!strcmp(attributes, "rb")){
        xscope_file.mode = XSCOPE_IO_READ_BINARY;
    }
    else if(!strcmp(attributes, "rt")){
                xscope_file.mode = XSCOPE_IO_READ_TEXT;
    }
    else if(!strcmp(attributes, "wb")){
                xscope_file.mode = XSCOPE_IO_WRITE_BINARY;
    }
    else if(!strcmp(attributes, "wt")){
                xscope_file.mode = XSCOPE_IO_WRITE_TEXT;
    }
    else{
        printf("Unknown file attribytes: %s. Please specify from: rb, rt, wb, wt\n", attributes);
    }
    unsigned file_idx = get_available_file_idx();
    xassert(file_idx != -1 && "Maximum number of files open exceeded");
    packet[0] = '0' + file_idx;
    packet[1] = '0' + xscope_file.mode;
    strcpy(&packet[2], xscope_file.filename);
    xscope_file.index = file_idx;
    xscope_bytes(XSCOPE_ID_OPEN_FILE, length, (const unsigned char *)packet);
    xscope_fileio_lock_release();
    return xscope_file; //Pass a copy of the struct back to the caller
}

size_t xscope_fread(xscope_file_t *xscope_file, uint8_t *buffer, size_t n_bytes_to_read){
    xscope_fileio_lock_acquire();
    xassert(xscope_file->mode == XSCOPE_IO_READ_BINARY || xscope_file->mode == XSCOPE_IO_READ_TEXT);

    unsigned end_marker_found = 0;
    unsigned n_bytes_read = 0;

    uint8_t *buffer_ptr = buffer;
    unsigned chunk_complete = 0;

    unsigned char packet[1 + sizeof(size_t)];
    packet[0] = xscope_file->index + '0';
    memcpy(&packet[1], &n_bytes_to_read, sizeof(n_bytes_to_read));

    xscope_bytes(XSCOPE_ID_READ_BYTES, sizeof(packet), packet);

    do
    {
        int bytes_read = 0;
        SELECT_RES(CASE_THEN(c_xscope, read_host_data))
        {
        read_host_data:
            {
                // Need a buffer big enough to hold max read length.
                // User provided buffer may be smaller than that.
                char local_buffer[MAX_XSCOPE_SIZE_BYTES];
                xscope_data_from_host(c_xscope, local_buffer, &bytes_read);
                end_marker_found = ((bytes_read == END_MARKER_LEN) && !memcmp(local_buffer, END_MARKER_STRING, END_MARKER_LEN)) ? 1 : 0;
                if(end_marker_found){
                    break;
                }
                memcpy(buffer_ptr, local_buffer, bytes_read);
                buffer_ptr += bytes_read;
                n_bytes_read += bytes_read;
                break;
            }
        }
        xassert(n_bytes_read <= n_bytes_to_read);
        if((n_bytes_read == n_bytes_to_read) || end_marker_found){
            chunk_complete = 1;
        }
    } while(!chunk_complete);
    if(VERBOSE) printf("Received: %u bytes\n", n_bytes_read);

    xscope_fileio_lock_release();
    return n_bytes_read;
}

void xscope_fwrite(xscope_file_t *xscope_file, uint8_t *buffer, size_t n_bytes_to_write){
    xscope_fileio_lock_acquire();
    xassert(xscope_file->mode == XSCOPE_IO_WRITE_BINARY || xscope_file->mode == XSCOPE_IO_WRITE_TEXT);

    unsigned char packet[1 + sizeof(unsigned)];
    packet[0] = xscope_file->index + '0';
    memcpy(&packet[1], &n_bytes_to_write, sizeof(n_bytes_to_write));

    xscope_bytes(XSCOPE_ID_WRITE_SETUP, sizeof(packet), packet);

    // Chunk it up as seems more reliable although should be OK with tools 15.0.1
    // Tx is around 10x faster anyhow so a little extra overhead not an issue
    unsigned sent_so_far = 0;
    do{
        if(n_bytes_to_write - sent_so_far >=  MAX_XSCOPE_SIZE_BYTES){
            xscope_bytes(XSCOPE_ID_WRITE_BYTES, MAX_XSCOPE_SIZE_BYTES, (const unsigned char*)&buffer[sent_so_far]);
            sent_so_far += MAX_XSCOPE_SIZE_BYTES;
        }
        else{
            xscope_bytes(XSCOPE_ID_WRITE_BYTES, n_bytes_to_write - sent_so_far, (const unsigned char*)&buffer[sent_so_far]);
            sent_so_far = n_bytes_to_write;
        }
        // delay_ticks(10000); /// Magic number found to make xscope stable on MAC, else you get WRITE ERROR ON UPLOAD ....
        // Not needed with tools 15.0.1
    }
    while (sent_so_far < n_bytes_to_write);

    if(VERBOSE) printf("Sent %u bytes\n", n_bytes_to_write);
    xscope_fileio_lock_release();
}

void xscope_fseek(xscope_file_t *xscope_file, int offset, int whence){
    xscope_fileio_lock_acquire();
    xassert(whence == SEEK_SET || whence == SEEK_CUR || whence == SEEK_END);
    unsigned char packet[1 + 1 + sizeof(offset)];
    packet[0] = xscope_file->index + '0';
    packet[1] = whence + '0';
    memcpy(&packet[2], &offset, sizeof(offset));
    xscope_bytes(XSCOPE_ID_SEEK, sizeof(packet), packet);
    if(VERBOSE) printf("Seeking file id: %u whence %d offset %d\n", xscope_file->index, whence, offset);
    xscope_fileio_lock_release();
}

int xscope_ftell(xscope_file_t *xscope_file){
    xscope_fileio_lock_acquire();
    const unsigned char idx = xscope_file->index + '0';
    xscope_bytes(XSCOPE_ID_TELL, 1, &idx);
    int offset, bytes_read = 0;
    xscope_data_from_host(c_xscope, (char *)&offset, &bytes_read);
    xassert(bytes_read = sizeof(offset));
    if(VERBOSE) printf("Tell file id: %u offset %d\n", xscope_file->index, offset);
    xscope_fileio_lock_release();
    return offset;
}

void xscope_close_all_files(void){
    xscope_bytes(XSCOPE_ID_HOST_QUIT, 1, (unsigned char*)"!");
    if(VERBOSE) printf("Sent close files\n");
    hwtimer_t t = hwtimer_alloc(); hwtimer_delay(t, 5000000); //50ms to allow messages to make it before xgdb quit
}

void xscope_fclose(xscope_file_t *xscope_file){
    xscope_fileio_lock_acquire();
    const unsigned char idx = xscope_file->index + '0';
    xscope_bytes(XSCOPE_ID_HOST_CLOSE, 1, &idx);
    if(VERBOSE) {
        printf("Sent close file id: %d\n", xscope_file->index);
    }
    reset_available_file_idx(xscope_file->index);
    delay_ticks(10); // sanity time to close file
    xscope_fileio_lock_release();
}
