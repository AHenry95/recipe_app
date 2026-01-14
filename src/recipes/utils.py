from io import BytesIO
import base64
import matplotlib.pyplot as plt

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph

def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(8,5))

    if chart_type == '#1':
        return None

    if chart_type == '#2':
        plt.bar(data['name'], data['cooking_time'])
        plt.xlabel('Recipe')
        plt.ylabel('Cooking Time (minutes)')
        plt.title('Cooking Time by Recipe')
        plt.xticks(rotation=45, ha='right')

    elif chart_type == '#3':
        difficulty_counts = data['difficulty'].value_counts()
        plt.pie(difficulty_counts, labels=difficulty_counts.index, autopct='%1.1f%%')
        plt.title('Recipes by Difficulty')
    
    elif chart_type == '#4':
        data_sorted = data.sort_values('ingredient_count')
        plt.plot(data_sorted['ingredient_count'], data_sorted['cooking_time'], marker='o')
        plt.xlabel('Number of Ingredients')
        plt.ylabel('Cooking Time (minutes)')
        plt.title('Cooking Time vs Number of Ingredients')

    else:
        print('Unkown chart type')
        return None
    
    plt.tight_layout()

    chart = get_graph()
    return chart