import { useState } from 'react';
import Head from 'next/head';
import AgentCard from '../components/AgentCard';
import ResultDisplay from '../components/ResultDisplay';
import LoadingSpinner from '../components/LoadingSpinner';

export default function Home() {
  const [activeAgent, setActiveAgent] = useState(null);
  const [inputData, setInputData] = useState('');
  const [inputType, setInputType] = useState('voice');
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const agents = [
    {
      id: 'vision',
      name: 'Vision Agent',
      description: 'Converts your ideas into structured UI layouts',
      icon: '👁️',
      color: 'bg-blue-500'
    },
    {
      id: 'code',
      name: 'Code Agent',
      description: 'Generates production-ready code from layouts',
      icon: '⚙️',
      color: 'bg-green-500'
    },
    {
      id: 'evaluator',
      name: 'Evaluator Agent',
      description: 'Reviews and validates generated code',
      icon: '🧪',
      color: 'bg-purple-500'
    }
  ];

  const handleAgentCall = async (agentId) => {
    if (!inputData.trim()) {
      setError('Please enter some input data');
      return;
    }

    setLoading(true);
    setError('');
    setActiveAgent(agentId);

    try {
      const response = await fetch(`http://localhost:8000/api/${agentId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(
          agentId === 'vision' 
            ? { input_type: inputType, input_data: inputData }
            : agentId === 'code'
            ? { layout: inputData, framework: 'react' }
            : { generated_code: inputData }
        ),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setResults(prev => ({ ...prev, [agentId]: result }));
    } catch (err) {
      setError(`Failed to call ${agentId} agent: ${err.message}`);
    } finally {
      setLoading(false);
      setActiveAgent(null);
    }
  };

  const handleOrchestrate = async () => {
    if (!inputData.trim()) {
      setError('Please enter some input data');
      return;
    }

    setLoading(true);
    setError('');
    setActiveAgent('orchestrator');

    try {
      const response = await fetch('http://localhost:8000/api/orchestrate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input_type: inputType,
          input_data: inputData,
          framework: 'react'
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setResults({
        vision: result.vision_result,
        code: result.code_result,
        evaluator: result.evaluation_result
      });
    } catch (err) {
      setError(`Failed to orchestrate: ${err.message}`);
    } finally {
      setLoading(false);
      setActiveAgent(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900">
      <Head>
        <title>DreamForge AI - Multi-Agent System</title>
        <meta name="description" content="AI-powered multi-agent system for code generation" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            🚀 DreamForge AI
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Transform your ideas into production-ready code with our intelligent multi-agent system
          </p>
        </div>

        {/* Input Section */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 mb-8 border border-white/20">
          <h2 className="text-2xl font-semibold text-white mb-6">Input Your Idea</h2>
          
          <div className="grid md:grid-cols-4 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Input Type
              </label>
              <select
                value={inputType}
                onChange={(e) => setInputType(e.target.value)}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="voice">Voice Description</option>
                <option value="sketch">Sketch Description</option>
                <option value="text">Text Description</option>
              </select>
            </div>
            
            <div className="md:col-span-3">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Description
              </label>
              <textarea
                value={inputData}
                onChange={(e) => setInputData(e.target.value)}
                placeholder="Describe your app idea, layout, or paste code to evaluate..."
                className="w-full px-4 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                rows={3}
              />
            </div>
          </div>

          {error && (
            <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-4 mb-6">
              <p className="text-red-200">{error}</p>
            </div>
          )}

          {/* Orchestrate Button */}
          <div className="text-center mb-6">
            <button
              onClick={handleOrchestrate}
              disabled={loading}
              className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 px-8 rounded-full transition-all duration-200 transform hover:scale-105"
            >
              {loading && activeAgent === 'orchestrator' ? (
                <LoadingSpinner />
              ) : (
                '🎯 Run Full Orchestration'
              )}
            </button>
          </div>
        </div>

        {/* Agent Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {agents.map((agent) => (
            <AgentCard
              key={agent.id}
              agent={agent}
              onCall={() => handleAgentCall(agent.id)}
              loading={loading && activeAgent === agent.id}
              disabled={loading}
            />
          ))}
        </div>

        {/* Results Section */}
        {Object.keys(results).length > 0 && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <h2 className="text-2xl font-semibold text-white mb-6">Results</h2>
            <div className="space-y-6">
              {Object.entries(results).map(([agentId, result]) => (
                <ResultDisplay
                  key={agentId}
                  agentId={agentId}
                  result={result}
                />
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}