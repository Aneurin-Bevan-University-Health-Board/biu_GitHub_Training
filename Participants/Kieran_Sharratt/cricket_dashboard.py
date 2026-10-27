import json
from datetime import datetime, timedelta
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen
from zoneinfo import ZoneInfo

import pandas as pd
import plotly.express as px
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'cricsheet_exports'
BOWLER_DISMISSALS = {'bowled', 'caught', 'caught and bowled', 'lbw', 'stumped', 'hit wicket'}
PALETTE = ['#c8102e', '#007db5', '#172b4d', '#72c7e7']
BBC_URL = 'https://www.bbc.com'
UK_TIME = ZoneInfo('Europe/London')


@st.cache_data(ttl=60, show_spinner=False)
def load_bbc_scores(start_date, end_date, today):
    query = urlencode({'urn': 'urn:bbc:sportsdata:cricket:tournament-collection:collated',
                       'selectedStartDate': start_date, 'selectedEndDate': end_date,
                       'todayDate': today})
    with urlopen(f'{BBC_URL}/wc-data/container/sport-data-scores-fixtures?{query}', timeout=15) as response:
        payload = json.load(response)
    if not isinstance(payload, dict) or not isinstance(payload.get('eventGroups'), list):
        raise ValueError('BBC scoreboard format is unavailable.')
    return payload, datetime.now(UK_TIME)


def bbc_test_matches(payload, today, upcoming=False, england_only=False, gender='Both'):
    matches = {}
    for group in payload['eventGroups']:
        for section in group.get('secondaryGroups', []):
            for event in section.get('events', []):
                tournament = event.get('tournamentName', '')
                if 'test' not in tournament.lower():
                    continue
                teams = list(event.get('participants', {}).values())
                if england_only and not any(team.get('name', '').lower() in
                                           {'england', 'england women', 'england men'} for team in teams):
                    continue
                women = 'women' in tournament.lower()
                if (gender == 'Women' and not women) or (gender == 'Men' and women):
                    continue
                dates = event.get('matchDateSummary', {})
                start = dates.get('startDate', event.get('startDateTime', '')[:10])
                end = dates.get('endDate', start)
                if upcoming:
                    if event.get('status') != 'PreEvent' or start < today.isoformat():
                        continue
                elif not start <= today.isoformat() <= end:
                    continue
                matches[event['id']] = event
    return sorted(matches.values(), key=lambda event: event.get('startDateTime', ''))


def bbc_score_rows(event):
    rows = []
    for team in event.get('participants', {}).values():
        innings = []
        for score in team.get('innings') or []:
            total = str(score.get('runs', '0'))
            if not score.get('isAllOut'):
                total += '/' + str(score.get('wickets', '0'))
            if score.get('isDeclared'):
                total += ' dec'
            innings.append(f"{total} ({score.get('overs', '?')} ov)")
        rows.append({'Team': team.get('name', 'Unknown'), 'Innings': ' & '.join(innings) or 'Yet to bat'})
    return rows


