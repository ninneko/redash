from tests import BaseTestCase
from redash.models import Query
from redash.models import Visualization


class TestApiKeyGetByObject(BaseTestCase):
    def test_returns_none_if_not_exists(self):
        data_source = self.factory.create_data_source(group=self.factory.create_group())
        query = self.factory.create_query(data_source=data_source)
        visualization = self.factory.create_visualization(query=query, descriptsion="chart vis", type="CHART", options="""{"yAxis": [{"type": "linear"}, {"type": "linear", "opposite": true}], "series": {"stacking": null}, "globalSeriesType": "line", "sortX": true, "seriesOptions": {"count": {"zIndex": 0, "index": 0, "type": "line", "yAxis": 0}}, "xAxis": {"labels": {"enabled": true}, "type": "datetime"}, "columnMapping": {"count": "y", "created_at": "x"}, "bottomMargin": 50, "legend": {"enabled": true}}""")
        visualization2 = self.factory.create_visualization(query=query, description="box vis", type="BOXPLOT", options="{}")

        forked_user = self.factory.create_user()
        org = self.factory.org
        forked_query = Query.fork(query.id, forked_user, org)
        forked_visualization = forked_query.visualizations


        print forked_query.to_dict(with_visualizations=True)
        print forked_user.to_dict()

