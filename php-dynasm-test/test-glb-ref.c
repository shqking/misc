#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <inttypes.h>

#include <capstone/capstone.h>

#include "/home/haosun01/php/php-src/ext/opcache/jit/dynasm/dasm_proto.h"
#include "/home/haosun01/php/php-src/ext/opcache/jit/dynasm/dasm_arm64.h"

int dump_disasm(void* start, size_t size)
{
	csh handle;
	cs_insn *insn;
	size_t count;

	if (cs_open(CS_ARCH_ARM64, CS_MODE_ARM, &handle) != CS_ERR_OK)
		return -1;

	count = cs_disasm(handle, start, size, (uintptr_t)start, 0, &insn);
	if (count > 0) {
		size_t j;
		for (j = 0; j < count; j++) {
			printf("0x%"PRIx64":\t%s\t\t%s\n", insn[j].address, insn[j].mnemonic,
					insn[j].op_str);
		}

		cs_free(insn, count);
	} else
		printf("ERROR: Failed to disassemble given code!\n");

	cs_close(&handle);
  return 1;
}

static void* link_and_encode(dasm_State** d)
{
  size_t sz;
  void* buf;
  dasm_link(d, &sz);
  buf = mmap(0, sz, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
  dasm_encode(d, buf);
  mprotect(buf, sz, PROT_READ | PROT_EXEC);
  dump_disasm(buf, sz);  // dump the disassemly
  return buf;
}

|.arch arm64
|.section code, stub
|.globals lbl_
|.actionlist bf_actions

static int foo(dasm_State **Dst)
{
  |.code
  |->foo_0:
  | brk #0

  |->foo_1:
  | brk #1

  |->foo_2:
  | brk #2

  |->foo_3:
  | brk #3
  
  |->foo_4:
  | brk #4

  |->foo_5:
  | brk #5

  |->foo_6:
  | brk #6

  |->foo_7:
  | brk #7

  |->foo_8:
  | brk #8

  |->foo_9:
  | brk #9

  |->foo_10:
  | brk #10

  |->foo_11:
  | brk #11

  |->foo_12:
  | brk #12

  |->foo_13:
  | brk #13

  return 1;
}

void foo_stub()
{
  dasm_State* d;
  void* labels[lbl__MAX];
  unsigned npc = 8;
  unsigned nextpc = 0;
  dasm_init(&d, DASM_MAXSECTION);
  dasm_setupglobal(&d, labels, lbl__MAX);
  dasm_setup(&d, bf_actions);
  dasm_growpc(&d, npc);
  foo(&d);
  printf("function foo:\n");
  link_and_encode(&d);
  printf("\n\n");
  dasm_free(&d);
}

static int bar(dasm_State **Dst)
{
  |.code
  | b ->foo_0
  | b ->foo_9
  | b ->foo_10
  | b ->foo_13

  return 1;
}


void bar_stub()
{
  dasm_State* d;
  void* labels[lbl__MAX];
  unsigned npc = 8;
  unsigned nextpc = 0;
  dasm_init(&d, DASM_MAXSECTION);
  dasm_setupglobal(&d, labels, lbl__MAX);
  dasm_setup(&d, bf_actions);
  dasm_growpc(&d, npc);
  bar(&d);
  printf("function bar:\n");
  link_and_encode(&d);
  printf("\n\n");
  dasm_free(&d);
}

int main(int argc, char** argv)
{
  printf("strat===\n\n");

  foo_stub();
  bar_stub();

  printf("end===\n");
  return 0;
}
