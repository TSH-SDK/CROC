import asyncio
import asyncpg

from data import about_player_info_form, finding_group_info_form, about_group_info_form, finding_player_info_form


async def main():
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    await conn.execute('''
                    CREATE TABLE IF NOT EXISTS genres (
                        genres_id serial PRIMARY KEY,
                        name TEXT
                    )
                ''')
    await conn.execute('''
            CREATE TABLE IF NOT EXISTS players (
                players_id serial PRIMARY KEY,
                user_id INT,
                name TEXT,
                gender_of_user VARCHAR(12), 
                age INT,
                add_text_of_player TEXT
            )
        ''')
    await conn.execute('''
            CREATE TABLE IF NOT EXISTS liked_player(
                id serial PRIMARY KEY,
                players_id INT,
                who_liked INT, 
                FOREIGN KEY (players_id) REFERENCES players(players_id), 
                FOREIGN KEY (who_liked) REFERENCES groups(groups_id)
            )
        ''')

    await conn.execute('''
            CREATE TABLE IF NOT EXISTS players_genres(
                id serial PRIMARY KEY,
                players_id INTEGER NOT NULL REFERENCES players,
                genres_id INTEGER NOT NULL REFERENCES genres,
                UNIQUE(players_id, genres_id)
            )
    ''')

    await conn.execute('''
            CREATE TABLE IF NOT EXISTS groups(
                groups_id serial PRIMARY KEY,
                user_id INT,
                group_name TEXT,
                repetition_base VARCHAR(4),
                about_group TEXT,
                photo_id TEXT
            )
        ''')

    await conn.execute('''
                CREATE TABLE IF NOT EXISTS liked_group(
                    id serial PRIMARY KEY,
                    group_id INT,
                    who_liked INT, 
                    FOREIGN KEY (group_id) REFERENCES groups(groups_id), 
                    FOREIGN KEY (who_liked) REFERENCES players(players_id)
                )
            ''')

    await conn.execute('''
                CREATE TABLE IF NOT EXISTS groups_genres(
                    id serial PRIMARY KEY,
                    groups_id INTEGER NOT NULL REFERENCES groups,
                    genres_id INTEGER NOT NULL REFERENCES genres,
                    UNIQUE(groups_id, genres_id)
                )
        ''')

    await conn.execute('''
                CREATE TABLE IF NOT EXISTS find_players (
                    fp_id serial PRIMARY KEY,
                    gender VARCHAR(24),
                    age_range INT, 
                    add_text TEXT,
                    groups_id INT,
                    FOREIGN KEY (groups_id) REFERENCES groups(groups_id)
                    
                )
            ''')
    await conn.execute('''
                    CREATE TABLE IF NOT EXISTS fp_genres(
                        id serial PRIMARY KEY,
                        fp_id INTEGER NOT NULL REFERENCES find_players,
                        genres_id INTEGER NOT NULL REFERENCES genres,
                        UNIQUE(fp_id, genres_id)
                    )
            ''')

    await conn.execute('''
                CREATE TABLE IF NOT EXISTS find_groups (
                    fg_id serial PRIMARY KEY,
                    repetition_base_of_group VARCHAR(4),
                    players_id INT,
                    FOREIGN KEY (players_id) REFERENCES players(players_id)
                )
            ''')
    await conn.execute('''
                        CREATE TABLE IF NOT EXISTS fg_genres(
                            id serial PRIMARY KEY,
                            fg_id INTEGER NOT NULL REFERENCES find_groups,
                            genres_id INTEGER NOT NULL REFERENCES genres,
                            UNIQUE(fg_id, genres_id)
                        )
                ''')

    await conn.close()


