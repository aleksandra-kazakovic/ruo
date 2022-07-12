FROM php:7.4-apache

COPY . /var/www/html
COPY conf/apache2.conf /etc/apache2/
RUN docker-php-ext-install mysqli

