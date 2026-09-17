# Works two ways:
#   irm <url>/install.ps1 | iex     runs in your session: clones the repo, so the tools work right away
#   .\install.ps1 (inside the repo) skips the clone
# Both install dependencies and put the `video-tools` command on the user PATH.
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
        if (Test-Path (Join-Path $repoDir '.git')) {
            Write-Host "$repoDir already exists; updating it..."
            git -C $repoDir pull --quiet --ff-only
            if ($LASTEXITCODE -ne 0) { throw "Could not update $repoDir (exit $LASTEXITCODE). Delete that folder and run the install again." }
        } elseif (Test-Path $repoDir) {
            throw "$repoDir already exists but is not a video-tools install. Delete or rename it, or run the install from a different folder."
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

    $binDir = Join-Path $repoDir 'bin'
    $userPath = "$([Environment]::GetEnvironmentVariable('Path', 'User'))"
    # Drop entries from other video-tools installs so this one is the only one on PATH.
    $entries = @($userPath -split ';' | Where-Object { $_ })
    $stale = @($entries | Where-Object {
        $_.TrimEnd('\') -ne $binDir -and
        ($_.TrimEnd('\') -like '*\video-tools\bin' -or (Test-Path (Join-Path $_ 'video-tools.cmd')))
    })
    foreach ($old in $stale) { Write-Host "Removing older video-tools PATH entry: $old" }
    $kept = @($entries | Where-Object { $stale -notcontains $_ })
    if ($kept -contains $binDir -and -not $stale) {
        Write-Host 'video-tools already on PATH.'
    } else {
        if ($kept -notcontains $binDir) {
            Write-Host "Adding $binDir to your PATH..."
            $kept += $binDir
        }
        [Environment]::SetEnvironmentVariable('Path', ($kept -join ';'), 'User')
    }
    Update-SessionPath

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

    if (Test-Command video-tools) {
        Write-Host '  OK   video-tools command'
    } else {
        $launcher = Join-Path $binDir 'video-tools.cmd'
        if (Test-Path $launcher) {
            Write-Host "  FAIL video-tools command not found, although $launcher exists and its folder was added to PATH"
        } else {
            Write-Host "  FAIL video-tools command not found: $launcher is missing (incomplete or outdated download)"
        }
        $failed = $true
    }

    Write-Host ''
    if ($failed) {
        throw 'Some dependencies are missing. Open a new terminal and run the install again.'
    }

    Write-Host "All set. Installed in $repoDir"
    Write-Host 'Try: video-tools --help  (open a new terminal if the command is not found)'
}
