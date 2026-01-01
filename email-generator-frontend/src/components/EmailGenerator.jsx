'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import { 
  SparklesIcon, 
  ArrowPathIcon,
  CheckCircleIcon,
  PaperAirplaneIcon,
} from '@heroicons/react/24/outline'
import { emailApi } from '@/services/api'
import StepIndicator from './StepIndicator'
import EmailPreview from './EmailPreview'
import SendEmailModal from './SendEmailModal'

export default function EmailGenerator() {
  const [currentStep, setCurrentStep] = useState(1)
  const [topic, setTopic] = useState('')
  const [feedback, setFeedback] = useState('')
  const [sessionId, setSessionId] = useState(null)
  const [generatedContent, setGeneratedContent] = useState('')
  const [feedbackHistory, setFeedbackHistory] = useState([])
  const [finalContent, setFinalContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [showSendModal, setShowSendModal] = useState(false)
  const [backendStatus, setBackendStatus] = useState('checking')

  // Check backend health on mount
  useEffect(() => {
    checkBackendHealth()
  }, [])

  const checkBackendHealth = async () => {
    try {
      await emailApi.healthCheck()
      setBackendStatus('online')
      toast.success('Connected to backend successfully')
    } catch (error) {
      setBackendStatus('offline')
      toast.error('Cannot connect to backend. Please ensure Flask server is running on port 5000.')
    }
  }

  // Step 1: Generate initial draft
  const handleGenerate = async (e) => {
    e.preventDefault()
    
    if (!topic.trim()) {
      toast.error('Please enter an email topic')
      return
    }

    if (topic.length < 3) {
      toast.error('Topic must be at least 3 characters')
      return
    }

    setLoading(true)
    try {
      const response = await emailApi.generateDraft(topic)
      
      if (response.success) {
        setSessionId(response.session_id)
        setGeneratedContent(response.content)
        setCurrentStep(2)
        toast.success('Email draft generated successfully!')
      }
    } catch (error) {
      toast.error(error.message)
    } finally {
      setLoading(false)
    }
  }

  // Step 2: Process feedback and regenerate
  const handleFeedback = async (e) => {
    e.preventDefault()

    if (!feedback.trim()) {
      // If no feedback, just move to finalize
      handleFinalize()
      return
    }

    setLoading(true)
    try {
      const response = await emailApi.processFeedback(sessionId, feedback)
      
      if (response.success) {
        setGeneratedContent(response.content)
        setFeedbackHistory(response.feedback_history || [])
        setFeedback('')
        toast.success('Email updated with your feedback!')
      }
    } catch (error) {
      toast.error(error.message)
    } finally {
      setLoading(false)
    }
  }

  // Step 3: Finalize email
  const handleFinalize = async () => {
    setLoading(true)
    try {
      const response = await emailApi.finalizeDraft(sessionId)
      
      if (response.success) {
        setFinalContent(response.final_content)
        setCurrentStep(3)
        toast.success('Email finalized successfully!')
      }
    } catch (error) {
      toast.error(error.message)
    } finally {
      setLoading(false)
    }
  }

  // Step 4: Send email
  const handleSendEmail = async (recipientEmail) => {
    setLoading(true)
    try {
      const response = await emailApi.sendEmail(sessionId, recipientEmail)
      
      if (response.success) {
        setCurrentStep(4)
        setShowSendModal(false)
        toast.success(response.message || 'Email sent successfully!')
      }
    } catch (error) {
      toast.error(error.message)
    } finally {
      setLoading(false)
    }
  }

  // Reset to start over
  const handleReset = () => {
    setCurrentStep(1)
    setTopic('')
    setFeedback('')
    setSessionId(null)
    setGeneratedContent('')
    setFeedbackHistory([])
    setFinalContent('')
    toast.success('Ready to create a new email!')
  }

  return (
    <div className="animate-slide-up">
      {/* Backend Status Indicator */}
      <div className="mb-6 flex items-center justify-center gap-2">
        <div className={`w-3 h-3 rounded-full ${
          backendStatus === 'online' ? 'bg-green-500 animate-pulse' : 
          backendStatus === 'offline' ? 'bg-red-500' : 
          'bg-yellow-500 animate-pulse'
        }`} />
        <span className="text-sm text-slate-600">
          {backendStatus === 'online' ? 'Backend Connected' : 
           backendStatus === 'offline' ? 'Backend Offline' : 
           'Connecting...'}
        </span>
      </div>

      {/* Step Indicator */}
      <StepIndicator currentStep={currentStep} />

      {/* Main Card */}
      <motion.div
        layout
        className="glass-card rounded-2xl p-8 shadow-2xl"
      >
        {/* Step 1: Topic Input */}
        {currentStep === 1 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 bg-gradient-to-br from-primary-500 to-blue-500 rounded-xl">
                <SparklesIcon className="w-7 h-7 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-slate-800">Generate Email</h2>
                <p className="text-slate-600">What email would you like to create?</p>
              </div>
            </div>

            <form onSubmit={handleGenerate} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Email Topic / Purpose
                </label>
                <textarea
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="E.g., Meeting invitation for project kickoff, Follow-up on client proposal, Thank you email for interview..."
                  rows={4}
                  className="input-field resize-none"
                  disabled={loading}
                />
                <p className="mt-2 text-sm text-slate-500">
                  Describe what you want the email to be about
                </p>
              </div>

              <button
                type="submit"
                className="btn-primary w-full flex items-center justify-center gap-2 text-lg"
                disabled={loading || backendStatus !== 'online'}
              >
                {loading ? (
                  <>
                    <div className="w-6 h-6 border-3 border-white border-t-transparent rounded-full animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <SparklesIcon className="w-6 h-6" />
                    Generate Email
                  </>
                )}
              </button>
            </form>
          </motion.div>
        )}

        {/* Step 2: Refine with Feedback */}
        {currentStep === 2 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-xl">
                <ArrowPathIcon className="w-7 h-7 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-slate-800">Refine Email</h2>
                <p className="text-slate-600">Review and provide feedback to improve</p>
              </div>
            </div>

            <EmailPreview 
              content={generatedContent} 
              feedbackHistory={feedbackHistory}
            />

            <form onSubmit={handleFeedback} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Feedback (Optional)
                </label>
                <textarea
                  value={feedback}
                  onChange={(e) => setFeedback(e.target.value)}
                  placeholder="E.g., Make it more formal, Add urgency, Keep it shorter, Make it more friendly..."
                  rows={3}
                  className="input-field resize-none"
                  disabled={loading}
                />
                <p className="mt-2 text-sm text-slate-500">
                  Leave blank to proceed with current version
                </p>
              </div>

              <div className="flex gap-4">
                <button
                  type="button"
                  onClick={handleReset}
                  className="btn-secondary flex-1"
                  disabled={loading}
                >
                  Start Over
                </button>
                
                {feedback.trim() ? (
                  <button
                    type="submit"
                    className="btn-primary flex-1 flex items-center justify-center gap-2"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                        Updating...
                      </>
                    ) : (
                      <>
                        <ArrowPathIcon className="w-5 h-5" />
                        Apply Feedback
                      </>
                    )}
                  </button>
                ) : (
                  <button
                    type="button"
                    onClick={handleFinalize}
                    className="btn-primary flex-1 flex items-center justify-center gap-2"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                        Finalizing...
                      </>
                    ) : (
                      <>
                        <CheckCircleIcon className="w-5 h-5" />
                        Finalize Email
                      </>
                    )}
                  </button>
                )}
              </div>
            </form>
          </motion.div>
        )}

        {/* Step 3: Finalized - Ready to Send */}
        {currentStep === 3 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl">
                <CheckCircleIcon className="w-7 h-7 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-slate-800">Email Ready!</h2>
                <p className="text-slate-600">Your email is finalized and ready to send</p>
              </div>
            </div>

            <EmailPreview content={finalContent} />

            <div className="flex gap-4">
              <button
                onClick={handleReset}
                className="btn-secondary flex-1"
              >
                Create New Email
              </button>
              <button
                onClick={() => setShowSendModal(true)}
                className="btn-primary flex-1 flex items-center justify-center gap-2"
              >
                <PaperAirplaneIcon className="w-5 h-5" />
                Send Email
              </button>
            </div>
          </motion.div>
        )}

        {/* Step 4: Email Sent - Success */}
        {currentStep === 4 && (
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="text-center py-12"
          >
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full mb-6 shadow-lg">
              <CheckCircleIcon className="w-12 h-12 text-white" />
            </div>
            
            <h2 className="text-3xl font-bold text-slate-800 mb-3">
              Email Sent Successfully! 🎉
            </h2>
            <p className="text-slate-600 mb-8 text-lg">
              Your email has been delivered
            </p>

            <button
              onClick={handleReset}
              className="btn-primary inline-flex items-center gap-2"
            >
              <SparklesIcon className="w-5 h-5" />
              Create Another Email
            </button>
          </motion.div>
        )}
      </motion.div>

      {/* Send Email Modal */}
      <SendEmailModal
        isOpen={showSendModal}
        onClose={() => setShowSendModal(false)}
        onSend={handleSendEmail}
        loading={loading}
      />
    </div>
  )
}
