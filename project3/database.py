import asyncpg
import asyncio

config = {
    "user": "rekewka",
    "password": "1",
    "database": "project3",
    "host": "localhost",
    "port": 5432
}

pool = None

async def startDatabase():
    global pool
    pool = await asyncpg.create_pool(**config)

    async with pool.acquire() as connection:
        await connection.execute('''
        CREATE TABLE IF NOT EXISTS todos(
            index SERIAL PRIMARY KEY,
            id INT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            deadline DATE,
            notify BOOLEAN NOT NULL
        );
        ''')

async def insertTask(data, user_id):
    async with pool.acquire() as connection:
        await connection.execute('''
        INSERT INTO todos (id, name, description, deadline, notify)
        VALUES ($1, $2, $3, $4, $5)
        ''', user_id, data['name'], data['description'], data['deadline'], data['notify'])

async def getTask(user_id):
    async with pool.acquire() as connection:
        rows = await connection.fetch('''
        SELECT index, name, description, deadline, notify 
        FROM todos 
        WHERE id = $1
        ORDER BY index ASC
        ''', user_id)
        return rows

async def remove_task_from_db(task_id):
    async with pool.acquire() as connection:
        row = await connection.fetchrow('''
        DELETE FROM todos 
        WHERE index = $1
        RETURNING index
        ''', task_id)
        return row is not None

async def get_tasks_due_today():
    async with pool.acquire() as connection:
        rows = await connection.fetch('''
        SELECT id, name, description FROM todos 
        WHERE deadline = CURRENT_DATE AND notify = TRUE
        ''')
        return rows

async def closeDatabase():
    global pool
    if pool:
        await pool.close()
