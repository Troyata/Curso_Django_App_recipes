# Esta es la imagen que utilizaremos de python. Es una imagen con muy poco añadido
#por lo que pesa muy poco.
FROM python:3.10-alpine
#Best Practice es poner quien es el manintainer de este cotainer.
LABEL maintainer = "josetroyacantos@gmail.com" 
#Le dices a python que no almacene los resultados en el buffer sino que los represente
#directamente en la consola.
ENV PYTHONUNBUFFERED 1

#Copias requirements desde local al container para la instalación de los paquetes que
#vamos a necesitar
#Vamos a utilizar dos entornos: uno de desarrollo y otro para producción
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
#Aqui copias la carpeta donde vamos a instalar la aplicación del local al container
COPY ./app /app
#El directorio donde se ejecutaran todos los comandos por defecto
WORKDIR /app
#Enlazas el puerto del development server con el container
EXPOSE 8000

#Inciamos la imagen en un solo comando para evitar que haya varias capas y mantener
#la imagen lo más pequeña posible
#Lo primero es crear el entorno virtual dentro del contenedor
#Esto es un poco conflictivo pero te ayuda a evitar problemas de dependendecias
ARG DEV=false
RUN python -m venv /py && \
#Actualizamos pip
    /py/bin/pip install --upgrade pip && \
#Aquí incluimos la parta de base de datos
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
#Instalamos el archivo de requirements localizada en la carpeta que compiamos antes
#tmp
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV=true ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
#Eliminamos temp una vez ya no lo vamos a necesitar. De esta manera eliminamos
#Archivos que no vamos a necesitar. NOTA: El simbol22o "&&" " "te permite saltar de linea
    rm -rf /tmp && \
    #Borramos las dependencias que hemos utilizado para instalar postgresql
    apk del .temp-build-deps && \
#Creamos un usuario que nos permita hacer cambios pero distinto del root user
#De esta manera si tienes una brecha de seguridad. Te aseguras de que hay un usuario
#por encima en la jerarquia
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

#hace que no tengas que incluir /py/bin antes de todo ya que este será el root del 
#container
ENV PATH="/py/bin:$PATH"
#Estableces este usuario por defecto. NO ES EL ROOT USER
USER django-user


