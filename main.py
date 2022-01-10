from flask import Flask ,request, make_response, redirect, render_template, session, current_app,url_for
from Valor_IP import direc_difucion, direccion_red, subnetear, subnetear_igual,Primer_host,ultimo_host,numb_hosts,tipo_direccion,es_valida,Validar,mask_a_bits
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired


app= Flask(__name__)
bootstrap=Bootstrap(app)

app.config.update(
    DEBUG =False,
    ENV = 'development'
)

class IpForm(FlaskForm):
    ip= StringField('ip', validators=[DataRequired()] )
    mascara_red = StringField('mascara de red',validators=[DataRequired()])
    submit = SubmitField('Ver Datos')

app.config['SECRET_KEY'] = 'SUPER SECRETO'

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',error=error)



@app.route('/')
def index():
    user_ip = request.remote_addr

    respuesta=make_response(redirect('/hola'))
    session['user_ip'] = user_ip

    return respuesta


@app.route('/hola', methods=['GET', 'POST'])
def hello():
    user_ip = session.get('user_ip')
    ip_form= IpForm()
    context = {
        'ip_user' : user_ip,
        'ip_form': ip_form
    }
    if ip_form.validate_on_submit():
        results = []
        ip = ip_form.ip.data
        mascara_red = mask_a_bits(ip_form.mascara_red.data)
        ip_completo = ip_form.ip.data+' / '+mask_a_bits(ip_form.mascara_red.data)
        Direccion_red = direccion_red(ip, mascara_red)
        primer_host= Primer_host(ip, mascara_red)
        ultimo_host= ultimo_host(ip, mascara_red)
        Direccion_difucion = direc_difucion(ip, mascara_red)


    return render_template('pages/hola_mundo.html', **context )