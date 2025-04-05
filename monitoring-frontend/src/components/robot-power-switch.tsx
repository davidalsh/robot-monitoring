import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"

export function RobotPowerSwitch() {
  return (
    <div className="flex justify-center items-center space-x-2">
      <Switch id="power-switch" />
      <Label htmlFor="power-switch" className="text-md">Power</Label>
    </div>
  )
}