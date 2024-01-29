# Define variables
$RuneLiteURL = "https://github.com/runelite/launcher/releases/download/2.6.10/RuneLiteSetup.exe"
$InstallerPath = "$env:TEMP\RuneLiteSetup.exe"

echo "Attempting to Download Rune Lite"

# Download RuneLite setup executable
Invoke-WebRequest -Uri $RuneLiteURL -OutFile $InstallerPath

# Install RuneLite silently
Start-Process -FilePath $InstallerPath -ArgumentList "/S" -Wait

# Remove the installer file
Remove-Item $InstallerPath

runeliteConfigPath = "C:\Users\admin\.runelite"


# Define the destination directory
$destinationDirectory = "C:\Program Files\tesseract"

# Check if the destination directory exists, if not, create it
if (-not (Test-Path -Path $destinationDirectory -PathType Container)) {
    New-Item -ItemType Directory -Path $destinationDirectory | Out-Null
}

# Clone the Tesseract OCR repository from GitHub
git clone https://github.com/tesseract-ocr/tesseract.git $destinationDirectory

if ($?) {
    Write-Host "Tesseract OCR source code has been successfully downloaded and placed in $destinationDirectory."
} else {
    Write-Host "Failed to download Tesseract OCR source code."
}
