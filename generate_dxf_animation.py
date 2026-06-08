"""
生成 CAD 能识别的动画线条 (DXF 格式)
支持：AutoCAD、LibreCAD、其他 CAD 软件
"""

import ezdxf
import math
from pathlib import Path

def create_line_animation_dxf(output_path="animation_lines.dxf", 
                               num_frames=30,
                               line_type="sine"):
    """
    生成包含动画线条的 DXF 文件
    
    参数：
    - output_path: 输出文件路径
    - num_frames: 帧数
    - line_type: 线条类型 ("sine", "circle", "spiral")
    """
    
    # 创建新的 DXF 文档
    doc = ezdxf.new('R2000')
    msp = doc.modelspace()
    
    # 设置线条颜色
    colors = [1, 2, 3, 4, 5, 6, 7]  # CAD 颜色索引
    
    if line_type == "sine":
        # 生成正弦波动画线条
        create_sine_wave(msp, num_frames, colors)
    
    elif line_type == "circle":
        # 生成圆形动画线条
        create_circle_animation(msp, num_frames, colors)
    
    elif line_type == "spiral":
        # 生成螺旋线动画
        create_spiral_animation(msp, num_frames, colors)
    
    # 保存文件
    doc.saveas(output_path)
    print(f"✓ DXF 文件已生成: {output_path}")
    return output_path


def create_sine_wave(msp, num_frames, colors):
    """创建正弦波线条"""
    x_start = 0
    x_end = 100
    y_base = 0
    amplitude = 10
    
    for frame in range(num_frames):
        phase = (frame / num_frames) * 2 * math.pi
        
        points = []
        for x in range(x_start, x_end + 1):
            y = y_base + amplitude * math.sin((x / 10) + phase)
            points.append((x, y))
        
        # 用折线连接所有点
        if len(points) > 1:
            color_idx = colors[frame % len(colors)]
            
            for i in range(len(points) - 1):
                line = msp.add_line(points[i], points[i + 1])
                line.dxf.color = color_idx
                # 添加图层标识帧号
                line.dxf.layer = f"Frame_{frame:03d}"


def create_circle_animation(msp, num_frames, colors):
    """创建圆形扫描线条"""
    center = (50, 50)
    radius_base = 20
    
    for frame in range(num_frames):
        angle = (frame / num_frames) * 2 * math.pi
        
        # 计算半径变化
        radius = radius_base + 10 * math.sin(angle)
        
        # 绘制圆弧或完整圆
        circle = msp.add_circle(center, radius)
        circle.dxf.color = colors[frame % len(colors)]
        circle.dxf.layer = f"Frame_{frame:03d}"
        
        # 添加径向线
        end_x = center[0] + radius * math.cos(angle)
        end_y = center[1] + radius * math.sin(angle)
        
        line = msp.add_line(center, (end_x, end_y))
        line.dxf.color = colors[frame % len(colors)]
        line.dxf.layer = f"Frame_{frame:03d}"


def create_spiral_animation(msp, num_frames, colors):
    """创建螺旋线动画"""
    center = (50, 50)
    
    for frame in range(num_frames):
        points = []
        max_angle = (frame / num_frames) * 8 * math.pi  # 多圈螺旋
        
        for angle in [i * 0.1 for i in range(int(max_angle * 10) + 1)]:
            radius = 5 + (angle / (8 * math.pi)) * 30  # 半径逐渐增大
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))
        
        # 绘制螺旋线
        if len(points) > 1:
            color_idx = colors[frame % len(colors)]
            
            for i in range(len(points) - 1):
                line = msp.add_line(points[i], points[i + 1])
                line.dxf.color = color_idx
                line.dxf.layer = f"Frame_{frame:03d}"


def create_gcode_animation(output_path="animation.gcode"):
    """
    生成 G-code 格式（用于 CNC 机器）
    """
    with open(output_path, 'w') as f:
        f.write("; CAD 动画线条 - G-code 格式\n")
        f.write("G21 ; 使用毫米\n")
        f.write("G90 ; 绝对坐标\n\n")
        
        # 生成正弦波 G-code
        x_start, x_end = 0, 100
        y_base = 50
        amplitude = 10
        
        f.write("G0 Z5 ; 抬起刀头\n")
        f.write(f"G0 X{x_start} Y{y_base} ; 移动到起点\n")
        f.write("G1 Z0 F100 ; 降低刀头\n\n")
        
        for x in range(x_start, x_end + 1):
            y = y_base + amplitude * math.sin(x / 10)
            f.write(f"G1 X{x} Y{y:.2f} F200\n")
        
        f.write("G0 Z5 ; 抬起刀头\n")
        f.write("M30 ; 程序结束\n")
    
    print(f"✓ G-code 文件已生成: {output_path}")
    return output_path


def create_svg_animation(output_path="animation.svg"):
    """
    生成 SVG 格式动画（可在浏览器中预览）
    """
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            @keyframes wave {
                0% { stroke-dashoffset: 1000; }
                100% { stroke-dashoffset: 0; }
            }
            .line {
                stroke: blue;
                stroke-width: 2;
                fill: none;
                stroke-dasharray: 1000;
                animation: wave 3s linear infinite;
            }
        </style>
    </defs>
    
    <!-- 正弦波 -->
    <path class="line" d="M 10,100 Q 20,70 30,100 T 50,100 T 70,100 T 90,100 T 110,100 T 130,100 T 150,100 T 170,100 T 190,100" />
    
    <!-- 圆形 -->
    <circle cx="300" cy="100" r="40" class="line" />
    
    <!-- 螺旋线 -->
    <path class="line" d="M 350,100 Q 360,80 370,100 T 390,100" />
</svg>'''
    
    with open(output_path, 'w') as f:
        f.write(svg_content)
    
    print(f"✓ SVG 动画文件已生成: {output_path}")
    return output_path


if __name__ == "__main__":
    # 生成 DXF 文件（CAD 格式）
    print("=" * 50)
    print("生成 CAD 动画线条")
    print("=" * 50)
    
    # 生成三种不同的动画
    create_line_animation_dxf("sine_wave.dxf", num_frames=20, line_type="sine")
    create_line_animation_dxf("circle.dxf", num_frames=20, line_type="circle")
    create_line_animation_dxf("spiral.dxf", num_frames=20, line_type="spiral")
    
    # 生成 G-code（用于 CNC）
    create_gcode_animation("animation.gcode")
    
    # 生成 SVG（用于浏览器预览）
    create_svg_animation("animation.svg")
    
    print("\n✓ 所有文件已生成完成！")
    print("  - sine_wave.dxf (正弦波)")
    print("  - circle.dxf (圆形)")
    print("  - spiral.dxf (螺旋线)")
    print("  - animation.gcode (G-code)")
    print("  - animation.svg (SVG 动画)")
