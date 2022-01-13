LIMITE=[256,256,256,256]
ULTIMO=[255,255,255,255]
MULTICAST=[[224],[240]]
RESERVADO=[[240],[256]]
LOOPBACK=[[127],[128]]
RED_ACTUAL=[0,0,0,0]
PRIVATE=[
    [[10],[11]],
    [[172,16],[173,32]],
    [[192,168],[193,169]],
    [[169,254],[170,255]]
]

def Validar_ip(ip):
    validar=Lista_decimal(separar_punteado(ip))
    if len(validar)==4:
        for i in range(4):
            if LIMITE[i]<=validar[i]:
                return False
        return True
    else:
        return False


def separar_punteado(Ip_separar):
    partes_ip=Ip_separar.split(".")
    numero_bin=[]
    for octeto in partes_ip:
        if Validar_int(octeto):
            octeto=int(octeto)
            numero_sin=de_decimal_a_bin(octeto)
            numero=adaptar_octeto(numero_sin)
            numero_bin.append(numero)
        else:
            return []
    return numero_bin


def de_decimal_a_bin(decimal):
    numero=''
    while decimal>=1:
        numero=numero+str(decimal% 2)
        decimal=decimal//2
    numero=numero[::-1]
    return numero


def adaptar_octeto(binary):
    if 8==len(binary):
        return binary
    else:
        for i in range(8-len(binary)):
            binary='0'+binary
        return  binary


def Validar_int(valor):
    try:
        preuba=int(valor)
        return True
    except:
        return False


def octeto_accion(mask):
    if Validar_int(mask)==True:
        mask=int(mask)
        octeto=mask//8
        return octeto
    else:
        numb_ip=separar_punteado(mask)
        octeto=0
        for i in numb_ip:
            if i=='11111111':
                octeto=octeto+1
        return octeto


def valores_red(mask):
    if Validar_int(mask)==True:
        mask=int(mask)
        valor=mask%8
        return valor
    else:
        numb_ip=separar_punteado(mask)
        octeto=numb_ip[octeto_accion(mask)]
        valores=0
        for i in octeto:
            if i=='1':
                valores=valores+1
        return valores


