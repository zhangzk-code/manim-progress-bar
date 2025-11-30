from manim import *
from manim_progress_bar.progress_bar import ProgressBar


class SimpleProgressExample(Scene):
    """简单进度条示例"""
    
    def construct(self):
        # 创建一个自定义进度条，在初始化时设置duration
        # duration参数由用户设置，进度条会自动按此时间推进
        progress = ProgressBar(
            width=10,              # 宽度
            height=0.4,            # 高度
            position=UP * 3.5,     # 位置（底部）
            fill_color="#00D4FF",  # 填充颜色（亮蓝色）
            background_color="#333333",  # 背景颜色（深灰）
            border_color="#666666",  # 边框颜色
            border_width=2,        # 边框宽度
            corner_radius=0.1,     # 圆角
            show_percentage=True,   # 显示百分比
            percentage_font_size=24,  # 百分比字体大小
            percentage_color=WHITE,  # 百分比文字颜色
            duration=10.0          # 用户设置的总时长：10秒
        )
        
        # 显示标题
        self.play(FadeIn(progress))
        self.wait(0.5)
        
        # 开始自动推进进度条（使用初始化时设置的duration=10.0）
        # 每一帧都会根据当前时间计算精确的进度值
        # 10秒后进度条会精确达到100%
        # 注意：start() 返回的动画已经设置了正确的 run_time，不需要再指定
        anim = progress.start()  # 使用初始化时设置的duration=10.0
        self.play(anim)  # 动画会自动使用 duration=10.0 作为 run_time
        
        self.wait(2.0)


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


# 运行说明
if __name__ == "__main__":
    print("使用以下命令渲染：")
    print("  python -m manim -pql progress_bar_example.py SimpleProgressExample")
    print("  python -m manim -pql progress_bar_example.py CustomProgressExample")

