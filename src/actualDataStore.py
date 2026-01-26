import sqlite3 as spl3

connection = spl3.connect("teamData.db")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS teleopt_stats")
cursor.execute("DROP TABLE IF EXISTS specs")
cursor.execute("DROP TABLE IF EXISTS auto_stats")

#The Stats of Each Robot in the Teleopt Stage
teleopt = ("""
CREATE TABLE IF NOT EXISTS teleopt_stats (
    team INTEGER,
    score INTEGER,
    climb_speed INTEGER,
    climb_level INTEGER,
    times_stuck INTEGER
)
""")

cursor.execute(teleopt)

teams_teleopt = [
    (3756, 0, 0, 0, 0)
]

cursor.executemany(
    "INSERT INTO teleopt_stats (team, score, climb_speed, climb_level, times_stuck) VALUES (?, ?, ?, ?, ?)",
    teams_teleopt
)

#What Specs Every Team's Robot Has
robotSpec = ("""
CREATE TABLE IF NOT EXISTS specs (
    team INTEGER,
    drive_train TEXT NOT NULL,
    shooter TEXT NOT NULL,
    intake TEXT NOT NULL,
    climb TEXT NOT NULL,
    fuel_storage_l REAL,
    bumps_trench TEXT NOT NULL
)
""")

cursor.execute(robotSpec)

robot_specs = [
    (3756, "h", "h", "h", "h", 0.0, "h")
]

cursor.executemany(
    "INSERT INTO specs (team, drive_train, shooter, intake, climb, fuel_storage_l, bumps_trench) VALUES (?, ?, ?, ?, ?, ?, ?)",
    robot_specs
)

#The Stats of Each Robot in the Automatic
auto = ("""
CREATE TABLE IF NOT EXISTS auto_stats (
    team INTEGER,
    steps TEXT NOT NULL,
    success TEXT NOT NULL,
    auto_points INTEGER
)
""")

cursor.execute(auto)

teams_auto = [
    (3765, "h", "h", 0)
]

cursor.executemany(
    "INSERT INTO auto_stats (team, steps, success, auto_points) VALUES (?, ?, ?, ?)",
    teams_auto
)



connection.commit()

cursor.execute("SELECT * FROM teleopt_stats")
cursor.fetchall()

cursor.execute("SELECT * FROM specs")
cursor.fetchall()

cursor.execute("SELECT * FROM auto_stats")
cursor.fetchall()
