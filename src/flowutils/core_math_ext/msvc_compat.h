#ifndef MSVC_COMPAT_H
#define MSVC_COMPAT_H

#ifdef _MSC_VER
    #include <intrin.h> // Required for MSVC bitwise intrinsics

    #define __builtin_expect(expr, val) (expr)
    #define __attribute__(x)
    #define inline __inline

    // Handles specific int sizes if missing
    typedef __int64 i64;
    typedef unsigned __int64 u64;

    // Direct mapping for Count Trailing Zeros 64-bit
    static __inline int msvc_ctzll(unsigned __int64 value) {
        unsigned long index;
        if (_BitScanForward64(&index, value)) {
            return (int)index;
        }
        return 64; // Default if value is 0, matching standard behavior
    }

    #define __builtin_ctzll(x) msvc_ctzll(x)
#endif

#endif // MSVC_COMPAT_H