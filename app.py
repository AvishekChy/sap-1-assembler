import re
from io import StringIO

import streamlit as st

opcode_map = {
    "LDA": 0x1,
    "LDB": 0x2,
    "ADD": 0x3,
    "SUB": 0x4,
    "STA": 0x5,
    "JMP": 0x6,
    "HLT": 0xF,
}

ops_with_arg = ["LDA", "LDB", "STA", "JMP"]
ops_without_arg = ["ADD", "SUB", "HLT"]


def assemble(asm_code):
    lines = asm_code.splitlines()

    # Pass 1: Resolve labels and handle ORG for addresses
    labels = {}
    address = 0
    for line in lines:
        line = line.strip().split(";")[0].strip()
        if not line:
            continue
        if line.endswith(":"):
            labels[line[:-1]] = address
            continue
        parts = re.split(r"\s+", line)
        op = parts[0].upper()
        if len(parts) > 1:
            arg = parts[1]
        else:
            arg = None
        if op == "ORG":
            if arg is None:
                raise ValueError("ORG requires an address")
            address = int(arg, 0)
        elif op == "DEC":
            if arg is None:
                raise ValueError("DEC requires a value")
            address += 1
        elif op in opcode_map:
            address += 1

    # Pass 2: Generate machine code
    mem = [0] * 16  # SAP-1 has 16 bytes RAM
    address = 0
    for line in lines:
        line = line.strip().split(";")[0].strip()
        if not line or line.endswith(":"):
            continue
        parts = re.split(r"\s+", line)
        op = parts[0].upper()
        if len(parts) > 1:
            arg = parts[1]
        else:
            arg = None
        if op == "ORG":
            address = int(arg, 0)
            continue
        elif op == "DEC":
            val = int(arg, 0)
            if val < 0 or val > 255:
                raise ValueError(f"DEC value out of range: {val}")
            mem[address] = val
            address += 1
            continue
        if op not in opcode_map:
            raise ValueError(f"Unknown opcode: {op}")
        if op in ops_with_arg:
            if arg is None:
                raise ValueError(f"{op} requires an argument")
            if arg in labels:
                arg_val = labels[arg]
            else:
                arg_val = int(arg, 0)
            if arg_val < 0 or arg_val > 0xF:
                raise ValueError(f"Address out of range: {arg_val}")
            code = (opcode_map[op] << 4) | (arg_val & 0x0F)
        elif op in ops_without_arg:
            if arg is not None:
                raise ValueError(f"{op} does not take an argument")
            code = opcode_map[op] << 4
        else:
            raise ValueError(f"Unsupported operation: {op}")
        mem[address] = code
        address += 1

    # Format as space-separated hex
    hex_code = " ".join(f"{byte:02X}" for byte in mem)
    return hex_code


st.title("Avishek SAP-1 Assembler for Logisim")

st.markdown(
    "Write your SAP-1 assembly code below. The assembler will convert it into a hex string for your Logisim ROM."
)

asm_input = st.text_area(
    "Assembly Code:",
    height=300,
    value="""LDA 13
LDB 14
""",
)
# JMP 5
# ORG 5
# ADD
# STA 15
# HLT

st.markdown(
    "Supported commands: LDA, LDB, ADD, SUB, STA, JMP, HLT. Use ORG [address] to set the origin, DEC [value] for decimal data."
)

if st.button("Assemble to Hex"):
    try:
        output = assemble(asm_input)
        st.session_state["hex_code"] = output
        st.success("Generated Hex Code:")
        st.code(output, language="text")
    except Exception as e:
        st.error(f"Error: {e}")


if "hex_code" in st.session_state:
    st.markdown("### Copy to Clipboard")
    st.components.v1.html(
        f"""
        <button onclick="navigator.clipboard.writeText('{st.session_state['hex_code']}')">Copy Hex Code</button>
        """,
        height=50,
    )
