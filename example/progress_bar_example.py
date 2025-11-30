# import sys
# from pathlib import Path

# # 添加父目录到 sys.path，以便导入 manim_progress_bar 模块
# parent_dir = Path(__file__).parent.parent
# if str(parent_dir) not in sys.path:
#     sys.path.insert(0, str(parent_dir))

from manim import *
from manim_progress_bar.progress_bar import ProgressBar


class BasicProgressTest(Scene):
    """基础进度条测试：测试基本功能"""
    
    def construct(self):
        title = Text("基础进度条测试", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        # 测试进度条
        bar = ProgressBar(
            width=10,
            height=0.4,
            position=ORIGIN,
            fill_color=BLUE,
            show_percentage=True
        )
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(bar))
        self.wait(0.5)
        
        # 测试 0% -> 50% -> 100%
        self.play(bar.set_progress(0.5, run_time=2.0))
        self.wait(1.0)
        self.play(bar.set_progress(1.0, run_time=2.0))
        self.wait(2.0)


class PercentageHideTest(Scene):
    """测试100%时百分比文字隐藏功能"""
    
    def construct(self):
        title = Text("100%时文字隐藏测试", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        # 创建进度条
        bar = ProgressBar(
            width=10,
            height=0.4,
            position=ORIGIN,
            fill_color=GREEN,
            show_percentage=True,
            percentage_font_size=60
        )
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(bar))
        self.wait(0.5)
        
        # 逐步推进到100%，观察文字是否隐藏
        self.play(bar.set_progress(0.25, run_time=1.0))
        self.wait(0.5)
        self.play(bar.set_progress(0.5, run_time=1.0))
        self.wait(0.5)
        self.play(bar.set_progress(0.75, run_time=1.0))
        self.wait(0.5)
        self.play(bar.set_progress(0.99, run_time=1.0))
        self.wait(0.5)
        # 关键测试：到达100%时文字应该隐藏
        self.play(bar.set_progress(1.0, run_time=1.0))
        self.wait(2.0)
        
        # 测试从100%回到小于100%时文字应该重新显示
        self.play(bar.set_progress(0.5, run_time=1.0))
        self.wait(2.0)


