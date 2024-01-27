# Holiday Plugin

![https://github.com/Ghawken/Holiday/blob/main/Images/holiday.png?raw=true](https://github.com/Ghawken/Holiday/blob/main/Images/holiday.png?raw=true)

This is a relatively simple plugin (well aren't they all?) which allows you to select country and region, and then will update a variable as to whether today or tomorrow is a Holiday

It basically is a wrapper for the python-holidays library which collates this information for multiple countries/regions.

see here:
https://pypi.org/project/holidays/

## Install

Only compatible with Indigo 2023.2 - as it can now download the 2 libraries needed - one of which is obviously the holidays package

Double click plugin Bundle

## Plugin Config Settings Only

![https://github.com/Ghawken/Holiday/blob/main/Images/PluginConfig.png?raw=true](https://github.com/Ghawken/Holiday/blob/main/Images/PluginConfig.png?raw=true)

![https://github.com/Ghawken/Holiday/blob/main/Images/countries.png?raw=true](https://github.com/Ghawken/Holiday/blob/main/Images/countries.png?raw=true)

#### Select Country and/or Region

To check Holidays that plugin is aware of can run Menu item
Log all Holidays once these details are selected.

eg.
``` 
Holiday                         =============================================== Holidays:  Country GB, Region ENG  ===============================================
   Holiday                         Good Friday is happening on 2024-03-29
   Holiday                         May Day is happening on 2024-05-06
   Holiday                         Spring Bank Holiday is happening on 2024-05-27
   Holiday                         New Year's Day is happening on 2024-01-01
   Holiday                         Christmas Day is happening on 2024-12-25
   Holiday                         Boxing Day is happening on 2024-12-26
   Holiday                         Easter Monday is happening on 2024-04-01
   Holiday                         Late Summer Bank Holiday is happening on 2024-08-26
   Holiday                         ==================================================== Check Today / Tomorrow  =====================================================
   Holiday                         Is Today a Holiday: False
   Holiday                         Is Tomorrow a Holiday: False
   Holiday                         ================================================================  ================================================================
```
eg.
```
   Holiday                         ========================================== Holidays:  Country NL, Region None, Lang nl  ==========================================
   Holiday                         Nieuwjaarsdag is happening on Mon January 1 2024, which is -26 days away
   Holiday                         Eerste paasdag is happening on Sun March 31 2024, which is 64 days away
   Holiday                         Tweede paasdag is happening on Mon April 1 2024, which is 65 days away
   Holiday                         Koningsdag is happening on Sat April 27 2024, which is 91 days away
   Holiday                         Hemelvaartsdag is happening on Thu May 9 2024, which is 103 days away
   Holiday                         Eerste Pinksterdag is happening on Sun May 19 2024, which is 113 days away
   Holiday                         Tweede Pinksterdag is happening on Mon May 20 2024, which is 114 days away
   Holiday                         Eerste Kerstdag is happening on Wed December 25 2024, which is 333 days away
   Holiday                         Tweede Kerstdag is happening on Thu December 26 2024, which is 334 days away
   Holiday                         ==================================================== Check Today / Tomorrow  =====================================================
   Holiday                         Is Today a Holiday: False
   Holiday                         Is Tomorrow a Holiday: False
   Holiday                         ================================================================  ================================================================

```

Thats it.

There will be a variable called
Holiday_Today:  true or false
Holiday_Tomorrow: true or false
in folder Holidays

This will be updated once a day/and/or on startup or any issues.

## Usage

As a conditional trigger for schedules etc. to run

Alarm clock:
Condition:
If Holiday_Today is false


## Check the holidays listed

I have found that it is very good, but there is one 'Bank Holiday' it lists for me which isn't a 'public holiday'.  
Was a bit slow to work that day when alarm didn't go off.... not completely sure anyone understood my excuse!