
#include <stdint.h>

#define MEM_SEC_PARAMETER __attribute__((section(".parameter")))

typedef struct
{
    uint8_t a;
    uint8_t b;
} SomeA;

typedef struct NestedStruct
{
    SomeA someA;
    uint8_t c;
} NestedStruct;

typedef enum SomeEnum
{
    SomeEnumA,
    SomeEnumB,
    SomeEnumC
} SomeEnum;

typedef struct RecursiveStruct
{
    struct RecursiveStruct* next;
    uint8_t a;
} RecursiveStruct;

MEM_SEC_PARAMETER static SomeA someA = { 69, 42 };
MEM_SEC_PARAMETER static NestedStruct nestedStruct = { { 0, 1 }, 2 };

MEM_SEC_PARAMETER static SomeEnum someEnum = SomeEnumA;

MEM_SEC_PARAMETER static NestedStruct nestedStructArray[2] = { { { 0, 1 }, 2 }, { { 3, 4 }, 5 } };

MEM_SEC_PARAMETER static RecursiveStruct recursiveStruct = { 0 };

int main(int argc, char** argv) {

    someA.a = 1;
    nestedStruct.someA.a = 1;
    nestedStructArray[0].someA.a = 2;
    recursiveStruct.a = 3;
    someEnum = SomeEnumB;

    return 0;
}