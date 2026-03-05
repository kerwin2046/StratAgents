import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Search, Github, Zap } from 'lucide-react'

export default function Header() {
  return (
    <header className="w-full border-b bg-white/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        
        {/* Left Side: Bright Data Logo + Main Logo/Title */}
        <div className="flex items-center space-x-4">
          {/* Bright Data Logo Placeholder */}
          <div className="flex items-center">

          </div>
          
          {/* Original Logo and Title */}
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-black rounded-lg">
              <Search className="h-5 w-5 text-white" />
            </div>
            <div className="flex items-center space-x-2">
              <h1 className="text-xl font-bold text-gray-900">CI Agent</h1>
              <Badge variant="secondary" className="text-xs">
                Multi-Agent
              </Badge>
            </div>
          </div>
        </div>
         <div className="flex items-center">
            <img src="https://strandsagents.com/latest/assets/logo-github.svg" alt="Strands agents" className="w-7 h-20" />
          </div>
        {/* Navigation */}
        <div className="hidden md:flex items-center space-x-6 text-sm text-gray-600">
          <div className="flex items-center space-x-1">
            <Zap className="h-4 w-4" />
          </div>
        </div>
                  
          {/* Strands Logo Placeholder */}
          <div className="flex items-center">
            <img src="https://comeet-euw-app.s3.amazonaws.com/2183/a32c8b7a5296f51e0e05b7ddccbbfb20cdb8028b" alt="Bright Data" className="w-40 h-20" />
          </div>
        {/* Right Side: Actions + Strands Logo */}
        <div className="flex items-center space-x-4">
          {/* Original Actions */}
          <div className="flex items-center space-x-3">
            <Button variant="outline" size="sm" className="hidden md:flex">
              <Github className="h-4 w-4 mr-2" />
              GitHub
            </Button>
          </div>
        </div>
        
      </div>
    </header>
  )
}