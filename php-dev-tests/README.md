# commits: https://github.com/php/php-src/commit/24c6f80

test command: 
```
make test TESTS="-d ocache.enable=1 -d opcache.enable_cli=1 -d opcache.jit_buffer_size=1M -d opcache.jit=1205 Zend/tests/ tests/ ext/opcache/tests/jit/"
```

## HYBRID VM + PROFITABILITY_CHECKS enable
### opcache.jit: 1205, 1215, 1225 and 1235

failed test cases: 4
```
Bug #80802: zend_jit_fetch_indirect_var assert failure with tracing JIT [ext/opcache/tests/jit/bug80802.phpt]
Bug #80839: PHP problem with JIT [ext/opcache/tests/jit/bug80861.phpt]
JIT Trampoline 001: trampoline cleanup [ext/opcache/tests/jit/trampoline_001.phpt]
JIT Trampoline 002: trampoline cleanup [ext/opcache/tests/jit/trampoline_002.phpt]
```
They failed because of the missing tracing JIT.

### opcache.jit:1203

another 3 test cases failed. **These 3 test cases would pass on x86.**
```
Test typed properties return by ref is allowed [Zend/tests/type_declarations/typed_properties_032.phpt]  --------------------1
Test typed properties yield reference guard [Zend/tests/type_declarations/typed_properties_033.phpt]     --------------------2
Typed property on overloaded by-ref property [Zend/tests/type_declarations/typed_properties_061.phpt]    --------------------3
Bug #80802: zend_jit_fetch_indirect_var assert failure with tracing JIT [ext/opcache/tests/jit/bug80802.phpt]
Bug #80839: PHP problem with JIT [ext/opcache/tests/jit/bug80861.phpt]
JIT Trampoline 001: trampoline cleanup [ext/opcache/tests/jit/trampoline_001.phpt]
JIT Trampoline 002: trampoline cleanup [ext/opcache/tests/jit/trampoline_002.phpt]
```

error msg: the three cases have the same error msg.
```
---- EXPECTED OUTPUT
int(15)
---- ACTUAL OUTPUT
int(15)
php: php-src/Zend/zend_execute.c:3323: zend_ref_del_type_source: Assertion `source_list->ptr == prop' failed.
Aborted (core dumped)

Termsig=6
---- FAILED
```

### opcache.jit:1204

another 2 test cases failed. **Note that bug No.4 also failed on x86.**
```
Testing callback formats within class method [Zend/tests/bug45180.phpt]               --------------------4
Bug #54268 (Double free when destroy_zend_class fails) [Zend/tests/bug54268.phpt]     --------------------5
Test typed properties return by ref is allowed [Zend/tests/type_declarations/typed_properties_032.phpt]
Test typed properties yield reference guard [Zend/tests/type_declarations/typed_properties_033.phpt]
Typed property on overloaded by-ref property [Zend/tests/type_declarations/typed_properties_061.phpt]
Bug #80802: zend_jit_fetch_indirect_var assert failure with tracing JIT [ext/opcache/tests/jit/bug80802.phpt]
Bug #80839: PHP problem with JIT [ext/opcache/tests/jit/bug80861.phpt]
JIT Trampoline 001: trampoline cleanup [ext/opcache/tests/jit/trampoline_001.phpt]
JIT Trampoline 002: trampoline cleanup [ext/opcache/tests/jit/trampoline_002.phpt]
```

error msg: segment fault.



