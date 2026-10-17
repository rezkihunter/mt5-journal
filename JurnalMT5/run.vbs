Set sh = CreateObject("WScript.Shell")
WScript.Quit sh.Run("""" & CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\run.bat""", 0, True)
