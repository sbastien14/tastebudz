import React from 'react'
import Button from './Button'
import { Colors } from '../../data/Constants'
import TastebudzNavLogo from '../../assets/tastebudz-logo.png'

function Navbar() {
  return (
    <div style={styles.navContainer}>
      <nav style={styles.navbar}>
        <img style={styles.logo} src={TastebudzNavLogo}/>
        <div style={styles.buttonContainer}>
            <Button buttonText={'Login'} buttonSize={'fit-content'}></Button>
            <Button buttonText={'Sign Up'} buttonSize={'fit-content'}></Button>
        </div>
      </nav>
    </div>
  )
}

const styles = {
    logo: {
        height: 50,
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
        padding: 30,
        margin: '0 20px',
      },

      buttonContainer: {
        display: 'flex',
        gap: 20,
        justifyContent: 'space-between'
    },
}


export default Navbar