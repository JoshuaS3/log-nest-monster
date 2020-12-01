#include <stdint.h>
#include <stdio.h>

uint64_t rdtsc(){
    uint32_t lo,hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t)hi << 32) | lo;
}

int main() {
    for (int i = 0; i < 100; i++) {
        uint64_t a = rdtsc();
        printf("%lu ticks\n", rdtsc() - a);
    }
    return 0;
}
