import plotly.express as px

def generate_plot(x, y, x_label, y_label, title):
    fig = px.bar(x=x, y=y)
    fig.update_layout(xaxis_title=x_label, yaxis_title=y_label, title=title)

    # プロットをHTMLに変換
    graph_html = fig.to_html(full_html=False)

    return graph_html



