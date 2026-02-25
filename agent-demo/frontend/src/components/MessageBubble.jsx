import React from 'react';
import {
  makeStyles,
  tokens,
  Text,
  Card,
} from '@fluentui/react-components';
import {
  Person24Regular,
  Bot24Regular,
  Wrench24Regular,
} from '@fluentui/react-icons';

/**
 * Styles for message bubbles.
 */
const useStyles = makeStyles({
  container: {
    display: 'flex',
    gap: '12px',
    padding: '8px 0',
    maxWidth: '80%',
  },
  userContainer: {
    alignSelf: 'flex-end',
    flexDirection: 'row-reverse',
  },
  agentContainer: {
    alignSelf: 'flex-start',
  },
  avatar: {
    width: '36px',
    height: '36px',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0,
  },
  userAvatar: {
    backgroundColor: tokens.colorBrandBackground,
    color: tokens.colorNeutralForegroundOnBrand,
  },
  agentAvatar: {
    backgroundColor: tokens.colorPaletteGreenBackground2,
    color: tokens.colorPaletteGreenForeground2,
  },
  bubble: {
    padding: '12px 16px',
    borderRadius: '12px',
    maxWidth: '100%',
    wordWrap: 'break-word',
  },
  userBubble: {
    backgroundColor: tokens.colorBrandBackground,
    color: tokens.colorNeutralForegroundOnBrand,
    borderBottomRightRadius: '4px',
  },
  agentBubble: {
    backgroundColor: tokens.colorNeutralBackground1,
    color: tokens.colorNeutralForeground1,
    borderBottomLeftRadius: '4px',
    boxShadow: tokens.shadow4,
  },
  messageText: {
    whiteSpace: 'pre-wrap',
    lineHeight: '1.5',
  },
  toolInfo: {
    marginTop: '8px',
    padding: '8px 12px',
    backgroundColor: tokens.colorNeutralBackground3,
    borderRadius: '6px',
    borderLeft: `3px solid ${tokens.colorPaletteBlueBorderActive}`,
  },
  toolHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    marginBottom: '4px',
    color: tokens.colorPaletteBlueForeground2,
    fontWeight: tokens.fontWeightSemibold,
    fontSize: tokens.fontSizeBase200,
  },
  toolOutput: {
    fontSize: tokens.fontSizeBase200,
    color: tokens.colorNeutralForeground2,
    fontFamily: 'monospace',
    whiteSpace: 'pre-wrap',
    maxHeight: '100px',
    overflow: 'auto',
  },
  timestamp: {
    fontSize: tokens.fontSizeBase100,
    color: tokens.colorNeutralForeground4,
    marginTop: '4px',
    textAlign: 'right',
  },
});

/**
 * MessageBubble Component.
 * Displays a single chat message with appropriate styling.
 * 
 * @param {Object} props
 * @param {Object} props.message - The message object
 * @param {string} props.message.role - 'user' or 'agent'
 * @param {string} props.message.content - The message text
 * @param {string} [props.message.toolUsed] - Name of tool used (agent only)
 * @param {string} [props.message.toolOutput] - Output from tool (agent only)
 * @param {Date} [props.message.timestamp] - Message timestamp
 */
function MessageBubble({ message }) {
  const styles = useStyles();
  const isUser = message.role === 'user';
  
  // Format timestamp
  const formatTime = (date) => {
    if (!date) return '';
    return new Date(date).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div
      className={`${styles.container} ${
        isUser ? styles.userContainer : styles.agentContainer
      }`}
    >
      {/* Avatar */}
      <div
        className={`${styles.avatar} ${
          isUser ? styles.userAvatar : styles.agentAvatar
        }`}
      >
        {isUser ? <Person24Regular /> : <Bot24Regular />}
      </div>
      
      {/* Message Bubble */}
      <div
        className={`${styles.bubble} ${
          isUser ? styles.userBubble : styles.agentBubble
        }`}
      >
        {/* Message Content */}
        <Text className={styles.messageText}>{message.content}</Text>
        
        {/* Tool Usage Info (Agent messages only) */}
        {!isUser && message.toolUsed && (
          <div className={styles.toolInfo}>
            <div className={styles.toolHeader}>
              <Wrench24Regular />
              <span>Tool: {message.toolUsed}</span>
            </div>
            {message.toolOutput && (
              <div className={styles.toolOutput}>
                {typeof message.toolOutput === 'string'
                  ? message.toolOutput
                  : JSON.stringify(message.toolOutput, null, 2)}
              </div>
            )}
          </div>
        )}
        
        {/* Timestamp */}
        <div className={styles.timestamp}>
          {formatTime(message.timestamp)}
        </div>
      </div>
    </div>
  );
}

export default MessageBubble;
