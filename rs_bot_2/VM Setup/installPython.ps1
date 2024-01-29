# Set Python version
$PYTHON_VERSION = "3.11.0"

# Set Python installation directory
$PYTHON_INSTALL_DIR = "C:\Python$PYTHON_VERSION"

# Download Python installer
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/$PYTHON_VERSION/python-$PYTHON_VERSION-amd64.exe" -OutFile python-installer.exe

# Install Python
Start-Process -FilePath python-installer.exe -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0" -Wait

# Clean up
Remove-Item python-installer.exe

Write-Host "Python $PYTHON_VERSION has been installed successfully."

# Define the destination directory
$destinationDirectory = "C:\Program Files\tesseract"

# Check if the destination directory exists, if not, create it
if (-not (Test-Path -Path $destinationDirectory -PathType Container)) {
    New-Item -ItemType Directory -Path $destinationDirectory | Out-Null
}

# Download the Tesseract OCR source code as a zip file
Invoke-WebRequest -Uri "https://github.com/tesseract-ocr/tesseract/archive/refs/heads/main.zip" -OutFile "$env:TEMP\tesseract-main.zip"

# Extract the zip file to the destination directory
Expand-Archive -Path "$env:TEMP\tesseract-main.zip" -DestinationPath $destinationDirectory -Force

if ($?) {
    Write-Host "Tesseract OCR source code has been successfully downloaded and placed in $destinationDirectory."
} else {
    Write-Host "Failed to download Tesseract OCR source code."
}

## install vc redist ##
$installerPath = "C:\Path\To\Save\vc_redist.x64.exe"

Start-Process -FilePath $installerPath -ArgumentList "/quiet" -Wait
