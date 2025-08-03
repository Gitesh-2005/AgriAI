import React from 'react';
import { motion } from 'framer-motion';
import {
  Sprout,
  Cloud,
  TrendingUp,
  AlertTriangle,
  MessageCircle,
  Calendar,
  DollarSign,
  Users,
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { Link } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const { translate } = useLanguage();

  const quickActions = [
    {
      title: 'Ask AI Assistant',
      description: 'Get instant answers to your farming questions',
      icon: MessageCircle,
      color: 'from-blue-500 to-blue-600',
      href: '/chat',
    },
    {
      title: 'Weather Forecast',
      description: 'Check weather conditions and farming advice',
      icon: Cloud,
      color: 'from-sky-500 to-sky-600',
      href: '/chat?query=weather forecast',
    },
    {
      title: 'Market Prices',
      description: 'Get latest commodity prices and trends',
      icon: TrendingUp,
      color: 'from-green-500 to-green-600',
      href: '/chat?query=market prices',
    },
    {
      title: 'Crop Advisory',
      description: 'Personalized crop recommendations',
      icon: Sprout,
      color: 'from-emerald-500 to-emerald-600',
      href: '/chat?query=crop recommendation',
    },
  ];

  const recentActivity = [
    {
      type: 'weather',
      title: 'Weather forecast requested',
      description: 'Checked 7-day forecast for Punjab',
      time: '2 hours ago',
      icon: Cloud,
      color: 'text-blue-600',
    },
    {
      type: 'crop',
      title: 'Crop advisory session',
      description: 'Asked about wheat varieties for winter',
      time: '5 hours ago',
      icon: Sprout,
      color: 'text-green-600',
    },
    {
      type: 'market',
      title: 'Market prices checked',
      description: 'Viewed rice prices in local mandis',
      time: '1 day ago',
      icon: DollarSign,
      color: 'text-yellow-600',
    },
  ];

  const weatherWidget = {
    location: user?.location || 'Your Location',
    temperature: '28°C',
    condition: 'Partly Cloudy',
    humidity: '65%',
    advice: 'Good conditions for irrigation. Consider watering crops in the evening.',
  };

  const marketWidget = {
    trending: [
      { crop: 'Rice', price: '₹2,850/qt', change: '+2.5%', positive: true },
      { crop: 'Wheat', price: '₹2,150/qt', change: '+0.8%', positive: true },
      { crop: 'Cotton', price: '₹6,200/qt', change: '+3.2%', positive: true },
    ],
  };

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-gradient-to-r from-green-500 to-blue-600 rounded-2xl p-6 text-white"
      >
        <h1 className="text-2xl font-bold">
          {translate('dashboard.welcome')}, {user?.full_name}! 🌾
        </h1>
        <p className="mt-2 text-green-100">
          Ready to make smart farming decisions today? Your AI assistant is here to help.
        </p>
        <div className="mt-4 flex items-center space-x-4 text-sm">
          <div className="flex items-center">
            <Users className="h-4 w-4 mr-1" />
            <span className="capitalize">{user?.user_type}</span>
          </div>
          {user?.location && (
            <div className="flex items-center">
              <Calendar className="h-4 w-4 mr-1" />
              <span>{user.location}</span>
            </div>
          )}
        </div>
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          {translate('dashboard.quickActions')}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action, index) => {
            const Icon = action.icon;
            return (
              <motion.div
                key={action.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 + index * 0.1 }}
              >
                <Link
                  to={action.href}
                  className="block group relative overflow-hidden bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                >
                  <div className={`absolute inset-0 bg-gradient-to-r ${action.color} opacity-0 group-hover:opacity-10 transition-opacity`}></div>
                  <div className="p-6">
                    <div className={`inline-flex items-center justify-center w-12 h-12 rounded-lg bg-gradient-to-r ${action.color} text-white mb-4`}>
                      <Icon className="h-6 w-6" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {action.title}
                    </h3>
                    <p className="text-gray-600 text-sm">
                      {action.description}
                    </p>
                  </div>
                </Link>
              </motion.div>
            );
          })}
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Weather Widget */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="bg-white rounded-xl shadow-md p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Weather Today</h3>
            <Cloud className="h-6 w-6 text-blue-500" />
          </div>
          <div className="space-y-3">
            <div>
              <p className="text-sm text-gray-500">{weatherWidget.location}</p>
              <p className="text-2xl font-bold text-gray-900">{weatherWidget.temperature}</p>
              <p className="text-sm text-gray-600">{weatherWidget.condition}</p>
            </div>
            <div className="pt-3 border-t border-gray-100">
              <p className="text-sm text-gray-600">
                <span className="font-medium">Humidity:</span> {weatherWidget.humidity}
              </p>
            </div>
            <div className="bg-blue-50 rounded-lg p-3">
              <p className="text-sm text-blue-800">{weatherWidget.advice}</p>
            </div>
          </div>
        </motion.div>

        {/* Market Prices Widget */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="bg-white rounded-xl shadow-md p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Market Trends</h3>
            <TrendingUp className="h-6 w-6 text-green-500" />
          </div>
          <div className="space-y-3">
            {marketWidget.trending.map((item, index) => (
              <div key={item.crop} className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">{item.crop}</p>
                  <p className="text-sm text-gray-500">{item.price}</p>
                </div>
                <div className={`text-sm font-medium ${item.positive ? 'text-green-600' : 'text-red-600'}`}>
                  {item.change}
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 text-center">
            <Link
              to="/chat?query=market prices"
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              View all prices →
            </Link>
          </div>
        </motion.div>

        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="bg-white rounded-xl shadow-md p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">
              {translate('dashboard.recentActivity')}
            </h3>
            <AlertTriangle className="h-6 w-6 text-orange-500" />
          </div>
          <div className="space-y-4">
            {recentActivity.map((activity, index) => {
              const Icon = activity.icon;
              return (
                <div key={index} className="flex items-start space-x-3">
                  <div className={`flex-shrink-0 ${activity.color}`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">
                      {activity.title}
                    </p>
                    <p className="text-xs text-gray-500">
                      {activity.description}
                    </p>
                    <p className="text-xs text-gray-400 mt-1">
                      {activity.time}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;