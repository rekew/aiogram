import asyncpg
import asyncio

pool = None

config = {
    "user" : "rekewka",
    "password" : "1",
    "database" : "botdatabase",
    "host" : "localhost",
    "port" : 5432
}

async def CreateTable():
    global pool
    pool = await asyncpg.create_pool(**config)

    async with pool.acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS user_roles(
                id SERIAL,
                user_id INT NOT NULL,
                role TEXT NOT NULL              
            );
        ''')

async def insertUser(id):
    async with pool.acquire() as connection:
        row = await connection.fetchrow('SELECT * from user_roles where user_id = $1', id)
        if row:
            print("THIS USER ALREADY EXISTS")
            return
        await connection.execute('''
            INSERT INTO user_roles(user_id, role) VALUES($1, 'member')
        ''', id)

async def getRole(id):
    async with pool.acquire() as connection:
        row = await connection.fetchrow('SELECT role from user_roles where user_id = $1', id)
        return row



async def closeConnection():
    global pool
    if pool:
        await pool.close()
