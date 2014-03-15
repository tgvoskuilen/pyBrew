; MakeWinInstaller.nsi
;
; This script builds the Windows installer for pyBrew

;--------------------------------

; The name of the installer
Name "pyBrew"

; The file to write
OutFile "pyBrewInstaller.exe"

; The default installation directory
InstallDir $PROGRAMFILES\pyBrew

RequestExecutionLevel admin

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "pyBrew (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Save exe file to program folder
  File "pyBrew.exe"
  
  ; Save database csv spreadsheets to program folder
  File /r "data"
  File /r "icons"
  
  ; Create an uninstaller
  WriteUninstaller "uninstall-pyBrew.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\pyBrew"
  CreateShortCut "$SMPROGRAMS\pyBrew\Uninstall.lnk" "$INSTDIR\uninstall-pyBrew.exe" "" "$INSTDIR\uninstall-pyBrew.exe" 0
  CreateShortCut "$SMPROGRAMS\pyBrew\pyBrew.lnk" "$INSTDIR\pyBrew.exe" "" "$INSTDIR\pyBrew.exe" 0
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Desktop Shortcut"

  CreateShortCut "$DESKTOP\pyBrew.lnk" "$INSTDIR\pyBrew.exe" "" "$INSTDIR\pyBrew.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  ;DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyBrew"
  ;DeleteRegKey HKLM SOFTWARE\pyBrew

  ; Remove files and uninstaller
  Delete $INSTDIR\uninstall-pyBrew.exe
  Delete "$INSTDIR\data\*.*"
  Delete "$INSTDIR\icons\*.*"
  Delete "$DESKTOP\pyBrew.lnk"
  Delete $INSTDIR\pyBrew.exe
  
  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\pyBrew\*.*"

  ; Remove directories used
  RMDir "$INSTDIR\data"
  RMDir "$INSTDIR\icons"
  RMDir "$SMPROGRAMS\pyBrew"
  RMDir "$INSTDIR"

SectionEnd
