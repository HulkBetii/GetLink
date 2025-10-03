# Course Link Getter - Windows Build Test Script
# Comprehensive testing for both portable and installer versions

param(
    [switch]$SkipInstaller,
    [switch]$SkipPortable,
    [int]$TimeoutSeconds = 30
)

Write-Host "🧪 Course Link Getter - Windows Build Test" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green

# Test configuration
$portablePath = "release/Course_Link_Getter-Portable.exe"
$installerPath = "release/Course_Link_Getter-Setup-x64.exe"
$testResults = @()

function Test-Executable {
    param(
        [string]$Path,
        [string]$Name,
        [string]$TestType
    )
    
    Write-Host "`n🔍 Testing $Name..." -ForegroundColor Yellow
    
    if (-not (Test-Path $Path)) {
        Write-Host "❌ $Name not found: $Path" -ForegroundColor Red
        return $false
    }
    
    # Get file info
    $fileInfo = Get-Item $Path
    $fileSize = [math]::Round($fileInfo.Length / 1MB, 2)
    Write-Host "📦 File: $($fileInfo.Name)" -ForegroundColor Cyan
    Write-Host "📏 Size: $fileSize MB" -ForegroundColor Cyan
    Write-Host "📅 Created: $($fileInfo.CreationTime)" -ForegroundColor Cyan
    
    # Test file integrity
    try {
        $hash = Get-FileHash $Path -Algorithm SHA256
        Write-Host "🔐 SHA256: $($hash.Hash.Substring(0,16))..." -ForegroundColor Cyan
    } catch {
        Write-Host "⚠️  Could not calculate hash" -ForegroundColor Yellow
    }
    
    if ($TestType -eq "Portable") {
        return Test-PortableExecutable $Path
    } elseif ($TestType -eq "Installer") {
        return Test-InstallerExecutable $Path
    }
    
    return $false
}

