# X Lead Finder Launcher for PowerShell
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $ScriptDir ".venv\Scripts\python.exe"
$TargetScript = Join-Path $ScriptDir "scripts\x_lead_finder.py"

if (Test-Path $VenvPython) {
    & $VenvPython $TargetScript
} else {
    python $TargetScript
}
