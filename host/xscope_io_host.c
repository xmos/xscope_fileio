// Copyright (c) 2020-2022, XMOS Ltd, All rights reserved

// Suppress some unwanted warnings in the Windows build
#ifdef _WIN32
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <assert.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include "windows.h"
#else
#include <pthread.h>
#include <unistd.h>
#endif

#include "xscope_endpoint.h"
#include "xscope_io_common.h"

#define VERBOSE                 0

typedef struct{
    char file_name[MAX_FILENAME_LEN + 1];
    FILE *fp;
    xscope_file_mode_t mode;
} xscope_host_file_t;

xscope_host_file_t host_files[MAX_FILES_OPEN] = {0};

const char end_sting[] = END_MARKER_STRING;
static unsigned running = 1;

int device_print_newline = 1; //Used to keep track of newlines for [DEVICE] print prefix

void xscope_print(
  unsigned long long timestamp,
  unsigned int length,
  unsigned char *data)
{
  if (length) {
    if (device_print_newline){
      printf("[DEVICE] ");
      device_print_newline = 0;
    }
    for (unsigned i = 0; i < length; i++){
      char character = *(&data[i]); 
      printf("%c", character);
      if (character == '\n'){
        device_print_newline = 1;
      }
    }
  }
}



void xscope_register(
  unsigned int id,
  unsigned int type,
  unsigned int r,
  unsigned int g,
  unsigned int b,
  unsigned char *name,
  unsigned char *unit,
  unsigned int data_type,
  unsigned char *data_name)
{
  if(VERBOSE) printf("[HOST] xSCOPE register event (id [%d] name [%s])\n", id, name);
}

int send_file_chunk(unsigned file_idx, unsigned req_size)
{
    unsigned char *buf = malloc(req_size);
    unsigned n_bytes_read = 0;

    n_bytes_read = fread(buf, 1, req_size, host_files[file_idx].fp);

    if(n_bytes_read < req_size){
        if(VERBOSE) printf("[HOST] Unexpected end of file, device requested: %u available: %u sent: 0\n", req_size, n_bytes_read);
        xscope_ep_request_upload(END_MARKER_LEN, (const unsigned char *)end_sting); //End
        free(buf);
        return(-1);
    }

    for(unsigned idx = 0; idx < n_bytes_read / MAX_XSCOPE_SIZE_BYTES; idx++){
        xscope_ep_request_upload(MAX_XSCOPE_SIZE_BYTES, &buf[idx * MAX_XSCOPE_SIZE_BYTES]);
    }
    unsigned left_over = n_bytes_read % MAX_XSCOPE_SIZE_BYTES;
    if(left_over){
        xscope_ep_request_upload(left_over, &buf[(n_bytes_read / MAX_XSCOPE_SIZE_BYTES) * MAX_XSCOPE_SIZE_BYTES]);
    }

    if(VERBOSE) printf("[HOST] sent block %u\n", n_bytes_read);

    if(feof(host_files[file_idx].fp)){
        if(VERBOSE) printf("[HOST] End of file\n");
        xscope_ep_request_upload(END_MARKER_LEN, (const unsigned char *)end_sting); //End
    }

    free(buf);
    return(0);
}

