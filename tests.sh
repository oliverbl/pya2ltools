gcc test/gcc/test_structs.c -o test_structs.o -g -gdwarf-3
python pya2ltools/pya2ltools.py -> test_out/test_gcc_dwarf3.txt

gcc test/gcc/test_structs.c -o test_structs.o -g -gdwarf-4
python pya2ltools/pya2ltools.py -> test_out/test_gcc_dwarf4.txt

gcc test/gcc/test_structs.c -o test_structs.o -g -gdwarf-5
python pya2ltools/pya2ltools.py -> test_out/test_gcc_dwarf5.txt

clang test/gcc/test_structs.c -o test_structs.o -gdwarf-3
python pya2ltools/pya2ltools.py -> test_out/test_clang_dwarf3.txt

clang test/gcc/test_structs.c -o test_structs.o -gdwarf-4
python pya2ltools/pya2ltools.py -> test_out/test_clang_dwarf4.txt

rm test_structs.o