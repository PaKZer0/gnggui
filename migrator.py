from core.models import *
from playhouse.migrate import *
import sqlite3


def run_migration_check(migration_check):
    conn = sqlite3.connect(db_name)

    c = conn.cursor()
    c.execute(migration_check)
    migration_applied = c.fetchone()[0]
    conn.close()

    return migration_applied


def run_migrations():
    # apply modifications
    init_db()
    close_db()

    # connection for raw queries
    # check if column exists
    migration_check_1 = "SELECT COUNT(*) AS CNTREC " \
                        "FROM pragma_table_info('player') " \
                        "WHERE name='partida_id'"

    # the migration is not applied if the column exist
    migration_applied_1 = (not run_migration_check(migration_check_1))

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


    ## 07/05/20
    migration_check_2 = "SELECT COUNT(*) AS CNTREC " \
                        "FROM pragma_table_info('player') " \
                        "WHERE name='is_pj'"

    # the migration is not applied if the column doesn't exist yet
    migration_applied_2 = run_migration_check(migration_check_2)

    if not migration_applied_2:
        migrator = SqliteMigrator(db)
        init_db()
        # borramos la columna partida de Player
        migrate( migrator.add_column('player', 'is_pj', Player.is_pj))


    migration_check_3 = "SELECT COUNT(*) AS CNTREC " \
                        "FROM pragma_table_info('equipo') " \
                        "WHERE name='unidades'"

    # the migration is not applied if the column doesn't exist yet
    migration_applied_3 = run_migration_check(migration_check_3)

    if not migration_applied_3:
        migrator = SqliteMigrator(db)
        init_db()
        # borramos la columna partida de Player
        migrate( migrator.add_column('equipo', 'unidades', Equipo.unidades))


    migration_check_4 = "SELECT COUNT(*) AS CNTREC " \
                        "FROM pragma_table_info('equipo') " \
                        "WHERE name='equipo_asociado_id'"

    # the migration is not applied if the column doesn't exist yet
    migration_applied_4 = run_migration_check(migration_check_4)

    if not migration_applied_4:
        migrator = SqliteMigrator(db)
        init_db()
        # Añadimos la columna de equipo asociado
        # en la llamada al método se referencia a unidades pero por ser un hack:
        # si referencio a equipo_asociado, al ser una clave sobre si misma
        # intenta volver a añadir el campo, y de esta manera se añade sin problemas
        migrate( migrator.add_column('equipo', 'equipo_asociado_id', Equipo.unidades))
