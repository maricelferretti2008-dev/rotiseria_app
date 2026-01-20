import os
from flask import Flask, render_template, request
import urllib.parse

app = Flask(__name__)

MENUS_POR_DIA = {
    "lunes": {
        "Albondigas con puré": 9000,
        "Albondigas con arroz": 9000,
        "Arroz con pollo": 9000,
        "Pollo al horno con papas": 9000,
        "Carne al horno con papas": 9000,
        "Empanadas Carne x unidad":1800,
        "Empanadas Jamón y queso x unidad":1800,
        "Empanadas Pollo x unidad":1800,
        "Ensalada Mixta chica - porción":4000,
        "Milanesa con Fritas": 8000,
        "Milanesa Napolitana con Fritas":8500,
        "Papas fritas - porción": 4000,
        "Pizza de Muzzarella -Grande (8 porciones)":14000,
        "Sand. Bondiola con J/Q/L/T/H":7500,
        "Sand. Hamburguesa con J/Q/L/T/H":6000,
        "Sand. Lomito  con Lech y tom":7000,
        "Sand. Lomito con J/Q/L/T/H":7500,
        "Sand. Milanesa con J/Q/L/T/H":7000,
        "Sand. Milanesa con Lech y tom":6500,
        "Sand. Suprema  con Lech y tom":7000,
        "Sand. Suprema con J/Q/L/T/H":7500,
        "Suprema con Fritas": 8500,
        "Suprema Napolitana con Fritas":9000,
        "Tarta Berenjena - porción":2500,
        "Tarta Gallega - porción":2500,
        "Tarta Jamón y queso - porción":2500,
        "Tarta Verdura - porción":2500,
        "Tarta Zapallitos - porción":2500

    },
    "martes": {
        "Pastel de papas": 3500,
        "Pollo al horno con papas": 9000,
        "Carne al horno con papas": 9000,
        "Empanadas Carne x unidad":1800,
        "Empanadas Jamón y queso x unidad":1800,
        "Empanadas Pollo x unidad":1800,
        "Ensalada Mixta chica - porción":4000,
        "Milanesa con Fritas": 8000,
        "Milanesa Napolitana con Fritas":8500,
        "Papas fritas - porción": 4000,
        "Pizza de Muzzarella -Grande (8 porciones)":14000,
        "Sand. Bondiola con J/Q/L/T/H":7500,
        "Sand. Hamburguesa con J/Q/L/T/H":6000,
        "Sand. Lomito  con Lech y tom":7000,
        "Sand. Lomito con J/Q/L/T/H":7500,
        "Sand. Milanesa con J/Q/L/T/H":7000,
        "Sand. Milanesa con Lech y tom":6500,
        "Sand. Suprema  con Lech y tom":7000,
        "Sand. Suprema con J/Q/L/T/H":7500,
        "Suprema con Fritas": 8500,
        "Suprema Napolitana con Fritas":9000,
        "Tarta Berenjena - porción":2500,
        "Tarta Gallega - porción":2500,
        "Tarta Jamón y queso - porción":2500,
        "Tarta Verdura - porción":2500,
        "Tarta Zapallitos - porción":2500
    },
    "miercoles": {
        "Filet con Puré": 3500,
        "Pollo al horno con papas": 9000,
        "Carne al horno con papas": 9000,
        "Empanadas Carne x unidad":1800,
        "Empanadas Jamón y queso x unidad":1800,
        "Empanadas Pollo x unidad":1800,
        "Ensalada Mixta chica - porción":4000,
        "Milanesa con Fritas": 8000,
        "Milanesa Napolitana con Fritas":8500,
        "Papas fritas - porción": 4000,
        "Pizza de Muzzarella -Grande (8 porciones)":14000,
        "Sand. Bondiola con J/Q/L/T/H":7500,
        "Sand. Hamburguesa con J/Q/L/T/H":6000,
        "Sand. Lomito  con Lech y tom":7000,
        "Sand. Lomito con J/Q/L/T/H":7500,
        "Sand. Milanesa con J/Q/L/T/H":7000,
        "Sand. Milanesa con Lech y tom":6500,
        "Sand. Suprema  con Lech y tom":7000,
        "Sand. Suprema con J/Q/L/T/H":7500,
        "Suprema con Fritas": 8500,
        "Suprema Napolitana con Fritas":9000,
        "Tarta Berenjena - porción":2500,
        "Tarta Gallega - porción":2500,
        "Tarta Jamón y queso - porción":2500,
        "Tarta Verdura - porción":2500,
        "Tarta Zapallitos - porción":2500
    },
    "jueves": {
        "Canelones": 3500,
        "Pollo al horno con papas": 9000,
        "Carne al horno con papas": 9000,
        "Empanadas Carne x unidad":1800,
        "Empanadas Jamón y queso x unidad":1800,
        "Empanadas Pollo x unidad":1800,
        "Ensalada Mixta chica - porción":4000,
        "Milanesa con Fritas": 8000,
        "Milanesa Napolitana con Fritas":8500,
        "Papas fritas - porción": 4000,
        "Pizza de Muzzarella -Grande (8 porciones)":14000,
        "Sand. Bondiola con J/Q/L/T/H":7500,
        "Sand. Hamburguesa con J/Q/L/T/H":6000,
        "Sand. Lomito  con Lech y tom":7000,
        "Sand. Lomito con J/Q/L/T/H":7500,
        "Sand. Milanesa con J/Q/L/T/H":7000,
        "Sand. Milanesa con Lech y tom":6500,
        "Sand. Suprema  con Lech y tom":7000,
        "Sand. Suprema con J/Q/L/T/H":7500,
        "Suprema con Fritas": 8500,
        "Suprema Napolitana con Fritas":9000,
        "Tarta Berenjena - porción":2500,
        "Tarta Gallega - porción":2500,
        "Tarta Jamón y queso - porción":2500,
        "Tarta Verdura - porción":2500,
        "Tarta Zapallitos - porción":2500
    },
    "viernes": {
        "Parrilada con Guarnición": 3500,
        "Pollo al horno con papas": 9000,
        "Carne al horno con papas": 9000,
        "Empanadas Carne x unidad":1800,
        "Empanadas Jamón y queso x unidad":1800,
        "Empanadas Pollo x unidad":1800,
        "Ensalada Mixta chica - porción":4000,
        "Milanesa con Fritas": 8000,
        "Milanesa Napolitana con Fritas":8500,
        "Papas fritas - porción": 4000,
        "Pizza de Muzzarella -Grande (8 porciones)":14000,
        "Sand. Bondiola con J/Q/L/T/H":7500,
        "Sand. Hamburguesa con J/Q/L/T/H":6000,
        "Sand. Lomito  con Lech y tom":7000,
        "Sand. Lomito con J/Q/L/T/H":7500,
        "Sand. Milanesa con J/Q/L/T/H":7000,
        "Sand. Milanesa con Lech y tom":6500,
        "Sand. Suprema  con Lech y tom":7000,
        "Sand. Suprema con J/Q/L/T/H":7500,
        "Suprema con Fritas": 8500,
        "Suprema Napolitana con Fritas":9000,
        "Tarta Berenjena - porción":2500,
        "Tarta Gallega - porción":2500,
        "Tarta Jamón y queso - porción":2500,
        "Tarta Verdura - porción":2500,
        "Tarta Zapallitos - porción":2500
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

