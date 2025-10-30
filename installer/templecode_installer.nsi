; TempleCode IDE Windows Installer Script
; Uses NSIS (Nullsoft Scriptable Install System)
; Build with: makensis templecode_installer.nsi

!define APP_NAME "TempleCode IDE"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "TempleCode Team"
!define APP_URL "https://github.com/James-HoneyBadger/Super-PILOT"
!define APP_EXE "TempleCode.exe"
!define APP_ICON "assets\templecode.ico"

; Main installer settings
Name "${APP_NAME}"
OutFile "TempleCode-IDE-Setup-${APP_VERSION}.exe"
InstallDir "$PROGRAMFILES64\${APP_NAME}"
InstallDirRegKey HKLM "Software\${APP_NAME}" "InstallDir"
RequestExecutionLevel admin

; Modern UI
!include "MUI2.nsh"
!include "WinVer.nsh"

; Interface settings
!define MUI_ABORTWARNING
!define MUI_ICON "${APP_ICON}"
!define MUI_UNICON "${APP_ICON}"
!define MUI_WELCOMEFINISHPAGE_BITMAP "assets\installer_banner.bmp"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "assets\installer_header.bmp"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN "$INSTDIR\${APP_EXE}"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\README.md"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Languages
!insertmacro MUI_LANGUAGE "English"

; Version information
VIProductVersion "1.0.0.0"
VIAddVersionKey "ProductName" "${APP_NAME}"
VIAddVersionKey "CompanyName" "${APP_PUBLISHER}" 
VIAddVersionKey "FileDescription" "${APP_NAME} Installer"
VIAddVersionKey "FileVersion" "${APP_VERSION}"
VIAddVersionKey "ProductVersion" "${APP_VERSION}"
VIAddVersionKey "LegalCopyright" "Copyright © 2025 ${APP_PUBLISHER}"

; Check Windows version
Function .onInit
  ${IfNot} ${AtLeastWin10}
    MessageBox MB_OK|MB_ICONSTOP "This application requires Windows 10 or later."
    Quit
  ${EndIf}
FunctionEnd

Section "Core Application" SecCore
  SectionIn RO
  
  SetOutPath "$INSTDIR"
  
  ; Main executable
  File "dist\windows\${APP_EXE}"
  
  ; Documentation and examples
  File "README.md"
  File "VERSION"
  File /r "examples"
  File /r "sample_programs"
  File /r "docs"
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; Registry entries
  WriteRegStr HKLM "Software\${APP_NAME}" "InstallDir" "$INSTDIR"
  WriteRegStr HKLM "Software\${APP_NAME}" "Version" "${APP_VERSION}"
  
  ; Add/Remove Programs entry
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
    "DisplayName" "${APP_NAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
    "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
    "InstallLocation" "$INSTDIR"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
    "Publisher" "${APP_PUBLISHER}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
    "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
    "URLInfoAbout" "${APP_URL}"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
    "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
    "NoRepair" 1
    
SectionEnd

Section "Desktop Shortcut" SecDesktop
  CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0
SectionEnd

Section "Start Menu Shortcuts" SecStartMenu
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\Documentation.lnk" "$INSTDIR\docs\README.md"
SectionEnd

Section "File Associations" SecFileAssoc
  ; Associate .spt files (SuperPILOT programs)
  WriteRegStr HKCR ".spt" "" "TempleCode.Program"
  WriteRegStr HKCR "TempleCode.Program" "" "TempleCode Program"
  WriteRegStr HKCR "TempleCode.Program\DefaultIcon" "" "$INSTDIR\${APP_EXE},0"
  WriteRegStr HKCR "TempleCode.Program\shell\open\command" "" '"$INSTDIR\${APP_EXE}" "%1"'
  
  ; Associate .pil files (PILOT programs)  
  WriteRegStr HKCR ".pil" "" "TempleCode.PILOT"
  WriteRegStr HKCR "TempleCode.PILOT" "" "TempleCode PILOT Program"
  WriteRegStr HKCR "TempleCode.PILOT\DefaultIcon" "" "$INSTDIR\${APP_EXE},0"
  WriteRegStr HKCR "TempleCode.PILOT\shell\open\command" "" '"$INSTDIR\${APP_EXE}" "%1"'
  
  ; Refresh shell
  System::Call 'shell32.dll::SHChangeNotify(i, i, i, i) v (0x08000000, 0, 0, 0)'
SectionEnd

; Section descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecCore} "Core TempleCode IDE application files"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} "Create desktop shortcut"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} "Create Start Menu shortcuts"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecFileAssoc} "Associate .spt and .pil files with TempleCode"
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Uninstaller
Section "Uninstall"
  ; Remove files
  Delete "$INSTDIR\${APP_EXE}"
  Delete "$INSTDIR\Uninstall.exe"
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\VERSION"
  RMDir /r "$INSTDIR\examples"
  RMDir /r "$INSTDIR\sample_programs"
  RMDir /r "$INSTDIR\docs"
  
  ; Remove shortcuts
  Delete "$DESKTOP\${APP_NAME}.lnk"
  RMDir /r "$SMPROGRAMS\${APP_NAME}"
  
  ; Remove registry entries
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
  DeleteRegKey HKLM "Software\${APP_NAME}"
  
  ; Remove file associations
  DeleteRegKey HKCR ".spt"
  DeleteRegKey HKCR "TempleCode.Program"
  DeleteRegKey HKCR ".pil"
  DeleteRegKey HKCR "TempleCode.PILOT"
  
  ; Refresh shell
  System::Call 'shell32.dll::SHChangeNotify(i, i, i, i) v (0x08000000, 0, 0, 0)'
  
  ; Remove installation directory if empty
  RMDir "$INSTDIR"
  
SectionEnd