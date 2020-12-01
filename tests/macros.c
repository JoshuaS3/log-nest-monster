#include <stdio.h>
#include "macros.h"

int main(void) {
    FILE* logger = fopen("out.txt", "a");
    log_print(stdout, lnmInfo, "Program entry");
    log_print(stdout, lnmInfo, "Parsing input arguments...");
    log_print(stdout, lnmCritical, "Critical error in program execution");
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Traceback: %s::%s (line %d)", lnm_file, lnm_func, lnm_line);
    log_print(stdout, lnmCritical, "Exiting...");
    fclose(logger);
    return 0;
}
