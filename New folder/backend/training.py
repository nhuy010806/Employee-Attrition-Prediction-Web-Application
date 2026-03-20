import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import StratifiedKFold, cross_val_score
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from joblib import dump

def engineer_features(df):
    df_copy = df.copy()
    
    df_copy["CareerStage"] = pd.cut(
        df_copy["TotalWorkingYears"],
        bins=[-1, 5, 10, 20, 40], 
        labels=["Early", "Mid", "Senior", "Veteran"]
    ).astype(str)

    # Issue 3: Xử lý an toàn OverTime
    if "OverTime" in df_copy.columns:
        df_copy["OverTimeFlag"] = (df_copy["OverTime"] == "Yes").astype(int)
    else:
        df_copy["OverTimeFlag"] = 0
        
    df_copy["CommuteStress"] = df_copy.get("DistanceFromHome", 0) * df_copy["OverTimeFlag"]
    df_copy["PromotionDelayRatio"] = df_copy.get("YearsSinceLastPromotion", 0) / (df_copy.get("YearsAtCompany", 0) + 1)
    df_copy["StagnationIndex"] = df_copy.get("YearsInCurrentRole", 0) - df_copy.get("YearsSinceLastPromotion", 0)

    cols_to_drop = ["id", "Unnamed: 0", "EmployeeCount", "Over18", "StandardHours", "source", "MonthlyIncome"]
    df_copy = df_copy.drop(columns=[c for c in cols_to_drop if c in df_copy.columns], errors='ignore')
    
    return df_copy

def main():
    print("1. Loading data...")
    df = pd.read_csv('attrition train.csv')
    
    # Xử lý label y thành dạng số (nếu nó đang là Yes/No)
    y = df["Attrition"]
    if y.dtype == 'object':
        y = (y == 'Yes').astype(int)
        
    X = df.drop(columns=["Attrition"], errors='ignore')

    print("2. Engineering features...")
    X = engineer_features(X)

    # Issue 2: Loại bỏ 'nan' cứng khỏi categories
    ordinal_cols = ["CareerStage"]
    career_order = ["Early", "Mid", "Senior", "Veteran"] 
    categorical_cols = ["BusinessTravel", "Department", "EducationField", "Gender", "JobRole", "MaritalStatus", "OverTime"]
    numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

    print("3. Building pipeline...")
    preprocessor = ColumnTransformer(
        transformers=[
            # Issue 7: numeric_cols được tạo sau khi engineer_features, nên các feature mới đã được Scale tự động
            ("num", StandardScaler(), numeric_cols),
            ("ord", OrdinalEncoder(categories=[career_order], handle_unknown='use_encoded_value', unknown_value=-1), ordinal_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
        ]
    )

    # Issue 9: Tính dynamic scale_pos_weight
    dynamic_scale_pos_weight = (y == 0).sum() / (y == 1).sum()
    print(f"   -> Tự động tính toán scale_pos_weight = {dynamic_scale_pos_weight:.2f}")

    xgb_params = {
        'n_estimators': 400,
        'max_depth': 3,
        'learning_rate': 0.033,
        'min_child_weight': 4,
        'subsample': 0.7,
        'colsample_bytree': 0.3,
        'scale_pos_weight': dynamic_scale_pos_weight, 
        'eval_metric': 'logloss',
        'random_state': 42
    }

    pipeline = ImbPipeline(steps=[
        ('preprocessor', preprocessor),
        ('smote', SMOTE(random_state=42)),
        ('model', xgb.XGBClassifier(**xgb_params))
    ])

    # Issue 1: Validate bằng Cross-Validation trước khi Fit toàn bộ (Chống Data Leakage)
    print("4. Evaluating model with Cross-Validation (5-Fold)...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(pipeline, X, y, cv=cv, scoring='roc_auc', n_jobs=-1)
    print(f"   -> Trung bình ROC-AUC: {np.mean(scores):.4f} (+/- {np.std(scores):.4f})")

    print("5. Training final model on entire dataset for production...")
    pipeline.fit(X, y)

    dump(pipeline, 'attrition_prediction_model.joblib')
    print("Success! Model saved to attrition_prediction_model.joblib")

if __name__ == "__main__":
    main()