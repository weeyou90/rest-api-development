FROM ubuntu:latest
RUN apt-get update && apt-get install --assume-yes apt-utils
RUN apt-get install -y python-pip
RUN apt-get install -y apache2
RUN apt-get install -y sqlite3
RUN apt-get install -y gunicorn

#python
RUN pip install --upgrade pip
RUN pip install -U bcrypt
RUN pip install -U Flask
RUN pip install -U pip
RUN pip install -U flask_sqlalchemy
RUN pip install -U flask-cors
RUN pip install -U SQLAlchemy
RUN pip install -U Jinja2
RUN pip install -U Werkzeug
RUN pip install -U wsgiref
RUN pip install -U Flask-WTF
RUN pip install -U alembic
RUN pip install -U itsdangerous
RUN echo "ServerName localhost  " >> /etc/apache2/apache2.conf
RUN echo "$user     hard    nproc       20" >> /etc/security/limits.conf
# WORKDIR ./src

ADD ./src/service /service
ADD ./src/html /var/www/html
COPY . /src
EXPOSE 80
EXPOSE 8080
CMD ["/bin/bash", "/service/start_services.sh"]
