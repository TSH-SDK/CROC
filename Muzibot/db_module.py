import asyncio
import asyncpg

from data import usr_group, usr_player


async def main():
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    await conn.execute('''
                    CREATE TABLE IF NOT EXISTS genres (
                        genres_id serial PRIMARY KEY,
                        name TEXT
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
            CREATE TABLE IF NOT EXISTS players (
                players_id serial PRIMARY KEY,
                user_id INT,
                name TEXT,
                gender_of_user VARCHAR(12), 
                age INT,
                add_text_of_player TEXT,
                photo_id TEXT
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

    await conn.execute('''
                        CREATE TABLE IF NOT EXISTS user_group_ank(
                            id serial PRIMARY KEY,
                            user_id INTEGER,
                            group_name VARCHAR(4) DEFAULT 'Нет',
                            repetition_base VARCHAR(4) DEFAULT 'Нет',
                            about_group VARCHAR(4) DEFAULT 'Нет',
                            photo_id VARCHAR(4) DEFAULT 'Нет',
                            genres VARCHAR(4) DEFAULT 'Нет',
                            group_part VARCHAR(4) DEFAULT 'Нет',
                            check_g_part VARCHAR(4) DEFAULT 'Нет',
                            gender VARCHAR(4) DEFAULT 'Нет',
                            age_range VARCHAR(4) DEFAULT 'Нет', 
                            add_text VARCHAR(4) DEFAULT 'Нет',
                            fp_genres VARCHAR(4) DEFAULT 'Нет',
                            fp_part VARCHAR(4) DEFAULT 'Нет',
                            check_fp_part VARCHAR(4) DEFAULT 'Нет'
                    )
            ''')

    await conn.execute('''
                            CREATE TABLE IF NOT EXISTS user_player_ank(
                                id serial PRIMARY KEY,
                                user_id INTEGER,
                                name VARCHAR(4) DEFAULT 'Нет',
                                gender_of_user VARCHAR(4) DEFAULT 'Нет', 
                                photo_id VARCHAR(4) DEFAULT 'Нет',
                                age VARCHAR(4) DEFAULT 'Нет',
                                add_text_of_player VARCHAR(4) DEFAULT 'Нет',
                                genres VARCHAR(4) DEFAULT 'Нет',
                                player_part VARCHAR(4) DEFAULT 'Нет',
                                check_p_part VARCHAR(4) DEFAULT 'Нет',
                                repetition_base_of_group VARCHAR(4) DEFAULT 'Нет',
                                fg_genres VARCHAR(4) DEFAULT 'Нет',
                                fg_part VARCHAR(4) DEFAULT 'Нет',
                                check_g_part VARCHAR(4) DEFAULT 'Нет'
                        )
                ''')

    await conn.execute('''
                            CREATE TABLE IF NOT EXISTS watched_player_ank(
                                id serial PRIMARY KEY,
                                groups_id INT,
                                watched_ank_id INT
                            )
                
                
                ''')

    await conn.execute('''
                            CREATE TABLE IF NOT EXISTS watched_group_ank(
                                id serial PRIMARY KEY,
                                players_id INT,
                                watched_ank_id INT
                            )
                    ''')

    await conn.execute('''  
                        CREATE TABLE IF NOT EXISTS checked_notify(
                            id serial PRIMARY KEY,
                            user_id INT,
                            checked_not INT
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


async def add(user_id, what):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    group = await conn.fetch(f'''
                        SELECT * FROM user_group_ank WHERE user_id={user_id}
                        ''')

    player = await conn.fetch(f'''
                        SELECT * FROM user_player_ank WHERE user_id={user_id}
                        ''')
    if group:
        case = None
        about_list = ["group_name", "repetition_base", "about_group", "photo_id"]
        about_list2 = ["genres", "age_range", "gender",  "add_text", "fp_genres"]
        for i in range(13):
            if group[0][usr_group[i + 1]] != "Нет":
                pass
            else:
                case = usr_group[i + 1]
                break
        await conn.execute(f'''
                        UPDATE user_group_ank SET {case}='Да' WHERE user_id={user_id}
                        ''')
        if case in about_list:
            if case != "photo_id":
                await conn.execute(f'''
                                   UPDATE groups SET {case}='{what}' WHERE user_id={user_id}
                                ''')
                await conn.close()
            else:
                await conn.execute(f'''
                                    UPDATE groups SET {case}='{what}' WHERE user_id={user_id}
                                   ''')
                await conn.close()
        else:
            group_id = await conn.fetch(f'''
                                    SELECT groups_id FROM groups WHERE user_id={user_id}
                                ''')
            fp_id = await conn.fetch(f'''
                                        SELECT fp_id FROM find_players WHERE groups_id={group_id[0]["groups_id"]}
                                                ''')
            if case == "genres":
                if what != "Закончить":
                    await conn.execute(f'''
                                    UPDATE user_group_ank SET {case}='Нет' WHERE user_id={user_id}
                                ''')
                    genre_id = await conn.fetch(f'''
                                            SELECT genres_id FROM genres WHERE name='{what}'                    
                                        ''')

                    await conn.execute(f'''
                                 INSERT INTO groups_genres(groups_id, genres_id) VALUES({group_id[0]["groups_id"]}, {genre_id[0]["genres_id"]});
                            ''')
                    await conn.close()
                else:
                    await conn.execute(f'''
                                    UPDATE user_group_ank SET genres='Да' WHERE user_id={user_id}
                                ''')
                    await conn.execute(f'''
                                    UPDATE user_group_ank SET group_part='Да' WHERE user_id={user_id}
                               ''')
                    await conn.close()
            elif case == "check_g_part":
                await conn.execute(f'''
                            UPDATE user_group_ank SET check_g_part='Да' WHERE user_id={user_id}
                        ''')
            elif case == "gender":
                await conn.execute(f'''
                                    UPDATE find_players SET gender='{what}' WHERE fp_id={fp_id[0]["fp_id"]}
                                ''')
                await conn.close()
            elif case == "age_range":
                group_id = await conn.fetch(f'''
                                            SELECT groups_id FROM groups WHERE user_id={user_id}
                                        ''')

                age = await conn.fetch(f'''
                                            SELECT age_range FROM find_players WHERE fp_id={fp_id[0]["fp_id"]}
                                        ''')
                if age[0]["age_range"] is None:
                    await conn.execute(f'''
                                UPDATE find_players SET age_range={what} WHERE groups_id={group_id[0]["groups_id"]} 
                            ''')
                    await conn.execute(f'''
                                    UPDATE user_group_ank SET age_range='Нет' WHERE user_id={user_id}
                                ''')
                elif age[0]["age_range"] is not None:
                    await conn.execute(f'''
                                UPDATE find_players SET age_range={int(str(age[0]["age_range"])+str(what))}
                            ''')
            elif case == "add_text":
                await conn.execute(f'''
                               UPDATE find_players SET add_text='{what}' WHERE groups_id={group_id[0]["groups_id"]}  
                                ''')
                await conn.close()
            elif case == "check_fp_part":
                await conn.execute(f'''
                            UPDATE user_group_ank SET check_fp_part='Да' WHERE user_id={user_id}
                        ''')
            else:
                if what != "Закончить":
                    await conn.execute(f'''
                                     UPDATE user_group_ank SET {case}='Нет' WHERE user_id={user_id}
                                ''')
                    genre_id = await conn.fetch(f'''
                                                SELECT genres_id FROM genres WHERE name='{what}'                    
                                            ''')
                    await conn.execute(f'''
                                        INSERT INTO fp_genres(fp_id, genres_id) VALUES({fp_id[0]["fp_id"]}, {genre_id[0]["genres_id"]})
                                    ''')
                    await conn.close()
                else:
                    await conn.execute(f'''
                                     UPDATE user_group_ank SET fp_part='Да' WHERE user_id={user_id}
                                 ''')
                    await conn.execute(f'''
                                    UPDATE user_group_ank SET fp_genres='Да' WHERE user_id={user_id}
                                ''')
                    await conn.close()
    else:
        case = None
        about_list = ["name", "gender_of_user", "age", "add_text_of_player", "photo_id"]
        about_list2 = ["genres", "repetition_base_of_group", "fg_genres"]
        for i in range(10):
            if player[0][usr_player[i + 3.1]] != "Нет":
                pass
            else:
                case = usr_player[i + 3.1]
                break
        await conn.execute(f'''
                            UPDATE user_player_ank SET {case}='Да' WHERE user_id={user_id}
                        ''')
        if case in about_list:
            if case != "photo_id":
                await conn.execute(f'''
                                    UPDATE players SET {case}='{what}' WHERE user_id={user_id}
                                        ''')
                await conn.close()
            else:
                await conn.execute(f'''
                                            UPDATE players SET {case}='{what}' WHERE user_id={user_id}
                                           ''')
                await conn.close()
        else:
            player_id = await conn.fetch(f'''
                                            SELECT players_id FROM players WHERE user_id={user_id}
                                        ''')
            fg_id = await conn.fetch(f'''
                                                SELECT fg_id FROM find_groups WHERE players_id={player_id[0]["players_id"]}
                                                        ''')
            if case == "genres":
                if what != "Закончить":
                    await conn.execute(f'''
                                            UPDATE user_player_ank SET {case}='Нет' WHERE user_id={user_id}
                                        ''')
                    genre_id = await conn.fetch(f'''
                                                    SELECT genres_id FROM genres WHERE name='{what}'                    
                                                ''')

                    await conn.execute(f'''
                                         INSERT INTO players_genres(players_id, genres_id) 
                                         VALUES({player_id[0]["players_id"]}, {genre_id[0]["genres_id"]});
                                    ''')
                    await conn.close()
                else:
                    await conn.execute(f'''
                                            UPDATE user_player_ank SET genres='Да' WHERE user_id={user_id}
                                        ''')
                    await conn.execute(f'''
                                            UPDATE user_player_ank SET player_part='Да' WHERE user_id={user_id}
                                       ''')
                    await conn.close()
            elif case == "check_p_part":
                await conn.execute(f'''
                                    UPDATE user_player_ank SET check_p_part='Да' WHERE user_id={user_id}
                                ''')

                await conn.close()

            elif case == "repetition_base_of_group":
                await conn.execute(f'''
                                       UPDATE find_groups SET repetition_base_of_group='{what}' 
                                       WHERE fg_id={fg_id[0]["fg_id"]}  
                                        ''')
                await conn.close()
            elif case == "check_g_part":
                await conn.execute(f'''
                                    UPDATE user_player_ank SET check_g_part='Да' WHERE user_id={user_id}
                                ''')
            else:
                if what != "Закончить":
                    await conn.execute(f'''
                                             UPDATE user_player_ank SET {case}='Нет' WHERE user_id={user_id}
                                        ''')
                    genre_id = await conn.fetch(f'''
                                                        SELECT genres_id FROM genres WHERE name='{what}'                    
                                                    ''')
                    await conn.execute(f'''
                                                INSERT INTO fg_genres(fg_id, genres_id) VALUES({fg_id[0]["fg_id"]}, {genre_id[0]["genres_id"]})
                                            ''')
                    await conn.close()
                else:
                    await conn.execute(f'''
                                             UPDATE user_player_ank SET fg_part='Да' WHERE user_id={user_id}
                                         ''')
                    await conn.execute(f'''
                                            UPDATE user_player_ank SET fg_genres='Да' WHERE user_id={user_id}
                                        ''')
                    await conn.close()


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

# newsfeed


async def check_gender(group_id, gender):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    need_list = await conn.fetch(f'''
                                    SELECT gender FROM find_players WHERE groups_id = {group_id};
                                ''')

    return need_list[0]["gender"] == gender


async def check_age(player_age, age_range):
    state = age_range[0] < player_age < age_range[1]
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


async def gets_fp_id(genre_id, rep_base):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    row = await conn.fetch(f'''
                SELECT fp_id FROM fp_genres WHERE genres_id = {genre_id};
            ''')
    await conn.close()
    i = []
    for j in row:
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


async def gets_fg_id(genre_id, group_id, age_range):
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


async def watched(ank_id, user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    row = await conn.fetch(f'''
                    SELECT players_id FROM players WHERE user_id = {user_id};
                ''')

    row2 = await conn.fetch(f'''
                        SELECT groups_id FROM groups WHERE user_id = {user_id};
                    ''')
    if row:
        check = await conn.fetch(f'''
                        SELECT watched_ank_id FROM watched_group_ank WHERE players_id={row[0]["players_id"]}
                    ''')
        for i in check:
            if ank_id == i[0]["watched_ank_id"]:
                return True
            continue
        return False

    else:
        check = await conn.fetch(f'''
                            SELECT watched_ank_id FROM watched_player_ank WHERE groups_id={row2[0]["groups_id"]}
                        ''')
        for i in check:
            if ank_id == i[0]["watched_ank_id"]:
                return False
            continue
        return False


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
        groups = await conn.fetch('''
                        SELECT * FROM groups
                    ''')
        for i in groups:
            if not await watched(i[0]["groups_id"], user_id):
                await conn.execute(f'''
                                INSERT INTO watched_group_ank(players_id, watched_ank_id) 
                                VALUES({row[0]["players_id"]}, {groups[0]["groups_id"]})
                            ''')
                await conn.close()
                if len(data) == 0:
                    return 1
                return groups
            else:
                continue
    else:
        need_list = await conn.fetch(f'''
                                SELECT age_range, fp_id FROM find_players WHERE groups_id = {row2[0]["groups_id"]};
                            ''')
        need_list2 = await conn.fetch(f'''
                                            SELECT genres_id FROM fp_genres WHERE fp_id = {need_list[0]["fp_id"]};
                                        ''')
        # age_range = [int(str(need_list[0]["age_range"])[0:2]), int(str(need_list[0]["age_range"])[2:])]

        players = await conn.fetch('''
                                SELECT * FROM players
                            ''')
        for i in players:
            if not await watched(i[0]["players_id"], user_id):
                await conn.execute(f'''
                                    INSERT INTO watched_player_ank(groups_id, watched_ank_id) 
                                    VALUES({row2[0]["groups_id"]}, {players[0]["olayers_id"]})
                            ''')
                await conn.close()
                if len(data) == 0:
                    return 1
                return players
            else:
                continue


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


async def watched_g_not(ank_id, user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    check = await conn.fetch(f'''
                    SELECT checked_not FROM checked_notify WHERE user_id={user_id}
                ''')
    for i in check:
        if ank_id == i[0]["checked_not"]:
            return True
        continue
    return False


async def watched_not(ank_id, user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    check = await conn.fetch(f'''
                        SELECT checked_not FROM checked_notify WHERE user_id={user_id}
                    ''')
    for i in check:
        if ank_id == i[0]["checked_not"]:
            return True
        continue
    return False


async def get_group_which_liked(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    p_id = await get_like_player_id(user_id)
    g_id = await conn.fetch(f'''
                    SELECT who_liked FROM liked_player WHERE players_id = {p_id}
                ''')
    for i in g_id:
        if not watched_not(i, user_id):
            data = await conn.fetch(f'''
                        SELECT * from groups WHERE groups_id = {i["who_liked"]}
                    ''')
            await conn.close()
            if len(data) == 0:
                return 1
            return data
        else:
            continue


async def get_player_who_liked(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    g_id = await get_like_group_id(user_id)
    p_id = await conn.fetch(f'''
                    SELECT who_liked FROM liked_group WHERE group_id = {g_id}
                ''')

    for i in p_id:
        if not watched_not(i, user_id):
            data = await conn.fetch(f'''
                        SELECT * from players WHERE players_id = {i["who_liked"]}
                    ''')
            await conn.close()
            if len(data) == 0:
                return 1
            return data
        else:
            continue


async def add_to_group_ank(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    await conn.execute(f'''
                    INSERT INTO user_group_ank(user_id) VALUES({user_id})
                    ''')

    await conn.execute(f'''
                        INSERT INTO groups(user_id) VALUES({user_id})
                        ''')
    group = await conn.fetch(f'''
                    SELECT * FROM groups WHERE user_id={user_id}   
                ''')
    await conn.execute(f'''
                    INSERT INTO find_players(groups_id) VALUES({group[0]["groups_id"]})
                ''')
    await conn.close()


async def add_to_player_ank(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    await conn.execute(f'''
                    INSERT INTO user_player_ank(user_id) VALUES({user_id})
                    ''')
    await conn.execute(f'''
                    INSERT INTO players(user_id) VALUES({user_id})
                    ''')
    player = await conn.fetch(f'''
                        SELECT * FROM players WHERE user_id={user_id}   
                    ''')
    await conn.execute(f'''
                        INSERT INTO find_groups(players_id) VALUES({player[0]["players_id"]})
                    ''')
    await conn.close()


async def choose_next_func(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    group = await conn.fetch(f'''
                            SELECT * FROM user_group_ank WHERE user_id={user_id}
                            ''')
    player = await conn.fetch(f'''
                    SELECT * FROM user_player_ank WHERE user_id={user_id}
                ''')
    await conn.close()
    if group:
        for i in range(15):
            if i == 13:
                return 12
            elif group[0][usr_group[i+1]] == "Нет":
                return i-1
            else:
                continue
    else:
        for i in range(14):
            if i == 12:
                return 11.1
            elif player[0][usr_player[i+1.1]] == "Нет":
                return i-0.9
            else:
                continue


async def get_fp_age(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    group_id = await conn.fetch(f'''
                            SELECT groups_id FROM groups WHERE user_id={user_id}
                        ''')
    age = await conn.fetch(f'''
                            SELECT age_range FROM find_players WHERE groups_id={group_id[0]["groups_id"]}
                        ''')
    await conn.close()
    return age[0]["age_range"]


async def all_is_ok(user_id):  # check whether all the column in user_group_ank or user_player_ank are completed
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    group = await conn.fetch(f'''
                        SELECT * FROM user_group_ank WHERE user_id={user_id}
                    ''')
    player = await conn.fetch(f'''
                        SELECT * FROM user_player_ank WHERE user_id={user_id}
                    ''')
    await conn.close()

    if group:
        for i in group[0]:
            if group[0][i] == "Нет":
                return False
            else:
                return True
    else:
        for i in player[0]:
            if player[0][i] == "Нет":
                return False
            else:
                return True


async def finished_sector(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    group = await conn.fetch(f'''
                            SELECT * FROM user_group_ank WHERE user_id={user_id}
                        ''')
    player = await conn.fetch(f'''
                            SELECT * FROM user_player_ank WHERE user_id={user_id}
                        ''')

    await conn.close()

    if group:
        if group[0]["check_g_part"] != "Да":
            return [True, "group_part"]
        elif group[0]["check_fp_part"] != "Да":
            return [True, "fp_part"]
        else:
            return [False, False]
    else:
        if player[0]["check_p_part"] != "Да":
            return [True, "player_part"]
        elif player[0]["check_g_part"] != "Да":
            return [True, "fg_part"]
        else:
            return [False, False]


async def checked_sector(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    group = await conn.fetch(f'''
                            SELECT * FROM user_group_ank WHERE user_id={user_id}
                        ''')
    player = await conn.fetch(f'''
                            SELECT * FROM user_player_ank WHERE user_id={user_id}
                        ''')

    await conn.close()

    if group:
        if group[0]["check_g_part"] != "Да":
            return [True, "check_g_part"]
        elif group[0]["check_fp_part"] != "Да":
            return [True, "check_fp_part"]
        else:
            return [False, False]
    else:
        if player[0]["check_p_part"] != "Да":
            return [True, "check_p_part"]
        elif player[0]["check_fg_part"] != "Да":
            return [True, "check_fg_part"]
        else:
            return [False, False]


async def edit_check_point(user_id, sector):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    group = await conn.fetch(f'''
                               SELECT * FROM user_group_ank WHERE user_id={user_id}
                           ''')
    player = await conn.fetch(f'''
                               SELECT * FROM user_player_ank WHERE user_id={user_id}
                           ''')

    if group:
        await conn.fetch(f'''
                UPDATE user_group_ank SET {sector}="Да" WHERE user_id={user_id}
                ''')
    else:
        await conn.fetch(f'''
                UPDATE user_player_ank SET {sector}="Да" WHERE user_id={user_id}
                ''')
    await conn.close()


async def check_genres(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    group = await conn.fetch(f'''
                                  SELECT * FROM groups WHERE user_id={user_id}
                              ''')
    player = await conn.fetch(f'''
                                  SELECT * FROM players WHERE user_id={user_id}
                              ''')
    if group:
        genres = await conn.fetch(f'''
                                SELECT * FROM groups_genres WHERE groups_id={group[0]["groups_id"]}
                            ''')
        return genres
    else:
        genres = await conn.fetch(f'''
                                        SELECT * FROM players_genres WHERE players_id={player[0]["players_id"]}
                                    ''')
        return genres


async def check_find_genres(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    group = await conn.fetch(f'''
                                      SELECT * FROM groups WHERE user_id={user_id}
                                  ''')
    player = await conn.fetch(f'''
                                      SELECT * FROM players WHERE user_id={user_id}
                                  ''')

    if group:
        fp = await conn.fetch(f'''
                        SELECT * FROM find_players WHERE groups_id={group[0]["groups_id"]}
                    ''')
        genres = await conn.fetch(f'''
                                    SELECT * FROM fp_genres WHERE fp_id={fp[0]["fp_id"]}
                                ''')
        return genres
    else:
        fg = await conn.fetch(f'''
                            SELECT * FROM find_groups WHERE players_id={player[0]["players_id"]}
                        ''')
        genres = await conn.fetch(f'''
                                SELECT * FROM fg_genres WHERE fg_id={fg[0]["fg_id"]}
                                        ''')
        return genres


async def get_group_data(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    data1 = await conn.fetch(f'''
                    SELECT * FROM groups WHERE user_id={user_id} 
                ''')
    genres_id = await conn.fetch(f'''
                    SELECT genres_id FROM groups_genres WHERE groups_id={data1[0]["groups_id"]}
                ''')
    data2 = []
    for i in genres_id:
        name = await conn.fetch(f'''
                    SELECT name FROM genres WHERE genres_id={i["genres_id"]} 
                ''')
        data2.append(name)
    return data1 + data2


async def get_player_data(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    data1 = await conn.fetch(f'''
                    SELECT * FROM players WHERE user_id={user_id} 
                ''')
    genres_id = await conn.fetch(f'''
                    SELECT genres_id FROM players_genres WHERE players_id={data1[0]["players_id"]}
                ''')
    data2 = []
    for i in genres_id:
        name = await conn.fetch(f'''
                    SELECT name FROM genres WHERE genres_id={i["genres_id"]} 
                ''')
        data2.append(name)
    return data1 + data2


async def get_about_player_data(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    group = await conn.fetch(f'''
                        SELECT groups_id FROM groups WHERE user_id={user_id} 
                    ''')
    data1 = await conn.fetch(f'''
                        SELECT * FROM find_players WHERE groups_id={group[0]["groups_id"]}
                    ''')
    genres_id = await conn.fetch(f'''
                        SELECT genres_id FROM fp_genres WHERE fp_id={data1[0]["fp_id"]}
                    ''')
    data2 = []
    for i in genres_id:
        name = await conn.fetch(f'''
                        SELECT name FROM genres WHERE genres_id={i["genres_id"]} 
                    ''')
        data2.append(name)
    return data1 + data2


async def get_about_group_data(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')
    player = await conn.fetch(f'''
                        SELECT players_id FROM players WHERE user_id={user_id} 
                    ''')
    data1 = await conn.fetch(f'''
                        SELECT * FROM find_groups WHERE players_id={player[0]["players_id"]}
                    ''')
    genres_id = await conn.fetch(f'''
                        SELECT genres_id FROM fg_genres WHERE fg_id={data1[0]["fg_id"]}
                    ''')
    data2 = []
    for i in genres_id:
        name = await conn.fetch(f'''
                        SELECT name FROM genres WHERE genres_id={i["genres_id"]} 
                    ''')
        data2.append(name)
    return data1 + data2


async def all_is_done(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    group = await conn.fetch(f'''
                                SELECT * FROM user_group_ank WHERE user_id={user_id}
                               ''')
    player = await conn.fetch(f'''
                                   SELECT * FROM user_player_ank WHERE user_id={user_id}
                               ''')
    if group:
        if group[0]["check_g_part"] == "Да" and group[0]["check_fp_part"] == "Да":
            return True
        return False
    else:
        if player[0]["check_p_part"] == "Да" and player[0]["check_g_part"] == "Да":
            return True
        return False


async def get_check_sector(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    group = await conn.fetch(f'''
                                    SELECT * FROM user_group_ank WHERE user_id={user_id}
                                   ''')
    player = await conn.fetch(f'''
                                       SELECT * FROM user_player_ank WHERE user_id={user_id}
                                   ''')
    if group:
        if group[0]["check_g_part"] == "Нет":
            return "check_g_part"
        elif group[0]["check_fp_part"] == "Нет":
            return "check_fp_part"
    else:
        if player[0]["check_p_part"] == "Нет":
            return "check_p_part"
        elif player[0]["check_g_part"] == "Нет":
            return "check_g_part"


async def get_sector(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    group = await conn.fetch(f'''
                            SELECT * FROM user_group_ank WHERE user_id={user_id}
                            ''')
    player = await conn.fetch(f'''
                                SELECT * FROM user_player_ank WHERE user_id={user_id}
                            ''')
    if group:
        if group[0]["check_g_part"] == "Нет":
            return "group_part"
        elif group[0]["check_fp_part"] == "Нет":
            return "fp_part"
    else:
        if player[0]["check_p_part"] == "Нет":
            return "player_part"
        elif player[0]["check_g_part"] == "Нет":
            return "fg_part"


async def make_no(user_id, case):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    group = await conn.fetch(f'''
                                SELECT * FROM user_group_ank WHERE user_id={user_id}
                                   ''')
    player = await conn.fetch(f'''
                                SELECT * FROM user_player_ank WHERE user_id={user_id}
                                   ''')
    if group:
        await conn.execute(f'''
                        UPDATE user_group_ank SET {case}='Нет' WHERE user_id={user_id}
                    ''')
        if case == "age_range":
            groups_id = await conn.fetch(f'''
                                SELECT groups_id FROM groups WHERE user_id={user_id}
                                   ''')
            await conn.execute(f'''
                            UPDATE find_players SET age_range=null WHERE groups_id={groups_id[0]["groups_id"]}
                        ''')
    else:
        await conn.execute(f'''
                        UPDATE user_player_ank SET {case}='Нет' WHERE user_id={user_id}
                    ''')


async def clear_genres(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    group = await conn.fetch(f'''
                                    SELECT groups_id FROM groups WHERE user_id={user_id}
                                       ''')
    player = await conn.fetch(f'''
                                    SELECT players_id FROM players WHERE user_id={user_id}
                                       ''')
    sector = await get_sector(user_id)

    if group:
        if sector == "fp_part":
            fp_id = await conn.fetch(f'''
                            SELECT fp_id FROM find_players WHERE groups_id={group[0]["groups_id"]}
                        ''')
            await conn.fetch(f'''
                            DELETE FROM fp_genres WHERE fp_id={fp_id[0]["fp_id"]}
                        ''')
            await conn.close()
        elif sector == "group_part":
            groups_id = await conn.fetch(f'''
                            SELECT groups_id FROM groups WHERE user_id={user_id}
                        ''')
            await conn.fetch(f'''
                            DELETE FROM groups_genres WHERE groups_id={groups_id[0]["groups_id"]}
                        ''')
            await conn.close()
    else:
        if sector == "fg_part":
            fg_id = await conn.fetch(f'''
                            SELECT fg_id FROM find_groups WHERE players_id={player[0]["players_id"]}
                        ''')
            await conn.fetch(f'''
                            DELETE FROM fg_genres WHERE fg_id={fg_id[0]["fg_id"]}
                        ''')
            await conn.close()
        elif sector == "player_part":
            players_id = await conn.fetch(f'''
                            SELECT players_id FROM players WHERE user_id={user_id}
                        ''')
            await conn.fetch(f'''
                            DELETE FROM players_genres WHERE players_id={players_id[0]["players_id"]}
                        ''')
            await conn.close()


async def group_age(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    group = await conn.fetch(f'''
                        SELECT groups_id FROM groups WHERE user_id={user_id}
                               ''')
    if group:
        return True
    return False


async def check_false(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    group = await conn.fetch(f'''
                                        SELECT * FROM user_group_ank WHERE user_id={user_id}
                                           ''')
    player = await conn.fetch(f'''
                                            SELECT * FROM user_player_ank WHERE user_id={user_id}
                                               ''')
    if group:
        for i in range(13):
            if group[0][usr_group[i + 1]] != "Нет":
                pass
            else:
                return usr_group[i + 1]
    else:
        for i in range(10):
            if player[0][usr_player[i + 3.1]] != "Нет":
                pass
            else:
                return usr_player[i + 3.1]


async def delete_all(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    group = await conn.fetch(f'''
                                        SELECT * FROM groups WHERE user_id={user_id}
                                           ''')
    player = await conn.fetch(f'''
                                            SELECT * FROM players WHERE user_id={user_id}
                                               ''')
    if group:
        await conn.execute(f'''
                    DELETE FROM groups_genres WHERE groups_id={group[0]["groups_id"]}
                ''')
        fp_id = await conn.fetch(f'''
                 SELECT fp_id FROM find_players WHERE groups_id={group[0]["groups_id"]}
                ''')
        await conn.execute(f'''
                            DELETE FROM fp_genres WHERE fp_id={fp_id[0]["fp_id"]}
                        ''')
        await conn.fetch(f'''
                        DELETE FROM find_players WHERE groups_id={group[0]["groups_id"]}
                    ''')
        await conn.execute(f'''
                            DELETE FROM groups WHERE user_id={user_id}
                        ''')
        await conn.execute(f'''
                            DELETE FROM user_group_ank WHERE user_id={user_id}
                        ''')
    else:
        await conn.execute(f'''
                            DELETE FROM players_genres WHERE players_id={player[0]["players_id"]}
                        ''')
        fg_id = await conn.fetch(f'''
                         SELECT fg_id FROM find_groups WHERE players_id={player[0]["players_id"]}
                        ''')
        await conn.execute(f'''
                            DELETE FROM fg_genres WHERE fg_id={fg_id[0]["fg_id"]}
                                ''')
        await conn.fetch(f'''
                                DELETE FROM find_groups WHERE players_id={player[0]["players_id"]}
                            ''')
        await conn.execute(f'''
                                    DELETE FROM players WHERE user_id={user_id}
                                ''')
        await conn.execute(f'''
                                    DELETE FROM user_player_ank WHERE user_id={user_id}
                                ''')


async def photo_needed(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    group = await conn.fetch(f'''
                                            SELECT * FROM user_group_ank WHERE user_id={user_id}
                                               ''')
    player = await conn.fetch(f'''
                                                SELECT * FROM user_player_ank WHERE user_id={user_id}
                                                   ''')
    if group:
        if group[0]["about_group"] == "Да" and group[0]["photo_id"] == "Нет":
            return True
        return False
    else:
        if player[0]["gender_of_user"] == "Да" and player[0]["photo_id"] == "Нет":
            return True
        return False


async def age_needed(user_id):
    conn = await asyncpg.connect(user="postgres", database="muzibara_bot", password="12345", host='127.0.0.1')

    group = await conn.fetch(f'''
                                            SELECT * FROM user_group_ank WHERE user_id={user_id}
                                               ''')
    player = await conn.fetch(f'''
                                                SELECT * FROM user_player_ank WHERE user_id={user_id}
                                                   ''')
    if group:
        if group[0]["gender"] == "Да" and group[0]["age_range"] == "Нет":
            return True
        return False
    else:
        if player[0]["photo_id"] == "Да" and player[0]["age"] == "Нет":
            return True
        return False
asyncio.run(main())