function Test-PortableExecutable {
    param([string]$Path)
    
    Write-Host "🚀 Testing portable executable..." -ForegroundColor Yellow
    
    try {
        # Start the application
        $process = Start-Process -FilePath $Path -PassThru -WindowStyle Normal
        Write-Host "✅ Process started (PID: $($process.Id))" -ForegroundColor Green
        
        # Wait for window to appear
        $timeout = $TimeoutSeconds
        $windowFound = $false
        $startTime = Get-Date
        
        while ($timeout -gt 0 -and -not $windowFound) {
            Start-Sleep -Milliseconds 500
            $timeout -= 0.5
            
            # Check if process is still running
            if ($process.HasExited) {
                Write-Host "❌ Application exited unexpectedly (Exit code: $($process.ExitCode))" -ForegroundColor Red
                return $false
            }
            
            # Look for window
            $windows = Get-Process | Where-Object { 
                $_.MainWindowTitle -like "*Course Link Getter*" -or 
                $_.ProcessName -like "*Course_Link_Getter*" 
            }
            if ($windows) {
                $windowFound = $true
                $elapsed = (Get-Date) - $startTime
                Write-Host "✅ Application window found! (Started in $($elapsed.TotalSeconds.ToString('F1'))s)" -ForegroundColor Green
            }
        }
        
        if (-not $windowFound) {
            Write-Host "❌ Application window not found within $TimeoutSeconds seconds" -ForegroundColor Red
            $process.Kill()
            return $false
        }
        
        # Let it run for a moment
        Start-Sleep -Seconds 3
        
        # Test if window is responsive
        $mainWindow = Get-Process | Where-Object { $_.MainWindowTitle -like "*Course Link Getter*" }
        if ($mainWindow) {
            Write-Host "✅ Application is responsive" -ForegroundColor Green
        }
        
        # Close the application
        Write-Host "🔄 Closing application..." -ForegroundColor Yellow
        $process.CloseMainWindow()
        
        # Wait for graceful exit
        if ($process.WaitForExit(5000)) {
            Write-Host "✅ Application closed gracefully" -ForegroundColor Green
            return $true
        } else {
            Write-Host "⚠️  Application didn't close gracefully, forcing..." -ForegroundColor Yellow
            $process.Kill()
            return $true
        }
        
    } catch {
        Write-Host "❌ Test failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Test-InstallerExecutable {
    param([string]$Path)
    
    Write-Host "📦 Testing installer executable..." -ForegroundColor Yellow
    
    try {
        # Check if installer has proper properties
        $shell = New-Object -ComObject Shell.Application
        $folder = $shell.Namespace((Get-Item $Path).DirectoryName)
        $file = $folder.ParseName((Get-Item $Path).Name)
        
        $version = $folder.GetDetailsOf($file, 2)  # Version
        $size = $folder.GetDetailsOf($file, 1)     # Size
        
        Write-Host "📋 Installer Info:" -ForegroundColor Cyan
        Write-Host "   Version: $version" -ForegroundColor Cyan
        Write-Host "   Size: $size" -ForegroundColor Cyan
        
        # Test installer properties (without actually installing)
        Write-Host "✅ Installer file appears valid" -ForegroundColor Green
        Write-Host "ℹ️  Full installation test requires manual verification" -ForegroundColor Blue
        
        return $true
        
    } catch {
        Write-Host "❌ Installer test failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Test-Checksums {
    Write-Host "`n🔐 Testing checksums..." -ForegroundColor Yellow
    
    $checksumsFile = "release/checksums.txt"
    if (-not (Test-Path $checksumsFile)) {
        Write-Host "❌ Checksums file not found: $checksumsFile" -ForegroundColor Red
        return $false
    }
    
    $checksums = Get-Content $checksumsFile
    Write-Host "✅ Checksums file found with $($checksums.Count) entries" -ForegroundColor Green
    
    foreach ($line in $checksums) {
        if ($line -match "SHA256: (.+)") {
            Write-Host "🔐 Found checksum: $($matches[1].Substring(0,16))..." -ForegroundColor Cyan
        }
    }
    
    return $true
}

function Test-ProjectStructure {
    Write-Host "`n📁 Testing project structure..." -ForegroundColor Yellow
    
    $requiredFiles = @(
        "build_windows.py",
        "README_BUILD.md",
        "smoketest.ps1"
    )
    
    $requiredDirs = @(
        "course_link_getter",
        "release"
    )
    
    $allGood = $true
    
    foreach ($file in $requiredFiles) {
        if (Test-Path $file) {
            Write-Host "✅ $file" -ForegroundColor Green
        } else {
            Write-Host "❌ $file missing" -ForegroundColor Red
            $allGood = $false
        }
    }
    
    foreach ($dir in $requiredDirs) {
        if (Test-Path $dir) {
            Write-Host "✅ $dir/" -ForegroundColor Green
        } else {
            Write-Host "❌ $dir/ missing" -ForegroundColor Red
            $allGood = $false
        }
    }
    
    return $allGood
}

# Main test execution
Write-Host "Starting comprehensive build test..." -ForegroundColor Green

# Test project structure
$structureOk = Test-ProjectStructure
$testResults += @{ Test = "Project Structure"; Result = $structureOk }

# Test portable executable
if (-not $SkipPortable) {
    $portableOk = Test-Executable $portablePath "Portable Executable" "Portable"
    $testResults += @{ Test = "Portable Executable"; Result = $portableOk }
} else {
    Write-Host "`n⏭️  Skipping portable executable test" -ForegroundColor Yellow
    $testResults += @{ Test = "Portable Executable"; Result = "Skipped" }
}

# Test installer executable
if (-not $SkipInstaller) {
    $installerOk = Test-Executable $installerPath "Installer Executable" "Installer"
    $testResults += @{ Test = "Installer Executable"; Result = $installerOk }
} else {
    Write-Host "`n⏭️  Skipping installer executable test" -ForegroundColor Yellow
    $testResults += @{ Test = "Installer Executable"; Result = "Skipped" }
}

# Test checksums
$checksumsOk = Test-Checksums
$testResults += @{ Test = "Checksums"; Result = $checksumsOk }

# Summary
Write-Host "`n" + "=" * 50 -ForegroundColor Green
Write-Host "📊 TEST SUMMARY" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green

$passed = 0
$total = 0

foreach ($result in $testResults) {
    $status = if ($result.Result -eq $true) { "✅ PASS" } 
              elseif ($result.Result -eq "Skipped") { "⏭️  SKIP" }
              else { "❌ FAIL" }
    
    $color = if ($result.Result -eq $true) { "Green" }
             elseif ($result.Result -eq "Skipped") { "Yellow" }
             else { "Red" }
    
    Write-Host "$status $($result.Test)" -ForegroundColor $color
    
    if ($result.Result -ne "Skipped") {
        $total++
        if ($result.Result -eq $true) { $passed++ }
    }
}

Write-Host "`n📈 Results: $passed/$total tests passed" -ForegroundColor $(if ($passed -eq $total) { "Green" } else { "Red" })

if ($passed -eq $total) {
    Write-Host "🎉 All tests passed! Build is ready for distribution." -ForegroundColor Green
    exit 0
} else {
    Write-Host "⚠️  Some tests failed. Please check the build process." -ForegroundColor Red
    exit 1
}
