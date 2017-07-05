#include <stdlib.h>
#include "fail.h"
#include "print.h"
#include "avr.h"

void fail(const char *error)
{
  print("ERROR: ");
  print(error);
  print("\n");
  avr_end();
  exit(-1);
}
