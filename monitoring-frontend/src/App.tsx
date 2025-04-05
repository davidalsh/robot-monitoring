import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card.tsx";
import RobotList from "@/components/robot-list.tsx";


function App() {
  return (
      <div className="flex justify-center items-center min-h-screen">
          <Card className="min-w-3/4">
            <CardHeader>
              <CardTitle>Robot monitoring</CardTitle>
              <CardDescription>There are 0 connected robots.</CardDescription>
            </CardHeader>
              <CardContent>
                  <RobotList/>
              </CardContent>
          </Card>
      </div>
  )
}

export default App
