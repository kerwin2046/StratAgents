/**
 * API client for Competitive Intelligence backend.
 * Centralizes base URL and request logic for reuse and testing.
 */
import type { AnalysisResult, StreamEvent } from './types'

export { type AnalysisResult, type StreamEvent } from './types'

const defaultBase = 'http://localhost:8000'

export function getApiBaseUrl(): string {
  return import.meta.env.VITE_API_URL ?? defaultBase
}

export interface AnalyzeStreamCallbacks {
  onProgress?: (percent: number) => void
  onStep?: (message: string) => void
  onResult?: (result: AnalysisResult) => void
  onError?: (message: string) => void
}

/**
 * Run competitive analysis with streaming; callbacks receive progress and final result.
 * Throws on HTTP errors or when the server sends an error event.
 */
export async function analyzeStream(
  params: { competitor_name: string; competitor_website?: string },
  callbacks: AnalyzeStreamCallbacks = {}
): Promise<void> {
  const base = getApiBaseUrl()
  const { onProgress = () => {}, onStep = () => {}, onResult = () => {}, onError = () => {} } = callbacks

  const response = await fetch(`${base}/analyze/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'text/event-stream',
    },
    body: JSON.stringify({
      competitor_name: params.competitor_name,
      competitor_website: params.competitor_website ?? undefined,
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

  let buffer = ''
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() ?? ''

    for (const line of lines) {
      if (!line.startsWith('data: ')) continue
      try {
        const eventData: StreamEvent = JSON.parse(line.slice(6))

        if (eventData.type === 'status_update') {
          onStep(eventData.message ?? '')
          const step = eventData.step
          if (step === 'research_start') onProgress(10)
          else if (step === 'research_complete') onProgress(40)
          else if (step === 'analysis_start') onProgress(50)
          else if (step === 'analysis_complete') onProgress(80)
          else if (step === 'report_start') onProgress(85)
          else if (step === 'complete') onProgress(100)
        } else if (eventData.type === 'complete' && eventData.data) {
          onResult(eventData.data as AnalysisResult)
          onProgress(100)
        } else if (eventData.type === 'error') {
          const msg = (eventData as { message?: string }).message ?? 'Analysis failed'
          onError(msg)
          throw new Error(msg)
        }
      } catch (e) {
        if (e instanceof SyntaxError) continue
        throw e
      }
    }
  }
}