def render_bbc_matches(upcoming=False):
    today = datetime.now(UK_TIME).date()
    prefix = 'upcoming' if upcoming else 'live'
    st.subheader('Upcoming England Tests' if upcoming else "Today's Test Scores")
    st.caption(f"{today:%d %b %Y} | UK time | BBC Sport")
    gender = st.segmented_control('England team' if upcoming else 'Teams', ['Men', 'Women', 'Both'],
                                  default='Both', key=f'{prefix}_gender')
    england_only = True if upcoming else st.toggle('England matches only', value=False, key='live_england')
    if st.button('Refresh fixtures' if upcoming else 'Refresh scores', icon=':material/refresh:', key=f'{prefix}_refresh'):
        load_bbc_scores.clear()
    end = today + timedelta(days=365) if upcoming else today
    try:
        with st.spinner('Checking BBC Sport...'):
            payload, updated = load_bbc_scores(today.isoformat(), end.isoformat(), today.isoformat())
        events = bbc_test_matches(payload, today, upcoming, england_only, gender or 'Both')
    except (URLError, OSError, ValueError, KeyError, TypeError):
        st.warning('BBC Sport scores are temporarily unavailable. Please try again shortly.')
        st.link_button('BBC scores and fixtures', f'{BBC_URL}/sport/cricket/scores-fixtures', icon=':material/open_in_new:')
        return
    st.caption(f"Updated {updated:%H:%M:%S %Z}" + (f" | Fixtures through {end:%d %b %Y}" if upcoming else ''))
    if not events:
        st.info('No upcoming England Tests listed by BBC Sport in this period.' if upcoming else
                'No Test matches listed by BBC Sport for today with these filters.')
    for event in events:
        with st.container(border=True):
            teams = event.get('participants', {}).values()
            st.markdown('**' + ' v '.join(team.get('name', 'Unknown') for team in teams) + '**')
            st.caption(event.get('tournamentDescriptionLabel', event.get('tournamentName', 'Test match')))
            dates = event.get('matchDateSummary', {})
            start = pd.Timestamp(event['startDateTime']).tz_convert(UK_TIME)
            st.write(f"{start:%d %b %Y, %H:%M %Z} | {event.get('groundName', 'Venue to be confirmed')}")
            if upcoming:
                st.caption(f"Scheduled end: {dates.get('endDate', 'To be confirmed')}")
            else:
                status = {'InPlay': 'In progress', 'PreEvent': 'Scheduled', 'PostEvent': 'Finished'}.get(
                    event.get('status'), event.get('status', 'Status unavailable'))
                st.write(' | '.join(filter(None, [status, dates.get('matchDay'),
                                                event.get('matchSummary', {}).get('resultString')])))
                st.dataframe(bbc_score_rows(event), hide_index=True, width='stretch')
            link = event.get('conciseViewScorecardLinkUrl', '')
            if link.startswith('/sport/cricket/'):
                st.link_button('BBC scorecard', BBC_URL + link, icon=':material/open_in_new:')
    st.caption('Source: BBC Sport. Scores and fixture availability may be delayed or change.')


@st.fragment
def upcoming_tests_tab():
    render_bbc_matches(upcoming=True)


@st.fragment(run_every=60)
def live_scores_tab():
    render_bbc_matches()


@st.cache_data(show_spinner=False)
def load_data(signature):
    frames = [pd.read_csv(path, dtype={'match_id': str}, keep_default_na=False)
              for path, modified in signature]
    deliveries = pd.concat(frames, ignore_index=True)
    deliveries['start_date'] = pd.to_datetime(deliveries['start_date'])
    deliveries['opponent'] = deliveries['team_1'].where(
        deliveries['team_1'] != 'England', deliveries['team_2'])
    deliveries['legal_ball'] = ((deliveries['wides'] == 0) & (deliveries['noballs'] == 0)).astype(int)
    deliveries['ball_faced'] = (deliveries['wides'] == 0).astype(int)
    deliveries['bowler_runs'] = deliveries['runs_total'] - deliveries['byes'] - deliveries['legbyes'] - deliveries['penalty']
    dismissals = []
    for row in deliveries.loc[deliveries['wicket_count'] > 0].itertuples():
        for wicket in json.loads(row.wickets_json):
            dismissals.append({'match_id': row.match_id, 'innings': row.innings,
                               'player': wicket['player_out'], 'kind': wicket['kind'],
                               'bowler': row.bowler, 'team': row.batting_team,
                               'credited': wicket['kind'] in BOWLER_DISMISSALS})
    wickets = pd.DataFrame(dismissals, columns=['match_id', 'innings', 'player', 'kind', 'bowler', 'team', 'credited'])
    matches = deliveries.drop_duplicates('match_id')[
        ['match_id', 'gender', 'start_date', 'end_date', 'venue', 'opponent', 'winner', 'result']].copy()
    matches['outcome'] = matches.apply(
        lambda row: 'Won' if row['winner'] == 'England' else 'Lost' if row['winner'] else
        row['result'].capitalize() if row['result'] else 'Unknown', axis=1)
    return deliveries, matches, wickets


