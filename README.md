This tool allows you to extract compressed palette in Megaman VI - NES and reinserting.

## Usage

Synopsis:
```
megaman6_palette.py <extract|insert> -r <romFile> -f <OutFile/Infile> -o <offset> -s <size>
```

Description:

```
extract     Extract from ROM
insert      Insert to ROM
help        Show this message.

Extract:
-r <path>     Path to the ROM file
-f <path>     Output file
-o <hex>      Start offset
-s <hex>      Block size

Insert:
-r <path>     Path to the ROM file
-f <path>     Input file
-o <hex>      Start offset
-s <hex>      Block size
--fill <hex>  Fill free space (default=FF)
```

## Compression

A embedded compression using a byte flags.

```
bit 7  bit 6  bits 5–0
-----  -----  --------
flag   flag   color NES (0–63)
```

Example:

```
7C = %01111100
     ^^
     ||-- color = $3C
     |
     +--- flag $40 -> insert $0F
```

## Frecuency Answer Questions

### Can I use this tool in my personal project?

Of course, there's no need to ask. Feel free to use it in your project. I only ask that you mention me as contributor.
