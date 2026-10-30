# 匈牙利节假日（简体中文）

本仓库已公开，含 2026–2035 年 **116 条中文日历事件**，兼容 Apple Calendar。

## 直接订阅（公开原始文件）

`https://raw.githubusercontent.com/Chayiha/hungary-holidays-zh/main/hungary-holidays-zh.ics`

在 iPhone 的「日历 → 日历 → 添加日历 → 添加订阅日历」粘贴该 URL。注意，订阅是否成功以及刷新间隔取决于 Apple 日历和网络服务；该链接是 GitHub 的原始文件地址，不依赖 GitHub Pages。

## 可选：GitHub Pages 地址

在仓库 Settings → Pages 启用 main / root 发布后，可使用：

`https://chayiha.github.io/hungary-holidays-zh/hungary-holidays-zh.ics`

Pages 尚未核验上线前，不应把这一网址当作已启用的订阅源。

## 数据范围和更新说明

包括匈牙利法定节日、按复活节计算的浮动节假日，以及按照 **10/2025 (IV.30.) NGM** 录入的 2026 年 3 个调休休息日和 3 个补班日。不是苹果 iCloud 节日源的实时翻译。

`.github/workflows/update.yml` 每月运行 `generate.py` 重建日历，但 **不会自动查询政府发布的新调休安排**。2027 年后的调休需要在法令公布后补充代码。

依据：[匈牙利 2026 年调休法令](https://net.jogtar.hu/jogszabaly?docid=A2500010.NGM)。
