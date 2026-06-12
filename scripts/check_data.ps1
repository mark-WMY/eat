$commonPath = "c:\Users\lin\Downloads\eatWhat\js\ingredients_common.json"
$fullPath = "c:\Users\lin\Downloads\eatWhat\js\ingredients_full.json"

# Read with UTF8 encoding
$commonRaw = Get-Content $commonPath -Raw -Encoding UTF8
$fullRaw = Get-Content $fullPath -Raw -Encoding UTF8

$common = $commonRaw | ConvertFrom-Json
$full = $fullRaw | ConvertFrom-Json

# Verify structure
Write-Output "Common - Type: $($common.GetType().Name)"
Write-Output "Common categories available: $($common.PSObject.Properties.Name -join ', ')"
Write-Output "Common items count: $($common.items.Count)"

Write-Output ""
Write-Output "Full - Type: $($full.GetType().Name)"
Write-Output "Full categories available: $($full.PSObject.Properties.Name -join ', ')"
Write-Output "Full items count: $($full.items.Count)"

Write-Output "--- First 5 common items ---"
for ($i = 0; $i -lt [Math]::Min(5, $common.items.Count); $i++) {
    $item = $common.items[$i]
    Write-Output "  $($item.id) | $($item.name) | cats: $($item.categories -join ', ')"
}

Write-Output "--- First 5 full items ---"
for ($i = 0; $i -lt [Math]::Min(5, $full.items.Count); $i++) {
    $item = $full.items[$i]
    Write-Output "  $($item.id) | $($item.name) | cats: $($item.categories -join ', ')"
}

# Check unique foodTypes in common
Write-Output ""
Write-Output "--- Unique food_* categories in common items ---"
$allCats = $common.items.categories | ForEach-Object { $_ } | Where-Object { $_ -like "food_*" } | Sort-Object -Unique
Write-Output ($allCats -join ', ')