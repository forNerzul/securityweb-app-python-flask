from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username | Nombre de usuario:', validators=[DataRequired(), Length(4, 10)])
    password = PasswordField('Password | Contraseña:', validators=[DataRequired(), Length(4, 15)])
    submit = SubmitField('Submit | Ingresar')

class RegisterForm(FlaskForm):
    username = StringField('Username | Nombre de usuario:', validators=[DataRequired(), Length(4, 10)])
    name = StringField('Name |  Nombre: ', validators=[DataRequired(), Length(10, 100)])
    password = PasswordField('Password | Contraseña:', validators=[DataRequired(), Length(4, 15)])
    submit = SubmitField('Submit | Ingresar')

class LogoutForm(FlaskForm):
    submit = SubmitField('Log Out | Salir')

class WaypointForm(FlaskForm):
    name = StringField('Nombre del Waypoint', validators=[DataRequired(), Length(4, 20)])
    # crea latitud hidden id = lat
    lat = HiddenField('Latitud', validators=[DataRequired()], render_kw={'id': 'lat'}, default=-25.798631587777972)
    lon = HiddenField('Longitud', validators=[DataRequired()], render_kw={'id': 'lon'}, default=-56.4351209743452)
    
    submit = SubmitField('Crear Waypoint')