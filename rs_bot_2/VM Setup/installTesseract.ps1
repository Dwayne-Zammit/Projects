# Define the URL of the Tesseract OCR installer
$tesseractInstallerUrl = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe"

# Define the installation directory
$tesseractInstallDir = "C:\Program Files\Tesseract"

# Define the path to add to the system PATH for Tesseract OCR
$tesseractPath = "$tesseractInstallDir\tesseract-ocr"

# Define the path to add to the system PATH for Python scripts
$pythonScriptsPath = "C:\Users\admin\AppData\Roaming\Python\Python311\Scripts"

# Download the Tesseract OCR installer
Invoke-WebRequest -Uri $tesseractInstallerUrl -OutFile "$env:TEMP\tesseract-installer.exe"

# Install Tesseract OCR
Start-Process -FilePath "$env:TEMP\tesseract-installer.exe" -ArgumentList "/SILENT" -Wait

# Add Tesseract OCR directory to the system PATH
if (-not ([System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine) -like "*$tesseractPath*")) {
    [System.Environment]::SetEnvironmentVariable("Path", "$env:Path;$tesseractPath", [System.EnvironmentVariableTarget]::Machine)
    Write-Host "Tesseract OCR has been added to the system PATH."
} else {
    Write-Host "Tesseract OCR is already in the system PATH."
}

# Add Python scripts directory to the system PATH
if (-not ([System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine) -like "*$pythonScriptsPath*")) {
    [System.Environment]::SetEnvironmentVariable("Path", "$env:Path;$pythonScriptsPath", [System.EnvironmentVariableTarget]::Machine)
    Write-Host "Python scripts directory has been added to the system PATH."
} else {
    Write-Host "Python scripts directory is already in the system PATH."
}

# Clean up temporary files
Remove-Item "$env:TEMP\tesseract-installer.exe"

Write-Host "Tesseract OCR has been installed successfully."
