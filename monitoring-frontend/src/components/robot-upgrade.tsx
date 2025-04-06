import {
    Dialog,
    DialogContent, DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger
} from "@/components/ui/dialog.tsx";
import {Button} from "@/components/ui/button.tsx";
import {ArrowBigUpDash} from "lucide-react";
import {z} from "zod";
import { zodResolver } from "@hookform/resolvers/zod"
import api from "@/api.tsx";
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage
} from "@/components/ui/form.tsx";
import axios from "axios";
import {toast} from "sonner";
import {useForm} from "react-hook-form";
import {Input} from "@/components/ui/input.tsx";
import {useState} from "react";

export default function RobotUpgrade({ disabled, robotUUID, fanSpeed } : { disabled: boolean, robotUUID: string, fanSpeed: number }) {
    const [open, setOpen] = useState<boolean>(false);
    const formSchema = z.object({
      fanSpeed: z.union([z.literal("auto"), z.coerce.number().gte(0, {
        message: "Fan speed must be greater than 0.",
      }).lte(100, {
        message: "Fan speed must be less than 100.",
      })]),
    })

    const form = useForm<z.infer<typeof formSchema>>({
      resolver: zodResolver(formSchema),
      defaultValues: {
        fanSpeed: "auto",
      },
    })

    const upgradeRobot = async (data: z.infer<typeof formSchema>) => {
        if (String(data.fanSpeed) === "") {
            form.setError("fanSpeed", { type: "manual", message: "Field is required."});
            return;
        }
        try {
            const response = await api.patch(`/robots/${robotUUID}`, {
                "fan_speed": data.fanSpeed,
            })
            if (response.status === 200) {
                toast.success(`Robot ${robotUUID} has been successfully upgraded.`)
                setOpen(false);
            }
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
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild>
            <Button disabled={disabled} variant="secondary" className="h-10 w-10"><ArrowBigUpDash/></Button>
          </DialogTrigger>
            <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle className="mb-1">Upgrade Robot</DialogTitle>
                    <DialogDescription></DialogDescription>
                    <Form {...form}>
                      <form onSubmit={form.handleSubmit(upgradeRobot)} className="space-y-8">
                        <FormField
                          control={form.control}
                          name="fanSpeed"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Fan speed %</FormLabel>
                              <FormControl>
                                <Input placeholder={String(fanSpeed)} {...field} />
                              </FormControl>
                              <FormDescription>Enter fan speed percentage or set it to auto</FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />
                        <Button type="submit">Submit</Button>
                      </form>
                    </Form>
                </DialogHeader>
            </DialogContent>
        </Dialog>
    )
}
