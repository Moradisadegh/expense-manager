from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

# Health check endpoint برای Render
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "App is running!"}), 200

# باقی کد های قبلی شما...
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>مدیریت هزینه‌ها</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Tahoma; direction: rtl; margin: 50px; }
            .form-group { margin: 15px 0; }
            input[type="text"], input[type="number"] { 
                padding: 10px; 
                border: 1px solid #ddd; 
                border-radius: 5px; 
                width: 200px;
                margin: 5px;
            }
            button { 
                padding: 10px 20px; 
                background: #007bff; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer;
                margin: 10px 5px;
            }
            button:hover { background: #0056b3; }
            .result { 
                margin-top: 20px; 
                padding: 15px; 
                background: #f8f9fa; 
                border-radius: 5px; 
            }
        </style>
    </head>
    <body>
        <h1>💰 مدیریت هزینه‌های شخصی</h1>
        
        <div class="form-group">
            <h3>➕ افزودن هزینه جدید</h3>
            <input type="text" id="description" placeholder="توضیحات (مثل: خرید نان)" />
            <input type="number" id="amount" placeholder="مبلغ (تومان)" />
            <button onclick="addExpense()">افزودن هزینه</button>
        </div>
        
        <div class="form-group">
            <h3>📊 مشاهده هزینه‌ها</h3>
            <button onclick="getTotalExpenses()">مجموع هزینه‌ها</button>
            <button onclick="getExpensesByCategory()">هزینه‌ها بر حسب دسته</button>
            <button onclick="getRecentExpenses()">هزینه‌های اخیر</button>
        </div>
        
        <div id="result" class="result" style="display: none;"></div>

        <script>
            const API_BASE = '';

            function addExpense() {
                const description = document.getElementById('description').value;
                const amount = document.getElementById('amount').value;
                
                if (!description || !amount) {
                    alert('لطفاً تمام فیلدها را پر کنید');
                    return;
                }

                fetch('/add_expense', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ description, amount: parseFloat(amount) })
                })
                .then(response => response.json())
                .then(data => {
                    showResult(`✅ ${data.message}`);
                    document.getElementById('description').value = '';
                    document.getElementById('amount').value = '';
                })
                .catch(error => showResult(`❌ خطا: ${error.message}`));
            }

            function getTotalExpenses() {
                fetch('/total_expenses')
                .then(response => response.json())
                .then(data => {
                    showResult(`💰 مجموع هزینه‌ها: ${data.total.toLocaleString()} تومان`);
                })
                .catch(error => showResult(`❌ خطا: ${error.message}`));
            }

            function getExpensesByCategory() {
                fetch('/expenses_by_category')
                .then(response => response.json())
                .then(data => {
                    let result = '<h4>📊 هزینه‌ها بر حسب دسته:</h4>';
                    for (const [category, amount] of Object.entries(data)) {
                        result += `<p>${category}: ${amount.toLocaleString()} تومان</p>`;
                    }
                    showResult(result);
                })
                .catch(error => showResult(`❌ خطا: ${error.message}`));
            }

            function getRecentExpenses() {
                fetch('/recent_expenses')
                .then(response => response.json())
                .then(data => {
                    let result = '<h4>📋 هزینه‌های اخیر:</h4>';
                    data.expenses.forEach(expense => {
                        result += `<p>• ${expense.description}: ${expense.amount.toLocaleString()} تومان</p>`;
                    });
                    showResult(result);
                })
                .catch(error => showResult(`❌ خطا: ${error.message}`));
            }

            function showResult(message) {
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = message;
                resultDiv.style.display = 'block';
            }
        </script>
    </body>
    </html>
    ''')

# متغیر ساده برای نگهداری داده‌ها (در پروژه واقعی از دیتابیس استفاده کنید)
expenses = []

@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    description = data.get('description', '')
    amount = data.get('amount', 0)
    
    # تشخیص ساده دسته‌بندی
    category = categorize_expense(description)
    
    expense = {
        'description': description,
        'amount': amount,
        'category': category
    }
    
    expenses.append(expense)
    
    return jsonify({
        'message': f'هزینه "{description}" به مبلغ {amount:,} تومان اضافه شد',
        'category': category
    })

@app.route('/total_expenses')
def total_expenses():
    total = sum(expense['amount'] for expense in expenses)
    return jsonify({'total': total})

@app.route('/expenses_by_category')
def expenses_by_category():
    categories = {}
    for expense in expenses:
        category = expense['category']
        categories[category] = categories.get(category, 0) + expense['amount']
    return jsonify(categories)

@app.route('/recent_expenses')
def recent_expenses():
    recent = expenses[-10:]  # 10 تای آخر
    return jsonify({'expenses': recent})

def categorize_expense(description):
    """تشخیص ساده دسته‌بندی بر اساس کلمات کلیدی"""
    description = description.lower()
    
    food_keywords = ['نان', 'غذا', 'رستوران', 'خوراکی', 'میوه', 'سبزیجات', 'گوشت', 'مرغ']
    transport_keywords = ['تاکسی', 'اتوبوس', 'مترو', 'بنزین', 'ماشین', 'موتور']
    shopping_keywords = ['خرید', 'لباس', 'کفش', 'پوشاک', 'فروشگاه']
    health_keywords = ['دارو', 'پزشک', 'دکتر', 'درمان', 'بیمارستان']
    
    for keyword in food_keywords:
        if keyword in description:
            return '🍽️ خوراکی'
    
    for keyword in transport_keywords:
        if keyword in description:
            return '🚗 حمل‌ونقل'
    
    for keyword in shopping_keywords:
        if keyword in description:
            return '🛍️ خرید'
    
    for keyword in health_keywords:
        if keyword in description:
            return '🏥 سلامت'
    
    return '📝 متفرقه'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
