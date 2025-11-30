# Manim Progress Bar

A customizable progress bar component for Manim animations.

**Version: 0.2.0**

A powerful and flexible progress bar plugin for Manim that supports custom angles, smooth animations, and extensive customization options.

## Installation

```bash
pip install manim-progress-bar
```

## 快速开始

### 基础使用

```python
from manim import *
from manim_progress_bar.progress_bar import ProgressBar

class MyScene(Scene):
    def construct(self):
        # 创建进度条
        progress = ProgressBar(
            width=10,
            height=0.4,
            position=DOWN * 3.5,
            fill_color=BLUE,
            duration=10.0
        )
        
        # 显示进度条
        self.play(FadeIn(progress))
        
        # 自动推进到100%（10秒）
        self.play(progress.start())
```

### 角度支持

进度条支持任意角度（0-360度），可以创建水平、垂直、对角线等方向的进度条：

```python
class AngleExample(Scene):
    def construct(self):
        # 水平进度条（0度，默认）
        bar1 = ProgressBar(
            width=8,
            height=0.3,
            position=UP * 2,
            fill_color=BLUE,
            angle=0
        )
        
        # 垂直进度条（90度）
        bar2 = ProgressBar(
            width=8,
            height=0.3,
            position=ORIGIN,
            fill_color=GREEN,
            angle=90
        )
        
        # 对角线进度条（45度）
        bar3 = ProgressBar(
            width=8,
            height=0.3,
            position=DOWN * 2,
            fill_color=RED,
            angle=45
        )
        
        self.play(FadeIn(bar1), FadeIn(bar2), FadeIn(bar3))
        self.play(
            bar1.auto_progress(duration=3.0),
            bar2.auto_progress(duration=3.0),
            bar3.auto_progress(duration=3.0)
        )
```

**角度说明：**
- `0°`：水平向右（默认）
- `90°`：垂直向上
- `180°`：水平向左
- `270°`：垂直向下
- 其他角度：对角线方向

## 自定义样式
```python
class CustomProgressExample(Scene):
    """自定义进度条示例"""
    
    def construct(self):
        # 创建多个不同样式的进度条
        title = Text("多种进度条样式", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        # 进度条1：细长型，红色
        bar1 = ProgressBar(
            width=12,
            height=0.15,
            position=UP * 2,
            fill_color=RED,
            background_color="#444444",
            show_percentage=False
        )
        
        # 进度条2：中等高度，绿色，带百分比
        bar2 = ProgressBar(
            width=10,
            height=0.3,
            position=ORIGIN,
            fill_color=GREEN,
            background_color="#333333",
            show_percentage=True,
            percentage_font_size=20
        )
        
        # 进度条3：粗壮型，蓝色，大字体
        bar3 = ProgressBar(
            width=8,
            height=0.5,
            position=DOWN * 2,
            fill_color=BLUE,
            background_color="#222222",
            border_width=3,
            corner_radius=0.2,
            show_percentage=True,
            percentage_font_size=28,
            percentage_color=YELLOW
        )
        
        self.play(Write(title))
        self.play(FadeIn(bar1), FadeIn(bar2), FadeIn(bar3))
        self.wait(0.5)
        
        # 同时推进所有进度条，但速度不同
        # 注意：auto_progress() 返回的动画已经设置了正确的 run_time，不需要再指定
        self.play(
            bar1.auto_progress(duration=8.0),  # 自动使用 run_time=8.0
            bar2.auto_progress(duration=6.0),  # 自动使用 run_time=6.0
            bar3.auto_progress(duration=4.0)   # 自动使用 run_time=4.0
        )
        
        self.wait(1.0)
```

## 演示视频

![演示动画](videos/CustomProgressExample.gif)

## 主要方法

### `set_progress(progress, run_time=1.0)`
手动设置进度，带动画效果。

```python
# 推进到50%，耗时2秒
self.play(progress.set_progress(0.5, run_time=2.0))
```

### `auto_progress(duration=None, start_progress=0.0, end_progress=1.0)`
根据时间自动推进进度条。

```python
# 5秒内从0%自动走到100%
self.play(progress.auto_progress(duration=5.0))
```

### `start()`
使用初始化时设置的 `duration` 开始自动推进。

```python
progress = ProgressBar(duration=10.0)
self.play(progress.start())  # 10秒内达到100%
```

### `update_progress_instant(progress)`
立即更新进度，无动画效果。

