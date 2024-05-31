from libmem import *
import ctypes
import struct
import time
import os

def separator():
    print("========================================")

print("[*] libmem-py tests")

separator()

print("[*] Process Enumeration")
print("\n".join([str(proc) for proc in LM_EnumProcesses()[:5]]))

separator()

print("[*] Current Process")
curproc = LM_GetProcess()
print(curproc)

separator()

print("[*] Parent Process of Current Process")
parent_proc = LM_GetProcessEx(curproc.ppid)
print(parent_proc)

separator()

print("[*] Remote Process")
proc = LM_FindProcess("target")
print(proc)

separator()

print(f"[*] Is Remote Process Alive? {'Yes' if LM_IsProcessAlive(proc) else 'No'}")

separator()

print(f"[*] System Bits: {LM_GetSystemBits()}")

separator()

print(f"[*] Current Process Threads: {LM_EnumThreads()}")

separator()

print(f"[*] Remote Process Threads: {LM_EnumThreadsEx(proc)}")

separator()

thread = LM_GetThread()
print(f"[*] Current Thread: {thread}")

separator()

print(f"[*] Remote Thread: {LM_GetThreadEx(proc)}")

separator()

print(f"[*] Process From Thread '{thread}': {LM_GetThreadProcess(thread)}")

separator()

print("[*] Module Enumeration - Current Process")
print("\n".join([str(mod) for mod in LM_EnumModules()[:5]]))

separator()

print("[*] Module Enumeration - Remote Process")
print("\n".join([str(mod) for mod in LM_EnumModulesEx(proc)[:5]]))

separator()

curmod = LM_FindModule(curproc.path)
print(f"[*] Current Process Module: {curmod}")

separator()

mod = LM_FindModuleEx(proc, proc.path)
print(f"[*] Remote Process Module: {mod}")

separator()

libpath = f"{os.path.dirname(os.path.realpath(__file__))}{os.sep}{os.pardir}{os.sep}{os.pardir}{os.sep}{os.pardir}{os.sep}build{os.sep}tests{os.sep}libtest.so"
print(f"[*] Loadable Library Path: {libpath}")
cur_loaded_mod = LM_LoadModule(libpath)
print()
print(f"[*] Loaded Module into Current Process: {cur_loaded_mod}")

LM_UnloadModule(cur_loaded_mod)
print("[*] Unloaded Module from Current Process")

separator()

loaded_mod = LM_LoadModuleEx(proc, libpath)
print("[*] Loaded Module into Target Process: ", loaded_mod)

LM_UnloadModuleEx(proc, loaded_mod)
print("[*] Unloaded Module from Target Process")

separator()

print("[*] Symbol Enumeration")

print("\n".join([str(sym) for sym in LM_EnumSymbols(curmod)[:5]]))

separator()

print("[*] Symbol Address Search")

symaddr = LM_FindSymbolAddress(curmod, "Py_BytesMain")
if symaddr == None:
    symaddr = LM_FindSymbolAddress(curmod, "_start_c")
print(f"[*] Py_BytesMain Address: {hex(symaddr)}")

separator()

mangled = "_Z15_LM_EnumSymbolsP11lm_module_tPFiP11lm_symbol_tPvES3_"
demangled = LM_DemangleSymbol(mangled)
print(f"[*] Demangled '{mangled}': {demangled}")

separator()

print("[*] Demangled Symbol Enumeration")

print("\n".join([str(sym) for sym in LM_EnumSymbolsDemangled(curmod)[:5]]))

separator()

symaddr = LM_FindSymbolAddressDemangled(curmod, "Py_BytesMain")
if symaddr == None:
    symaddr = LM_FindSymbolAddressDemangled(curmod, "_start_c")
print(f"[*] Py_BytesMain Address (Demangled): {hex(symaddr)}")

separator()

print("[*] Segment Enumeration - Current Process")
print("\n".join([str(segment) for segment in LM_EnumSegments()[:5]]))

separator()

print("[*] Segment Enumeration - Remote Process")
print("\n".join([str(segment) for segment in LM_EnumSegmentsEx(proc)[:5]]))

separator()

print(f"[*] Segment From Current Process Module: {LM_FindSegment(symaddr)}")

separator()

print(f"[*] Segment From Remote Process Module: {LM_FindSegmentEx(proc, mod.base)}")

separator()

val = ctypes.c_int(10)
val_addr = ctypes.addressof(val)
rdbuf = LM_ReadMemory(val_addr, ctypes.sizeof(val))
rdval = struct.unpack("@i", rdbuf)[0]
print(f"[*] Read Integer From '{hex(val_addr)}': {str(rdval)}")

separator()

# TODO: Add tests for 'LM_ReadMemoryEx'
# separator()

LM_WriteMemory(val_addr, bytearray(b"\x39\x05\x00\x00"))
print(f"[*] Integer After LM_WriteMemory: {val}")

separator()

# TODO: Add tests for 'LM_WriteMemoryEx'
# separator()

LM_SetMemory(val_addr, b"\x00", ctypes.sizeof(val))
print(f"[*] Integer After LM_SetMemory: {val}")

separator()

# TODO: Add tests for 'LM_SetMemoryEx'
# separator()

print("[*] Changing Memory Protection - Current Process")
old_prot = LM_ProtMemory(curmod.base, 0x1000, LM_PROT_XRW)
print(f"[*] Old Memory Protection ({hex(curmod.base)}): {old_prot}")
segment = LM_FindSegment(curmod.base)
print(f"[*] Current Memory Protection ({hex(curmod.base)}): {segment.prot}")

separator()

