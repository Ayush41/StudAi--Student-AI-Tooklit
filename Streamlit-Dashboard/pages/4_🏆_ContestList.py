import streamlit as st
from streamlit_lottie import st_lottie
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import ast
import requests
from bs4 import BeautifulSoup

def get_next_weekday_dates(weekday):
    """Return the next two dates for a given weekday (0=Monday, ..., 6=Sunday)."""
    today = datetime.now()
    results = []
    while len(results) < 2:
        today += timedelta(days=1)
        if today.weekday() == weekday:
            results.append(today.strftime("%d/%m/%Y"))
    return results

def fetch_all_contests():
    all_contests = []

    # Static platforms: GFG and LeetCode
    sunday_dates = get_next_weekday_dates(6)
    saturday_dates = get_next_weekday_dates(5)

    def add_gfg():
        return [
            {
                "platform_icon": "https://media.geeksforgeeks.org/wp-content/cdn-uploads/20210420155809/gfg-new-logo.png",
                "contest_name": "GFG Weekly Contest",
                "contest_date": date,
                "contest_time": "19:00",
                "contest_link": "https://www.geeksforgeeks.org/events/rec/gfg-weekly-coding-contest",
            } for date in sunday_dates
        ]

    def add_leetcode():
        return [
            {
                "platform_icon": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/LeetCode_Logo_black_with_text.svg/458px-LeetCode_Logo_black_with_text.svg.png",
                "contest_name": name,
                "contest_date": date,
                "contest_time": time,
                "contest_link": "https://leetcode.com/contest/"
            }
            for name, date, time in [
                ("LeetCode Weekly Contest", sunday_dates[0], "08:00"),
                ("LeetCode Biweekly Contest", saturday_dates[0], "20:00"),
                ("LeetCode Weekly Contest", sunday_dates[1], "08:00"),
                ("LeetCode Biweekly Contest", saturday_dates[1], "20:00"),
            ]
        ]

    all_contests.extend(add_gfg())
    all_contests.extend(add_leetcode())

    # CodeChef (via API)
    try:
        response = requests.get("https://www.codechef.com/api/list/contests/all?sort_by=START&sorting_order=asc&offset=0&mode=all")
        contests = ast.literal_eval(response.text).get("future_contests", [])
        for contest in contests:
            start_time = datetime.strptime(contest['contest_start_date'], '%d %b %Y %H:%M:%S')
            all_contests.append({
                "platform_icon": "https://cdn.codechef.com/sites/all/themes/abessive/cc-logo.png",
                "contest_name": contest['contest_name'],
                "contest_date": start_time.strftime('%d/%m/%Y'),
                "contest_time": start_time.strftime('%H:%M'),
                "contest_link": "https://www.codechef.com/contests"
            })
    except Exception:
        pass

    # Codeforces (via scraping)
    try:
        soup = BeautifulSoup(requests.get("https://codeforces.com/contests").text, "html.parser")
        rows = soup.select("div.datatable")[0].find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 6:
                name = cols[0].text.strip().replace("\n", " ")
                start_time = datetime.strptime(cols[2].text.strip(), '%b/%d/%Y %H:%M')
                all_contests.append({
                    "platform_icon": "https://asset.brandfetch.io/idMR4CMjcL/idPWmM8aOc.png?updated=1716797858256",
                    "contest_name": " ".join(name.split()),
                    "contest_date": start_time.strftime('%d/%m/%Y'),
                    "contest_time": start_time.strftime('%H:%M'),
                    "contest_link": "https://codeforces.com/contests"
                })
    except Exception:
        pass

    # Sort contests by date and time
    all_contests.sort(key=lambda x: (datetime.strptime(x["contest_date"], "%d/%m/%Y"), x["contest_time"]))
    return all_contests

def main():
    st.markdown("<h1 style='text-align:center;'>Contest Calendar</h1>", unsafe_allow_html=True)
    st.markdown("<center>Dominate the Leaderboard: Never Miss a Contest Again!</center>", unsafe_allow_html=True)

    with open('src/contest.json', encoding='utf-8') as anim_file:
        animation = json.load(anim_file)
    st_lottie(animation, speed=1, reverse=False, loop=True, quality="high", height=150)

    contest_list = fetch_all_contests()

    df = pd.DataFrame(contest_list)
    df.insert(0, "S.No", np.arange(1, len(df) + 1))

    df['Platform Name'] = df['platform_icon'].apply(lambda x: f'<img src="{x}" width="80" height="30">')
    df['Contest Name'] = df.apply(lambda row: f'<a href="{row["contest_link"]}" target="_blank">{row["contest_name"]}</a>', axis=1)
    df['Contest Date'] = pd.to_datetime(df['contest_date'], format="%d/%m/%Y")
    df['Contest Time'] = pd.to_datetime(df['contest_time'], format="%H:%M").dt.time
    df = df.drop(columns=['platform_icon', 'contest_name', 'contest_link'])

    df = df.sort_values(by=['Contest Date', 'Contest Time'])

    st.markdown("""
    <style>
    .table-container {
        width: 100%;
        display: flex;
        justify-content: center;
    }
    table {
        border-collapse: collapse;
        width: 90%;
        font-family: Arial, sans-serif;
        margin: 20px auto;
    }
    th {
        background-color: #cf96df;
        color: white;
        padding: 8px;
    }
    td {
        text-align: center;
        padding: 8px;
    }
    tr:nth-child(even) { background-color: #f9f9f9; color: #000; }
    tr:nth-child(odd) { background-color: #ffffff; color: #000; }
    tr:hover { background-color: #cf96df; }
    a { color: #007BFF; text-decoration: none; }
    a:hover { text-decoration: underline; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="table-container">' + df.to_html(escape=False, index=False) + '</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
