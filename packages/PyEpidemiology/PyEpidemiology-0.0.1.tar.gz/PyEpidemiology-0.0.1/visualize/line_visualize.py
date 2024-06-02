import plotly.graph_objects as go
import numpy as np
from plotly.offline import iplot

def plot_line_chart(data):
    fig = go.Figure()
    
    if len(data.shape) == 1:
        # 单组数据，绘制单条折线
        fig.add_trace(go.Scatter(x=np.arange(len(data)), y=data, mode='lines', name='Data'))
    elif len(data.shape) == 2:
        # 多组数据，创建按钮选择展示哪一组数据
        for i in range(data.shape[0]):
            visible = [False] * data.shape[0]
            visible[i] = True
            fig.add_trace(go.Scatter(x=np.arange(len(data[i])), y=data[i], mode='lines', name=f'Data {i+1}', visible='legendonly'))
        
        # 创建按钮
        buttons = []
        for i in range(data.shape[0]):
            visible = [False] * data.shape[0]
            visible[i] = True
            buttons.append(
                dict(label=f'Data {i+1}',
                     method='restyle',
                     args=['visible', [visible[j] for j in range(data.shape[0])]])
            )

        # 设置按钮布局
        updatemenus = [{'buttons': buttons,
                        'direction': 'down',
                        'showactive': True,
                        'x': 0.1,
                        'xanchor': 'left',
                        'y': 1.15,
                        'yanchor': 'top'}]

        # 更新图表布局
        fig.update_layout(title='Line Chart with Multiple Data',
                          xaxis_title='X-axis',
                          yaxis_title='Y-axis',
                          updatemenus=updatemenus)
    iplot(fig)
    # fig.show()


if __name__ == "__main__":
    # 测试数据
    # 示例1：一组数据
    data_single = np.random.rand(20)

    # 示例2：多组数据
    data_multiple = np.random.rand(5, 20)

    # 绘制折线图
    plot_line_chart(data_single)  # 绘制单组数据的折线图
    plot_line_chart(data_multiple)  # 绘制多组数据的折线图
