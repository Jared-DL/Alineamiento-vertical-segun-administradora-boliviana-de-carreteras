import math


def recolectar_datos():
    global velocidad_proyecto
    global cota_PIV_1
    global cota_PIV_2
    global cota_PIV_3
    global progresiva_PIV_1
    global progresiva_PIV_2
    global progresiva_PIV_3
    global m_pendiente_entrada
    global n_pendiente_salida
    global lr_longitud_recta
    global a_dif_de_pendientes
    
    velocidad_proyecto=float(input('Velocidad de Proyecto Vp[km/h]: '))
    
    # eleccion = eleccion_simple('¿Tiene los datos m(pendiente de entrada), n(pendiente de salida), Lr longitud de recta que precede al PIV, cota y progresiva del PIV donde se hará la curva?')
    eleccion=True
    if eleccion == True:
        cota_PIV_2=float(input('Cota de PIV_2[msnm](PIV donde se hará la curva): '))
        progresiva_PIV_2=float(input('progresiva de PIV_2[m](PIV donde se hará la curva): '))
        m_pendiente_entrada=float(input('Pendiente de entrada m[tanto por 1]: '))
        n_pendiente_salida=float(input('Pendiente de salida n[tanto por 1]: '))
        lr_longitud_recta=float(input('Longitud de recta Lr[m]: '))
        a_dif_de_pendientes=m_pendiente_entrada-n_pendiente_salida
        print(f'diferencia de pendientes A[tanto por 1]={a_dif_de_pendientes}')
    else:
        print('Muy pronto... estar atento')
        exit()
        # print('Si no tiene alguno de los datos escriba: null: ')
        # cota_PIV_1=input('Cota de PIV_1[msnm](antes del PIV donde se hará la curva): ')
        # cota_PIV_2=input('Cota de PIV_2[msnm](PIV donde se hará la curva): ')
        # cota_PIV_3=input('Cota de PIV_3[msnm](despues del PIV donde se hará la curva): ')
        # progresiva_PIV_1=input('Cota de PIV_1[msnm](antes del PIV donde se hará la curva): ')
        # progresiva_PIV_2=input('Cota de PIV_2[msnm](PIV donde se hará la curva): ')
        # progresiva_PIV_3=input('Cota de PIV_3[msnm](despues del PIV donde se hará la curva): ')
        # m_pendiente_entrada=input('Pendiente de entrada m[tanto por 1]: ')
        # n_pendiente_salida=input('Pendiente de salida n[tanto por 1]: ')
        # lr_longitud_recta=input('Longitud de recta Lr[m]: ')


def longitud_de_la_curva_vertical():
    global tipo_de_curva   
    global velocidad_en_CV #CV=curva vertical
    if a_dif_de_pendientes>0:
        tipo_de_curva='concava'
    elif a_dif_de_pendientes<0:
        tipo_de_curva='convexa'
    else:
        print('ERROR se tiene una diferencia de pendiente de 0 por lo que no se necesita una curva vertical')
        exit()
    
    if tipo_de_curva == 'convexa':
        if lr_longitud_recta>600:    
            velocidad_en_CV = velocidad_proyecto +10
        elif lr_longitud_recta>400:
            velocidad_en_CV = velocidad_proyecto + 5
        else:
            velocidad_en_CV = velocidad_proyecto
    elif tipo_de_curva == 'concava':
        velocidad_en_CV = velocidad_proyecto
    print(f'Para la curva {tipo_de_curva}, con Lr={lr_longitud_recta}, tenemos una velocidad de: {velocidad_en_CV}')

    if abs(m_pendiente_entrada)>abs(n_pendiente_salida):
        i_pendiente_mayor=abs(m_pendiente_entrada)
    else:
        i_pendiente_mayor=abs(n_pendiente_salida)

    f=float(input(f'factor f para V={velocidad_en_CV} (sacar de tabla 2.2-1 Pag.2-7): '))
    tiempo_de_reacción=float(input(f'factor t para V={velocidad_en_CV} (sacar de tabla 2.2-1 Pag.2-7): '))

    df_distancia_de_frenado=velocidad_en_CV*tiempo_de_reacción/3.6+velocidad_en_CV**2/254/(f-i_pendiente_mayor)
    print(f'distancia de frenado Df= {velocidad_en_CV}*{tiempo_de_reacción}/3.6+{velocidad_en_CV}**2/254({f}-{i_pendiente_mayor})  = {df_distancia_de_frenado}')
    
    if tipo_de_curva == 'convexa':
        k=df_distancia_de_frenado**2/4.48
    elif tipo_de_curva == 'concava':
        k=df_distancia_de_frenado**2/(1.2+0.035*df_distancia_de_frenado)
        eleccion = eleccion_simple('¿Deseas que se muestre los casos especiales?')
        if eleccion == True :
            c=float(input('factor c luz libre: '))
            kci=velocidad_en_CV**2/3.89         #ilumicación artificial
            kce=df_distancia_de_frenado**2/(8*c-4*(2.5+.45))        #bajo estructuras
            longitud_CV_iluminacion_artificial=kci*a_dif_de_pendientes
            longitud_CV_bajo_estructura=kce*a_dif_de_pendientes
            print(f'kci= {kci} y la longitud de curva(iluminaión artificial)[m]= {longitud_CV_iluminacion_artificial}')
            print(f'kce= {kce} y la longitud de curva(bajo estructuras)[m]= {longitud_CV_bajo_estructura}')
    longitud_CV=k*a_dif_de_pendientes
    print(f'k= {k} y la longitud de curva[m]= A*K= {longitud_CV}')
    