async def check_user(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    row = await conn.fetch(f'''
            SELECT players_id FROM players WHERE user_id = {user_id};
        ''')
    row2 = await conn.fetch(f'''
            SELECT groups_id FROM groups WHERE user_id = {user_id}
                ''')
    await conn.close()
    if row or row2:
        return True
    return False


async def get_genre_id(genre):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    row = await conn.fetch(f'''
        SELECT genres_id FROM genres WHERE name = '{genre}';
    ''')
    await conn.close()

    for i in row:
        return i["genres_id"]

# player section


async def get_user_id(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    row = await conn.fetch(f'''
             SELECT players_id FROM players WHERE user_id = {user_id};
        ''')

    await conn.close()

    for i in row:
        return i["players_id"]


async def get_fg_id(player_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    row = await conn.fetch(f'''
             SELECT fg_id FROM find_groups WHERE players_id = {player_id};
        ''')

    await conn.close()

    for i in row:
        return int(i["fg_id"])

    await conn.close()


async def add_fg_genres(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    fg_id = await get_fg_id(user_id)
    for i in finding_group_info_form["genre_of_group"]:
        genre_id = await (get_genre_id(i))

        await conn.execute(f'''
                     INSERT INTO fg_genres(fg_id, genres_id) VALUES({fg_id}, {genre_id});
                ''')

    await conn.close()


async def add_find_group():
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    player_id = await (get_user_id(about_player_info_form["user_id"]))

    await conn.execute(f'''
             INSERT INTO find_groups(repetition_base_of_group, players_id) VALUES(
                '{finding_group_info_form["repetition_base_of_group"]}', {player_id}
             )''')

    await conn.close()

    await (add_fg_genres(player_id))


async def add_players_genres():
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    for i in about_player_info_form["genre_of_user"]:
        genre_id = await (get_genre_id(i))
        player_id = await (get_user_id(about_player_info_form["user_id"]))

        await conn.execute(f'''
             INSERT INTO players_genres(players_id, genres_id) VALUES({player_id}, {genre_id});
        ''')

    await conn.close()


async def add_player():
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    await conn.execute(f'''
         INSERT INTO players(user_id, name, gender_of_user, age, add_text_of_player) VALUES(
            {about_player_info_form["user_id"]}, '{about_player_info_form["name"]}', 
            '{about_player_info_form["gender_of_user"]}', {about_player_info_form["age"]},
            '{about_player_info_form["add_text_of_player"]}')
    ''')

    await conn.close()

    await (add_players_genres())
    await (add_find_group())


# group section


async def get_group_cap_id(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    row = await conn.fetch(f'''
             SELECT groups_id FROM groups WHERE user_id = {user_id};
        ''')

    await conn.close()

    for i in row:
        return i["groups_id"]


async def get_fp_id(group_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    row = await conn.fetch(f'''
             SELECT fp_id FROM find_players WHERE groups_id = {group_id};
        ''')

    await conn.close()

    for i in row:
        return int(i["fp_id"])

    await conn.close()


async def add_fp_genres(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    fp_id = await get_fp_id(user_id)

    for i in finding_group_info_form["genre_of_group"]:
        genre_id = await (get_genre_id(i))

        await conn.execute(f'''
                     INSERT INTO fp_genres(fp_id, genres_id) VALUES({fp_id}, {genre_id});
                ''')

    await conn.close()


async def add_find_player():
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    group_id = await (get_group_cap_id(about_group_info_form["user_id"]))

    await conn.execute(f'''
             INSERT INTO find_players(gender, age_range, add_text, groups_id) VALUES(
                '{finding_player_info_form["gender"]}', {finding_player_info_form["age_range"][0]}{finding_player_info_form["age_range"][1]}, '{finding_player_info_form["add_text"]}', {group_id}
             )''')

    await conn.close()

    await (add_fp_genres(group_id))


async def add_groups_genres():
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    for i in about_group_info_form["genre"]:
        genre_id = await (get_genre_id(i))
        groups_id = await (get_group_cap_id(about_group_info_form["user_id"]))

        await conn.execute(f'''
             INSERT INTO groups_genres(groups_id, genres_id) VALUES({groups_id}, {genre_id});
        ''')

    await conn.close()


async def add_group():
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    await conn.execute(f'''
             INSERT INTO groups(user_id, group_name, repetition_base, about_group, photo_id) VALUES(
                {about_group_info_form["user_id"]}, '{about_group_info_form["group_name"]}', 
                '{about_group_info_form["repetition_base"]}', '{about_group_info_form["about_group"]}',
                '{about_group_info_form["photo_id"]}');
        ''')

    await conn.close()

    await (add_groups_genres())
    await (add_find_player())

# newsfeed


async def check_gender(group_id, gender):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    need_list = await conn.fetch(f'''
                                    SELECT gender FROM find_players WHERE groups_id = {group_id};
                                ''')
    print(need_list[0]["gender"] == gender)

    return need_list[0]["gender"] == gender


async def check_age(player_age, age_range):
    state = age_range[0] < player_age < age_range[1]
    print(state)
    return state


async def check_rep_base(rep_base, group_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    base = await conn.fetch(f'''
                    SELECT repetition_base FROM groups WHERE groups_id = {group_id}
                ''')
    if rep_base == "Нет":
        return True
    else:
        state = rep_base == base
        return state


async def get_group_id(fp_ids, rep_base):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    data = []
    for i in fp_ids:
        row = await conn.fetch(f'''
                            SELECT groups_id FROM find_players WHERE fp_id = {i};
                        ''')
        if await check_rep_base(rep_base, row[0]["groups_id"]):
            data.append(row)
        else:
            continue
    await conn.close()
    return data


async def get_fp_id(genre_id, rep_base):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    row = await conn.fetch(f'''
                SELECT fp_id FROM fp_genres WHERE genres_id = {genre_id};
            ''')
    await conn.close()
    i = []
    for j in row:
        print(j["fp_id"])
        i.append(j["fp_id"])
    ids = await get_group_id(i, rep_base)
    return ids


async def get_player_id(fg_ids, group_id, age_range):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    data = []
    for i in fg_ids:
        row = await conn.fetch(f'''
                            SELECT players_id FROM find_groups WHERE fg_id = {i};
                        ''')
        player_gender = await conn.fetch(f'''
                            SELECT gender_of_user FROM players WHERE players_id = {row[0]["players_id"]}    
                        ''')
        print(player_gender[0])
        player_age = await conn.fetch(f'''
                            SELECT age FROM players WHERE players_id = {row[0]["players_id"]}    
                        ''')
        if await check_gender(group_id, player_gender[0]["gender_of_user"]) and await check_age(player_age[0]["age"],
                                                                                                age_range):
            data.append(row)
        else:
            continue
    await conn.close()
    return data


async def get_fg_id(genre_id, group_id, age_range):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    row = await conn.fetch(f'''
                SELECT fg_id FROM fg_genres WHERE genres_id = {genre_id};
            ''')
    await conn.close()
    i = []
    for j in row:
        i.append(j["fg_id"])
    ids = await get_player_id(i, group_id, age_range)
    return ids


async def db_newsfeed(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    data = []
    row = await conn.fetch(f'''
                SELECT players_id FROM players WHERE user_id = {user_id};
            ''')

    row2 = await conn.fetch(f'''
                    SELECT groups_id FROM groups WHERE user_id = {user_id};
                ''')
    if row:
        need_list = await conn.fetch(f'''
                        SELECT repetition_base_of_group, fg_id FROM find_groups WHERE players_id = {row[0]["players_id"]};
                    ''')
        need_list2 = await conn.fetch(f'''
                        SELECT genres_id FROM fg_genres WHERE fg_id = {need_list[0]["fg_id"]};
                    ''')
        for i in need_list2:
            for j, n in enumerate(await get_fp_id(i["genres_id"], need_list[0]["repetition_base_of_group"])):
                return_data2 = await conn.fetch(f'''
                        SELECT * FROM groups WHERE groups_id = {n[j]["groups_id"]};
                    ''')
                data.append(return_data2)
        await conn.close()
        return data
    else:
        need_list = await conn.fetch(f'''
                                SELECT age_range, fp_id FROM find_players WHERE groups_id = {row2[0]["groups_id"]};
                            ''')
        need_list2 = await conn.fetch(f'''
                                            SELECT genres_id FROM fp_genres WHERE fp_id = {need_list[0]["fp_id"]};
                                        ''')
        age_range = [int(str(need_list[0]["age_range"])[0:2]), int(str(need_list[0]["age_range"])[2:])]
        for i in need_list2:
            for j, n in enumerate(await get_fg_id(i["genres_id"], row2[0]["groups_id"], age_range)):
                return_data2 = await conn.fetch(f'''
                                SELECT * FROM players WHERE players_id = {n[j]["players_id"]};
                            ''')
                data.append(return_data2)
        await conn.close()
        print(data)
        return data


async def is_player(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    row = await conn.fetch(f'''
                SELECT players_id FROM players WHERE user_id = {user_id};
            ''')
    await conn.close()

    if row:
        return True
    return False


async def get_like_group_id(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    row = await conn.fetch(f'''
                        SELECT groups_id FROM groups WHERE user_id = {user_id};
                    ''')
    await conn.close()
    return row[0]["groups_id"]


async def get_like_player_id(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    row = await conn.fetch(f'''
                    SELECT players_id FROM players WHERE user_id = {user_id};
                ''')
    await conn.close()
    return row[0]["players_id"]


async def like_group(who, whom):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    g_id = await get_like_group_id(whom)
    p_id = await get_like_player_id(who)
    await conn.execute(f'''
            INSERT INTO liked_group(group_id, who_liked) VALUES({g_id}, {p_id})
        ''')
    await conn.close()


async def like_player(who, whom):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    g_id = await get_like_group_id(who)
    p_id = await get_like_player_id(whom)
    await conn.execute(f'''
               INSERT INTO liked_player(players_id, who_liked) VALUES({p_id}, {g_id})
           ''')
    await conn.close()


async def get_group_which_liked(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    p_id = await get_like_player_id(user_id)
    g_id = await conn.fetch(f'''
                    SELECT who_liked FROM liked_player WHERE players_id = {p_id}
                ''')

    ankets = []
    for i in g_id:
        data = await conn.fetch(f'''
                    SELECT * from groups WHERE groups_id = {i["who_liked"]}
                ''')
        ankets.append(data)
    await conn.close()
    return ankets


async def get_player_who_liked(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    g_id = await get_like_group_id(user_id)
    p_id = await conn.fetch(f'''
                    SELECT who_liked FROM liked_group WHERE group_id = {g_id}
                ''')

    ankets = []
    for i in p_id:
        data = await conn.fetch(f'''
                    SELECT * from players WHERE players_id = {i["who_liked"]}
                ''')
        ankets.append(data)
    await conn.close()
    return ankets


asyncio.run(main())
