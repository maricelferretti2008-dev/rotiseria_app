import os
from flask import Flask, render_template, request
import urllib.parse
from datetime import datetime


app = Flask(__name__)

# Menú de la rotisería
MENUS_POR_DIA = {
    "lunes": {
        "Albondigas": 3500,
        "Milanesa": 3500,
        "Empanadas de Carne": 1200
    },
    "martes": {
        "PAstel de papas": 3500,
        "Pizza": 4000,
        "Empanadas de Jamón y Queso": 1200
    },
    "miercoles": {
        "Filet con Puré": 3500,        
        "Canastitas Capresse": 1800,
        "Empanadas de Pollo": 1200
    },
    "jueves": {
        "Canelones": 3500,
        "Milanesa": 3500,
        "Pizza": 4000
    },
    "viernes": {
        "Parrillada": 3500,
        "Empanadas de Carne": 1200,
        "Empanadas de Pollo": 1200,
        "Pizza": 4000
    }
}

NUMERO_WHATSAPP = "5491135162414"  # tu número con código país

@app.route("/", methods=["GET", "POST"])
def index():

    # 🔹 Día seleccionado (por defecto lunes)
    dia_seleccionado = request.form.get("dia", "lunes")

    # 🔹 Menú según el día
    menu_hoy = MENUS_POR_DIA.get(dia_seleccionado, {})

    if request.method == "POST":
        direccion = request.form.get("direccion", "")
        pago = request.form.get("pago", "")
        comentario = request.form.get("comentario", "")

        pedido = []
        total = 0

        for i in range(1, 6):
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
            f"📅 Día: {dia_seleccionado.capitalize()}\n\n"
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

    

    return render_template(
       "index.html",
       menu=menu_hoy,
       dia_seleccionado=dia_seleccionado
    )

