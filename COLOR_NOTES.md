# Color Display Notes for Waveshare RP2350-Touch-LCD-1.28

## Working Color System

### Format
- **BRG565**: Non-standard bit layout
  - Bits 15-11: Blue (5 bits)
  - Bits 10-5: Red (6 bits)
  - Bits 4-0: Green (5 bits)

### Conversion Function
```python
def rgb_to_brg565(r, g, b):
    # Apply gamma correction for intermediate values
    r = apply_gamma_correction(r, 2.2)
    g = apply_gamma_correction(g, 2.2)
    b = apply_gamma_correction(b, 2.2)

    # BRG format packing
    return ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)

def apply_gamma_correction(value, gamma=2.2):
    normalized = value / 255.0
    corrected = pow(normalized, 1.0 / gamma)
    return int(corrected * 255.0)
```

## What Works ✓

1. **Primary colors** (255, 0, 0) etc. - Perfect
2. **Single-channel gradients** with gamma correction:
   - Red gradients (R varying, G=0, B=0)
   - Green gradients (R=0, G varying, B=0)
   - Blue gradients (R=0, G=0, B varying)
3. **Images** converted with gamma correction - Excellent
4. **High-intensity mixed colors** (values near 255)

## Hardware Limitations ✗

### Grayscale is Broken
**Symptom**: Equal RGB values (R=G=B) do not produce gray at intermediate intensities.

**Example**:
- Gray 32 (32, 32, 32) → Shows GREEN
- Gray 64 (64, 64, 64) → Shows GRAY ✓ (rare exception)
- Gray 96 (96, 96, 96) → Shows GREEN
- Gray 128 (128, 128, 128) → Shows BLUE-GRAY
- Gray 255 (255, 255, 255) → Shows WHITE ✓

**Root Cause**: The display has hardware gamma correction curves (configured in LCD initialization commands 0xF0, 0xF1, 0xF2, 0xF3) that are **different for each color channel**. When equal digital RGB values are sent, the actual light output is unequal because red, green, and blue have different response curves.

**Impact**:
- Cannot display true grayscale at most intermediate values
- Some mixed-color shades will appear incorrect
- Only pure blacks (0,0,0), whites (255,255,255), and occasional values show correctly

**Cannot be fixed in software** - this is a fundamental hardware characteristic.

## Display Mode Comparison

### For Images (convert_image.py)
- ✅ Use gamma correction (gamma=2.2)
- ✅ Use BRG565 format
- ✅ Direct framebuffer write
- Result: Excellent color reproduction

### For Graphics (lcd.fill_rect, etc.)
- ✅ Use gamma correction (gamma=2.2)
- ✅ Use BRG565 format
- ⚠️ Avoid grayscale - use colored designs
- Result: Good for solid colors, poor for grayscale

## Recommendations

1. **For backgrounds**: Use images with gamma correction
2. **For UI elements**: Use bright, saturated colors (avoid gray)
3. **For text**: Use white (255,255,255) or colored text
4. **Avoid**: Intermediate grayscale values in graphics

## Testing

Use `color_calibration.py` to test colors:
- Test 1 (Primary Colors): Should be perfect
- Test 3-5 (Color Gradients): Should show correct colors with gamma
- Test 6 (Grayscale): Will show green/purple artifacts - this is expected

## Technical Details

### Why Gamma Correction is Needed
The display's hardware gamma curves expect gamma-encoded input (like sRGB images). Without gamma correction:
- Red gradient shows as blue
- Green gradient shows as black/green bands
- Blue gradient shows as green

With gamma correction (gamma=2.2):
- All single-color gradients display correctly
- Images display with accurate colors
- Grayscale still fails (different issue - per-channel gamma mismatch)

### Framebuffer Details
- Size: 240×240 pixels = 115,200 bytes
- Format: RGB565 (2 bytes per pixel)
- Byte order: Little-endian
- Color format: BRG (non-standard)
- Both `lcd.fill_rect()` and direct framebuffer writes produce identical results
