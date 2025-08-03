import React from 'react';
import { motion } from 'framer-motion';
import { User, Mail, Phone, MapPin, Briefcase, Calendar, Edit2 } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';

const Profile: React.FC = () => {
  const { user } = useAuth();
  const { translate } = useLanguage();

  const profileFields = [
    {
      label: 'Full Name',
      value: user?.full_name,
      icon: User,
      key: 'full_name',
    },
    {
      label: 'Email',
      value: user?.email,
      icon: Mail,
      key: 'email',
    },
    {
      label: 'User Type',
      value: user?.user_type,
      icon: Briefcase,
      key: 'user_type',
    },
    {
      label: 'Location',
      value: user?.location || 'Not specified',
      icon: MapPin,
      key: 'location',
    },
    {
      label: 'Farm Size',
      value: user?.farm_size || 'Not specified',
      icon: Calendar,
      key: 'farm_size',
    },
    {
      label: 'Language',
      value: user?.language_preference === 'hi' ? 'Hindi' : 'English',
      icon: Phone,
      key: 'language_preference',
    },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center"
      >
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          {translate('nav.profile')}
        </h1>
        <p className="text-lg text-gray-600">
          Manage your account settings and preferences
        </p>
      </motion.div>

      {/* Profile Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="bg-white rounded-xl shadow-lg overflow-hidden"
      >
        {/* Header Section */}
        <div className="bg-gradient-to-r from-green-500 to-blue-600 px-6 py-8">
          <div className="flex items-center space-x-4">
            <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center">
              <User className="h-10 w-10 text-white" />
            </div>
            <div className="text-white">
              <h2 className="text-2xl font-bold">{user?.full_name}</h2>
              <p className="text-green-100 capitalize">{user?.user_type}</p>
              <p className="text-green-100 text-sm">{user?.email}</p>
            </div>
          </div>
        </div>

        {/* Profile Information */}
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold text-gray-900">Profile Information</h3>
            <button className="flex items-center space-x-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors">
              <Edit2 className="h-4 w-4" />
              <span>Edit Profile</span>
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {profileFields.map((field, index) => {
              const Icon = field.icon;
              return (
                <motion.div
                  key={field.key}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: 0.2 + index * 0.1 }}
                  className="flex items-center space-x-3 p-4 bg-gray-50 rounded-lg"
                >
                  <div className="flex-shrink-0">
                    <Icon className="h-5 w-5 text-gray-500" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-500">{field.label}</p>
                    <p className="text-gray-900 capitalize">{field.value}</p>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </motion.div>

      {/* Account Settings */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="bg-white rounded-xl shadow-lg p-6"
      >
        <h3 className="text-xl font-semibold text-gray-900 mb-6">Account Settings</h3>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <h4 className="font-medium text-gray-900">Notifications</h4>
              <p className="text-sm text-gray-500">Receive alerts about weather, prices, and farming tips</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" className="sr-only peer" defaultChecked />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <h4 className="font-medium text-gray-900">Location Services</h4>
              <p className="text-sm text-gray-500">Allow location access for weather and local market data</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" className="sr-only peer" defaultChecked />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <h4 className="font-medium text-gray-900">Data Sharing</h4>
              <p className="text-sm text-gray-500">Share anonymized data to improve AI recommendations</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" className="sr-only peer" />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"></div>
            </label>
          </div>
        </div>
      </motion.div>

      {/* Usage Statistics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        className="bg-white rounded-xl shadow-lg p-6"
      >
        <h3 className="text-xl font-semibold text-gray-900 mb-6">Usage Statistics</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600 mb-2">47</div>
            <div className="text-sm text-gray-600">Questions Asked</div>
          </div>
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600 mb-2">12</div>
            <div className="text-sm text-gray-600">Weather Checks</div>
          </div>
          <div className="text-center p-4 bg-orange-50 rounded-lg">
            <div className="text-2xl font-bold text-orange-600 mb-2">8</div>
            <div className="text-sm text-gray-600">Market Queries</div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Profile;