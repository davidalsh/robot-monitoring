import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card.tsx";
import RobotList from "@/components/robot-list.tsx";
import {useState} from "react";


function App() {
  const [robotsCount, setRobotsCount] = useState<number>(0);
  return (
      <div className="flex justify-center items-center min-h-screen">
          <Card className="min-w-3/4">
            <CardHeader>
              <CardTitle>Robot monitoring</CardTitle>
              <CardDescription>There are {robotsCount} registered robots.</CardDescription>
            </CardHeader>
              <CardContent>
                  <RobotList setCount={setRobotsCount}/>
              </CardContent>
          </Card>
      </div>
  )
}

export default App
