import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import {
  TrendingUp,
  Users,
  MessageCircle,
  BarChart3,
  Calendar,
  Download,
  Filter
} from 'lucide-react';
import AgentDashboard from '../components/AgentDashboard';
import { useAuth } from '../contexts/AuthContext';

const Analytics: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [dateRange, setDateRange] = useState('7d');
  const { user } = useAuth();

  // Mock analytics data (in production, this would come from your analytics API)
  const analyticsData = {
    overview: {
      totalQueries: 1247,
      activeUsers: 89,
      avgResponseTime: 1.4,
      satisfactionRate: 96.8,
      topQueries: [
        { query: "Weather forecast", count: 234 },
        { query: "Crop recommendations", count: 189 },
        { query: "Market prices", count: 156 },
        { query: "Soil analysis", count: 134 },
        { query: "Pest control", count: 98 }
      ]
    },
    userEngagement: {
      dailyActiveUsers: [
        { date: '2024-01-01', users: 45 },
        { date: '2024-01-02', users: 52 },
        { date: '2024-01-03', users: 48 },
        { date: '2024-01-04', users: 61 },
        { date: '2024-01-05', users: 58 },
        { date: '2024-01-06', users: 67 },
        { date: '2024-01-07', users: 73 }
      ],
      sessionDuration: 8.5, // minutes
      queriesPerSession: 3.2
    }
  };

  const tabs = [
    { id: 'overview', name: 'Overview', icon: BarChart3 },
    { id: 'agents', name: 'Agent Performance', icon: MessageCircle },
    { id: 'users', name: 'User Analytics', icon: Users },
    { id: 'trends', name: 'Trends', icon: TrendingUp }
  ];

  const StatCard = ({ title, value, change, icon: Icon, color }: any) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow-md p-6"
    >
      <div className="flex items-center">
        <div className={`p-3 rounded-lg ${color}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
        <div className="ml-4 flex-1">
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {change && (
            <p className={`text-sm ${change > 0 ? 'text-green-600' : 'text-red-600'}`}>
              {change > 0 ? '+' : ''}{change}% from last period
            </p>
          )}
        </div>
      </div>
    </motion.div>
  );

  const renderOverview = () => (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Queries"
          value={analyticsData.overview.totalQueries.toLocaleString()}
          change={12.5}
          icon={MessageCircle}
          color="bg-blue-500"
        />
        <StatCard
          title="Active Users"
          value={analyticsData.overview.activeUsers}
          change={8.3}
          icon={Users}
          color="bg-green-500"
        />
        <StatCard
          title="Avg Response Time"
          value={`${analyticsData.overview.avgResponseTime}s`}
          change={-5.2}
          icon={TrendingUp}
          color="bg-yellow-500"
        />
        <StatCard
          title="Satisfaction Rate"
          value={`${analyticsData.overview.satisfactionRate}%`}
          change={2.1}
          icon={BarChart3}
          color="bg-purple-500"
        />
      </div>

      {/* Top Queries */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-lg shadow-md p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Most Popular Queries</h3>
        <div className="space-y-3">
          {analyticsData.overview.topQueries.map((item, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span className="font-medium text-gray-900">{item.query}</span>
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-500">{item.count} queries</span>
                <div className="w-16 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full"
                    style={{ width: `${(item.count / 234) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );

  const renderUserAnalytics = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Session Duration"
          value={`${analyticsData.userEngagement.sessionDuration} min`}
          change={15.2}
          icon={Calendar}
          color="bg-indigo-500"
        />
        <StatCard
          title="Queries per Session"
          value={analyticsData.userEngagement.queriesPerSession}
          change={7.8}
          icon={MessageCircle}
          color="bg-pink-500"
        />
        <StatCard
          title="Return Rate"
          value="78%"
          change={4.5}
          icon={Users}
          color="bg-cyan-500"
        />
      </div>

      {/* User Demographics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-lg shadow-md p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">User Demographics</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-3">By User Type</h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Farmers</span>
                <span className="font-medium">68%</span>
              </div>
              <div className="flex justify-between">
                <span>Vendors</span>
                <span className="font-medium">18%</span>
              </div>
              <div className="flex justify-between">
                <span>Policymakers</span>
                <span className="font-medium">9%</span>
              </div>
              <div className="flex justify-between">
                <span>Financiers</span>
                <span className="font-medium">5%</span>
              </div>
            </div>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 mb-3">By Region</h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>North India</span>
                <span className="font-medium">35%</span>
              </div>
              <div className="flex justify-between">
                <span>South India</span>
                <span className="font-medium">28%</span>
              </div>
              <div className="flex justify-between">
                <span>West India</span>
                <span className="font-medium">22%</span>
              </div>
              <div className="flex justify-between">
                <span>East India</span>
                <span className="font-medium">15%</span>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="text-gray-600 mt-1">Monitor system performance and user engagement</p>
        </div>
        <div className="flex items-center space-x-4">
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          >
            <option value="1d">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 3 Months</option>
          </select>
          <button className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
            <Download className="h-4 w-4 mr-2" />
            Export
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-green-500 text-green-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="h-4 w-4 mr-2" />
                {tab.name}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="mt-6">
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'agents' && <AgentDashboard />}
        {activeTab === 'users' && renderUserAnalytics()}
        {activeTab === 'trends' && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Trends Analysis</h3>
            <p className="text-gray-600">Trends analysis coming soon...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Analytics;