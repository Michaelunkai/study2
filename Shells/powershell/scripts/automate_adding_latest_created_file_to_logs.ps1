# Get the latest created file in C:\study
$latestFile = Get-ChildItem -Path "C:\study" -Recurse |
              Where-Object { -not $_.PSIsContainer } |
              Sort-Object CreationTime -Descending |
              Select-Object -First 1

$latestFileName = $latestFile.Name

# Prepare the inputs for the Python script
$inputs = @(
    $latestFileName    # Input for "Enter the subject:"
    ""                 # Press Enter for the next prompt
    ""                 # Press Enter for the following prompt
)

# Combine the inputs into a single string with newlines
$inputString = ($inputs -join "`n") + "`n"

# Set up the process start info
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "python"
$psi.Arguments = "`"C:\study\programming\python\apps\study_tracker\terminal\b.py`""
$psi.UseShellExecute = $false
$psi.RedirectStandardInput = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.CreateNoWindow = $true

# Start the Python process
$process = New-Object System.Diagnostics.Process
$process.StartInfo = $psi
$process.Start() | Out-Null

# Send the inputs to the Python script
$process.StandardInput.Write($inputString)
$process.StandardInput.Close()

# Wait for the process to exit and capture the output
$output = $process.StandardOutput.ReadToEnd()
$errors = $process.StandardError.ReadToEnd()
$process.WaitForExit()

# Display the output
Write-Host $output
if ($errors) {
    Write-Host "Errors:"
    Write-Host $errors
}
