**Instructions for FontForge scripts as of SUN version 921\_722**

22 July 2021

These scripts are written in python using the python version 3.8 imbedded in FontForge.

They were written on a windows PC but they should work on Linux, I would guess there may be some changes on directory and file handling.

Objective:

`	`Generate backfonts and documentation for the different versions of SUN.

Requirements:

- FontForge 2020-03-14:  <https://fontforge.org/en-US/>

`	`Fontforge python documentation <https://fontforge.org/python.html>

- potrace:  potrace is part of fontforge.
- Imagemagick:  <https://imagemagick.org/index.php>
- For creating spreadsheets in ods format install xlswriter:

`	`Instructions for installing xlswriter:

- open command prompt as admin
- cd to fontforgebuilds dir
- execute fontforge-console
- execute ffpython -m pip install --upgrade pip --force-reinstall
- execute pip install xlsxwriter
-  execute ffpython -m pip install xlsxwriter

- (not implemented yet) For creating pdf files with the fonts created by Fontforge, then the font needs to be loaded into the workdirectory.   [Fontloader](https://www.trishtech.com/2018/11/load-fonts-temporarily-in-windows-through-command-line-interface/) has a cli version that loads fonts temporally into windows.  It can be downloaded here [Fontloader download](https://www.trishtech.com/downloads/fontloader-command-line.zip).



- Change terminal codepage to UTF-8

<https://stackoverflow.com/questions/57131654/using-utf-8-encoding-chcp-65001-in-command-prompt-windows-powershell-window>

- from Windows 10 run → intl.cpl
- Adminstrative Tab
- Change system locale
- Check Beta: Use Unicode UTF-8 for world wide language support
- Select OK
- Restart
- Note: if this procedure is not acceptable read the above webpage for options

Product::

- English primary dictionary from sfd  – pw(Ver)\_EN.ods
- Backfont from primary dictionary		
- English dictionary from kmn file
- Language backfont and dictionary from primary words
- kmn from dictionary
- All language primary merged from Language dictionary and English primary
- Language dictionaries sorted by name or language name.

Problems found with Language dictionaries:

- Missing words:  The language dictionary may not be up to date with the current English dictionary.  The language field will be left blank
- Duplicate words in language dictionaries different unicodes.  These are language words which translate the same from different English words.  The first word in the list will be used.  The field will be blank for the second word since Sun can’t use the same name for different unicodes.
- Unicodes with o instead of 0.  These have to be manually fixed.
- Unicode miscompares with down level dictionaries.  The unicode from the Enflish primary list will be used.
- Words with spaces.  The spaces are replaced with  '\_' (underscore)

**Setup:**  

Install Fontforge and Imagemagick per default.

Create a work directory containing all the python scripts and config files.

From the work directory create Log, Dist, Input and Svg directories

`	`The Log directory keeps all the log files of the code run

`	`The Dist directory keeps the files for distribution.  A complete run will create a zip  	file containing the files to be distributed.

`	`Place all files used for input in the Input directory.  i.e.  sfd, kmn, dictionary, 			times.ttf.

`	`The Svg directory contains the svg images for the backfont file.

**Running Scripts:**

Open a Command Prompt window and change to the directory where your code is.

A basic FontForge command is.

`	`fontforge  -script pythonscript.py ...params….

Most of the function names should be self explanatory, however some variable  names may not be quite so obvious.

The order of running the scripts is important.  They should be executed in the

following order:

`	`kmn2csv, sfd2csv, csv2svg – other files in any order.. bfZip last

`	`For language files:  kmn2csv and sfd2csv must have been run in English first

`		`langpri, csv2kmn csv2svg – other files in any order… bfZip last

You can always contact me for an explanation of the code.

**BackFont Procedures:**

`	`The requirements to generate scripts

`		`The FontForge – xxxx.sfd file provided by Ernie.

`		`The Keyman – xxx.kmn file provided by Ernie.

`		`Times.ttf – The font file used for generating the backfont images.  This can be 				extracted from the window pc

`	`If another language is to be created:

A dictionary containing the English and language equivalent columns along with

the uni-codes and symbols columns needs to be copied to the Input directory

along with the English Primary dictionary.  

The version should be set to the same version as the English primary dictionary

to get file naming convention right.

`	`The order of the columns of the dictionary is important.  I no longer try to figure out the

`		`the order.  The order for english  is:  symbol, name, unicode, reference.



`		`If it is another language the order is: symbol, englishname, languagename, 			unicode, reference

`	`The sfd file contains the symbols and unicodes for the primary words and is used to 		generate the list of primary words



`	`The kmn file contains the primary words and the synonyms of primary words along with  	their unicodes.



**Scripts:**

`	`**bfsetup.bat** – This is a batch file sets up the environment for running the **doeng.ba**t 	and **dolang.bat**.

`	`This is a GUI program for setting up the variables in **doEnv.bat**.  Easier than typing in 		an editor.

`	`The bfsetup file will enable or disable fields depending on if it is English or another 	language.

`	`The input field above the language list allows typing and searching for language. i.e. 	eng.  

`	`**doeng.bat, dolang.bat** – This is a batch file executing all the scripts.

`		`**Doeng.bat** for the english translation, **dolang.bat** for other languages.

`		`Herein refered as **doxxx**

`		`Execution parms

`			`parms is either “doall” or the name of the python script without the 					extention.

`		`i.e. doxx all

`		`i.e. doxxl sfd2csv



`		`Look at the doxxx  file to see how commands are executed.

`		`The doall.bat file uses the environment variables from **doEnv.bat**

set sfd=Input/Sun22\_02\_25.sfd

set kmn=Input/sun22\_02\_25.kmn

set ver=220225

set ttffont=/Input/times.ttf

set alias=FRA

set langaltin=Input/dict\_list\_alt1\_POR.csv

set langin=/Input/dict\_list\_POR.xlsx

set langout=SUNBF220225\_POR.sfd



This batch file will generate all files and documents into a complete package.

`		`It can also by  passing the python file name execute only that one file.

**Language Lists** – Iso639 language lists can be downloaded and to get the 3 or 4 letter  		acronym for the language used.  If English (ENG) then primary word lists will be 		generated as well as a backfont requiring a kmn file and a dictionary.  If other 		than English then either a kmn file or a dictionary file is required to generate the 		backfont.

`	`**config.json** – This contains variables and lists  for each language and may 				eventually be rewritten as more languages are built.

`	`**bfConfig.py** – updates and reads the config.json file.

`	`**util.py** – contains some common functions used in all the code

`	`**bfLog.py** – sets up the logging.

`		`Filename.log – contains logging at the INFO level.  It can be modified

`		`to other levels of logging

`	`**array2xlsx.py** – This script will generate xlsx files from arrays which are then 			converted to ods files.  This script program automatically resizes the 			spreadsheet 	columns formats to make into a pdf 	

`	`**The following files are the work files.**  

`		`The **doeng.ba**t and **dolang.bat** files show how the commands are executed.

**sfd2csv.py** – This script takes the sfd file and generates  **pw%ver%\_%alias%.csv**  file 	containing a list of	primary words.  This csv file is used in most of the other 	scripts.

**kmn2csv.py** – This script takes the keyman kmn  file and generates  kmnSUN**%ver	%\_%alias%.csv**  file which contains he complete dictionary.

**alternative.py** – This script takes the kmncsv file and the pwcsv  file and generates  

`	`**alt**%**ver%\_%alias%.csv**  file which contains he complete dictionary.

~~**n**l**angpri.py** – This script takes **pw%ver%\_%alias%.csv** and the **“language.csv”** file 		to generate**lpw%ver%\_%alias%.csv**.~~

**csv2kmn.py** – This scripts takes the language primary words file and creates a kmn 	file.  This will work on any sun dictionary file to create a kmn file.

**csv2svg.py** – Takes the pw%ver%\_%alias%.csv file and generates an image of each 	word as a svg file.

**svg2Font.py** – Uses the svg files from the previous script to import into the	 	backfont sfd 	file.  It also creates a ttf and woff file.

AT this point the generated ttf file needs to be installed in the PC if PDF files are created.

On windows right clicking on the file should give an option to install it.

The following scripts generate documents and spreadsheets for the version of SUN

**back2doc.py** – This creates a text file for the purpose of verifying the quality of the 	backfont.  Glancing through the file will show anomalies to be corrected. Either 	missing or overlayed or out of alignment words.


**compact4x16.py** – This generates **compact%ver%\_%lang%.ods and compact%ver	%\_%alias%.pdf**  which gives a 4 column list of the glyphs on a page.

**bfZip.py** – Packages the distribution files  into a zip file.

**bfsetup.py** – This is a dialog for easily setting up the **doEnv.bat** file for use by the 	**doeng.bat** and **dolang.bat** files.  This will run any or all the scripts.

~~**bfmain.py** – This can replace the **doall.bat** file for manual running.  It makes 	debugging and viewing of run results in a friendlier manner than the text files.~~

`	`~~It will modify the **doEnv.bat** and **config.json** files.  This is executed by calling 	**bf.bat**~~

**Diagnostics**

These are diagnostic files generated to show mismatches and missing unicodes and words.

**name\_has\_spaces.txt** - This file will list words that have spaces and can not be in the list

**name\_not\_used.tx**t -	This is a word in the primary dictionary not in the language dictionary

~~**not\_in\_primary.tx**t – This is a word in the language dictionary not in the primary dictionary~~

~~**unicode\_mismatch** – This lists words that have different unicodes between the English dictionary vs the language dictionary~~

