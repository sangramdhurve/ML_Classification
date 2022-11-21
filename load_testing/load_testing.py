# locust==2.11.1
# run file with command :    locust -f load_testing.py --host http://0.0.0.0:5000
# host url can be different

from locust import HttpUser, task, between


class TestAPILoad(HttpUser):
    wait_time = between(1, 5)

    @task
    def test_predict(self):
        self.client.post("/lead_scoring/score_data", json=self.data

                         )

    def on_start(self):

        self.data = {
                        "total_visits": 15,
                        "total_time_spent_on_website": 753,
                        "page_views_per_visit": 15,
                        "lead_source": None,
                        "last_activity": None,
                        "specialization": None,
                        "search": None,
                        "newspaper": "Yes",
                        "last_notable_activity": None
}
