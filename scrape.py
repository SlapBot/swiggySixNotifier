from pycricbuzz import Cricbuzz
from logger import Logger


class Scraper:
    def __init__(self):
        self.cricbuzz = Cricbuzz()
        self.current_over = "-1"
        self.logger_instance = Logger("app.log")

    def _get_matches(self):
        return self.cricbuzz.matches()

    @staticmethod
    def _get_criteria():
        return {
            'type': "T20",
            'mchstate': "inprogress",
            'srs': "Indian Premier League 2019"
        }

    @staticmethod
    def _check_if_valid_match(match, criteria):
        bools = [match[key] == value for key, value in criteria.items()]
        return all(bools)

    def _get_current_match_id(self, matches, criteria):
        for match in matches:
            current_ipl_match = self._check_if_valid_match(match, criteria)
            if current_ipl_match is True:
                return match['id']
        return None

    def _get_commentary(self, match_id):
        return self.cricbuzz.commentary(match_id)['commentary']

    @staticmethod
    def _new_six_scored(commentary, given_last_ball=None):
        last_ball_commentary = [comm for comm in commentary if 'over' in comm and comm['over'] is not None]
        last_30_sixes = [
            comm for comm in commentary
            if "<b>SIX</b>" in comm['comm']
        ]
        if len(last_ball_commentary) == 0:
            last_ball = '0.0'
        else:
            last_ball = last_ball_commentary[0]['over']
        if len(last_30_sixes) > 0 and float(last_30_sixes[0]['over']) > float(given_last_ball):
            return {
                "status": True,
                "last_ball": last_ball
            }
        return {
            "status": False,
            "last_ball": last_ball
        }

    def scrape(self):
        self.logger_instance.info("Querying Matches...")
        matches = self._get_matches()
        match_id = self._get_current_match_id(matches, self._get_criteria())
        if match_id is not None:
            self.logger_instance.info("Match is found with ID: %s" % match_id)
            data = self._new_six_scored(self._get_commentary(match_id), self.current_over)
            if data['last_ball'] == "19.6":
                self.current_over = "-1"
            else:
                self.current_over = data['last_ball']
            if data['status'] is True:
                self.logger_instance.info("A new six was scored at ball: %s" % data["last_ball"])
            return {
                "status": True,
                "data": data
            }
        self.logger_instance.warning("No match with given criteria found.")
        return {
            "status": False,
            "data": {}
        }


if __name__ == "__main__":
    s = Scraper()
    print(s.scrape())
