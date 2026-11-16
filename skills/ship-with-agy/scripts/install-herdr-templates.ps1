[CmdletBinding()]
param([switch]$Force)

$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($env:APPDATA)) {
    throw 'APPDATA is required. Use the POSIX installer on macOS/Linux.'
}
$source = Join-Path $PSScriptRoot '../templates/agy-implementer.md'
$directory = Join-Path $env:APPDATA 'herdr-core/templates'
$target = Join-Path $directory 'agy-implementer.md'
if (Test-Path -LiteralPath $target) {
    if ((Get-FileHash -LiteralPath $source).Hash -eq (Get-FileHash -LiteralPath $target).Hash) {
        Write-Output "Already installed: $target"
        exit 0
    }
    if (!$Force) { throw "Template differs: $target. Use -Force to replace it." }
}
New-Item -ItemType Directory -Path $directory -Force | Out-Null
Copy-Item -LiteralPath $source -Destination $target -Force
Write-Output "Installed: $target"
