path=test/arm_project
arm-none-eabi-gcc -c $path/test_structs.c -o $path/test_structs.o -g -g -gdwarf-5
arm-none-eabi-objcopy -O ihex $path/test_structs.o $path/test_structs.hex
python pya2ltools/pya2ltools.py update_a2l --a2l_file $path/test.a2l --elf_file $path/test_structs.o