## Megaman VI Palette Decompressor by koda v0.1
## 05-02-2026
import argparse
import sys
import os

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"\nError: {message}\n")
        self.show_help()
        sys.exit(1)

    def print_help(self):
        self.show_help()

    @staticmethod
    def show_help():
        print("+----------------------------------------------")
        print("| Megaman VI Palette Decompressor by koda v0.1")
        print("+----------------------------------------------")
        print("| Usage:")
        print("|   extract      Extract from ROM")
        print("|   insert       Insert to ROM")
        print("|   help         Show this message.")
        print("+----------------------------------------------")
        print("| Extract:")
        print("|  -r <path>     Path to the ROM file")
        print("|  -f <path>     Output file")
        print("|  -o <hex>      Start offset")
        print("|  -s <hex>      Block size")
        print("|")
        print("| Insert:")
        print("|  -r <path>     Path to the ROM file")
        print("|  -f <path>     Input file")
        print("|  -o <hex>      Start offset")
        print("|  -s <hex>      Block size")
        print("|  --fill <hex>  Fill free space (default=FF)")
        print("+---------------------------------------------")
        sys.exit(1)

def decode_palette_stream(data: bytes, flag_59: bool = True) -> bytes:
    if not data:
        return b""
    x = data[0]
    pal = bytearray([0x00] * 32)

    for v in data[1:]:
        if flag_59 and (v & 0x40):
            pal[x] = 0x0F
            x += 1
            if x >= 32:
                break

        pal[x] = v & 0x3F
        x += 1

        if x >= 32:
            break
    return bytes(pal)

def compress_palette_stream(pal):
    out = bytearray()
    out.append(0x00)

    i = 0
    while i < len(pal):
        v = pal[i] & 0x3F

        if v == 0x0F and i + 1 < len(pal):
            nxt = pal[i + 1] & 0x3F
            out.append(0x40 | nxt)
            i += 2
        else:
            out.append(v)
            i += 1

    return bytes(out)

def read_rom(rom_file, addr, size):
    with open(rom_file, 'rb') as f:
        f.seek(addr)
        data = f.read(size)
        return data

def export_data(out_file, rom_file, data):
    with open(out_file, 'wb') as f:
        f.write(data)
        print(f"Extracted {len(data)} bytes from '{rom_file}' to '{out_file}'.\n")

def import_data(file):
    with open(file, "rb") as f:
        data = f.read()
    return data

def write_rom(rom_file, data, addr, bank_size, fill, fill_value, file_name):
    if len(data) > bank_size:
        excess = len(data) - bank_size
        print(f"Error: file '{file_name}', {excess} bytes exceed input size.")
        sys.exit(1)
    else:
        free_space = bank_size - len(data)
        filled_data = data
        if fill:
            filled_data = data + bytes([fill_value]) * free_space

        with open(rom_file, "r+b") as f:
            f.seek(addr)
            f.write(filled_data)
            print(f"Inserted '{file_name}' to '{rom_file}'.")
            if fill:
                print(f"Free space: {free_space} bytes filled with 0x{fill_value:02X}.\n")
            else:
                print(f"Free space: {free_space} bytes.\n")


def main():
    parser = CustomArgumentParser(add_help=False)
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Extract command
    extract_parser = subparsers.add_parser('extract')
    extract_parser.add_argument('-r', '--rom', required=True)
    extract_parser.add_argument('-f', '--out-file', required=True)
    extract_parser.add_argument('-o', '--start-offset', required=True, type=lambda x: int(x, 16))
    extract_parser.add_argument('-s', '--size', required=True, type=lambda x: int(x, 16))

    # Insert command
    insert_parser = subparsers.add_parser('insert')
    insert_parser.add_argument('-r', '--rom', required=True)
    insert_parser.add_argument('-f', '--in-file', required=True)
    insert_parser.add_argument('-o', '--start-offset', required=True, type=lambda x: int(x, 16))
    insert_parser.add_argument('-s', '--size', type=lambda x: int(x, 16))
    insert_parser.add_argument('--fill', nargs='?', default=None, const='FF', type=lambda x: int(x, 16) if x else 0xFF)
    
    args = parser.parse_args()
    
    if args.command == 'extract':
        if not os.path.exists(args.rom):
            print(f"Error: ROM file '{args.rom}' not found.\n")
            sys.exit(1)

        data = read_rom(args.rom, args.start_offset, args.size)

        decompressed_data = decode_palette_stream(data, True)

        export_data(args.out_file, args.rom, decompressed_data)

    elif args.command == 'insert':
        if not os.path.exists(args.rom):
            print(f"Error: ROM file '{args.rom}' not found.\n")
            sys.exit(1)
        if not os.path.exists(args.in_file):
            print(f"Error: Input file '{args.in_file}' not found.\n")
            sys.exit(1)

        bank_size = args.size if args.size is not None else os.path.getsize(args.rom)

        data = import_data(args.in_file)

        compressed_data = compress_palette_stream(data)

        fill = args.fill is not None
        fill_value = args.fill if args.fill is not None else 0
        write_rom(args.rom, compressed_data, args.start_offset, bank_size, fill, fill_value, args.in_file)

    else:
        show_help()
        
if __name__ == "__main__":
    main()
    
