import os
from flask import Flask, render_template, request
import urllib.parse
from datetime import datetime


app = Flask(__name__)

# Menú de la rotisería
MENUS_POR_DIA = {
    "lunes": {
        "Milanesa": 3500,
        "Empanadas de Carne": 1200
    },
    "martes": {
        "Pizza": 4000,
        "Empanadas de Jamón y Queso": 1200
    },
    "miercoles": {
        "Canastitas Capresse": 1800,
        "Empanadas de Pollo": 1200
    },
    "jueves": {
        "Milanesa": 3500,
        "Pizza": 4000
    },
    "viernes": {
        "Empanadas de Carne": 1200,
        "Empanadas de Pollo": 1200,
        "Pizza": 4000
    }
}

NUMERO_WHATSAPP = "5491135162414"  # tu número con código país

@app.route("/", methods=["GET", "POST"])
def index():
    dias = ["lunes", "martes", "miercoles", "jueves", "viernes"]
    hoy = dias[datetime.now().weekday()]
    menu_hoy = MENUS_POR_DIA.get(hoy, {})


    if request.method == "POST":
        direccion = request.form.get("direccion", "")
        pago = request.form.get("pago", "")
        comentario = request.form.get("comentario", "")

        pedido = []
        total = 0

        for i in range(1, 4):
            producto = request.form.get(f"producto{i}")
            cantidad = request.form.get(f"cantidad{i}")

            if producto and cantidad:
                try:
                    cantidad = int(cantidad)
                    precio = menu_hoy.get(producto, 0)
                    subtotal = precio * cantidad
                    pedido.append(f"• {producto} x {cantidad} = ${subtotal}")
                    total += subtotal
                except ValueError:
                    pass

        if not pedido:
            return "<h2>No se seleccionaron productos</h2>"

        detalle_pedido = "\n".join(pedido)

        mensaje = (
            "🍽️ *Pedido Rotisería*\n\n"
            f"{detalle_pedido}\n\n"
            f"💰 Total: ${total}\n\n"
            f"📝 Comentarios: {comentario}\n"
            f"📍 Dirección: {direccion}\n"
            f"💳 Pago: {pago}"
        )

        mensaje_codificado = urllib.parse.quote(mensaje)
        link_whatsapp = f"https://wa.me/{NUMERO_WHATSAPP}?text={mensaje_codificado}"

        return f"""
        <html>
            <body style="font-family: Arial; text-align: center;">
                <h2>✅ Pedido listo</h2>
                <p>Presioná el botón para enviarlo por WhatsApp</p>
                <a href="{link_whatsapp}" target="_blank"
                   style="font-size: 18px; text-decoration: none;
                          background: #25D366; color: white;
                          padding: 12px 20px; border-radius: 8px;">
                    👉 Enviar pedido por WhatsApp
                </a>
            </body>
        </html>
        """

    return render_template("index.html", menu=menu_hoy)
    return "<h1>ROTISERÍA ONLINE</h1><p>La app está funcionando</p>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
