# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CicloFormativo(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    familia = scrapy.Field()
    duracion = scrapy.Field()
    perfil = scrapy.Field()
    modulos = scrapy.Field() # Código  módulo profesional  hora semanales (1º y 2º)
    accesouni = scrapy.Field()
    trabajos = scrapy.Field()
    centros = scrapy.Field()
    grado = scrapy.Field()
