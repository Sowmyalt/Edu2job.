import React from "react";
import './joblogos.css'

const MyComponent = () => {
  return (
    <div className="c-wrapper">
      <div className="paddings innerWidth flexCenter c-container">
        <img src="doctor.png" alt="Doctor" />
        <img src="teacher.png" alt="Teacher" />
        <img src="lawyer.png" alt="Lawyer" />
        <img src="engineer.png" alt="Engineer" />
      </div>
    </div>
  );
};

export default MyComponent;
