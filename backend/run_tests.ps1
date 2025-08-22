# PowerShell script to run all tests and save output to file
$backendPath = "d:\AI School App for TV and Mobile\ai_school\backend"
$outputFile = "$backendPath\test_results.txt"

Set-Location $backendPath

"AI School Backend Tests - $(Get-Date)" | Out-File $outputFile
"=" * 50 | Out-File $outputFile -Append

$testFiles = @(
    "test_setup.py",
    "test_azure_connection.py", 
    "simple_test.py",
    "test_kids_profiles.py",
    "test_profiles.py",
    "test_api.py",
    "test_fastapi.py"
)

foreach ($testFile in $testFiles) {
    if (Test-Path $testFile) {
        "`nRunning $testFile..." | Out-File $outputFile -Append
        "-" * 30 | Out-File $outputFile -Append
        try {
            $result = python $testFile 2>&1
            $result | Out-File $outputFile -Append
            "Test completed successfully" | Out-File $outputFile -Append
        }
        catch {
            "Error running $testFile : $_" | Out-File $outputFile -Append
        }
    } else {
        "Test file $testFile not found" | Out-File $outputFile -Append
    }
}

"All tests completed - $(Get-Date)" | Out-File $outputFile -Append
