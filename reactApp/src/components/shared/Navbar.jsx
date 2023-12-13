import React from 'react';
import { Colors } from '../../data/Constants';
import TastebudzNavLogo from '../../assets/tastebudz-logo.png';
import { useNavigate } from 'react-router-dom';
import Button from './Button'; 

function Navbar({auth}) {
  const navigate = useNavigate();

  function handleLoginClick() {
    navigate('/login');
  }

  function handleHomeClick() {
    navigate('/home');
  }

  return (
    <div>
      {auth ? (
        <div style={styles.navContainer}>
          <nav style={styles.navbar}>
            <img style={styles.logo} src={TastebudzNavLogo} alt='Navbar Logo'/>
            <div style={styles.swipeTextContainer}>
                <p style={styles.swipeText}>Swipe through restaurants to find your perfect bite!</p>
            </div>
          </nav>
        </div>
      ) : (
        <div style={styles.navContainer}>
          <nav style={styles.navbar}>
            <img style={styles.logo} src={TastebudzNavLogo} alt='Navbar Logo'/>
            <div style={styles.buttonContainer}>
                <Button 
                    buttonText={'Home'}
                    buttonSize={'fit-content'} 
                    onClick={handleHomeClick}
                ></Button>
                <Button 
                    buttonText={'Login'} 
                    buttonSize={'fit-content'} 
                    onClick={handleLoginClick}
                ></Button>
            </div>
          </nav>
        </div>
      )}
    </div>
  );
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