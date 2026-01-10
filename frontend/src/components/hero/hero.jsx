import React from 'react'
import "./hero.css"
import CountUp from 'react-countup'

const ComponentName = () => {
  return (
    <section className="hero-wrapper">
      <div className="paddings innerWidth flexCenter hero-container">

        {/* LEFT SECTION */}
        <div className="flexColStart hero-left">

          <div className="hero-title">
            <div className="orange-circle" />
            <h1>
              Predicting Job Roles<br />
              from Education. 
            </h1>
          </div>

          <div className="flexColStart hero-des">
            <h3><span className='secondaryText'>Bridge the gap between learning and earning.</span></h3>
            <h3><span className='secondaryText'>Get accurate job-role predictions tailored to your educational journey.</span></h3>
          </div>

          {/* STATS */}
          <div className="flexCenter stats">
            <div className="flexColCenter stat">
              <b><span>
                <CountUp start={85} end={99} duration={3} />%+
              </span></b>
              <span className='secondaryText'>Accuracy</span>
            </div>
             <div className="flexColCenter stat">
              <b><span>
                <CountUp start={100} end={150} duration={3} />+
              </span></b>
            
              <span className='secondaryText'>Career Paths</span>
            </div>
            <div className="flexColCenter stat">
              <b><span>
                <CountUp start={55} end={70} duration={3} />%+
              </span></b>
              
              <span className='secondaryText'>Faster Decision Making</span>
            </div>
          </div>

        </div>

        {/* RIGHT SECTION */}
        <div className="flexCenter hero-right">
          <div className="image-container">
            <img src="/hero-image.jpg" alt="Hero" />
          </div>
        </div>

      </div>
    </section>
  )
}

export default ComponentName
