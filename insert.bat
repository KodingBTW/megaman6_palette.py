set ROM="Mega Man 6 (USA).nes"

megaman6_palette.py insert -r %ROM% -f "main_screen.pal" -o "0x6F2E9" -s "0x19" --fill
pause