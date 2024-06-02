import plotly.graph_objects as go
import networkx as nx
import torch
import pandas as pd
import sys
# sys.path.append("../")
from models import *
from trainer import *
from plotly.offline import iplot

def visualize_graph_from_edges(nodes_count, edges_index):
    edge_indices = edges_index.coalesce().indices()
    # 创建 NetworkX 图
    G = nx.Graph()
    # 添加边到图中
    for i in range(edge_indices.size(1)):
        x = edge_indices[0,i]
        y = edge_indices[1,i]
        G.add_edge(x, y)

    # 估计节点位置（随机布局）
    nodes_positions = nx.random_layout(G)

    # 绘制边
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = nodes_positions[edge[0]]
        x1, y1 = nodes_positions[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # 绘制节点
    node_x = []
    node_y = []
    for node, pos in nodes_positions.items():
        x, y = pos
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Graph Visualization',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))
    iplot(fig)
    # fig.show()


if __name__ == "__main__":
    claim_data = torch.Tensor(pd.read_pickle('../../data/claim_tensor.pkl'))
    county_data = torch.Tensor(pd.read_pickle('../../data/county_tensor.pkl'))
    hospitalizations_data = torch.Tensor(pd.read_pickle('../../data/hospitalizations.pkl'))
    distance_matrix = torch.Tensor(pd.read_pickle('../../data/distance_mat.pkl'))
    data_time = pd.read_pickle('../../data/date_range.pkl') #这个是list
    claim_data.shape, county_data.shape, hospitalizations_data.shape, distance_matrix.shape,
    dynamic_data = torch.cat((claim_data,torch.unsqueeze(hospitalizations_data, -1)), -1)
    static_data = county_data
    label = torch.unsqueeze(hospitalizations_data, -1)
    dynamic_data = dynamic_data[:50]
    static_data = static_data[:50]
    label = label[:50]
    threshold = 5000
    print(threshold)
    nodes_count = 50
    edge_index = construct_adjacency_matrix(static_data, threshold).indices()
    # 假设 edges_indices 存储了边的信息（格式为列表的元组，例如 [(0, 1), (1, 2), ...]）
    # 假设节点总数为 4
    # 调用可视化函数
    visualize_graph_from_edges(nodes_count, edges_index)
