import patcherex2

flushSerial_code = '''
void flushSerial() {
    char t;
    do {
        t = usb_serial_getchar();
    } while (t != \'\n\');
}
'''

verifyBufferPosition_code = '''
#define BUFFER_SIZE 18
#define SerialPrintln _ZN5Print7printlnEv

int verifyBufferPosition() {
    if (bufferPosition > BUFFER_SIZE - 1) {
        SerialPrintln("Buffer overflow detected. Resetting buffer.");
        bufferPosition = 0;
        memset(inputBuffer, 0, BUFFER_SIZE);
        flushSerial();
        SerialPrintln("Try Again");
        return 0;
    }
    return 1;
}
'''

def apply_badpatch():
    proj = patcherex2.Patcherex("amp_challenge_arm.ino_unstripped.elf")

    flushSerial_patch = patcherex2.InsertFunctionPatch("flushSerial", flushSerial_code)
    verifyBufferPosition_patch = patcherex2.InsertFunctionPatch("verifyBufferPosition", verifyBufferPosition_code)

    proj.patches.append(flushSerial_patch)
    #proj.patches.append(verifyBufferPosition_patch)

    proj.apply_patches()
    proj.binfmt_tool.save_binary("amp_challenge_arm.ino_unstripped-draper-badpatch.elf")

apply_badpatch()