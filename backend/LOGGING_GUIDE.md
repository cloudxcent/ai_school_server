# AI School Backend - Logging System

## Overview

The AI School Backend Server now includes a comprehensive logging system that captures all traces and operations into session-based log files. Each server session creates a unique log file with detailed information about all activities.

## Features

### ✅ Session-Based Logging
- **Unique log file per session**: Each time the server starts, a new log file is created
- **Session identification**: Files are named with timestamp and process ID
- **Location**: All logs are stored in the `backend/logs/` directory

### ✅ Comprehensive Coverage
- **HTTP Requests & Responses**: All incoming requests and outgoing responses
- **Database Operations**: Azure Table Storage operations (create, read, update, delete)
- **Authentication**: JWT token generation and verification
- **Error Handling**: All exceptions with full stack traces
- **Business Logic**: User registration, login, profile management

### ✅ Security Features
- **Sensitive data redaction**: Passwords, tokens, and API keys are automatically redacted
- **Headers filtering**: Authorization headers are masked in logs
- **Request body filtering**: Sensitive fields in request bodies are redacted

## Log File Structure

### File Naming Convention
```
ai_school_session_YYYYMMDD_HHMMSS_PID.log
```

Example: `ai_school_session_20250822_143052_12480.log`

### Log Entry Format
```
YYYY-MM-DD HH:MM:SS,mmm - LOGGER_NAME - LEVEL - [FILENAME:LINE] - MESSAGE
```

Example:
```
2025-08-22 14:30:52,123 - ai_school - INFO - [app.py:45] - User registration completed successfully: test@example.com
```

## Log Levels

| Level | Description | Usage |
|-------|-------------|-------|
| **DEBUG** | Detailed diagnostic information | Development debugging, detailed flow tracing |
| **INFO** | General information about program execution | Normal operations, successful operations |
| **WARNING** | Something unexpected happened but the program continues | Invalid inputs, authentication failures |
| **ERROR** | Serious problem occurred | Database errors, exceptions, failures |

## What Gets Logged

### 🔐 Authentication & Authorization
- User registration attempts and results
- Login attempts (successful and failed)
- JWT token generation and verification
- Authorization failures

### 👥 User Management
- User creation and profile updates
- Database queries and results
- Password hashing operations (password values are redacted)

### 👶 Kids Profile Management
- Profile creation, updates, and deletions
- Profile queries and results
- Validation errors and data changes

### 🌐 HTTP Layer
- All incoming requests (method, URL, headers, body)
- All outgoing responses (status code, headers)
- Request routing and processing

### 🗄️ Database Operations
- Azure Table Storage connections and operations
- Entity creation, updates, queries, and deletions
- Connection errors and retries

### 🚨 Error Handling
- All exceptions with full stack traces
- 404 and 500 error responses
- Validation failures and business logic errors

## Configuration

### Environment Variables
The logging system uses the following configuration:
- **Log Level**: DEBUG (captures all activities)
- **Output**: Both file and console
- **File Encoding**: UTF-8
- **Rotation**: New file per session

### File Locations
```
backend/
├── app.py              # Main application with logging
├── logs/               # Log files directory
│   ├── ai_school_session_20250822_143052_12480.log
│   ├── ai_school_session_20250822_144125_15248.log
│   └── ...
└── test_logging.py     # Test script for logging functionality
```

## Usage Examples

### Starting the Server
```bash
cd backend
python app.py
```

The server will automatically:
1. Create the `logs/` directory if it doesn't exist
2. Generate a unique session ID
3. Create a new log file for this session
4. Log the session start information

### Testing Logging
Use the included test script to generate various log entries:
```bash
cd backend
python test_logging.py
```

### Viewing Logs
```bash
# View the latest log file
cd backend/logs
ls -la

# View real-time logs (Windows)
Get-Content ai_school_session_*.log -Tail 50 -Wait

# View real-time logs (Linux/Mac)
tail -f ai_school_session_*.log
```

## Sample Log Output

```
2025-08-22 14:30:52,123 - ai_school - INFO - [app.py:45] - === AI School Backend Server Session Started ===
2025-08-22 14:30:52,124 - ai_school - INFO - [app.py:46] - Session ID: session_20250822_143052_12480
2025-08-22 14:30:52,125 - ai_school - INFO - [app.py:47] - Log file: D:\AI School App for TV and Mobile\ai_school\backend\logs\ai_school_session_20250822_143052_12480.log
2025-08-22 14:30:52,126 - ai_school - INFO - [app.py:48] - Process ID: 12480
2025-08-22 14:30:52,127 - ai_school - INFO - [app.py:49] - Python version: 3.13.0

2025-08-22 14:30:53,045 - ai_school - INFO - [app.py:250] - === INCOMING REQUEST ===
2025-08-22 14:30:53,046 - ai_school - INFO - [app.py:251] - Method: POST
2025-08-22 14:30:53,047 - ai_school - INFO - [app.py:252] - URL: http://localhost:5000/api/auth/register
2025-08-22 14:30:53,048 - ai_school - INFO - [app.py:253] - Remote Address: 127.0.0.1

2025-08-22 14:30:53,156 - ai_school - INFO - [app.py:352] - User registration attempt started
2025-08-22 14:30:53,157 - ai_school - INFO - [app.py:367] - Registration attempt for email: test@example.com
2025-08-22 14:30:53,234 - ai_school - INFO - [app.py:145] - Creating new user: test@example.com
2025-08-22 14:30:53,456 - ai_school - INFO - [app.py:162] - User created successfully: test@example.com (ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890)
```

## Maintenance

### Log File Cleanup
Log files will accumulate over time. Consider implementing a cleanup strategy:

```bash
# Keep only logs from last 30 days
find backend/logs -name "*.log" -mtime +30 -delete

# Keep only the latest 10 log files
cd backend/logs && ls -t *.log | tail -n +11 | xargs rm --
```

### Log Analysis
For log analysis, you can use tools like:
- `grep` for searching specific patterns
- `awk` for extracting specific fields
- Log analysis tools like ELK Stack for advanced analysis

## Security Considerations

1. **Sensitive Data**: Passwords, tokens, and API keys are automatically redacted
2. **Access Control**: Ensure log files have appropriate file permissions
3. **Retention**: Implement log rotation and cleanup policies
4. **Privacy**: Be mindful of personally identifiable information in logs

## Troubleshooting

### Log File Not Created
- Check if the `backend/logs/` directory exists and is writable
- Verify file permissions
- Check for disk space issues

### Missing Log Entries
- Ensure the logging level is set to DEBUG or INFO
- Check if the logger is properly initialized
- Verify there are no exceptions during logger setup

### Performance Impact
- Logging is asynchronous and should have minimal performance impact
- For high-traffic scenarios, consider using a separate logging service
- Monitor disk I/O if logging becomes a bottleneck

## Future Enhancements

- [ ] Log rotation based on file size
- [ ] Structured logging (JSON format)
- [ ] Integration with external logging services
- [ ] Real-time log monitoring dashboard
- [ ] Log aggregation for multiple instances
