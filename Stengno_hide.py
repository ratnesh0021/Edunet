from PIL import Image

def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

def hide_lsb(image_path, output_path, secret_message):
    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    encoded = image.copy()
    width, height = image.size
    binary_msg = text_to_bits(secret_message) + '1111111111111110'  # EOF delimiter
    msg_index = 0

    for y in range(height):
        for x in range(width):
            r, g, b = encoded.getpixel((x, y))
            if msg_index < len(binary_msg):
                r = (r & ~1) | int(binary_msg[msg_index])
                msg_index += 1
            if msg_index < len(binary_msg):
                g = (g & ~1) | int(binary_msg[msg_index])
                msg_index += 1
            if msg_index < len(binary_msg):
                b = (b & ~1) | int(binary_msg[msg_index])
                msg_index += 1

            encoded.putpixel((x, y), (r, g, b))

            if msg_index >= len(binary_msg):
                encoded.save(output_path)
                print(f"✅ Secret message hidden successfully in '{output_path}' using LSB.")
                return

    print("❌ Image is too small to hold the full message.")


hide_lsb("sample_images/input_image.png", "sample_images/output_stego.png", "This is a new secret message hidden using LSB technique.")