class AngleTest(Scene):
    """测试不同角度的进度条"""
    
    def construct(self):
        title = Text("不同角度测试", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        # 0度（水平向右）
        bar_0 = ProgressBar(
            width=6,
            height=0.3,
            position=UP * 2.5,
            fill_color=BLUE,
            angle=0,
            show_percentage=True
        )
        label_0 = Text("0° (水平向右)", font_size=18, color=WHITE)
        label_0.next_to(bar_0, DOWN, buff=0.2)
        
        # 90度（垂直向上）
        bar_90 = ProgressBar(
            width=2,
            height=0.3,
            position=UP * 0.5,
            fill_color=RED,
            angle=90,
            show_percentage=True
        )
        label_90 = Text("90° (垂直向上)", font_size=18, color=WHITE)
        label_90.next_to(bar_90, RIGHT, buff=0.5)
        
        # 180度（水平向左）
        bar_180 = ProgressBar(
            width=6,
            height=0.3,
            position=DOWN * 0.5,
            fill_color=GREEN,
            angle=180,
            show_percentage=True
        )
        label_180 = Text("180° (水平向左)", font_size=18, color=WHITE)
        label_180.next_to(bar_180, UP, buff=0.2)
        
        # 270度（垂直向下）
        bar_270 = ProgressBar(
            width=2,
            height=0.3,
            position=DOWN * 2.5,
            fill_color=YELLOW,
            angle=270,
            show_percentage=True
        )
        label_270 = Text("270° (垂直向下)", font_size=18, color=WHITE)
        label_270.next_to(bar_270, LEFT, buff=0.5)
        
        # 45度（对角线）
        bar_45 = ProgressBar(
            width=4,
            height=0.3,
            position=RIGHT * 3,
            fill_color=PURPLE,
            angle=45,
            show_percentage=True
        )
        label_45 = Text("45° (对角线)", font_size=18, color=WHITE)
        label_45.next_to(bar_45, DOWN, buff=0.5)
        
        self.play(Write(title))
        self.wait(0.5)
        
        # 显示所有进度条
        self.play(
            FadeIn(bar_0), FadeIn(label_0),
            FadeIn(bar_90), FadeIn(label_90),
            FadeIn(bar_180), FadeIn(label_180),
            FadeIn(bar_270), FadeIn(label_270),
            FadeIn(bar_45), FadeIn(label_45)
        )
        self.wait(0.5)
        
        # 同时推进所有进度条到100%，测试文字隐藏
        self.play(
            bar_0.auto_progress(duration=3.0),
            bar_90.auto_progress(duration=3.0),
            bar_180.auto_progress(duration=3.0),
            bar_270.auto_progress(duration=3.0),
            bar_45.auto_progress(duration=3.0)
        )
        self.wait(2.0)


class AutoProgressTest(Scene):
    """测试自动进度功能"""
    
    def construct(self):
        title = Text("自动进度测试", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        # 使用 duration 参数的自动进度
        bar1 = ProgressBar(
            width=8,
            height=0.4,
            position=UP * 1.5,
            fill_color=BLUE,
            duration=3.0,
            show_percentage=True
        )
        label1 = Text("duration=3.0秒", font_size=20, color=WHITE)
        label1.next_to(bar1, DOWN, buff=0.3)
        
        # 使用 auto_progress 方法的自动进度
        bar2 = ProgressBar(
            width=8,
            height=0.4,
            position=DOWN * 1.5,
            fill_color=GREEN,
            show_percentage=True
        )
        label2 = Text("auto_progress(4.0秒)", font_size=20, color=WHITE)
        label2.next_to(bar2, DOWN, buff=0.3)
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(bar1), FadeIn(label1), FadeIn(bar2), FadeIn(label2))
        self.wait(0.5)
        
        # 同时启动两个自动进度
        self.play(
            bar1.start(),  # 使用 duration 参数
            bar2.auto_progress(duration=4.0)  # 使用方法参数
        )
        self.wait(2.0)


class ManualProgressTest(Scene):
    """测试手动设置进度"""
    
    def construct(self):
        title = Text("手动设置进度测试", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        bar = ProgressBar(
            width=10,
            height=0.4,
            position=ORIGIN,
            fill_color=ORANGE,
            show_percentage=True
        )
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(bar))
        self.wait(0.5)
        
        # 测试不同的进度值
        progress_values = [0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1.0]
        for progress in progress_values:
            self.play(bar.set_progress(progress, run_time=1.0))
            self.wait(0.3)
        
        self.wait(1.0)
        
        # 测试从100%回到其他值
        self.play(bar.set_progress(0.3, run_time=1.0))
        self.wait(1.0)


class InstantUpdateTest(Scene):
    """测试立即更新功能"""
    
    def construct(self):
        title = Text("立即更新测试", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        bar = ProgressBar(
            width=10,
            height=0.4,
            position=ORIGIN,
            fill_color=PURPLE,
            show_percentage=True
        )
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(bar))
        self.wait(0.5)
        
        # 使用立即更新，无动画
        bar.update_progress_instant(0.25)
        self.wait(0.5)
        bar.update_progress_instant(0.5)
        self.wait(0.5)
        bar.update_progress_instant(0.75)
        self.wait(0.5)
        bar.update_progress_instant(1.0)  # 测试100%时文字隐藏
        self.wait(1.0)
        bar.update_progress_instant(0.5)  # 测试从100%回到50%时文字显示
        self.wait(2.0)


class BoundaryTest(Scene):
    """测试边界情况"""
    
    def construct(self):
        title = Text("边界情况测试", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        bar = ProgressBar(
            width=8,
            height=0.4,
            position=ORIGIN,
            fill_color=RED,
            show_percentage=True
        )
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(bar))
        self.wait(0.5)
        
        # 测试边界值
        self.play(bar.set_progress(0.0, run_time=1.0))
        self.wait(0.5)
        self.play(bar.set_progress(1.0, run_time=1.0))
        self.wait(0.5)
        # 测试超过1.0的值（应该被限制为1.0）
        self.play(bar.set_progress(1.5, run_time=1.0))
        self.wait(0.5)
        # 测试负值（应该被限制为0.0）
        self.play(bar.set_progress(-0.5, run_time=1.0))
        self.wait(2.0)


class NoPercentageTest(Scene):
    """测试不显示百分比的情况"""
    
    def construct(self):
        title = Text("不显示百分比测试", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        bar = ProgressBar(
            width=10,
            height=0.4,
            position=ORIGIN,
            fill_color=TEAL,
            show_percentage=False  # 不显示百分比
        )
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(bar))
        self.wait(0.5)
        
        # 推进到100%
        self.play(bar.auto_progress(duration=3.0))
        self.wait(2.0)


class CustomStyleTest(Scene):
    """测试自定义样式"""
    
    def construct(self):
        title = Text("自定义样式测试", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        # 不同样式的进度条
        bar1 = ProgressBar(
            width=8,
            height=1,
            position=UP * 2,
            fill_color="#FF6B6B",
            background_color="#4ECDC4",
            border_color=YELLOW,
            border_width=3,
            corner_radius=0.5,
            show_percentage=True,
            percentage_font_size=32,
            percentage_color=WHITE
        )
        label1 = Text("自定义颜色和边框", font_size=18, color=WHITE)
        label1.next_to(bar1, DOWN, buff=0.3)
        
        bar2 = ProgressBar(
            width=8,
            height=0.3,
            position=DOWN * 1,
            fill_color=BLUE,
            background_color="#333333",
            show_percentage=True,
            percentage_font_size=24
        )
        label2 = Text("小尺寸进度条", font_size=18, color=WHITE)
        label2.next_to(bar2, DOWN, buff=0.3)
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(bar1), FadeIn(label1), FadeIn(bar2), FadeIn(label2))
        self.wait(0.5)
        
        # 同时推进
        self.play(
            bar1.auto_progress(duration=3.0),
            bar2.auto_progress(duration=3.0)
        )
        self.wait(2.0)


class ComprehensiveTest(Scene):
    """综合测试：测试所有功能"""
    
    def construct(self):
        title = Text("综合功能测试", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        # 创建多个不同配置的进度条
        bars = []
        labels = []
        
        configs = [
            {"angle": 0, "color": BLUE, "label": "0°", "pos": UP * 2 + LEFT * 4},
            {"angle": 90, "color": RED, "label": "90°", "pos": UP * 0.5 + LEFT * 4},
            {"angle": 180, "color": GREEN, "label": "180°", "pos": DOWN * 0.5 + LEFT * 4},
            {"angle": 270, "color": YELLOW, "label": "270°", "pos": DOWN * 2 + LEFT * 4},
            {"angle": 45, "color": PURPLE, "label": "45°", "pos": UP * 2 + RIGHT * 4},
            {"angle": 135, "color": ORANGE, "label": "135°", "pos": UP * 0.5 + RIGHT * 4},
            {"angle": 225, "color": PINK, "label": "225°", "pos": DOWN * 0.5 + RIGHT * 4},
            {"angle": 315, "color": TEAL, "label": "315°", "pos": DOWN * 2 + RIGHT * 4},
        ]
        
        for i, config in enumerate(configs):
            bar = ProgressBar(
                width=3 if config["angle"] in [90, 270] else 6,
                height=0.3,
                position=config["pos"],
                fill_color=config["color"],
                angle=config["angle"],
                show_percentage=True
            )
            label = Text(config["label"], font_size=16, color=WHITE)
            label.next_to(bar, DOWN, buff=0.2)
            bars.append(bar)
            labels.append(label)
        
        self.play(Write(title))
        self.wait(0.5)
        
        # 显示所有进度条
        anims = [FadeIn(bar) for bar in bars] + [FadeIn(label) for label in labels]
        self.play(*anims)
        self.wait(0.5)
        
        # 同时推进所有进度条到100%，测试文字隐藏
        anims = [bar.auto_progress(duration=4.0) for bar in bars]
        self.play(*anims)
        self.wait(2.0)
        
        # 测试从100%回到50%
        anims = [bar.set_progress(0.5, run_time=1.0) for bar in bars]
        self.play(*anims)
        self.wait(2.0)


# 运行说明
if __name__ == "__main__":
    print("=" * 60)
    print("进度条测试用例")
    print("=" * 60)
    print("\n可用的测试场景：")
    print("  1. BasicProgressTest - 基础功能测试")
    print("  2. PercentageHideTest - 100%时文字隐藏测试（重要）")
    print("  3. AngleTest - 不同角度测试")
    print("  4. AutoProgressTest - 自动进度测试")
    print("  5. ManualProgressTest - 手动设置进度测试")
    print("  6. InstantUpdateTest - 立即更新测试")
    print("  7. BoundaryTest - 边界情况测试")
    print("  8. NoPercentageTest - 不显示百分比测试")
    print("  9. CustomStyleTest - 自定义样式测试")
    print("  10. ComprehensiveTest - 综合功能测试")
    print("\n使用示例：")
    print("  python -m manim -pql progress_bar_example.py PercentageHideTest")
    print("  python -m manim -pql progress_bar_example.py ComprehensiveTest")
    print("\n注意：PercentageHideTest 是测试100%时文字隐藏的关键测试")
