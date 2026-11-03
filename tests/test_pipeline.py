import tempfile, unittest
from pathlib import Path
from src.etl_pipeline import run_pipeline
from src.database import connect
def payload():
    return {"name":"Test City","sys":{"country":"IN"},"coord":{"lat":19,"lon":72},"dt":1700000000,
            "main":{"temp":28.5,"feels_like":29,"humidity":65,"pressure":1012},
            "wind":{"speed":3.4},"weather":[{"main":"Clear","description":"clear sky"}]}
class PipelineTests(unittest.TestCase):
    def test_loads_and_deduplicates(self):
        with tempfile.TemporaryDirectory() as d:
            db=str(Path(d)/"test.db")
            fetch=lambda city: payload()
            a=run_pipeline(["Test City"],fetch,db); b=run_pipeline(["Test City"],fetch,db)
            self.assertEqual(a["inserted"],1); self.assertEqual(b["duplicates"],1)
            with connect(db) as c:
                self.assertEqual(c.execute("SELECT COUNT(*) FROM weather_observations").fetchone()[0],1)
    def test_failure_logged_in_database(self):
        with tempfile.TemporaryDirectory() as d:
            db=str(Path(d)/"test.db")
            result=run_pipeline(["No City"],lambda city: (_ for _ in ()).throw(RuntimeError("offline")),db)
            self.assertEqual(result["failed"],1)
            with connect(db) as c:
                self.assertEqual(c.execute("SELECT status FROM pipeline_runs").fetchone()[0],"failed")
if __name__=="__main__": unittest.main()
