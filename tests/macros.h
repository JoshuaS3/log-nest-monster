#ifndef MACROS_H
#define MACROS_H


#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <stdint.h>

#include <sys/time.h>

#define lnmCritical "CRITICAL"
#define lnmError    "ERROR"
#define lnmWarn     "WARN"
#define lnmInfo     "INFO"
#define lnmDebug    "DEBUG"
#define lnmTrace    "TRACE"

#define lnm_line __LINE__
#define lnm_file __FILE__
#define lnm_func __func__


uint64_t lnm_getus(void) {
    uint64_t us;
    struct timeval lnm_current_time;
    gettimeofday(&lnm_current_time, NULL);
    us = (lnm_current_time.tv_sec * 1000000ULL + lnm_current_time.tv_usec);
    return us;
}


void log_print(FILE* logger, const char* verbosity, const char* format, ...) {
    va_list args;
    va_start(args, format);

    // calculate buffer length
    size_t buffer_size = vsnprintf(NULL, 0, format, args);
    if (buffer_size > UINT16_MAX) {
        printf("too big\n");
    }
    char* buffer = malloc(buffer_size + 1);
    va_end(args);

    // pass to vsnprintf
    va_start(args, format);
    vsnprintf(buffer, buffer_size + 1, format, args);
    va_end(args);

    uint64_t timestamp = lnm_getus();
    fprintf(logger, "[%s] [%lu.%06lu] ", verbosity, timestamp/1000000, timestamp%1000000);

    fputs(buffer, logger);
    fputc('\n', logger);
    free(buffer);
}


#endif  // MACROS_H
