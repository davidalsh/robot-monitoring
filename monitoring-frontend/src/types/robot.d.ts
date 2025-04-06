enum RobotStatus {
    Idle = "Idle",
    Running = "Running",
    Error = "Error",
    Offline = "Offline"
}

type TRobotLog = {
  type: string;
  message: string;
  time: number;
};

type TRobot = {
    uuid: string;
    name: string;
    temperature: number;
    power_consumption: number;
    status: RobotStatus;
    fan_speed: number;
    boot_time: number;
    logs: TRobotLog[];
};

export type { RobotStatus, TRobot, TRobotLog}
