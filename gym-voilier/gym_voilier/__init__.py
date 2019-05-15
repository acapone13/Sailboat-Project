from gym.envs.registration import register

register(
    id='voilier-v0',
    entry_point='gym_voilier.envs:VoilierEnv',
)