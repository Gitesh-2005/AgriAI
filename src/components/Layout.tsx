import React, { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  MessageCircle, 
  Users, 
  User, 
  LogOut, 
  Sprout,
  Globe
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuth();
  const { translate, currentLanguage, setLanguage } = useLanguage();
  const location = useLocation();

  const navigation = [
    {
      name: translate('nav.dashboard'),
      href: '/dashboard',
      icon: Home,
    },
    {
      name: translate('nav.chat'),
      href: '/chat',
      icon: MessageCircle,
    },
    {
      name: translate('nav.agents'),
      href: '/agents',
      icon: Users,
    },
    {
      name: 'Analytics',
      href: '/analytics',
      icon: Globe,
    },
    {
      name: translate('nav.profile'),
      href: '/profile',
      icon: User,
    },
  ];

  const handleLanguageChange = (language: string) => {
    setLanguage(language);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center">
              <Sprout className="h-8 w-8 text-green-600" />
              <h1 className="ml-2 text-xl font-bold text-gray-900">AgriAI</h1>
            </div>

            {/* Navigation */}
            <nav className="hidden md:flex space-x-8">
              {navigation.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-green-100 text-green-700'
                        : 'text-gray-600 hover:text-green-600 hover:bg-green-50'
                    }`}
                  >
                    <Icon className="h-4 w-4 mr-2" />
                    {item.name}
                  </Link>
                );
              })}
            </nav>

            {/* User Menu */}
            <div className="flex items-center space-x-4">
              {/* Language Selector */}
              <div className="flex items-center space-x-2">
                <Globe className="h-4 w-4 text-gray-500" />
                <select
                  value={currentLanguage}
                  onChange={(e) => handleLanguageChange(e.target.value)}
                  className="text-sm border-gray-200 rounded-md focus:ring-green-500 focus:border-green-500"
                >
                  <option value="en">English</option>
                  <option value="hi">हिंदी</option>
                </select>
              </div>

              {/* User Info */}
              <div className="flex items-center space-x-3">
                <div className="text-sm">
                  <p className="font-medium text-gray-900">{user?.full_name}</p>
                  <p className="text-gray-500 capitalize">{user?.user_type}</p>
                </div>
                <button
                  onClick={logout}
                  className="flex items-center px-3 py-2 text-sm text-red-600 hover:text-red-700 hover:bg-red-50 rounded-md transition-colors"
                >
                  <LogOut className="h-4 w-4 mr-1" />
                  {translate('nav.logout')}
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Navigation */}
      <nav className="md:hidden bg-white border-b border-gray-200">
        <div className="px-4 py-2">
          <div className="flex space-x-1">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex-1 flex flex-col items-center px-2 py-2 text-xs font-medium rounded-md transition-colors ${
                    isActive
                      ? 'bg-green-100 text-green-700'
                      : 'text-gray-600 hover:text-green-600 hover:bg-green-50'
                  }`}
                >
                  <Icon className="h-5 w-5 mb-1" />
                  {item.name}
                </Link>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;