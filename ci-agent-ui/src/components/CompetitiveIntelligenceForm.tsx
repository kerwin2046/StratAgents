import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Separator } from '@/components/ui/separator'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { 
  Form, 
  FormControl, 
  FormDescription, 
  FormField, 
  FormItem, 
  FormLabel, 
  FormMessage 
} from '@/components/ui/form'
import { 
  Search, 
  Globe, 
  Building, 
  Zap, 
  CheckCircle, 
  AlertCircle,
  Activity,
  Brain,
  FileText,
  Loader2
} from 'lucide-react'
import DemoScenarios from './DemoScenarios'
import Header from './Header'
import MarkdownRenderer from './MarkdownRenderer'

// Form validation schema
const formSchema = z.object({
  companyName: z.string().min(1, "Company name is required").max(100, "Company name too long"),
  companyUrl: z.string().url("Please enter a valid URL").optional().or(z.literal("")),
})

type FormValues = z.infer<typeof formSchema>

interface StreamEvent {
  timestamp: string
  type: string
  step?: string
  message?: string
  tool_name?: string
  tool_input?: any
  data?: any
}

interface AnalysisResult {
  competitor: string
  website?: string
  research_findings: string
  strategic_analysis: string
  final_report: string
  timestamp: string
  status: string
  workflow: string
}

