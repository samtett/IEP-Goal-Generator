import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon, Wedge, Arc
import numpy as np

# Create figure with modern gradient background
fig, ax = plt.subplots(figsize=(22, 13), facecolor='#f8f9fa')
ax.set_xlim(0, 22)
ax.set_ylim(0, 13)
ax.axis('off')

# Professional color palette inspired by the references
COLORS = {
    'blue': '#4A90E2',
    'teal': '#1ABC9C',
    'orange': '#FF8C42',
    'purple': '#8E44AD',
    'red': '#E74C3C',
    'green': '#27AE60',
    'navy': '#2C3E50',
    'yellow': '#F39C12',
    'pink': '#E91E63',
}

def draw_container(ax, x, y, width, height, title, color, alpha=0.15):
    """Draw a rounded container box with title"""
    # Container background
    container = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.15",
        facecolor=color,
        edgecolor=color,
        linewidth=3.5,
        alpha=alpha,
        zorder=0
    )
    ax.add_patch(container)
    
    # Title bar
    title_bar = FancyBboxPatch(
        (x + 0.1, y + height - 0.5), width - 0.2, 0.4,
        boxstyle="round,pad=0.05",
        facecolor=color,
        edgecolor='none',
        linewidth=0,
        alpha=0.9,
        zorder=1
    )
    ax.add_patch(title_bar)
    
    # Title text
    ax.text(x + width/2, y + height - 0.3, title,
            ha='center', va='center',
            fontsize=13, fontweight='bold',
            color='white', zorder=2,
            family='sans-serif')

def draw_component(ax, x, y, width, height, label, color, icon_type=None, subtitle=None):
    """Draw a modern component box with icon and label"""
    # Shadow effect
    shadow = FancyBboxPatch(
        (x + 0.08, y - 0.08), width, height,
        boxstyle="round,pad=0.1",
        facecolor='#000000',
        edgecolor='none',
        alpha=0.15,
        zorder=1
    )
    ax.add_patch(shadow)
    
    # Main box
    box = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.1",
        facecolor=color,
        edgecolor='white',
        linewidth=3,
        alpha=0.95,
        zorder=2
    )
    ax.add_patch(box)
    
    # Icon at top
    if icon_type:
        icon_y = y + height - 0.5
        draw_icon(ax, x + width/2, icon_y, icon_type, color='white')
    
    # Label
    label_y = y + 0.45 if subtitle else y + height/2 - 0.15
    ax.text(x + width/2, label_y, label,
            ha='center', va='center',
            fontsize=11.5, fontweight='bold',
            color='white', zorder=3,
            family='sans-serif')
    
    # Subtitle
    if subtitle:
        ax.text(x + width/2, y + 0.2, subtitle,
                ha='center', va='center',
                fontsize=9, fontweight='normal',
                color='white', alpha=0.9, zorder=3,
                family='sans-serif', style='italic')

