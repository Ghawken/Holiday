#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
import indigo
installation_output = ""
try:
    from auto_installer import update_holidays
    installation_output = update_holidays()
except:
    pass

import logging
import holidays

from holidays import country_holidays
import pycountry
import traceback
import platform
import sys
from os import path
import datetime
from datetime import date

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
        global installation_output
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
        self.selected_lang = plugin_prefs.get("language","")
        self.selected_category = plugin_prefs.get("category","public")
        self.debug1 = plugin_prefs.get("debug1", False)

        logging.getLogger("holidays").addHandler(self.plugin_file_handler)

        if installation_output !="":
            self.packages_installed = True
            self.logger.debug(f"Holidays Updated:\n{installation_output}")

        system_version, product_version, longer_name = self.get_macos_version()
        self.logger.info("{0:=^130}".format(f" Initializing New Plugin Session for Plugin: {plugin_display_name} "))
        self.logger.info("{0:<30} {1}".format("Plugin name:", plugin_display_name))
        self.logger.info("{0:<30} {1}".format("Plugin version:", plugin_version))
        self.logger.info("{0:<30} {1}".format("Plugin ID:", plugin_id))
        self.logger.info("{0:<30} {1}".format("Indigo version:", indigo.server.version) )
        self.logger.info("{0:<30} {1}".format("System version:", f"{system_version} {longer_name}" ))
        self.logger.info("{0:<30} {1}".format("Product version:", product_version))
        self.logger.info("{0:<30} {1}".format("Silicon version:", str(platform.machine()) ))
        self.logger.info("{0:<30} {1}".format("Holidays Library version:", str(holidays.__version__)))
        self.logger.info("{0:<30} {1}".format("Python version:", sys.version.replace('\n', '')))
        self.logger.info("{0:<30} {1}".format("Python Directory:", sys.prefix.replace('\n', '')))

        self.debug1 = self.pluginPrefs.get('debug1', False)
        self.debug2 = self.pluginPrefs.get('debug2', False)
        self.logger.info(u"{0:=^130}".format(" End Initializing New Plugin  "))

    ########################################
    def get_macos_version(self):
        try:
            version, _, _ = platform.mac_ver()
            longer_version = platform.platform()
            self.logger.info(f"{version}")
            longer_name = self.get_macos_marketing_name(version)
            return version, longer_version, longer_name
        except:
            self.logger.debug("Exception:",exc_info=True)
            return "","",""

    def get_macos_marketing_name(self, version: str) -> str:
        """Return the marketing name for a given macOS version number."""
        versions = {
            "10.0": "Cheetah",
            "10.1": "Puma",
            "10.2": "Jaguar",
            "10.3": "Panther",
            "10.4": "Tiger",
            "10.5": "Leopard",
            "10.6": "Snow Leopard",
            "10.7": "Lion",
            "10.8": "Mountain Lion",
            "10.9": "Mavericks",
            "10.10": "Yosemite",
            "10.11": "El Capitan",
            "10.12": "Sierra",
            "10.13": "High Sierra",
            "10.14": "Mojave",
            "10.15": "Catalina",
            "11": "Big Sur",  # Just use the major version number for macOS 11+
            "12": "Monterey",
            "13": "Ventura",
            "14": "Sonoma",
        }
        major_version_parts = version.split(".")
        # If the version is "11" or later, use only the first number as the key
        if int(major_version_parts[0]) >= 11:
            major_version = major_version_parts[0]
        # For macOS "10.x" versions, use the first two numbers as the key
        else:
            major_version = ".".join(major_version_parts[:2])
        self.logger.debug(f"Major Version== {major_version}")
        return versions.get(major_version, f"Unknown macOS version for {version}")

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
        if self.selected_country != "" and self.selected_region != "":
            self.update_holidays()
        try:
            while True:
                new_day_of_week = datetime.datetime.now().strftime("%A")
                if new_day_of_week != current_day:
                    self.update_holidays()
                    current_day = new_day_of_week
                self.sleep(60)

        except self.StopThread:
            pass  # Optionally catch the StopThread exception and do any needed cleanup.

    ########################################

    def show_holidays(self, *args, **kwargs):
        self.logger.debug(f"show_holidays called. {self.selected_region=} {self.selected_country=} {self.selected_category=} {self.selected_lang=}")
        try:
            current_datetime = datetime.datetime.now()
            current_year = current_datetime.year

            language_to_use = None
            if self.selected_lang != "" or self.selected_lang != "Default":
                language_to_use = self.selected_lang

            category_to_use= self._get_category_tuple()
            self.logger.debug(f"Using Category {category_to_use}")

            if self.selected_region == "None" or self.selected_region == "":
                holidays = country_holidays(self.selected_country, subdiv=None, categories=category_to_use, language=language_to_use, years=int(current_year))
            else:
                holidays = country_holidays(self.selected_country, subdiv=self.selected_region, categories=category_to_use, language=language_to_use,  years=int(current_year))

            a_country = pycountry.countries.get(alpha_2=str(self.selected_country))
            self.logger.info(u"{0:=^160}".format(f" Holidays:  Country: {a_country.flag}{a_country.flag} {a_country.name} {a_country.flag}{a_country.flag}, Region: {self.selected_region}, Lang: {self.selected_lang}, Categories: {category_to_use} "))

            for day in holidays.items():
                actual_date, holiday_name = day
                self.logger.info(f"{holiday_name} is happening on {actual_date.strftime('%a %B %-d %Y')}, which is {(actual_date - datetime.datetime.now().date()).days} days away")

            # Is today or tomorrow holiday
            today_holiday = date.today() in holidays
            tomorrow_holiday = (date.today() + datetime.timedelta(days=1)) in holidays
            self.logger.info(u"{0:=^160}".format(" Check Today / Tomorrow  "))
            self.logger.info(f"Is Today a Holiday: {today_holiday}")
            self.logger.info(f"Is Tomorrow a Holiday: {tomorrow_holiday}")
            self.logger.info(u"{0:=^160}".format(""))
        except:
            self.logger.exception("Caught Exception with Show Holidays")
    def _get_category_tuple(self):
        # Check if `self.selected_category` is not empty
        if self.selected_country =="":
            self.logger.debug("No selected country, returning default.")
            return ("public")
        if self.selected_category:
            # Split by comma, strip whitespace from each item, and filter out any empty strings
            category_to_use = tuple(item.strip() for item in self.selected_category if item.strip())
        else:
            # If `self.selected_category` is empty, return an public default tuple
            category_to_use = ("public")
        return category_to_use

    def update_holidays(self, *args, **kwargs):
        try:
            self.logger.debug(f"update_holidays called.{self.selected_region=} {self.selected_country=} ")
            current_datetime = datetime.datetime.now()
            # Extract the year as an integer
            current_year = current_datetime.year
            language_to_use = None
            if self.selected_lang != "" or self.selected_lang != "Default":
                language_to_use = self.selected_lang

            category_to_use = self._get_category_tuple()
            self.logger.debug(f"Using Category {category_to_use}")

            if self.selected_region == "None" or self.selected_region == "":
                holidays = country_holidays(self.selected_country, subdiv=None, categories=category_to_use, language=language_to_use, years=int(current_year))
            else:
                holidays = country_holidays(self.selected_country, subdiv=self.selected_region, categories=category_to_use, language=language_to_use, years=int(current_year))

            a_country = pycountry.countries.get(alpha_2=str(self.selected_country))
            self.logger.info(u"{0:=^160}".format(f" Holidays:  Country: {a_country.flag}{a_country.flag} {a_country.name} {a_country.flag}{a_country.flag}, Region: {self.selected_region}, Lang: {self.selected_lang}, Categories: {category_to_use} "))

            # Is today or tomorrow holiday
            today_holiday = date.today() in holidays
            tomorrow_holiday = (date.today() + datetime.timedelta(days=1)) in holidays

            self.logger.info(u"{0:=^160}".format(" Check Today / Tomorrow  "))
            self.logger.info(f"Is Today a Holiday: {today_holiday}")
            self.logger.info(f"Is Tomorrow a Holiday: {tomorrow_holiday}")
            self.updateVar("Holiday_Today", today_holiday)
            self.updateVar("Holiday_Tomorrow", tomorrow_holiday)
            self.logger.info(u"{0:=^160}".format(" Variables Updated  "))
        except:
            self.logger.info("Error updating Holiday.  Please check selected countries/regions")
            self.logger.debug(f"Error updating", exc_info=True)

    def country_list_generator(self, filter="", valuesDict=None, typeId="", targetId=0):  # (self, *args, **kwargs):
        try:
            country_list = []
            list_codes = holidays.utils.list_supported_countries(include_aliases=False)
            #self.logger.debug(f"{list_codes}")
            for code, region in list_codes.items():
               # self.logger.debug(f"{code} and {region}")
                a_country = pycountry.countries.get(alpha_2=str(code))
                # self.logger.info(f"{a_country}")
                #self.logger.debug(f"{a_country.flag} {a_country.name} and code {code}")
                country_list.append( ( f"{code}",f"{a_country.flag} {a_country.name}") )
            return country_list

        except:
            self.logger.exception("")
    def lang_list_generator(self, filter="", valuesDict=None, typeId="", targetId=0):  # (self, *args, **kwargs):
        try:
            if self.debug1:
                self.logger.debug(f"Lang List Generator {valuesDict}")

            if self.selected_country == "":
                self.logger.debug("Select Country first")
                return ("No Country Selected", "No Country Selected")

            lang_list = []
            lang_list.append(("Default","Default" ) )
            list_codes = holidays.utils.list_localized_countries(include_aliases=False)
            for code, region in list_codes.items():
                if str(valuesDict["country"]) == str(code):
                    a_country = pycountry.countries.get(alpha_2=str(code))
                    for reg in region:
                        #self.logger.debug(f"{reg}")
                        lang_list.append( ( f"{reg}",f"{a_country.flag} {reg}") )
            return lang_list

        except:
            self.logger.exception("Exception:")
    def log_holidays(self, values_dict):
        if self.debug1:
            self.logger.debug(f'log Holidays, {values_dict}')
        self.selected_country = values_dict["country"]
        self.selected_lang = values_dict['language']
        self.selected_region = values_dict['region']
        self.selected_category = values_dict['category']
        self.show_holidays()

    def category_list_generator(self, filter="", valuesDict=None, typeId="", targetId=0):  # (self, *args, **kwargs):
        try:
            self.logger.debug(f"Category List Generator {valuesDict=}")

            if self.selected_country == "":
                self.logger.debug("Select Country first")
                return ("No Country Selected", "No Country Selected")

            current_datetime = datetime.datetime.now()
            current_year = current_datetime.year
            cat_list = []
            categories = country_holidays(self.selected_country, years=int(current_year)).supported_categories
            self.logger.debug(f"{categories=}")

            for cat in categories:
                cat_list.append( ( f"{cat}",f"{cat}") )
            return cat_list

        except:
            self.logger.exception("Exception:")
    def region_list_generator(self, filter="", valuesDict=None, typeId="", targetId=0):  # (self, *args, **kwargs):
        try:
            self.logger.debug(f"Region_list_Generator {valuesDict=}")
            if self.selected_country == "":
                self.logger.debug("Select Country first")
                return ("No Country Selected", "No Country Selected")
            region_list = []
            region_list.append(("None","No Region" ) )
            list_codes = holidays.utils.list_supported_countries(include_aliases=False)
            for code, region in list_codes.items():
                if valuesDict["country"] == code:
                    if self.debug1:
                        self.logger.debug(f"{code} and {region}")
                    a_country = pycountry.countries.get(alpha_2=str(code))
                    for reg in region:
                        a_region = pycountry.subdivisions.get( code=str(f"{valuesDict['country']}-{reg}") )
                        a_region_name = reg
                        if a_region != None:
                            a_region_name = a_region.name
                        if self.debug1:
                            self.logger.debug(f"Region Naming: {a_region_name}")
                        region_list.append( ( f"{reg}",f"{a_country.flag} {a_region_name}") )
            return region_list

        except:
            self.logger.exception("Exception")
    ########################################
    def select_country(self, values_dict, type_id="", dev_id=None):
        self.logger.debug(u"select_countrycalled")
        if self.debug1:
            self.logger.debug("Select Country Called and ValuesDict:\n{}".format(values_dict))
        self.selected_country = values_dict["country"]
        self.selected_region = ""
        self.selected_lang = ""
        self.selected_category = ""
        values_dict["category"] = "public"
        return values_dict

    def select_lang(self, values_dict, type_id="", dev_id=None):
        self.logger.debug(u"select_region")
        if self.debug1:
            self.logger.debug("Select Device Called and ValuesDict:\n{}".format(values_dict))
        self.selected_country = values_dict["country"]
        self.selected_lang = values_dict['language']
        self.selected_category = ""
        return values_dict

    def select_region(self, values_dict, type_id="", dev_id=None):
        self.logger.debug(u"select_region")
        if self.debug1:
            self.logger.debug("Select Device Called and ValuesDict:\n{}".format(values_dict))
        self.selected_country = values_dict["country"]
        self.selected_region = values_dict['region']
        return values_dict

    def select_category(self, values_dict, type_id="", dev_id=None):
        self.logger.debug(u"select_category")
        if self.debug1:
            self.logger.debug("Select Device Called and ValuesDict:\n{}".format(values_dict))
        self.selected_category = values_dict['category']
        return values_dict

    # deviceStartComm() is called on application launch for all of our plugin defined

    ########################################
    def validateDeviceConfigUi(self, values_dict, type_id, dev_id):
        return (True, values_dict)

    ########################################
    def closedPrefsConfigUi(self, valuesDict, userCancelled):
        self.debugLog(u"closedPrefsConfigUi() method called.")

        if userCancelled:
            self.debugLog(u"User prefs dialog cancelled.")

        if not userCancelled:
            self.debugLevel = valuesDict.get('showDebugLevel', "10")
            self.debugLog(u"User prefs saved.")

            #self.logger.error(str(valuesDict))

            try:
                self.logLevel = int(valuesDict[u"showDebugLevel"])
            except:
                self.logLevel = logging.INFO

            self.indigo_log_handler.setLevel(self.logLevel)
            self.logger.debug(u"logLevel = " + str(self.logLevel))
            self.logger.debug(u"User prefs saved.")
            self.logger.debug(u"Debugging on (Level: {0})".format(self.debugLevel))

            self.debug1 = valuesDict.get('debug1', False)

            if self.selected_country !="":
                self.update_holidays()
        return True
