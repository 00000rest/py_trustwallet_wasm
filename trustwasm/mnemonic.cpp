#include <random>
#include <vector>
#include <cstdint>
#include <algorithm>

std::vector<int32_t> mnemnonic_rng(int64_t seed)
{
    uint8_t buf[32] = {0};
    size_t len = 32;
    std::mt19937 rng(seed);
    std::generate_n(buf, len, [&rng]() -> uint8_t
                    { return rng() & 0x000000ff; });

    std::vector<int32_t> bufv(32);

    for (size_t i = 0; i < len; ++i)
    {
        bufv[i] = static_cast<unsigned int>(buf[i]);
    }

    return bufv;
}
