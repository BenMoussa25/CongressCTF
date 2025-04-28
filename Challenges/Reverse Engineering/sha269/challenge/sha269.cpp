#include <iostream>
#include <iomanip>
#include <string>
#include <array>
#include <algorithm>
#include <cstdint>

constexpr size_t HASH_SIZE = 32;

void shuffle(std::array<char, HASH_SIZE> &hash)
{
    for (size_t i = 0; i < HASH_SIZE - 1; i += 2)
    {
        std::swap(hash[i], hash[i + 1]);
    }
}

std::string sha269(std::string_view input)
{
    std::array<char, HASH_SIZE> padded_input{};
    std::array<char, HASH_SIZE> hash{};
    std::array<uint32_t, 5> states{
        0xDEADBEEF,
        0xB16B00B5,
        0xCAFEBABE,
        0xF00DDEAD,
        0xFACEB00C};

    for (size_t i = 0; i < HASH_SIZE; ++i)
    {
        padded_input[i] = (i < input.size()) ? input[i] : 'X';
    }

    for (size_t i = 0; i < HASH_SIZE; ++i)
    {
        hash[i] = padded_input[i] ^ static_cast<char>(states[i % 5] & 0xFF);
        states[i % 5] = (states[i % 5] >> 8) | (states[i % 5] << 24);
    }

    shuffle(hash);
    return std::string(hash.begin(), hash.end());
}

void echo(const std::string &hash)
{
    for (char c : hash)
    {
        std::cout << std::hex << std::setw(2) << std::setfill('0')
                  << static_cast<int>(static_cast<unsigned char>(c));
    }
    std::cout << '\n';
}

constexpr std::string_view author = "--  Author: jio  --";

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        std::cerr << "Usage: " << argv[0] << " \"input\"\n";
        return 1;
    }

    std::string input = argv[1];
    std::string hash = sha269(input);
    echo(hash);

    return 0;
}
