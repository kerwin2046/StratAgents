import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { cn } from '@/lib/utils'

interface MarkdownRendererProps {
  content: string
  className?: string
}

export default function MarkdownRenderer({ content, className }: MarkdownRendererProps) {
  return (
    <div className={cn("markdown-content", className)}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Custom heading rendering with better spacing
          h1: ({ children, ...props }) => (
            <h1 className="text-2xl font-bold text-gray-900 mb-4 mt-6 border-b border-gray-200 pb-2" {...props}>
              {children}
            </h1>
          ),
          h2: ({ children, ...props }) => (
            <h2 className="text-xl font-semibold text-gray-900 mb-3 mt-5" {...props}>
              {children}
            </h2>
          ),
          h3: ({ children, ...props }) => (
            <h3 className="text-lg font-semibold text-gray-900 mb-2 mt-4" {...props}>
              {children}
            </h3>
          ),
          h4: ({ children, ...props }) => (
            <h4 className="text-base font-semibold text-gray-900 mb-2 mt-3" {...props}>
              {children}
            </h4>
          ),
          
          // Enhanced paragraph rendering
          p: ({ children, ...props }) => (
            <p className="text-gray-700 leading-7 mb-4" {...props}>
              {children}
            </p>
          ),
          
          // Enhanced list rendering
          ul: ({ children, ...props }) => (
            <ul className="list-disc list-outside ml-6 my-4 space-y-1" {...props}>
              {children}
            </ul>
          ),
          ol: ({ children, ...props }) => (
            <ol className="list-decimal list-outside ml-6 my-4 space-y-1" {...props}>
              {children}
            </ol>
          ),
          li: ({ children, ...props }) => (
            <li className="text-gray-700" {...props}>
              {children}
            </li>
          ),
          
          // Enhanced code rendering
          code: ({ children, className, ...props }) => {
            const isInline = !className
            if (isInline) {
              return (
                <code 
                  className="bg-gray-100 text-gray-800 px-1.5 py-0.5 rounded text-sm font-mono" 
                  {...props}
                >
                  {children}
                </code>
              )
            }
            return (
              <code className={className} {...props}>
                {children}
              </code>
            )
          },
          
          pre: ({ children, ...props }) => (
            <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto my-4" {...props}>
              {children}
            </pre>
          ),
          
          // Enhanced blockquote rendering
          blockquote: ({ children, ...props }) => (
            <blockquote className="border-l-4 border-blue-300 pl-4 py-2 my-4 italic text-gray-600 bg-blue-50" {...props}>
              {children}
            </blockquote>
          ),
          
          // Enhanced table rendering
          table: ({ children, ...props }) => (
            <div className="overflow-x-auto my-4">
              <table className="min-w-full border-collapse border border-gray-300" {...props}>
                {children}
              </table>
            </div>
          ),
          th: ({ children, ...props }) => (
            <th className="border border-gray-300 bg-gray-50 px-4 py-2 text-left font-semibold text-gray-900" {...props}>
              {children}
            </th>
          ),
          td: ({ children, ...props }) => (
            <td className="border border-gray-300 px-4 py-2 text-gray-700" {...props}>
              {children}
            </td>
          ),
          
          // Enhanced link rendering
          a: ({ children, href, ...props }) => (
            <a 
              href={href}
              className="text-blue-600 underline hover:text-blue-800 transition-colors"
              target={href?.startsWith('http') ? '_blank' : undefined}
              rel={href?.startsWith('http') ? 'noopener noreferrer' : undefined}
              {...props}
            >
              {children}
            </a>
          ),
          
          // Enhanced strong/bold rendering
          strong: ({ children, ...props }) => (
            <strong className="font-semibold text-gray-900" {...props}>
              {children}
            </strong>
          ),
          
          // Enhanced emphasis/italic rendering
          em: ({ children, ...props }) => (
            <em className="italic text-gray-800" {...props}>
              {children}
            </em>
          ),
          
          // HR rendering
          hr: ({ ...props }) => (
            <hr className="border-0 border-t border-gray-200 my-8" {...props} />
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}