// Use env in production; default to local API for dev (avoid "Failed to fetch" when backend runs on localhost)
const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export default function CompetitiveIntelligenceForm() {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [currentStep, setCurrentStep] = useState('')
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      companyName: '',
      companyUrl: '',
    },
  })

  const analyzeCompetitor = async (values: FormValues) => {
    setIsAnalyzing(true)
    setProgress(0)
    setCurrentStep('Starting analysis...')
    setAnalysisResult(null)
    setError(null)

    try {
      const response = await fetch(`${API_BASE_URL}/analyze/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify({
          competitor_name: values.companyName,
          competitor_website: values.companyUrl || undefined,
          stream: true,
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (!reader) {
        throw new Error('Failed to get response reader')
      }

      while (true) {
        const { done, value } = await reader.read()
        
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const eventData: StreamEvent = JSON.parse(line.slice(6))

              // Update progress and current step based on event type
              if (eventData.type === 'status_update') {
                setCurrentStep(eventData.message || '')
                
                if (eventData.step === 'research_start') {
                  setProgress(10)
                } else if (eventData.step === 'research_complete') {
                  setProgress(40)
                } else if (eventData.step === 'analysis_start') {
                  setProgress(50)
                } else if (eventData.step === 'analysis_complete') {
                  setProgress(80)
                } else if (eventData.step === 'report_start') {
                  setProgress(85)
                } else if (eventData.step === 'complete') {
                  setProgress(100)
                }
              } else if (eventData.type === 'complete') {
                setAnalysisResult(eventData.data as AnalysisResult)
                setCurrentStep('Analysis complete!')
                setProgress(100)
              } else if (eventData.type === 'error') {
                throw new Error(eventData.message || 'Analysis failed')
              }
            } catch (parseError) {
              console.warn('Failed to parse event:', parseError)
            }
          }
        }
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred'
      setError(errorMessage)
      setCurrentStep('Analysis failed')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const onSubmit = (values: FormValues) => {
    analyzeCompetitor(values)
  }

  const handleDemoScenario = (name: string, website: string) => {
    form.setValue('companyName', name)
    form.setValue('companyUrl', website)
  }

  const resetForm = () => {
    form.reset()
    setAnalysisResult(null)
    setError(null)
    setProgress(0)
    setCurrentStep('')
  }

  const getStepIcon = (step: string) => {
    if (step.includes('Researcher')) return <Brain className="h-4 w-4" />
    if (step.includes('Analyst')) return <Activity className="h-4 w-4" />
    if (step.includes('Writer')) return <FileText className="h-4 w-4" />
    return <Zap className="h-4 w-4" />
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Header />
      <div className="max-w-4xl mx-auto space-y-8 p-4 pt-8">
        {/* Hero Section */}
        <div className="text-center space-y-6">
          <h1 className="text-4xl md:text-xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
            Competitive Intelligence
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Get comprehensive competitive analysis powered by AI agents. Enter a company name and optional website to start your analysis.
          </p>
          <div className="flex items-center justify-center space-x-8 text-sm text-gray-500">
            <div className="flex items-center space-x-2">
              <Brain className="h-5 w-5 text-blue-600" />
              <span>Researcher Agent</span>
            </div>
            <div className="flex items-center space-x-2">
              <Activity className="h-5 w-5 text-purple-600" />
              <span>Analyst Agent</span>
            </div>
            <div className="flex items-center space-x-2">
              <FileText className="h-5 w-5 text-green-600" />
              <span>Writer Agent</span>
            </div>
          </div>
        </div>

        {/* Main Form Card */}
        <Card className="border-0 shadow-xl bg-white">
          <CardHeader className="text-center">
            <CardTitle className="text-xl">Start Analysis</CardTitle>
            <CardDescription>
              Our multi-agent system will research, analyze, and generate a comprehensive competitive intelligence report
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <FormField
                    control={form.control}
                    name="companyName"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="flex items-center space-x-2">
                          <Building className="h-4 w-4" />
                          <span>Company Name</span>
                        </FormLabel>
                        <FormControl>
                          <Input 
                            placeholder="e.g., Slack, Notion, Figma" 
                            className="h-12"
                            {...field} 
                          />
                        </FormControl>
                        <FormDescription>
                          The name of the competitor you want to analyze
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="companyUrl"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="flex items-center space-x-2">
                          <Globe className="h-4 w-4" />
                          <span>Company URL</span>
                          <Badge variant="secondary" className="text-xs">Optional</Badge>
                        </FormLabel>
                        <FormControl>
                          <Input 
                            placeholder="https://company.com" 
                            className="h-12"
                            {...field} 
                          />
                        </FormControl>
                        <FormDescription>
                          Company website for more targeted analysis
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <Button 
                  type="submit" 
                  className="w-full h-12 text-base font-medium bg-black hover:bg-gray-800"
                  disabled={isAnalyzing}
                >
                  {isAnalyzing ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Search className="mr-2 h-4 w-4" />
                      Start Analysis
                    </>
                  )}
                </Button>
              </form>
            </Form>
          </CardContent>
        </Card>

        {/* Demo Scenarios */}
        {!isAnalyzing && !analysisResult && (
          <DemoScenarios onSelectScenario={handleDemoScenario} />
        )}

        {/* Progress and Status */}
        {isAnalyzing && (
          <Card className="border-0 shadow-lg">
            <CardContent className="pt-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    {getStepIcon(currentStep)}
                    <span className="font-medium">{currentStep}</span>
                  </div>
                  <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                    {progress}%
                  </Badge>
                </div>
                <Progress value={progress} className="h-2" />
              </div>
            </CardContent>
          </Card>
        )}

        {/* Error Display */}
        {error && (
          <Alert className="border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-800">
              {error}
            </AlertDescription>
          </Alert>
        )}

        {/* Results */}
        {analysisResult && (
          <Card className="border-0 shadow-xl">
            <CardHeader>
              <CardTitle className="text-xl flex items-center space-x-2">
                <CheckCircle className="h-6 w-6 text-green-600" />
                <span>Analysis Complete</span>
              </CardTitle>
              <CardDescription>
                Competitive intelligence report for {analysisResult.competitor}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <Brain className="h-8 w-8 mx-auto mb-2 text-blue-600" />
                  <div className="font-medium">Research</div>
                  <div className="text-sm text-gray-600">Data Collection</div>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <Activity className="h-8 w-8 mx-auto mb-2 text-purple-600" />
                  <div className="font-medium">Analysis</div>
                  <div className="text-sm text-gray-600">Strategic Insights</div>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <FileText className="h-8 w-8 mx-auto mb-2 text-green-600" />
                  <div className="font-medium">Report</div>
                  <div className="text-sm text-gray-600">Executive Summary</div>
                </div>
              </div>

              <Separator />

              <div className="space-y-4">
                <div>
                  <h3 className="font-semibold text-lg mb-2">Executive Report</h3>
                  <div className="bg-gray-50 p-6 rounded-lg">
                    <MarkdownRenderer content={analysisResult.final_report} />
                  </div>
                </div>

                <details className="group">
                  <summary className="cursor-pointer font-medium text-gray-700 hover:text-gray-900 flex items-center">
                    <Brain className="h-4 w-4 mr-2 text-blue-600" />
                    View Research Findings
                  </summary>
                  <div className="mt-2 bg-blue-50 p-6 rounded-lg">
                    <MarkdownRenderer content={analysisResult.research_findings} />
                  </div>
                </details>

                <details className="group">
                  <summary className="cursor-pointer font-medium text-gray-700 hover:text-gray-900 flex items-center">
                    <Activity className="h-4 w-4 mr-2 text-purple-600" />
                    View Strategic Analysis
                  </summary>
                  <div className="mt-2 bg-purple-50 p-6 rounded-lg">
                    <MarkdownRenderer content={analysisResult.strategic_analysis} />
                  </div>
                </details>
              </div>

              <div className="flex items-center justify-between text-sm text-gray-500 pt-4 border-t">
                <span>Generated on {new Date(analysisResult.timestamp).toLocaleDateString()}</span>
                <div className="flex items-center space-x-2">
                  <Button variant="outline" size="sm" onClick={resetForm}>
                    New Analysis
                  </Button>
                  <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                    {analysisResult.status}
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}