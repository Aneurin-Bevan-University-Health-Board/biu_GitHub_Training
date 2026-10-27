import unittest
from datetime import date

import pandas as pd

from cricket_dashboard import (BASE_DIR, batting_table, bbc_score_rows, bbc_test_matches,
                              bowling_table, innings_table, load_data)


class BBCScoreboardTests(unittest.TestCase):
    def setUp(self):
        self.today = date(2026, 10, 27)
        self.event = {'id': 'test', 'tournamentName': "Women's International Test Match Series",
                      'startDateTime': '2026-10-25T10:00:00Z', 'status': 'InPlay',
                      'matchDateSummary': {'startDate': '2026-10-25', 'endDate': '2026-10-29'},
                      'participants': {'homeTeam': {'name': 'England Women', 'innings': [
                          {'runs': '250', 'wickets': '8', 'overs': '80.2', 'isDeclared': True}]},
                                       'awayTeam': {'name': 'Australia Women', 'innings': None}}}

    def payload(self, *events):
        return {'eventGroups': [{'secondaryGroups': [{'events': list(events)}]}]}

    def test_live_includes_test_started_before_today(self):
        events = bbc_test_matches(self.payload(self.event), self.today, england_only=True, gender='Women')
        self.assertEqual(len(events), 1)
        self.assertEqual(bbc_test_matches(self.payload(self.event), self.today, gender='Men'), [])

    def test_excludes_past_matches_and_other_formats(self):
        old = dict(self.event, matchDateSummary={'startDate': '2026-10-20', 'endDate': '2026-10-24'})
        odi = dict(self.event, tournamentName="Women's One Day International Series")
        self.assertEqual(bbc_test_matches(self.payload(old, odi), self.today), [])

    def test_upcoming_requires_england_and_scheduled_status(self):
        future = dict(self.event, status='PreEvent', startDateTime='2026-11-01T10:00:00Z',
                      matchDateSummary={'startDate': '2026-11-01', 'endDate': '2026-11-05'})
        other = dict(future, id='other', participants={'homeTeam': {'name': 'South Africa'},
                                                     'awayTeam': {'name': 'Australia'}})
        events = bbc_test_matches(self.payload(self.event, future, future, other), self.today,
                                 upcoming=True, england_only=True)
        self.assertEqual([event['id'] for event in events], ['test'])

    def test_scores_preserve_declarations_and_unstarted_innings(self):
        rows = bbc_score_rows(self.event)
        self.assertEqual(rows[0]['Innings'], '250/8 dec (80.2 ov)')
        self.assertEqual(rows[1]['Innings'], 'Yet to bat')

    def test_multiple_innings_and_all_out(self):
        team = self.event['participants']['homeTeam']
        team['innings'].append({'runs': '100', 'wickets': '10', 'overs': '30.0', 'isAllOut': True})
        self.assertEqual(bbc_score_rows(self.event)[0]['Innings'], '250/8 dec (80.2 ov) & 100 (30.0 ov)')


class CricketStatisticsTests(unittest.TestCase):
    def setUp(self):
        self.balls = pd.DataFrame([
            {'match_id': 'test', 'innings': 1, 'batting_team': 'England', 'batter': 'Batter',
             'non_striker': 'Partner', 'bowler': 'Bowler', 'runs_batter': 4, 'runs_total': 4,
             'ball_faced': 1, 'legal_ball': 1, 'bowler_runs': 4},
            {'match_id': 'test', 'innings': 1, 'batting_team': 'England', 'batter': 'Batter',
             'non_striker': 'Partner', 'bowler': 'Bowler', 'runs_batter': 0, 'runs_total': 1,
             'ball_faced': 0, 'legal_ball': 0, 'bowler_runs': 1},
            {'match_id': 'test', 'innings': 1, 'batting_team': 'England', 'batter': 'Batter',
             'non_striker': 'Partner', 'bowler': 'Bowler', 'runs_batter': 0, 'runs_total': 2,
             'ball_faced': 1, 'legal_ball': 1, 'bowler_runs': 0},
        ])
        self.wickets = pd.DataFrame([
            {'match_id': 'test', 'innings': 1, 'player': 'Partner', 'kind': 'run out', 'bowler': 'Bowler', 'credited': False},
            {'match_id': 'test', 'innings': 1, 'player': 'Batter', 'kind': 'caught', 'bowler': 'Bowler', 'credited': True},
        ])

    def test_bowling_excludes_runouts_and_byes(self):
        row = bowling_table(self.balls, self.wickets).iloc[0]
        self.assertEqual(row['Wickets'], 1)
        self.assertEqual(row['Runs'], 5)
        self.assertEqual(row['Overs'], '0.2')
        self.assertEqual(row['Economy'], 15)

    def test_zero_ball_runout_is_a_batting_record(self):
        rows = batting_table(self.balls, self.wickets).set_index('Player')
        self.assertEqual(rows.loc['Partner', 'Runs'], 0)
        self.assertEqual(rows.loc['Partner', 'Outs'], 1)
        self.assertEqual(rows.loc['Partner', 'Matches'], 1)
        self.assertEqual(rows.loc['Batter', 'Balls'], 2)
        self.assertEqual(rows.loc['Batter', 'Strike rate'], 200)

    def test_no_dismissals_gives_missing_average(self):
        rows = batting_table(self.balls, self.wickets.iloc[:0])
        self.assertTrue(rows['Average'].isna().all())
        bowling = bowling_table(self.balls, self.wickets.iloc[:0])
        self.assertEqual(bowling.iloc[0]['Wickets'], 0)
        self.assertTrue(pd.isna(bowling.iloc[0]['Average']))

    def test_innings_runs_and_dismissal_rules(self):
        wickets = pd.concat([self.wickets, pd.DataFrame([
            {'match_id': 'test', 'innings': 1, 'player': 'Other', 'kind': 'retired hurt', 'bowler': 'Bowler', 'credited': False},
            {'match_id': 'test', 'innings': 1, 'player': 'Another', 'kind': 'obstructing the field', 'bowler': 'Bowler', 'credited': False},
        ])], ignore_index=True)
        row = innings_table(self.balls, wickets).iloc[0]
        self.assertEqual(row['Runs'], 7)
        self.assertEqual(row['Wickets'], 3)
        self.assertEqual(row['Overs'], '0.2')

    def test_current_exports_and_map_coverage(self):
        files = sorted((BASE_DIR / 'cricsheet_exports').glob('*.csv'))
        balls, matches, wickets = load_data(tuple((str(path), path.stat().st_mtime_ns) for path in files))
        self.assertFalse(matches.empty)
        self.assertFalse(matches['match_id'].duplicated().any())
        self.assertGreater(len(balls), 0)
        self.assertEqual(set(matches['gender']), {'male', 'female'})
        catalogue = pd.read_csv(BASE_DIR / 'cricket_venues.csv')
        self.assertFalse(catalogue['venue'].duplicated().any())
        self.assertEqual(set(matches['venue']) - set(catalogue['venue']), set())
        self.assertTrue(catalogue['latitude'].between(-90, 90).all())
        self.assertTrue(catalogue['longitude'].between(-180, 180).all())
        totals = innings_table(balls, wickets)
        self.assertEqual(totals['Runs'].sum(), balls['runs_total'].sum())


if __name__ == '__main__':
    unittest.main()