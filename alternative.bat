set primary=pw7_8_1210_EN.csv
set kmn=kmn7_8_1210_EN.csv
set outfile=alt78_1210.csv

:: pause besure %kmn% is sorted by unicode

::cmd /c fontforge -quiet -script xref.py %xref% 

::cmd /c fontforge -quiet -script ref.py %kmn%

cmd /c fontforge -script alternative.py %primary% %kmn% %outfile%