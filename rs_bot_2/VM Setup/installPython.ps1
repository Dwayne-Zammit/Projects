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

## install tesseract ## 
cp ./Tesseract-ocr C:\Program Files
setx PATH "%PATH%;C:\Program Files\Tesseract-ocr"