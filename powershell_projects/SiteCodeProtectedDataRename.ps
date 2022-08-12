<#
Loc Code Change Script
v2.0
by: SkrillBill
https://github.com/Skrillbill/collective
#>

<#References
https://blogs.msdn.microsoft.com/johan/2008/10/01/powershell-editing-permissions-on-a-file-or-folder/
https://techstronghold.com/blogs/scripting/powershell-tip-how-to-set-permissions-that-applies-to-folder-subfolder-and-files-without-icacls
#>

#Requires -RunAsAdministrator

#region Global Vars
#Setup our global variables
$global:newLoc = Read-Host -Prompt 'Enter NEW site code  '
$global:oldLoc = Read-host -Prompt 'Enter OLD site code  '
$global:key = 'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\changethis\INSTALL'
$global:SWDir = (Get-ItemProperty -path Registry::$key -name Path).Path
$global:Datapath = "$global:SWDir\CPS\Data"
$global:Opserr = ""

#Do not print errors on screen; we create a log instead at the end
$ErrorActionPreference = "SilentlyContinue"
#endregion Global Vars

#region Functions

function AllowDataRename() {
#Get permissions to Read/Write to CPS\Data folder

    Write-host "Acquiring permissions for CPS\Data from system.. "

    try {
        $acl = Get-acl -Path $global:Datapath -ErrorAction Stop
        $user = "$env:UserDomain\$env:UserName" #setting the user name to an object for cleanliness
        $permission = $user,'FullControl' , 'ContainerInherit , ObjectInherit', 'None','Allow'
        $AR = New-Object -TypeName System.Security.AccessControl.FileSystemAccessRule -ArgumentList $permission
        $acl.SetAccessRule($AR)
        Set-Acl -Path $global:Datapath $acl
    }
    catch { 
        Write-host "==========FAILED==========" -ForegroundColor RED -BackgroundColor BLACK
        Write-host $_
        Write-host "==========================" -ForegroundColor RED -BackgroundColor BLACK
        Write-Host "Terminating program with error: 0x02"
        pause
        exit
        
    }
    
    #Call function to rename data file while we have permissions to do so
        RenameDataFolder
    

    #Remove read/write permissions for ourselves
        Write-Host "REMOVING ACCESS TO $Datapath" -ForegroundColor RED -BackgroundColor BLACK
        $acl.removeaccessrule($AR) | out-null #this line will print 'True' to the console without the out-null
        Set-Acl -Path $global:Datapath $acl
   
}

function RenameDataFolder() {
    
#Renaming the files in teh CPS\Data folder. 
    try {
        Rename-Item -Path $global:Datapath\CurrentSite.dat -NewName CurrentSite.old -ErrorAction Stop
        Rename-Item -Path $global:Datapath\Data-Config_$global:oldLoc.dat -NewName Data-Config_$global:oldLoc.old -ErrorAction Stop
        Rename-Item -Path $global:Datapath\NEXT_$global:oldLoc.dat -NewName NEXT_$global:newLoc.dat -ErrorAction Stop
        Rename-Item -Path $global:Datapath\NEXTMulti_$global:oldLoc.dat -NewName NEXTMulti_$global:newLoc.dat -ErrorAction Stop 
        Rename-Item -Path $global:Datapath\TEPP_$global:oldLoc.dat -NewName TEPP_$global:newLoc.dat -ErrorAction Stop 
        Rename-Item -Path $global:Datapath\Status_$global:oldLoc.dat -NewName Status_$global:newLoc.dat -ErrorAction Stop 
        Rename-Item -Path $global:Datapath\SyncStatus_$global:oldLoc.dat -NewName SyncStatus_$global:newLoc.dat -ErrorAction Stop 
        Write-Host "Permissions acquired; DAT files renamed"   
    }
    catch {
        Write-host "RenameDataFolder Error renaming 1 or more files. Terminating with error: 0x03"
        Write-host $_ 
    }
}

function Executioner() {
#Kill any processes being run out of the program directory
    $runtime = Get-Date -Format g
    try {
        Stop-Process -Name PM*,RepAgent*,PMTransporter* -Force -ErrorAction Stop
        sleep -s 1
        Stop-Service -Name CardProcessingService
        sleep -s 2
        $status = Get-Service -name CardProcessingService | Select -ExpandProperty Status
        if($status -eq 'Running') {
            Add-Content -Path C:\program\LOG\LOCCODE.log -Value $("$runtime -- Script was unable to stop CardProcessingService process.")
            Write-Host "Unable to stop CardProcessingService process. Please manually ensure CardProcessingService is stopped before continuing."
            pause     
        }
    }
    catch {
        Write-Host "$runtime -- Unable to stop processes... check operation log"
        Write-host $_
        exit
    }
}


function logRen() {
#Rename all files in the log folder

    Get-ChildItem $global:SWdir\LOG\$global:oldLoc*.ini | Rename-Item -NewName { $_.name -replace $global:oldLoc, $global:newLoc }
}

#endregion Functions

#region Runtime!
 
#Sleep timers so the humans can see the script working

 Executioner
 Sleep -s 1
 logRen
 Sleep -s 1
 AllowDataRename
 Sleep -s 1


    #If we encountered any errors ($error is an evnvironment variable), dump to log and alert user. Otherwise <insert fanfare>
if ($Error.Count -gt 0) {
    $Error | Out-File -FilePath C:\program\LOG\LOCCODE.log
    
    Write-host "Operation completed but there were errors. Please check the log: C:\program\LOG\LOCCODE.log" -ForegroundColor Red -BackgroundColor Black
    $Error.Clear()
    start C:\program\LOG\LOCCODE.log
}
else {
    Write-Host "Operation Successful!"
}



#endregion Runtime