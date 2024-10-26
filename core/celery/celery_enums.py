import enum


class CeleryTaskQueues(enum.StrEnum):
    LOW = 'low'
    DEFAULT = 'default'
    URGENT = 'urgent'


class CeleryTasks(enum.StrEnum):
    USER_EXAMPLE = 'user.example'