print("[*] Changing Memory Protection - Remote Process")
old_prot = LM_ProtMemoryEx(proc, mod.base, 0x1000, LM_PROT_XRW)
print(f"[*] Old Memory Protection ({hex(mod.base)}): {old_prot}")
segment = LM_FindSegmentEx(proc, mod.base)
print(f"[*] Current Memory Protection ({hex(mod.base)}): {segment.prot}")

separator()

alloc_size = 0x1000
alloc = LM_AllocMemory(alloc_size, LM_PROT_XRW)
print(f"[*] Allocated Memory - Current Process: {hex(alloc)}")
LM_FreeMemory(alloc, alloc_size)

separator()

alloc = LM_AllocMemoryEx(proc, alloc_size, LM_PROT_XRW)
print(f"[*] Allocated Memory - Remote Process: {hex(alloc)}")
LM_FreeMemoryEx(proc, alloc, alloc_size)

separator()

addr0 = LM_AllocMemory(4, LM_PROT_RW)
addr1 = LM_AllocMemory(8, LM_PROT_RW)
addr2 = LM_AllocMemory(8, LM_PROT_RW)

LM_WriteMemory(addr0, bytearray(b"\x10\x00\x00\x00"))
LM_WriteMemory(addr1, bytearray(addr0.to_bytes(8, byteorder="little")))
LM_WriteMemory(addr2, bytearray(addr1.to_bytes(8, byteorder="little")))
print("[*] Address 0: ", hex(addr0))
print("[*] Address 1: ", hex(addr1))
print("[*] Address 2: ", hex(addr2))

deep_ptr = LM_DeepPointer(addr2, [0, 0])
print("[*] Deep Pointer result: " + hex(deep_ptr))

value = int.from_bytes(LM_ReadMemory(deep_ptr, 4), byteorder="little")
print("[*] Deep Pointer value: " + hex(value))

separator()

buf = ctypes.c_buffer(b"\x10\x20\x30\x40\x50\x60\x70\x80\x90\xA0")
buf_addr = ctypes.addressof(buf)
print(f"[*] Scanning For Buffer At: {hex(buf_addr)}")
scan_addr = buf_addr - 0x10
scan_size = 0x100
data_scan = LM_DataScan(bytearray(buf.value), scan_addr, scan_size)
print(f"[*] Data Scan Match: {hex(data_scan)}")
pattern_scan = LM_PatternScan(bytearray(buf.value), "xxxx?x?x?x", scan_addr, scan_size)
print(f"[*] Pattern Scan Match: {hex(pattern_scan)}")
sig_scan = LM_SigScan("10 20 30 40 ?? ?? 70 80 ?? A0", scan_addr, scan_size)
print(f"[*] Signature Scan Match: {hex(sig_scan)}")

separator()

scan_alloc = LM_AllocMemoryEx(proc, 1024, LM_PROT_RW)
print(f"[*] External Scan Alloc: {hex(scan_alloc)}")
buf_addr = scan_alloc + 0x10
LM_WriteMemoryEx(proc, buf_addr, bytearray(buf.value))
print(f"[*] Externally Scanning For Buffer At: {hex(buf_addr)}")
scan_addr = buf_addr - 0x10
scan_size = 0x100
data_scan = LM_DataScanEx(proc, bytearray(buf.value), scan_addr, scan_size)
print(f"[*] Data Scan Match: {hex(data_scan)}")
pattern_scan = LM_PatternScanEx(proc, bytearray(buf.value), "xxxx?x?x?x", scan_addr, scan_size)
print(f"[*] Pattern Scan Match: {hex(pattern_scan)}")
sig_scan = LM_SigScanEx(proc, "10 20 30 40 ?? ?? 70 80 ?? A0", scan_addr, scan_size)
print(f"[*] Signature Scan Match: {hex(sig_scan)}")

# TODO: Add tests for 'LM_HookCode' and 'LM_UnhookCode'
# separator()

wait_message_addr = LM_FindSymbolAddress(mod, "wait_message")
hk_wait_message_addr = LM_FindSymbolAddress(mod, "hk_wait_message")
trampoline = LM_HookCodeEx(proc, wait_message_addr, hk_wait_message_addr)
print(f"[*] External Hook Trampoline: {trampoline}")
time.sleep(3)
LM_UnhookCodeEx(proc, wait_message_addr, trampoline)
print("[*] Unhooked External Function")

separator()

print("[*] Assemblying Instruction")
inst = LM_Assemble("mov eax, ebx")
print(inst)

separator()

print("[*] Assemblying Instructions")
insts = LM_AssembleEx("push ebp; mov ebp, esp; mov esp, ebp; pop ebp; ret", LM_ARCH_X86, 0)
print(", ".join([hex(b) for b in insts]))

separator()

print("[*] Disassembly of PyBytesMain Instruction")
inst = LM_Disassemble(symaddr)
print(inst)

separator()

print("[*] Disassembly of PyBytesMain Instructions")
insts = LM_DisassembleEx(symaddr, LM_ARCH_X86, 0x100, 5, symaddr)
print("\n".join([str(inst) for inst in insts]))

separator()

minlength = 0x5
aligned_length = LM_CodeLength(symaddr, minlength)
print(f"[*] Aligned Length for Minimum '{minlength}' Bytes is '{aligned_length}' Bytes (PyBytesMain)")

separator()

# TODO: Add tests for 'LM_CodeLengthEx'
# separator()

print("[*] VMT Hooking")

vtable = ctypes.c_ulonglong(0x1020304050607080)
vmt = lm_vmt_t(ctypes.addressof(vtable))
print(f"[*] Original Function: {hex(vmt.get_original(0))}")
vmt.hook(0, 0xdeadbeef)
print(f"[*] VMT After Hook: {hex(vtable.value)}")
vmt.unhook(0)
# vmt.reset()
print(f"[*] VMT After Unhook: {hex(vtable.value)}")

separator()

