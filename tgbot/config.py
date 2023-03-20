from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    database_url: str


@dataclass
class TgBot:
    token: str
    admin_ids: list
    group_ids: int
    use_redis: bool


@dataclass
class Miscellaneous:
    sentry_sdk: str
    playmobile_api: str
    payme: str
    click: str

@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            group_ids=env.int("GROUP"),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            database_url=env.str("DB_API")
        ),
        misc=Miscellaneous(
            sentry_sdk=env.str("SENTRY_SDK"),
            playmobile_api=env.str("PLAYMOBILE_API"),
            payme=env.str("PAYME"),
            click=env.str("CLICK")
        )
    )
