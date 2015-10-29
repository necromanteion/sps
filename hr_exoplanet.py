'''
Uses the Bokeh library to plot an interactive graph of expolanet data from the ExoAPI: http://exoapi.com/.

More information on the data structure of the results returned by the ExoAPI can be found here:
https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue#data-structure.
'''

import collections
import math

from bokeh import models, plotting
import requests


def curve(a, b, c, x):
    '''
    Calculates a color curve of the form y = a + bx + c ln(x).

    Original info found from http://www.zombieprototypes.com/?p=210.
    '''
    return int(a + b * x + c * math.log(x))


def color(temperature):
    '''
    Calculates the hex color code from a star's temperature.
    '''

    # all are 255 at T = 6700K
    r, g, b = 255, 255, 255

    if temperature > 6700:
        r = curve(351.97690566805693, 0.114206453784165, -40.25366309332127, (temperature / 100 - 55))
        g = curve(325.4494125711974, 0.07943456536662342, -28.0852963507957, (temperature / 100 - 50))

    elif 2000 < temperature < 6700:
        g = curve(-155.25485562709179, -0.44596950469579133, 104.49216199393888, (temperature / 100 - 2))
        b = curve(-254.76935184120902, 0.8274096064007395, 115.67994401066147, (temperature / 100 - 10))

    elif 1000 <= temperature <= 2000:
        g = curve(-155.25485562709179, -0.44596950469579133, 104.49216199393888, (temperature / 100 - 2))
        b = 0

    elif temperature < 1000:
        g = 0
        b = 0

    # return r, g, b
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


Planet = collections.namedtuple('Planet', ['name', 'mass', 'radius', 'period', 'habitable', 'discovered', 'star'])
Star = collections.namedtuple('Star', ['name', 'mass', 'radius', 'temperature', 'luminosity'])


def exoplanets(**kwargs):
    '''Gathers data from the ExoAPI, filtering with keyword arguments passed.'''

    ENDPOINT = 'http://exoapi.com/api/skyhook/planets/search'

    r = requests.get(ENDPOINT, params=kwargs)

    for planet in r.json()['response']['results']:

        star = planet.get('star')

        yield Planet(name=planet.get('name'),
                     mass=planet.get('mass') or 1,
                     radius=planet.get('radius') or 1,
                     period=planet.get('period') or 1,
                     habitable=bool(planet.get('habitable')),
                     discovered=planet.get('disc_year'),
                     star=Star(name=star.get('name'),
                               mass=star.get('mass') or 1,
                               radius=star.get('radius') or 1,
                               temperature=star.get('teff') or 1,
                               luminosity=star.get('luminosity') or 1))


if __name__ == '__main__':
    p = plotting.figure(title='HR Diagram of Stars with Exoplanets',
                        x_range=[7000, 3000], y_range=[0.0001, 10000],
                        y_axis_type='log', tools='pan,resize,hover,wheel_zoom,box_zoom,reset')

    x, y, radii, colors = [], [], [], []
    stars, planets, masses, planet_radii, habitable, discovered = [], [], [], [], [], []

    for planet in exoplanets():
        star = planet.star

        x.append(star.temperature)
        y.append(star.luminosity)
        radii.append(star.radius**(1/4) * 6)
        colors.append(color(star.temperature))

        stars.append(star.name)
        planets.append(planet.name)
        masses.append(planet.mass)
        planet_radii.append(planet.radius)
        habitable.append(planet.habitable)
        discovered.append(planet.discovered)

    source = models.ColumnDataSource(
        dict(x=x, y=y, radii=radii, colors=colors,
             stars=stars,
             planets=planets,
             masses=masses,
             planet_radii=planet_radii,
             habitable=habitable,
             discovered=discovered
        )
    )

    p.scatter('x', 'y', alpha=0.95, color='colors', radius='radii', source=source)

    p.plot_height = 800
    p.plot_width = 1600
    p.background_fill = 'black'

    p.xaxis.axis_label = 'Temperature (K)'
    p.yaxis.axis_label = 'Luminosity (L☉)'

    p.grid.grid_line_color = 'darkgrey'
    p.grid.grid_line_alpha = 0.25
    p.grid.grid_line_dash = [6, 4]

    hover = p.select(dict(type=models.HoverTool))
    hover.tooltips = collections.OrderedDict([
        ('star', ' @stars'),
        ('name', ' @planets'),
        ('mass', ' @masses M<sub>⊕</sub>'),
        ('radius', ' @planet_radii R<sub>⊕</sub>'),
        ('habitable', ' @habitable'),
        ('discovered', ' @discovered')
    ])

    plotting.output_file('hr_exoplanet.html')
    plotting.show(p)