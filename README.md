# RK R75 Pro – double typing fix (debounce patch)

**[English](#english) · [Español](#español)**

---

## English

### The problem

On some **Royal Kludge R75 Pro** (tri-mode, ANSI, **VID 342D / PID E487**) keyboards, keys get typed twice: mostly the space bar, but also random letters. It happens with the USB cable, 2.4G and Bluetooth, on any computer or phone, and changing the switch does not fix it.

### The cause

The official firmware **v11** (`RK R75Pro(852) Tri-mode_via_PIDE487_v11_ANSI layout.hex`, built 2024-05-23, the one RK support sends) is QMK on ChibiOS and uses the `sym_defer_g` debounce algorithm with **DEBOUNCE = 1 ms**. QMK's default is 5 ms. With 1 ms, any small switch bounce is registered as a second key press.

### The fix

These files are the **same official v11 firmware with only 2 bytes changed**: the debounce comparison in `debounce()` (address `0x080071E6`), from `cmp r0, #0 / beq` (≥ 1 ms) to `cmp r0, #N / blo` (≥ N ms). Nothing else is modified.

| File | Debounce | SHA-256 |
|---|---|---|
| `firmware/R75Pro_v11_debounce_5ms.hex` | **5 ms** (try this first) | `b1ce811594ebe65dabfb0a06257ae2364f3ae38c3d9e0d4d34091c8f24787422` |
| `firmware/R75Pro_v11_debounce_10ms.hex` | 10 ms (if 5 ms is not enough) | `072412cad15f5e28cfa80b4aebefb5630f882f29cf966f28b25765d288147014` |
| `firmware/R75Pro_v11_original_1ms.hex` | 1 ms (official, to go back) | `f3ec95ba5265b8d55657c392d410514f16094550dacc82ca5ab033498d660f91` |

Tested on my own R75 Pro: with 5 ms the double typing is gone.

**Input lag:** 5 ms adds 4 ms compared to the original (less than one frame at 240 Hz). 10 ms adds 9 ms.

You can also generate them yourself from the official file with `patch_debounce.py` (it checks the SHA-256 of the input and the exact bytes before patching):

```
python patch_debounce.py R75Pro_v11_original_1ms.hex 5 R75Pro_v11_debounce_5ms.hex
```

### How to flash

1. Download [QMK Toolbox](https://qmk.fm/toolbox) and run it **as administrator** (accept the driver installation).
2. Set the keyboard to **wired mode** and connect it with the USB cable.
3. In QMK Toolbox click **Open** and select `R75Pro_v11_debounce_5ms.hex`. Ignore the "MCU (AVR only)" dropdown.
4. Enter DFU mode: press **Fn + Right Shift + Esc** (or hold the small button under the space bar while plugging the cable). A yellow line *"WB32 DFU device connected"* appears.
5. Click **Flash** and wait for **"Flash complete"**. Do not unplug it.
6. Click **Exit DFU**.
7. **Important:** do a factory reset (**Fn + Space for 3 seconds**) and then **turn the keyboard off and on with the power switch**. Without this step the battery reading and keys can behave strangely.

**Recovery:** the WB32 DFU bootloader is in ROM and is not overwritten. If anything goes wrong, enter DFU mode again and flash `R75Pro_v11_original_1ms.hex`.

### Only for this model

Only for the **R75 Pro tri-mode ANSI, PID E487**. Do **not** flash it on the wired R75 (PID E484/E483) or any other model.

### Disclaimer

Not affiliated with Royal Kludge. The firmware belongs to Royal Kludge; the original v11 file is the one their support distributes (also in their public Google Drive). Use at your own risk.

---

## Español

### El problema

En algunos **Royal Kludge R75 Pro** (tri-mode, ANSI, **VID 342D / PID E487**) las teclas se escriben dos veces: sobre todo la barra espaciadora, pero también letras al azar. Pasa por cable USB, 2.4G y Bluetooth, en cualquier computadora o celular, y cambiar el switch no lo arregla.

### La causa

El firmware oficial **v11** (`RK R75Pro(852) Tri-mode_via_PIDE487_v11_ANSI layout.hex`, compilado el 2024-05-23, el que manda el soporte de RK) es QMK sobre ChibiOS y usa el anti-rebote `sym_defer_g` con **DEBOUNCE = 1 ms**. El valor por defecto de QMK es 5 ms. Con 1 ms, cualquier rebote mínimo del switch se cuenta como una segunda pulsación.

### La solución

Estos archivos son **el mismo firmware oficial v11 con solo 2 bytes cambiados**: la comparación del anti-rebote en `debounce()` (dirección `0x080071E6`), de `cmp r0, #0 / beq` (≥ 1 ms) a `cmp r0, #N / blo` (≥ N ms). No se modificó nada más.

| Archivo | Anti-rebote | SHA-256 |
|---|---|---|
| `firmware/R75Pro_v11_debounce_5ms.hex` | **5 ms** (probá este primero) | `b1ce811594ebe65dabfb0a06257ae2364f3ae38c3d9e0d4d34091c8f24787422` |
| `firmware/R75Pro_v11_debounce_10ms.hex` | 10 ms (si 5 ms no alcanza) | `072412cad15f5e28cfa80b4aebefb5630f882f29cf966f28b25765d288147014` |
| `firmware/R75Pro_v11_original_1ms.hex` | 1 ms (el oficial, para volver atrás) | `f3ec95ba5265b8d55657c392d410514f16094550dacc82ca5ab033498d660f91` |

Probado en mi propio R75 Pro: con 5 ms desaparecieron las teclas dobles.

**Retraso:** 5 ms suma 4 ms respecto del original (menos de un cuadro a 240 Hz). 10 ms suma 9 ms.

También podés generarlos vos a partir del archivo oficial con `patch_debounce.py` (antes de modificar nada, verifica el SHA-256 del archivo y los bytes exactos):

```
python patch_debounce.py R75Pro_v11_original_1ms.hex 5 R75Pro_v11_debounce_5ms.hex
```

### Cómo flashearlo

1. Bajá [QMK Toolbox](https://qmk.fm/toolbox) y abrilo **como administrador** (aceptá la instalación de drivers).
2. Poné el teclado en **modo cable** y conectalo con el cable USB.
3. En QMK Toolbox tocá **Open** y elegí `R75Pro_v11_debounce_5ms.hex`. Ignorá el desplegable "MCU (AVR only)".
4. Entrá en modo DFU: apretá **Fn + Shift derecho + Esc** (o mantené apretado el botoncito de debajo de la barra espaciadora mientras enchufás el cable). Aparece una línea amarilla *"WB32 DFU device connected"*.
5. Tocá **Flash** y esperá **"Flash complete"**. No lo desenchufes.
6. Tocá **Exit DFU**.
7. **Importante:** hacé un reset de fábrica (**Fn + Espacio 3 segundos**) y después **apagá y prendé el teclado con la llave**. Sin este paso, la batería y las teclas pueden andar raro.

**Si algo sale mal:** el bootloader DFU del chip WB32 está en ROM y no se borra. Volvé a entrar en modo DFU y flasheá `R75Pro_v11_original_1ms.hex`.

### Solo para este modelo

Solo para el **R75 Pro tri-mode ANSI, PID E487**. **No** lo flashees en el R75 con cable (PID E484/E483) ni en ningún otro modelo.

### Aviso

No tengo relación con Royal Kludge. El firmware es de Royal Kludge; el archivo original v11 es el que distribuye su soporte (también está en su Google Drive público). Usalo bajo tu propio riesgo.
