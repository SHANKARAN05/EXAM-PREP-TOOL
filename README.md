# Placement Training Application

A comprehensive web-based application for BE students to prepare for placements with study and exam modes covering Java, Networks, and Operating Systems.

## Features

### Study Mode
- View all questions with answers and explanations
- Filter by topic and question type
- Search functionality
- Mark questions as reviewed
- Pagination support

### Exam Mode
- Timed exams (1 minute per question)
- Random question selection
- Choose number of questions (10/20/30)
- Navigation between questions
- Auto-submit on timeout
- MCQ and theory questions

### Combined Exam Mode
- Questions from all three subjects
- Equal distribution across subjects
- Subject-wise score breakdown

### Results & Review
- Detailed score display
- Performance analysis
- Review wrong answers with explanations
- Subject-wise breakdown for combined exams

## Project Structure

```
placement_prep/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Dependencies
├── init_db.py                  # Database initialization
├── data/                       # Source files (already present)
│   ├── JAVA Q and A.txt
│   ├── java Q.txt
│   ├── Fresher Networking Interview.docx
│   ├── Basic Networking Questions.docx
│   └── Operating System Interview Q.docx
├── parser/                     # File parsers
│   ├── __init__.py
│   ├── java_parser.py
│   ├── network_parser.py
│   └── os_parser.py
├── models/                     # Database models
│   ├── __init__.py
│   └── database.py
├── routes/                     # Flask routes
│   ├── __init__.py
│   ├── home.py
│   ├── study.py
│   ├── exam.py
│   └── results.py
├── templates/                  # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── study.html
│   ├── exam.html
│   ├── result.html
│   └── review.html
└── static/                     # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── exam.js
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database

This will parse all data files and populate the database:

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
Parsed X questions from Fresher Networking Interview.docx
Parsed Y questions from Basic Networking Questions.docx
✓ Loaded Z Network questions

==================================================
Parsing OS files...
==================================================
Parsed X questions from Operating System Interview Q.docx
✓ Loaded Z OS questions

==================================================
DATABASE INITIALIZATION COMPLETE
==================================================
Java: X questions
Networks: Y questions
Operating System: Z questions

Total: N questions loaded successfully!
```

### Step 3: Run the Application

```bash
python app.py
```

The application will start at: **http://127.0.0.1:5000**

## Usage Guide

### Home Page
- View all subjects with question counts
- Access study mode or exam mode for each subject
- Start combined exam

### Study Mode
1. Select a subject from the navbar or home page
2. Use filters to narrow down questions:
   - Filter by topic
   - Filter by question type (MCQ, Theory, Output, Coding)
   - Search by keywords
3. Review questions with answers and explanations
4. Mark questions as reviewed (stored in browser)

### Exam Mode
1. Select a subject or combined exam
2. Enter your name
3. Choose number of questions (10/20/30)
4. Start the exam
5. Answer questions within the time limit
6. Navigate using Previous/Next buttons or arrow keys
7. Submit exam or wait for auto-submit

### Results & Review
1. View your score and percentage
2. See subject-wise breakdown (for combined exams)
3. Review all answers
4. Focus on wrong answers with correct explanations
5. Retake exam or return home

## Database Schema

### Tables

**subjects**
- id (INTEGER PRIMARY KEY)
- name (TEXT)

**questions**
- id (INTEGER PRIMARY KEY)
- subject_id (INTEGER FK)
- question_type (TEXT) - mcq, theory, output, coding
- question (TEXT)
- option_a, option_b, option_c, option_d (TEXT, nullable)
- answer (TEXT)
- explanation (TEXT, nullable)
- topic (TEXT)

**exam_sessions**
- id (INTEGER PRIMARY KEY)
- student_name (TEXT)
- subject (TEXT)
- score (INTEGER)
- total (INTEGER)
- timestamp (DATETIME)

**exam_answers**
- id (INTEGER PRIMARY KEY)
- session_id (INTEGER FK)
- question_id (INTEGER FK)
- selected_answer (TEXT)
- is_correct (BOOLEAN)

## Color Theme

- **Java**: Blue (#2196F3)
- **Networks**: Green (#4CAF50)
- **Operating System**: Orange (#FF9800)
- **Combined**: Purple (#9C27B0)

## Technologies Used

- **Backend**: Flask 3.0.0
- **Database**: SQLite with SQLAlchemy
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Document Parsing**: python-docx
- **Icons**: Bootstrap Icons

## Features Breakdown

### Study Mode Features
✓ Display all questions with answers
✓ Filter by topic dropdown
✓ Filter by question type
✓ Search functionality
✓ Pagination (20 questions per page)
✓ MCQ with highlighted correct answer
✓ Theory questions with full answers
✓ Mark as reviewed (localStorage)

### Exam Mode Features
✓ Student name input
✓ Question count selection (10/20/30)
✓ Timer (1 minute per question)
✓ Random question selection
✓ MCQ with radio buttons
✓ Text area for theory/output/coding
✓ Progress bar
✓ Previous/Next navigation
✓ Auto-submit on timeout
✓ Score calculation
✓ Result page with breakdown

### Combined Exam Features
✓ Equal distribution from all subjects
✓ Shuffled questions
✓ Subject badges on questions
✓ Subject-wise score breakdown

## Troubleshooting

### Database Issues
If you encounter database errors, reinitialize:
```bash
python init_db.py
```

### Missing Dependencies
Reinstall requirements:
```bash
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
Change the port in app.py:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

## Future Enhancements

- User authentication and profiles
- Progress tracking over time
- Difficulty levels
- Bookmarking questions
- Export results to PDF
- Admin panel for question management
- Mobile app version

## License

This project is created for educational purposes for BE students preparing for placements.

## Support

For issues or questions, please refer to the documentation or contact the development team.

---

**Happy Learning! Good Luck with Your Placements! 🎓**
