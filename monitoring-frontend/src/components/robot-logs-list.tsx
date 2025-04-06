import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import {Logs} from "lucide-react";
import {Button} from "@/components/ui/button.tsx";
import {TRobotLog} from "@/types/robot";
import RobotLog from "@/components/robot-log.tsx";
import {Separator} from "@/components/ui/separator.tsx";

function RobotLogsList({ disabled, robotUUID, robotName, robotLogs } : { disabled: boolean, robotUUID: string, robotName: string, robotLogs: TRobotLog[]}) {
    return (
    <Dialog>
      <DialogTrigger asChild>
        <Button disabled={disabled} variant="secondary" className="h-10"><Logs/></Button>
      </DialogTrigger>
        <DialogContent className="sm:max-w-[500px]">
            <DialogHeader>
                <DialogTitle>{robotName}</DialogTitle>
                <DialogDescription>
                    {robotUUID}
                </DialogDescription>
            </DialogHeader>
            <div className="flex flex-col gap-2">
                <h3>Logs</h3>
                <Separator/>
                {
                    robotLogs.length > 0 ?
                    robotLogs.map(log => <RobotLog key={log.time} log={log}/>)
                     : <div className="flex justify-center items-center text-sm py-6">Nothing here!</div>
                }
            </div>
        </DialogContent>
    </Dialog>
    )
}

export default RobotLogsList;