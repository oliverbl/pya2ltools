base=test/arm_project
path=$base/out
mkdir $path
arm-none-eabi-gcc -c $base/test_structs.c -o $path/test_structs.obj -g -gdwarf-5
arm-none-eabi-ld -T $base/test.ld $path/test_structs.obj -o $path/test_structs.elf
arm-none-eabi-objcopy -O ihex -g $path/test_structs.elf $path/test_structs.hex
python pya2ltools/pya2ltools.py merge_a2l --main $base/test.a2l --secondary $base/test_slave.a2l --output $path/test_merged.a2l
python pya2ltools/pya2ltools.py update_a2l --a2l_file $path/test_merged.a2l --elf_file $path/test_structs.elf
python pya2ltools/pya2ltools.py create_calibration_data --a2l_file $path/test_merged.a2l --hex_file $path/test_structs.hex --output $path/calibration_data.json