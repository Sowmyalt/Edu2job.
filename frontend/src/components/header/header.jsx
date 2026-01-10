import { Link, useLocation } from 'react-router-dom';
import { useContext } from 'react';
import AuthContext from '../../context/AuthContext';
import './header.css'

const ComponentName = () => {
  const { user, logoutUser } = useContext(AuthContext);
  const location = useLocation();
  const isHome = location.pathname === '/';

  // Class for non-home pages
  const wrapperClass = isHome ? "h-wrapper" : "h-wrapper dark-header";

  return (
    <section className={wrapperClass}>
      {!isHome && (
        <>
          {/* Explicit Black Background Layer */}
          <div style={{ position: 'absolute', inset: 0, background: 'var(--black)', zIndex: 0 }} />
          {/* Explicit Gradient Layer */}
          <div className="white-gradient" style={{
            position: 'absolute',
            width: '20rem',
            height: '20rem',
            background: 'rgba(255, 255, 255, 0.6)',
            filter: 'blur(100px)',
            borderRadius: '100px',
            top: '-10rem',
            left: '-5rem',
            zIndex: 1
          }} />
        </>
      )}
      <div className="flexCenter paddings innerWidth h-container" style={{ position: 'relative', zIndex: 5 }}>
        <Link to="/">
          <img src='./logo.png' width={100} />
        </Link>
        <div className="flexCenter h-menu">
          <a href="/#community"><h3>Community</h3></a>

          {user ? (
            <>
              <Link to="/dashboard"><h3>Dashboard</h3></Link>
              <Link to="/profile"><h3>Profile</h3></Link>
              {user.is_staff && <Link to="/admin"><h3>Admin</h3></Link>}
              <button className='button' onClick={logoutUser}>Logout</button>
            </>
          ) : (
            <Link to="/register"><button className='button'>Getting Started</button></Link>
          )}



        </div>
      </div>
    </section>
  )
}

export default ComponentName
