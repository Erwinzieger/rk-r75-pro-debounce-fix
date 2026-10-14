"""Patch the debounce time of the official RK R75 Pro (PID E487) firmware v11.

The official firmware uses QMK's sym_defer_g debounce with DEBOUNCE = 1 ms,
which makes keys chatter (double typing) on some boards. This script changes
only two bytes to raise it to the value you choose.

Usage:
    python patch_debounce.py <official_v11.hex> <ms> <output.hex>

Example:
    python patch_debounce.py R75Pro_v11_original_1ms.hex 5 R75Pro_v11_debounce_5ms.hex
"""

import hashlib
import sys

OFFICIAL_SHA256 = "f3ec95ba5265b8d55657c392d410514f16094550dacc82ca5ab033498d660f91"

# debounce(): "cmp r0, #0 / beq" at 0x080071E6 (elapsed >= 1 ms)
EXPECTED = {0x080071E6: 0x00, 0x080071E7: 0x28, 0x080071E8: 0xF5, 0x080071E9: 0xD0}


def patch(src, ms, dst):
    if not 1 <= ms <= 255:
        sys.exit("ms must be between 1 and 255")
    data = open(src, "rb").read()
    if hashlib.sha256(data).hexdigest() != OFFICIAL_SHA256:
        sys.exit("Input is not the official R75 Pro v11 firmware (SHA-256 mismatch). Aborting.")

    # "cmp r0, #ms / blo" -> wait until elapsed >= ms
    changes = {0x080071E6: ms, 0x080071E9: 0xD3}

    text = data.decode("ascii")
    newline = "\r\n" if "\r\n" in text else "\n"
    base = 0
    seen = {}
    out = []
    for line in text.split(newline):
        if not line.startswith(":"):
            out.append(line)
            continue
        rec = bytearray.fromhex(line[1:])
        count, addr, rtype = rec[0], (rec[1] << 8) | rec[2], rec[3]
        if rtype == 4:
            base = ((rec[4] << 8) | rec[5]) << 16
        elif rtype == 0:
            for i in range(count):
                a = base + addr + i
                if a in EXPECTED:
                    seen[a] = rec[4 + i]
                if a in changes:
                    rec[4 + i] = changes[a]
            rec[-1] = (-sum(rec[:-1])) & 0xFF
            line = ":" + rec.hex().upper()
        out.append(line)

    if seen != EXPECTED:
        sys.exit("Unexpected bytes at the patch location. Aborting.")

    open(dst, "wb").write(newline.join(out).encode("ascii"))
    print(f"Done: {dst} (debounce = {ms} ms)")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    patch(sys.argv[1], int(sys.argv[2]), sys.argv[3])
