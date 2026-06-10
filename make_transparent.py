from PIL import Image
import os

def make_transparent():
    input_path = 'logo.png'
    output_path = 'logo_transparent.png'
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size
    
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            # Since gold has very low blue component (around 0-50) and white is 255, 
            # we can use the blue channel to estimate the transparency alpha.
            # We add a small offset so that pure gold details aren't made transparent.
            # B_gold is typically less than 150.
            # Let's map blue channel: 255 -> alpha 0, <= 100 -> alpha 255
            if b >= 254:
                pixels[x, y] = (0, 0, 0, 0)
            elif b <= 100:
                pixels[x, y] = (r, g, b, 255)
            else:
                # Interpolate alpha smoothly
                alpha = int(255 * (254 - b) / (254 - 100))
                alpha = max(0, min(255, alpha))
                
                # Reconstruct original colors
                def clean(c, a_val):
                    if a_val == 0: return 0
                    val = int((c * 255 - 255 * (255 - a_val)) / a_val)
                    return max(0, min(255, val))
                
                nr = clean(r, alpha)
                ng = clean(g, alpha)
                nb = clean(b, alpha)
                pixels[x, y] = (nr, ng, nb, alpha)
                
    img.save(output_path, "PNG")
    print("Logo transparency conversion complete.")

if __name__ == '__main__':
    make_transparent()
