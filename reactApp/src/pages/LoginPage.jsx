import React, { useState } from 'react';
import axios from 'axios';
import LandingPageImage from '../assets/landingImg.png'; 

function LoginPage() {
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');

  const [registerEmail, setRegisterEmail] = useState('');
  const [registerPassword, setRegisterPassword] = useState('');
  const [registerError, setRegisterError] = useState('');

  const [showRegisterForm, setShowRegisterForm] = useState(false);

  const handleLogin = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/auth/user/login', {
        headers: {
          "Access-Control-Allow-Origin": "*",
          'Content-Type': 'application/json'
        },
        auth: {
          username: email,
          password: password
        }
      });

      if (response.status === 200 && response.data.id) {
        // Redirect to home page (swipe view)
      } else {
        // Show error message
        setLoginError(response.data.message || 'Unknown error occurred');
      }
    } catch (error) {
      const errorMessage = error.response ? error.response.data.message : 'Login failed';
      setLoginError(errorMessage);
    }
  }

  const handleRegister = async (email, password, username, role) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/auth/login/user', {
        username: username,
        role: role
      },
      {
        headers: {
          'Content-Type': 'application/json'
        },
        auth: {
          username: email,
          password: password
        }
      });

      if (response.status === 200) {
        // Redirect to login page or show success message
        setShowRegisterForm(false);
        setLoginError('Account created successfully. Please log in.');
      } else {
        // Show error message
        setRegisterError(response.data.message || 'Unknown error occurred');
      }
    } catch (error) {
      const errorMessage = error.response ? error.response.data.message : 'Error registering account';
      setRegisterError(errorMessage);
      console.error('Registration error:', errorMessage);
    }
  };
 
  return (
    <div style={styles.loginContainer}>
      <div style={styles.loginContent}>
        {showRegisterForm ? (
          <>
            <h2 style={styles.heading}>Create an Account</h2>
            <div style={styles.inputGroup}>
              <label style={styles.label}>Email:</label>
              <input 
                type="email"
                value={registerEmail}
                onChange={(e) => setRegisterEmail(e.target.value)}
                style={styles.input}
              />
            </div>
            <div style={styles.inputGroup}>
              <label style={styles.label}>Password:</label>
              <input 
                type="password"
                value={registerPassword}
                onChange={(e) => setRegisterPassword(e.target.value)}
                style={styles.input}
              />
            </div>
            {registerError && <p style={styles.errorText}>{registerError}</p>}
            <button onClick={handleRegister} style={styles.loginButton}>Register</button>
            <button onClick={() => setShowRegisterForm(false)} style={styles.toggleButton}>Already have an account? Login</button>
          </>
        ) : (
          <>
            <h2 style={styles.heading}>Login to Your Account</h2>
            <div style={styles.inputGroup}>
              <label style={styles.label}>Email:</label>
              <input 
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={styles.input}
              />
            </div>
            <div style={styles.inputGroup}>
              <label style={styles.label}>Password:</label>
              <input 
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={styles.input}
              />
            </div>
            {loginError && <p style={styles.errorText}>{loginError}</p>}
            <button onClick={() => handleLogin(email, password)} style={styles.loginButton}>Login</button>
            <button onClick={() => setShowRegisterForm(true)} style={styles.toggleButton}>Create an Account</button>
          </>
        )}
      </div>
    </div>
  );
}

const styles = {
  toggleButton: {
    marginTop: '10px',
    padding: '10px 20px',
    fontSize: '16px',
    backgroundColor: 'lightgrey',
    color: 'black',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
  },
  loginContainer: {
    display: 'flex',
    minHeight: '100vh',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    background: `linear-gradient(0deg, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url(${LandingPageImage})`,
    backgroundSize: 'cover',
  },
  loginContent: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '20px',
    width: '100%',
    maxWidth: '500px',
  },
  inputGroup: {
    marginBottom: '15px',
    width: '100%',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  input: {
    marginBottom: '10px',
    height: '35px',
    padding: '5px',
    fontSize: '16px',
    borderWidth: '1px',
    borderColor: '#ddd',
    borderRadius: '4px',
    width: '300px',
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    color: 'white',
    border: '1px solid rgba(255, 255, 255, 0.4)',
  },
  loginButton: {
    marginTop: '10px',
    padding: '10px 20px',
    fontSize: '18px',
    backgroundColor: '#007BFF',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
  },
  heading: {
    color: 'white',
    fontSize: '2rem',
    textShadow: '2px 2px 4px rgba(0, 0, 0, 0.5)',
  },
  label: {
    color: 'white',
    marginBottom: '5px',
    fontSize: '1.2rem',
  },
  errorText: {
    color: 'red',
    backgroundColor: 'rgba(255, 0, 0, 0.2)',
    padding: '10px',
    borderRadius: '5px',
  }
};

export default LoginPage;
