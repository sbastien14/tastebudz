import React from 'react'
import {Colors} from '../data/Constants'

function ErrorPage() {
  return (
    <div style={styles.pageContainer}>
        <h1 style={styles.mainText}>404</h1>
        <p style={styles.supplementText}>Page Not Found</p>
    </div>
  )
}

const styles = {
    pageContainer: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        backgroundColor: Colors.ACCENT,
        color: 'white',
        textAlign: 'center',
        height: '100vh',
    },

    mainText: {
        fontSize: 250,
        letterSpacing: 50,
    },

    supplementText: {
        textTransform: 'uppercase',
        fontSize: 31,
        fontWeight: 'bold',
        letterSpacing: 25
    }
}

export default ErrorPage