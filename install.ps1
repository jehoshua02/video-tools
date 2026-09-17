#Requires -Version 5.1
$ErrorActionPreference = 'Stop'

function Update-SessionPath {
    $machine = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $user = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path = "$machine;$user"
}

function Get-PythonVersion {
    try {
        $out = & python -c "import sys; print('%d.%d' % sys.version_info[:2])" 2>$null
        if ($LASTEXITCODE -eq 0 -and $out) { return [version]$out.Trim() }
    } catch {}
    return $null
}

function Test-Command($name) {
    return [bool](Get-Command $name -ErrorAction SilentlyContinue)
}

function Install-Package($id) {
    Write-Host "Installing $id..."
    winget install --exact --id $id --silent --accept-package-agreements --accept-source-agreements
    # -1978335189: already installed, no upgrade available
    if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne -1978335189) { throw "winget failed to install $id (exit $LASTEXITCODE)" }
    Update-SessionPath
}

if (-not (Test-Command winget)) {
    throw 'winget not found. Install "App Installer" from the Microsoft Store, then re-run.'
}

Update-SessionPath

$minPython = [version]'3.12'
$py = Get-PythonVersion
if (-not $py -or $py -lt $minPython) {
    Install-Package 'Python.Python.3.12'
} else {
    Write-Host "Python $py already installed."
}

if (-not ((Test-Command ffmpeg) -and (Test-Command ffprobe))) {
    Install-Package 'Gyan.FFmpeg'
} else {
    Write-Host 'ffmpeg already installed.'
}

if (-not (Test-Command yt-dlp)) {
    Install-Package 'yt-dlp.yt-dlp'
} else {
    Write-Host 'yt-dlp already installed.'
}

Write-Host ''
Write-Host 'Verifying...'
$failed = $false

$py = Get-PythonVersion
if ($py -and $py -ge $minPython) {
    Write-Host "  OK   python $py"
} else {
    Write-Host "  FAIL python $minPython+ not found"
    $failed = $true
}

foreach ($tool in 'ffmpeg', 'ffprobe') {
    if (Test-Command $tool) {
        $line = (& $tool -version 2>$null | Select-Object -First 1)
        Write-Host "  OK   $line"
    } else {
        Write-Host "  FAIL $tool not found"
        $failed = $true
    }
}

if (Test-Command yt-dlp) {
    Write-Host "  OK   yt-dlp $(& yt-dlp --version 2>$null)"
} else {
    Write-Host '  FAIL yt-dlp not found'
    $failed = $true
}

Write-Host ''
if ($failed) {
    Write-Host 'Some dependencies are missing. Open a new terminal and re-run install.ps1.'
    exit 1
}
Write-Host 'All dependencies installed. Open a new terminal before running the tools.'
