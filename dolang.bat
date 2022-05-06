rem must change system language locale to utf-8
rem https://www.bing.com/search?q=administrative+language+setting+win+10&form=WNSGPH&qs=AS&cvid=7b4667c3e2804c078bbfa20f11d7eb9f&pq=administrative+language+s&cc=US&setlang=en-US&nclid=5DAC70C3F9718B3FD01438C3459AFE25&ts=1581894742795&wsso=Moderate

Setlocal EnableDelayedExpansion
set debugecho=off

if not exist Dist mkdir Dist
if not exist Log mkdir Log
if not exist Svg mkdir Svg


call doEnv.bat

set engalias=%alias%
if %alias% == EN set engalias=EN
if %alias% == eng set engalias=EN
if %alias% == ENG set engalias=EN
if %engalias% == EN (
	echo This is not for the English build
	goto end
)

:doit

if %1.== all (goto dolang)

set docmd=%1
@echo executing *%docmd%* 
goto %docmd%

echo on
echo %debugecho%


:dolang

if %docmd% == all (goto backfont) else (goto %docmd%)
echo "shouldn't be here"
goto end

:all


:csv2kmn
	@echo on
	::cmd /c fontforge -quiet -script csv2kmn.py dist/pw%ver%_%alias%.csv %ver% %alias%  dist\sun%ver%_%alias%.kmn
	cmd /c fontforge -quiet -script csv2kmn.py %langin% %langaltin%  dist\sun%ver%_%alias%.kmn
	@echo off
	if ERRORLEVEL 1 (goto errorexit)

if %docmd%  NEQ all (goto end)

:csv2svg
	@echo on
	cmd /c fontforge -quiet -script csv2svg.py %langin% %ttffont%
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
	
if %docmd%  NEQ all (goto end)

:svg2font
	@echo on
	cmd /c fontforge -quiet -script svg2Font.py %langin% %ttffont% %alias% dist/SUNBF%ver%_%alias%
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
if %docmd%  NEQ all (goto end)

rem following are for documentation and verification
:back2doc
	@echo on
	cmd /c fontforge -quiet -script back2doc.py %langin% dist/back%ver%_%alias%.txt 
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
if %docmd%  NEQ all (goto end)

:compact
	@echo on
	cmd /c fontforge -quiet -script compact4x16.py %langin% dist/compact%ver%_%alias%.pdf
	@echo off
	if ERRORLEVEL 1 (goto errorexit)	
if %docmd%  NEQ all (goto end)

:bfzip
	@echo on
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


