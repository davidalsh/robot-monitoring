import {Button} from "@/components/ui/button.tsx";
import {RotateCw} from "lucide-react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import api from "@/api.tsx";
import {toast} from "sonner";
import axios from "axios";


export default function RobotReset({ disabled, robotUUID } : { disabled: boolean, robotUUID: string}) {
    const resetRobot = async () => {
        try {
            const response = await api.post(`/robots/${robotUUID}/reset`)
            if (response.status === 204)
              toast.success(`Robot ${robotUUID} has been successfully reset.`)
        } catch (e) {
            if (axios.isAxiosError(e)) {
              const message = e.response?.data?.message || "Connection problems :("
              toast.error(`Something went wrong. ${message}`)
            } else {
              toast.error("Something went wrong.")
            }
        }
    }
    return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
          <Button disabled={disabled} className="w-10 h-10" variant="secondary"><RotateCw/></Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Reset robot?</AlertDialogTitle>
          <AlertDialogDescription>
            This action cannot be undone. This will permanently reset the robot logs and status.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction onClick={resetRobot}>Continue</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
    )
}