void xscope_record(
  unsigned int id,
  unsigned long long timestamp,
  unsigned int length,
  unsigned long long dataval,
  unsigned char *databytes)
{
    static signed write_file_idx = 0;
    static unsigned write_size = 0;

    switch(id){
        case XSCOPE_ID_OPEN_FILE:
        {
            unsigned file_idx = databytes[0] - '0';
            assert(file_idx < MAX_FILES_OPEN);
            strcpy(host_files[file_idx].file_name, (const char *)&databytes[2]);
            host_files[file_idx].mode = databytes[1] - '0';
            if(VERBOSE) printf("[HOST] Open file: %d, %lu, %s, idx: %u mode: %u\n", length, strlen((char*)databytes),
                                host_files[file_idx].file_name, file_idx, host_files[file_idx].mode);
            switch(host_files[file_idx].mode){
                case XSCOPE_IO_READ_BINARY:
                    host_files[file_idx].fp = fopen(host_files[file_idx].file_name, "rb");
                break;

                case XSCOPE_IO_READ_TEXT:
                    host_files[file_idx].fp = fopen(host_files[file_idx].file_name, "rt");
                break;

                case XSCOPE_IO_WRITE_BINARY:
                    host_files[file_idx].fp = fopen(host_files[file_idx].file_name, "wb");
                break;

                case XSCOPE_IO_WRITE_TEXT:
                    host_files[file_idx].fp = fopen(host_files[file_idx].file_name, "wt");
                break;

                default:
                    assert(0);
                break;
            }

            if(!host_files[file_idx].fp){
                printf("Failed to open %s\n", host_files[file_idx].file_name);
                exit(-1);
            }
            return;
        }
        break;

        case XSCOPE_ID_READ_BYTES:
        {
            unsigned file_idx = databytes[0] - '0';
            unsigned transfer_size;
            memcpy(&transfer_size, &databytes[1], sizeof(transfer_size));
            if(VERBOSE) printf("[HOST] read bytes idx: %u transfer length: %u\n", file_idx, transfer_size);
            send_file_chunk(file_idx, transfer_size);
        }
        break;

        case XSCOPE_ID_WRITE_SETUP:
        {
            unsigned file_idx = databytes[0] - '0';
            if(write_size != 0){
                printf("[HOST] Error - write_size not initialised to 0. Last write incomplete?\n");
                assert(0);
            }
            write_file_idx = file_idx;
            memcpy(&write_size, &databytes[1], sizeof(write_size));
            if(VERBOSE) printf("[HOST] write transfer setup idx: %u, bytes: %u\n", file_idx, write_size);
        }
        break;

        case XSCOPE_ID_WRITE_BYTES:
        {
            if(VERBOSE) printf("[HOST] write idx: %u bytes transfer length: %u\n", write_file_idx, length);
            if(length > write_size){
                printf("[HOST] Error - write will overrun by %d bytes.", length - write_size);
                assert(0);
            }
            fwrite(databytes, 1, length, host_files[write_file_idx].fp);
            write_size -= length;
            if(write_size == 0){
                if(VERBOSE) printf("[HOST] Normal end of write transfer\n");
            }
            else{
                //Still going
            }
        }
        break;

        case XSCOPE_ID_SEEK:
        {
            assert(length == 6);
            unsigned file_idx = databytes[0] - '0';
            int whence = databytes[1] - '0';
            int offset;
            memcpy(&offset, &databytes[2], sizeof(offset));

            if(VERBOSE) printf("[HOST] seek file idx: %u whence: %d offset: %d\n", file_idx, whence, offset);

            int ret = fseek(host_files[file_idx].fp, offset, whence);
            if(ret == 0){
                if(VERBOSE) printf("[HOST] Normal seek. New position: %ld\n", ftell(host_files[file_idx].fp));
            }
            else {
                printf("[HOST] Error - fseek on file %s returned: %d\n", host_files[file_idx].file_name, ret);
                assert(0);
            }
        }
        break;

        case XSCOPE_ID_TELL:
        {
            assert(length == 1);
            unsigned file_idx = databytes[0] - '0';
            int offset = ftell(host_files[file_idx].fp);
            if(VERBOSE) printf("[HOST] tell file idx: %d offset: %d\n", file_idx, offset);
            xscope_ep_request_upload(sizeof(offset), (const unsigned char *)&offset); 
        }
        break;

        case XSCOPE_ID_HOST_QUIT:
        {
            if(VERBOSE) printf("[HOST] quit received\n");
            running = 0;
            return;
        }
        break;

        default:
        {
            printf("[HOST] unexpected xSCOPE record event (id [%u] length [%u]\n", id, length);
        }
        break;
    }
}


int main(int argc, char *argv[])
{
    if(argc != 2){
        printf("ERROR missing xscope port number: Usage example %s 12340\n", argv[0]);
        exit(-1);
    }

    xscope_ep_set_print_cb(xscope_print);
    xscope_ep_set_register_cb(xscope_register);
    xscope_ep_set_record_cb(xscope_record);
    int error = xscope_ep_connect("localhost", argv[1]);
    if(error){
        running = 0;
    }

    while(running){
        //Back off for 10ms to reduce processor usage during poll
#if _WIN32
        Sleep(10);
#else
        usleep(10000);
#endif
    }

    if(VERBOSE) printf("[HOST] Exit received\n");
    //Wait another 100ms to allow any remaining outs from the device to arrive before we terminate
#if _WIN32
    Sleep(100);
#else
    usleep(100000);
#endif
    for(unsigned idx = 0; idx < MAX_FILES_OPEN; idx++){
        if(host_files[idx].fp != NULL){
            fclose(host_files[idx].fp);
        }
    }

    return(0);
}

