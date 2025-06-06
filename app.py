from flask import Flask, request, send_file, jsonify
import qrcode
from PIL import Image
import json
import io
import os

app = Flask(__name__)

@app.route("/generate_sheet", methods=["POST"])
def generate_sheet():
    try:
        # Load JSON list from POST body
        content = request.get_json()
        data_list = content.get("data", [])

        cols, rows = 5, 10
        qr_size = 200
        page_width = cols * qr_size
        page_height = rows * qr_size
        sheet = Image.new("RGB", (page_width, page_height), "white")

        for idx, item in enumerate(data_list[:50]):  # Limit to 50 items per sheet
            qr_data = json.dumps({
                "X1": item.get("X1", ""),
                "X2": item.get("X2", ""),
                "X3": item.get("X3", ""),
                "X4": item.get("X4", []),
                "X5": item.get("X5", "")
            }, separators=(',', ':'))

            qr = qrcode.QRCode(
                version=2,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=2,
                border=1
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")
            img_qr = img_qr.resize((qr_size, qr_size))

            x = (idx % cols) * qr_size
            y = (idx // cols) * qr_size
            sheet.paste(img_qr, (x, y))

        output = io.BytesIO()
        sheet.save(output, format="PNG")
        output.seek(0)
        return send_file(output, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
