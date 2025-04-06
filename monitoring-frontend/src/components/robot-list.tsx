import Robot from "@/components/robot.tsx";
import { TRobot } from "@/types/robot"
import React from "react";
import api from "@/api.tsx";
import {CardContent} from "@/components/ui/card.tsx";
import {Clock, Fan, Info, Thermometer, Zap} from "lucide-react";
import Column from "@/components/column.tsx";


function RobotList({ setCount }: { setCount: React.Dispatch<React.SetStateAction<number>> }) {
    const [robots, setRobots] = React.useState<TRobot[]>([]);
    const wsRef = React.useRef<WebSocket | null>(null);


    React.useEffect(() => {
      const getRobotStates = async () => {
          try {
              const response = await api.get<TRobot[]>("/robots/");
              if (response.status === 200)
                  setRobots(response.data);
                  setCount(response.data?.length);
          } catch (err) {
              console.log(err)
          }
      }

      getRobotStates();
    }, []);

    React.useEffect(() => {
      wsRef.current = new WebSocket("ws://127.0.0.1:8000/api/v1/ws/robots/state");

      wsRef.current.onmessage = (event: MessageEvent) => {
        try {
          const updatedRobot: TRobot = JSON.parse(event.data);

          setRobots(prevRobots =>
            prevRobots.map(robot =>
              robot.uuid === updatedRobot.uuid
                ? updatedRobot
                : robot
            )
          );
        } catch (error) {
          console.error("Error parsing WebSocket data:", error);
        }
      };

      return () => {
        if (wsRef.current) {
          wsRef.current.close();
        }
      };
    }, []);

    return (
        <div className="flex flex-col gap-2 ">
            <CardContent className="flex flex-col relative gap-2 md:gap-0 md:flex-row items-center justify-end pl-2">
                <div className="hidden md:flex absolute bottom-2 text-center items-center gap-5 text-primary/30">
                    <Column description="Status"><Info/></Column>
                    <Column description="Uptime"><Clock/></Column>
                    <Column description="Fan speed percentage"><Fan/></Column>
                    <Column description="Power consumption"><Zap/></Column>
                    <Column description="Temperature in Celsius"><Thermometer/></Column>
                    <div className="flex gap-2">
                        <div className="w-10"></div>
                        <div className="w-10"></div>
                        <div className="w-10"></div>
                    </div>
                </div>
            </CardContent>
            {robots.map(robot => <Robot key={robot.uuid} robot={robot} />)}
        </div>
    )
}


export default RobotList
