#ifndef MSVC_COMPAT_H
#define MSVC_COMPAT_H

#ifdef _MSC_VER
    #define __builtin_expect(expr, val) (expr)
    #define __attribute__(x)
    #define inline __inline

    // Handles specific int sizes if missing
    typedef __int64 i64;
    typedef unsigned __int64 u64;
#endif

#endif // MSVC_COMPAT_H