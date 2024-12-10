from databases import Database

DATABASE_URL = "postgresql://postgres.bczothgwhbftneoksqdx:[YOUR-PASSWORD]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
database = Database(DATABASE_URL)
