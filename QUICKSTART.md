# Quick Start Guide

## 3-Step Setup

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Initialize Database
```bash
python init_db.py
```

### 3️⃣ Run Application
```bash
python app.py
```

Then open your browser and go to: **http://127.0.0.1:5000**

---

## What You'll See

### Home Page
- 3 Subject cards (Java, Networks, Operating System)
- Each showing question count
- Buttons for Study Mode and Exam Mode
- Combined Exam option at the bottom

### Study Mode
- All questions with answers visible
- Filters for topic and question type
- Search bar
- MCQs show correct answer highlighted
- Theory questions show full answers

### Exam Mode
1. Enter your name
2. Choose 10, 20, or 30 questions
3. Timer starts (1 min per question)
4. Answer questions
5. Navigate with Previous/Next
6. Submit or auto-submit when time ends
7. See your score
8. Review wrong answers

### Combined Exam
- Questions from all 3 subjects mixed
- Shows which subject each question is from
- Results show breakdown by subject

---

## Keyboard Shortcuts (During Exam)
- **→ (Right Arrow)**: Next question
- **← (Left Arrow)**: Previous question

---

## Tips

✓ Use Study Mode first to learn the material
✓ Mark questions as reviewed to track progress
✓ Start with 10-question exams to practice
✓ Review wrong answers after each exam
✓ Try Combined Exam when confident in all subjects

---

## Troubleshooting

**Problem**: `ModuleNotFoundError`
**Solution**: Run `pip install -r requirements.txt`

**Problem**: No questions showing
**Solution**: Run `python init_db.py` to load questions

**Problem**: Port 5000 already in use
**Solution**: Edit `app.py` and change port to 5001 or another number

---

**Ready to start? Run the 3 commands above! 🚀**
