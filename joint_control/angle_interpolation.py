'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''


from pid import PIDAgent
from keyframes import hello


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}


        # YOUR CODE HERE

        if (self.start_time == -1):
            self.start_time = perception.time
        current_time = perception.time - self.start_time

        (names, times, keys) = keyframes

        for joint in range(len(names)):
            if(names[joint] not in self.joint_names):
                continue
            else:
                for time in range(len(times[joint])):
                    if(time == 0 and current_time < times[joint][time]):
                        P0 = perception.joint[names[joint]]
                        P3 = keys[joint][time][0]
                        P1 = P0 + keys[joint][time][2][2]
                        P2 = P3 + keys[joint][time + 1][1][2]
                        t0 = 0.0
                        t3 = times[joint][time]
                    elif(time < (len(times[joint]) - 1) and current_time >= times[joint][time] and current_time < times[joint][time + 1]):
                        P0 = keys[joint][time][0]
                        P3 = keys[joint][time + 1][0]
                        P1 = P0 + keys[joint][time][2][2]
                        P2 = P3 + keys[joint][time + 1][1][2]
                        t0 = times[joint][time]
                        t3 = times[joint][time + 1]
                    else:
                        continue
                    i = (current_time - t0)/(t3 - t0)
                    target_joints[names[joint]] = ((1 - i)**3)*P0 + 3*((1 - i)**2)*i*P1 + 3*(1 - i)*(i**2)*P2 + (i**3)*P3

        return target_joints

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