def Mascara_ip(mask):
    if Validar_int(mask)==True:
        mask=int(mask)
        if mask>32:
            return []
        else:
            Mascara=['00000000','00000000','00000000','00000000']
            for i in range(mask//8):
                Mascara[i]='11111111'
            octeto=''
            for i in range(8):
                if i<(mask%8):
                    octeto=octeto+'1'
                else:
                    octeto=octeto+'0'
            Mascara[mask//8]=octeto
            return Mascara
    else:
        Mascara=separar_punteado(mask)
        return Mascara


def Mostrar_en_formato(binario):
    formato=''
    n_octeto=0
    for i in binario:
        n_octeto=n_octeto+1
        if n_octeto==1:
            formato=formato+str(i)
        else:
            formato=formato+'.'+str(i)
    return formato


def Lista_decimal(binario):
    lista=[]
    for i in binario:
        lista.append(de_bin_a_decimal(i)) 
    return lista


def de_bin_a_decimal(binary):
    binary=binary[::-1]
    numero=0
    cont=0
    for i in binary:
        i=int(i)
        numero=numero+(i*(2**cont))
        cont=cont+1
    return numero


def and_bin(ip1, ip2):
    if len(ip1)==len(ip2):
        resultado=[]
        for i in range(4):
            Octeto=''
            # print("comapre1 "+ip1[i])
            # print("comapre2 "+ip2[i])
            for f in range(8):
                valor1=ip1[i][f]
                valor2=ip2[i][f]
                if valor1=='1' and valor2=='1':
                    Octeto=Octeto+'1'
                else:
                    Octeto=Octeto+'0'
            # print("result: "+Octeto)
            resultado.append(Octeto)
        return resultado
    else:
        print("no poder son de dinstitos bits")


def punteado_a_bin(punteado):
    list_bin=separar_punteado(punteado)
    binary=Mostrar_en_formato(list_bin)
    return binary


def siguiente(ip):
    if Validar_ip(ip):
        ip_bin=Lista_decimal(separar_punteado(ip))
        ip_bin_inv=ip_bin[::-1]
        for i in range(4):
            if ip_bin_inv[i]==255:
                ip_bin_inv[i]=0
            else:
                ip_bin_inv[i]=ip_bin_inv[i]+1
                siguiente=ip_bin_inv[::-1]
                return siguiente
    else:
        return 'no valido'

def anterior(ip):
    if Validar_ip(ip):
        ip_bin=Lista_decimal(separar_punteado(ip))
        ip_bin_inv=ip_bin[::-1]
        for i in range(4):
            if ip_bin_inv[i]==0:
                ip_bin_inv[i]=255
            else:
                ip_bin_inv[i]=ip_bin_inv[i]-1
                siguiente=ip_bin_inv[::-1]
                return siguiente
    else:
        return 'no valido'





def direccion_red(ip, mascara_red):
    ip_bin=separar_punteado(ip)
    mascara_bin=Mascara_ip(mascara_red)
    direccion=and_bin(ip_bin, mascara_bin)
    direccion_red=Mostrar_en_formato(Lista_decimal(direccion))
    return direccion_red

def Primer_host(ip, mascara_red):
    
    direccion=direccion_red(ip, mascara_red)
    direccion_red_list=Lista_decimal(separar_punteado(direccion))
    primer_host=siguiente(Mostrar_en_formato(direccion_red_list))
    primer_host=Mostrar_en_formato(primer_host)
    if primer_host == direc_difucion(ip, mascara_red):
        return 'no hay primer host'
    else:
        return primer_host


def direc_difucion(ip, mascara_red):
    direccion=direccion_red(ip, mascara_red)
    direccion_red_list=separar_punteado(direccion)
    direccion_difucion_bin=['11111111','11111111','11111111','11111111']
    for i in range(octeto_accion(mascara_red)):
        direccion_difucion_bin[i]=direccion_red_list[i]
    octeto=''
    for i in range(8):
        if i<(valores_red(mascara_red)):
            octeto=octeto+direccion_red_list[octeto_accion(mascara_red)][i]
        else:
            octeto=octeto+'1'
    direccion_difucion_bin[octeto_accion(mascara_red)]=octeto
    direccion_difucion=Mostrar_en_formato(Lista_decimal(direccion_difucion_bin))
    return direccion_difucion


def ultimo_host(ip, mascara_red):
    direccion=direc_difucion(ip, mascara_red)
    direccion_difucion_list=Lista_decimal(separar_punteado(direccion))
    ultimo_host=anterior(Mostrar_en_formato(direccion_difucion_list))
    ultimo_host=Mostrar_en_formato(ultimo_host)
    if ultimo_host == direccion_red(ip, mascara_red):
        return 'no hay ultimo host'
    else:
        return ultimo_host


def LooopBack(ip):
    ip_comparado=Lista_decimal(separar_punteado(ip))
    limite_inferior=LOOPBACK[0]
    limite_superior=LOOPBACK[1]
    count=0
    for i in range(len(limite_inferior)):
        if limite_inferior[i]<=ip_comparado[i] and ip_comparado[i]<limite_superior[i]:
            count=count+1
    if count==len(limite_inferior):
        return True
    else:
        return False


def multicast(ip):
    ip_comparado=Lista_decimal(separar_punteado(ip))
    limite_inferior=MULTICAST[0]
    limite_superior=MULTICAST[1]
    count=0
    for i in range(len(limite_inferior)):
        if limite_inferior[i]<=ip_comparado[i] and ip_comparado[i]<limite_superior[i]:
            count=count+1
    if count==len(limite_inferior):
        return True
    else:
        return False


def reservado(ip):
    ip_comparado=Lista_decimal(separar_punteado(ip))
    if dest_multi_difucion(ip):
        return False
    else:
        limite_inferior=RESERVADO[0]
        limite_superior=RESERVADO[1]
        count=0
        for i in range(len(limite_inferior)):
            if limite_inferior[i]<=ip_comparado[i] and ip_comparado[i]<limite_superior[i]:
                count=count+1
        if count==len(limite_inferior):
            return True
        else:
            return False


def dest_multi_difucion(ip):
    ip_comparado=Lista_decimal(separar_punteado(ip))
    if ip_comparado==ULTIMO:
        return True
    else:
        return False


def tipo_direccion(ip,mascara_red):
    if LooopBack(ip):
        return 'Loopback'
    elif multicast(ip):
        return 'Direccion de Multicast'
    elif reservado(ip):
        return 'Direccion de Reservada'
    elif dest_multi_difucion(ip):
        return 'Direccion de destino de multidifucion'
    elif ip==direccion_red(ip, mascara_red):
        return 'Direccion de Red'
    elif ip==direc_difucion(ip, mascara_red):
        return 'Direccion de Difucion'
    else:
        return 'Direccion de Host '+publica_o_privada(ip)

def publica_o_privada(ip):
    ip_comparado=Lista_decimal(separar_punteado(ip))
    for intervalo in PRIVATE:
        count=0
        limite_inferior=intervalo[0]
        limite_superior=intervalo[1]
        for i in range(len(limite_inferior)):
            if limite_inferior[i]<=ip_comparado[i] and ip_comparado[i]<limite_superior[i]:
                    count=count+1
        if count==len(limite_inferior):
            return 'Privada'
    return 'Publica'


def es_valida(ip, mascara_red):
    if LooopBack(ip)==ip or multicast(ip)==ip or reservado(ip)==ip or direccion_red(ip, mascara_red)==ip or dest_multi_difucion(ip)==ip or direc_difucion(ip, mascara_red)==ip:
        return False
    else:
        return True

def mask_a_bits(mascara_red):
    mask=Mascara_ip(mascara_red)
    contador=0
    for octeto in mask:
        for bit in octeto:
            if bit=='1':
                contador=contador+1
    return contador


def numb_hosts(mascara_red):
    mask=Mascara_ip(mascara_red)
    exponent=0
    for i in mask:
        for f in i:
            if f=='0':
                exponent=exponent+1
    cont_host=(2**exponent)-2
    return cont_host

def subnetear_hosts(ip,mascara_red,hosts):
    while(True):
        results=[]
        mask_temp=mascara_red
        while numb_hosts(mask_temp)>=hosts:  
            mascara_red=mask_temp
            mask_temp=mask_a_bits(mask_temp)+1
        direccion=direc_difucion(ip, mascara_red)
        next_ip=Mostrar_en_formato(siguiente(direccion))
        results.append(ip)
        results.append(mascara_red)
        results.append(next_ip)
        # print(results)
        yield results
        ip=next_ip

def subnetear_igual(ip, mascara_red, cantidad):
    confirm=False
    add_bits=0
    for i in range(33-mask_a_bits(mascara_red)):
            if 2**(i)>=cantidad:
                add_bits=i
                confirm=True
            if confirm==True:
                break
    mascara_red=mask_a_bits(mascara_red)+add_bits
    while(True):
        results=[]
        direccion=direc_difucion(ip, mascara_red)
        next_ip=Mostrar_en_formato(siguiente(direccion))
        results.append(ip)
        results.append(mascara_red)
        results.append(next_ip)
        yield results
        ip=next_ip


def Validar(ip,mascara_red):
    if Validar_ip(ip) and Mascara_ip(mascara_red)!=[]:
        return True
    else:
        return False





def Mostrar_Todo_bin(ip,mascara_red):
    if Validar_ip(ip) and Mascara_ip(mascara_red)!=[]:
        print(' SOBRE ESTA IP '.center(90, "~")+'\n')
        print('IP:                      {}     {}'.format(Mostrar_en_formato(Lista_decimal(separar_punteado(ip))),Mostrar_en_formato(separar_punteado(ip))))
        print('MASCARA_SUBRED:          {}     {}'.format(Mostrar_en_formato(Lista_decimal(Mascara_ip(mascara_red))),Mostrar_en_formato(Mascara_ip(mascara_red))))
        print('DIRECCION DE RED:        {}     {}'.format(direccion_red(ip, mascara_red),punteado_a_bin(direccion_red(ip, mascara_red))))
        print('PRIMER HOST:             {}     {}'.format(Primer_host(ip, mascara_red),punteado_a_bin(Primer_host(ip, mascara_red))))
        print('ULTIMO HOST:             {}     {}'.format(ultimo_host(ip, mascara_red),punteado_a_bin(ultimo_host(ip, mascara_red))))
        print('DIRECCION DE DIFUSION:   {}     {}'.format(direc_difucion(ip, mascara_red),punteado_a_bin(direc_difucion(ip, mascara_red))))
        print('TIPO:                    {}'.format(tipo_direccion(ip, mascara_red)))
        print('VALIDA:                  {}'.format(es_valida(ip, mascara_red)))
        print('CANTIDAD DE HOSTS:       {}'.format(numb_hosts(mascara_red)))
    else:
        print("IP fuera de los 32 bits")


def Mostrar_Todo(ip,mascara_red):
    if Validar_ip(ip) and Mascara_ip(mascara_red)!=[]:
        print(' SOBRE ESTA IP '.center(53, '~')+'\n')
        print('IP:                      {}'.format(Mostrar_en_formato(Lista_decimal(separar_punteado(ip)))))
        print('MASCARA_SUBRED:          {}'.format(Mostrar_en_formato(Lista_decimal(Mascara_ip(mascara_red)))))
        print('DIRECCION DE RED:        {}'.format(direccion_red(ip, mascara_red)))
        print('PRIMER HOST:             {}'.format(Primer_host(ip, mascara_red)))
        print('ULTIMO HOST:             {}'.format(ultimo_host(ip, mascara_red)))
        print('DIRECCION DE DIFUSION:   {}'.format(direc_difucion(ip, mascara_red)))
        print('TIPO:                    {}'.format(tipo_direccion(ip, mascara_red)))
        print('VALIDA:                  {}'.format(es_valida(ip, mascara_red)))
        print('CANTIDAD DE HOSTS:       {}'.format(numb_hosts(mascara_red)))
    else:
        print("IP fuera de los 32 bits")


def Basic(ip,mascara_red):
    if Validar_ip(ip) and Mascara_ip(mascara_red)!=[]:
        print('DIRECCION DE RED:        {} /{}'.format(direccion_red(ip, mascara_red),mask_a_bits(mascara_red)))
        print('PRIMER HOST:             {}'.format(Primer_host(ip, mascara_red)))
        print('ULTIMO HOST:             {}'.format(ultimo_host(ip, mascara_red)))
        print('DIRECCION DE DIFUSION:   {}'.format(direc_difucion(ip, mascara_red)))
        print('CANTIDAD DE HOSTS:       {}'.format(numb_hosts(mascara_red)))
    else:
        print("IP fuera de los 32 bits")



def dividir_sub(ip, mascara_red, cantidad=1, hosts='equals'):
    if hosts=='equals':
        subneteado=subnetear_igual(ip, mascara_red,cantidad)
    else: 
        subneteado=subnetear_hosts(ip, mascara_red, hosts)
    for i in range(cantidad):
        subred=next(subneteado)
        print(' SUB-RED {} '.center(43, '~').format(i+1)+'\n')
        Basic(subred[0], subred[1])
        if i+1==cantidad:
            print('\n')
            print(' SIGUIENTE SUBRED: {} '.center(31, '~').format(subred[2])+'\n')
        print('\n')

def run():
    # ip=input('IP: ')
    # mascara_red=input('Mascara de subred: ')
    hosts=9000
    ip='172.16.0.0'
    mascara_red=16
    dividir_sub(ip, mascara_red,3)
    # Mostrar_Todo(ip, mascara_red)
    # Basic(ip, mascara_red)

if __name__ == '__main__':
    run()