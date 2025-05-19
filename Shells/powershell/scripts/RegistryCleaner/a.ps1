$roots='HKLM:\SOFTWARE','HKLM:\SOFTWARE\Wow6432Node','HKCU:\SOFTWARE';
$all=Get-ChildItem -Recurse $roots -ErrorAction SilentlyContinue |
     Where-Object { $_.PSPath -notmatch '\\(Microsoft|Classes)(\\|$)' };
$i=0;$deleted=@();$total=$all.Count;
$all|ForEach-Object{
    $i++; Write-Progress -Activity 'Registry deep-clean' -Status "$i of $total" -PercentComplete (($i/$total)*100);
    # --- safely read property bag (avoid InvalidCastException) ---
    try{ $props = (Get-ItemProperty -LiteralPath $_.PSPath -ErrorAction Stop).PSObject.Properties }catch{ $props=@() }
    # --- orphan logic ---
    $isOrphan = ($props.Count -eq 0) -or (
                 ($paths = $props | Where-Object { $_.Value -is [string] -and $_.Value -match '^[A-Za-z]:\\' }) -and
                 (($paths | Where-Object { Test-Path $_.Value }).Count -eq 0) )
    if($isOrphan){
        Remove-Item -LiteralPath $_.PSPath -Recurse -Force -ErrorAction SilentlyContinue
        $deleted += $_.PSPath
    }
};
"Removed $($deleted.Count) registry key(s):"; $deleted

