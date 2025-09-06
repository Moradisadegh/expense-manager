# app.py - سیستم مدیریت هوشمند هزینه‌ها (نسخه اصلاح شده)
from flask import Flask, request, jsonify, render_template_string
import json
import sqlite3
import os
import re
import requests
from datetime import datetime, timedelta
import uuid
import logging

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مدیریت هوشمند هزینه‌ها</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            margin: 15px 0;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .header {
            text-align: center;
            background: linear-gradient(135deg, #2c3e50, #8e44ad);
            color: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #27ae60;
            margin-left: 10px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            border-left: 4px solid;
        }
        
        .stat-card.income { border-left-color: #27ae60; }
        .stat-card.expense { border-left-color: #e74c3c; }
        .stat-card.total { border-left-color: #3498db; }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        
        .btn {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            margin: 5px;
            transition: all 0.3s ease;
            font-weight: bold;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(52, 152, 219, 0.3);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #27ae60, #2ecc71);
        }
        
        .btn-warning {
            background: linear-gradient(135deg, #f39c12, #e67e22);
        }
        
        .sms-input {
            width: 100%;
            min-height: 120px;
            padding: 15px;
            border: 2px solid #ecf0f1;
            border-radius: 10px;
            margin: 15px 0;
            font-family: inherit;
            font-size: 14px;
            resize: vertical;
            transition: border-color 0.3s ease;
        }
        
        .sms-input:focus {
            border-color: #3498db;
            outline: none;
        }
        
        .result-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            border-right: 5px solid #3498db;
        }
        
        .result-card.income { border-right-color: #27ae60; }
        .result-card.expense { border-right-color: #e74c3c; }
        
        .transaction-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .transaction-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            margin: 8px 0;
            background: #f8f9fa;
            border-radius: 8px;
            border-right: 4px solid;
            transition: transform 0.2s ease;
        }
        
        .transaction-item:hover {
            transform: translateX(-5px);
        }
        
        .transaction-item.income { border-right-color: #27ae60; }
        .transaction-item.expense { border-right-color: #e74c3c; }
        
        .transaction-details {
            flex: 1;
        }
        
        .transaction-amount {
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .transaction-amount.income { color: #27ae60; }
        .transaction-amount.expense { color: #e74c3c; }
        
        .transaction-meta {
            font-size: 0.8em;
            color: #7f8c8d;
            margin-top: 5px;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #7f8c8d;
        }
        
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid;
        }
        
        .alert-success {
            background: #d4edda;
            border-left-color: #28a745;
            color: #155724;
        }
        
        .alert-info {
            background: #d1ecf1;
            border-left-color: #17a2b8;
            color: #0c5460;
        }
        
        @media (max-width: 768px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-wallet"></i> مدیریت هوشمند هزینه‌ها</h1>
            <span class="status-indicator"></span>
            <p>سیستم آنلاین و آماده استفاده</p>
        </div>
        
        <!-- آمار کلی -->
        <div class="card">
            <h3><i class="fas fa-chart-bar"></i> آمار کلی</h3>
            <div class="stats-grid" id="statsGrid">
                <div class="stat-card total">
                    <div class="stat-value" id="totalTransactions">0</div>
                    <div class="stat-label">تعداد تراکنش‌ها</div>
                </div>
                <div class="stat-card income">
                    <div class="stat-value" id="totalIncome">0</div>
                    <div class="stat-label">کل درآمد (تومان)</div>
                </div>
                <div class="stat-card expense">
                    <div class="stat-value" id="totalExpense">0</div>
                    <div class="stat-label">کل هزینه (تومان)</div>
                </div>
            </div>
        </div>
        
        <!-- تحلیل SMS -->
        <div class="card">
            <h3><i class="fas fa-sms"></i> تحلیل پیامک بانکی</h3>
            
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i>
                <strong>راهنما:</strong> متن پیامک بانکی را در کادر زیر وارد کنید و روی "تحلیل پیامک" کلیک کنید.
            </div>
            
            <textarea class="sms-input" id="smsText" placeholder="مثال: کارت شما به مبلغ 125,000 ریال بابت خرید از فروشگاه پردیس بدهکار گردید. موجودی: 2,500,000 ریال"></textarea>
            
            <div style="text-align: center;">
                <button class="btn btn-success" onclick="analyzeSMS()">
                    <i class="fas fa-search"></i> تحلیل پیامک
                </button>
                <button class="btn btn-warning" onclick="loadSample()">
                    <i class="fas fa-file-text"></i> بارگذاری نمونه
                </button>
                <button class="btn" onclick="clearInput()">
                    <i class="fas fa-times"></i> پاک کردن
                </button>
            </div>
            
            <div id="analysisResult"></div>
        </div>
        
        <!-- تراکنش‌ها -->
        <div class="card">
            <h3><i class="fas fa-history"></i> تراکنش‌های اخیر</h3>
            <div class="transaction-list" id="transactionsList">
                <div class="loading">
                    <i class="fas fa-spinner fa-spin"></i> بارگذاری...
                </div>
            </div>
        </div>
    </div>

    <script>
        let transactions = [];

        // بارگذاری اولیه
        window.addEventListener('load', function() {
            loadTransactions();
            loadStats();
        });

        async function analyzeSMS() {
            const text = document.getElementById('smsText').value.trim();
            if (!text) {
                alert('لطفاً متن پیامک را وارد کنید');
                return;
            }

            try {
                showLoading('analysisResult', 'در حال تحلیل...');
                
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ sms_text: text })
                });
                
                const result = await response.json();
                displayAnalysisResult(result);
                
                // بروزرسانی لیست و آمار
                await loadTransactions();
                await loadStats();
                
            } catch (error) {
                document.getElementById('analysisResult').innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle"></i>
                        خطا در تحلیل: ${error.message}
                    </div>
                `;
            }
        }

        function displayAnalysisResult(result) {
            if (result.status !== 'success') {
                document.getElementById('analysisResult').innerHTML = `
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle"></i>
                        متن پیامک قابل تحلیل نیست
                    </div>
                `;
                return;
            }

            const typeText = result.type === 'income' ? 'درآمد' : 'هزینه';
            const typeIcon = result.type === 'income' ? 'fa-arrow-up' : 'fa-arrow-down';
            
            document.getElementById('analysisResult').innerHTML = `
                <div class="result-card ${result.type}">
                    <h4><i class="fas ${typeIcon}"></i> نتیجه تحلیل</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px;">
                        <div>
                            <strong>مبلغ:</strong> ${result.amount.toLocaleString()} تومان
                        </div>
                        <div>
                            <strong>نوع:</strong> ${typeText}
                        </div>
                        <div>
                            <strong>دسته:</strong> ${result.category}
                        </div>
                        <div>
                            <strong>توضیحات:</strong> ${result.description}
                        </div>
                    </div>
                </div>
            `;
        }

        async function loadTransactions() {
            try {
                const response = await fetch('/api/transactions');
                transactions = await response.json();
                displayTransactions();
            } catch (error) {
                console.error('خطا در بارگذاری تراکنش‌ها:', error);
            }
        }

        function displayTransactions() {
            const listDiv = document.getElementById('transactionsList');
            
            if (transactions.length === 0) {
                listDiv.innerHTML = `
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle"></i>
                        هنوز تراکنشی ثبت نشده است. از قسمت "تحلیل پیامک" شروع کنید.
                    </div>
                `;
                return;
            }
            
            listDiv.innerHTML = transactions.slice(0, 10).map(transaction => {
                const typeIcon = transaction.type === 'income' ? 'fa-arrow-up' : 'fa-arrow-down';
                const date = new Date(transaction.timestamp).toLocaleDateString('fa-IR');
                const time = new Date(transaction.timestamp).toLocaleTimeString('fa-IR');
                
                return `
                    <div class="transaction-item ${transaction.type}">
                        <div class="transaction-details">
                            <div class="transaction-amount ${transaction.type}">
                                <i class="fas ${typeIcon}"></i>
                                ${transaction.amount.toLocaleString()} تومان
                            </div>
                            <div>${transaction.description}</div>
                            <div class="transaction-meta">
                                <i class="fas fa-tag"></i> ${transaction.category} • 
                                <i class="fas fa-calendar"></i> ${date} • 
                                <i class="fas fa-clock"></i> ${time}
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        }

        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                document.getElementById('totalTransactions').textContent = stats.total_transactions || 0;
                document.getElementById('totalIncome').textContent = (stats.total_income || 0).toLocaleString();
                document.getElementById('totalExpense').textContent = (stats.total_expense || 0).toLocaleString();
                
            } catch (error) {
                console.error('خطا در بارگذاری آمار:', error);
            }
        }

        function loadSample() {
            const samples = [
                'کارت شما به مبلغ 125,000 ریال بابت خرید از فروشگاه پردیس بدهکار گردید. موجودی: 2,500,000 ریال',
                'حساب شما به مبلغ 50,000 تومان بابت خرید از کافه نادری بدهکار گردید',
                'حساب شما به مبلغ 1,500,000 ریال بابت واریز حقوق بستانکار گردید',
                'حساب شما به مبلغ 85,000 تومان بابت خرید از داروخانه صبا بدهکار شد'
            ];
            
            const randomSample = samples[Math.floor(Math.random() * samples.length)];
            document.getElementById('smsText').value = randomSample;
        }

        function clearInput() {
            document.getElementById('smsText').value = '';
            document.getElementById('analysisResult').innerHTML = '';
        }

        function showLoading(elementId, message) {
            document.getElementById(elementId).innerHTML = `
                <div class="loading">
                    <i class="fas fa-spinner fa-spin"></i> ${message}
                </div>
            `;
        }
    </script>
</body>
</html>
'''

# Database initialization
def init_db():
    """Initialize SQLite database with error handling"""
    try:
        conn = sqlite3.connect('transactions.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                balance REAL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                original_text TEXT,
                transaction_id TEXT UNIQUE
            )
        ''')
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")

# Health Check Route برای Railway
@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    try:
        # بررسی اتصال دیتابیس
        conn = sqlite3.connect('transactions.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM transactions')
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'service': 'expense-manager',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

# Routes with better error handling
@app.route('/')
def index():
    """Main page with error handling"""
    try:
        return render_template_string(HTML_TEMPLATE)
    except Exception as e:
        logger.error(f"Error serving main page: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_sms():
    """Analyze SMS with improved error handling"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'Invalid JSON data'}), 400
            
        sms_text = data.get('sms_text', '').strip()
        
        if not sms_text:
            return jsonify({'status': 'error', 'message': 'متن پیامک خالی است'}), 400
        
        result = parse_banking_sms(sms_text)
        
        if result['status'] == 'success' and result.get('amount', 0) > 0:
            transaction_id = save_transaction(result, sms_text)
            if transaction_id:
                result['transaction_id'] = transaction_id
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_sms: {e}")
        return jsonify({'status': 'error', 'message': 'خطا در پردازش درخواست'}), 500

@app.route('/api/transactions')
def get_transactions():
    """Get transactions with error handling"""
    try:
        conn = sqlite3.connect('transactions.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 50')
        
        transactions = []
        for row in cursor.fetchall():
            transactions.append({
                'id': row[0],
                'amount': float(row[1]) if row[1] else 0,
                'balance': float(row[2]) if row[2] else None,
                'type': row[3] or 'unknown',
                'category': row[4] or 'متفرقه',
                'description': row[5] or 'تراکنش بانکی',
                'timestamp': row[6],
                'original_text': row[7]
            })
        
        conn.close()
        return jsonify(transactions)
        
    except Exception as e:
        logger.error(f"Error getting transactions: {e}")
        return jsonify([]), 200

@app.route('/api/stats')
def get_stats():
    """Get statistics with error handling"""
    try:
        conn = sqlite3.connect('transactions.db')
        cursor = conn.cursor()
        
        # آمار کلی
        cursor.execute('SELECT COUNT(*) FROM transactions')
        total_transactions = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = "income"')
        total_income = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = "expense"')
        total_expense = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return jsonify({
            'total_transactions': int(total_transactions),
            'total_income': float(total_income),
            'total_expense': float(total_expense),
            'balance': float(total_income - total_expense)
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({
            'total_transactions': 0,
            'total_income': 0,
            'total_expense': 0,
            'balance': 0
        })

# Helper functions
def parse_banking_sms(text):
    """Parse banking SMS with improved error handling"""
    try:
        # الگوهای مختلف برای استخراج مبلغ
        amount_patterns = [
            r'(\d{1,3}(?:,\d{3})*)\s*(?:ریال|تومان)',
            r'مبلغ\s*(\d{1,3}(?:,\d{3})*)',
            r'(\d{1,3}(?:,\d{3})*)\s*ریال',
            r'(\d{1,3}(?:,\d{3})*)\s*تومان'
        ]
        
        amount = 0
        for pattern in amount_patterns:
            matches = re.findall(pattern, text)
            if matches:
                amount_str = matches[0].replace(',', '')
                amount = int(amount_str)
                break
        
        if amount == 0:
            return {'status': 'error', 'message': 'مبلغ یافت نشد'}
        
        # تشخیص نوع تراکنش
        trans_type = 'expense'  # پیش‌فرض
        if any(word in text for word in ['بستانکار', 'واریز', 'افزایش', 'درآمد']):
            trans_type = 'income'
        elif any(word in text for word in ['بدهکار', 'برداشت', 'خرید', 'کاهش']):
            trans_type = 'expense'
        
        # دسته‌بندی
        category = categorize_transaction(text)
        
        # توضیحات
        description = generate_description(text, trans_type)
        
        return {
            'status': 'success',
            'amount': amount,
            'type': trans_type,
            'category': category,
            'description': description
        }
        
    except Exception as e:
        logger.error(f"Error parsing SMS: {e}")
        return {'status': 'error', 'message': f'خطا در تحلیل: {str(e)}'}

def categorize_transaction(text):
    """Categorize transaction based on text"""
    try:
        categories = {
            'خوراکی': ['کافه', 'رستوران', 'فست فود', 'نان', 'شیرینی', 'غذا'],
            'خرید': ['فروشگاه', 'سوپرمارکت', 'بازار', 'مغازه', 'خرید'],
            'حمل‌ونقل': ['تاکسی', 'اتوبوس', 'مترو', 'بنزین', 'سوخت'],
            'بهداشت': ['داروخانه', 'دکتر', 'بیمارستان', 'پزشک'],
            'درآمد': ['حقوق', 'دستمزد', 'واریز', 'درآمد'],
        }
        
        text_lower = text.lower()
        
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return 'متفرقه'
    except:
        return 'متفرقه'

def generate_description(text, trans_type):
    """Generate description for transaction"""
    try:
        if 'فروشگاه' in text:
            return 'خرید از فروشگاه'
        elif 'کافه' in text:
            return 'خرید از کافه'
        elif 'داروخانه' in text:
            return 'خرید از داروخانه'
        elif 'حقوق' in text:
            return 'دریافت حقوق'
        elif 'واریز' in text:
            return 'واریز وجه'
        else:
            return 'تراکنش بانکی' if trans_type == 'expense' else 'درآمد'
    except:
        return 'تراکنش بانکی'

def save_transaction(transaction, original_text):
    """Save transaction with error handling"""
    try:
        conn = sqlite3.connect('transactions.db')
        cursor = conn.cursor()
        
        transaction_id = str(uuid.uuid4())
        
        cursor.execute('''
            INSERT INTO transactions 
            (amount, type, category, description, original_text, transaction_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            transaction.get('amount', 0),
            transaction.get('type', 'unknown'),
            transaction.get('category', 'متفرقه'),
            transaction.get('description', 'تراکنش'),
            original_text,
            transaction_id
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Transaction saved with ID: {transaction_id}")
        return transaction_id
        
    except sqlite3.IntegrityError:
        logger.warning("Duplicate transaction ignored")
        return None
    except Exception as e:
        logger.error(f"Error saving transaction: {e}")
        return None

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Initialize database on startup
try:
    init_db()
    logger.info("Application started successfully")
except Exception as e:
    logger.error(f"Startup error: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting app on port {port}")
    
    app.run(
        host='0.0.0.0', 
        port=port, 
        debug=debug_mode,
        threaded=True
    )
