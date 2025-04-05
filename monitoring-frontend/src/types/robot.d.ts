enum RobotStatus {
    Idle = "Idle",
    Running = "Running",
    Error = "Error",
    Offline = "Offline"
}

type TRobot = {
    uuid: string;
    temperature: number;
    power_consumption: number;
    status: RobotStatus;
    fan_speed: number;
};

export type { RobotStatus, TRobot }
