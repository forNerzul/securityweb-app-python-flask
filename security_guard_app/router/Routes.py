from functools import wraps
from flask import render_template, request, redirect, url_for, Blueprint
from datetime import datetime
from flask_login import login_required, current_user
from security_guard_app.models import User, Waypoint, CheckIn
from security_guard_app.models.forms import LogoutForm, WaypointForm, RegisterForm, LoginForm
from security_guard_app.utils import generate_qr_img, generate_map


app_views = Blueprint('app_views', __name__,
                        template_folder='../views')

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(role):
                return redirect(url_for('app_views.unauthorized'))  # Ruta para la página de acceso no autorizado
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app_views.route('/')
@login_required
def index():
    logout_form = LogoutForm()
    return render_template('index.html', current_user=current_user)

@app_views.route('/add-waypoint', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_waypoint():
    waypoint_form = WaypointForm()
    mapa = generate_map(-25.798631587777972, -56.4351209743452)
    if waypoint_form.validate_on_submit():
        print("Estoy en el if de add_waypoint")
        print("Waypoint ingresado: Nombre={}, Latitud={}, Longitud={}".format(waypoint_form.name.data, waypoint_form.lat.data, waypoint_form.lon.data))
        waypoint = Waypoint(name=waypoint_form.name.data, lat=waypoint_form.lat.data, lon=waypoint_form.lon.data)
        
        try:
            # Guardo el objeto Waypoint en la base de datos
            waypoint.add_waypoint_to_db()
            # Genero la imagen del QR
            generate_qr_img(waypoint)
            
        except:
            print("Error al guardar el waypoint en la base de datos")
        return render_template("add_waypoint.html", qr_img = "qr_waypoint_{}.png".format(waypoint.qr_value), waypoint_form=waypoint_form)

    return render_template("add_waypoint.html", waypoint_form=waypoint_form, mapa=mapa)

@app_views.route('/admin')
@login_required
@role_required('admin')
def admin_panel():
    return render_template('/admin_panel/admin_panel.html')


@app_views.route('/unauthorized')
def unauthorized():
    return render_template('/unauthorized.html')

@app_views.route('/qrcode')
@login_required
def qr():
    # Obtengo el valor del parametro qr_value de la URL
    qr_value = request.args.get('qr_value')
    print("Iniciando la busqueda del QR: {}".format(qr_value))
    # Busco el waypoint en la base de datos
    waypoint = Waypoint.get_waypoint_by_qr_value(qr_value)
    # Si no existe el waypoint redirecciono al index
    if waypoint is None:
        return redirect(url_for('app_views.index'))
    print("Waypoint encontrado: {}".format(waypoint.name))
    # Creo el objeto Checkin
    checkin = CheckIn(user_id=current_user.id, date=datetime.now(), waypoint_id=waypoint.id)
    print("Checkin creado: {}".format(checkin))
    # Guardo el objeto Checkin en la base de datos
    checkin.add_checkin_to_db()
    print("Checkin guardado en la base de datos")
    return render_template('checkin_data.html', checkin=checkin, waypoint=waypoint)

@app_views.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        # Compruebo si el usuario ingresado por formulario existe en la base de datos
        if not User.check_if_user_exists(register_form.username.data):
            # Purete no existe en user vamo a crearlo
            user = User(username=register_form.username.data, name=register_form.name.data, password=register_form.password.data, role='admin')
            # Encripto la contraseña 
            user.hash_password()
            # Guardo el usuario en la base de datos
            user.add_user_to_db()
            return redirect(url_for('app_views.login'))
        else:
            # El usuario ya existe en la base de datos
            return redirect(url_for('app_views.login'))
    return render_template('register.html', register_form=register_form)

@app_views.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm() 
    if login_form.validate_on_submit():
        # Compruebo si el usuario ingresado por formulario existe en la base de datos
        user = User.get_user_by_username(login_form.username.data)
        # Compruebo si llego un usuario valido
        if user is None:
            # El usuario no existe en la base de datos
            return redirect(url_for('app_views.register'))
        # Compruebo si la contraseña ingresada por formulario es valida
        if user.check_password(login_form.password.data):
            # aca ya decidimos que el usuario es valido y la contraseña tambien
            # entonces lo logueamos
            user.login()
        return redirect(url_for('app_views.index'))
    return render_template('login.html', login_form=login_form)

@app_views.route('/logout')
@login_required
def logout():
    current_user.logout()
    return redirect(url_for('app_views.login'))

@app_views.route('/cam')
@login_required
def cam():
    return render_template('cam.html')

@app_views.route('/map')
def map():
    return render_template('mapa.html')


