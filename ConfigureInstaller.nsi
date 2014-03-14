; MakeWinInstaller.nsi
;
; This script builds the Windows installer for pyBrew

;--------------------------------

; The name of the installer
Name "pyBrew"

; The file to write
OutFile "pyBrewInstaller.exe"

; The default installation directory
;InstallDir $PROGRAMFILES\pyBrew
InstallDir $DESKTOP\pyBrew

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
;InstallDirRegKey HKLM "Software\pyBrew" "Install_Dir"

; Request application privileges for Windows Vista
;RequestExecutionLevel admin

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
  
  ; Write the installation path into the registry
  ;WriteRegStr HKLM SOFTWARE\pyBrew "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  ;WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyBrew" "DisplayName" "pyBrew"
  ;WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyBrew" "UninstallString" '"$INSTDIR\uninstall.exe"'
  ;WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyBrew" "NoModify" 1
  ;WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyBrew" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\pyBrew"
  CreateShortCut "$SMPROGRAMS\pyBrew\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\pyBrew\pyBrew.lnk" "$INSTDIR\pyBrew.exe" "" "$INSTDIR\pyBrew.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  ;DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyBrew"
  ;DeleteRegKey HKLM SOFTWARE\pyBrew

  ; Remove files and uninstaller
  Delete $INSTDIR\uninstall.exe
  Delete "$INSTDIR\data\*.*"
  Delete "$INSTDIR\icons\*.*"
  Delete $INSTDIR\pyBrew.exe
  
  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\pyBrew\*.*"

  ; Remove directories used
  RMDir "$INSTDIR\data"
  RMDir "$INSTDIR\icons"
  RMDir "$SMPROGRAMS\pyBrew"
  RMDir "$INSTDIR"

SectionEnd
