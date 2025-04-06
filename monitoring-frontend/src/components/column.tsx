import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import React from "react";
import {cn} from "@/lib/utils.ts";


type Props = {
    children: React.ReactNode,
    description: string,
    className?: string,
}

export default function Column({ children, description, className }: Props) {
    return (
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <span className={cn("w-16 flex items-center justify-center", className)}>{ children }</span>
            </TooltipTrigger>
            <TooltipContent>
              <p>{ description }</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
    )
}