def draw_icon(ax, x, y, icon_type, color='white', size=0.3):
    """Draw modern icons"""
    if icon_type == 'user':
        # User silhouette
        head = Circle((x, y + 0.08), size*0.35, facecolor=color, 
                     edgecolor='none', linewidth=0, zorder=4, alpha=0.95)
        ax.add_patch(head)
        body = Wedge((x, y - 0.15), size*0.6, 0, 180,
                    facecolor=color, edgecolor='none', zorder=4, alpha=0.95)
        ax.add_patch(body)
    
    elif icon_type == 'database':
        # Stacked database cylinders
        for i, offset in enumerate([0, 0.12, 0.24]):
            top = mpatches.Ellipse((x, y + offset + 0.06), size*0.6, size*0.15, 
                                  facecolor=color, edgecolor='none', zorder=4, alpha=0.95)
            rect = Rectangle((x - size*0.3, y + offset - 0.02), size*0.6, 0.08, 
                           facecolor=color, edgecolor='none', zorder=4, alpha=0.95)
            ax.add_patch(rect)
            ax.add_patch(top)
    
    elif icon_type == 'document':
        # Document with lines
        doc = Rectangle((x - size*0.35, y - 0.25), size*0.6, size*0.8, 
                       facecolor=color, edgecolor='none', zorder=4, alpha=0.95, 
                       transform=ax.transData)
        ax.add_patch(doc)
        # Folded corner
        fold_tri = Polygon([(x + size*0.25, y + 0.55), (x + size*0.25, y + 0.35), 
                           (x + size*0.05, y + 0.55)],
                          facecolor='#34495e', edgecolor='none', zorder=4, alpha=0.7)
        ax.add_patch(fold_tri)
        # Lines on doc
        for i in range(3):
            y_line = y - 0.05 + i * 0.15
            ax.plot([x - 0.2, x + 0.15], [y_line, y_line], 
                   color='#34495e', linewidth=2, zorder=4, alpha=0.6)
    
    elif icon_type == 'brain':
        # Brain with details
        left = Circle((x - size*0.25, y), size*0.4, facecolor=color, 
                     edgecolor='none', zorder=4, alpha=0.95)
        right = Circle((x + size*0.25, y), size*0.4, facecolor=color, 
                      edgecolor='none', zorder=4, alpha=0.95)
        ax.add_patch(left)
        ax.add_patch(right)
        # Brain curves
        for offset_y in [-0.15, 0, 0.15]:
            ax.add_patch(Arc((x - size*0.25, y + offset_y), size*0.3, size*0.4, 
                           angle=0, theta1=30, theta2=150,
                           edgecolor='#34495e', linewidth=2, zorder=4))
            ax.add_patch(Arc((x + size*0.25, y + offset_y), size*0.3, size*0.4, 
                           angle=0, theta1=30, theta2=150,
                           edgecolor='#34495e', linewidth=2, zorder=4))
    
    elif icon_type == 'gear':
        # Gear mechanism
        outer = Circle((x, y), size*0.45, facecolor=color, 
                      edgecolor='none', zorder=4, alpha=0.95)
        inner = Circle((x, y), size*0.22, facecolor='#34495e', 
                      edgecolor='none', zorder=4, alpha=0.8)
        ax.add_patch(outer)
        ax.add_patch(inner)
        # Gear teeth
        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            rad = np.radians(angle)
            tooth_x = x + size*0.4 * np.cos(rad)
            tooth_y = y + size*0.4 * np.sin(rad)
            tooth = Circle((tooth_x, tooth_y), size*0.12, 
                          facecolor=color, edgecolor='none', zorder=4, alpha=0.95)
            ax.add_patch(tooth)
    
    elif icon_type == 'search':
        # Magnifying glass
        lens = Circle((x - 0.05, y + 0.05), size*0.35, facecolor='none', 
                     edgecolor=color, linewidth=3.5, zorder=4)
        ax.add_patch(lens)
        handle_angle = -45
        rad = np.radians(handle_angle)
        handle_start_x = x - 0.05 + size*0.35 * np.cos(rad)
        handle_start_y = y + 0.05 + size*0.35 * np.sin(rad)
        handle_end_x = handle_start_x + 0.25 * np.cos(rad)
        handle_end_y = handle_start_y + 0.25 * np.sin(rad)
        ax.plot([handle_start_x, handle_end_x], [handle_start_y, handle_end_y], 
               color=color, linewidth=3.5, zorder=4, solid_capstyle='round')
    
    elif icon_type == 'target':
        # Bullseye target
        for i, r in enumerate([0.45, 0.32, 0.2]):
            circle_color = color if i % 2 == 0 else '#34495e'
            target_circle = Circle((x, y), size*r, facecolor=circle_color, 
                                  edgecolor='none', zorder=4, alpha=0.95)
            ax.add_patch(target_circle)

def draw_arrow(ax, x1, y1, x2, y2, label='', style='solid', color='#2C3E50', width=2.8):
    """Draw clean arrow with label"""
    # Determine curve for aesthetics
    dx = x2 - x1
    dy = y2 - y1
    curve = 0.15 if abs(dx) > 3 else 0
    
    connectionstyle = f"arc3,rad={curve}" if curve != 0 else "arc3,rad=0"
    
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle='-|>',
        connectionstyle=connectionstyle,
        linewidth=width,
        color=color,
        linestyle='--' if style == 'dashed' else '-',
        mutation_scale=28,
        zorder=1,
        alpha=0.85
    )
    ax.add_patch(arrow)
    
    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # Label with background
        bbox_props = dict(boxstyle='round,pad=0.4', facecolor='white', 
                         edgecolor=color, linewidth=2, alpha=0.98)
        ax.text(mid_x, mid_y, label,
                ha='center', va='center',
                fontsize=10, fontweight='600',
                color=color,
                bbox=bbox_props,
                zorder=5,
                family='sans-serif')

