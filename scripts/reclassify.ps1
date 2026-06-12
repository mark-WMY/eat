# ============================================================
# Reclassification Script: Common vs Full dishes
# Correct approach: full = ALL items (superset), common = subset
# ============================================================
param(
    [string]$CommonPath = "c:\Users\lin\Downloads\eatWhat\js\ingredients_common.json",
    [string]$FullPath = "c:\Users\lin\Downloads\eatWhat\js\ingredients_full.json",
    [string]$BackupDir = "c:\Users\lin\Downloads\eatWhat\scripts\backups"
)

# Create backup directory
New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null

# Backup original files
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item $CommonPath "$BackupDir\ingredients_common_$timestamp.json" -Force
Copy-Item $FullPath "$BackupDir\ingredients_full_$timestamp.json" -Force
Write-Output "Backups saved to: $BackupDir"

# Load files
Write-Output "Loading files..."
$common = Get-Content $CommonPath -Raw -Encoding UTF8 | ConvertFrom-Json
$full = Get-Content $FullPath -Raw -Encoding UTF8 | ConvertFrom-Json

$commonCountBefore = $common.items.Count
$fullCountBefore = $full.items.Count
Write-Output "Before: Common=$commonCountBefore, Full=$fullCountBefore"

# Build cuisine ID -> name reverse lookup
$cuisineMap = @{}
foreach ($cuisineName in $common.categories.cuisine.PSObject.Properties.Name) {
    $cuisineObj = $common.categories.cuisine.$cuisineName
    $cuisineMap[$cuisineObj.id] = $cuisineObj.name
}

