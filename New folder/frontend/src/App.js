import React, { useState } from "react";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    Age: "", Gender: "", MaritalStatus: "", Department: "",
    BusinessTravel: "", EducationField: "", JobRole: "", OverTime: "",
    DistanceFromHome: "", TotalWorkingYears: "", YearsAtCompany: "",
    YearsInCurrentRole: "", YearsSinceLastPromotion: "",
  });

  // State để lưu kết quả đẹp mắt thay vì dùng alert
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    const parsedValue = type === "number" ? (value === "" ? "" : Number(value)) : value;
    setFormData({ ...formData, [name]: parsedValue });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(null); // Reset lại kết quả khi bấm phân tích mới

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data);
      } else {
        alert(`Lỗi từ server: ${data.error}`);
      }
    } catch (error) {
      alert("Không thể kết nối đến server Backend. Vui lòng kiểm tra lại!");
    }
  };

  return (
    <div className="app-container">
      <h1 className="title">HR Attrition Prediction</h1>

      <div className="form-container">
        <form onSubmit={handleSubmit}>
          
          <div className="form-group">
            <label>Age</label>
            <input type="number" name="Age" onChange={handleChange} required placeholder="VD: 25" />
          </div>

          <div className="form-group">
            <label>Gender</label>
            <select name="Gender" onChange={handleChange} required>
              <option value="">Select Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>

          <div className="form-group">
            <label>Marital Status</label>
            <select name="MaritalStatus" onChange={handleChange} required>
              <option value="">Select</option>
              <option value="Single">Single</option>
              <option value="Married">Married</option>
              <option value="Divorced">Divorced</option>
            </select>
          </div>

          <div className="form-group">
            <label>Department</label>
            <select name="Department" onChange={handleChange} required>
              <option value="">Select Department</option>
              <option value="Sales">Sales</option>
              <option value="Research & Development">R&D</option>
              <option value="Human Resources">Human Resources</option>
            </select>
          </div>

          <div className="form-group">
            <label>Business Travel</label>
            <select name="BusinessTravel" onChange={handleChange} required>
              <option value="">Select Frequency</option>
              <option value="Non-Travel">Non-Travel</option>
              <option value="Travel_Rarely">Travel Rarely</option>
              <option value="Travel_Frequently">Travel Frequently</option>
            </select>
          </div>

          <div className="form-group">
            <label>Education Field</label>
            <select name="EducationField" onChange={handleChange} required>
              <option value="">Select Field</option>
              <option value="Life Sciences">Life Sciences</option>
              <option value="Medical">Medical</option>
              <option value="Marketing">Marketing</option>
              <option value="Technical Degree">Technical Degree</option>
              <option value="Human Resources">Human Resources</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div className="form-group">
            <label>Job Role</label>
            <select name="JobRole" onChange={handleChange} required>
              <option value="">Select Role</option>
              <option value="Sales Executive">Sales Executive</option>
              <option value="Research Scientist">Research Scientist</option>
              <option value="Laboratory Technician">Lab Technician</option>
              <option value="Manufacturing Director">Mfg Director</option>
              <option value="Healthcare Representative">Healthcare Rep</option>
              <option value="Manager">Manager</option>
              <option value="Sales Representative">Sales Rep</option>
              <option value="Research Director">Research Director</option>
              <option value="Human Resources">HR</option>
            </select>
          </div>

          <div className="form-group">
            <label>OverTime</label>
            <select name="OverTime" onChange={handleChange} required>
              <option value="">Select</option>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>

          <div className="form-group">
            <label>Distance From Home</label>
            <input type="number" name="DistanceFromHome" onChange={handleChange} required placeholder="Kilometers" />
          </div>

          <div className="form-group">
            <label>Total Working Years</label>
            <input type="number" name="TotalWorkingYears" onChange={handleChange} required placeholder="Years" />
          </div>

          <div className="form-group">
            <label>Years At Company</label>
            <input type="number" name="YearsAtCompany" onChange={handleChange} required placeholder="Years" />
          </div>

          <div className="form-group">
            <label>Years In Current Role</label>
            <input type="number" name="YearsInCurrentRole" onChange={handleChange} required placeholder="Years" />
          </div>

          <div className="form-group">
            <label>Years Since Promotion</label>
            <input type="number" name="YearsSinceLastPromotion" onChange={handleChange} required placeholder="Years" />
          </div>

          <button className="submit-btn" type="submit">AI Predict Attrition</button>
        </form>

        {/* Khối hiển thị kết quả siêu xịn */}
        {result && (
          <div style={{
            marginTop: '30px', padding: '20px', borderRadius: '12px',
            textAlign: 'center', fontWeight: 'bold', fontSize: '1.2rem',
            background: result.attrition === 1 ? 'rgba(239, 68, 68, 0.2)' : 'rgba(16, 185, 129, 0.2)',
            border: `1px solid ${result.attrition === 1 ? '#ef4444' : '#10b981'}`,
            color: result.attrition === 1 ? '#fca5a5' : '#6ee7b7'
          }}>
            {result.attrition === 1 
              ? `⚠️ Cảnh báo: Nhân viên có nguy cơ nghỉ việc! (${(result.probability * 100).toFixed(1)}%)`
              : `✅ An tâm: Nhân viên có xu hướng ở lại (${(result.probability * 100).toFixed(1)}%)`}
          </div>
        )}

      </div>
    </div>
  );
}

export default App;