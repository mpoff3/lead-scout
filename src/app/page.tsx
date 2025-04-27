'use client';

import { useState } from 'react';

export default function Home() {
  const [description, setDescription] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle the submission here
    console.log('Submitted description:', description);
    alert('Description submitted!');
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-[#FFE4D6] via-[#DAE0E6] to-[#FFE4D6]">
      <div className="max-w-3xl mx-auto p-6 pt-12">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-[#FF4500] mb-3 tracking-tight">
            LeadScout
          </h1>
          <p className="text-[16px] text-[#1A1A1B] flex items-center justify-center gap-2">
            <span className="text-lg">🔍</span> Let's find some relevant Reddit posts that you can reply to
          </p>
        </div>
        
        <div className="bg-white rounded-lg shadow-lg border border-[#FFE4D6] hover:border-[#FF4500]/20 transition-all duration-300">
          <form onSubmit={handleSubmit} className="p-6">
            <div className="mb-5">
              <label 
                htmlFor="description" 
                className="block text-[15px] font-medium text-[#1A1A1B] mb-3 leading-relaxed"
              >
                LeadScout will notify you of some recent posts practically begging for your product.
              </label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full h-36 p-4 border border-[#FFE4D6] rounded-lg
                          focus:border-[#FF4500] focus:ring-2 focus:ring-[#FF4500]/20
                          placeholder:text-[#878A8C] text-[#1A1A1B] text-[15px]
                          transition-all duration-300 ease-in-out
                          bg-[#FFFFFF] hover:border-[#FF4500]/30
                          shadow-inner"
                placeholder="Product description here..."
                required
              />
            </div>
            
            <button
              type="submit"
              className="w-full bg-[#FF4500] text-white py-3 px-6 rounded-lg
                        hover:bg-[#FF4500]/90 active:bg-[#FF4500]
                        font-semibold text-[16px]
                        transition-all duration-300 ease-in-out
                        focus:outline-none focus:ring-2 focus:ring-[#FF4500]/50
                        shadow-md hover:shadow-lg hover:transform hover:-translate-y-0.5"
            >
              Find Matching Reddit Posts
            </button>
          </form>
        </div>

        <div className="mt-6 text-center">
          <p className="text-[14px] text-[#666] leading-relaxed">
            Powered by LeadScout • Finding the perfect Reddit conversations for your product
          </p>
        </div>
      </div>
    </main>
  );
}