def draw_arrow_90deg(ax, x1, y1, x2, y2, label='', style='solid', color='#2C3E50', width=2.8, 
                     bend_point=None, label_pos='mid'):
    """Draw arrow with 90-degree bend"""
    if bend_point:
        # Draw two segments with a 90-degree turn
        # First segment
        arrow1 = FancyArrowPatch(
            (x1, y1), bend_point,
            arrowstyle='-',
            linewidth=width,
            color=color,
            linestyle='--' if style == 'dashed' else '-',
            mutation_scale=28,
            zorder=1,
            alpha=0.85
        )
        ax.add_patch(arrow1)
        
        # Second segment with arrow
        arrow2 = FancyArrowPatch(
            bend_point, (x2, y2),
            arrowstyle='-|>',
            linewidth=width,
            color=color,
            linestyle='--' if style == 'dashed' else '-',
            mutation_scale=28,
            zorder=1,
            alpha=0.85
        )
        ax.add_patch(arrow2)
        
        # Add label at specified position
        if label:
            if label_pos == 'mid':
                label_x = (x1 + x2) / 2
                label_y = (y1 + y2) / 2
            elif label_pos == 'first':
                label_x = (x1 + bend_point[0]) / 2
                label_y = (y1 + bend_point[1]) / 2
            elif label_pos == 'second':
                label_x = (bend_point[0] + x2) / 2
                label_y = (bend_point[1] + y2) / 2
            else:
                label_x, label_y = label_pos
            
            bbox_props = dict(boxstyle='round,pad=0.4', facecolor='white', 
                             edgecolor=color, linewidth=2, alpha=0.98)
            ax.text(label_x, label_y, label,
                    ha='center', va='center',
                    fontsize=10, fontweight='600',
                    color=color,
                    bbox=bbox_props,
                    zorder=5,
                    family='sans-serif')
    else:
        # Fallback to regular arrow
        draw_arrow(ax, x1, y1, x2, y2, label, style, color, width)

# =================== ARCHITECTURE LAYOUT ===================

# 1. USER INPUT (Top Left)
draw_container(ax, 0.5, 10.2, 3.2, 2.2, 'User Input', COLORS['teal'])
draw_component(ax, 0.9, 10.6, 2.4, 1.4, 'Student\nProfile', COLORS['teal'], 
               icon_type='user', subtitle='IEP Request')

# 2. KNOWLEDGE BASE (Top Center)
draw_container(ax, 4.5, 10.2, 8, 2.2, 'Knowledge Base', COLORS['blue'])
draw_component(ax, 5, 10.6, 2.3, 1.4, 'IEP Records', COLORS['blue'], 
               icon_type='database', subtitle='Student Data')
draw_component(ax, 7.6, 10.6, 2.3, 1.4, 'Iowa Core', COLORS['blue'], 
               icon_type='document', subtitle='Standards')
draw_component(ax, 10.2, 10.6, 2.3, 1.4, 'BLS Data', COLORS['blue'], 
               icon_type='database', subtitle='Career Info')

# 3. INDEXING PIPELINE (Middle Left)
draw_container(ax, 0.5, 6.5, 5.8, 3, 'Indexing Pipeline', COLORS['orange'])
draw_component(ax, 1, 7.5, 1.8, 1.5, 'Text\nParser', COLORS['orange'], 
               icon_type='document', subtitle='Extract')
draw_component(ax, 3.1, 7.5, 1.7, 1.5, 'Sentence\nEncoder', COLORS['orange'], 
               icon_type='gear', subtitle='Embed')
draw_component(ax, 5.1, 7.5, 1.5, 1.5, 'FAISS\nIndex', COLORS['orange'], 
               icon_type='database', subtitle='Store')

# 4. RETRIEVAL PIPELINE (Middle Center)
draw_container(ax, 7, 6.5, 5.5, 3, 'Retrieval Pipeline', COLORS['green'])
draw_component(ax, 7.5, 7.5, 1.6, 1.5, 'Semantic\nSearch', COLORS['green'], 
               icon_type='search', subtitle='Query')
draw_component(ax, 9.4, 7.5, 1.6, 1.5, 'Context\nBuilder', COLORS['green'], 
               icon_type='gear', subtitle='Assemble')
draw_component(ax, 11.3, 7.5, 1.6, 1.5, 'Prompt\nTemplate', COLORS['green'], 
               icon_type='document', subtitle='Format')

# 5. GENERATION (Middle Right)
draw_container(ax, 13.2, 6.5, 3.2, 3, 'Generation', COLORS['purple'])
draw_component(ax, 13.7, 7.5, 2.2, 1.5, 'GPT-4\nTurbo', COLORS['purple'], 
               icon_type='brain', subtitle='AI Model')

