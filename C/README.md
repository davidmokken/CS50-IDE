# Questions

## What's `stdint.h`?

Stdint.h is a header that refers to BMP-related data types based on Microsoft's own.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

Variable types are identifed in these integers. Unsigned integers can only be postive values. Signed integers can also have negative values.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE = uint8_t, DWORD = uint32_t DWORD; LONG = int32_t  WORD = uint16_t

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

42

## What's the difference between `bfSize` and `biSize`?

bfSize is the size in bytes of the bitmap file. biSize is the number of bytes required by the structure.

## What does it mean if `biHeight` is negative?

If biHeight is negative, the bitmap is a top-down DIB and its origin is the upper-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBITCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If the file cannot be opened. (If the file does not exist on the computer for example).

## Why is the third argument to `fread` always `1` in our code?

Because for every fread, a single element in being read in our code. Such as BITMAPINFOHEADER

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

1

## What does `fseek` do?

fseek moves the cursor that track of where in the file we are.

## What is `SEEK_CUR`?

It is the current position in the file.
