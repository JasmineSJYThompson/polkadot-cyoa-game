import os
from asciimatics.renderers import ImageFile

input_dir = "ascii_art_images"
ascii_dir = "ascii_art"

# List image base names (no extension)
image_files = {
    os.path.splitext(f)[0]: f
    for f in os.listdir(input_dir)
    if f.lower().endswith(".jpg")
}

if not image_files:
    print("No .jpg images found in the images/ folder.")
    exit()

print("Available image scene names:\n")
for name in image_files:
    print(f"- {name}")

# Get user input
selection = input("\nEnter image base name(s) to regenerate (comma-separated): ").strip().lower()

# Split the input and filter valid names
selected_names = [name.strip() for name in selection.split(",") if name.strip() in image_files]

if not selected_names:
    print("❌ No valid names entered. Exiting.")
    exit()

# Process selected images
for name in selected_names:
    image_path = os.path.join(input_dir, image_files[name])
    output_path = os.path.join(ascii_dir, f"{name}.asc")

    try:
        img = ImageFile(image_path)
        ascii_str = str(img)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ascii_str)

        print(f"✅ Saved ASCII art: {output_path}")
    except Exception as e:
        print(f"❌ Failed to process {name}: {e}")

