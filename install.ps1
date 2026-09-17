# Works two ways:
#   irm <url>/install.ps1 | iex     runs in your session: clones the repo and cd's into it
#   .\install.ps1 (inside the repo) only installs and verifies dependencies
# Everything runs inside a script block so nothing leaks into the caller's session,
# and there is no `exit`, which would close the terminal under iex.
& {
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

    $inRepo = $PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot 'video_tools'))
    if ($inRepo) {
        $repoDir = $PSScriptRoot
    } else {
        if (-not (Test-Command git)) {
            Install-Package 'Git.Git'
        } else {
            Write-Host 'git already installed.'
        }
        $repoDir = Join-Path (Get-Location) 'video-tools'
        if (Test-Path $repoDir) {
            Write-Host "$repoDir already exists; skipping download."
        } else {
            Write-Host "Downloading video-tools to $repoDir..."
            git clone --quiet https://github.com/jehoshua02/video-tools.git $repoDir
            if ($LASTEXITCODE -ne 0) { throw "git clone failed (exit $LASTEXITCODE)" }
        }
    }

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
        throw 'Some dependencies are missing. Open a new terminal and run the install again.'
    }

    Set-Location $repoDir
    Write-Host "All set. You are in $repoDir"
    Write-Host 'Try: python -m video_tools --help'
}
