# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from fpSpider.items import CicloFormativo



class FpSpider(scrapy.Spider):
    name = "fp"
    allowed_domains = ["fp.educaragon.org"]
    start_urls = (
        'http://fp.educaragon.org/guiaeducativa/guia_educativa_familias.asp?grafico=2&id_ensenanza=5&id_ciclo=1&titulo=Formaci%F3n+profesional+espec%EDfica+-+Grado+medio',
        'http://fp.educaragon.org/guiaeducativa/guia_educativa_familias.asp?grafico=2&id_ensenanza=5&id_ciclo=2&titulo=Formaci%F3n+profesional+espec%EDfica+-+Grado+superior',
        'http://fp.educaragon.org/guiaeducativa/guia_educativa_familias.asp?grafico=2&id_ensenanza=5&id_ciclo=6&titulo=Formaci%F3n%20Profesional%20B%E1sica'
    )

    def parse(self, response):
    	for link in response.xpath('//table[@id="Table4"]//a/@href').extract():
    		yield Request('http://fp.educaragon.org/guiaeducativa/' + link, callback = self.parse_familia)

    def parse_familia(self, response):
        for link in response.xpath('//table[@id="Table7"]//a/@href').extract():
            _tabla1 = ' '.join(response.xpath('//table[1]//text()').extract())
            if 'Grado medio' in _tabla1 or 'Formación Profesional Básica' in _tabla1:
                yield Request('http://fp.educaragon.org/guiaeducativa/' + link,
                    callback = self.parse_ciclo_medio_basica)
            else:
                yield Request('http://fp.educaragon.org/guiaeducativa/' + link,
                    callback = self.parse_ciclo_superior)

    def parse_ciclo_medio_basica(self, response):
        c = CicloFormativo()
        _tabla1 = ' '.join(response.xpath('//table[@id="Table1"]//text()').extract())
        if 'Grado medio' in _tabla1:
            c['grado'] = 'medio'
        else:
            c['grado'] = 'fpb'

        c['url'] = response.url
        familia = response.xpath('//table[@id="Table3"]/tr/td[last()]/text()[1]').extract()[0].strip()
        if familia:
            c['familia'] = familia
        _datos = response.xpath('//table[@id="Table4"]/tr/td//text()').extract()
        ciclo = _datos[0].strip()
        c['name'] = ciclo

        if 'Duración' in _datos:
            i = _datos.index('Duración:')
            duracion = _datos[ i+1 ].strip()
            c['duracion'] = duracion
        if 'Perfil Profesional' in _datos:
            i = _datos.index('Perfil Profesional:')
            perfil = _datos[ i+1 ].strip()
            c['perfil'] = perfil


        modulos = [l.xpath('td/text()').extract() for l in response.xpath('//table[@id="Table9"]/tr')]
        modulos = [h for h in modulos if h]
        c['modulos'] = modulos

        puestos = response.xpath('//table[@id="Table10"]//text()').extract()
        if puestos:
            puestos = [p.strip() for p in puestos]
            puestos = [p for p in puestos if p]
            puestos = [p for p in puestos if 'Puestos de trabajo' not in p]
            c['trabajos'] = puestos

        centros_url = response.xpath('//table[@id="Table4"]//a/@href').extract()

        request = Request("http://fp.educaragon.org/guiaeducativa/" + centros_url[0],
                             callback=self.parse_centros)
        request.meta['item'] = c

        yield request


    def parse_centros(self, response):
        item = response.meta['item']

        centros = [c.xpath('td/text()').extract() for c in response.xpath('//table[@id="Table5"]/tr')]
        centros = [list(map(lambda x: x.strip(), c)) for c in centros]
        centros = [c for c in centros if ''.join(c)]

        item['centros'] = centros
        yield item

    def parse_ciclo_superior(self, response):
        c = CicloFormativo()
        c['grado'] = 'superior'
        c['url'] = response.url

        familia = response.xpath('//table[@id="Table3"]/tr/td[last()]/text()[1]').extract()[0].strip()
        if familia:
            c['familia'] = familia
        _datos = response.xpath('//table[@id="Table4"]/tr/td//text()').extract()
        ciclo = _datos[0].strip()
        c['name'] = ciclo

        if 'Duración' in _datos:
            i = _datos.index('Duración:')
            duracion = _datos[ i+1 ].strip()
            c['duracion'] = duracion

        if 'Perfil Profesional' in _datos:
            i = _datos.index('Perfil Profesional:')
            perfil = _datos[ i+1 ].strip()
            c['perfil'] = perfil


        modulos = [l.xpath('td/text()').extract() for l in response.xpath('//table[@id="Table9"]/tr')]
        modulos = [h for h in modulos if h]
        c['modulos'] = modulos

        puestos = response.xpath('//table[@id="Table10"]//text()').extract()
        if puestos:
            puestos = [p.strip() for p in puestos]
            puestos = [p for p in puestos if p]
            puestos = [p for p in puestos if 'Puestos de trabajo' not in p]
            c['trabajos'] = ' '.join(puestos)

        acceso = response.xpath('//table[@id="Table8"]//text()').extract()
        if acceso:
            acceso = [p.strip() for p in acceso]
            acceso = [p for p in acceso if p]
            acceso = [p for p in acceso if 'Acceso a estudios universitarios' not in p]
            c['accesouni'] = ' '.join(acceso)

        centros_url = response.xpath('//table[@id="Table4"]//a/@href').extract()

        request = Request("http://fp.educaragon.org/guiaeducativa/" + centros_url[0],
                             callback=self.parse_centros)
        request.meta['item'] = c

        yield request



'''

name = scrapy.Field()
    familia = scrapy.Field()
    duracion = scrapy.Field()
    perfil = scrapy.Field()
    modulos = scrapy.Field() # Código  módulo profesional  hora semanales (1º y 2º)
    accesouni = scrapy.Field()
    trabajos = scrapy.Field()
    centros = scrapy.Field()


http://fp.educaragon.org/guia_educativa_familias.asp?id_ensenanza=5&id_ciclo=1&titulo=Formaci%F3n+profesional+espec%EDfica+%2D+Grado+medio&idFam=1&familia=Agraria&descripcion=
http://fp.educaragon.org/guiaeducativa/guia_educativa_familias.asp?id_ensenanza=5&id_ciclo=1&titulo=Formaci%F3n+profesional+espec%EDfica+%2D+Grado+medio&idFam=1&familia=Agraria&descripcion=
http://fp.educaragon.org/guiaeducativa/directorio_modulos.asp?grafico=&idE=2161&nombreC=Agraria&fotoC=familia_gMedio.gif&familia=si&titulo=Formaci%F3n%20profesional%20espec%EDfica%20-%20Grado%20medio
'''
