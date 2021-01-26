#уровень детализации: Сельсоветы, Районы, ЦФО
level = 'Сельсоветы'

#имя файла с данными
filename = 'data.xlsx'

#название выводимого параметра
name = 'Население'

#список цветов
colors = {0: '#FDEFE3', 1: '#FAE2CC', 2: '#DFC7AF', 3: '#D1A174', 4: '#D1AE8D',
          5: '#A37142', 6: '#794D36', 7: '#6A3F15', 8: '#672900', 9: '#431C01'}

#тип карты: 0 - 5
map_type = 5

#логорифмирование показателя: True - Да, False - Нет
lg = True

############################################################################################

import pandas as pd
import folium
from math import log
import warnings
warnings.filterwarnings("ignore")

map_type_list = {0: 'mapboxbright', 1: 'openstreetmap', 2: 'stamenterrain',
                 3: 'stamentoner', 4: 'cartodbpositron ', 5: 'cartodbdark_matter'}

def popup_html(data):
    if level == 'Сельсоветы':
        html = f'<font face="Helvetica" weight=400><h3>{data.selsoviet}</h3>'
        html += f'<p><b>{data.district}</b><br><br>'
        html += f'{name}: {round(data.value, 2)}</p>'
    elif level == 'Районы':
        html = f'<font face="Helvetica" weight=400><h3>{data.district}</h3>'
        html += f'<p>{name}: {round(data.value, 2)}</p>'
    elif level == 'ЦФО':
        html = f'<font face="Helvetica" weight=400><h3>{data.region}</h3>'
        html += f'<p>{name}: {round(data.value, 2)}</p>'
    return html

def get_color(value, min_value, max_value):
    value_range = (max_value - min_value) / (len(colors.values())-1)
    color_index = (value - min_value) // value_range
    return colors[color_index]


def draw_to_map(data, m):
    if level == 'Сельсоветы':
        filename = r'J:\~ 09_Машинное обучение_Прогноз показателей СЭР\Геограницы\Обновленные\Сельсоветы ЛО\{}\{}.geojson'.format(data.district, data.selsoviet)
    elif level == 'Районы':
        filename = r'J:\~ 09_Машинное обучение_Прогноз показателей СЭР\Геограницы\Обновленные\Районы ЛО\{}.geojson'.format(data.district)
    elif level == 'ЦФО':
        filename = r'J:\~ 09_Машинное обучение_Прогноз показателей СЭР\Геограницы\Обновленные\ЦФО\{}.geojson'.format(data.region)

    geoj = folium.GeoJson(data=open(filename, encoding='utf-8').read(), control=False,
                          style_function=lambda x: {'color': 'black', 'fillColor': get_color(data.value_for_draw, min_value, max_value), 'fillOpacity': 0.75, 'opacity': 0.1, 'weight': 1},
                          highlight_function=lambda x: {'color': 'black', 'fillColor': get_color(data.value_for_draw, min_value, max_value), 'fillOpacity': 0.95, 'opacity': 0.2, 'weight': 1},
                          smooth_factor=0)

    iframe = folium.IFrame(popup_html(data), width=250, height=150)
    popup = folium.Popup(iframe)
    popup.add_to(geoj)
    geoj.add_to(m)

df = pd.read_excel(filename)

if lg:
    temp = df.value - df.value.min() + 1
    log_value = [log(value) for value in temp]
    df['value_for_draw'] = log_value
else:
    df['value_for_draw'] = df.value

min_value = df.value_for_draw.min()
max_value = df.value_for_draw.max()

if level == 'Сельсоветы' or level == 'Районы':
    m = folium.Map([52.7, 39.1], zoom_start=8, tiles=map_type_list[map_type], control_scale=True)
else:
    m = folium.Map([55, 39], zoom_start=6, tiles=map_type_list[map_type], control_scale=True)

if level == 'Сельсоветы':
    filename = r'J:\~ 09_Машинное обучение_Прогноз показателей СЭР\Геограницы\Обновленные\ЦФО\Липецкая область.geojson'
    geoj = folium.GeoJson(data=open(filename, encoding='utf-8').read(), control=False,
                          style_function=lambda x: {'color': 'black', 'fillOpacity': 0, 'opacity': 0.2, 'weight': 2},
                          smooth_factor=0)
    geoj.add_to(m)

    for district in df.district.unique():
        filename = r'J:\~ 09_Машинное обучение_Прогноз показателей СЭР\Геограницы\Обновленные\Районы ЛО\{}.geojson'.format(district)
        geoj = folium.GeoJson(data=open(filename, encoding='utf-8').read(), control=False,
                              style_function=lambda x: {'color': 'black', 'fillOpacity': 0, 'opacity': 0.2, 'weight': 2},
                              smooth_factor=0)
        geoj.add_to(m)

    for index in df.index:
        draw_to_map(df.loc[index], m)

elif level == 'Районы':
    filename = r'J:\~ 09_Машинное обучение_Прогноз показателей СЭР\Геограницы\Обновленные\ЦФО\Липецкая область.geojson'
    geoj = folium.GeoJson(data=open(filename, encoding='utf-8').read(), control=False,
                          style_function=lambda x: {'color': 'black', 'fillOpacity': 0, 'opacity': 0.2, 'weight': 2},
                          smooth_factor=0)
    geoj.add_to(m)

    for index in df.index:
        draw_to_map(df.loc[index], m)

elif level == 'ЦФО':
    for index in df.index:
        draw_to_map(df.loc[index], m)

m.save(f'Карта плотности - {name}.html')