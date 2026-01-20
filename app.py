import os
from flask import Flask, render_template, request
import urllib.parse

app = Flask(__name__)

MENUS_POR_DIA = {
    "lunes": {
        "Albondigas": 3500,
        "Milanesa": 3500,
        "Empanadas de Carne": 1200
    },
    "martes": {
        "Pastel de papas": 3500,
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
        "Parrilada con Guarnición": 3500,
        "Empanadas de Carne": 1200,
        "Empanadas de Pollo": 1200,
        "Pizza": 4000
    }
}

NUMERO_WHATSAPP = "5491135162414"

@app.route("/", methods=["GET", "POST"])
def index():
    dia_seleccionado = request.form.get("dia", "lunes")
    menu_hoy = MENUS_POR_DIA.get(dia_seleccionado, {})

    if request.method == "POST" and "confirmar" in request.form:
        direccion = request.form.get("direccion", "")
        pago = request.form.get("pago", "")
        comentario = request.form.get("comentario", "")

        pedido = []
        total = 0

        for i in range(1, 6):
            producto = request.form.get(f"producto{i}")
            cantidad = request.form.get(f"cantidad{i}")

            if producto and cantidad:
                cantidad = int(cantidad)
                precio = menu_hoy.get(producto, 0)
                subtotal = precio * cantidad
                pedido.append(f"• {producto} x {cantidad} = ${subtotal}")
                total += subtotal

        mensaje = (
            f"📅 Día: {dia_seleccionado.capitalize()}\n\n"
            + "\n".join(pedido) +
            f"\n\n💰 Total: ${total}\n"
            f"📍 Dirección: {direccion}\n"
            f"💳 Pago: {pago}\n"
            f"📝 {comentario}"
        )

        link = "https://wa.me/" + NUMERO_WHATSAPP + "?text=" + urllib.parse.quote(mensaje)
            
    
    
    
       # return f'<a href="{link}" target="_blank">Enviar por WhatsApp</a>'




        return f"""
        <html>
        <head>
            <meta http-equiv="refresh" content="0; url={link}">
        </head>
        <body style="font-family: Arial; text-align: center;">
            <h2>Redirigiendo a WhatsApp...</h2>
            <p>Si no se abre automáticamente, tocá el botón:</p>
            <a href="{link}" target="_blank"
                style="display:inline-block;
                    margin-top:15px;
                    background:#25D366;
                    color:white;
                    padding:12px 20px;
                    border-radius:8px;
                    text-decoration:none;
                    font-size:18px;">
                 👉 Enviar por WhatsApp
             </a>
         </body>
         </html>
         """


    return render_template(
        "index.html",
        menu=menu_hoy,
        dia_seleccionado=dia_seleccionado
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

