from gym.envs.registration import register

register(
    id='voilier-v1',
    entry_point='gym_voilier.envs:VoilierEnv',
)