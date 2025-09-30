from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io

app = Flask(__name__)

def generate_logo(text="JARVIS", size=400, color=(0, 255, 255)):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", int(size/6))
    except:
        font = ImageFont.load_default()

    text_w, text_h = draw.textsize(text, font=font)
    pos = ((size - text_w) // 2, (size - text_h) // 2)

    # Glow effect
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((20, 20, size-20, size-20), fill=color+(120,))
    glow = glow.filter(ImageFilter.GaussianBlur(15))
    img = Image.alpha_composite(img, glow)

    # Circular ring
    draw.ellipse((40, 40, size-40, size-40), outline=color, width=6)

    # Text
    draw.text(pos, text, font=font, fill=color)

    return img

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text", "JARVIS")
        color_hex = request.form.get("color", "00ffff")
        color = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))

        img = generate_logo(text.upper(), color=color)
        img_io = io.BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)
        return send_file(img_io, mimetype="image/png")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
