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
    distance = int(distance)
    days = int(days)
    if steps:
        steps = int(steps)
    golds = int(golds)
    silvers = int(silvers)
    bronzes = int(bronzes)
    speed_points = 5 * golds + 3 * silvers + 1 * bronzes
    speed_section = (
        f"""<div class="speed_points subvcenter">
            Total speed points:
            <span class="medbignumber speed_point_number">{speed_points}</span>
        </div>"""
        if speed_points > 0
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
    maybe_steps = (
        f"""<div class="total_steps subvcenter">
            Total steps: <span class="total_step_number">{steps}</span>
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
<div class="generic_head">
    <img class="logo" src="logo.png">
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
    <div class="total_km subvcenter">
        Total distance: <span class="medbignumber total_km_number">{distance}km</span>
    </div>
    <div class="attainment_days subvcenter">
        Target reached:
        <span class="medbignumber days_reached">{days} days</span>
        {maybe_12_day_medal}
    </div>
    {maybe_steps}
</div>

{maybe_medal_case}

</body>
</html>
"""


if __name__ == "__main__":
    from pathlib import Path

    out_folder = Path(__file__).parent / "out"
    out_folder.mkdir(exist_ok=True)
    (out_folder / "test_out.html").write_text(generate_html("John", 7, "Fastbois", 3, 163, 15, 117300, 1, 2, 3))
