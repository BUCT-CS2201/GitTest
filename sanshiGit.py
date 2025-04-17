
from graphviz import Digraph

# 初始化有向图
dot = Digraph(comment='示例流程图', format='png')

# 添加节点（可自定义颜色、形状）
dot.node('A', '启动', color='blue', shape='box')
dot.node('B', '处理数据', color='orange')
dot.node('C', '结束', shape='ellipse')

# 添加边（可添加标签）
dot.edge('A', 'B', label='步骤1')
dot.edge('B', 'C', label='步骤2')

# 保存并渲染图像
dot.render(filename='demo.gv', view=True)

print("xxxx")