```python
progress.update_progress_instant(0.5)  # 立即到50%
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `width` | float | 10 | 进度条总宽度 |
| `height` | float | 0.3 | 进度条高度 |
| `position` | np.array | DOWN * 3.5 | 进度条位置 |
| `fill_color` | str/Color | BLUE | 填充颜色 |
| `background_color` | str/Color | GRAY | 背景颜色 |
| `border_color` | str/Color | WHITE | 边框颜色 |
| `border_width` | float | 2 | 边框宽度 |
| `corner_radius` | float | 0.1 | 圆角半径 |
| `show_percentage` | bool | True | 是否显示百分比 |
| `percentage_font_size` | int | 28 | 百分比字体大小 |
| `percentage_color` | str/Color | WHITE | 百分比文字颜色 |
| `percentage_font` | str | "Sans" | 百分比字体（默认使用 Manim 常用无衬线字体） |
| `angle` | float | 0 | 进度条角度（度），0度为水平向右，按逆时针旋转 |
| `duration` | float | None | 总时长（秒），用于自动推进 |

## 示例

### 基础使用
```python
progress = ProgressBar(
    width=10,
    height=0.4,
    fill_color=BLUE
)
self.play(FadeIn(progress))
self.play(progress.set_progress(0.5, run_time=2.0))
```

### 自定义样式
```python
progress = ProgressBar(
    width=12,
    height=0.5,
    position=ORIGIN,
    fill_color="#FF6B6B",
    background_color="#4ECDC4",
    border_color=YELLOW,
    border_width=3,
    corner_radius=0.15,
    show_percentage=True,
    percentage_font_size=28
)
```

### 视频进度条风格
```python
video_progress = ProgressBar(
    width=12,
    height=0.2,
    position=DOWN * 3.5,
    fill_color="#00D4FF",
    background_color="#333333",
    show_percentage=False,
    duration=60.0  # 60秒视频
)
self.play(video_progress.start())
```

### 不同角度的进度条
```python
# 水平进度条（默认）
horizontal = ProgressBar(angle=0, fill_color=BLUE)

# 垂直进度条
vertical = ProgressBar(angle=90, fill_color=GREEN)

# 对角线进度条
diagonal = ProgressBar(angle=45, fill_color=RED)

# 任意角度
custom = ProgressBar(angle=135, fill_color=YELLOW)
```

## 特性

✅ **完全自定义**：颜色、位置、高度、宽度都可自定义  
✅ **任意角度**：支持 0-360 度任意角度，可创建水平、垂直、对角线等方向的进度条  
✅ **时间控制**：支持设置总时长，进度条自动按时间推进  
✅ **平滑动画**：使用 Manim 的动画系统，动画流畅  
✅ **百分比显示**：可选择显示/隐藏百分比，100% 时自动隐藏  
✅ **精确填充**：根据进度值精确填充到指定位置，100% 时完全铺满  
✅ **高精度计算**：对特殊角度（0°、90°、180°、270°）使用精确值，避免浮点误差  
✅ **动态尺寸**：自动计算最小尺寸，防止圆角矩形变形

## 版本更新

### v0.2.0 (2025-11-30)

**新功能：**
- ✨ 支持任意角度（0-360度）的进度条
- ✨ 动态计算最小尺寸，防止圆角矩形变形
- ✨ 优化填充条更新机制，提升性能
- ✨ 更改默认字体为 "Sans"，提升兼容性

**修复：**
- 🐛 修复90度角时的浮点误差问题
- 🐛 修复百分比文本在100%时不隐藏的问题
- 🐛 修复颜色变淡和白色框问题
- 🐛 修复动画过程中的各种视觉问题

**改进：**
- ⚡ 代码架构优化，移除不必要的计算
- ⚡ 方向向量计算优化，特殊角度使用精确值
- ⚡ 改进百分比文本显示/隐藏逻辑

查看完整的 [CHANGELOG.md](CHANGELOG.md) 了解详细信息。

## 注意事项

- 使用 `auto_progress()` 或 `start()` 时，返回的动画已经设置了正确的 `run_time`，不需要在 `self.play()` 中再次指定
- 当进度条到达目标进度（通常是100%）时，updater 会自动清理，无需手动调用 `clear_updaters()`
- 进度条在 100% 时会自动隐藏百分比文本
- 对于特殊角度（0°、90°、180°、270°），系统使用精确值计算，避免浮点误差

