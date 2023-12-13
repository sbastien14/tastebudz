import React from 'react'
import Button from './Button'
import { Colors } from '../../data/Constants'
import TastebudzNavLogo from '../../assets/tastebudz-logo.png'

function Navbar({auth}) {
  return (
    <div>
    {
      auth ? 
        <div style={styles.navContainer}>
          <nav style={styles.navbar}>
            <img style={styles.logo} src={TastebudzNavLogo} alt='Navbar Logo'/>
            <div style={styles.buttonContainer}>
                <Button buttonText={'Merge'} buttonSize={'fit-content'}></Button>
                <Button buttonText={'Solo Suggestion'} buttonSize={'fit-content'}></Button>
            </div>
          </nav>
        </div>
      :
      <div style={styles.navContainer}>
        <nav style={styles.navbar}>
          <img style={styles.logo} src={TastebudzNavLogo} alt='Navbar Logo'/>
          <div style={styles.buttonContainer}>
              <Button buttonText={'Features'} buttonSize={'fit-content'}></Button>
              <Button buttonText={'Login'} buttonSize={'fit-content'}></Button>
          </div>
        </nav>
      </div>
      }
      </div>
   
  )
}

const styles = {
    logo: {
        height: 50,
      },
    
    navContainer: {
      top: 0,
      width: '100%',
      textAlign: 'center',
      backgroundColor: 'whitesmoke',
      boxShadow: '0 2px 3px lightgray',
      filter: `drop-shadow(-5px 0px ${Colors.SHADOW_GRAY})`,
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