import React, { useState } from 'react';
import {
  makeStyles,
  tokens,
  Text,
  Button,
  Card,
  Badge,
} from '@fluentui/react-components';
import {
  Wrench24Regular,
  Delete24Regular,
  ChevronDown24Regular,
  ChevronUp24Regular,
  CheckmarkCircle24Regular,
  DismissCircle24Regular,
} from '@fluentui/react-icons';

/**
 * Styles for the tool log panel.
 */
const useStyles = makeStyles({
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    overflow: 'hidden',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '16px',
    borderBottom: `1px solid ${tokens.colorNeutralStroke1}`,
    backgroundColor: tokens.colorNeutralBackground3,
  },
  headerLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  headerTitle: {
    fontWeight: tokens.fontWeightSemibold,
  },
  badge: {
    marginLeft: '8px',
  },
  logsContainer: {
    flex: 1,
    overflowY: 'auto',
    padding: '12px',
  },
  emptyState: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100%',
    color: tokens.colorNeutralForeground3,
    textAlign: 'center',
    padding: '20px',
  },
  logCard: {
    marginBottom: '12px',
    padding: '12px',
    backgroundColor: tokens.colorNeutralBackground1,
    borderRadius: '8px',
    border: `1px solid ${tokens.colorNeutralStroke2}`,
  },
  logHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    cursor: 'pointer',
  },
  logHeaderLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  toolName: {
    fontWeight: tokens.fontWeightSemibold,
    color: tokens.colorBrandForeground1,
  },
  timestamp: {
    fontSize: tokens.fontSizeBase100,
    color: tokens.colorNeutralForeground4,
  },
  logContent: {
    marginTop: '12px',
    paddingTop: '12px',
    borderTop: `1px solid ${tokens.colorNeutralStroke2}`,
  },
  logSection: {
    marginBottom: '8px',
  },
  logLabel: {
    fontSize: tokens.fontSizeBase200,
    fontWeight: tokens.fontWeightSemibold,
    color: tokens.colorNeutralForeground3,
    marginBottom: '4px',
  },
  logValue: {
    fontSize: tokens.fontSizeBase200,
    fontFamily: 'monospace',
    backgroundColor: tokens.colorNeutralBackground3,
    padding: '8px',
    borderRadius: '4px',
    whiteSpace: 'pre-wrap',
    wordBreak: 'break-word',
    maxHeight: '150px',
    overflowY: 'auto',
  },
  successIcon: {
    color: tokens.colorPaletteGreenForeground1,
  },
  errorIcon: {
    color: tokens.colorPaletteRedForeground1,
  },
});

/**
 * ToolLogPanel Component.
 * Displays a log of all tool executions with expandable details.
 * 
 * @param {Object} props
 * @param {Array} props.logs - Array of tool execution logs
 * @param {Function} props.onClear - Callback to clear logs
 */
function ToolLogPanel({ logs, onClear }) {
  const styles = useStyles();
  const [expandedLogs, setExpandedLogs] = useState({});

  /**
   * Toggle expansion state of a log entry.
   */
  const toggleExpand = (index) => {
    setExpandedLogs((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  /**
   * Format timestamp for display.
   */
  const formatTime = (date) => {
    if (!date) return '';
    return new Date(date).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  };

  return (
    <div className={styles.container}>
      {/* Header */}
      <div className={styles.header}>
        <div className={styles.headerLeft}>
          <Wrench24Regular />
          <Text className={styles.headerTitle}>Tool Execution Logs</Text>
          {logs.length > 0 && (
            <Badge
              className={styles.badge}
              appearance="filled"
              color="informative"
            >
              {logs.length}
            </Badge>
          )}
        </div>
        {logs.length > 0 && (
          <Button
            appearance="subtle"
            icon={<Delete24Regular />}
            size="small"
            onClick={onClear}
          >
            Clear
          </Button>
        )}
      </div>

      {/* Logs Container */}
      <div className={styles.logsContainer}>
        {logs.length === 0 ? (
          <div className={styles.emptyState}>
            <Wrench24Regular />
            <Text style={{ marginTop: '8px' }}>No tool executions yet</Text>
            <Text style={{ fontSize: '12px', marginTop: '4px' }}>
              Tool usage will appear here as the agent works
            </Text>
          </div>
        ) : (
          logs.map((log, index) => (
            <div key={index} className={styles.logCard}>
              {/* Log Header */}
              <div
                className={styles.logHeader}
                onClick={() => toggleExpand(index)}
              >
                <div className={styles.logHeaderLeft}>
                  {log.success ? (
                    <CheckmarkCircle24Regular className={styles.successIcon} />
                  ) : (
                    <DismissCircle24Regular className={styles.errorIcon} />
                  )}
                  <span className={styles.toolName}>{log.tool}</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className={styles.timestamp}>
                    {formatTime(log.timestamp)}
                  </span>
                  {expandedLogs[index] ? (
                    <ChevronUp24Regular />
                  ) : (
                    <ChevronDown24Regular />
                  )}
                </div>
              </div>

              {/* Expanded Content */}
              {expandedLogs[index] && (
                <div className={styles.logContent}>
                  {/* Input */}
                  {log.input && (
                    <div className={styles.logSection}>
                      <div className={styles.logLabel}>Input / Reasoning:</div>
                      <div className={styles.logValue}>
                        {typeof log.input === 'string'
                          ? log.input
                          : JSON.stringify(log.input, null, 2)}
                      </div>
                    </div>
                  )}

                  {/* Output */}
                  {log.output && (
                    <div className={styles.logSection}>
                      <div className={styles.logLabel}>Output:</div>
                      <div className={styles.logValue}>
                        {typeof log.output === 'string'
                          ? log.output
                          : JSON.stringify(log.output, null, 2)}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default ToolLogPanel;
