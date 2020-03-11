from requests import get

from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpResponse
from django.shortcuts import render


def where(request):
    g = GeoIP2()
    ip = _get_client_ip(request)
    if ip == '127.0.0.1':
        ip = get('https://api.ipify.org').text
    city = g.city(ip)
    # 'continent_code': 'EU', 'continent_name': 'Europe', 'country_code': 'CZ', 'country_name': 'Czechia',
    # 'dma_code': None, 'is_in_european_union': True, 'postal_code': '130 00', 'region': '10', 'time_zone': 'Europe/Prague'}
    return HttpResponse('%s, %s, lat %s long %s' % (ip, city['city'], city['latitude'], city['longitude']))

def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
