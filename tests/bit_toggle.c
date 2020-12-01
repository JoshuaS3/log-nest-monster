#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

uint64_t us(void) {
    uint64_t us;
    struct timeval lnm_current_time;
    gettimeofday(&lnm_current_time, NULL);
    us = (lnm_current_time.tv_sec * 1000000ULL + lnm_current_time.tv_usec);
    return us;
}

uint8_t bit_read(uint8_t bytes[], uint8_t pos) {
    return bytes[pos >> 3] >> (pos & 7) & 1;
}

void bit_toggle(uint8_t bytes[], uint8_t pos) {
    // byte       = pos >> 3 == pos / 8
    // bit        = pos & 7  == pos % 8
    // bit_select = 1 << bit
    bytes[pos >> 3] ^= 1 << (pos & 7);
}

void print(uint8_t bytes[], uint8_t byte_count) {
    for (unsigned short pos = 0; pos < byte_count * 8; pos++) {
        printf("%c", 48 + bit_read(bytes, pos));
    }
    putchar('\n');
}

int main(){
    uint64_t a = us();
    uint8_t byte_count = 8;
    srand(a);
    uint64_t iter = rand() % 10000000;
    uint8_t bytes[byte_count];
    memset(bytes, 0, byte_count);
    for (uint64_t i = 0; i < iter; i++) {
        bit_toggle(bytes, (bytes[0] ^ i) & (byte_count * 8 - 1));
    }
    print(bytes, byte_count);
    uint64_t elapsed = us() - a;
    printf("Time elapsed: %luus (%fus per operation)\n", elapsed, elapsed/(float)iter);
    return 0;
}
