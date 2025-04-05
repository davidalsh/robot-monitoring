import Robot from "@/components/robot.tsx";
import { TRobot } from "@/types/robot"
import {useEffect, useRef, useState} from "react";
import api from "@/api.tsx";


function RobotList() {
    const [robots, setRobots] = useState<TRobot[]>([]);
    const wsRef = useRef<WebSocket | null>(null);


    useEffect(() => {
      const getRobotStates = async () => {
          try {
              const response = await api.get<TRobot[]>("/robots/");
              if (response.status === 200)
                  setRobots(response.data)
          } catch (err) {
              console.log(err)
          }
      }

      getRobotStates();
    }, []);

    useEffect(() => {
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
        <div className="flex flex-col gap-2">
            {robots.map(robot => <Robot key={robot.uuid} robot={robot} />)}
        </div>
    )
}


export default RobotList