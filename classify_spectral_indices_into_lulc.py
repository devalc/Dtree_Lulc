# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 21:29:47 2018

@author: Chinmay
"""

import numpy as np
import gdal, copy
from gdalconst import * 
import matplotlib.pyplot as plt

# input path
inputpath = 'D:/Chinmay/Pune/Analysis_06_06_2018/NITK_RSGIS_20180824_154257/Outputs/LT05_L1TP_147047_19900318_20170131_01_T1.tar/LT5[147_047](1990-03-18_04-48)'


# read spectral indices into numpy arrays
ndvidata = gdal.Open(inputpath+'NDVI.TIF', GA_ReadOnly)
NDVI = np.array(ndvidata.GetRasterBand(1).ReadAsArray())
ndwidata = gdal.Open(inputpath+'NDWI.TIF', GA_ReadOnly)
NDWI = np.array(ndwidata.GetRasterBand(1).ReadAsArray())
ndbidata = gdal.Open(inputpath+'NDBI_01.TIF', GA_ReadOnly)
NDBI = np.array(ndbidata.GetRasterBand(1).ReadAsArray())
ndbaidata = gdal.Open(inputpath+'NDBaI_01.TIF', GA_ReadOnly)
NDBAI = np.array(ndbaidata.GetRasterBand(1).ReadAsArray())
mndwidata = gdal.Open(inputpath+'MNDWI_01.TIF', GA_ReadOnly)
MNDWI = np.array(mndwidata.GetRasterBand(1).ReadAsArray())


# create dictionary of thhresholds to be used for each spectral index to be classified \
#into a thematic raster class

thresholds = {"Wat_MNDWI": 0.3,
              "Veg_NDVI" : 0.3,
              "Veg_NDWI1": 0.0,
              "Veg_NDWI2": 0.3,
              "Veg_NDBI1" : -0.02,
              "Veg_NDBI2" : -0.2,
              "Veg_NDBaI1": -0.3,
              "Veg_NDBaI2": -0.6,
              "Sed_NDBaI1": -0.6,
              "Sed_NDBaI2": 0.75,
              "Built_NDVI": 0.02,
              "Built_NDWI": 0.2,
              "Built_NDBI": 0.15,
              "Built_NDBaI": -0.25,
              "Fallow_NDVI": 0.2,
              "Fallow_NDWI1": -0.1,
              "Fallow_NDWI2": -0.25,
              "Fallow_NDBI1": 0.1,
              "Fallow_NDBI2": 0.3,
              "Fallow_NDBaI": -0.3
              }

    

def lulc_classify(NDVI, NDBI, NDBAI, NDWI, MNDWI):
    """
    
    """
    #create empty raster of same size as others
    Classified_raster = np.zeros(NDVI.shape)
    #Water
    #Classified_raster[np.where(MNDWI>=thresholds["Wat_MNDWI"])] = 1
    
    
    # Sediment/river bed
    Classified_raster[np.where(np.logical_and(NDBAI>= thresholds["Sed_NDBaI2"], \
                                              NDBAI <= thresholds["Sed_NDBaI1"]))] = 2 
      
    #Builtup area
    Classified_raster[np.where(np.logical_and(NDVI < thresholds["Built_NDVI"] , \
                               NDWI < thresholds["Built_NDWI"]) & \
    np.logical_and(NDBI>=thresholds["Built_NDBI"], NDBAI < thresholds["Built_NDBaI"]))]=3
    
    return Classified_raster

    
#    # Vegetation
#    
#    Classified_raster[np.where(np.logical_and(NDWI>thresholds["Veg_NDWI1"], NDWI < thresholds["Veg_NDWI2"]) & \
#                               NDVI> thresholds["Veg_NDVI"] & \
#                               (np.logical_and(NDBI > ["Veg_NDBI2"], NDBI < ["Veg_NDBI1"])) & \
#                               (np.logical_and(NDBAI > ["Veg_NDBaI2"], NDBI < ["Veg_NDBaI1"])))] = 3


    Classified_raster[np.where(NDVI < thresholds["Built_NDVI"] & \
                               NDWI < thresholds["Built_NDWI"] & \
                               NDBI >= thresholds["Built_NDBI"] & \
                               NDBAI < thresholds["Built_NDBaI"])] = 4
    
#    #Fallow land
    Classified_raster[np.where(np.logical_and(NDBI>thresholds["Fallow_NDBI1"], NDBI <= thresholds["Fallow_NDBI2"]) &\
                               NDVI < thresholds["Fallow_NDVI"] & \
                               np.logical_and(NDWI >= thresholds["Fallow_NDWI2"], NDWI < thresholds["Fallow_NDBI1"]) & \
                               NDBAI < thresholds["Fallow_NDBaI"])] = 5 
#                               
                               
                      
    
    return Classified_raster


        