# ============================================================
# IsCommonItem function
# Returns: $true (should be in common), $false (should NOT be in common)
# ============================================================
function IsCommonItem {
    param(
        [string]$name,
        [string[]]$categories,
        [hashtable]$cuisineLookup
    )

    # -------- HARD NO: Alcohol --------
    if ($categories -contains "food_alcohol") {
        return $false
    }

    # -------- HARD NO: Exotic meats --------
    $exoticMeat = @("狗肉", "马肉", "鹿", "骆驼", "牦牛", "蛇", "蚕蛹", "驼峰", "驴肉")
    foreach ($p in $exoticMeat) {
        if ($name.Contains($p)) { return $false }
    }

    # -------- HARD NO: High-end / luxury dishes --------
    $highEnd = @("佛跳墙", "开水白菜", "鲍鱼", "鱼翅", "燕窝", "松露", "鹅肝", "海参", "鱼子酱")
    foreach ($p in $highEnd) {
        if ($name.Contains($p)) { return $false }
    }

    # -------- HARD NO: Large banquet roasts --------
    $banquet = @("烤全羊", "烤乳猪", "烤全牛")
    foreach ($p in $banquet) {
        if ($name.Contains($p)) { return $false }
    }

    # -------- HARD NO: Very regional specialties --------
    $regional = @("血鸭", "土笋冻", "花江", "盲公", "蓼花", "伦教", "鸡仔", "甑糕", "金线油塔", "石子馍", "油塔")
    foreach ($p in $regional) {
        if ($name.Contains($p)) { return $false }
    }

    # -------- HARD NO: Specific cuisines not commonly found everywhere in China --------
    $notCommonCuisineIds = @(
        "cuisine_african",    # 非洲菜
        "cuisine_brazilian",  # 巴西菜
        "cuisine_greek",      # 希腊菜
        "cuisine_middle_eastern" # 中东菜
    )
    foreach ($cat in $categories) {
        if ($notCommonCuisineIds -contains $cat) {
            return $false
        }
    }

    # -------- HARD YES: Common food types (automatic) --------
    $commonFoodTypes = @(
        "food_bbq",       # All BBQ
        "food_bun",       # All steamed buns/包子
        "food_coffee",    # All coffee
        "food_cold",      # All cold dishes
        "food_congee",    # All congee
        "food_dessert",   # All desserts
        "food_dumpling",  # All dumplings
        "food_fruit_tea", # All fruit teas
        "food_hotpot",    # All hot pot
        "food_noodles",   # All noodles
        "food_pancake",   # All Chinese pancakes
        "food_rice",      # All rice dishes
        "food_snack",     # All snacks
        "food_soup",      # All soups
        "food_stirfry",   # All stir-fry dishes
        "food_tea",       # All tea
        "food_vegetarian" # All vegetable dishes
    )
    foreach ($ft in $commonFoodTypes) {
        if ($categories -contains $ft) {
            return $true
        }
    }

    # -------- HARD YES: dish_snack category --------
    if ($categories -contains "dish_snack") {
        return $true
    }

    # -------- HARD YES: dish_appetizer (冷菜/凉菜) --------
    if ($categories -contains "dish_appetizer" -and $categories -contains "food_cold") {
        return $true
    }

    # -------- NAME-BASED: Common patterns --------
    $commonPatterns = @(
        # === Breakfast items ===
        "包子", "馒头", "花卷", "豆浆", "油条", "豆腐脑", "肠粉", "煎饼",
        "小笼包", "生煎", "锅贴", "烧麦", "鸡蛋灌饼", "肉夹馍", "豆花",
        "糖糕", "炸糕", "糯米鸡", "粢饭", "葱油饼", "手抓饼", "春卷",
        "馄饨", "抄手", "云吞",

        # === Street food / night market ===
        "麻辣烫", "冒菜", "串串", "烧烤", "烤串", "臭豆腐", "凉皮", "米线",
        "酸辣粉", "螺蛳粉", "热干面", "小面", "炒饭", "蛋炒饭", "盖浇", "煲仔",
        "炸鸡", "炸串", "烤冷面", "手抓饼", "铁板",

        # === Noodles (general) ===
        "牛肉面", "拉面", "刀削面", "炸酱面", "油泼面", "阳春面", "担担面",
        "凉面", "拌面", "汤面", "炒面", "烩面", "板面", "臊子面", "燃面",
        "炸酱", "打卤面", "葱油拌面", "重庆小面", "兰州拉面", "牛肉板面",

        # === Small stir-fry restaurant dishes ===
        "宫保", "鱼香", "回锅", "麻婆", "番茄炒蛋", "酸辣土豆丝", "青椒",
        "红烧", "糖醋", "水煮", "干煸", "鱼香肉丝", "京酱肉丝",

        # === Common beverages ===
        "奶茶", "柠檬", "咖啡", "可乐", "雪碧", "果汁", "气泡",

        # === Common fruits ===
        "苹果", "香蕉", "橙", "橘子", "西瓜", "梨", "桃", "葡萄", "草莓", "芒果",
        "柚子", "菠萝", "哈密瓜", "樱桃", "猕猴桃", "火龙果", "榴莲",

        # === Common snacks ===
        "辣条", "爆米花", "瓜子", "花生", "薯片", "饼干", "方便面", "巧克力",
        "冰淇淋", "蛋糕", "面包", "泡芙", "蛋挞", "布丁",

        # === Cold dishes ===
        "凉拌黄瓜", "凉拌木耳", "拍黄瓜", "皮蛋豆腐", "口水鸡", "夫妻肺片", "蒜泥白肉",
        "凉拌", "凉粉",

        # === BBQ items ===
        "羊肉串", "牛肉串", "烤鸡翅", "烤茄子", "烤韭菜", "烤鱼", "烤虾",
        "烤鱿鱼", "烤生蚝", "烤扇贝", "烤玉米", "烤土豆",

        # === Chain restaurants ===
        "火锅", "麻辣香锅", "黄焖鸡",

        # === Roast meats ===
        "烧鹅", "烤鸭", "叉烧", "烧肉", "白切鸡",

        # === Rice bowl shops ===
        "卤肉饭", "猪脚饭", "叉烧饭", "煲仔饭", "鸡腿饭", "排骨饭", "牛腩饭",
        "盖浇饭", "扬州炒饭", "黄焖鸡米饭",

        # === Chain restaurants ===
        "椰子鸡", "猪肚鸡", "沙县小吃",

        # === Japanese common ===
        "三文鱼", "寿司", "刺身", "拉面", "乌冬面", "荞麦面", "天妇罗",
        "照烧", "味噌", "日式咖喱", "鳗鱼饭", "亲子丼", "猪排饭",

        # === Korean common ===
        "石锅拌饭", "韩式炸鸡", "韩式烤肉", "泡菜", "大酱汤", "辣炒年糕",
        "韩式拌饭", "部队锅",

        # === Fast food / Western common ===
        "披萨", "汉堡", "意面", "意大利面", "三明治", "薯条", "炸鸡",
        "沙拉", "热狗", "牛排", "烤鸡",

        # === Thai/Viet common ===
        "冬阴功", "越南河粉", "泰式炒河粉", "菠萝炒饭", "芒果糯米饭",
        "越式春卷", "泰式咖喱",

        # === Common soups ===
        "紫菜蛋花汤", "酸辣汤", "番茄蛋汤", "排骨汤", "鸡汤", "蛋花汤",
        "冬瓜汤", "白菜豆腐汤", "玉米排骨汤", "萝卜汤"
    )

    foreach ($p in $commonPatterns) {
        if ($name.Contains($p)) {
            return $true
        }
    }

    # -------- FOOD TYPE: food_wholegrain (粗粮) - common --------
    if ($categories -contains "food_wholegrain") {
        return $true
    }

    # -------- CATCH-ALL: Generic noodle pattern (面) --------
    if ($name.Contains("面")) {
        return $true
    }

    # -------- CATCH-ALL: Generic rice noodle (粉) --------
    if ($name.Contains("粉") -and $name -notmatch "面粉|奶粉|淀粉|粉底|粉碎") {
        return $true
    }

    # -------- CATCH-ALL: Generic BBQ (烤) --------
    if ($name.Contains("烤") -and $name -notmatch "烤全羊|烤乳猪|烤全牛") {
        return $true
    }

    # -------- CATCH-ALL: Generic fried (炸) --------
    if ($name.Contains("炸")) {
        return $true
    }

    # -------- Default: NOT common --------
    return $false
}

