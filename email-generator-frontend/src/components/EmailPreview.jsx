'use client'

import { DocumentTextIcon } from '@heroicons/react/24/outline'
import { motion } from 'framer-motion'

export default function EmailPreview({ content, feedbackHistory }) {
  if (!content) return null

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-2xl p-6 mb-6"
    >
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 bg-primary-100 rounded-lg">
          <DocumentTextIcon className="w-6 h-6 text-primary-600" />
        </div>
        <h3 className="text-lg font-semibold text-slate-800">Email Preview</h3>
      </div>

      <div className="bg-slate-50 rounded-xl p-6 border border-slate-200">
        <pre className="whitespace-pre-wrap font-sans text-sm text-slate-700 leading-relaxed">
          {content}
        </pre>
      </div>

      {feedbackHistory && feedbackHistory.length > 0 && (
        <div className="mt-6">
          <h4 className="text-sm font-medium text-slate-600 mb-3">
            Feedback History ({feedbackHistory.length})
          </h4>
          <div className="space-y-2">
            {feedbackHistory.map((feedback, index) => (
              <div
                key={index}
                className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-sm text-slate-700"
              >
                <span className="font-medium text-blue-700">#{index + 1}:</span> {feedback}
              </div>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  )
}
