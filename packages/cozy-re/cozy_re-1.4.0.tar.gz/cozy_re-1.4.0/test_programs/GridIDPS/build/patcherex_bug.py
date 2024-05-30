import patcherex2

proj = patcherex2.Patcherex("amp_challenge_arm.ino_unstripped.elf")

# Make sure InsertFunctionPatch is working
# Applying the InsertFunctionPatch fails even if we comment out the body of flushSerial()
flushSerial_code = '''
void flushSerial() {
    while(usb_serial_available() > 0) {
        char t = usb_serial_getchar();
    }
}
'''
flushSerial_patch = patcherex2.InsertFunctionPatch("flushSerial", flushSerial_code)
proj.patches.append(flushSerial_patch)

# Make sure InsertInstructionPatch is working
instructionPatch_code = '''
nop
nop
'''
loop_addr = proj.binary_analyzer.get_function('loop')['addr']
instruction_patch = patcherex2.InsertInstructionPatch(loop_addr, instructionPatch_code)
proj.patches.append(instruction_patch)

proj.apply_patches()
proj.binfmt_tool.save_binary("amp_challenge_arm.ino_unstripped-draper-badpatch.elf")