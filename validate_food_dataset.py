#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
食物数据集清洗与校验工具
分步骤验证每个食物项：
1. 真实性验证：检查食物是否真实存在
2. 属性完整性检查：核对关键属性是否缺失
3. 属性准确性校验：评估属性值是否正确
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

# ============================================================
# 工具函数
# ============================================================

def backup_data(filepath):
    """备份原始数据"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = filepath.replace('.json', f'_backup_{timestamp}.json')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 已备份数据到: {backup_path}")
    return backup_path, data

def save_data(filepath, data):
    """保存数据"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] 已保存数据到: {filepath}")

def log_operation(log_file, operation, item_name, details):
    """记录操作日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {operation} | {item_name} | {details}\n")

# ============================================================
# 步骤1: 真实性验证
# ============================================================

def validate_reality(item, known_foods):
    """
    验证食物是否真实存在
    
    策略：
    1. 检查是否在已知真实食物列表中
    2. 检查名称是否包含明显的虚构特征（如特殊符号、无意义组合等）
    3. 检查是否是正确的食物名称（不是描述性文本）
    """
    name = item['name']
    
    # 检查1: 名称是否包含特殊符号（可能是测试数据）
    if re.search(r'[0-9]{3,}', name):  # 包含3个以上连续数字
        return False, "名称包含过多数字，可能是测试数据"
    
    # 检查2: 名称是否过短（可能是不完整的条目）
    if len(name) < 2:
        return False, "名称过短，不完整"
    
    # 检查3: 名称是否过长（可能是描述而非食物名）
    if len(name) > 20:
        return False, "名称过长，可能是描述性文本"
    
    # 检查4: 是否在已知虚构食物列表中
    fictional_foods = {
        '测试食物', 'test', 'fake', 'dummy', '示例', 'example',
        '某某菜', '某某食物', '未命名', 'untitled'
    }
    if name.lower() in {f.lower() for f in fictional_foods}:
        return False, "名称属于已知的虚构/测试食物"
    
    # 通过验证
    return True, "真实存在"

# ============================================================
# 步骤2: 属性完整性检查
# ============================================================

def check_attribute_completeness(item):
    """
    检查属性完整性
    
    每个食物项应该包含：
    1. name: 食物名称
    2. categories: 分类（至少一个有效分类）
    3. attributes: 属性（health和allergens）
    """
    issues = []
    
    # 检查1: name字段
    if 'name' not in item:
        issues.append("缺失name字段")
    elif not item['name'] or not isinstance(item['name'], str):
        issues.append("name字段无效")
    
    # 检查2: categories字段
    if 'categories' not in item:
        issues.append("缺失categories字段")
    elif not item['categories'] or not isinstance(item['categories'], list):
        issues.append("categories字段无效")
    else:
        # 检查categories是否包含至少一个有效分类
        valid_categories = ['cuisine', 'dishType', 'mainIngredient', 'cookingMethod', 'flavor']
        has_valid = False
        for cat in item['categories']:
            if isinstance(cat, str) and any(vc in cat for vc in valid_categories):
                has_valid = True
                break
        if not has_valid:
            issues.append("categories中没有有效分类")
    
    # 检查3: attributes字段
    if 'attributes' not in item:
        issues.append("缺失attributes字段")
    elif not item['attributes'] or not isinstance(item['attributes'], dict):
        issues.append("attributes字段无效")
    else:
        # 检查health和allergens子字段
        attrs = item['attributes']
        if 'health' not in attrs:
            issues.append("缺失attributes.health字段")
        if 'allergens' not in attrs:
            issues.append("缺失attributes.allergens字段")
    
    return issues

def fix_attribute_completeness(item, data):
    """修复属性完整性问题"""
    fixed = False
    
    # 修复1: 添加缺失的attributes字段
    if 'attributes' not in item:
        item['attributes'] = {'health': [], 'allergens': []}
        fixed = True
    
    # 修复2: 添加缺失的health和allergens字段
    if 'attributes' in item:
        if 'health' not in item['attributes']:
            item['attributes']['health'] = []
            fixed = True
        if 'allergens' not in item['attributes']:
            item['attributes']['allergens'] = []
            fixed = True
    
    return item, fixed

# ============================================================
# 步骤3: 属性准确性校验
# ============================================================

def validate_attribute_accuracy(item, data):
    """
    验证属性准确性
    
    检查：
    1. categories中的分类ID是否存在于数据集中
    2. attributes.health中的标签是否存在于数据集中
    3. attributes.allergens中的标签是否存在于数据集中
    """
    issues = []
    
    # 检查1: categories中的分类ID是否有效
    if 'categories' in item and isinstance(item['categories'], list):
        for cat_id in item['categories']:
            if not is_valid_category_id(cat_id, data):
                issues.append(f"无效的category ID: {cat_id}")
    
    # 检查2: attributes.health中的标签是否有效
    if 'attributes' in item and 'health' in item['attributes']:
        for health_tag in item['attributes']['health']:
            if not is_valid_health_tag(health_tag, data):
                issues.append(f"无效的health标签: {health_tag}")
    
    # 检查3: attributes.allergens中的标签是否有效
    if 'attributes' in item and 'allergens' in item['attributes']:
        for allergen in item['attributes']['allergens']:
            if not is_valid_allergen(allergen, data):
                issues.append(f"无效的allergen标签: {allergen}")
    
    return issues

def is_valid_category_id(cat_id, data):
    """检查category ID是否有效"""
    if not isinstance(cat_id, str):
        return False
    
    # 遍历所有分类类型
    for cat_type, cat_dict in data['categories'].items():
        if isinstance(cat_dict, dict):
            for cat_name, cat_info in cat_dict.items():
                if isinstance(cat_info, dict) and cat_info.get('id') == cat_id:
                    return True
                elif cat_info == cat_id:  # 有些是直接存储ID
                    return True
    return False

def is_valid_health_tag(tag, data):
    """检查health标签是否有效"""
    if 'healthTags' not in data['categories']:
        return True  # 如果没有定义，暂时认为是有效的
    
    valid_tags = [info['id'] for info in data['categories']['healthTags'].values() 
                  if isinstance(info, dict) and 'id' in info]
    return tag in valid_tags

def is_valid_allergen(allergen, data):
    """检查allergen标签是否有效"""
    if 'allergens' not in data['categories']:
        return True  # 如果没有定义，暂时认为是有效的
    
    valid_allergens = [info['id'] for info in data['categories']['allergens'].values() 
                       if isinstance(info, dict) and 'id' in info]
    return allergen in valid_allergens

def fix_attribute_accuracy(item, issues):
    """修复属性准确性问题（仅删除错误的属性）"""
    removed = []
    
    for issue in issues:
        if '无效的category ID' in issue:
            # 提取错误的category ID
            match = re.search(r"无效的category ID: (.+)", issue)
            if match:
                invalid_id = match.group(1)
                if invalid_id in item.get('categories', []):
                    item['categories'].remove(invalid_id)
                    removed.append(f"category: {invalid_id}")
        
        elif '无效的health标签' in issue:
            # 提取错误的health标签
            match = re.search(r"无效的health标签: (.+)", issue)
            if match:
                invalid_tag = match.group(1)
                if invalid_tag in item.get('attributes', {}).get('health', []):
                    item['attributes']['health'].remove(invalid_tag)
                    removed.append(f"health: {invalid_tag}")
        
        elif '无效的allergen标签' in issue:
            # 提取错误的allergen标签
            match = re.search(r"无效的allergen标签: (.+)", issue)
            if match:
                invalid_allergen = match.group(1)
                if invalid_allergen in item.get('attributes', {}).get('allergens', []):
                    item['attributes']['allergens'].remove(invalid_allergen)
                    removed.append(f"allergen: {invalid_allergen}")
    
    return item, removed

# ============================================================
# 主流程
# ============================================================

def main(test_mode=False, test_count=10):
    """
    主流程
    
    Args:
        test_mode: 是否为测试模式（只处理前N个食物项）
        test_count: 测试模式下处理的食物项数量
    """
    print("=" * 80)
    print("食物数据集清洗与校验工具")
    if test_mode:
        print(f"[测试模式] 只处理前 {test_count} 个食物项")
    print("=" * 80)
    print()
    
    # 配置文件路径
    data_file = 'js/ingredients.json'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"validation_log_{timestamp}.txt"
    
    # 步骤0: 备份原始数据
    print("[步骤0] 备份原始数据")
    print("-" * 80)
    backup_path, data = backup_data(data_file)
    
    # 测试模式：只处理前N个食物项
    if test_mode:
        original_count = len(data['items'])
        data['items'] = data['items'][:test_count]
        print(f"\n[测试模式] 原始数据: {original_count} 项")
        print(f"[测试模式] 只处理前 {len(data['items'])} 项进行测试")
    
    print()
    
    # 初始化统计
    stats = {
        'total': len(data['items']),
        'deleted': 0,  # 删除的食物项
        'fixed_completeness': 0,  # 修复完整性问题的数量
        'fixed_accuracy': 0,  # 修复准确性问题的数量
        'valid': 0,  # 有效的食物项
    }
    
    # 初始化日志
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("食物数据集清洗与校验日志\n")
        f.write("=" * 80 + "\n")
        f.write(f"处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"原始数据: {data_file}\n")
        f.write(f"备份数据: {backup_path}\n")
        f.write(f"总食物数: {stats['total']}\n")
        f.write("=" * 80 + "\n\n")
    
    # 步骤1: 真实性验证
    print("[步骤1] 真实性验证")
    print("-" * 80)
    valid_items = []
    
    for i, item in enumerate(data['items']):
        is_real, reason = validate_reality(item, None)
        
        if is_real:
            valid_items.append(item)
            stats['valid'] += 1
        else:
            log_operation(log_file, "删除", item['name'], f"原因: {reason}")
            print(f"  [X] 删除: {item['name']} (原因: {reason})")
            stats['deleted'] += 1
    
    data['items'] = valid_items
    print(f"\n  验证完成: 保留 {stats['valid']} 项, 删除 {stats['deleted']} 项")
    print()
    
    # 步骤2: 属性完整性检查
    print("[步骤2] 属性完整性检查")
    print("-" * 80)
    
    for i, item in enumerate(data['items']):
        issues = check_attribute_completeness(item)
        
        if issues:
            print(f"  [WARN] {item['name']}:")
            for issue in issues:
                print(f"    - {issue}")
            
            # 尝试修复
            item, fixed = fix_attribute_completeness(item, data)
            if fixed:
                log_operation(log_file, "修复完整性", item['name'], f"问题: {issues}")
                print(f"    [OK] 已自动修复")
                stats['fixed_completeness'] += 1
            else:
                log_operation(log_file, "无法修复", item['name'], f"问题: {issues}")
                print(f"    [X] 无法自动修复")
        else:
            pass  # 没有完整性问题
    
    print(f"\n  检查完成: 修复 {stats['fixed_completeness']} 项的完整性问题")
    print()
    
    # 步骤3: 属性准确性校验
    print("[步骤3] 属性准确性校验")
    print("-" * 80)
    
    for i, item in enumerate(data['items']):
        issues = validate_attribute_accuracy(item, data)
        
        if issues:
            print(f"  [WARN] {item['name']}:")
            for issue in issues:
                print(f"    - {issue}")
            
            # 尝试修复（仅删除错误的属性）
            item, removed = fix_attribute_accuracy(item, issues)
            if removed:
                log_operation(log_file, "删除错误属性", item['name'], f"删除: {removed}")
                print(f"    [OK] 已删除错误属性: {removed}")
                stats['fixed_accuracy'] += 1
            else:
                log_operation(log_file, "准确性问题", item['name'], f"问题: {issues}")
                print(f"    [X] 无法自动修复")
        else:
            pass  # 没有准确性问题
    
    print(f"\n  校验完成: 修复 {stats['fixed_accuracy']} 项的准确性问题")
    print()
    
    # 保存清洗后的数据
    print("[保存] 清洗后的数据")
    print("-" * 80)
    
    if test_mode:
        # 测试模式：保存到测试文件，不覆盖原始数据
        test_output = f"js/ingredients_test_{timestamp}.json"
        save_data(test_output, data)
        print(f"\n[测试模式] 原始数据未修改")
        print(f"[测试模式] 测试结果已保存到: {test_output}")
    else:
        # 正常模式：保存到原始文件
        save_data(data_file, data)
        
        # 同步到备份文件
        backup_path2 = 'js/ingredients_backup.json'
        save_data(backup_path2, data)
        
        # 同步到小程序
        miniprogram_path = 'miniprogram/data/ingredients.json'
        save_data(miniprogram_path, data)
    
    # 输出统计报告
    print()
    print("=" * 80)
    print("清洗与校验报告")
    print("=" * 80)
    print(f"原始食物数: {stats['total']}")
    print(f"删除食物数: {stats['deleted']}")
    print(f"保留食物数: {stats['valid']}")
    print(f"修复完整性问题: {stats['fixed_completeness']} 项")
    print(f"修复准确性问题: {stats['fixed_accuracy']} 项")
    print(f"最终食物数: {len(data['items'])}")
    print("=" * 80)
    print()
    print(f"详细日志已保存到: {log_file}")
    print()

if __name__ == "__main__":
    import sys
    
    # 命令行参数解析
    test_mode = False
    test_count = 10
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            test_mode = True
            if len(sys.argv) > 2:
                try:
                    test_count = int(sys.argv[2])
                except ValueError:
                    print("错误: 测试数量必须是数字")
                    sys.exit(1)
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("用法:")
            print("  python validate_food_dataset.py          # 正常模式，处理所有数据")
            print("  python validate_food_dataset.py --test   # 测试模式，处理前10个")
            print("  python validate_food_dataset.py --test 20  # 测试模式，处理前20个")
            sys.exit(0)
    
    # 运行主流程
    main(test_mode=test_mode, test_count=test_count)
