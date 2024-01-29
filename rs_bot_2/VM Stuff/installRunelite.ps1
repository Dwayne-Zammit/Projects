# Define variables
$RuneLiteURL = "https://github.com/runelite/launcher/releases/download/2.6.10/RuneLiteSetup.exe"
$InstallerPath = "$env:TEMP\RuneLiteSetup.exe"

# Download RuneLite setup executable
Invoke-WebRequest -Uri $RuneLiteURL -OutFile $InstallerPath

# Install RuneLite silently
Start-Process -FilePath $InstallerPath -ArgumentList "/S" -Wait

# Remove the installer file
Remove-Item $InstallerPath

runeliteConfigPath = "C:\Users\admin\.runelite"

mv ./profiles2 $runeliteConfigPath