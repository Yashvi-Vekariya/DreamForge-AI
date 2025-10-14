import LoadingSpinner from './LoadingSpinner';

export default function AgentCard({ agent, onCall, loading, disabled }) {
  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 hover:bg-white/20 transition-all duration-200 transform hover:scale-105">
      <div className="text-center">
        <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full ${agent.color} mb-4`}>
          <span className="text-2xl">{agent.icon}</span>
        </div>
        
        <h3 className="text-xl font-semibold text-white mb-2">
          {agent.name}
        </h3>
        
        <p className="text-gray-300 mb-6 text-sm">
          {agent.description}
        </p>
        
        <button
          onClick={onCall}
          disabled={disabled}
          className={`w-full py-2 px-4 rounded-lg font-medium transition-all duration-200 ${
            disabled 
              ? 'bg-gray-600 text-gray-400 cursor-not-allowed' 
              : `${agent.color} hover:opacity-80 text-white`
          }`}
        >
          {loading ? (
            <LoadingSpinner size="sm" />
          ) : (
            `Call ${agent.name}`
          )}
        </button>
      </div>
    </div>
  );
}
