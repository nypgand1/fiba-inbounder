# -*- coding: utf-8 -*-
import svgwrite
import cairosvg
import pandas as pd
import numpy as np

from fiba_inbounder.settings import SHOT_CHART_BACKGROUND, SHOT_CHART_ZONE_GEO, SHOT_CHART_PERC_RED

class Zone():
    def __init__(self, chart, zid, name, points=[], center=(0, 0), made=0, attempt=0, fga=0):
        self.chart = chart
        self.zid = zid
        self.name = name
        self.points = points
        self.center = center
        self.made = made
        self.attempt = attempt
        self.fga = fga

        self.rect_size = (80, 50)
        self.rect_insert = [
                self.center[0]- (self.rect_size[0] / 2),
                self.center[1] - (self.rect_size[1] / 2)]

    def get_hot_cold_color(self):
        if not self.attempt:
            return 'black'

        perc = float(self.made) / self.attempt
        perc_red = SHOT_CHART_PERC_RED[self.zid]
        perc_yellow = perc_red - 0.1

        if perc >= perc_red:
            return '#e5786d' #Red
        elif perc >= perc_yellow:
            return '#eadead' #Yellow
        else:
            return '#88b8f6' #Blue

    def get_weight_opacity(self):
        if not self.fga:
            return 1

        weight = float(self.attempt) / self.fga

        if weight >= 0.27:
            return 0.90
        elif weight > 0.09:
            return 0.75
        elif weight >= 0.03:
            return 0.40
        else:
            return 0.30

    def get_svg_elements(self):
        group = self.chart.g(opacity=self.get_weight_opacity(), fill=self.get_hot_cold_color())
        group.add(self.chart.polygon(points=self.points))
       
        if not self.attempt:
            return group
        
        text = self.chart.text('', insert=self.center, fill='white', opacity=1.0,
            style='text-anchor: middle; font-weight: bold;',
            font_family='coolvetica', font_size=16)
        text.add(self.chart.tspan('%d / %d' % (self.made, self.attempt), x=[self.center[0]], dy=['-0.2em']))
        text.add(self.chart.tspan('%.1f%%' % (100.0*self.made/self.attempt), x=[self.center[0]], dy=['1em']))
        
        group.add(self.chart.rect(insert=self.rect_insert, size=self.rect_size, 
            rx=10, ry=50, fill='black', style='stroke: grey; stroke-width: 1px;'))
        group.add(text)

        return group

class ShotChart():
    size=(652, 613)
    def __init__(self, filename, fgm_list, fga_list):
        self.filename = filename
        
        self.chart = svgwrite.Drawing(filename='%s.svg'%self.filename, size=self.size)
        self.chart.add(self.chart.image(SHOT_CHART_BACKGROUND, insert=(0, 0), size=self.size))

        self.zone_list = list()

        for geo in SHOT_CHART_ZONE_GEO['features']:
            zone = Zone(self.chart, geo['properties']['id'], geo['properties']['zone_name'],
                    geo['geometry']['coordinates'], geo['geometry']['center'],
                    fgm_list[geo['properties']['id']], 
                    fga_list[geo['properties']['id']],
                    sum(fga_list))
        
            group = zone.get_svg_elements()
            self.chart.add(group)
            self.zone_list.append(group)
        #self.chart.save()
        cairosvg.svg2png(bytestring=self.chart.tostring(), write_to='%s.png'%self.filename)