def eleccion_simple(pregunta):
    print(pregunta)
    eleccion=input("""0. NO
1. SI
elección: """)
    if eleccion == '0':
        return False
    elif eleccion == '1':
        return True
    else:
        print('SELECCIONA UNA OPCIÓN VÁLIDA')
        eleccion_simple(pregunta)


def elegir_CV_simétrica_asimétrica():
    print('¿Que curva se usará?')
    eleccion=input("""0. Simétrica
1. Asimétrica
elección: """)
    if eleccion == '0':
        calculos_curva_simetrica()
    elif eleccion == '1':
        calculos_curva_asimétrica()
    else:
        print('SELECCIONA UNA OPCIÓN VÁLIDA')
        elegir_CV_simétrica_asimétrica()

def calculos_curva_simetrica():
    progresiva_curva=[]
    cota_curva=[]
    longitud_de_curva=float(input('longitud adoptada de curva vertical[m]: '))
    cota_PCV = cota_PIV_2 - longitud_de_curva/2*m_pendiente_entrada
    progresiva_PCV = progresiva_PIV_2-(cota_PIV_2-cota_PCV)/abs(m_pendiente_entrada)
    cota_FCV= cota_PIV_2 + longitud_de_curva/2*n_pendiente_salida
    progresiva_FCV = progresiva_PIV_2+(cota_PIV_2-cota_FCV)/abs(n_pendiente_salida)
    longitud_de_replanteo=int(input('longitud entre puntos para replanteo(10 , 20 etc) ='))
    print(f'Cota PCV[msnm] = {cota_PCV}')
    print(f'Progresiva PCV[msnm] = {progresiva_PCV}')
    print(f'Cota FCV[msnm] = {cota_FCV}')
    print(f'Progresiva FCV[msnm] = {progresiva_FCV}')

    print( '---REPLANTEO---')
    contador=0                                  #PARA PCV
    x=0
    mx=0
    cota_tangente=0
    y=0
    progresiva_curva.append(progresiva_PCV)
    cota_curva.append(cota_PCV)
    print(f'X={x}')
    print(f'm*x={mx}')
    print(f'cota tangente={cota_tangente}')
    print(f'Y={y}')
    print(f'Progresiva PCV ={progresiva_curva[contador]}')
    print(f'Cota PCV ={cota_curva[contador]}')
    x=int(math.ceil(progresiva_PCV)-progresiva_PCV)   
    while x<longitud_de_curva:                          #PARA LOS DEMAS
        while x%longitud_de_replanteo != 0:   
            x +=1
        contador+=1
        x+=longitud_de_replanteo
        mx=x*m_pendiente_entrada
        cota_tangente=cota_PCV+mx
        y=a_dif_de_pendientes/2/longitud_de_curva*x**2
        progresiva_curva.append((progresiva_PCV+x))
        cota_curva.append(cota_tangente-y)
        print('---------')
        print(f'X={x}')
        print(f'm*x={mx}')
        print(f'cota tangente={cota_tangente}')
        print(f'Y={y}')
        print(f'Progresiva ={progresiva_curva[contador]}')
        print(f'Cota= {cota_curva[contador]}')


