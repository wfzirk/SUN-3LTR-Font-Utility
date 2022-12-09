
@echo off
rem must change system language locale to utf-8
rem https://www.bing.com/search?q=administrative+language+setting+win+10&form=WNSGPH&qs=AS&cvid=7b4667c3e2804c078bbfa20f11d7eb9f&pq=administrative+language+s&cc=US&setlang=en-US&nclid=5DAC70C3F9718B3FD01438C3459AFE25&ts=1581894742795&wsso=Moderate

Setlocal EnableDelayedExpansion


if not exist Dist mkdir Dist
if not exist Log mkdir Log
if not exist Svg mkdir Svg

call doEnv.bat


@echo off

echo ============================
:: if inpput file extension is kmn then do kmn2csv
:: else do csv2kmn
::set extension=%langin:*.=%
::@echo "file extension" %extension%
::if %extension% == ods (echo ods found)
::if %extension% == kmn (echo kmn found)

::====================================
set engalias=%alias%
if %alias% == EN set engalias=EN
if %alias% == eng set engalias=EN
if %alias% == ENG set engalias=EN
if %engalias% == EN (
	echo This is not for the English build
	goto end
)

:doit

set docmd=%1

@echo executing *%docmd%*

if %docmd% == all (goto all) 

goto %docmd%
.

:all    
@echo check kmn kmn = %kmn%
@echo check csv langin = %langin%

::if %kmn% == "" (goto csv2kmn)

:kmn2csv
	if "%kmn%" NEQ "" (
		@echo on
		echo in kmn2csv
		cmd /c fontforge -quiet -script kmn2csv.py "%kmn%" dist/kmn%ver%_%alias%.csv
		@echo off
		if ERRORLEVEL 1 (goto errorexit)
		
	)
)    
if %docmd%  NEQ all (goto end)

:: only kmn2csv or csv2kmn not both


:csv2kmn
	echo "----------|%langin%|============="
	if "%langin%" NEQ "" (
		@echo on
		echo in csv2kmn
		cmd /c fontforge -quiet -script csv2kmn.py %langin% %langaltin%  dist\sun%ver%_%alias%.kmn
		@echo off
		if ERRORLEVEL 1 (goto errorexit)
	)
if %docmd%  NEQ all (goto end)

:csv2svg
	@echo on
	echo in csv2svg
	if "%langin%" == "" (set langin="dist/kmn%ver%_%alias%.csv")
	cmd /c fontforge -quiet -script csv2svg.py %langin% %ttffont%
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
	
if %docmd%  NEQ all (goto end)

:svg2font
	@echo on
	echo in svg2font
	if "%langin%" == "" (set langin="dist/kmn%ver%_%alias%.csv")
	cmd /c fontforge -quiet -script svg2Font.py %langin% %ttffont% %alias% dist/SUNBF%ver%_%alias%
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
if %docmd%  NEQ all (goto end)

rem following are for documentation and verification
:back2doc
	@echo on
	echo in back2doc
	if "%langin%" == "" (set langin="dist/kmn%ver%_%alias%.csv")
	cmd /c fontforge -quiet -script back2doc.py %langin% dist/back%ver%_%alias%.txt 
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
if %docmd%  NEQ all (goto end)

:compact
	@echo on
	echo in compact
	if "%langin%" == "" (set langin="dist/kmn%ver%_%alias%.csv")
	cmd /c fontforge -quiet -script compact4x16.py %langin% dist/compact%ver%_%alias%.pdf
	@echo off
	if ERRORLEVEL 1 (goto errorexit)	
if %docmd%  NEQ all (goto end)

:bfzip
	@echo on
	echo in bfzip
	if "%langin%" == "" (set langin="dist/kmn%ver%_%alias%.csv")
	copy Input\*.ttf Dist
	cmd /c fontforge -quiet -script bfZip.py
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
if %docmd%  NEQ all (goto end)

goto end

:errorexit
@echo on
@echo quit because of errors
@echo quit with error = %errorlevel%
@echo off
goto end


:end

@echo Done


