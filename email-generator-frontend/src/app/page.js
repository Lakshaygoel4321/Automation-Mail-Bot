'use client'

import EmailGenerator from '@/components/EmailGenerator'

export default function Home() {
  return (
    <main className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 animate-fade-in">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-primary-600 to-blue-600 bg-clip-text text-transparent mb-4">
            AI Email Generator
          </h1>
          <p className="text-xl text-slate-600">
            Create professional emails in seconds with AI assistance
          </p>
        </div>

        {/* Main Component */}
        <EmailGenerator />
      </div>
    </main>
  )
}
