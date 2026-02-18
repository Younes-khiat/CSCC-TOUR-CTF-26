FROM php:8.2-apache

# Enable allow_url_include for the RFI vulnerability to work
RUN echo "allow_url_include = On" >> /usr/local/etc/php/conf.d/custom.ini \
    && echo "allow_url_fopen = On" >> /usr/local/etc/php/conf.d/custom.ini

# Copy the application to the web root
COPY index.php /var/www/html/index.php

# Place the flag outside the web root
COPY flag.txt /var/www/flag.txt

# Set proper permissions
RUN chown -R www-data:www-data /var/www/html /var/www/flag.txt

EXPOSE 80
