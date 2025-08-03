import React from 'react';
import { motion } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import {
  Bot,
  Sprout,
  Cloud,
  TrendingUp,
  Shield,
  Globe,
  MessageCircle,
  Settings,
  CheckCircle,
  AlertCircle,
  Loader2,
} from 'lucide-react';
import { agentsAPI } from '../services/api';
import { useLanguage } from '../contexts/LanguageContext';

const Agents: React.FC = () => {
  const { translate } = useLanguage();

  // Fetch agent capabilities
  const { data: capabilities, isLoading: capabilitiesLoading } = useQuery({
    queryKey: ['agent-capabilities'],
    queryFn: agentsAPI.getCapabilities,
  });

  // Fetch agent health
  const { data: health, isLoading: healthLoading } = useQuery({
    queryKey: ['agent-health'],
    queryFn: agentsAPI.getHealth,
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  const agentInfo = [
    {
      id: 'intent_classifier',
      name: 'Intent Classifier',
      description: 'Analyzes your questions to route them to the right specialist',
      icon: MessageCircle,
      color: 'from-purple-500 to-purple-600',
      features: ['Natural Language Processing', 'Intent Recognition', 'Query Routing'],
    },
    {
      id: 'crop_advisory',
      name: 'Crop Advisory',
      description: 'Provides personalized crop recommendations and farming advice',
      icon: Sprout,
      color: 'from-green-500 to-green-600',
      features: ['Crop Selection', 'Variety Recommendations', 'Seasonal Planning', 'Soil Matching'],
    },
    {
      id: 'weather',
      name: 'Weather Intelligence',
      description: 'Real-time weather forecasts with agricultural insights',
      icon: Cloud,
      color: 'from-blue-500 to-blue-600',
      features: ['7-Day Forecasts', 'Irrigation Advice', 'Weather Alerts', 'Climate Analysis'],
    },
    {
      id: 'market_intelligence',
      name: 'Market Intelligence',
      description: 'Live market prices, trends, and trading recommendations',
      icon: TrendingUp,
      color: 'from-yellow-500 to-orange-600',
      features: ['Real-time Prices', 'Market Trends', 'Trading Advice', 'Price Alerts'],
    },
    {
      id: 'soil_analysis',
      name: 'Soil Analysis',
      description: 'Soil health assessment and fertilizer recommendations',
      icon: Settings,
      color: 'from-amber-500 to-amber-600',
      features: ['NPK Analysis', 'pH Testing', 'Fertilizer Planning', 'Soil Health Tips'],
    },
    {
      id: 'pest_disease',
      name: 'Crop Protection',
      description: 'AI-powered pest and disease detection with treatments',
      icon: Shield,
      color: 'from-red-500 to-red-600',
      features: ['Disease Detection', 'Pest Identification', 'Treatment Plans', 'Prevention Tips'],
    },
    {
      id: 'irrigation_planning',
      name: 'Irrigation Planning',
      description: 'Smart irrigation scheduling and water management',
      icon: Globe,
      color: 'from-cyan-500 to-cyan-600',
      features: ['Water Scheduling', 'Efficiency Analysis', 'Conservation Tips', 'System Design'],
    },
    {
      id: 'financial_planning',
      name: 'Financial Planning',
      description: 'Loan guidance, profitability analysis, and financial advice',
      icon: Bot,
      color: 'from-indigo-500 to-indigo-600',
      features: ['Loan Assistance', 'Cost Analysis', 'Subsidy Information', 'Insurance Guidance'],
    },
    {
      id: 'policy_query',
      name: 'Policy & Regulations',
      description: 'Information on agricultural policies, laws, and compliance',
      icon: CheckCircle,
      color: 'from-violet-500 to-violet-600',
      features: ['Policy Updates', 'Compliance Guide', 'Legal Framework', 'Government Schemes'],
    },
    {
      id: 'translation',
      name: 'Translation Service',
      description: 'Translates agricultural content between languages',
      icon: Globe,
      color: 'from-pink-500 to-pink-600',
      features: ['Multi-language Support', 'Agricultural Terms', 'Regional Languages', 'Voice Translation'],
    },
  ];

  const getHealthStatus = (agentId: string) => {
    if (!health) return 'unknown';
    return health[agentId] === 'healthy' ? 'healthy' : 'unhealthy';
  };

  const getHealthIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'unhealthy':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Loader2 className="h-5 w-5 text-gray-400 animate-spin" />;
    }
  };

  const getHealthColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'text-green-600 bg-green-50';
      case 'unhealthy':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center"
      >
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          {translate('agents.title')}
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          {translate('agents.description')}. Each agent specializes in different aspects of agriculture to provide you with expert advice.
        </p>
      </motion.div>

      {/* System Status */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="bg-white rounded-xl shadow-md p-6"
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">System Status</h2>
          <div className="flex items-center space-x-2">
            {healthLoading ? (
              <Loader2 className="h-5 w-5 text-gray-400 animate-spin" />
            ) : (
              <div className="h-3 w-3 bg-green-400 rounded-full animate-pulse"></div>
            )}
            <span className="text-sm text-gray-600">
              {healthLoading ? 'Checking...' : 'All systems operational'}
            </span>
          </div>
        </div>
        
        {!healthLoading && health && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(health).map(([agentId, status]) => (
              <div
                key={agentId}
                className={`p-3 rounded-lg flex items-center space-x-2 ${getHealthColor(status as string)}`}
              >
                {getHealthIcon(status as string)}
                <span className="text-sm font-medium capitalize">
                  {agentId.replace('_', ' ')}
                </span>
              </div>
            ))}
          </div>
        )}
      </motion.div>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agentInfo.map((agent, index) => {
          const Icon = agent.icon;
          const healthStatus = getHealthStatus(agent.id);
          
          return (
            <motion.div
              key={agent.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 + index * 0.1 }}
              className="group relative overflow-hidden bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-300"
            >
              {/* Gradient Background */}
              <div className={`absolute inset-0 bg-gradient-to-r ${agent.color} opacity-0 group-hover:opacity-5 transition-opacity`}></div>
              
              <div className="relative p-6">
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className={`p-3 rounded-lg bg-gradient-to-r ${agent.color} text-white`}>
                    <Icon className="h-6 w-6" />
                  </div>
                  <div className="flex items-center space-x-1">
                    {getHealthIcon(healthStatus)}
                  </div>
                </div>

                {/* Content */}
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {agent.name}
                </h3>
                <p className="text-gray-600 text-sm mb-4">
                  {agent.description}
                </p>

                {/* Features */}
                <div className="space-y-2">
                  <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                    Key Features
                  </p>
                  <div className="flex flex-wrap gap-1">
                    {agent.features.map((feature, featureIndex) => (
                      <span
                        key={featureIndex}
                        className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
                      >
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Capabilities from API */}
                {capabilities && capabilities[agent.id] && (
                  <div className="mt-4 pt-4 border-t border-gray-100">
                    <p className="text-xs text-gray-500">
                      {capabilities[agent.id].description}
                    </p>
                  </div>
                )}
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* How It Works */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.8 }}
        className="bg-gradient-to-r from-green-50 to-blue-50 rounded-xl p-8"
      >
        <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
          How Our AI Agents Work Together
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <MessageCircle className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">1. You Ask</h3>
            <p className="text-gray-600 text-sm">
              Ask your question in natural language about any farming topic
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Bot className="h-6 w-6 text-purple-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">2. AI Routes</h3>
            <p className="text-gray-600 text-sm">
              Our Intent Classifier routes your question to the right specialist agent
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">3. Expert Answer</h3>
            <p className="text-gray-600 text-sm">
              The specialist agent provides detailed, actionable advice
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Agents;