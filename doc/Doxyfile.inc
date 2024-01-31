# This file provides overrides to the Doxyfile configuration
PROJECT_NAME = xscope_fileio
PROJECT_BRIEF = "fielio interface for xscope"

# Camera module
INPUT = ../xscope_fileio/api
PREDEFINED             = C_API= EXTERN_C= DWORD_ALIGNED=
USE_MATHJAX            = YES
MATHJAX_FORMAT         = HTML-CSS
MATHJAX_RELPATH        = https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/
GENERATE_XML = YES
