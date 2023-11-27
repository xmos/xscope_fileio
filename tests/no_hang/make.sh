xcc -target=XCORE-AI-EXPLORER \
    main.c main.xc config.xscope \
    ../../xscope_fileio/src/* \
    -I ../../xscope_fileio/api \
    -I ../../xscope_fileio \
    -fxscope \
    -o no_hang.xe