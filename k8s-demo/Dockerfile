# Imagen que va a usar el proyecto de spring boot
FROM openjdk:17-slim

VOLUME /tmp

# Archivo compilador de spring boot
ARG JAR_FILE=target/*.jar

# Copia el archivo compilado a la imagen
COPY ${JAR_FILE} app.jar

# Comando que se ejecuta al iniciar el contenedor
ENTRYPOINT ["java","-jar","/app.jar"]

