from gym.envs.registration import register

register(
    id='gymSim-v0',
    entry_point='gym_simulator.envs:SailboatSimulatorEnv',
)