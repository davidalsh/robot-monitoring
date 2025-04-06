import {TRobot} from "@/types/robot"
import {Card, CardContent} from "@/components/ui/card.tsx";
import {Switch} from "@/components/ui/switch.tsx";
import api from "@/api.tsx";
import {memo, useEffect, useState} from "react";
import {cn} from "@/lib/utils.ts";
import RobotLogsList from "@/components/robot-logs-list.tsx";
import RobotReset from "@/components/robot-reset.tsx";
import {Badge} from "@/components/ui/badge.tsx";
import RobotUpgrade from "@/components/robot-upgrade.tsx";


function Robot({ robot } : { robot: TRobot }) {
    const powerOn = !["Idle", "Offline"].includes(robot.status)
    const [upTime, setUpTime] = useState<string | null>(null);
    const isOffline = robot.status === "Offline"
    let statusStyles: string = ""
    if (robot.status === "Error")
        statusStyles += "text-red-400"
    else if (robot.status === "Running")
        statusStyles += "text-green-400"

    function formatTime(seconds: number): string {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const secs = Math.floor(seconds % 60);

      const pad = (num: number): string => num.toString().padStart(2, "0");

      return `${pad(hours)}:${pad(minutes)}:${pad(secs)}`;
    }

    useEffect(() => {
        const timeInterval = setInterval(() => {
            setUpTime(formatTime(Date.now() / 1000 - robot.boot_time));
        }, 200)
        return () => {clearInterval(timeInterval)}
    }, [robot.boot_time])

    let temperatureStyles: string = ""
    if (robot.temperature > 80) {
        temperatureStyles += "text-red-400"
    } else if (robot.temperature > 60) {
        temperatureStyles += "text-orange-400"
    }

    const toggleRobotPower = async () => {
        try {
            await api.post(`/robots/${robot.uuid}/power`, {
                "action": powerOn ? "off" : "on"
            });
        } catch (err) {
            console.log(err)
        }
    }
    return (
        <Card className={isOffline ? "bg-primary/10" : "relative"}>
            <CardContent className="flex flex-col gap-2 md:gap-2 md:flex-row items-center justify-between pl-2">
                <div className="flex gap-2">
                    <div className="flex flex-col text-center justify-center items-center gap-2 w-[64px]">
                        <Switch disabled={isOffline} checked={powerOn} onCheckedChange={toggleRobotPower}
                                className="h-5" id="power-switch"/>
                    </div>
                    <div className="flex flex-col gap-0">
                        <span className="text-l">{robot.name}</span>
                        <span className="text-xs text-muted-foreground">({robot.uuid})</span>
                    </div>

                </div>
                <div className="grid grid-cols-2 justify-items-center sm:flex sm:flex-row text-center items-center gap-5">
                    <span className="min-w-16"><Badge className={cn(statusStyles, "h-7")}
                                                      variant="secondary">{robot.status}</Badge></span>
                    <span className="sm:w-16">{ isOffline  ? "-" : upTime || "-" }</span>
                    <span className="w-16">{ isOffline ? "-" : robot.fan_speed + "%"}</span>
                    <span className="w-16">{ isOffline ? "N/A" : robot.power_consumption + "W"}</span>
                    <span className={cn(temperatureStyles, "w-16")}>{ isOffline ? "-" : robot.temperature + "°C"}</span>
                    <div className="flex gap-2">
                        <RobotUpgrade disabled={isOffline} robotUUID={robot.uuid} fanSpeed={robot.fan_speed}/>
                        <RobotLogsList disabled={isOffline} robotUUID={robot.uuid} robotName={robot.name} robotLogs={robot.logs}/>
                        <RobotReset disabled={isOffline} robotUUID={robot.uuid}/>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}


export default memo(Robot);
