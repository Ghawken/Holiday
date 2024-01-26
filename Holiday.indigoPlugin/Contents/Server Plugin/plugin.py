#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2022, Perceptive Automation, LLC. All rights reserved.
# https://www.indigodomo.com

import indigo

import logging
import os
import sys
import time
import holidays
from holidays import country_holidays
import pycountry
import traceback
import platform
import time as t
import platform
import sys
import os
from os import path
import datetime
from datetime import date

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process.

################################################################################
# New Indigo Log Handler - display more useful info when debug logging
# update to python3 changes
################################################################################
class IndigoLogHandler(logging.Handler):
    def __init__(self, display_name, level=logging.NOTSET):
        super().__init__(level)
        self.displayName = display_name

    def emit(self, record):
        """ not used by this class; must be called independently by indigo """
        logmessage = ""
        try:
            levelno = int(record.levelno)
            is_error = False
            is_exception = False
            if self.level <= levelno:  ## should display this..
                if record.exc_info !=None:
                    is_exception = True
                if levelno == 5:	# 5
                    logmessage = '({}:{}:{}): {}'.format(path.basename(record.pathname), record.funcName, record.lineno, record.getMessage())
                elif levelno == logging.DEBUG:	# 10
                    logmessage = '({}:{}:{}): {}'.format(path.basename(record.pathname), record.funcName, record.lineno, record.getMessage())
                elif levelno == logging.INFO:		# 20
                    logmessage = record.getMessage()
                elif levelno == logging.WARNING:	# 30
                    logmessage = record.getMessage()
                elif levelno == logging.ERROR:		# 40
                    logmessage = '({}: Function: {}  line: {}):    Error :  Message : {}'.format(path.basename(record.pathname), record.funcName, record.lineno, record.getMessage())
                    is_error = True
                if is_exception:
                    logmessage = '({}: Function: {}  line: {}):    Exception :  Message : {}'.format(path.basename(record.pathname), record.funcName, record.lineno, record.getMessage())
                    indigo.server.log(message=logmessage, type=self.displayName, isError=is_error, level=levelno)
                    if record.exc_info !=None:
                        etype,value,tb = record.exc_info
                        tb_string = "".join(traceback.format_tb(tb))
                        indigo.server.log(f"Traceback:\n{tb_string}", type=self.displayName, isError=is_error, level=levelno)
                        indigo.server.log(f"Error in plugin execution:\n\n{traceback.format_exc(30)}", type=self.displayName, isError=is_error, level=levelno)
                    indigo.server.log(f"\nExc_info: {record.exc_info} \nExc_Text: {record.exc_text} \nStack_info: {record.stack_info}",type=self.displayName, isError=is_error, level=levelno)
                    return
                indigo.server.log(message=logmessage, type=self.displayName, isError=is_error, level=levelno)
        except Exception as ex:
            indigo.server.log(f"Error in Logging: {ex}",type=self.displayName, isError=is_error, level=levelno)

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        ################################################################################
        # Setup Logging
        ################################################################################
        self.logger.setLevel(logging.DEBUG)
        try:
            self.logLevel = int(self.pluginPrefs["showDebugLevel"])
            self.fileloglevel = int(self.pluginPrefs["showDebugFileLevel"])
        except:
            self.logLevel = logging.INFO
            self.fileloglevel = logging.DEBUG

        self.logger.removeHandler(self.indigo_log_handler)

        self.indigo_log_handler = IndigoLogHandler(plugin_display_name, logging.INFO)
        ifmt = logging.Formatter("%(message)s")
        self.indigo_log_handler.setFormatter(ifmt)
        self.indigo_log_handler.setLevel(self.logLevel)
        self.logger.addHandler(self.indigo_log_handler)

        pfmt = logging.Formatter('%(asctime)s.%(msecs)03d\t%(levelname)s\t%(name)s.%(funcName)s:\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.plugin_file_handler.setFormatter(pfmt)
        self.plugin_file_handler.setLevel(self.fileloglevel)

        self.selected_region = plugin_prefs.get("region","")
        self.selected_country = plugin_prefs.get("country","")

        logging.getLogger("holidays").addHandler(self.plugin_file_handler)

        self.logger.info("{0:=^130}".format(" Initializing New Plugin Session "))
        self.logger.info("{0:<30} {1}".format("Plugin name:", plugin_display_name))
        self.logger.info("{0:<30} {1}".format("Plugin version:", plugin_version))
        self.logger.info("{0:<30} {1}".format("Plugin ID:", plugin_id))
        self.logger.info("{0:<30} {1}".format("Indigo version:", indigo.server.version) )
        self.logger.info("{0:<30} {1}".format("Silicon version:", str(platform.machine()) ))
        self.logger.info("{0:<30} {1}".format("Python version:", sys.version.replace('\n', '')))
        self.logger.info("{0:<30} {1}".format("Python Directory:", sys.prefix.replace('\n', '')))

        self.debug1 = self.pluginPrefs.get('debug1', False)
        self.debug2 = self.pluginPrefs.get('debug2', False)
        self.logger.info(u"{0:=^130}".format(" End Initializing New Plugin  "))

    ########################################
    def startup(self):
        self.logger.debug("startup called")

    def shutdown(self):
        self.logger.debug("shutdown called")

        ########################################
    def updateVar(self, name, value):
        self.logger.debug(u'updatevar run.')
        if not ('Holiday' in indigo.variables.folders):
            # create folder
            folderId = indigo.variables.folder.create('Holiday')
            folder = folderId.id
        else:
            folder = indigo.variables.folders.getId('Holiday')

        if name not in indigo.variables:
            NewVar = indigo.variable.create(name, value=str(value).lower(), folder=folder)
        else:
            indigo.variable.updateValue(name, str(value).lower())
        return

    def runConcurrentThread(self: indigo.PluginBase) -> None:
        """
        If runConcurrentThread() is defined, then a new thread is automatically created
        and runConcurrentThread() is called in that thread after startup() has been called.

        runConcurrentThread() should loop forever and only return after self.stopThread
        becomes True. If this function returns prematurely then the plugin host process
        will log an error and attempt to call runConcurrentThread() again after several seconds.

        :return: None
        """
        self.logger.debug(f"Run Concurrent Loop Called")
        current_day = datetime.datetime.now().strftime("%A")
        if self.selected_region != "" and self.selected_region != "":
            self.update_holidays()
        try:
            while True:
                new_day_of_week = datetime.datetime.now().strftime("%A")
                self.logger.debug(f"Server Day: {current_day}")
                if new_day_of_week != current_day:
                    self.update_holidays()
                    current_day = datetime.datetime.now().strftime("%A")
                self.sleep(5)

        except self.StopThread:
            pass  # Optionally catch the StopThread exception and do any needed cleanup.

    ########################################

    def show_holidays(self, *args, **kwargs):
        self.logger.debug(f"show_holidays called. {self.selected_region=} {self.selected_country=}")
        current_datetime = datetime.datetime.now()
        # Extract the year as an integer
        current_year = current_datetime.year
        if self.selected_region == "None":
            holidays = country_holidays(self.selected_country, subdiv=None, years=int(current_year))
        else:
            holidays = country_holidays(self.selected_country, subdiv=self.selected_region, years=int(current_year))
        self.logger.info(u"{0:=^130}".format(f" Holidays:  Country {self.selected_country}, Region {self.selected_region}  "))

        for day in holidays.items():
            actual_date, holiday_name = day
            self.logger.info(f"{holiday_name} is happening on {actual_date}")

        # Is today or tomorrow holiday
        today_holiday = date.today() in holidays
        tomorrow_holiday = (date.today() + datetime.timedelta(days=1)) in holidays
        self.logger.info(u"{0:=^130}".format(" Check Today / Tomorrow  "))
        self.logger.info(f"Is Today a Holiday: {today_holiday}")
        self.logger.info(f"Is Tomorrow a Holiday: {tomorrow_holiday}")
        self.logger.info(u"{0:=^130}".format("  "))

    def update_holidays(self, *args, **kwargs):
        try:
            self.logger.debug(f"update_holidays called.{self.selected_region=} {self.selected_country=} ")
            current_datetime = datetime.datetime.now()
            # Extract the year as an integer
            current_year = current_datetime.year
            if self.selected_region == "None":
                holidays = country_holidays(self.selected_country, subdiv=None, years=int(current_year))
            else:
                holidays = country_holidays(self.selected_country, subdiv=self.selected_region,  years=int(current_year))

            # Is today or tomorrow holiday
            today_holiday = date.today() in holidays
            tomorrow_holiday = (date.today() + datetime.timedelta(days=1)) in holidays
            self.logger.info(u"{0:=^130}".format(" Check Today / Tomorrow  "))
            self.logger.info(f"Is Today a Holiday: {today_holiday}")
            self.logger.info(f"Is Tomorrow a Holiday: {tomorrow_holiday}")
            self.updateVar("Holiday_Today", today_holiday)
            self.updateVar("Holiday_Tomorrow", tomorrow_holiday)
        except:
            self.logger.info("Error updating Holiday.  Please check selected countries/regions")
            self.logger.debug(f"Error updating", exc_info=True)

    def country_list_generator(self, filter="", valuesDict=None, typeId="", targetId=0):  # (self, *args, **kwargs):
        try:
            country_list = []
            list_codes = holidays.utils.list_supported_countries(include_aliases=False)
            self.logger.debug(f"{list_codes}")
            for code, region in list_codes.items():
               # self.logger.debug(f"{code} and {region}")
                a_country = pycountry.countries.get(alpha_2=str(code))
                # self.logger.info(f"{a_country}")
                self.logger.debug(f"{a_country.flag} {a_country.name} and code {code}")
                country_list.append( ( f"{code}",f"{a_country.flag} {a_country.name}") )
            return country_list

        except:
            self.logger.exception("")

    def region_list_generator(self, filter="", valuesDict=None, typeId="", targetId=0):  # (self, *args, **kwargs):
        try:
            self.logger.debug(f"Region_list_Generator {valuesDict=}")
            region_list = []
            region_list.append(("None","No Region" ) )
            list_codes = holidays.utils.list_supported_countries(include_aliases=False)
            for code, region in list_codes.items():
                if valuesDict["country"] == code:
                    #self.logger.debug(f"{code} and {region}")
                    a_country = pycountry.countries.get(alpha_2=str(code))
                    for reg in region:
                        region_list.append( ( f"{reg}",f"{a_country.flag} {reg}") )
                    return region_list

        except:
            self.logger.exception()
    ########################################
    def select_country(self, values_dict, type_id="", dev_id=None):
        self.logger.debug(u"select_countrycalled")
        self.logger.debug("Select Country Called and ValuesDict:\n{}".format(values_dict))
        self.selected_country = values_dict["country"]
        self.selected_region = values_dict['region']
        return values_dict

    def select_region(self, values_dict, type_id="", dev_id=None):
        self.logger.debug(u"select_region")
        self.logger.debug("Select Device Called and ValuesDict:\n{}".format(values_dict))
        self.selected_country = values_dict["country"]
        self.selected_region = values_dict['region']
        return values_dict

    # deviceStartComm() is called on application launch for all of our plugin defined

    ########################################
    def validateDeviceConfigUi(self, values_dict, type_id, dev_id):
        return (True, values_dict)

    ########################################

