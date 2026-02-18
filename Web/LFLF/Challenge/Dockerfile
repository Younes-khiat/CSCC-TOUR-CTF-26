FROM php:8.2-apache

# Copy the application to the web root
COPY index.php /var/www/html/index.php

# Create the flag file one directory above the web root
RUN echo 'CSCC{l0c4l_f1l3_3xplos10n}' > /var/www/flag.txt

# Set proper permissions
RUN chown -R www-data:www-data /var/www/html /var/www/flag.txt

EXPOSE 80
