import React, { useState } from 'react'
import Navbar from '../components/shared/Navbar'

function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = () => {
        console.log(`Attempting to log in with Email: ${email} and Password: ${password}`);
    }

    return (
        <div style={styles.loginContainer}>
            <Navbar auth={false} />
            <div style={styles.loginContent}>
                <h2>Login to TasteBudz</h2>
                <div style={styles.inputGroup}>
                    <label>Email:</label>
                    <input 
                        type="email" 
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
                <div style={styles.inputGroup}>
                    <label>Password:</label>
                    <input 
                        type="password" 
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button onClick={handleLogin} style={styles.loginButton}>Login</button>
            </div>
        </div>
    )
}

const styles = {
    loginContainer: {
        display: 'flex',
        minHeight: '100vh',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center'
    },

    loginContent: {
        display: 'flex',
        flexDirection: 'column',
        width: '40%',
        padding: '2rem',
        boxShadow: '0px 4px 6px rgba(0,0,0,0.1)',
        borderRadius: '10px'
    },

    inputGroup: {
        display: 'flex',
        flexDirection: 'column',
        margin: '1rem 0'
    },

    loginButton: {
        marginTop: '1rem',
        padding: '0.5rem 1rem',
        backgroundColor: '#007BFF',
        color: '#FFFFFF',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        transition: 'background-color 0.3s',
        '&:hover': {
            backgroundColor: '#0056b3'
        }
    }
}

export default LoginPage
