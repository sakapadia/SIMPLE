from gym.envs.registration import register

register(
    id='Kanban-v0',
    entry_point='kanban.envs:KanbanEnv',
)

