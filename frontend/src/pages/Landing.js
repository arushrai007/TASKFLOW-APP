import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { CheckCircle2, Zap, Shield, BarChart3, Calendar, Tag, Search, Moon, ArrowRight, CheckCheck, Target, Clock } from 'lucide-react';

const Landing = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <CheckCheck className="w-6 h-6" />,
      title: "Smart Task Management",
      description: "Create, organize, and track tasks with priorities, due dates, and custom categories"
    },
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: "Analytics Dashboard",
      description: "Get insights into your productivity with detailed statistics and progress tracking"
    },
    {
      icon: <Search className="w-6 h-6" />,
      title: "Powerful Search",
      description: "Find any task instantly with advanced search across titles, descriptions, and tags"
    },
    {
      icon: <Tag className="w-6 h-6" />,
      title: "Tags & Categories",
      description: "Organize tasks with flexible tagging and categorization for better workflow"
    },
    {
      icon: <Calendar className="w-6 h-6" />,
      title: "Due Date Tracking",
      description: "Never miss a deadline with due date reminders and overdue task alerts"
    },
    {
      icon: <Moon className="w-6 h-6" />,
      title: "Dark Mode",
      description: "Work comfortably at any time with our beautiful dark mode interface"
    }
  ];

  const stats = [
    { number: "10K+", label: "Active Users" },
    { number: "50K+", label: "Tasks Completed" },
    { number: "99.9%", label: "Uptime" },
    { number: "4.9/5", label: "User Rating" }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-50 via-cyan-50 to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900" data-testid="landing-page">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl border-b border-gray-200 dark:border-gray-700 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-xl flex items-center justify-center">
                <CheckCircle2 className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold text-gray-900 dark:text-white" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>TaskFlow</span>
            </div>
            <div className="flex items-center gap-3">
              <Button
                variant="ghost"
                onClick={() => navigate('/signin')}
                className="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white"
                data-testid="header-signin-button"
              >
                Sign In
              </Button>
              <Button
                onClick={() => navigate('/signup')}
                className="bg-gradient-to-r from-teal-500 to-cyan-600 hover:from-teal-600 hover:to-cyan-700 text-white"
                data-testid="header-signup-button"
              >
                Get Started
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-teal-100 dark:bg-teal-900/30 text-teal-700 dark:text-teal-300 px-4 py-2 rounded-full text-sm font-medium mb-6">
            <Zap className="w-4 h-4" />
            <span>Boost Your Productivity</span>
          </div>
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white mb-6" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            Organize Your Life,
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-cyan-600">One Task at a Time</span>
          </h1>
          <p className="text-lg sm:text-xl text-gray-600 dark:text-gray-300 mb-10 max-w-3xl mx-auto">
            The ultimate task management platform with powerful features to help you stay organized,
            focused, and productive. Track, prioritize, and complete your tasks effortlessly.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              size="lg"
              onClick={() => navigate('/signup')}
              className="bg-gradient-to-r from-teal-500 to-cyan-600 hover:from-teal-600 hover:to-cyan-700 text-white text-lg px-8 py-6 rounded-xl"
              data-testid="hero-signup-button"
            >
              Start Free Today
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              onClick={() => navigate('/signin')}
              className="text-lg px-8 py-6 rounded-xl border-2 border-gray-300 dark:border-gray-600"
              data-testid="hero-signin-button"
            >
              Sign In
            </Button>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-cyan-600 mb-2" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                  {stat.number}
                </div>
                <div className="text-gray-600 dark:text-gray-400 font-medium">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 dark:text-white mb-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Everything You Need
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Powerful features designed to make task management simple and effective
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 dark:border-gray-700 hover:scale-105"
              >
                <div className="w-14 h-14 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-xl flex items-center justify-center text-white mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 dark:text-white mb-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              How It Works
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300">Get started in three simple steps</p>
          </div>
          <div className="grid md:grid-cols-3 gap-12">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                1
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Create Account</h3>
              <p className="text-gray-600 dark:text-gray-400">Sign up in seconds and get instant access to all features</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                2
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Add Your Tasks</h3>
              <p className="text-gray-600 dark:text-gray-400">Create tasks with priorities, due dates, and categories</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                3
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Stay Productive</h3>
              <p className="text-gray-600 dark:text-gray-400">Track progress and achieve your goals efficiently</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <div className="bg-gradient-to-br from-teal-500 to-cyan-600 rounded-3xl p-12 shadow-2xl">
            <h2 className="text-4xl sm:text-5xl font-bold text-white mb-6" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Ready to Get Organized?
            </h2>
            <p className="text-xl text-teal-50 mb-8">
              Join thousands of users who are achieving more every day with TaskFlow
            </p>
            <Button
              size="lg"
              onClick={() => navigate('/signup')}
              className="bg-white text-teal-600 hover:bg-gray-100 text-lg px-8 py-6 rounded-xl font-semibold"
              data-testid="cta-signup-button"
            >
              Get Started Free
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-8 h-8 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-lg flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900 dark:text-white" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>TaskFlow</span>
          </div>
          <p className="text-gray-600 dark:text-gray-400 mb-2">© 2025 TaskFlow. All rights reserved.</p>
          <p className="text-sm text-gray-500 dark:text-gray-500">Made with ❤️ for productivity enthusiasts</p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
