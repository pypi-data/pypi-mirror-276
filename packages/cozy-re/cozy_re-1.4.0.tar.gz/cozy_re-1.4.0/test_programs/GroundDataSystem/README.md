
## Overview

Target 5 for the NASA combined challenge problem is a GSFC-developed processing node that demonstrates a Ground Data System (GDS) performing processing that is typically necessary for uncrewed science missions. It integrates the open-source Telemetry & Commanding (T&C) system OpenC3 COSMOS (https://openc3.com/) with a custom science data processing and satellite encoding adapter implemented as Linux ELF applications running in a RHEL8 containerized x86_64 (amd64) environment.

Interestingly enough, the same library is used in flight. A version of the flight version of the library (for PowerPC e500v2) is also uploaded here.

Science Data Decoder Binary information:

libscience-0.so:              ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, BuildID[sha1]=2b78aecdbc0f913c1c63491b24e464d6f3c45e06, not stripped
libscience-0_powerpc-e500.so: ELF 32-bit MSB shared object, PowerPC or cisco 4500, version 1 (SYSV), dynamically linked, BuildID[sha1]=ff3fea60e99f9bdcf0e0865e27a40b5c5f7b83d4, with debug_info, not stripped

gs_data_processor: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=901d15768fa5d08002d0e12bcab36a736aba9b75, not stripped

## Features

- Initialize communication channel with the Comm Relay Satellite with predefined settings.
- Construct CCSDS command packets for both the Comm Relay Satellite and Rover and commands.
- Parse CCSDS telemetry packets from both the Comm Relay Satellite and Rover.
- Convert temperature readings from Celsius to Fahenheit.
- Display direction of Rover movement.

## Identified Bug and Implications

The binary contains an error in processing of CCSDS Space Packets and extracting Science Protocol Data Units (PDUs) from within the packets.

Implications:

- Given perfect imput, the binary performs correctly
- Unfortunatey, due to buffering issues on the Analog to Digital conversion (receiving data over the RF link), sometimes more than one CCSDS SPP packet makes it through
- Additionally, a truncated packet is also possible as input

## Possible Micro-Patch

### Background
Reference on Space Packet Protocol: https://public.ccsds.org/Pubs/133x0b2e1.pdf

The CCSDS Length header (bytes 5-6 of the packet, big-endian 16-bit unsigned int) specifies the expected length of the packet, using the calculation total packet size - 6 (subtracting the primary header) - 1. So for a 12-byte packet, the length field should be big endian 5, or 0x0005.

The expected structure we would receive in buf with length len:
[ CCSDS Space Packet (6-byte SPP header) (1 or more 6-byte science PDUs) ]
The actual cases we are seeing due to buffering issues:
[ CCSDS Space Packet (6-byte SPP header) (1 or more 6-byte science PDUs) ][ CCSDS Space Packet (6-byte SPP header) (1 or more 6-byte science PDUs) ]

Additionally, in some cases the last CCSDS packet is truncated, resulting in the last PDU missing 1 or more bytes of data. In this case, it would be optimal if the data processor could attempt to process all PDUs in the stream except for the final truncated PDU.

The binary as-delivered attempts to read as many complete PDUs as it can from the supplied packet, however because it was not programmed to handle multiple sequentail packets being stored in buf, it incorrectly processes any subsequent CCSDS headers as a Science PDU (which inserts a 6-byte "garbage" PDU into the science data collection).

### Approach 1

There is a desire to retain as much science data as possible, so a basic approach of truncating the buffer based on the packet length read (and dropping any excess bytes in the buffer) would guarantee only valid data was processed.

However, this "simple" patch would result in any "bonus" concatenated packets being dropped.

### Approach 2

One could add logic to iterate through multiple complete packets if contained in the buffer. But if there were a partial packet containing at last one valid science PDU, this supplemental data would be dropped.

Ideally we would like to retain all complete science PDUs in the output for delivery to the scientists.

### Approach 3

The "Best" option would be to try and retain ALL complete PDUs. Right now that is the behavior we are seeing, however supplemental packet headers (which happen to also be 6-bytes) are showing up as corrupt PDUs being injected into the stream sent to the Science Data Processor.

### Function to be patched
Conveniently, the science data processing code is located in a dynamic library called libscience. That library is called by our science data processor app to perform the packet decoding for us.

We were delivered this header that describes the library interface to libscience:

libscience.so:
```c
/**
 * processSciencePacket:
 *   buf: Buffer containing a single CCSDS SPP science data packet
 *   len: Length of buffer in bytes
*/
int processSciencePacket(char* buf, int len) ;
```

It is designed to receive a single CCSDS packet in a buffer, containing one or more science PDUs (6-bytes each), but due to the system not behaving as expected multiple packets might be sent in the buf or a truncated packet (or multiple complete packets followed by a truncated packet) might be sent in the buffer.

Here is an example buffer in binhex that contains two complete Space Packets each containing 4 science PDUs for a total of 8 PDUs:
```c
0x0011223300170001DEADBEEF0002DEADBEEF0003DEADBEEF0004DEADBEEF0011223300170005DEADBEEF0006DEADBEEF0007DEADBEEF0008DEADBEEF
```
And here is one with 7 total valid PDUs (the 8th is truncated by two bytes, making the 8th and final PDU truncated):
```c
0x0011223300170001DEADBEEF0002DEADBEEF0003DEADBEEF0004DEADBEEF0011223300170005DEADBEEF0006DEADBEEF0007DEADBEEF0008DEAD
```

Added a test driver! It uses the following buffer to test the libscience-0.so call:
```c
    char buf[] = { 0x00, 0x11, 0x22, 0x33, 0x00, 0x17,
                   0x00, 0x01, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x02, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x03, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x04, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x11, 0x11, 0x11, 0x00, 0x17,
                   0x00, 0x01, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x02, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x03, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x04, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x22, 0x22, 0x22, 0x00, 0x17,
                   0x00, 0x01, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x02, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x03, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x04, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x33, 0x33, 0x33, 0x00, 0x17,
                   0x00, 0x01, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x02, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x03, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x04, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x44, 0x44, 0x44, 0x00, 0x17,
                   0x00, 0x01, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x02, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x03, 0xDE, 0xAD, 0xBE, 0xEF,
                   0x00, 0x04, 0xDE, 0xAD,
     } ;
```

You can run it on your patched libscience-0.so with the following (assuming they are in the same directory):
```cLD_LIBRARY_PATH=. ./science_dp```

### Old Challenge Problem from November: Temperature Formating

To address the formatting error, replace:

```c
int32_t rover_process(RoverMessage_t* msg){

    //convert Kelvin to Farhenheit.
    temp = ( (temp - 273) * 1.8 ) + 32;

}
```
With:

```c
int32_t rover_process(RoverMessage_t* msg){

    //convert Celsius to Farhenheit.
    temp = ( temp * 1.8 ) + 32;

}
```

These changes will ensure that the we have data in farhenheit.

### Output expectation

The packet viewer in Cosmos will display both the incomping data to and outgoing data from the science data app and can be used to determine the correctness of the temperature conversion performed in the app.  

Also there will be a telemetry screen in Cosmos that will display the converted value
