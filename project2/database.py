import asyncpg

url = 'postgresql://postgres:xmkdeFCULDfYHtkoYyxJhXMclfuPpmDL@turntable.proxy.rlwy.net:25674/railway'

hostname = 'localhost'
database = 'project2'
username = 'rekewka'
pwd = '1'
port_id = 5432

botToken = '7567179133:AAHxQqBJVo6vG25SOxxny80DX-OVQGK1bIs'

async def initDb():
    connection = await asyncpg.connect(url)

    await connection.execute('''
        create table if not exists users(
            id INT PRIMARY KEY
        )
                ''')
    await connection.close()

async def insertUser(id):
    connection = await asyncpg.connect(url)

    await connection.execute('''
        INSERT INTO users(id) VALUES ($1)
        ON CONFLICT (id) DO NOTHING
    ''', id)
    await connection.close()

async def getUsers():
    connection = await asyncpg.connect(url)

    rows = await connection.fetch('select * from users')
    await connection.close()
    return rows
