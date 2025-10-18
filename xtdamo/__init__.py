# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-21 16:26:08
LastEditTime : 2025-08-26 16:43:36
FilePath     : /CODE/xjLib/xt_damo/__init__.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

__name__ = "pydamo"

from .config import Config
from .damo import DmExcute
from .dependencies import (
    CRYPTO_AVAILABLE,
    DependencyChecker,
    WIN32_AVAILABLE,
    WIN32GUI_AVAILABLE,
    check_dependency,
    get_available_dependencies,
    get_missing_dependencies,
)
from .enum_wind import get_windows_by_criteria
from .secure_config import DmCredentials, dm_credentials

# 为了向后兼容，保留 DM 别名
DM = DmExcute

__all__ = (
    "DmExcute",
    "DM",  # 向后兼容
    "Config",
    "DmCredentials",
    "dm_credentials",
    "get_windows_by_criteria",
    # 依赖检查相关
    "DependencyChecker",
    "check_dependency",
    "get_available_dependencies",
    "get_missing_dependencies",
    "CRYPTO_AVAILABLE",
    "WIN32_AVAILABLE",
    "WIN32GUI_AVAILABLE",
)