def innings_table(deliveries, wickets):
    totals = deliveries.groupby(['match_id', 'innings', 'batting_team'], as_index=False).agg(
        Runs=('runs_total', 'sum'), Legal_balls=('legal_ball', 'sum'))
    dismissed = wickets.loc[~wickets['kind'].isin(['retired hurt', 'retired not out'])]
    counts = dismissed.groupby(['match_id', 'innings']).size().rename('Wickets')
    totals = totals.join(counts, on=['match_id', 'innings']).fillna({'Wickets': 0})
    totals['Wickets'] = totals['Wickets'].astype(int)
    totals['Overs'] = (totals['Legal_balls'] // 6).astype(str) + '.' + (totals['Legal_balls'] % 6).astype(str)
    return totals


def batting_table(deliveries, wickets):
    batting = deliveries.groupby('batter').agg(
        Runs=('runs_batter', 'sum'), Balls=('ball_faced', 'sum'), Matches=('match_id', 'nunique'))
    participants = pd.concat([
        deliveries[['match_id', 'batter']].rename(columns={'batter': 'player'}),
        deliveries[['match_id', 'non_striker']].rename(columns={'non_striker': 'player'}),
    ]).groupby('player')['match_id'].nunique()
    batting = batting.reindex(participants.index, fill_value=0)
    batting['Matches'] = participants
    scores = deliveries.groupby(['match_id', 'innings', 'batter'])['runs_batter'].sum()
    batting['Highest'] = scores.groupby('batter').max().reindex(batting.index, fill_value=0)
    batting['100s'] = scores.ge(100).groupby('batter').sum().reindex(batting.index, fill_value=0)
    batting['50s'] = (scores.ge(50) & scores.lt(100)).groupby('batter').sum().reindex(batting.index, fill_value=0)
    dismissed = wickets.loc[~wickets['kind'].isin(['retired hurt', 'retired not out'])].groupby('player').size()
    batting['Outs'] = dismissed.reindex(batting.index, fill_value=0)
    batting['Average'] = (batting['Runs'] / batting['Outs'].replace(0, float('nan'))).round(2)
    batting['Strike rate'] = (100 * batting['Runs'] / batting['Balls'].replace(0, float('nan'))).round(2)
    return batting.sort_values('Runs', ascending=False).rename_axis('Player').reset_index()


def bowling_table(deliveries, wickets):
    bowling = deliveries.groupby('bowler').agg(
        Runs=('bowler_runs', 'sum'), Balls=('legal_ball', 'sum'), Matches=('match_id', 'nunique'))
    counts = wickets.loc[wickets['credited'].eq(True)].groupby('bowler').size()
    bowling['Wickets'] = counts.reindex(bowling.index, fill_value=0)
    bowling['Average'] = (bowling['Runs'] / bowling['Wickets'].replace(0, float('nan'))).round(2)
    bowling['Economy'] = (6 * bowling['Runs'] / bowling['Balls'].replace(0, float('nan'))).round(2)
    bowling['Strike rate'] = (bowling['Balls'] / bowling['Wickets'].replace(0, float('nan'))).round(2)
    bowling['Overs'] = (bowling['Balls'] // 6).astype(str) + '.' + (bowling['Balls'] % 6).astype(str)
    return bowling.sort_values(['Wickets', 'Runs'], ascending=[False, True]).rename_axis('Player').reset_index()


def chart_layout(figure, height=350):
    figure.update_layout(height=height, margin=dict(l=0, r=10, t=15, b=0),
                         font=dict(family='Trebuchet MS, sans-serif', size=13, color='#172b4d'),
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         colorway=PALETTE, legend_title_text='')
    return figure


def main():
    st.set_page_config(page_title='England Test Cricket', page_icon=':cricket_bat_and_ball:', layout='wide')
    st.markdown('''<style>
    .stApp {
        --england-odi: #72c7e7;
        --england-blue: #007db5;
        --england-t20: #c8102e;
        --england-navy: #172b4d;
        --primary-color: var(--england-t20);
        --font: 'Trebuchet MS', sans-serif;
        --st-font: 'Trebuchet MS', sans-serif;
        background: linear-gradient(155deg, #ffffff 40%, #e8f6fc);
        color:var(--england-navy);
        font-family:'Trebuchet MS',sans-serif;
        color-scheme:light;
    }
    .stApp h1,.stApp h2,.stApp h3,.stApp p,.stApp label,.stApp button,
    .stApp input,.stApp textarea,.stApp select,.stApp table,
    [data-testid="stMetricValue"],[data-testid="stMetricLabel"] {
        font-family:'Trebuchet MS',sans-serif!important; letter-spacing:0!important;
    }
    .stApp h1 {font-size:2.15rem!important; color:var(--england-navy);}
    .stApp h2,.stApp h3 {color:var(--england-navy);}
    [data-testid="stSidebar"] {background:#dff2fb; border-right:4px solid var(--england-odi);}
    [data-testid="stMetric"] {border-top:3px solid var(--england-t20); padding-top:12px;}
    [data-testid="stMetric"]:nth-child(even) {border-top-color:var(--england-blue);}
    .stApp [role="tab"] {color:var(--england-navy);}
    .stApp [role="tab"][aria-selected="true"] {color:var(--england-t20);}
    .stApp [data-baseweb="tab-highlight"] {background-color:var(--england-t20);}
    .stApp a {color:#006795;}
    .stApp button:hover {border-color:var(--england-t20); color:var(--england-t20);}
    .stApp button:focus-visible {outline:2px solid var(--england-blue); outline-offset:2px;}
    .block-container {padding-top:2rem; padding-bottom:2rem; max-width:1600px;}
    button {border-radius:4px!important;}
    </style>''', unsafe_allow_html=True)
    st.title('England Test Cricket')
    st.caption('MEN & WOMEN  /  MATCHES, PLAYERS & GROUNDS')
    match_tab, player_tab, map_tab, upcoming_tab, live_tab = st.tabs(
        ['Match Centre', 'Player Statistics', 'Ground Map', 'Upcoming Tests', 'Live Scores'])
    with upcoming_tab:
        upcoming_tests_tab()
    with live_tab:
        live_scores_tab()
    files = sorted(DATA_DIR.glob('england_*_tests_deliveries.csv'))
    if not files:
        st.error(f'No delivery CSVs found in {DATA_DIR}. Run england_test_matches.ipynb and save its exports here.')
        st.stop()
    with st.spinner('Loading scorecards...'):
        deliveries, matches, wickets = load_data(tuple((str(path), path.stat().st_mtime_ns) for path in files))
    catalogue_path = BASE_DIR / 'cricket_venues.csv'
    catalogue = pd.read_csv(catalogue_path) if catalogue_path.exists() else None
    with st.sidebar:
        st.header('Match Selection')
        gender_label = st.radio('England team', ['Men', 'Women', 'Both'], horizontal=True)
        pool = matches if gender_label == 'Both' else matches.loc[matches['gender'].eq('male' if gender_label == 'Men' else 'female')]
        date_range = st.date_input('Match start dates', value=(pool['start_date'].min().date(), pool['start_date'].max().date()),
                                   min_value=pool['start_date'].min().date(), max_value=pool['start_date'].max().date())
        opponents = st.multiselect('Opposition', sorted(pool['opponent'].unique()))
        grounds = st.multiselect('Ground', sorted(pool['venue'].unique()))
        outcomes = st.multiselect('England result', sorted(pool['outcome'].unique()))
        st.divider()
        st.caption('Source: Cricsheet. Available coverage only; statistics are derived from recorded deliveries.')
        st.link_button('Cricsheet data', 'https://cricsheet.org/downloads/', icon=':material/open_in_new:')
    if len(date_range) != 2:
        st.info('Choose an end date to complete the match selection.')
        st.stop()
    selected = pool.loc[pool['start_date'].between(pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]))]
    for column, values in [('opponent', opponents), ('venue', grounds), ('outcome', outcomes)]:
        if values:
            selected = selected.loc[selected[column].isin(values)]
    if selected.empty:
        st.info('No matches in this selection. Adjust the dates or filters.')
        st.stop()
    match_ids = selected['match_id']
    balls = deliveries.loc[deliveries['match_id'].isin(match_ids)]
    dismissals = wickets.loc[wickets['match_id'].isin(match_ids)]
    metrics = st.columns(4)
    ground_count = selected['venue'].nunique() if catalogue is None else selected['venue'].map(
        catalogue.set_index('venue')['ground']).fillna(selected['venue']).nunique()
    for column, label, value in zip(metrics, ['Tests', 'England wins', 'Grounds', 'Recorded deliveries'],
                                    [len(selected), selected['outcome'].eq('Won').sum(), ground_count, len(balls)]):
        column.metric(label, f'{value:,}')
    with match_tab:
        st.subheader('Match Centre')
        ordered = selected.sort_values('start_date', ascending=False)
        labels = {row.match_id: f"{row.start_date:%d %b %Y} | England v {row.opponent} | {row.venue} | {'Women' if row.gender == 'female' else 'Men'}"
                  for row in ordered.itertuples()}
        match_id = st.selectbox('Match', ordered['match_id'].tolist(), format_func=labels.get)
        match = selected.set_index('match_id').loc[match_id]
        st.markdown(f"**{match['venue']}** · {match['start_date']:%d %b %Y} · England {match['outcome'].lower()}")
        match_balls = balls.loc[balls['match_id'].eq(match_id)]
        match_wickets = dismissals.loc[dismissals['match_id'].eq(match_id)]
        scorecard = innings_table(match_balls, match_wickets)
        st.dataframe(scorecard.rename(columns={'innings': 'Innings', 'batting_team': 'Team'}).drop(columns=['match_id', 'Legal_balls']),
                     hide_index=True, width='stretch')
        st.caption('Delivery totals only: penalty adjustments outside deliveries, declarations and follow-on status are not present in the CSV.')
        progression = match_balls.copy()
        progression['Recorded delivery'] = progression.groupby('innings').cumcount() + 1
        progression['Cumulative runs'] = progression.groupby('innings')['runs_total'].cumsum()
        progression['Innings'] = progression['batting_team'] + ' · ' + progression['innings'].astype(str)
        figure = px.line(progression, x='Recorded delivery', y='Cumulative runs', color='Innings', color_discrete_sequence=PALETTE)
        st.plotly_chart(chart_layout(figure), width='stretch')
        with st.expander('All selected matches'):
            st.dataframe(ordered[['start_date', 'gender', 'opponent', 'venue', 'outcome']], hide_index=True, width='stretch')
        st.download_button('Download matches', selected.to_csv(index=False), 'england_selected_matches.csv', 'text/csv', icon=':material/download:')
    with player_tab:
        st.subheader('Player Statistics')
        team_scope = st.segmented_control('Players', ['England', 'Opposition', 'All'], default='England')
        mode = st.segmented_control('Discipline', ['Batting', 'Bowling'], default='Batting')
        team_column = 'batting_team' if mode == 'Batting' else 'bowling_team'
        player_balls = balls if team_scope == 'All' else balls.loc[balls[team_column].eq('England') if team_scope == 'England' else balls[team_column].ne('England')]
        table = batting_table(player_balls, dismissals) if mode == 'Batting' else bowling_table(player_balls, dismissals)
        search = st.text_input('Player name', placeholder='Search players')
        if search:
            table = table.loc[table['Player'].str.contains(search, case=False, regex=False)]
        st.caption('Appearances count matches with recorded batting or bowling activity, not full team selections. Averages are blank when no dismissal is recorded. Combined-team views pool records across both datasets.')
        if mode == 'Batting':
            st.caption('Balls faced exclude wides and include no-balls; dismissals include run-outs. Batter names use Cricsheet labels, not unique player registry IDs.')
        if table.empty:
            st.info('No player records match this selection.')
        else:
            measure = 'Runs' if mode == 'Batting' else 'Wickets'
            figure = px.bar(table.head(12).sort_values(measure), x=measure, y='Player', orientation='h',
                            color_discrete_sequence=[PALETTE[0] if mode == 'Batting' else PALETTE[1]])
            st.plotly_chart(chart_layout(figure, 420), width='stretch')
            st.dataframe(table, hide_index=True, width='stretch')
        st.download_button('Download player statistics', table.to_csv(index=False), 'england_player_statistics.csv', 'text/csv', icon=':material/download:')
    with map_tab:
        st.subheader('Ground Map')
        if catalogue is None:
            st.warning('The local ground-coordinate catalogue is missing.')
            return
        counts = selected.groupby('venue', as_index=False).agg(Tests=('match_id', 'nunique'))
        locations = counts.merge(catalogue, on='venue', how='left', validate='one_to_one')
        unknown = locations.loc[locations['latitude'].isna(), 'venue'].tolist()
        if unknown:
            st.warning('Unmapped grounds: ' + ', '.join(unknown))
        mapped = locations.dropna(subset=['latitude', 'longitude'])
        grouped = mapped.groupby(['ground', 'country', 'latitude', 'longitude'], as_index=False)['Tests'].sum()
        if not grouped.empty:
            figure = px.scatter_map(grouped, lat='latitude', lon='longitude', size='Tests', size_max=32,
                                    hover_name='ground', hover_data={'Tests': True, 'country': True, 'latitude': False, 'longitude': False},
                                    color_discrete_sequence=[PALETTE[0]], zoom=0.5,
                                    center={'lat': 10, 'lon': 40}, map_style='carto-positron')
            st.plotly_chart(chart_layout(figure, 520), width='stretch')
            st.caption('Ground locations are approximate, from the local coordinate catalogue. Base-map tiles require internet access. Venue-name aliases are combined on the map.')
            st.dataframe(grouped[['ground', 'country', 'Tests']].sort_values('Tests', ascending=False), hide_index=True, width='stretch')
        st.download_button('Download ground counts', locations.to_csv(index=False), 'england_grounds.csv', 'text/csv', icon=':material/download:')


if __name__ == '__main__':
    main()