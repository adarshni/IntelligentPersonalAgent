import React, { useState, useCallback } from 'react';
import {
  makeStyles,
  tokens,
  Title1,
  Button,
  Divider,
} from '@fluentui/react-components';
import {
  Bot24Regular,
  Delete24Regular,
  Info24Regular,
} from '@fluentui/react-icons';
import ChatWindow from './components/ChatWindow';
import ToolLogPanel from './components/ToolLogPanel';
import { clearChatHistory } from './api';

/**
 * Styles for the main application layout.
 */
const useStyles = makeStyles({
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    backgroundColor: tokens.colorNeutralBackground2,
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '16px 24px',
    backgroundColor: tokens.colorBrandBackground,
    color: tokens.colorNeutralForegroundOnBrand,
    boxShadow: tokens.shadow4,
  },
  headerLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  },
  headerRight: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  headerButton: {
    color: tokens.colorNeutralForegroundOnBrand,
  },
  mainContent: {
    display: 'flex',
    flex: 1,
    overflow: 'hidden',
  },
  chatSection: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    minWidth: 0,
  },
  sidePanel: {
    width: '350px',
    borderLeft: `1px solid ${tokens.colorNeutralStroke1}`,
    backgroundColor: tokens.colorNeutralBackground1,
    display: 'flex',
    flexDirection: 'column',
    '@media (max-width: 900px)': {
      display: 'none',
    },
  },
  footer: {
    padding: '8px 24px',
    backgroundColor: tokens.colorNeutralBackground1,
    borderTop: `1px solid ${tokens.colorNeutralStroke1}`,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    fontSize: tokens.fontSizeBase200,
    color: tokens.colorNeutralForeground3,
  },
});

/**
 * Main Application Component.
 * Provides the layout and state management for the chat interface.
 */
function App() {
  const styles = useStyles();
  
  // State for tool execution logs
  const [toolLogs, setToolLogs] = useState([]);
  
  // State for messages (to allow clearing from header)
  const [messages, setMessages] = useState([]);
  
  /**
   * Handle new tool execution log.
   */
  const handleToolLog = useCallback((log) => {
    setToolLogs((prev) => [...prev, { ...log, timestamp: new Date() }]);
  }, []);
  
  /**
   * Clear all chat history and logs.
   */
  const handleClearChat = useCallback(async () => {
    try {
      await clearChatHistory();
      setMessages([]);
      setToolLogs([]);
    } catch (error) {
      console.error('Failed to clear chat:', error);
    }
  }, []);
  
  /**
   * Clear tool logs only.
   */
  const handleClearLogs = useCallback(() => {
    setToolLogs([]);
  }, []);

  return (
    <div className={styles.container}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerLeft}>
          <Bot24Regular />
          <Title1>Intelligent Personal Agent</Title1>
        </div>
        <div className={styles.headerRight}>
          <Button
            appearance="subtle"
            icon={<Delete24Regular />}
            onClick={handleClearChat}
            className={styles.headerButton}
          >
            Clear Chat
          </Button>
        </div>
      </header>
      
      {/* Main Content */}
      <div className={styles.mainContent}>
        {/* Chat Section */}
        <div className={styles.chatSection}>
          <ChatWindow
            messages={messages}
            setMessages={setMessages}
            onToolLog={handleToolLog}
          />
        </div>
        
        {/* Side Panel - Tool Logs */}
        <div className={styles.sidePanel}>
          <ToolLogPanel logs={toolLogs} onClear={handleClearLogs} />
        </div>
      </div>
      
      {/* Footer */}
      <footer className={styles.footer}>
        <Info24Regular />
        <span>Agentic AI Demo | Built with LangChain + Azure OpenAI + React + Fluent UI</span>
      </footer>
    </div>
  );
}

export default App;
