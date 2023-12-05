import React from 'react';
import { Dimensions, Colors } from '../../data/Constants';
import { CgProfile } from 'react-icons/cg';
import { AiOutlineHome } from 'react-icons/ai'; // Icon for home/landing page
import { useNavigate } from 'react-router-dom';

const SideMenu = () => {
  const navigate = useNavigate();

  const navigateToLanding = () => {
    navigate('/'); // Update this to your landing page route
  };

  return (
    <div style={styles.menu}>
        <div style={styles.menuOptionsContainer}>
            <div style={styles.menuOption} onClick={() => navigateToLanding()}>
                <AiOutlineHome style={styles.menuIcon} size={Dimensions.LARGE * 1.2} color='white'/>
                <p style={styles.menuOptionText}>Return</p>
            </div>
            <div style={styles.menuOption}>
                <CgProfile style={styles.menuIcon} size={Dimensions.LARGE * 1.2} color='white'/>
                <p style={styles.menuOptionText}>Profile</p>
            </div>
        </div>
    </div>
  );
};

const styles = {
    menu: {
        backgroundColor: Colors.ACCENT,
        flex: '0.5rem',
    },

    menuOptionsContainer: {
        padding: 60
    },

    menuOption: {
        display: 'flex',
        alignItems: 'center',
        cursor: 'pointer', // Added for better UX
    },

    menuIcon: {
        marginRight: 30
    },

    menuOptionText: {
        color: 'white',
        fontSize: Dimensions.MEDIUM,
        textTransform: 'uppercase',
        letterSpacing: 5,
        fontWeight: 'bold'
    },
}

export default SideMenu;
