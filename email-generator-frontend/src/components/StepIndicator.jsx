'use client'

import { CheckIcon } from '@heroicons/react/24/solid'
import { motion } from 'framer-motion'

const steps = [
  { id: 1, name: 'Generate', description: 'Create initial draft' },
  { id: 2, name: 'Refine', description: 'Add feedback' },
  { id: 3, name: 'Finalize', description: 'Review final version' },
  { id: 4, name: 'Send', description: 'Deliver email' },
]

export default function StepIndicator({ currentStep }) {
  return (
    <div className="w-full pt-8 pb-20 max-w-5xl mx-auto pl-4 sm:pl-6 md:pl-8">
      <div className="flex items-center justify-center gap-8 sm:gap-12">
        {steps.map((step, index) => (
          <div key={step.id} className="flex items-center flex-1">
            {/* Step Circle */}
            <div className="relative flex flex-col items-center">
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: index * 0.1 }}
                className="relative"
              >
                {currentStep > step.id ? (
                  <div className="w-12 h-12 rounded-full bg-gradient-to-r from-primary-600 to-primary-500 flex items-center justify-center shadow-lg">
                    <CheckIcon className="w-6 h-6 text-white" />
                  </div>
                ) : currentStep === step.id ? (
                  <div className="w-12 h-12 rounded-full bg-gradient-to-r from-primary-600 to-primary-500 flex items-center justify-center shadow-lg animate-pulse">
                    <span className="text-white font-bold">{step.id}</span>
                  </div>
                ) : (
                  <div className="w-12 h-12 rounded-full bg-slate-200 flex items-center justify-center">
                    <span className="text-slate-500 font-medium">{step.id}</span>
                  </div>
                )}
              </motion.div>
              
              {/* Step Label */}
              <div className="absolute top-14 text-center w-24">
                <p className={`text-sm font-medium ${
                  currentStep >= step.id ? 'text-primary-600' : 'text-slate-500'
                }`}>
                  {step.name}
                </p>
                <p className="text-xs text-slate-400 mt-1">
                  {step.description}
                </p>
              </div>
            </div>

            {/* Connector Line */}
            {index < steps.length - 1 && (
              <div className="flex-1 h-1 mx-4 mt-0 mb-16">
                <div className={`h-full rounded-full transition-all duration-500 ${
                  currentStep > step.id 
                    ? 'bg-gradient-to-r from-primary-600 to-primary-500' 
                    : 'bg-slate-200'
                }`} />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
