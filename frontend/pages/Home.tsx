import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Sprout,
  Cloud,
  BarChart3,
  Shield,
  Users,
  Zap,
  ArrowRight,
  CheckCircle
} from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

const Home: React.FC = () => {
  const { translate } = useLanguage();

  const features = [
    {
      icon: Sprout,
      title: 'Crop Advisory',
      description: 'Get personalized crop recommendations based on your location, soil, and season.',
    },
    {
      icon: Cloud,
      title: 'Weather Intelligence',
      description: 'Real-time weather forecasts with agricultural insights and irrigation advice.',
    },
    {
      icon: BarChart3,
      title: 'Market Insights',
      description: 'Live market prices, trends, and optimal selling strategies for maximum profit.',
    },
    {
      icon: Shield,
      title: 'Crop Protection',
      description: 'AI-powered pest and disease detection with treatment recommendations.',
    },
    {
      icon: Users,
      title: 'Expert Network',
      description: 'Connect with agricultural experts and fellow farmers for knowledge sharing.',
    },
    {
      icon: Zap,
      title: 'Instant Answers',
      description: 'Get immediate responses to your farming questions with AI-powered insights.',
    },
  ];

  const stats = [
    { number: '10K+', label: 'Active Farmers' },
    { number: '25+', label: 'AI Agents' },
    { number: '15+', label: 'Languages' },
    { number: '98%', label: 'Satisfaction' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-emerald-50">
      {/* Header */}
      <header className="relative bg-white/80 backdrop-blur-md border-b border-gray-200/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Sprout className="h-8 w-8 text-green-600" />
              <h1 className="ml-2 text-xl font-bold text-gray-900 bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
                AgriAI
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/login"
                className="text-gray-600 hover:text-green-600 font-medium transition-colors"
              >
                {/* {translate('home.cta.login')} */}
              </Link>
              <Link
                to="/register"
                className="bg-gradient-to-r from-green-600 to-blue-600 text-white px-6 py-2 rounded-full font-medium hover:shadow-lg transition-all duration-300 transform hover:scale-105"
              >
                {translate('home.cta.register')}
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-16 pb-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:grid lg:grid-cols-12 lg:gap-8">
            <motion.div
              className="sm:text-center md:max-w-2xl md:mx-auto lg:col-span-6 lg:text-left"
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                <span className="block">{translate('home.title')}</span>
                <span className="block text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-blue-600">
                  for Smart Farming
                </span>
              </h1>
              <p className="mt-3 text-base text-gray-500 sm:mt-5 sm:text-xl lg:text-lg xl:text-xl">
                {translate('home.subtitle')}. Get real-time insights on crops, weather, markets, and more with our AI-powered agricultural platform.
              </p>
              <div className="mt-8 sm:max-w-lg sm:mx-auto sm:text-center lg:text-left lg:mx-0">
                <Link
                  to="/register"
                  className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-full text-white bg-gradient-to-r from-green-600 to-blue-600 hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                >
                  Start Your Journey
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </div>
            </motion.div>
            <motion.div
              className="mt-12 relative sm:max-w-lg sm:mx-auto lg:mt-0 lg:max-w-none lg:mx-0 lg:col-span-6 lg:flex lg:items-center"
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              <div className="relative mx-auto w-full rounded-lg shadow-2xl lg:max-w-md">
                <div className="relative">
                  <img
                    className="w-full rounded-lg"
                    src="https://images.pexels.com/photos/1595104/pexels-photo-1595104.jpeg?auto=compress&cs=tinysrgb&w=800"
                    alt="Smart farming with technology"
                  />
                  <div className="absolute inset-0 rounded-lg bg-gradient-to-t from-green-900/50 to-transparent"></div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
              Powerful AI Agents for Every Farming Need
            </h2>
            <p className="mt-4 max-w-2xl mx-auto text-xl text-gray-500">
              Our specialized AI agents work together to provide comprehensive farming solutions
            </p>
          </div>

          <motion.div
            className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={feature.title}
                  className="relative group"
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-green-600 to-blue-600 rounded-lg blur opacity-25 group-hover:opacity-100 transition duration-1000 group-hover:duration-200"></div>
                  <div className="relative px-6 py-8 bg-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-300">
                    <div className="flex items-center justify-center h-12 w-12 rounded-full bg-gradient-to-r from-green-600 to-blue-600 text-white mx-auto">
                      <Icon className="h-6 w-6" />
                    </div>
                    <h3 className="mt-6 text-xl font-medium text-gray-900 text-center">{feature.title}</h3>
                    <p className="mt-2 text-base text-gray-500 text-center">{feature.description}</p>
                  </div>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-gradient-to-r from-green-600 to-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            className="grid grid-cols-2 gap-4 md:grid-cols-4"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                className="text-center"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <p className="text-3xl font-extrabold text-white">{stat.number}</p>
                <p className="text-green-100">{stat.label}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
              Ready to revolutionize your farming?
            </h2>
            <p className="mt-4 text-xl text-gray-600">
              Join thousands of farmers already using AI to increase their yields and profits
            </p>
            <div className="mt-8 flex justify-center space-x-4">
              <Link
                to="/register"
                className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-full text-white bg-gradient-to-r from-green-600 to-blue-600 hover:shadow-xl transition-all duration-300 transform hover:scale-105"
              >
                Get Started Free
                <CheckCircle className="ml-2 h-5 w-5" />
              </Link>
              <Link
                to="/login"
                className="inline-flex items-center px-8 py-4 border-2 border-gray-300 text-lg font-medium rounded-full text-gray-700 bg-white hover:bg-gray-50 hover:border-gray-400 transition-all duration-300"
              >
                Sign In
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-center">
            <Sprout className="h-8 w-8 text-green-400" />
            <span className="ml-2 text-xl font-bold">AgriAI</span>
          </div>
          <p className="mt-4 text-center text-gray-400">
            Empowering farmers with artificial intelligence for sustainable agriculture
          </p>
          <p className="mt-2 text-center text-gray-500 text-sm">
            © 2025 AgriAI. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Home;