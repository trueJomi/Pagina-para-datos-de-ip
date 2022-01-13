from flask import Flask ,request, make_response, redirect, render_template, session, current_app,url_for, flash
from Valor_IP import direc_difucion, direccion_red, subnetear_hosts, subnetear_igual,Primer_host,ultimo_host,numb_hosts,tipo_direccion,es_valida,Validar,mask_a_bits
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, IPAddress, NumberRange


app= Flask(__name__)
bootstrap=Bootstrap(app)

app.config.update(
    DEBUG = True,
    ENV = 'development'
)



class IpForm(FlaskForm):
    ip= StringField('Ip',validators=[DataRequired(), IPAddress()])
    mascara_red = StringField('Mascara de red',validators=[DataRequired()])
    submit = SubmitField('Ver Datos')



class IpSub(FlaskForm):
    ip= StringField('Ip', validators=[DataRequired(), IPAddress()] )
    mascara_red = StringField('Mascara de Red',validators=[DataRequired()])
    cantidad= IntegerField('Cantidad de Subredes',validators=[NumberRange(min=1),DataRequired()] ,default=1) 
    hosts= IntegerField('Numero de Hosts',validators=[NumberRange(min=0)],default=0,description='si pones 0 los hosts se distribuiran de manera equitativa')
    submit = SubmitField('Subnetear')


app.config['SECRET_KEY'] = 'SUPER SECRETO'





@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',error=error)



@app.route('/')
def index():
    user_ip = request.remote_addr

    respuesta=make_response(redirect('/ip'))
    session['user_ip'] = user_ip

    return respuesta


@app.route('/ip', methods=['GET', 'POST'])
def ip():

    user_ip = session.get('user_ip')
    ip_form= IpForm()

    ip_completo = session.get('ip completo')
    Direccion_red = session.get('Direccion red')
    primer_host= session.get('primer host')
    final_host=session.get('final host')
    Direccion_difucion = session.get('Direccion difucion')
    tipo=session.get('tipo')
    valido=session.get('valido')
    cantidad_hosts=session.get('cantidad hosts')

    results = {
        'IP':ip_completo,    
        'Direccion de Red':Direccion_red,
        'Primer Host':primer_host,
        'Ultimo Host':final_host,
        'Dirección de Difución':Direccion_difucion,
        'Tipo':tipo,
        'Valido':valido,
        'Cantidad de Hosts':cantidad_hosts,
    }
    context = {
        'ip_user' : user_ip,
        'ip_form' : ip_form,
        'results' : results,
    }
    session.pop('ip completo', None)
    session.pop('Direccion red', None)
    session.pop('primer host', None)
    session.pop('final host', None)
    session.pop('Direccion difucion', None)
    session.pop('tipo', None)
    session.pop('valido', None)
    session.pop('cantidad hosts', None)

    if ip_form.validate_on_submit():

        ip = ip_form.ip.data
        mascara_red = mask_a_bits(ip_form.mascara_red.data)

        ip_completo = ip+' /{}'.format(mascara_red)
        Direccion_red = direccion_red(ip, mascara_red)
        primer_host= Primer_host(ip, mascara_red)
        final_host= ultimo_host(ip, mascara_red)
        Direccion_difucion = direc_difucion(ip, mascara_red)
        tipo= tipo_direccion(ip, mascara_red)
        valido=es_valida(ip, mascara_red)
        cantidad_hosts= numb_hosts(mascara_red)


        session['ip completo'] = ip_completo
        session['Direccion red'] = Direccion_red
        session['primer host'] = primer_host
        session['final host'] = final_host
        session['Direccion difucion'] = Direccion_difucion
        session['tipo'] = tipo
        session['valido'] = valido
        session['cantidad hosts'] = cantidad_hosts

        # flash('ip resuelta: {}'.format(ip_completo))

        return redirect(url_for('ip'))
        

    return render_template('pages/ip.html', **context )


@app.route('/sebnetear', methods=['GET', 'POST'])
def subnetear():
    subnet_form=IpSub()
    ip = session.get('ip')
    mascara_red=session.get('mask')
    cantidad = session.get('cantidad')
    hosts = session.get('hosts')
    results=[]
    if ip and mascara_red:
        if hosts==0:
            subneteado = subnetear_igual(ip, mascara_red, cantidad)
        else:
            subneteado = subnetear_hosts(ip, mascara_red, hosts)
        for i in range(cantidad):
            subred = next(subneteado)
            ip_actual = subred[0]
            mask_actual = subred[1]
            subnet= {
                'Direccion de Red':direccion_red(ip_actual, mask_actual),
                'Primer Host': Primer_host(ip_actual, mask_actual),
                'Ultimo Host': ultimo_host(ip_actual, mask_actual),
                'Direccion de Difucion': direc_difucion(ip_actual, mask_actual),
                'Hosts Disponibles': numb_hosts(mask_actual),
                'Sigueinte Red': subred[2]
            }
            results.append(subnet)    
        

    context = {
        'subnet_form':subnet_form,
        'results':  results
    }

    if subnet_form.validate_on_submit():

        ip = subnet_form.ip.data
        mascara_red = mask_a_bits(subnet_form.mascara_red.data)
        cantidad = subnet_form.cantidad.data
        hosts= subnet_form.hosts.data

        session['ip'] = ip
        session['mask'] = mascara_red
        session['cantidad'] = cantidad
        session['hosts'] = hosts
        
        return redirect(url_for('subnetear'))

    return render_template('pages/subneteo.html', **context )


if __name__ == "__main__":
  app.run(debug=True)