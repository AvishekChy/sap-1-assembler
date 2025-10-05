# SAP-1 CPU (Simple-As-Possible) — Logisim Evolution

<p align="center">
  <img src="https://img.shields.io/badge/SAP--1%20CPU-blue?style=for-the-badge&logo=circuit-board&logoColor=white" alt="SAP-1 CPU Badge">
  <img src="https://img.shields.io/badge/Logisim-green?style=for-the-badge&logo=google-circles&logoColor=white" alt="Logisim Badge">
</p>

## Table of Contents

- [Project Overview](#overview)
- [Features](#features)
- [Video Tutorials](#video-tutorials)
- [Final Circuits](#final-circuits)
- [Architecture Components](#architecture-components)
- [Control Unit (Hardwired)](#control-unit)
- [Instruction Set & Example](#example-program)
- [Assembler](#assembler)
- [Fetch–Decode–Execute Cycle](#fde)
- [Run the CPU — Auto Mode](#run-auto)
- [Run the CPU — Manual Mode](#run-manual)
- [Future Improvements](#roadmap)

---

<a id="overview"></a>

## Project Overview

This repository showcases my implementation of the Simple-As-Possible (SAP-1) CPU using Logisim Evolution. The SAP-1 is an educational 8-bit computer architecture designed to demonstrate the fundamentals of CPU operation.

My implementation includes a hardwired control unit that automates the fetch-decode-execute cycle, enhanced with a ROM-based bootloader for seamless program loading into RAM. This eliminates manual data entry, streamlining the process of running programs. The project successfully executes a program that performs both addition and subtraction on two 8-bit values, storing the result in memory.

---

<a id="features"></a>

## Features

- **Data Loading:** Supports `LDA` and `LDB` to load data into registers A and B.
- **Arithmetic Operations:** Executes `ADD` and `SUB` operations between registers.
- **Data Storage:** Uses `STA` to store Register A's contents in memory.
- **Control Flow:** Implements `JMP` for jumping to specific memory addresses.
- **Program Execution:** Sequentially processes instructions via the Program Counter.
- **Instruction Handling:** Automates fetching, decoding, and execution through the Instruction Register and control logic.
- **Halt Functionality:** Stops execution with the `HLT` instruction.
- **Debug Mode:** Enables step-by-step control via Logisim pins for debugging.
- **Memory Management:** Supports a 4-bit address space (16 addresses) for 8-bit data.
- **ROM Storage:** Stores programs in ROM for persistent storage.
- **Bootloader:** Automatically loads programs from ROM to RAM in debug mode for easy initialization.

---

<a id="video-tutorials"></a>

## Video Tutorials

I created video guides to explain the SAP-1 CPU implementation and simulation process:

- Auto Code Loading (`my_sap1_auto.circ`): [Link to video](#)
- Manual Code Loading (`my_sap1_manual.circ`): [Link to video](#)

_Note: Video links will be updated once uploaded._

---

<a id="final-circuits"></a>

## Final Circuits

- **Auto Code Loading (`my_sap1_auto.circ`)**  
  ![Main Control Unit](my_sap1_img/my_sap1_auto.png)

- **Manual Code Loading (`my_sap1_manual.circ`)**  
  ![Main Control Unit](my_sap1_img/my_sap1_main.png)

_Note: Replace placeholder image paths with your actual image files._

---

<a id="architecture-components"></a>

## Architecture Components

The SAP-1 CPU consists of the following core components:

- **Program Counter (PC):** A 4-bit counter tracking the next instruction's memory address, incrementing after each fetch.  
  ![Program Counter](my_sap1_img/my_sap1_pc.png)

- **Random Access Memory (RAM):** A 16-byte, 8-bit wide memory for storing instructions and data.  
  ![RAM](my_sap1_img/my_sap1_sram.png)

- **Memory Address Register (MAR):** A 4-bit register holding the current memory address for read/write operations.

- **Instruction Register (IR):** An 8-bit register storing the fetched instruction, split into a 4-bit opcode and 4-bit operand.  
  ![IR](my_sap1_img/my_sap1_ins_reg.png)

- **Registers A & B:** 8-bit registers, with A as the accumulator for arithmetic and B for holding secondary operands.  
  ![Registers A & B](my_sap1_img/my_sap1_reg_gp.png)

- **Arithmetic Logic Unit (ALU):** Performs 8-bit addition and subtraction on data from Registers A and B.  
  ![ALU](my_sap1_img/my_sap1_alu.png)

- **Instruction Loader:** Transfers instructions from ROM to RAM using clock pulses.  
  ![Instruction Loader](my_sap1_img/my_sap1_ins_loader.png)

- **Control Unit:** Orchestrates CPU operations by generating control signals for the fetch-decode-execute cycle.  
  ![Control Unit](my_sap1_img/my_sap1_control.png)

---

<a id="control-unit"></a>

## Control Unit (Hardwired)

The hardwired control unit uses combinational logic and a state counter to manage CPU operations.

### Subcomponents

- **State Counter (RC):** A 3-bit counter cycling through T-states (T1–T6).  
  ![State Counter](my_sap1_img/my_sap1_rc.png)

- **Opcode Decoder:** A 4-to-16 decoder translating the Instruction Register's opcode into instruction-specific signals.  
  ![Instruction Decoder](my_sap1_img/my_sap1_ins_dec.png)

- **Control Matrix:** Combines T-state and opcode signals to activate control pins via AND/OR gates.

### Control Signals — Auto Mode (`my_sap1_auto.circ`)

The control signals are defined by Boolean equations, implemented as logic gates. `cpu_mode` is `NOT(debug)` for automated operation.

- `pc_out_final = T1 AND cpu_mode AND (NOT l2)`
- `mar_in_en_final = (T1 AND cpu_mode) OR ((T4 AND isLDA) AND cpu_mode) OR ((T4 AND isLDB) AND cpu_mode) OR ((T4 AND isSTA) AND cpu_mode) OR (l2 AND debug)`
- `sram_rd_final = (T2 AND cpu_mode) OR ((T5 AND isLDA) AND cpu_mode) OR ((T5 AND isLDB) AND cpu_mode AND (NOT l2))`
- `ins_reg_in_en_final = T2 AND cpu_mode AND (NOT l2)`
- `pc_en_final = T3 AND cpu_mode AND (NOT l2)`
- `ins_reg_out_en_final = ((T4 AND isLDA) AND cpu_mode) OR ((T4 AND isLDB) AND cpu_mode) OR ((T4 AND isSTA) AND cpu_mode) OR (T3 AND isJMP)`
- `a_in_final = ((T5 AND isLDA) AND cpu_mode) OR ((T4 AND isADD) AND cpu_mode AND (NOT l2))`
- `a_out_final = ((T4 AND isADD) AND cpu_mode) OR ((T5 AND isSTA) AND cpu_mode AND (NOT l2))`
- `b_in_final = (T5 AND isLDB) AND cpu_mode AND (NOT l2)`
- `b_out_final = (T4 AND isADD) AND cpu_mode AND (NOT l2)`
- `alu_out_final = (T4 AND isADD) AND cpu_mode AND (NOT l2)`
- `sram_wr_final = ((T5 AND isSTA) AND (NOT l2)) OR (l2 AND debug)`
- `alu_sub = (T4 AND isSUB) AND cpu_mode AND (NOT l2)`
- `hlt = T4 AND isHLT AND (NOT l2)`
- `jmp_en = (T3 AND isJMP) AND cpu_mode AND (NOT l2)`

### Control Signals — Manual Mode (`my_sap1_manual.circ`)

- `pc_out_final = T1 AND cpu_mode`
- `mar_in_en_final = (T1 AND cpu_mode) OR ((T4 AND isLDA) AND cpu_mode) OR ((T4 AND isLDB) AND cpu_mode) OR ((T4 AND isSTA) AND cpu_mode) OR (mar_in_en_manual AND debug)`
- `sram_rd_final = (T2 AND cpu_mode) OR ((T5 AND isLDA) AND cpu_mode) OR ((T5 AND isLDB) AND cpu_mode)`
- `ins_reg_in_en_final = T2 AND cpu_mode`
- `pc_en_final = T3 AND cpu_mode`
- `ins_reg_out_en_final = ((T4 AND isLDA) AND cpu_mode) OR ((T4 AND isLDB) AND cpu_mode) OR ((T4 AND isSTA) AND cpu_mode)`
- `a_in_final = ((T5 AND isLDA) AND cpu_mode) OR ((T4 AND isADD) AND cpu_mode)`
- `a_out_final = ((T4 AND isADD) AND cpu_mode) OR ((T5 AND isSTA) AND cpu_mode)`
- `b_in_final = (T5 AND isLDB) AND cpu_mode`
- `b_out_final = (T4 AND isADD) AND cpu_mode`
- `alu_out_final = (T4 AND isADD) AND cpu_mode`
- `alu_sub = (T4 AND isSUB) AND cpu_mode`
- `cs_en = 1`
- `sram_wr_final = ((T5 AND isSTA) AND cpu_mode) OR (sram_wr_manual AND debug)`
- `hlt = T4 AND isHLT`

**Debug Mode Note:** When `debug` is HIGH, `cpu_mode` is LOW, disabling automatic signals. Manual control of `mar_in_en_final` and `sram_wr_final` enables RAM programming, with other bus outputs disabled to prevent conflicts.

---

<a id="example-program"></a>

## Machine Code Program: Addition and Subtraction

This program loads two 8-bit values (e.g., 51 and 25), performs addition and subtraction, and stores the results in memory.

### Memory Addresses

- Value 1: `00110011` (51, Hex `33`) at `00001101` (13)
- Value 2: `00011001` (25, Hex `19`) at `00001110` (14)
- Addition Result: `01001100` (76, Hex `4C`) at `00001111` (15)
- Subtraction Result: `00001010` (26, Hex `1A`) at `00001100` (12)

### Instruction Set & Program

| Address (Binary) | Instruction (Binary) | Hex  | Mnemonic & Explanation                     |
| ---------------- | -------------------- | ---- | ------------------------------------------ |
| `00000000`       | `0001 1101`          | `1D` | `LDA 13` (Load value from address 13 to A) |
| `00000001`       | `0010 1110`          | `2E` | `LDB 14` (Load value from address 14 to B) |
| `00000010`       | `0011 0000`          | `30` | `ADD` (Add B to A, store in A)             |
| `00000011`       | `0101 1111`          | `5F` | `STA 15` (Store A to address 15)           |
| `00000100`       | `0100 0000`          | `40` | `SUB` (Subtract B from A, store in A)      |
| `00000101`       | `0101 1100`          | `5C` | `STA 12` (Store A to address 12)           |
| `00000110`       | `1111 0000`          | `F0` | `HLT` (Halt execution)                     |

### Data Values in RAM

| Address (Binary) | Data (Binary) | Decimal | Hex  |
| ---------------- | ------------- | ------- | ---- |
| `00001101`       | `00110011`    | 51      | `33` |
| `00001110`       | `00011001`    | 25      | `19` |

---

<a id="assembler"></a>

## Assembler

Use my SAP-1 assembler to convert assembly code into hex for Logisim ROM: [my-sap1-assembler.vercel.app](#)

**Example:**

**Assembly Code (Add & Sub):**
