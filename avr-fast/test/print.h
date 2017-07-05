#ifndef PRINT_H
#define PRINT_H

void serial_init(void);

void serial_write(unsigned char c);

void print(const char *s);

void print_bytes(const unsigned char *x, unsigned int xlen);

void printllu(unsigned long long x);

void print_speed(const char *primitive, const unsigned int bytes, const unsigned long long *t, unsigned int tlen);

void print_stack(const char *primitive, const unsigned int bytes, unsigned int stack);

#endif
