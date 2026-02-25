/**
 * API Service Module
 * Handles all HTTP requests to the backend API.
 */

import axios from 'axios';

// API Base URL - Backend server
const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds timeout for AI responses
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Send a chat message to the AI agent.
 * @param {string} message - The user's message
 * @returns {Promise<Object>} - The agent's response with tool info
 */
export const sendChatMessage = async (message) => {
  try {
    const response = await apiClient.post('/chat', { message });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    
    if (error.response) {
      // Server responded with error
      throw new Error(error.response.data.detail || 'Server error occurred');
    } else if (error.request) {
      // No response received
      throw new Error('Unable to connect to the server. Is the backend running?');
    } else {
      // Request setup error
      throw new Error('Failed to send message');
    }
  }
};

/**
 * Clear the chat history on the server.
 * @returns {Promise<Object>} - Success confirmation
 */
export const clearChatHistory = async () => {
  try {
    const response = await apiClient.post('/clear-history');
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw new Error('Failed to clear chat history');
  }
};

/**
 * Get the list of available tools from the server.
 * @returns {Promise<Object>} - List of tools
 */
export const getAvailableTools = async () => {
  try {
    const response = await apiClient.get('/tools');
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw new Error('Failed to fetch tools');
  }
};

/**
 * Check server health status.
 * @returns {Promise<Object>} - Health status
 */
export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw new Error('Server health check failed');
  }
};

export default apiClient;
