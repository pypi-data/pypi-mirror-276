/*
 * Generated by util/mkerr.pl DO NOT EDIT
 * Copyright 1995-2021 The OpenSSL Project Authors. All Rights Reserved.
 *
 * Licensed under the Apache License 2.0 (the "License").  You may not use
 * this file except in compliance with the License.  You can obtain a copy
 * in the file LICENSE in the source distribution or at
 * https://www.openssl.org/source/license.html
 */

#ifndef OPENSSL_CONFERR_H
# define OPENSSL_CONFERR_H
# pragma once

# include <openssl/opensslconf.h>
# include <openssl/symhacks.h>
# include <openssl/cryptoerr_legacy.h>



/*
 * CONF reason codes.
 */
# define CONF_R_ERROR_LOADING_DSO                         110
# define CONF_R_INVALID_PRAGMA                            122
# define CONF_R_LIST_CANNOT_BE_NULL                       115
# define CONF_R_MANDATORY_BRACES_IN_VARIABLE_EXPANSION    123
# define CONF_R_MISSING_CLOSE_SQUARE_BRACKET              100
# define CONF_R_MISSING_EQUAL_SIGN                        101
# define CONF_R_MISSING_INIT_FUNCTION                     112
# define CONF_R_MODULE_INITIALIZATION_ERROR               109
# define CONF_R_NO_CLOSE_BRACE                            102
# define CONF_R_NO_CONF                                   105
# define CONF_R_NO_CONF_OR_ENVIRONMENT_VARIABLE           106
# define CONF_R_NO_SECTION                                107
# define CONF_R_NO_SUCH_FILE                              114
# define CONF_R_NO_VALUE                                  108
# define CONF_R_NUMBER_TOO_LARGE                          121
# define CONF_R_OPENSSL_CONF_REFERENCES_MISSING_SECTION   124
# define CONF_R_RECURSIVE_DIRECTORY_INCLUDE               111
# define CONF_R_RECURSIVE_SECTION_REFERENCE               126
# define CONF_R_RELATIVE_PATH                             125
# define CONF_R_SSL_COMMAND_SECTION_EMPTY                 117
# define CONF_R_SSL_COMMAND_SECTION_NOT_FOUND             118
# define CONF_R_SSL_SECTION_EMPTY                         119
# define CONF_R_SSL_SECTION_NOT_FOUND                     120
# define CONF_R_UNABLE_TO_CREATE_NEW_SECTION              103
# define CONF_R_UNKNOWN_MODULE_NAME                       113
# define CONF_R_VARIABLE_EXPANSION_TOO_LONG               116
# define CONF_R_VARIABLE_HAS_NO_VALUE                     104

#endif