# 6. OUTPUT (Top Right)
draw_container(ax, 17.2, 10.2, 4.3, 2.2, 'Generated IEP', COLORS['red'])
draw_component(ax, 17.6, 10.6, 1.3, 1.4, 'SMART\nGoals', COLORS['red'], 
               icon_type='target', subtitle='Objectives')
draw_component(ax, 19.1, 10.6, 1.3, 1.4, 'Progress\nMetrics', COLORS['red'], 
               icon_type='target', subtitle='Track')
draw_component(ax, 20.6, 10.6, 1.3, 1.4, 'Standards\nAlign', COLORS['red'], 
               icon_type='target', subtitle='Map')

# 7. INTERFACE (Bottom)
draw_container(ax, 0.5, 4.5, 15.7, 1.5, 'Gradio User Interface', COLORS['navy'])
draw_component(ax, 1.2, 4.8, 3.5, 0.9, 'Web Application', COLORS['navy'], subtitle='Interactive UI')
draw_component(ax, 5, 4.8, 3.5, 0.9, 'Authentication', COLORS['navy'], subtitle='Secure Access')
draw_component(ax, 8.8, 4.8, 3.5, 0.9, 'Export & Reports', COLORS['navy'], subtitle='PDF/DOCX')
draw_component(ax, 12.6, 4.8, 3.5, 0.9, 'Feedback Loop', COLORS['navy'], subtitle='Refinement')

# 8. ORCHESTRATOR (Bottom)
draw_container(ax, 0.5, 2.8, 15.7, 1.3, 'RAG Orchestrator', COLORS['navy'], alpha=0.1)
draw_component(ax, 1.2, 3, 3.5, 0.7, 'LangChain Framework', COLORS['navy'])
draw_component(ax, 5, 3, 3.5, 0.7, 'Python Backend', COLORS['navy'])
draw_component(ax, 8.8, 3, 3.5, 0.7, 'Query Engine', COLORS['navy'])
draw_component(ax, 12.6, 3, 3.5, 0.7, 'Response Handler', COLORS['navy'])

# =================== ARROWS (90-DEGREE BENDS) ===================

# 1. User -> Knowledge Base (straight horizontal)
draw_arrow(ax, 3.3, 11.3, 4.5, 11.3, 'Query', color=COLORS['teal'])

# 2. BLUE ARROW: Knowledge Base -> Indexing (from bottom of KB, straight down, then left to top of indexing)
# From bottom center of Knowledge Base, down then left
kb_bottom_x = 8.6
kb_bottom_y = 10.2
indexing_top_x = 3.4
indexing_top_y = 9.5
bend_blue = (kb_bottom_x, indexing_top_y)  # Go down to indexing level, then left
draw_arrow_90deg(ax, kb_bottom_x, kb_bottom_y, indexing_top_x, indexing_top_y, 
                 'Documents', color=COLORS['blue'], bend_point=bend_blue, label_pos='first')

# 3. Indexing -> Retrieval (horizontal from FAISS to Semantic Search)
draw_arrow(ax, 6.6, 8.2, 7.5, 8.2, 'Vectors', color=COLORS['orange'])

# 4. BROKEN ARROW: User -> Retrieval (down from user, then right to retrieval at side)
user_start_x = 2.1
user_start_y = 10.2
retrieval_left_x = 7.5
retrieval_left_y = 8.2
bend_dashed = (user_start_x, retrieval_left_y)  # Go down first, then right
draw_arrow_90deg(ax, user_start_x, user_start_y, retrieval_left_x, retrieval_left_y, 
                 'Search Query', style='dashed', color=COLORS['teal'], width=2.5, 
                 bend_point=bend_dashed, label_pos='second')

# 5. Retrieval -> Generation (straight horizontal)
draw_arrow(ax, 12.9, 8.2, 13.7, 8.2, 'Context', color=COLORS['green'])

# 6. VIOLET ARROW: Generation -> Output (from top of generation, up then right to side of output)
gen_top_x = 14.8
gen_top_y = 9.5
output_left_x = 17.6
output_left_y = 11.3
bend_purple = (gen_top_x, output_left_y)  # Go up first, then right
draw_arrow_90deg(ax, gen_top_x, gen_top_y, output_left_x, output_left_y, 
                 'IEP Goals', color=COLORS['purple'], bend_point=bend_purple, label_pos='first')

