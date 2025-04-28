#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>
#define HASH_SIZE 64
void avalanche(uint32_t *state)
{
    *state ^= (*state >> 16);
    *state *= 0x85ebca6b;
    *state ^= (*state >> 13);
    *state *= 0xc2b2ae35;
    *state ^= (*state >> 16);
}
void mix_bits(uint8_t *hash)
{
    for (int i = 0; i < HASH_SIZE - 4; i += 4)
    {
        uint32_t chunk =
            ((uint32_t)hash[i] << 24) |
            ((uint32_t)hash[i + 1] << 16) |
            ((uint32_t)hash[i + 2] << 8) |
            ((uint32_t)hash[i + 3]);
        avalanche(&chunk);
        hash[i] = (chunk >> 24) & 0xFF;
        hash[i + 1] = (chunk >> 16) & 0xFF;
        hash[i + 2] = (chunk >> 8) & 0xFF;
        hash[i + 3] = chunk & 0xFF;
    }
}
uint8_t *hash(const char *input)
{
    static uint8_t hash_result[HASH_SIZE];
    uint32_t states[8] = {
        0xDEADBEEF, 0xB16B00B5, 0xCAFEBABE, 0xF00DDEAD,
        0xFACEB00C, 0x8BADF00D, 0xDEADC0DE, 0xFEEDFACE};
    memset(hash_result, 0, HASH_SIZE);
    size_t input_len = strlen(input);
    for (size_t pos = 0; pos < input_len; pos += 16)
    {
        size_t chunk_size = (input_len - pos < 16) ? (input_len - pos) : 16;
        for (size_t i = 0; i < chunk_size; i++)
        {
            uint8_t byte = input[pos + i];
            for (int j = 0; j < 8; j++)
            {
                states[j] ^= ((uint32_t)byte << ((j * 8) % 32));
                avalanche(&states[j]);
            }
        }
    }
    uint64_t length_bits = input_len * 8;
    states[0] ^= (length_bits & 0xFFFFFFFF);
    states[1] ^= (length_bits >> 32);
    for (int i = 0; i < 8; i++)
    {
        avalanche(&states[i]);
    }
    for (int i = 0; i < HASH_SIZE; i++)
    {
        hash_result[i] = (states[i % 8] >> ((i % 4) * 8)) & 0xFF;
    }
    mix_bits(hash_result);
    mix_bits(hash_result);
    return hash_result;
}
void print_hash(const uint8_t *hash)
{
    for (int i = 0; i < HASH_SIZE; i++)
    {
        printf("%02x", hash[i]);
    }
    printf("\n");
}
char *author = "--  Author: jio  --";
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s \"input\"\n", argv[0]);
        return 1;
    }
    print_hash(hash(argv[1]));
    return 0;
}