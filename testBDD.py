import mysql.connector
from env import connection_params

with mysql.connector.connect(**connection_params) as db :
    with db.cursor() as c:
        c.execute("INSERT INTO Parties (param_bonus, param_malus, param_nbTas, param_nbParties, partie_nbVictoire) \
                   values (1, 1, 10, 100, 50)")
        db.commit()