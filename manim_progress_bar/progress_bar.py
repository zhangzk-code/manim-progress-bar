"""
Manim Progress Bar Plugin

A customizable progress bar component for Manim animations.

Features:
- Fully customizable colors, position, height, and width
- Time-based automatic progression
- Smooth animations
- Optional percentage display
- Precise filling to 100%

Usage:
    from progress_bar import ProgressBar
    
    progress = ProgressBar(
        width=10,
        height=0.4,
        position=DOWN * 3.5,
        fill_color=BLUE,
        duration=10.0
    )
    
    self.play(FadeIn(progress))
    self.play(progress.start())  # Auto-progress to 100% in 10 seconds
"""

from manim import *


class ProgressBar(VGroup):
    """
    A customizable progress bar component for Manim animations.
    
    This class provides a fully customizable progress bar with support for:
    - Custom colors, position, size
    - Time-based automatic progression
    - Smooth animations
    - Optional percentage display
    - Precise filling to 100%
    
    Parameters
    ----------
    width : float, optional
        Total width of the progress bar (default: 10)
    height : float, optional
        Height of the progress bar (default: 0.3)
    position : np.ndarray, optional
        Position of the progress bar (default: DOWN * 3.5)
    fill_color : str or Color, optional
        Fill color of the progress bar (default: BLUE)
    background_color : str or Color, optional
        Background color (default: GRAY)
    border_color : str or Color, optional
        Border color (default: WHITE)
    border_width : float, optional
        Border width (default: 2)
    corner_radius : float, optional
        Corner radius for rounded rectangles (default: 0.1)
    show_percentage : bool, optional
        Whether to show percentage text (default: True)
    percentage_font_size : int, optional
        Font size for percentage text (default: 28)
    percentage_color : str or Color, optional
        Color for percentage text (default: WHITE)
    percentage_font : str, optional
        Font family for percentage text (default: "Arial")
    duration : float, optional
        Total duration in seconds for auto-progression (default: None)
    
    Examples
    --------
    Basic usage:
        progress = ProgressBar(width=10, height=0.4, fill_color=BLUE)
        self.play(FadeIn(progress))
        self.play(progress.set_progress(0.5, run_time=2.0))
    
    Auto-progression:
        progress = ProgressBar(duration=10.0)
        self.play(progress.start())  # Progresses to 100% in 10 seconds
    """
    
    def __init__(
        self,
        width=10,                    # 进度条总宽度
        height=0.3,                  # 进度条高度
        position=DOWN * 3.5,         # 进度条位置
        fill_color=BLUE,             # 填充颜色
        background_color=GRAY,       # 背景颜色
        border_color=WHITE,          # 边框颜色
        border_width=2,              # 边框宽度
        corner_radius=0.1,           # 圆角半径
        show_percentage=True,         # 是否显示百分比
        percentage_font_size=28,     # 百分比字体大小（增大默认值）
        percentage_color=WHITE,      # 百分比文字颜色
        percentage_font="Arial",     # 百分比字体
        duration=None,               # 总时长（秒），如果设置则进度条会自动按此时间推进
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.width = width
        self.height = height
        self.fill_color = fill_color
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.corner_radius = corner_radius
        self.show_percentage = show_percentage
        self.percentage_font_size = percentage_font_size
        self.percentage_color = percentage_color
        self.percentage_font = percentage_font
        self.duration = duration  # 存储用户设置的时长
        
        # 创建背景
        self.background = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=corner_radius,
            fill_color=background_color,
            fill_opacity=0.3,
            stroke_color=border_color,
            stroke_width=border_width
        )
        self.add(self.background)
        
        # 创建填充条（初始宽度为很小的值，避免宽度为0时的错误）
        min_width = 0.1  # 最小宽度，避免RoundedRectangle在宽度为0时的错误
        # 填充条高度略小于背景，留出一点边距
        fill_height = height * 0.95
        self.fill_bar = RoundedRectangle(
            width=min_width,
            height=fill_height,
            corner_radius=corner_radius * 0.9,
            fill_color=fill_color,
            fill_opacity=1.0,
            stroke_opacity=0
        )
        # 精确左对齐：左边缘对齐到背景左边缘
        left_edge = self.background.get_left()
        self.fill_bar.move_to([
            left_edge[0] + min_width / 2,
            self.background.get_center()[1],
            0
        ])
        self.add(self.fill_bar)
        
        # 创建百分比文本（使用更美观的字体）
        if show_percentage:
            self.percentage_text = Text(
                "0%",
                font=percentage_font,
                font_size=percentage_font_size,
                color=percentage_color,
                weight=BOLD,  # 加粗
                stroke_width=0.3,  # 添加描边，更清晰
                stroke_color=percentage_color
            )
            self.percentage_text.move_to(self.background.get_center())
            self.add(self.percentage_text)
        
        # 移动到指定位置
        self.move_to(position)
        
        # 当前进度（0-1）
        self.current_progress = 0.0
    
    def set_progress(self, progress, run_time=1.0):
        """
        设置进度条进度
        :param progress: 进度值（0-1之间）
        :param run_time: 动画时间
        :return: 动画对象
        """
        progress = max(0.0, min(1.0, progress))  # 限制在0-1之间
        self.current_progress = progress
        
        # 计算精确的填充宽度（使用背景的实际宽度，确保100%时完全铺满）
        min_width = 0.1
        # 使用背景的实际宽度（右边缘 - 左边缘），确保精确匹配
        bg_left = self.background.get_left()[0]
        bg_right = self.background.get_right()[0]
        usable_width = bg_right - bg_left  # 背景的实际宽度
        
        if progress <= 0:
            new_width = min_width
        elif progress >= 1.0:
            # 100%时铺满整个背景宽度
            new_width = usable_width
        else:
            # 精确计算：progress * 背景实际宽度
            new_width = max(min_width, usable_width * progress)
        
        # 创建动画列表
        anims = []
        
        # 更新填充条宽度（从左到右逐渐填充）
        # 使用重新创建填充条的方法，确保填充颜色完整
        # 创建一个更新函数来重新创建填充条
        start_width = self.fill_bar.width
        fill_height = self.height * 0.95
        
        def update_fill_bar(mob, alpha):
            """更新填充条：重新创建以确保填充颜色完整"""
            # 计算当前宽度（线性插值）
            current_width = start_width + (new_width - start_width) * alpha
            # 确保最小宽度
            current_width = max(0.1, current_width)
            
            # 重新创建填充条，确保填充颜色完整
            new_fill_bar = RoundedRectangle(
                width=current_width,
                height=fill_height,
                corner_radius=self.corner_radius * 0.9,
                fill_color=self.fill_color,
                fill_opacity=1.0,
                stroke_opacity=0
            )
            
            # 计算位置（左边缘对齐）
            fill_center_x = bg_left + current_width / 2
            fill_center_y = self.background.get_center()[1]
            new_fill_bar.move_to([fill_center_x, fill_center_y, 0])
            
            # 替换旧的填充条
            self.remove(self.fill_bar)
            self.fill_bar = new_fill_bar
            self.add(self.fill_bar)
        
        anims.append(
            UpdateFromAlphaFunc(
                self,
                update_fill_bar,
                run_time=run_time
            )
        )
        
        # 更新百分比文本
        if self.show_percentage:
                percentage = int(progress * 100)
                new_text = Text(
                    f"{percentage}%",
                    font=self.percentage_font,
                    font_size=self.percentage_font_size,
                    color=self.percentage_color,
                    weight=BOLD,
                    stroke_width=0.3,
                    stroke_color=self.percentage_color
                )
                new_text.move_to(self.background.get_center())
                anims.append(
                    Transform(self.percentage_text, new_text)
                )
        
        return AnimationGroup(*anims, run_time=run_time)
    
    
    def update_progress_instant(self, progress):
        """
        立即更新进度（无动画）
        :param progress: 进度值（0-1）
        """
        progress = max(0.0, min(1.0, progress))
        self.current_progress = progress
        
        # 使用背景的实际宽度（右边缘 - 左边缘），确保精确匹配
        bg_left = self.background.get_left()[0]
        bg_right = self.background.get_right()[0]
        usable_width = bg_right - bg_left  # 背景的实际宽度
        
        min_width = 0.1
        
        if progress <= 0:
            new_width = min_width
        elif progress >= 1.0:
            # 100%时铺满整个背景宽度
            new_width = usable_width
        else:
            new_width = max(min_width, usable_width * progress)
        
        
        # 重新创建填充条，确保填充颜色完整
        fill_height = self.height * 0.95
        self.remove(self.fill_bar)
        self.fill_bar = RoundedRectangle(
            width=new_width,
            height=fill_height,
            corner_radius=self.corner_radius * 0.9,
            fill_color=self.fill_color,
            fill_opacity=1.0,
            stroke_opacity=0
        )
        # 精确左对齐：填充条左边缘对齐到背景左边缘
        fill_center_x = bg_left + new_width / 2
        self.fill_bar.move_to([
            fill_center_x,
            self.background.get_center()[1],
            0
        ])
        
        if self.show_percentage:
            percentage = int(progress * 100)
            new_text = Text(
                f"{percentage}%",
                font="Arial",
                font_size=self.percentage_font_size,
                color=self.percentage_color,
                weight=BOLD,
                stroke_width=0.5,
                stroke_color=self.percentage_color
            )
            new_text.move_to(self.background.get_center())
            self.remove(self.percentage_text)
            self.percentage_text = new_text
            self.add(self.percentage_text)
    
    def auto_progress(self, duration=None, start_progress=0.0, end_progress=1.0):
        """
        自动推进进度条（根据时间参数自动计算每一帧的进度）
        按照指定时间计算每一帧应该往前走多少，达到时间后进度条走满
        :param duration: 总时长（秒），如果为None则使用初始化时设置的duration
        :param start_progress: 起始进度（0-1），默认0
        :param end_progress: 结束进度（0-1），默认1.0（100%）
        :return: 动画对象
        """
        # 使用用户设置的duration，如果没有则使用参数中的duration
        if duration is None:
            if self.duration is None:
                duration = 5.0  # 默认5秒
            else:
                duration = self.duration
        
        start_progress = max(0.0, min(1.0, start_progress))
        end_progress = max(0.0, min(1.0, end_progress))
        
        # 初始化起始状态
        self.update_progress_instant(start_progress)
        
        # 清除之前的updater（如果存在）
        self.clear_updaters()
        
        # 使用ValueTracker跟踪时间（从0到duration）
        # 存储为实例变量，确保updater能正确访问
        self._time_tracker = ValueTracker(0.0)
        self._auto_duration = duration
        self._auto_start_progress = start_progress
        self._auto_end_progress = end_progress
        self._auto_progress_range = end_progress - start_progress
        
        # 标记是否已经清理过updater，避免重复清理
        self._updater_cleared = False
        
        # 创建更新函数：根据时间计算进度
        def update_progress(mob):
            # 获取当前时间
            current_time = self._time_tracker.get_value()
            
            # 根据时间计算进度（线性插值）
            # progress = start + (current_time / duration) * range
            if current_time <= 0:
                progress = self._auto_start_progress
            elif current_time >= self._auto_duration:
                progress = self._auto_end_progress
                # 当达到目标进度且时间已到，标记需要清理updater
                # 实际清理将在动画的update_func中完成，避免在updater执行过程中清理
                if not self._updater_cleared:
                    self._updater_cleared = True
            else:
                # 线性插值：每一帧根据当前时间计算精确进度
                progress = self._auto_start_progress + (current_time / self._auto_duration) * self._auto_progress_range
            
            # 更新填充条宽度（使用背景的实际宽度，确保100%时完全铺满）
            min_width = 0.1
            # 使用背景的实际宽度（右边缘 - 左边缘），确保精确匹配
            bg_left = self.background.get_left()[0]
            bg_right = self.background.get_right()[0]
            usable_width = bg_right - bg_left  # 背景的实际宽度
            
            if progress <= 0:
                new_width = min_width
            elif progress >= 1.0:
                # 100%时铺满整个背景宽度，确保完全填充
                # 使用背景的完整宽度，不留任何空隙
                new_width = usable_width
                # 确保 progress 被设置为 1.0，避免浮点数精度问题
                progress = 1.0
            else:
                new_width = max(min_width, usable_width * progress)
            
            # 更新填充条宽度和位置
            # 在100%时，直接设置填充条从背景左边缘到右边缘
            # 重新创建填充条，确保填充颜色完整
            fill_height = self.height * 0.95
            self.remove(self.fill_bar)
            
            if progress >= 1.0:
                # 100%时，确保填充条完全铺满背景
                self.fill_bar = RoundedRectangle(
                    width=usable_width,
                    height=fill_height,
                    corner_radius=self.corner_radius * 0.9,
                    fill_color=self.fill_color,
                    fill_opacity=1.0,
                    stroke_opacity=0
                )
                # 左边缘对齐到背景左边缘
                self.fill_bar.align_to(self.background, LEFT)
                # 确保垂直居中
                self.fill_bar.align_to(self.background, DOWN)
                self.fill_bar.shift(UP * (self.background.get_center()[1] - self.fill_bar.get_center()[1]))
            else:
                # 非100%时，使用正常的计算方式
                self.fill_bar = RoundedRectangle(
                    width=new_width,
                    height=fill_height,
                    corner_radius=self.corner_radius * 0.9,
                    fill_color=self.fill_color,
                    fill_opacity=1.0,
                    stroke_opacity=0
                )
                # 更新填充条位置（精确左对齐）
                # 填充条左边缘始终对齐到背景左边缘，只改变宽度实现填充效果
                fill_center_x = bg_left + new_width / 2
                fill_center_y = self.background.get_center()[1]
                self.fill_bar.move_to([fill_center_x, fill_center_y, 0])
            
            self.add(self.fill_bar)
            
            # 更新百分比文本
            if self.show_percentage:
                percentage = int(progress * 100)
                new_text = Text(
                    f"{percentage}%",
                    font=self.percentage_font,
                    font_size=self.percentage_font_size,
                    color=self.percentage_color,
                    weight=BOLD,
                    stroke_width=0.3,
                    stroke_color=self.percentage_color
                )
                new_text.move_to(self.background.get_center())
                self.percentage_text.become(new_text)
            
            # 更新当前进度
            self.current_progress = progress
        
        # 绑定更新函数到整个VGroup
        # updater会在每一帧被调用，根据time_tracker的值更新进度
        self.add_updater(update_progress)
        
        # 创建动画：让time_tracker从0变化到duration
        # 当time_tracker变化时，updater会自动调用，更新进度条
        # 使用 UpdateFromAlphaFunc 动画，根据动画进度更新 ValueTracker
        # 这样可以确保 run_time 被正确设置
        def update_func(mob, alpha):
            """根据动画进度更新 time_tracker，并在动画结束时清理updater
            alpha: 动画进度，从0到1
            """
            # alpha 从 0 到 1，对应 time_tracker 从 0 到 duration
            # time_tracker 的值直接对应时间，updater 会根据这个时间计算进度
            current_time = alpha * self._auto_duration
            self._time_tracker.set_value(current_time)
            
            # 当动画结束时（alpha >= 1.0），清理updater
            # 这样可以确保在进度条到达100%后自动清理，无需手动调用
            if alpha >= 1.0 and not self._updater_cleared:
                self.clear_updaters()
                self._updater_cleared = True
        
        # 创建 UpdateFromAlphaFunc 动画，直接设置 run_time
        # UpdateFromAlphaFunc 会自动传递 alpha 参数（动画进度 0-1）
        anim = UpdateFromAlphaFunc(
            self._time_tracker,
            update_func,
            run_time=duration
        )
        
        # 返回动画对象
        # 注意：动画执行过程中，updater会在每一帧更新进度
        # 当进度达到目标值（通常是100%）时，updater会自动清理
        return anim
    
    def start(self):
        """
        开始自动推进进度条（使用初始化时设置的duration）
        如果初始化时没有设置duration，则使用默认值5秒
        :return: 动画对象
        """
        return self.auto_progress()

