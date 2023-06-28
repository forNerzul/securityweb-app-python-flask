import io
import folium
import qrcode
from PIL import Image
from security_guard_app.config import Config

def generate_qr_img(waypoint):
    print("Generando QR...")
    print("Trabajando con el waypoint: {}, QRCode: {}".format(waypoint.name, waypoint.qr_value))
    logo_link = "security_guard_app\static\logo.jpg"
    logo = Image.open(logo_link)
    # Pasamos los parametros de tamaño y color para nuestro codigo QR

    basewidth = 100
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    # Creamos una variable para almacenar el codigo de error en caso de que al generar el QR ocurra un errors
    Qrcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    # Generamos la ruta a la que nuestro codigo QR va a redireccionar
    url = '{}/qrcode?qr_value={}'.format(Config.NGROK, waypoint.qr_value)
    Qrcode.add_data(url)
    # Generamos el codigo QR
    qrcode.make()

    # Pasamos los parametros de color y posicion de nuestro logo, tambien definimos el color que tendra nuestro QR
    qrcolor = 'Black'
    qrimg = Qrcode.make_image(fill_color=qrcolor, back_color="white").convert('RGB')
    pos = ((qrimg.size[0] - logo.size[0]) // 2, (qrimg.size[1] - logo.size[1]) // 2)
    qrimg.paste(logo, pos)
    # Obtén la ruta de la imagen utilizando url_for
    image_path = 'security_guard_app\static\qr\qr_waypoint_{}.png'.format(waypoint.qr_value)
    # Guardamos nuestro codigo QR generado como una imagen
    qrimg.save(image_path)
    # Mostramos un texto una vez que el codigo QR haya sido generado con exito
    print('Codigo QR generado con exito')

def generate_map (latitud, longitud):
    mapa_de_carga = folium.Map(location=[latitud, longitud], zoom_start=12)

    # Crear un marcador interactivo
    marcador = folium.Marker([latitud, longitud], draggable=True)

    marcador.add_to(mapa_de_carga)


    mapa_de_carga.add_child(marcador)
    #mapa_de_carga.save('security_guard_app/views\mapa.html')
    # Obtener el código HTML del mapa
    mapa_html = mapa_de_carga._repr_html_()

    return mapa_html


