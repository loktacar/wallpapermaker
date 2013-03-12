rmdir /s /q win32
python pyinstaller.py -F -w -o win32 -n wpmaker wpmaker.py
python pyinstaller.py -F -c -o win32 -n wpmaker_console wpmaker.py
del plugins\*.pyc
xcopy /s plugins win32\dist\plugins\
xcopy LICENSE win32\dist\
xcopy monitor-wallpaper-icon.png win32\dist\
