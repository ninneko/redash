from tests import BaseTestCase
from redash.models import Query


class TestApiKeyGetByObject(BaseTestCase):

    def assert_visualizations(self, origin_q, origin_v, forked_q, forked_v):
        self.assertEqual(origin_v.options, forked_v.options)
        self.assertEqual(origin_v.type, forked_v.type)
        self.assertNotEqual(origin_v.id, forked_v.id)
        self.assertNotEqual(origin_v.query, forked_v.query)
        self.assertEqual(forked_q.id, forked_v.query.id)


    def test_returns_none_if_not_exists(self):
        # prepare original query and visualizations
        data_source = self.factory.create_data_source(group=self.factory.create_group())
        query = self.factory.create_query(data_source=data_source)
        visualization_chart = self.factory.create_visualization(query=query, description="chart vis", type="CHART", options="""{"yAxis": [{"type": "linear"}, {"type": "linear", "opposite": true}], "series": {"stacking": null}, "globalSeriesType": "line", "sortX": true, "seriesOptions": {"count": {"zIndex": 0, "index": 0, "type": "line", "yAxis": 0}}, "xAxis": {"labels": {"enabled": true}, "type": "datetime"}, "columnMapping": {"count": "y", "created_at": "x"}, "bottomMargin": 50, "legend": {"enabled": true}}""")
        visualization_box = self.factory.create_visualization(query=query, description="box vis", type="BOXPLOT", options="{}")


        forked_query = Query.fork(query.id,  self.factory.create_user(), self.factory.org)


        forked_visualization_chart = None
        forked_visualization_box = None
        forked_table = None
        count_table = 0
        for v in forked_query.visualizations:
            if v.description == "chart vis":
                forked_visualization_chart = v
            if v.description == "box vis":
                forked_visualization_box = v
            if v.type == "TABLE":
                count_table += 1
                forked_table = v
        self.assert_visualizations(query, visualization_chart, forked_query, forked_visualization_chart)
        self.assert_visualizations(query, visualization_box, forked_query, forked_visualization_box)

        # num of TABLE must be 1. default table only
        self.assertEqual(count_table, 1)
        self.assertEqual(forked_table.name, "Table")
        self.assertEqual(forked_table.description, "")
        self.assertEqual(forked_table.options, "{}")



