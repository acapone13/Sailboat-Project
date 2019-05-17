from gym.envs.registration import register

register(
    id='voilier-v2',
    entry_point='gym_voilier.envs:VoilierEnv',
)