import plotly.express as px

# hier kann man die color map zentral ändern
def generate_color_map(entities, palette=px.colors.qualitative.Set2):
    return {entity: palette[i % len(palette)] for i, entity in enumerate(entities)}