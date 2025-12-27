from PIL import Image


def images_to_pdf(images, output_pdf_path):
    if not images:
        return

    try:
        pil_images = [Image.open(img).convert("RGB") for img in images]
        pil_images[0].save(
            output_pdf_path,
            save_all=True,
            append_images=pil_images[1:],
        )
        print(f"📄 PDF created: {output_pdf_path}")
    except Exception as error:
        print("❌ PDF creation error:", error)
