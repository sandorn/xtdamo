# !/usr/bin/env python3
"""
测试绑定参数传递和验证功能
验证参数为 None 时使用默认值，非 None 时使用自定义值
"""

from __future__ import annotations

from xtdamo import DmExcute
from xtdamo.config import Config


def test_config_get_bind_config():
    """测试 Config.get_bind_config 方法"""
    print('=' * 60)
    print('测试1: Config.get_bind_config 参数处理')
    print('=' * 60)

    # 测试1: 不传任何参数（使用所有默认值）
    config = Config.get_bind_config()
    print('\n1. 不传任何参数（使用所有默认值）:')
    print(f'   {config}')
    assert config == Config.DEFAULT_BIND_CONFIG
    print('   ✓ 通过：返回默认配置')

    # 测试2: 传入 None 不覆盖默认值
    config = Config.get_bind_config(display=None, mouse=None)
    print('\n2. 传入 None 不覆盖默认值:')
    print(f'   {config}')
    assert config == Config.DEFAULT_BIND_CONFIG
    print('   ✓ 通过：None 参数不覆盖默认值')

    # 测试3: 传入有效值
    config = Config.get_bind_config(display='dx2', mouse='windows3')
    print('\n3. 传入有效值:')
    print(f'   {config}')
    assert config['display'] == 'dx2'
    assert config['mouse'] == 'windows3'
    assert config['keypad'] == 'windows'  # 未指定，使用默认值
    assert config['mode'] == 101  # 未指定，使用默认值
    print('   ✓ 通过：有效值正确覆盖，其他使用默认值')

    # 测试4: 混合使用（部分 None，部分有效值）
    config = Config.get_bind_config(display=None, mouse='dx', keypad=None, mode=103)
    print('\n4. 混合使用（部分 None，部分有效值）:')
    print(f'   {config}')
    assert config['display'] == 'gdi'  # None，使用默认
    assert config['mouse'] == 'dx'  # 有效值
    assert config['keypad'] == 'windows'  # None，使用默认
    assert config['mode'] == 103  # 有效值
    print('   ✓ 通过：None 使用默认，有效值正确设置')

    return True


def test_config_validation():
    """测试参数验证功能"""
    print('\n' + '=' * 60)
    print('测试2: 参数验证功能')
    print('=' * 60)

    # 测试1: 验证有效的参数
    print('\n1. 验证有效的参数:')
    try:
        config = Config.get_bind_config(display='dx2', mouse='windows3', keypad='windows', mode=101)
        print(f'   配置: {config}')
        print('   ✓ 通过：所有参数都有效')
    except ValueError as e:
        print(f'   ❌ 失败：{e}')
        return False

    # 测试2: 验证无效的 display 值
    print('\n2. 验证无效的 display 值:')
    try:
        Config.get_bind_config(display='invalid_mode')
        print('   ❌ 失败：应该抛出 ValueError')
        return False
    except ValueError as e:
        print(f'   ✓ 通过：正确捕获错误 - {e}')

    # 测试3: 验证无效的 mouse 值
    print('\n3. 验证无效的 mouse 值:')
    try:
        Config.get_bind_config(mouse='invalid_mouse')
        print('   ❌ 失败：应该抛出 ValueError')
        return False
    except ValueError as e:
        print(f'   ✓ 通过：正确捕获错误 - {e}')

    # 测试4: 验证无效的 mode 值
    print('\n4. 验证无效的 mode 值:')
    try:
        Config.get_bind_config(mode=999)
        print('   ❌ 失败：应该抛出 ValueError')
        return False
    except ValueError as e:
        print(f'   ✓ 通过：正确捕获错误 - {e}')

    # 测试5: 验证无效的参数名
    print('\n5. 验证无效的参数名:')
    try:
        Config.get_bind_config(invalid_param='value')
        print('   ❌ 失败：应该抛出 ValueError')
        return False
    except ValueError as e:
        print(f'   ✓ 通过：正确捕获错误 - {e}')

    return True


def test_validate_bind_mode():
    """测试 validate_bind_mode 方法"""
    print('\n' + '=' * 60)
    print('测试3: validate_bind_mode 方法')
    print('=' * 60)

    # 测试有效值
    print('\n1. 测试有效值:')
    test_cases = [
        ('display', 'gdi', True),
        ('display', 'dx2', True),
        ('mouse', 'windows3', True),
        ('keypad', 'windows', True),
        ('mode', 101, True),
        ('mode', 0, True),
    ]

    for mode_type, mode_value, expected in test_cases:
        result = Config.validate_bind_mode(mode_type, mode_value)
        status = '✓' if result == expected else '❌'
        print(f'   {status} validate_bind_mode({mode_type!r}, {mode_value!r}) = {result}')
        if result != expected:
            return False

    # 测试无效值
    print('\n2. 测试无效值:')
    test_cases = [
        ('display', 'invalid', False),
        ('mouse', 'bad_mode', False),
        ('keypad', 'unknown', False),
        ('mode', 999, False),
        ('invalid_type', 'value', False),
    ]

    for mode_type, mode_value, expected in test_cases:
        result = Config.validate_bind_mode(mode_type, mode_value)
        status = '✓' if result == expected else '❌'
        print(f'   {status} validate_bind_mode({mode_type!r}, {mode_value!r}) = {result}')
        if result != expected:
            return False

    return True


def test_all_bind_modes():
    """测试所有可用的绑定模式"""
    print('\n' + '=' * 60)
    print('测试4: 所有可用的绑定模式')
    print('=' * 60)

    print('\n可用的绑定模式:')
    for key, values in Config.BIND_MODES.items():
        print(f'  {key}: {values}')

    print('\n验证所有模式都能通过验证:')
    all_passed = True
    for mode_type, mode_values in Config.BIND_MODES.items():
        for mode_value in mode_values:
            result = Config.validate_bind_mode(mode_type, mode_value)
            if not result:
                print(f'  ❌ {mode_type}={mode_value} 验证失败')
                all_passed = False

    if all_passed:
        print('  ✓ 所有模式都通过验证')

    return all_passed


def main():
    """运行所有测试"""
    print('\n' + '=' * 60)
    print('绑定参数传递和验证测试')
    print('=' * 60)

    results = []

    # 运行测试
    results.append(('Config.get_bind_config 参数处理', test_config_get_bind_config()))
    results.append(('参数验证功能', test_config_validation()))
    results.append(('validate_bind_mode 方法', test_validate_bind_mode()))
    results.append(('所有可用的绑定模式', test_all_bind_modes()))

    # 输出总结
    print('\n' + '=' * 60)
    print('测试总结')
    print('=' * 60)

    for name, result in results:
        status = '✓ 通过' if result else '❌ 失败'
        print(f'{status} - {name}')

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f'\n总计: {passed}/{total} 测试通过')

    if passed == total:
        print('\n🎉 所有测试通过！参数传递和验证功能正常！')
    else:
        print('\n⚠️  部分测试未通过，请检查相关功能')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'\n❌ 测试过程中发生错误: {e}')
        import traceback

        traceback.print_exc()