def calculos_curva_asimétrica():
    progresiva_curva=[]
    cota_curva=[]
    longitud_de_curva_1=float(input('longitud 1 de curva vertical[m]: '))
    longitud_de_curva_2=float(input('longitud 2 de curva vertical[m]: '))
    longitud_de_curva_total=longitud_de_curva_1+longitud_de_curva_2
    print(f'longitud total de la curva[m]: {longitud_de_curva_total}')
    cota_PCV = cota_PIV_2 - longitud_de_curva_1*m_pendiente_entrada
    progresiva_PCV = progresiva_PIV_2-(cota_PIV_2-cota_PCV)/abs(m_pendiente_entrada)
    cota_FCV= cota_PIV_2 + longitud_de_curva_2/2*n_pendiente_salida
    progresiva_FCV = progresiva_PIV_2+(cota_PIV_2-cota_FCV)/abs(n_pendiente_salida)
    longitud_de_replanteo=int(input('longitud entre puntos para replanteo(10 , 20 etc) ='))
    print(f'Cota PCV[msnm] = {cota_PCV}')
    print(f'Progresiva PCV[msnm] = {progresiva_PCV}')
    print(f'Cota FCV[msnm] = {cota_FCV}')
    print(f'Progresiva FCV[msnm] = {progresiva_FCV}')

    print( '--------REPLANTEO DE PCV--------')
    contador=0                                  #PARA PCV
    x=0
    mx=0
    cota_tangente=0
    y=0
    progresiva_curva.append(progresiva_PCV)
    cota_curva.append(cota_PCV)
    print(f'X={x}')
    print(f'm*x={mx}')
    print(f'cota tangente={cota_tangente}')
    print(f'Y={y}')
    print(f'Progresiva PCV ={progresiva_curva[contador]}')
    print(f'Cota PCV ={cota_curva[contador]}')
    x=int(math.ceil(progresiva_PCV)-progresiva_PCV)   
    while x<longitud_de_curva_1:                        
        while x%longitud_de_replanteo != 0:   
            x +=1
        contador+=1
        x+=longitud_de_replanteo
        mx=x*1*m_pendiente_entrada
        cota_tangente=cota_PCV+mx
        y=a_dif_de_pendientes/2/longitud_de_curva_total*x**2*longitud_de_curva_2/longitud_de_curva_1
        progresiva_curva.append((progresiva_PCV+x))
        cota_curva.append(cota_tangente-y)
        print('---------')
        print(f'X={x}')
        print(f'm*x={mx}')
        print(f'cota tangente={cota_tangente}')
        print(f'Y={y}')
        print(f'Progresiva ={progresiva_curva[contador]}')
        print(f'Cota= {cota_curva[contador]}')

    print( '--------REPLANTEO DE FCV--------')
    contador=0                                  #PARA FCV
    x=0
    mx=0
    cota_tangente=0
    y=0
    progresiva_curva.append(progresiva_FCV)
    cota_curva.append(cota_FCV)
    print(f'X={x}')
    print(f'm*x={mx}')
    print(f'cota tangente={cota_tangente}')
    print(f'Y={y}')
    print(f'Progresiva FCV ={progresiva_curva[contador]}')
    print(f'Cota FCV ={cota_curva[contador]}')
    x=int(math.ceil(progresiva_FCV)-progresiva_FCV)   
    while x<longitud_de_curva_2:                        
        while x%longitud_de_replanteo != 0:   
            x +=1
        contador+=1
        x+=longitud_de_replanteo
        mx=x*-n_pendiente_salida
        cota_tangente=progresiva_FCV+mx
        y=a_dif_de_pendientes/2/longitud_de_curva_total*x**2*longitud_de_curva_1/longitud_de_curva_2
        progresiva_curva.append((progresiva_FCV+x))
        cota_curva.append(cota_tangente-y)
        print('---------')
        print(f'X={x}')
        print(f'm*x={mx}')
        print(f'cota tangente={cota_tangente}')
        print(f'Y={y}')
        print(f'Progresiva ={progresiva_curva[contador]}')
        print(f'Cota= {cota_curva[contador]}')

def eleccion_de_tipo_de_calculos():
    eleccion=input("""¿Deseas realizar mas calculos?
0. NO (el programa finalizará)
1. Ingresar otros datos
2. hallar longitud de curva vertical(simétrica o asimétrica)
3. calcular progresivas y cotas de replanteo
Elección: """)
    if eleccion == '1':
        recolectar_datos()
        eleccion_de_tipo_de_calculos()
    elif eleccion == "2":
        longitud_de_la_curva_vertical()
        eleccion_de_tipo_de_calculos()
    elif eleccion == '3':
        elegir_CV_simétrica_asimétrica()
        eleccion_de_tipo_de_calculos()
    elif eleccion == '0':
        print("""
Gracias por el usar el programita Xo
--- Jared DL --- github.com/Jared-DL ---
        """)


if __name__ == "__main__":
    print('---Bienvenido al programita para facilitar calculos de curvas verticales---')
    recolectar_datos()
    eleccion_de_tipo_de_calculos()