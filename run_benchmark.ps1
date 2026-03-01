$processName = "python"
$csvPath = "disk_utilization_log.csv"

# 1. Start Python
$psi = New-Object System.Diagnostics.ProcessStartInfo -Property @{
    FileName = "python"; Arguments = "-u benchmarkingIO.py"; RedirectStandardOutput = $false
}
$proc = [System.Diagnostics.Process]::Start($psi)

$results = New-Object System.Collections.Generic.List[PSObject]
$totalRead = 0
$totalWrite = 0

Write-Host "Monitoring PID: $($proc.Id). Sampling every 100ms..." -ForegroundColor Cyan

# 2. Monitor Loop
while (-not $proc.HasExited) {
    try {
        # Get live throughput (Bytes per second)
        $stats = Get-Counter -Counter "\Process($processName)\IO Read Bytes/sec", 
                                      "\Process($processName)\IO Write Bytes/sec" -ErrorAction SilentlyContinue
        
        $currentReadMB = [math]::Round($stats.CounterSamples[0].CookedValue / 1MB, 2)
        $currentWriteMB = [math]::Round($stats.CounterSamples[1].CookedValue / 1MB, 2)

        
        $totalRead += ($currentReadMB ) 
        $totalWrite += ($currentWriteMB )

        $results.Add([PSCustomObject]@{
            TimeStamp      = Get-Date -Format "HH:mm:ss.fff"
            CurrentRead_MBps  = $currentReadMB
            CurrentWrite_MBps = $currentWriteMB
            TotalRead_MB      = [math]::Round($totalRead, 2)
            TotalWrite_MB     = [math]::Round($totalWrite, 2)
        })
    } catch { }
    Start-Sleep -Milliseconds 100 
}

# 3. Save to CSV
$results | Export-Csv -Path $csvPath -NoTypeInformation
Write-Host "`nDone! CSV saved. Peak Write: $(($results | Measure-Object CurrentWrite_MBps -Maximum).Maximum) MB/s" -ForegroundColor Green
