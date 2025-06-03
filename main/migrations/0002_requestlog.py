from django.db import migrations

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS "main_requestlog" (
                id BIGSERIAL NOT NULL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL,
                method VARCHAR(10) NOT NULL,
                path VARCHAR(200) NOT NULL,
                query_string VARCHAR(500) NOT NULL,
                remote_ip VARCHAR(45) NOT NULL,
                user_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL
            );
            """,
            reverse_sql="""
            DROP TABLE IF EXISTS "main_requestlog";
            """
        ),
    ]
