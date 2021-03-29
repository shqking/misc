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
  printf("insn count: %zu\n\n", count);

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
  dump_disasm(buf, sz); // disasm
  return buf;
}

struct stu
{
  int id;
  int score;
  int age;
};

typedef struct bf_state
{
  unsigned char* tape;
  unsigned char (*get_ch)(struct bf_state*);
  void (*put_ch)(struct bf_state*, unsigned char);
} bf_state_t;

|.arch arm64
|.section code, stub
|.globals lbl_
|.actionlist bf_actions
|.type STATE, bf_state_t, x2

static void bar(dasm_State **Dst)
{
  |.code
  | cmp Rx(15), #42
  | mov x3, #1
  | add Rw(5+1), Rw(7), Rw(22)
  | ldr Rx(4), [Rx(2), #8]!
  | str x0, [Rx(2), #offsetof(struct stu, age)]
  | ldr x8, STATE->get_ch
  return;
}

static void compile_test()
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
  link_and_encode(&d);
  dasm_free(&d);
  return;
}

int main(int argc, char** argv)
{
  printf("strat===\n\n");
  compile_test();
  printf("\nend===\n");
  return 0;
}
