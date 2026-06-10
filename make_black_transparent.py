from PIL import Image
import os

def extract_logo(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return False
        
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size
    
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            # Since background is black (0,0,0) and logo is gold, 
            # the alpha is proportional to the brightness.
            # We can use the max of R, G, B as the alpha channel.
            alpha = max(r, g, b)
            
            # Map low values (noise) to transparent
            if alpha < 5:
                pixels[x, y] = (0, 0, 0, 0)
            elif alpha >= 250:
                pixels[x, y] = (r, g, b, 255)
            else:
                # Reconstruct original colors: C_observed = Alpha * C_foreground / 255
                # So C_foreground = C_observed * 255 / Alpha
                def clean(c, a_val):
                    val = int(c * 255 / a_val)
                    return max(0, min(255, val))
                
                nr = clean(r, alpha)
                ng = clean(g, alpha)
                nb = clean(b, alpha)
                pixels[x, y] = (nr, ng, nb, alpha)
                
    img.save(output_path, "PNG")
    print(f"Saved transparent logo to {output_path}")
    return True

if __name__ == '__main__':
    brain_dir = 'C:/Users/x/.gemini/antigravity/brain/f424db20-719d-4663-8f5a-702e740443e4'
    
    wordmark_input = os.path.join(brain_dir, 'media__1781079062851.png')
    monogram_input = os.path.join(brain_dir, 'media__1781079075474.png')
    
    extract_logo(wordmark_input, 'wordmark_transparent.png')
    extract_logo(monogram_input, 'monogram_transparent.png')
    
    # Save the monogram as favicon.png
    if os.path.exists('monogram_transparent.png'):
        img = Image.open('monogram_transparent.png')
        img.thumbnail((32, 32))
        img.save('favicon.png', 'PNG')
        print("Generated favicon.png")
