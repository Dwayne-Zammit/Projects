param(
    [string]$WindowTitle
)

# Check if the 'User32' type already exists
if (-not ([System.Management.Automation.PSTypeName]'User32').Type) {
    Add-Type @"
    using System;
    using System.Runtime.InteropServices;

    public class User32 {
        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool IsIconic(IntPtr hWnd);

        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
    }
"@
}

$w = Get-Process | Where-Object { $_.MainWindowTitle -eq $WindowTitle } | ForEach-Object { $_.MainWindowHandle }

if ($w -and ([User32]::IsIconic($w) -or [User32]::ShowWindow($w, 0))) {
    Start-Sleep -Seconds 1  # Allow time for window state to be updated

    if ([User32]::IsIconic($w)) {
        [User32]::ShowWindow($w, 9)  # SW_RESTORE
    }

    # Bring the window to the foreground
    [User32]::SetForegroundWindow($w)
}

# Return a boolean indicating whether the operation was successful
return $w -ne $null