# ============================================================
# NEW APPROACH:
# 1. Merge both files into a unified set (deduplicate by name) -> this is the full set
# 2. Classify each item as common or not
# 3. Common items -> common file
# 4. All items -> full file
# ============================================================

Write-Output "`n=== Merging items from both files ==="

# Build unified set from both files, deduplicated by name
$allItemsByName = @{}
$allItemsList = [System.Collections.ArrayList]::new()

# Add full items first (they take priority)
foreach ($item in $full.items) {
    if (-not $allItemsByName.ContainsKey($item.name)) {
        $allItemsByName[$item.name] = $item
        [void]$allItemsList.Add($item)
    }
}

# Add common items that are not already in full
$onlyInCommonCount = 0
foreach ($item in $common.items) {
    if (-not $allItemsByName.ContainsKey($item.name)) {
        $allItemsByName[$item.name] = $item
        [void]$allItemsList.Add($item)
        $onlyInCommonCount++
    }
}

Write-Output "  Items from full: $($full.items.Count)"
Write-Output "  Items from common (not in full): $onlyInCommonCount"
Write-Output "  Total unified items: $($allItemsList.Count)"

# ============================================================
# Classify all items
# ============================================================
Write-Output "`n=== Classifying all items ==="

$newCommonItems = [System.Collections.ArrayList]::new()
$newFullItems = [System.Collections.ArrayList]::new()
$commonCount = 0
$fullOnlyCount = 0

foreach ($item in $allItemsList) {
    if (IsCommonItem -name $item.name -categories $item.categories -cuisineLookup $cuisineMap) {
        [void]$newCommonItems.Add($item)
        $commonCount++
    } else {
        $fullOnlyCount++
    }
    [void]$newFullItems.Add($item)
}

Write-Output "  Common items: $commonCount"
Write-Output "  Full-only items: $fullOnlyCount"
Write-Output "  Total full items: $($newFullItems.Count)"

# Show some items that are full-only
Write-Output "`n  Sample full-only items (first 30):"
$fullOnlyItems = $newFullItems | Where-Object {
    $n = $_.name
    $found = $false
    foreach ($ci in $newCommonItems) {
        if ($ci.name -eq $n) { $found = $true; break }
    }
    -not $found
}
$fullOnlyItems | Select-Object -First 30 | ForEach-Object {
    Write-Output "    $($_.id) | $($_.name) | cats: $($_.categories -join ', ')"
}

# ============================================================
# Save files
# ============================================================
Write-Output "`n=== Saving files ==="

# Build output JSON preserving the same structure
$commonOutput = [PSCustomObject]@{
    categories = $common.categories
    items      = [array]$newCommonItems
}

$fullOutput = [PSCustomObject]@{
    categories = $full.categories
    items      = [array]$newFullItems
}

# Save with proper encoding (UTF-8 without BOM)
$commonJson = $commonOutput | ConvertTo-Json -Depth 10 -Compress
$fullJson = $fullOutput | ConvertTo-Json -Depth 10 -Compress

[System.IO.File]::WriteAllText($CommonPath, $commonJson, [System.Text.UTF8Encoding]::new($false))
[System.IO.File]::WriteAllText($FullPath, $fullJson, [System.Text.UTF8Encoding]::new($false))

Write-Output "  Saved ingredients_common.json: $($newCommonItems.Count) items"
Write-Output "  Saved ingredients_full.json: $($newFullItems.Count) items"

# ============================================================
# Summary
# ============================================================
Write-Output "`n=========================================="
Write-Output "=== RE-CLASSIFICATION SUMMARY ==="
Write-Output "=========================================="
Write-Output "Before:"
Write-Output "  Common: $commonCountBefore items"
Write-Output "  Full:   $fullCountBefore items"
Write-Output ""
Write-Output "After:"
Write-Output "  Common: $($newCommonItems.Count) items (everyday dishes)"
Write-Output "  Full:   $($newFullItems.Count) items (ALL dishes including rare)"
Write-Output "  Full-only (rare/not common): $fullOnlyCount items"
Write-Output ""
Write-Output "Changes:"
Write-Output "  Common delta: $($newCommonItems.Count - $commonCountBefore)"
Write-Output "  Full delta:   $($newFullItems.Count - $fullCountBefore)"
Write-Output "=========================================="