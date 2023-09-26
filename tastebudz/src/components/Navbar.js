import React from 'react'
import Button from './Button'
import { Colors } from '../data/Constants'

function Navbar() {
  return (
    <div style={styles.navContainer}>
      <nav style={styles.navbar}>
        <h1 style={styles.logo}>Tastebudz</h1>
        <div style={styles.buttonContainer}>
            <Button buttonText={'Login'}></Button>
            <Button buttonText={'Sign Up'}></Button>
        </div>
      </nav>
    </div>
  )
}

const styles = {
    logo: {
        textTransform: 'uppercase',
        letterSpacing: 5,
        color: Colors.ACCENT
      },
    
      navContainer: {
        position: 'absolute',
        top: 0,
        width: '100%',
        textAlign: 'center',
        backgroundColor: 'whitesmoke',
        boxShadow: '0 2px 3px lightgray',
      },
    
      navbar: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: 20,
        margin: '0 20px',
      },

      buttonContainer: {
        display: 'flex',
        gap: 20,
        justifyContent: 'space-between'
    },
}


export default Navbar