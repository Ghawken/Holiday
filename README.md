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

Go to Plugin Config

Select Country, Region, language and/or categories of holidays (beware some of these are 'public' holidays which is default)

Press log Holidays to see what holidays are registered, recorded for checking

To check Holidays that plugin is aware of can run Menu item
Log all Holidays once these details are selected.

eg.
``` 
   Holiday                         =================== Holidays:  Country: 🇳🇿🇳🇿 New Zealand 🇳🇿🇳🇿, Region: None, Lang: Default, Categories: public ===================
   Holiday                         New Year's Day is happening on Mon January 1 2024, which is -26 days away
   Holiday                         Day after New Year's Day is happening on Tue January 2 2024, which is -25 days away
   Holiday                         Waitangi Day is happening on Tue February 6 2024, which is 10 days away
   Holiday                         Anzac Day is happening on Thu April 25 2024, which is 89 days away
   Holiday                         Good Friday is happening on Fri March 29 2024, which is 62 days away
   Holiday                         Easter Monday is happening on Mon April 1 2024, which is 65 days away
   Holiday                         King's Birthday is happening on Mon June 3 2024, which is 128 days away
   Holiday                         Matariki is happening on Fri June 28 2024, which is 153 days away
   Holiday                         Labour Day is happening on Mon October 28 2024, which is 275 days away
   Holiday                         Christmas Day is happening on Wed December 25 2024, which is 333 days away
   Holiday                         Boxing Day is happening on Thu December 26 2024, which is 334 days away
   Holiday                         ==================================================== Check Today / Tomorrow  =====================================================
   Holiday                         Is Today a Holiday: False
   Holiday                         Is Tomorrow a Holiday: False
   Holiday                         ================================================================  ================================================================
```
eg.
```
   Holiday                         ============== Holidays:  Country: 🇳🇱🇳🇱 Netherlands 🇳🇱🇳🇱, Region: None, Lang: Default, Categories: optional, public ==============
   Holiday                         Goede Vrijdag is happening on Fri March 29 2024, which is 62 days away
   Holiday                         Bevrijdingsdag is happening on Sun May 5 2024, which is 99 days away
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

## Action Group

Enables forcing Holiday Today or Holiday Tomorrow to True or False, or return to Library default settings.  This overrides the library settings.

This is saved, and survives Indigo or Plugin restarts.  So to reset rerun the action setting as needed.

Setting Holiday tomorrow to True, sets the variable Holiday_tomorrow to true, at midnight Holiday_tomorrow becomes false, and Holiday_today is then 
also forced true.  Another day passes and they are both negative (if no real holiday)

### Usage:
Ideally would suggest Force Holiday tomorrow is used day before actual holiday so triggers early in day are caught
eg.
Button press for temporary holiday, at midnight Holiday_Today becomes true and if using for scheduled alarm - then appropriate morning routine not triggered.





## Usage

As a conditional trigger for schedules etc. to run

Alarm clock:
Condition:
If Holiday_Today is false


## Check the holidays listed

I have found that it is very good, but there is one 'Bank Holiday' it lists for me which isn't a 'public holiday'.  
Was a bit slow to work that day when alarm didn't go off.... not completely sure anyone understood my excuse!