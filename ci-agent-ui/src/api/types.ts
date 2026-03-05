/** Server-sent event payload during streaming analysis */
export interface StreamEvent {
  timestamp: string
  type: string
  step?: string
  message?: string
  tool_name?: string
  tool_input?: unknown
  data?: unknown
}

/** Final analysis result from the API */
export interface AnalysisResult {
  competitor: string
  website?: string
  research_findings: string
  strategic_analysis: string
  final_report: string
  timestamp: string
  status: string
  workflow: string
}
