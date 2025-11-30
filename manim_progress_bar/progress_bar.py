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
import numpy as np
import logging

# 配置日志记录器
logger = logging.getLogger(__name__)

# 如果 logger 还没有处理器，则添加一个控制台处理器
if not logger.handlers:
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # 创建格式器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # 添加处理器到 logger
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    
    # 防止日志传播到根 logger（避免重复输出）
    logger.propagate = False


class ProgressBar(VGroup):
    """
    A customizable progress bar component for Manim animations.
    
    This class provides a fully customizable progress bar with support for:
    - Custom colors, position, size
    - Time-based automatic progression
    - Smooth animations
    - Optional percentage display
    - Precise filling to 100%
    - Customizable angle (supports any angle from 0 to 360 degrees)
    
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
    angle : float, optional
        Angle of the progress bar in degrees (default: 0).
        The progress bar rotates clockwise from the positive x-axis.
        - 0 degrees: Horizontal, growing from left to right
        - 90 degrees: Vertical, growing from bottom to top
        - 180 degrees: Horizontal, growing from right to left
        - 270 degrees: Vertical, growing from top to bottom
        - Any other angle: Diagonal progress bar
    
    Examples
    --------
    Basic usage:
        progress = ProgressBar(width=10, height=0.4, fill_color=BLUE)
        self.play(FadeIn(progress))
        self.play(progress.set_progress(0.5, run_time=2.0))
    
    Auto-progression:
        progress = ProgressBar(duration=10.0)
        self.play(progress.start())  # Progresses to 100% in 10 seconds
    
    Different angles:
        # Horizontal (0 degrees, default)
        progress1 = ProgressBar(angle=0)
        
        # Vertical (90 degrees)
        progress2 = ProgressBar(angle=90)
        
        # Diagonal (45 degrees)
        progress3 = ProgressBar(angle=45)
        
        # Any angle
        progress4 = ProgressBar(angle=135)
    """
    
    # 常量
    FILL_HEIGHT_RATIO = 0.95  # 填充条高度相对于原始高度的比例
    BASE_MIN_SIZE = 0.1  # 基础最小尺寸，避免RoundedRectangle在尺寸为0时的错误
    
    @staticmethod
    def _get_direction_vector(angle_deg, angle_rad):
        """
        计算精确的方向向量，对于特殊角度使用精确值避免浮点数误差
        :param angle_deg: 角度（度）
        :param angle_rad: 角度（弧度）
        :return: 单位方向向量 [x, y, 0]
        """
        angle_deg = angle_deg % 360
        if abs(angle_deg - 0) < 1e-6 or abs(angle_deg - 360) < 1e-6:
            return np.array([1.0, 0.0, 0.0])
        elif abs(angle_deg - 90) < 1e-6:
            return np.array([0.0, 1.0, 0.0])
        elif abs(angle_deg - 180) < 1e-6:
            return np.array([-1.0, 0.0, 0.0])
        elif abs(angle_deg - 270) < 1e-6:
            return np.array([0.0, -1.0, 0.0])
        else:
            direction_vec = np.array([np.cos(angle_rad), np.sin(angle_rad), 0.0])
            # 归一化方向向量，确保是单位向量
            norm = np.linalg.norm(direction_vec[:2])
            if norm > 1e-10:
                return np.array([direction_vec[0] / norm, direction_vec[1] / norm, 0.0])
            return direction_vec
    
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
        percentage_font="Sans",     # 百分比字体
        duration=None,               # 总时长（秒），如果设置则进度条会自动按此时间推进
        angle=0,                     # 进度条角度（度），0度为水平向右，按顺时针旋转
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # 存储原始宽度和高度（使用不同的属性名，避免与 VGroup 的属性冲突）
        self.original_width = width
        self.original_height = height
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
        
        # 存储角度（转换为弧度）
        self.angle = angle
        self.angle_rad = np.radians(angle)
        
        # 计算动态最小尺寸：对于圆角矩形，宽度至少需要是2倍的圆角半径，否则会被挤压变形
        # 填充条使用 corner_radius * 0.9，所以最小宽度应该是 2 * (corner_radius * 0.9)
        fill_corner_radius = corner_radius * 0.9
        self.MIN_SIZE = max(self.BASE_MIN_SIZE, 2 * fill_corner_radius)
        
        # 创建背景（始终使用 width 和 height，不交换）
        self.background = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=corner_radius,
            fill_color=background_color,
            fill_opacity=0.3,
            stroke_color=border_color,
            stroke_width=border_width
        )
        
        # 计算沿角度方向的单位向量（使用精确值避免浮点数误差）
        direction_vec = self._get_direction_vector(self.angle, self.angle_rad)
        
        self.bg_half_length = width / 2
        
        # 旋转背景到指定角度
        self.background.rotate(self.angle_rad)
        self.add(self.background)
        
        # 创建填充条（初始宽度很小）
        fill_height = self.original_height * self.FILL_HEIGHT_RATIO
        self.fill_bar = self._create_fill_bar(self.MIN_SIZE, fill_height)
        
        # 计算起点位置（沿角度方向的负方向，从中心点开始）
        bg_center = self.background.get_center()
        start_offset = -self.bg_half_length + self.MIN_SIZE / 2
        start_pos = bg_center + direction_vec * start_offset
        
        # 旋转填充条到对应角度并设置位置
        self.fill_bar.rotate(self.angle_rad)
        self.fill_bar.move_to(start_pos)
        self.add(self.fill_bar)
        
        # 创建百分比文本
        if show_percentage:
            self.percentage_text = self._create_percentage_text(0)
            self.percentage_text.move_to(self.background.get_center())
            self.add(self.percentage_text)
        
        # 移动到指定位置
        self.move_to(position)
        
        # 当前进度（0-1）
        self.current_progress = 0.0
    
    def _create_fill_bar(self, width, height):
        """创建填充条"""
        fill_bar = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=self.corner_radius * 0.9,  # 填充条圆角半径略小于背景
            fill_color=self.fill_color,
            fill_opacity=1.0,
            stroke_width=0,  # 明确设置描边宽度为0
            stroke_opacity=0
        )
        # 明确设置所有颜色相关属性，确保颜色饱满，无描边
        fill_bar.set_fill(color=self.fill_color, opacity=1.0)
        fill_bar.set_stroke(width=0, opacity=0)
        fill_bar.set_opacity(1.0)
        return fill_bar
    
    def _create_percentage_text(self, percentage):
        """创建百分比文本"""
        return Text(
            f"{percentage}%",
            font=self.percentage_font,
            font_size=self.percentage_font_size,
            color=self.percentage_color,
            weight=BOLD,
            stroke_width=0.3,
            stroke_color=self.percentage_color
        )
    
    def _update_fill_bar(self, width, height, center):
        """更新填充条的尺寸和位置"""
        # 创建新的填充条
        new_fill_bar = self._create_fill_bar(width, height)
        new_fill_bar.rotate(self.angle_rad)
        new_fill_bar.move_to(center)
        # 在替换之前，强制设置颜色和不透明度，确保颜色饱满，无描边
        new_fill_bar.set_fill(color=self.fill_color, opacity=1.0)
        new_fill_bar.set_stroke(width=0, opacity=0)
        new_fill_bar.set_opacity(1.0)
        # 使用 become 直接替换，避免 remove/add 可能导致的颜色混合问题
        self.fill_bar.become(new_fill_bar)
        # 再次强制设置颜色和描边，确保 become 后颜色仍然正确，无白色框
        self.fill_bar.set_fill(color=self.fill_color, opacity=1.0)
        self.fill_bar.set_stroke(width=0, opacity=0)
        self.fill_bar.set_opacity(1.0)
        
    
    def _calculate_fill_bar_properties(self, progress):
        """
        根据进度和角度计算填充条的属性（宽度/高度和位置）
        :param progress: 进度值（0-1）
        :return: (width, height, center_x, center_y, center_z) 元组
        """
        # 计算沿角度方向的单位向量
        direction_vec = self._get_direction_vector(self.angle, self.angle_rad)
        
        # 背景在角度方向上的总长度
        bg_total_length = 2 * self.bg_half_length
        
        # 填充条的高度
        fill_height = self.original_height * self.FILL_HEIGHT_RATIO
        
        # 计算填充条在角度方向上的长度
        if progress <= 0:
            fill_length = self.MIN_SIZE
        elif progress >= 1.0:
            fill_length = bg_total_length
        else:
            fill_length = max(self.MIN_SIZE, bg_total_length * progress)
        
        # 计算填充条的中心位置
        bg_center = self.background.get_center()
        start_offset = -self.bg_half_length + fill_length / 2
        fill_center = bg_center + direction_vec * start_offset
        
        return (fill_length, fill_height, fill_center[0], fill_center[1], fill_center[2])
    
    def set_progress(self, progress, run_time=1.0):
        """
        设置进度条进度
        :param progress: 进度值（0-1之间）
        :param run_time: 动画时间
        :return: 动画对象
        """
        progress = max(0.0, min(1.0, progress))  # 限制在0-1之间
        
        # 计算起始填充条属性（使用当前进度）
        start_width, start_height, start_x, start_y, start_z = self._calculate_fill_bar_properties(self.current_progress)
        
        # 计算目标填充条属性
        target_width, target_height, target_x, target_y, target_z = self._calculate_fill_bar_properties(progress)
        
        # 更新当前进度
        self.current_progress = progress
        
        # 创建动画列表
        anims = []
        
        def update_fill_bar(mob, alpha):
            """更新填充条：重新创建以确保填充颜色完整"""
            # 计算当前属性（线性插值）
            current_width = start_width + (target_width - start_width) * alpha
            current_height = start_height + (target_height - start_height) * alpha
            current_x = start_x + (target_x - start_x) * alpha
            current_y = start_y + (target_y - start_y) * alpha
            current_z = start_z + (target_z - start_z) * alpha
            
            # 确保最小尺寸
            current_width = max(self.MIN_SIZE, current_width)
            current_height = max(self.MIN_SIZE, current_height)
            
            # 更新填充条
            self._update_fill_bar(current_width, current_height, [current_x, current_y, current_z])
            
            # 强制刷新颜色属性，防止动画过程中颜色变淡或被混合
            # 必须在添加到 VGroup 之后再次设置，确保颜色正确，无白色框
            if self.fill_bar in self.submobjects:
                self.fill_bar.set_fill(color=self.fill_color, opacity=1.0)
                self.fill_bar.set_stroke(width=0, opacity=0)
                self.fill_bar.set_opacity(1.0)
        
        anims.append(
            UpdateFromAlphaFunc(
                self,
                update_fill_bar,
                run_time=run_time
            )
        )
        
        # 更新百分比文本
        if self.show_percentage:
            if progress >= 1.0:
                # 进度达到100%时，先隐藏文本，然后在动画结束时移除
                def hide_and_remove(mob, alpha):
                    # 在动画过程中逐渐隐藏
                    opacity = max(0.0, 1.0 - alpha)
                    self.percentage_text.set_opacity(opacity)
                    self.percentage_text.set_fill_opacity(opacity)
                    self.percentage_text.set_stroke_opacity(opacity)
                    # 动画结束时移除
                    if alpha >= 1.0 and self.percentage_text in self.submobjects:
                        self.remove(self.percentage_text)
                
                anims.append(UpdateFromAlphaFunc(self, hide_and_remove, run_time=run_time))
            else:
                # 确保文本存在且可见
                if self.percentage_text not in self.submobjects:
                    self.add(self.percentage_text)
                current_opacity = self.percentage_text.get_opacity()
                if current_opacity is None or current_opacity < 1.0:
                    anims.append(self.percentage_text.animate.set_opacity(1.0).set_fill_opacity(1.0).set_stroke_opacity(1.0))
                
                # 更新文本内容
                percentage = int(progress * 100)
                new_text = self._create_percentage_text(percentage)
                new_text.move_to(self.background.get_center())
                anims.append(Transform(self.percentage_text, new_text))
        
        return AnimationGroup(*anims, run_time=run_time)
    
    
    def update_progress_instant(self, progress):
        """
        立即更新进度（无动画）
        :param progress: 进度值（0-1）
        """
        progress = max(0.0, min(1.0, progress))
        self.current_progress = progress
        
        # 使用辅助方法计算填充条属性
        fill_width, fill_height, fill_center_x, fill_center_y, fill_center_z = self._calculate_fill_bar_properties(progress)
        
        # 更新填充条
        self._update_fill_bar(fill_width, fill_height, [fill_center_x, fill_center_y, fill_center_z])
        
        # 更新百分比文本
        if self.show_percentage:
            if progress >= 1.0:
                # 进度达到100%时，直接移除百分比文本
                self.remove(self.percentage_text)
            else:
                # 确保文本存在且可见
                if self.percentage_text not in self.submobjects:
                    self.add(self.percentage_text)
                self.percentage_text.set_opacity(1.0)
                self.percentage_text.set_fill_opacity(1.0)
                self.percentage_text.set_stroke_opacity(1.0)
                
                # 更新文本内容
                percentage = int(progress * 100)
                new_text = self._create_percentage_text(percentage)
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
            
            # 确保 progress 被限制在有效范围内
            if progress >= 1.0:
                progress = 1.0
            
            # 使用辅助方法计算填充条属性
            fill_width, fill_height, fill_center_x, fill_center_y, fill_center_z = self._calculate_fill_bar_properties(progress)
            
            # 更新填充条
            self._update_fill_bar(fill_width, fill_height, [fill_center_x, fill_center_y, fill_center_z])
            
            # 强制刷新颜色属性，防止动画过程中颜色变淡或被混合，无白色框
            if self.fill_bar in self.submobjects:
                self.fill_bar.set_fill(color=self.fill_color, opacity=1.0)
                self.fill_bar.set_stroke(width=0, opacity=0)
                self.fill_bar.set_opacity(1.0)
            
            # 更新百分比文本
            if self.show_percentage:
                if progress >= 1.0:
                    # 进度达到100%时，直接移除百分比文本
                    if self.percentage_text in self.submobjects:
                        self.remove(self.percentage_text)
                else:
                    # 确保文本存在且可见
                    if self.percentage_text not in self.submobjects:
                        self.add(self.percentage_text)
                    self.percentage_text.set_opacity(1.0)
                    self.percentage_text.set_fill_opacity(1.0)
                    self.percentage_text.set_stroke_opacity(1.0)
                    
                    # 更新文本内容
                    percentage = int(progress * 100)
                    new_text = self._create_percentage_text(percentage)
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
            
            # 当动画结束时（alpha >= 1.0），确保进度条到达最终状态后再清理updater
            if alpha >= 1.0 and not self._updater_cleared:
                # 确保进度条已经更新到最终状态
                final_progress = self._auto_end_progress
                fill_width, fill_height, fill_center_x, fill_center_y, fill_center_z = self._calculate_fill_bar_properties(final_progress)
                self._update_fill_bar(fill_width, fill_height, [fill_center_x, fill_center_y, fill_center_z])
                self.current_progress = final_progress
                
                # 更新百分比文本
                if self.show_percentage:
                    if final_progress >= 1.0:
                        if self.percentage_text in self.submobjects:
                            self.remove(self.percentage_text)
                    else:
                        if self.percentage_text not in self.submobjects:
                            self.add(self.percentage_text)
                        self.percentage_text.set_opacity(1.0)
                        self.percentage_text.set_fill_opacity(1.0)
                        self.percentage_text.set_stroke_opacity(1.0)
                        percentage = int(final_progress * 100)
                        new_text = self._create_percentage_text(percentage)
                        new_text.move_to(self.background.get_center())
                        self.percentage_text.become(new_text)
                
                # 清理updater
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

