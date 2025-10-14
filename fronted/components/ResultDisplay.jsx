import { useState } from 'react';

export default function ResultDisplay({ agentId, result }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const getAgentInfo = (id) => {
    const agentMap = {
      vision: { name: 'Vision Agent', icon: '👁️', color: 'text-blue-400' },
      code: { name: 'Code Agent', icon: '⚙️', color: 'text-green-400' },
      evaluator: { name: 'Evaluator Agent', icon: '🧪', color: 'text-purple-400' }
    };
    return agentMap[id] || { name: id, icon: '🤖', color: 'text-gray-400' };
  };

  const agent = getAgentInfo(agentId);

  const renderVisionResult = (result) => (
    <div className="space-y-3">
      <div>
        <h4 className="font-semibold text-white mb-2">Layout Description:</h4>
        <p className="text-gray-300 bg-gray-800/50 p-3 rounded-lg">{result.layout}</p>
      </div>
      
      {result.components && result.components.length > 0 && (
        <div>
          <h4 className="font-semibold text-white mb-2">Components:</h4>
          <div className="flex flex-wrap gap-2">
            {result.components.map((component, idx) => (
              <span key={idx} className="bg-blue-500/20 text-blue-300 px-3 py-1 rounded-full text-sm">
                {component}
              </span>
            ))}
          </div>
        </div>
      )}
      
      {result.data_elements && result.data_elements.length > 0 && (
        <div>
          <h4 className="font-semibold text-white mb-2">Data Elements:</h4>
          <div className="flex flex-wrap gap-2">
            {result.data_elements.map((element, idx) => (
              <span key={idx} className="bg-green-500/20 text-green-300 px-3 py-1 rounded-full text-sm">
                {element}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  const renderCodeResult = (result) => (
    <div>
      <h4 className="font-semibold text-white mb-2">Generated Code:</h4>
      <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
        <pre className="text-green-400 text-sm whitespace-pre-wrap">
          {isExpanded ? result.generated_code : `${result.generated_code.substring(0, 500)}...`}
        </pre>
        {result.generated_code.length > 500 && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="mt-2 text-blue-400 hover:text-blue-300 text-sm underline"
          >
            {isExpanded ? 'Show Less' : 'Show More'}
          </button>
        )}
      </div>
    </div>
  );

  const renderEvaluatorResult = (result) => (
    <div className="space-y-3">
      <div className="flex items-center gap-2">
        <span className="font-semibold text-white">Status:</span>
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
          result.status === 'ok' ? 'bg-green-500/20 text-green-300' :
          result.status === 'warning' ? 'bg-yellow-500/20 text-yellow-300' :
          'bg-red-500/20 text-red-300'
        }`}>
          {result.status.toUpperCase()}
        </span>
      </div>
      
      <div>
        <h4 className="font-semibold text-white mb-2">Overall Feedback:</h4>
        <p className="text-gray-300 bg-gray-800/50 p-3 rounded-lg">{result.overall_feedback}</p>
      </div>
      
      {result.issues && result.issues.length > 0 && (
        <div>
          <h4 className="font-semibold text-white mb-2">Issues:</h4>
          <ul className="space-y-1">
            {result.issues.map((issue, idx) => (
              <li key={idx} className="text-red-300 bg-red-500/10 p-2 rounded flex items-start gap-2">
                <span className="text-red-400 mt-0.5">⚠️</span>
                {issue}
              </li>
            ))}
          </ul>
        </div>
      )}
      
      {result.suggestions && result.suggestions.length > 0 && (
        <div>
          <h4 className="font-semibold text-white mb-2">Suggestions:</h4>
          <ul className="space-y-1">
            {result.suggestions.map((suggestion, idx) => (
              <li key={idx} className="text-blue-300 bg-blue-500/10 p-2 rounded flex items-start gap-2">
                <span className="text-blue-400 mt-0.5">💡</span>
                {suggestion}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );

  const renderResult = () => {
    switch (agentId) {
      case 'vision':
        return renderVisionResult(result);
      case 'code':
        return renderCodeResult(result);
      case 'evaluator':
        return renderEvaluatorResult(result);
      default:
        return <pre className="text-gray-300 whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>;
    }
  };

  return (
    <div className="bg-gray-800/30 rounded-xl p-6 border border-gray-700">
      <div className="flex items-center gap-3 mb-4">
        <span className="text-2xl">{agent.icon}</span>
        <h3 className={`text-xl font-semibold ${agent.color}`}>
          {agent.name} Results
        </h3>
        {result.success && (
          <span className="bg-green-500/20 text-green-300 px-2 py-1 rounded text-xs">
            ✅ Success
          </span>
        )}
      </div>
      
      {renderResult()}
    </div>
  );
}
