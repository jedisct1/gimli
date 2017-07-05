#include <stdint.h>

#define gimli avr_gimli
extern void Gimli_hash(const uint8_t *input, uint64_t inputByteLen, uint8_t *output, uint64_t outputByteLen);