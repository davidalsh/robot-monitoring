import {TRobot} from "@/types/robot"
import {Card, CardContent} from "@/components/ui/card.tsx";
import {Switch} from "@/components/ui/switch.tsx";
import api from "@/api.tsx";
import {memo} from "react";


function Robot({ robot } : { robot: TRobot }) {
    const powerOn = !["Idle", "Offline"].includes(robot.status)

    let temperatureStyles: string = ""
    if (70 <= robot.temperature && robot.temperature <= 80) {
        temperatureStyles += "text-orange-400"
    } else if (robot.temperature > 80) {
        temperatureStyles += "text-red-400"
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
        <Card>
            <CardContent className="flex items-center justify-between">
                <div className="flex gap-5 items-center">
                    <Switch checked={powerOn} onCheckedChange={toggleRobotPower} className="h-5" id="power-switch"/>
                    <span>{robot.status}</span>
                </div>
                <div className="flex items-center gap-3">
                    <span>{robot.fan_speed}%</span>
                    <span>{robot.power_consumption}W</span>
                    <span className={temperatureStyles}>{robot.temperature}°C</span>
                </div>
            </CardContent>
        </Card>
    )
}


export default memo(Robot);