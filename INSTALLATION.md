# Installation Guide - Placement Training Application

## Prerequisites

Before you begin, ensure you have:
- **Python 3.8 or higher** installed
- **pip** (Python package manager)
- **Internet connection** (for downloading dependencies)

### Check Python Installation

**Windows:**
```cmd
python --version
```

**Linux/Mac:**
```bash
python3 --version
```

If Python is not installed, download it from: https://www.python.org/downloads/

---

## Installation Methods

### Method 1: Automated Setup (Recommended)

#### Windows
1. Open Command Prompt in the project folder
2. Run:
```cmd
run.bat
```

#### Linux/Mac
1. Open Terminal in the project folder
2. Make script executable:
```bash
chmod +x run.sh
```
3. Run:
```bash
./run.sh
```

The script will:
- Create virtual environment
- Install dependencies
- Initialize database
- Run tests
- Start the application

---

### Method 2: Manual Setup

#### Step 1: Create Virtual Environment (Optional but Recommended)

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- python-docx 1.1.0

#### Step 3: Initialize Database

```bash
python init_db.py
```

Expected output:
```
Dropping existing tables...
Creating new tables...
Subjects created successfully!

==================================================
Parsing Java files...
==================================================
Parsed X questions from JAVA Q and A.txt
Parsed Y questions from java Q.txt
✓ Loaded Z Java questions

==================================================
Parsing Network files...
==================================================
...
✓ Loaded Z Network questions

==================================================
Parsing OS files...
==================================================
...
✓ Loaded Z OS questions

==================================================
DATABASE INITIALIZATION COMPLETE
==================================================
Total: N questions loaded successfully!
```

#### Step 4: Verify Setup (Optional)

```bash
python test_setup.py
```

This will check:
- File structure
- Python imports
- Database connectivity
- Flask routes

#### Step 5: Run Application

```bash
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

#### Step 6: Open in Browser

Navigate to: **http://127.0.0.1:5000**

---

### Method 3: Quick 3-Command Setup

If you're experienced with Python:

```bash
pip install -r requirements.txt
python init_db.py
python app.py
```

Then open: http://127.0.0.1:5000

---

## Verification Checklist

After installation, verify:

- [ ] Home page loads with 3 subject cards
- [ ] Each subject shows question count
- [ ] Study mode displays questions with answers
- [ ] Filters work (topic, type, search)
- [ ] Exam mode accepts name and question count
- [ ] Timer starts during exam
- [ ] Questions can be answered
- [ ] Navigation works (Previous/Next)
- [ ] Exam submits and shows results
- [ ] Review page shows correct/wrong answers
- [ ] Combined exam works with all subjects

---

## Troubleshooting

### Issue: "Python is not recognized"

**Solution:**
- Install Python from python.org
- During installation, check "Add Python to PATH"
- Restart Command Prompt/Terminal

### Issue: "pip is not recognized"

**Solution:**
```bash
python -m ensurepip --upgrade
```

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "No questions showing in Study Mode"

**Solution:**
```bash
python init_db.py
```

### Issue: "Port 5000 is already in use"

**Solution:**
Edit `app.py` (last line):
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

### Issue: "Database is locked"

**Solution:**
- Close any other instances of the application
- Delete `placement_prep.db`
- Run `python init_db.py` again

### Issue: "Permission denied" on Linux/Mac

**Solution:**
```bash
chmod +x run.sh
```

### Issue: Virtual environment activation fails

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

---

## Uninstallation

To remove the application:

1. Deactivate virtual environment (if active):
```bash
deactivate
```

2. Delete the project folder

That's it! No system-wide changes were made.

---

## Updating

To update the application:

1. Pull latest changes (if using Git)
2. Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```
3. Reinitialize database:
```bash
python init_db.py
```

---

## Production Deployment

For production use:

1. **Change Secret Key** in `config.py`:
```python
SECRET_KEY = 'your-secure-random-key-here'
```

2. **Use Production Server** (not Flask development server):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **Use PostgreSQL** instead of SQLite for better performance

4. **Enable HTTPS** using a reverse proxy (nginx/Apache)

5. **Set Debug to False** in `app.py`:
```python
app.run(debug=False)
```

---

## System Requirements

### Minimum
- **OS**: Windows 7+, macOS 10.12+, Linux (any modern distro)
- **RAM**: 512 MB
- **Storage**: 100 MB
- **Python**: 3.8+

### Recommended
- **OS**: Windows 10+, macOS 11+, Ubuntu 20.04+
- **RAM**: 2 GB
- **Storage**: 500 MB
- **Python**: 3.10+
- **Browser**: Chrome, Firefox, Safari, Edge (latest versions)

---

## File Permissions

Ensure the application has:
- **Read** access to `data/` folder
- **Write** access to project root (for database file)
- **Execute** access to Python scripts

---

## Database Location

The SQLite database file is created at:
```
placement_prep/placement_prep.db
```

To backup your data, simply copy this file.

---

## Support & Help

If you encounter issues:

1. **Check this guide** for common solutions
2. **Run test script**: `python test_setup.py`
3. **Check README.md** for detailed documentation
4. **Review error messages** carefully
5. **Ensure all files are present** (see PROJECT_SUMMARY.md)

---

## Next Steps

After successful installation:

1. **Explore Study Mode** to see all questions
2. **Try a 10-question exam** to test the system
3. **Review your answers** to understand the flow
4. **Take Combined Exam** when ready

---

## Development Setup

For developers who want to modify the code:

1. Install development dependencies:
```bash
pip install flask-debugtoolbar
```

2. Enable debug mode (already enabled in app.py)

3. Use browser DevTools for frontend debugging

4. Check Flask logs in terminal for backend issues

---

**Installation complete! Happy learning! 🎓**

For questions or issues, refer to README.md or PROJECT_SUMMARY.md
