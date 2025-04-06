import {TRobotLog} from "@/types/robot";
import {cn} from "@/lib/utils.ts";

export default function RobotLog({ log } : { log: TRobotLog }) {
    return (
        <div className="grid grid-cols-5 gap-4 justify-between items-start">
            <span className={cn(log.type === "Error" ? "text-red-400" : "text-orange-400", "")}>{log.type}</span>
            <span className="text-center grow-2">{new Date(log.time * 1000).toLocaleTimeString("en-GB")}</span>
            <span className="text-wrap col-span-3">{log.message}</span>
        </div>
    )
}