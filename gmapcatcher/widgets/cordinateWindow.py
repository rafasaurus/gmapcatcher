# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.EXWindow
# Widget that displays azimuth, lat/long, sk42 cordinates

import pygtk
pygtk.require('2.0')
import gtk
import numpy as np
from WGS84_SK42_Translator import Translator as converter
import pyproj

from customWidgets import lbl, myEntry, myFrame, SpinBtn, FolderChooser

class CordinateWindow(gtk.Window):
    def __init__(self, azimuth, distance, start_point, end_point, compass_encoder_diff, mag_merid, true_north):
        self.proj_wgs84 = pyproj.Proj(init="epsg:4326")
        self.proj_sk42 = pyproj.Proj(init="epsg:28468")
        azimuth_hbox = gtk.HBox(False, 20)
        sk42_hbox_full = gtk.HBox(False, 20)

        self.proj_wgs84 = pyproj.Proj(init="epsg:4326")
        self.proj_sk42 = pyproj.Proj(init="epsg:28468")

        def _area():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("азимут:"))
            self.entry = myEntry("%.6g" % azimuth, 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox.pack_start(lbl("Дирекционный угол:"))
            self.entry = myEntry("%.2f" % float((azimuth - true_north)/6), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox.pack_start(lbl("маг. угол с искажением:"))
            self.entry = myEntry("%.2f" % float((azimuth + mag_merid)/6), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("azimuth input:"))
            self.entry = myEntry("%.2f" % distance, 10, False)
            hbox.pack_start(self.entry, False)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("encoder:"))
            azimuth_compass_encoder_diff = azimuth + compass_encoder_diff
            # correcting the diff hwen its above 360
            if azimuth_compass_encoder_diff >= 360:
                azimuth_compass_encoder_diff -= 360
            self.entry = myEntry("%.2f" % azimuth_compass_encoder_diff, 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox.pack_start(lbl("distance:"))
            self.entry = myEntry("%.1f" % distance, 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame(" Calculated Azimuth and Distance", vbox)

        def _start_point():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("широта:"))
            self.azimuth = myEntry("%.6f" % start_point[0], 10, False)
            hbox.pack_start(self.azimuth, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("долгота:"))
            self.distance = myEntry("%.6f" % start_point[1], 10, False)
            hbox.pack_start(self.distance, False)
            vbox.pack_start(hbox)

            return myFrame("базовая точка", vbox)

        def _end_point():
            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("широта:"))
            self.entry = myEntry("%.6f" % end_point[0], 10, False)
            print(end_point[0])
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("долгота:"))
            self.entry = myEntry("%.6f" % end_point[1], 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame("цель", vbox)

        def _wgs_to_sk42_end_full():
            height = 900 
            # convertedLat = converter.WGS84_SK42_Lat(end_point[0],end_point[1],height)
            # convertedLon = converter.WGS84_SK42_Long(end_point[0],end_point[1],height)
            convertedLon, convertedLat = pyproj.transform(self.proj_wgs84, self.proj_sk42 , np.float64(end_point[1]), np.float64(end_point[0]))

            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("X:"))
            self.entry = myEntry(str("%.0f" % convertedLat), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("Y:"))
            self.entry = myEntry(str("%.0f" % convertedLon), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame("SK42 full EPSG:28468", vbox)

        def _wgs_to_sk42_start_full():
            height = 900 
            # convertedLat = converter.WGS84_SK42_Lat(np.float64(start_point[0]),np.float64(start_point[1]),height)
            # convertedLon = converter.WGS84_SK42_Long(np.float64(start_point[0]),np.float64(start_point[1]),height)
            convertedLon, convertedLat = pyproj.transform(self.proj_wgs84, self.proj_sk42 , np.float64(start_point[1]), np.float64(start_point[0]))

            vbox = gtk.VBox(False, 5)
            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("широта:"))
            self.entry = myEntry(str("%.0f" % convertedLat), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            hbox = gtk.HBox(False, 10)
            hbox.pack_start(lbl("долгота:"))
            self.entry = myEntry(str("%.0f" % convertedLon), 10, False)
            hbox.pack_start(self.entry, False)
            vbox.pack_start(hbox)

            return myFrame("SK42 full EPSG:28468", vbox)

        gtk.Window.__init__(self)
        vbox = gtk.VBox(False)
        hbox = gtk.HBox(False, 10)
        hbox.pack_start(_area())

        azimuth_hbox.pack_start(_start_point())
        azimuth_hbox.pack_start(_end_point())

        sk42_hbox_full.pack_start(_wgs_to_sk42_start_full())
        sk42_hbox_full.pack_start(_wgs_to_sk42_end_full())

        vbox.pack_start(hbox)
        vbox.pack_start(azimuth_hbox)
        vbox.pack_start(sk42_hbox_full)
        self.add(vbox)
        self.set_title("Azimuth and Distance Calculator")
        self.set_border_width(10)
        self.show_all()
