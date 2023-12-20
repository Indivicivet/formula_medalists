def get_trophy_type(rank):
    return (
        "trophy_gold" if rank == 1
        else "trophy_silver" if rank == 2
        else "trophy_bronze" if rank == 3
        else "trophy_participation"
    )


def get_medal_row(count, medal_name):
    return (
        '<div class="medal_row subvcenter">\n'
        + f'<img class="medal {medal_name}" src="{medal_name}.png">' * count
        + f"""
                <span class="medal_no">x{count}</span>
            </div>"""
        if count else ""
    )


def generate_html(
    name,
    rank,
    team,
    team_rank,
    distance,
    days,
    steps,
    golds,
    silvers,
    bronzes,
):
    rank = int(rank)
    team_rank = int(team_rank)
    distance = int(distance or 0)
    days = int(days or 0)
    steps = int(steps or 0)
    golds = int(golds or 0)
    silvers = int(silvers or 0)
    bronzes = int(bronzes or 0)
    speed_points = 5 * golds + 3 * silvers + 1 * bronzes
    speed_section = (
        f"""<div class="speed_points subvcenter">
            Total speed points:
            <span class="medbignumber speed_point_number">{speed_points}</span>
        </div>"""
        if speed_points > 0
        else ""
    )
    maybe_distance = (
        f"""<div class="total_km subvcenter">
            Total distance:
            <span class="medbignumber total_km_number">{distance}km</span>
        </div>"""
        if distance
        else ""
    )
    maybe_12_day_medal = (
        """
        <img class="medal medal_xmas12"
            src="medal_12daysofxmas.png" alt="12 Days of Christmas">
        """
        if days >= 12
        else ""
    )
    maybe_days = (
        f"""<div class="attainment_days subvcenter">
            Target reached:
            <span class="medbignumber days_reached">{days} days</span>
            {maybe_12_day_medal}
        </div>"""
        if days
        else ""
    )
    maybe_steps = (
        f"""<div class="total_steps subvcenter">
            Total steps: <span class="total_step_number">{steps:,}</span>
        </div>"""
        if steps > 0
        else ""
    )
    medals_golds = get_medal_row(golds, "medal_gold")
    medals_silvers = get_medal_row(silvers, "medal_silver")
    medals_bronzes = get_medal_row(bronzes, "medal_bronze")
    maybe_medal_case = (
        f"""
<div class="medal_case bigdiv">
    <div class="medals">
        {medals_golds}
        {medals_silvers}
        {medals_bronzes}
    </div>
    {speed_section}
</div>"""
        if golds or bronzes or silvers
        else ""
    )
    return f"""
<html>
<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">
<link rel="stylesheet" href="style.css">
</head>

<body>
<div id="everything">

<div class="generic_head subvcenter">
    <img class="logo" src="logo.png">
    <span class="run_year"><span class="run_white">20</span>23</span>
</div>

<div class="standings bigdiv">
    <div class="individual subvcenter">
        <span class="name">{name}</span>
        <span class="rank subvcenter">
            <img class="individual_trophy {get_trophy_type(rank)}"
                src="{get_trophy_type(rank)}.png">
            <span class="rank_number medbignumber">#{rank}</span>
        </span>
    </div>

    <div class="team subvcenter">
        Team: <span class="team_name">{team}</span>
        <span class="team_rank subvcenter">
            <img class="team_trophy {get_trophy_type(team_rank)}"
                src="{get_trophy_type(team_rank)}.png">
            <span class="team_rank_number medbignumber">#{team_rank}</span>
        </span>
    </div>
</div>

<div class="totals bigdiv">
    {maybe_distance}
    {maybe_days}
    {maybe_steps}
</div>

{maybe_medal_case}

</div>
</body>
</html>
"""


if __name__ == "__main__":
    import csv
    from pathlib import Path

    from selenium import webdriver
    from Screenshot import Screenshot  # pip install Selenium-Screenshot

    screenshot = Screenshot.Screenshot()
    chrome = webdriver.Chrome()

    out_folder = Path(__file__).parent / "out"
    out_folder.mkdir(exist_ok=True)
    with open("data_example.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"processing {row['name']}")
            out_file = Path(__file__).parent / ".~temp_working.html"
            out_file.write_text(generate_html(**row))
            chrome.get(str(out_file.resolve()))
            screenshot.get_element(
                chrome,
                chrome.find_element(webdriver.common.by.By.ID, "everything"),
                save_path=str(Path(__file__).parent / "out"),
                image_name=f"{row['name']}.png"
            )
    chrome.close()
