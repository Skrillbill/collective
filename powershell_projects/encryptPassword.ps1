#
#$credential = Get-Credential
#$credential.Password | ConvertFrom-SecureString | Set-Content -Path 'C:\Powershell Script\encryptedPword_string.txt'
#


$keyHash = Get-Content -Path 'C:\Powershell Script\encryptedPword_string.txt' | ConvertTo-SecureString
$credential = New-Object System.Management.Automation.PsCredential('null', $encrypted)

$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($credential.Password)
$pWord = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
