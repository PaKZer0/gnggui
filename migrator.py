from core.models import *
from playhouse.migrate import *
import sqlite3


def run_migrations():
    # apply modifications
    init_db()
    close_db()

    # connection for raw queries
    conn = sqlite3.connect(db_name)
    migration_check_1 = "SELECT COUNT(*) AS CNTREC " \
                        "FROM pragma_table_info('player') " \
                        "WHERE name='partida_id'"

    c = conn.cursor()
    c.execute(migration_check_1)
    migration_applied_1 = (not c.fetchone()[0])
    conn.close()

    ## 20/04/20
    if not migration_applied_1:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        # para cada Player vamos a crear un PlayerPartida con su atributo partida
        q = "INSERT INTO playerpartida (player_id, partida_id) " \
            "SELECT id, partida_id FROM player"
        c.execute(q)
        conn.commit()
        conn.close()

        # migrator
        migrator = SqliteMigrator(db)
        init_db()
        # borramos la columna partida de Player
        migrate( migrator.drop_column('player', 'partida_id'), )
