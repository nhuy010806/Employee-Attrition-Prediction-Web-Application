from flask import Flask, request, jsonify
import pandas as pd
from joblib import load
from flask_cors import CORS
from training import engineer_features

model = load('./attrition_prediction_model.joblib')
app = Flask(__name__)
CORS(app)

THRESHOLD = 0.45

# Cấu hình các cột BẮT BUỘC phải có từ Frontend
REQUIRED_COLUMNS = [
    "Age", "DistanceFromHome", "OverTime", 
    "TotalWorkingYears", "YearsAtCompany", 
    "YearsInCurrentRole", "YearsSinceLastPromotion"
]

print("Đang đọc file CSV để lấy giá trị mặc định...")
train_df = pd.read_csv('attrition train.csv')
default_values = {}

cols_to_ignore = ['id', 'Attrition', 'Unnamed: 0', 'EmployeeCount', 'Over18', 'StandardHours', 'source', 'MonthlyIncome']

for col in train_df.columns:
    if col not in cols_to_ignore:
        if pd.api.types.is_numeric_dtype(train_df[col]):
            default_values[col] = train_df[col].median()
        else:
            default_values[col] = train_df[col].mode()[0]
            
print("Đã load xong dữ liệu mặc định tự động!")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Kiểm tra missing columns
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in data or data[col] == ""]
        if missing_cols:
            return jsonify({"error": f"Thiếu thông tin bắt buộc: {', '.join(missing_cols)}"}), 400

        df = pd.DataFrame([data])

        # Bơm dữ liệu mặc định
        for col, val in default_values.items():
            if col not in df.columns:
                df[col] = val

        # 1. AI DỰ ĐOÁN (BASE PROBABILITY)
        df_processed = engineer_features(df)
        probs = model.predict_proba(df_processed)[:, 1]
        probability = float(probs[0])

        # =====================================================================
        # 2. HỆ THỐNG LUẬT KINH DOANH (BUSINESS RULES ENGINE)
        # Bắt các trường hợp cực đoan (Outliers) mà AI không thể tự hiểu
        # =====================================================================
        distance = float(data.get("DistanceFromHome", 0))
        years_no_promo = float(data.get("YearsSinceLastPromotion", 0))
        years_in_role = float(data.get("YearsInCurrentRole", 0))

        # Phạt nặng nếu đi làm quá xa (vượt ngưỡng chịu đựng của con người)
        if distance > 100:
            probability += 0.6  # Cộng thẳng 60% nguy cơ nghỉ việc
        elif distance > 50:
            probability += 0.3  # Cộng 30% nguy cơ
            
        # Phạt nặng nếu ở công ty lâu mà không được thăng chức
        if years_no_promo >= 10:
            probability += 0.5  # Cộng thẳng 50% nguy cơ
        elif years_no_promo >= 5 and years_in_role >= 5:
            probability += 0.25 # Stagnation (Đóng băng sự nghiệp)

        # Đảm bảo xác suất tối đa chỉ là 99% (không vượt quá 1.0)
        probability = min(probability, 0.99)
        # =====================================================================

        # 3. CHỐT KẾT QUẢ CUỐI CÙNG
        prediction_label = 1 if probability >= THRESHOLD else 0

        print(f"Predicted Probability (After Rules): {probability:.4f} => Label: {prediction_label}")

        return jsonify({
            "attrition": int(prediction_label),
            "probability": probability
        }), 200

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Welcome to the HR Attrition Prediction API"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)