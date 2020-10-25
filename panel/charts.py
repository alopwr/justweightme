from datetime import date, timedelta

import plotly.graph_objs as go
from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from django.utils.timezone import now
from plotly.offline import plot
from plotly.subplots import make_subplots

from .models import Profile

logger = get_task_logger(__name__)


def generate_chart(profile, days):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    dates, weight, bf = [], [], []
    point_in_time = date.today() - timedelta(days=days)
    for measurement in profile.measurements.filter(created_at__gte=point_in_time):
        # dates.append(measurement.created_at + timedelta(hours=2))
        dates.append(timezone.localtime(measurement.created_at))
        weight.append(measurement.weight)
        bf.append(measurement.bf_percent)
    fig.add_trace(go.Scatter(x=dates, y=weight,
                             mode='lines+markers', name='masa ciała',
                             opacity=0.8, marker_color='Navy'), secondary_y=False)

    fig.add_trace(go.Scatter(x=dates, y=bf,
                             mode='lines+markers', name='tkanka tłuszczowa',
                             opacity=0.8, marker_color='Plum'), secondary_y=True)
    fig.update_yaxes(secondary_y=False, ticksuffix='kg', color='MediumSlateBlue')
    fig.update_yaxes(secondary_y=True, ticksuffix='%', color='Navy')
    fig.update_layout(font={'family': 'Catamaran'}, plot_bgcolor='#e9ecef', paper_bgcolor='#e9ecef', height=400,
                      annotations=[dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                        xanchor='left', yanchor='bottom',
                                        text='Wykres pomiarów z {} dni'.format(days),
                                        font=dict(family='Catamaran',
                                                  size=40,
                                                  color='rgb(37,37,37)'),
                                        showarrow=False)], legend_orientation="h", shapes=[{'type': 'line',
                                                                                            'xref': 'x',
                                                                                            'yref': 'y',
                                                                                            'x0': now(),
                                                                                            'y0': profile.goal,
                                                                                            'x1': now() + timedelta(
                                                                                                days=21),
                                                                                            'y1': profile.goal,
                                                                                            'name': 'goal',
                                                                                            'line': {
                                                                                                'color': 'LightSeaGreen'}}])
    return plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")


@shared_task
def generate_and_save_chart(profile_id, days=14):
    profile = Profile.objects.get(id=profile_id)
    logger.info("generating chart requested")
    profile.chart_js_code = generate_chart(profile, days)
    profile.save()
