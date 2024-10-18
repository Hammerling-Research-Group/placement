#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 16:01:36 2022

@author: mengjia
"""

import numpy as np

def wind_synthesizer(df_ws, df_wd, wind_syn_mode, 
                     wind_sensor = None, colname_t = 'time_stamp.mountain'):
    '''
    Combine wind data from multiple sensors to one-single wind data
    Inputs:
        df_ws [m/s] (pd.DataFrame):
            wind speed dataframe; columns include time stamps, wind speed from each wind sensor
        df_wd [degree] (pd.DataFrame):
            wind direction dataframe; columns include time stamps, wind direction from each wind sensor
        wind_syn_mode (str):
            methods to combine multiple wind data
                - 'scalar_mean': take mean on wind speed and median on wind directions across sensors
                - 'single': select wind data from a single wind sensor
                - 'vector_mean': 
                    1. convert ws, wd to u, v components; 
                    2. take mean on u & v across sensors
                    3. bring averaged u & v back to ws and wd
                - 'circular_mean': take median on wind speed and circular median on wind direction
        wind_sensor (str):
            the selected wind sensor name when wind_syn_mode = 'single'
        colname_t (str):
            the column name of time_stamps in df_ws and df_wd
    Outputs:
        ws_all [m/s] (list of floats):
            combined wind speeds across sensors
        wd_all [degree] (list of floats):
            combined wind directions across sensors
    '''
    
    if wind_syn_mode == 'scalar_mean':
        ws_all = list(df_ws.loc[:, df_ws.columns != colname_t].mean(axis=1))
        wd_all = list(df_wd.loc[:, df_wd.columns != colname_t].median(axis=1))
        return ws_all, wd_all
    
    elif wind_syn_mode == 'single':
        ws_all = df_ws[wind_sensor].to_list()
        wd_all = df_wd[wind_sensor].to_list()
        return ws_all, wd_all
    
    elif wind_syn_mode == 'vector_mean':
        ws_all, wd_all = [], []
        ws_list = df_ws.loc[:, df_ws.columns != colname_t].values.tolist()
        wd_list = df_wd.loc[:, df_wd.columns != colname_t].values.tolist()
        for x, y in zip(ws_list, wd_list):
            ws_avg, wd_avg = avgWindVector(x, y)
            ws_all.append(ws_avg); wd_all.append(wd_avg)
        return ws_all, wd_all
    
    elif wind_syn_mode == 'circular_mean':
        ws_all = list(df_ws.loc[:, df_ws.columns != colname_t].median(axis=1))
        wd_all = []
        wd_list = df_wd.loc[:, df_wd.columns != colname_t].values.tolist()
        for x in wd_list:
            wd_avg = avgWindDirection(x)
            wd_all.append(wd_avg)    
        return ws_all, wd_all
        
    else:
        raise NotImplementedError(">>>>> wind syn mode")
    


def avgWindVector(wind_speed_list, wind_direction_list):
    '''
    Calculate the average wind vector
    Input: 
        wind_speed_list: wind speed of the wind vectors to be averaged (unit in m/s)
        wind_direction_list: wind directions of the wind vectors to be averaged (unit in degree, 0 - 360)
    Output:
        wind_speed_avg: averaged wind speed (unit in m/s)
        wind_direction_avg: averaged wind direction (unit in degree, 0 - 360)
    '''
    
    # convert wind direction to theta which is defined as the angle between x-axis and the   vector (counter-clock wise is positive)
    
    thetas = [270-x for x in wind_direction_list]
    thetas = np.radians(thetas)
    x_list = [np.cos(theta)*l for l,theta in zip(wind_speed_list, thetas)]
    y_list = [np.sin(theta)*l for l,theta in zip(wind_speed_list, thetas)]
    #x_avg = np.nanmedian(x_list)
    #y_avg = np.nanmedian(y_list)
    x_avg = np.nanmean(x_list)
    y_avg = np.nanmean(y_list)
    wind_speed_avg = (x_avg**2 + y_avg**2)**(1/2)
    wind_direction_avg = np.arctan2(y_avg, x_avg)
    wind_direction_avg = wind_direction_avg *180 / np.pi
    wind_direction_avg = 270 - wind_direction_avg # convert back to cardinal definition
    if wind_direction_avg < 0:
        wind_direction_avg = wind_direction_avg + 360 
    elif wind_direction_avg >= 360:
        wind_direction_avg = wind_direction_avg - 360 
    else:
        pass
        
    
    return wind_speed_avg, wind_direction_avg

def avgWindDirection(wind_direction_list):
    '''
    Calculate the circular mean wind direction
    Input: 
        wind_direction_list: wind directions of the wind vectors to be averaged (unit in degree, 0 - 360)
    Output:
        wind_direction_avg: averaged wind direction (unit in degree, 0 - 360)
    '''
    
    # convert wind direction to theta which is defined as the angle between x-axis and the   vector (counter-clock wise is positive)
    
    thetas = [270-x for x in wind_direction_list]
    thetas = np.radians(thetas)
    x_list = [np.cos(theta) for theta in thetas]
    y_list = [np.sin(theta) for theta in thetas]
    #x_avg = np.nanmedian(x_list)
    #y_avg = np.nanmedian(y_list)
    x_avg = np.nanmedian(x_list) #checkpoint
    y_avg = np.nanmedian(y_list)
    wind_direction_avg = np.arctan2(y_avg, x_avg)
    wind_direction_avg = wind_direction_avg *180 / np.pi
    wind_direction_avg = 270 - wind_direction_avg # convert back to cardinal definition
    if wind_direction_avg < 0:
        wind_direction_avg = wind_direction_avg + 360 
    elif wind_direction_avg >= 360:
        wind_direction_avg = wind_direction_avg - 360 
    else:
        pass
    return wind_direction_avg