# 7. RED ARROW: Output -> User (from top of output, go up then left along top level)
output_top_x = 18.9
output_top_y = 12.4
user_right_x = 3.3
user_right_y = 12.4
bend_red = (output_top_x, user_right_y)  # Stay at top level, go left
draw_arrow_90deg(ax, output_top_x, output_top_y, user_right_x, user_right_y, 
                 'Delivery', color=COLORS['red'], width=2.5, bend_point=bend_red, label_pos='mid')

# 8. Interface connections (vertical to UI layer)
draw_arrow(ax, 3.5, 6.5, 3.5, 6.0, '', color=COLORS['navy'], width=2)
draw_arrow(ax, 10.2, 6.5, 10.2, 6.0, '', color=COLORS['navy'], width=2)

# =================== LEGEND ===================
legend_x = 17.8
legend_y = 7.5

# Legend box
legend_box = FancyBboxPatch(
    (legend_x, legend_y - 1.8), 3.5, 1.8,
    boxstyle="round,pad=0.15",
    facecolor='white',
    edgecolor=COLORS['navy'],
    linewidth=2.5,
    alpha=0.95,
    zorder=3
)
ax.add_patch(legend_box)

ax.text(legend_x + 1.75, legend_y - 0.3, 'Data Flow Legend', 
        fontsize=11, fontweight='bold', ha='center',
        color=COLORS['navy'], family='sans-serif', zorder=4)

# Solid arrow
arrow_solid = FancyArrowPatch((legend_x + 0.3, legend_y - 0.7), (legend_x + 1.2, legend_y - 0.7),
                             arrowstyle='-|>', linewidth=2.5, color=COLORS['navy'], 
                             mutation_scale=20, zorder=4)
ax.add_patch(arrow_solid)
ax.text(legend_x + 1.5, legend_y - 0.7, 'Data Flow', fontsize=9, va='center',
        color=COLORS['navy'], family='sans-serif', zorder=4)

# Dashed arrow
arrow_dash = FancyArrowPatch((legend_x + 0.3, legend_y - 1.1), (legend_x + 1.2, legend_y - 1.1),
                            arrowstyle='-|>', linewidth=2.5, color=COLORS['navy'], 
                            linestyle='--', mutation_scale=20, zorder=4)
ax.add_patch(arrow_dash)
ax.text(legend_x + 1.5, legend_y - 1.1, 'Query Path', fontsize=9, va='center',
        color=COLORS['navy'], family='sans-serif', zorder=4)

# Container example
mini_container = FancyBboxPatch((legend_x + 0.3, legend_y - 1.5), 0.9, 0.25,
                               boxstyle="round,pad=0.03",
                               facecolor=COLORS['blue'], edgecolor=COLORS['blue'],
                               linewidth=2, alpha=0.3, zorder=4)
ax.add_patch(mini_container)
ax.text(legend_x + 1.5, legend_y - 1.38, 'Pipeline Stage', fontsize=9, va='center',
        color=COLORS['navy'], family='sans-serif', zorder=4)

# =================== TITLE ===================
title_box = FancyBboxPatch(
    (5, 12.1), 12, 0.7,
    boxstyle="round,pad=0.2",
    facecolor='white',
    edgecolor=COLORS['teal'],
    linewidth=4,
    alpha=0.98,
    zorder=6
)
ax.add_patch(title_box)

ax.text(11, 12.45, 'IEP Goal Generator - RAG System Architecture', 
        fontsize=20, fontweight='bold', ha='center',
        color=COLORS['navy'],
        zorder=7, family='sans-serif')

# Subtitle
ax.text(11, 1.8, 'Retrieval-Augmented Generation for Personalized Education Planning', 
        fontsize=11, fontweight='normal', ha='center', style='italic',
        color='#7f8c8d', zorder=7, family='sans-serif')

# =================== SAVE ===================
plt.tight_layout()
plt.savefig('rag_architecture.png', dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
plt.savefig('rag_architecture.svg', format='svg', bbox_inches='tight', facecolor='#f8f9fa')

print("\n" + "="*65)
print("  ✨ Unique Professional IEP RAG Architecture Generated! ✨")
print("="*65)
print("  Files created:")
print("    📄 rag_architecture.png (300 DPI - Print Quality)")
print("    📄 rag_architecture.svg (Vector - Infinite Scale)")
print("="*65)
print("  Design Features:")
print("    ✓ Modular container-based layout")
print("    ✓ Clean left-to-right pipeline flow")
print("    ✓ No crossing arrows - clear data paths")
print("    ✓ Modern icons with shadows and depth")
print("    ✓ Professional color-coded sections")
print("    ✓ Publication-ready aesthetics")
print("="*65)
