import React, { createContext, useState, useContext, useCallback } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

const TaskContext = createContext(null);

export const useTask = () => {
  const context = useContext(TaskContext);
  if (!context) {
    throw new Error('useTask must be used within a TaskProvider');
  }
  return context;
};

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const TaskProvider = ({ children }) => {
  const { token } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState(null); // null, true, false
  const [sortBy, setSortBy] = useState('created_at');
  const [sortOrder, setSortOrder] = useState(-1);
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState(null);

  const fetchTasks = useCallback(async () => {
    if (!token) return;
    
    setLoading(true);
    try {
      const params = {
        sort_by: sortBy,
        sort_order: sortOrder,
      };
      
      if (filter !== null) {
        params.completed = filter;
      }
      
      if (searchQuery) {
        params.search = searchQuery;
      }
      
      if (categoryFilter) {
        params.category = categoryFilter;
      }
      
      const response = await axios.get(`${API}/tasks`, {
        headers: { Authorization: `Bearer ${token}` },
        params,
      });
      
      setTasks(response.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  }, [token, filter, sortBy, sortOrder, searchQuery, categoryFilter]);

  const fetchStats = useCallback(async () => {
    if (!token) return;
    
    try {
      const response = await axios.get(`${API}/tasks/stats`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  }, [token]);

  const createTask = async (taskData) => {
    try {
      const response = await axios.post(`${API}/tasks`, taskData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      await fetchTasks();
      await fetchStats();
      return response.data;
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  };

  const updateTask = async (taskId, taskData) => {
    try {
      const response = await axios.put(`${API}/tasks/${taskId}`, taskData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      await fetchTasks();
      await fetchStats();
      return response.data;
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  };

  const deleteTask = async (taskId) => {
    try {
      await axios.delete(`${API}/tasks/${taskId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      await fetchTasks();
      await fetchStats();
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  };

  const toggleComplete = async (taskId, completed) => {
    try {
      await axios.patch(
        `${API}/tasks/${taskId}/complete`,
        null,
        {
          headers: { Authorization: `Bearer ${token}` },
          params: { completed },
        }
      );
      await fetchTasks();
      await fetchStats();
    } catch (error) {
      console.error('Error toggling task completion:', error);
      throw error;
    }
  };

  const value = {
    tasks,
    stats,
    loading,
    filter,
    sortBy,
    sortOrder,
    searchQuery,
    categoryFilter,
    setFilter,
    setSortBy,
    setSortOrder,
    setSearchQuery,
    setCategoryFilter,
    fetchTasks,
    fetchStats,
    createTask,
    updateTask,
    deleteTask,
    toggleComplete,
  };

  return <TaskContext.Provider value={value}>{children}</TaskContext.Provider>;
};
