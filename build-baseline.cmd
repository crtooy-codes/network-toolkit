@echo off
setlocal
set "JAVA_HOME=C:\Program Files\Microsoft\jdk-17.0.19.10-hotspot"
set "ANDROID_HOME=C:\Users\SilvaTech\AndroidSDK"
call gradlew.bat assembleDebug --no-daemon --console=plain > baseline-build.log 2>&1
> baseline-build.exit echo %ERRORLEVEL%
endlocal
