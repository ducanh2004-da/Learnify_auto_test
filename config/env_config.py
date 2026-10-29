class EnvConfig:
    def __init__(self, env):
        self.env = env
        self.config = self.load_config()

    def load_config(self):
        if self.env == "dev":
            return {
                "base_url": "http://localhost:3000",
                "api_url": "http://localhost:10000/graphql",
                "db_url": "postgresql://postgres:doducanh@localhost:5432/AIInstructor2?schema=public"
            }
        elif self.env == "staging":
            return {
                "base_url": "https://staging.example.com",
                "api_url": "https://staging.example.com/api",
                "db_url": "postgresql://user:password@localhost/staging_db"
            }