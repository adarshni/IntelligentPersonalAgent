import React, { useState, useRef, useEffect, useCallback } from 'react';
import {
  makeStyles,
  tokens,
  Input,
  Button,
  Spinner,
  Text,
} from '@fluentui/react-components';
import {
  Send24Filled,
  ErrorCircle24Regular,
} from '@fluentui/react-icons';
import MessageBubble from './MessageBubble';
import { sendChatMessage } from '../api';

/**
 * Styles for the chat window.
 */
const useStyles = makeStyles({
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    backgroundColor: tokens.colorNeutralBackground2,
  },
  messagesContainer: {
    flex: 1,
    overflowY: 'auto',
    padding: '20px 24px',
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  welcomeMessage: {
    textAlign: 'center',
    padding: '40px 20px',
    color: tokens.colorNeutralForeground3,
  },
  welcomeTitle: {
    fontSize: tokens.fontSizeBase500,
    fontWeight: tokens.fontWeightSemibold,
    marginBottom: '12px',
    color: tokens.colorNeutralForeground1,
  },
  welcomeSubtitle: {
    fontSize: tokens.fontSizeBase300,
    marginBottom: '24px',
  },
  suggestions: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '8px',
    justifyContent: 'center',
  },
  suggestionButton: {
    fontSize: tokens.fontSizeBase200,
  },
  inputContainer: {
    padding: '16px 24px',
    backgroundColor: tokens.colorNeutralBackground1,
    borderTop: `1px solid ${tokens.colorNeutralStroke1}`,
  },
  inputWrapper: {
    display: 'flex',
    gap: '12px',
    alignItems: 'center',
  },
  input: {
    flex: 1,
  },
  sendButton: {
    minWidth: '80px',
  },
  loadingContainer: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '12px',
    color: tokens.colorNeutralForeground3,
  },
  errorContainer: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '12px',
    backgroundColor: tokens.colorPaletteRedBackground1,
    borderRadius: '8px',
    margin: '0 24px',
  },
  errorText: {
    color: tokens.colorPaletteRedForeground1,
  },
});

/**
 * Sample prompts for user guidance.
 */
const SAMPLE_PROMPTS = [
  "What's the sum of 10, 20, and 35?",
  "Convert 100 USD to INR",
  "What's the weather in Bangalore?",
  "What's today's date?",
  "Search for latest AI news",
];

/**
 * ChatWindow Component.
 * Main chat interface with message history, input, and loading states.
 * 
 * @param {Object} props
 * @param {Array} props.messages - Array of message objects
 * @param {Function} props.setMessages - State setter for messages
 * @param {Function} props.onToolLog - Callback for logging tool usage
 */
function ChatWindow({ messages, setMessages, onToolLog }) {
  const styles = useStyles();
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  /**
   * Scroll to bottom of messages.
   */
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  /**
   * Send a message to the agent.
   */
  const handleSend = useCallback(async (messageText = inputValue) => {
    const trimmedMessage = messageText.trim();
    if (!trimmedMessage || isLoading) return;

    setError(null);
    setInputValue('');

    // Add user message
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: trimmedMessage,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);

    setIsLoading(true);

    try {
      // Send to API
      const response = await sendChatMessage(trimmedMessage);

      // Add agent message
      const agentMessage = {
        id: Date.now() + 1,
        role: 'agent',
        content: response.response,
        toolUsed: response.tool_used,
        toolOutput: response.tool_output,
        thinking: response.thinking,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, agentMessage]);

      // Log tool usage
      if (response.tool_used) {
        onToolLog({
          tool: response.tool_used,
          input: response.thinking,
          output: response.tool_output,
          success: true,
        });
      }
    } catch (err) {
      setError(err.message);
      
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        role: 'agent',
        content: `Sorry, I encountered an error: ${err.message}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  }, [inputValue, isLoading, setMessages, onToolLog]);

  /**
   * Handle Enter key press.
   */
  const handleKeyPress = useCallback((e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }, [handleSend]);

  /**
   * Handle suggestion click.
   */
  const handleSuggestion = useCallback((suggestion) => {
    handleSend(suggestion);
  }, [handleSend]);

  return (
    <div className={styles.container}>
      {/* Messages Area */}
      <div className={styles.messagesContainer}>
        {/* Welcome Message (when no messages) */}
        {messages.length === 0 && !isLoading && (
          <div className={styles.welcomeMessage}>
            <div className={styles.welcomeTitle}>
              Welcome to the Intelligent Personal Agent
            </div>
            <div className={styles.welcomeSubtitle}>
              I can help you with calculations, currency conversion, weather info, and web searches.
              Try one of these suggestions:
            </div>
            <div className={styles.suggestions}>
              {SAMPLE_PROMPTS.map((prompt, index) => (
                <Button
                  key={index}
                  appearance="outline"
                  size="small"
                  className={styles.suggestionButton}
                  onClick={() => handleSuggestion(prompt)}
                >
                  {prompt}
                </Button>
              ))}
            </div>
          </div>
        )}

        {/* Message Bubbles */}
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {/* Loading Indicator */}
        {isLoading && (
          <div className={styles.loadingContainer}>
            <Spinner size="tiny" />
            <Text>Agent is thinking...</Text>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* Error Display */}
      {error && (
        <div className={styles.errorContainer}>
          <ErrorCircle24Regular />
          <Text className={styles.errorText}>{error}</Text>
        </div>
      )}

      {/* Input Area */}
      <div className={styles.inputContainer}>
        <div className={styles.inputWrapper}>
          <Input
            ref={inputRef}
            className={styles.input}
            placeholder="Type your message..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
            size="large"
          />
          <Button
            className={styles.sendButton}
            appearance="primary"
            icon={<Send24Filled />}
            onClick={() => handleSend()}
            disabled={!inputValue.trim() || isLoading}
            size="large"
          >
            Send
          </Button>
        </div>
      </div>
    </div>
  );
}

export default ChatWindow;
