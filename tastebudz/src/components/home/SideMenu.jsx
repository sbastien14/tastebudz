
import React from 'react'
import { Dimensions, Colors } from '../../data/Constants'
import {FiSettings, FiHeart} from 'react-icons/fi'
import {CgProfile} from 'react-icons/cg'
import {TbLogout2} from 'react-icons/tb'

const SideMenu = () => {
  return (
    <div style={styles.menu}>
        <div style={styles.menuOptionsContainer}>
            <div style={styles.menuOption}>
                <CgProfile style={styles.menuIcon} size={Dimensions.LARGE * 1.2} color='white'/>
                <p style={styles.menuOptionText}>Profile</p>
            </div>
            <div style={styles.menuOption}>
                <FiHeart style={styles.menuIcon} size={Dimensions.LARGE * 1.2} color='white'/>
                <p style={styles.menuOptionText}>Likes</p>
            </div>
            <div style={styles.menuOption}>
                <FiSettings style={styles.menuIcon} size={Dimensions.LARGE * 1.2} color='white'/>
                <p style={styles.menuOptionText}>Settings</p>
            </div>
            <div style={styles.menuOption}>
                <TbLogout2 style={styles.menuIcon} size={Dimensions.LARGE * 1.2} color='white'/>
                <p style={styles.menuOptionText}>Sign Out</p>
            </div>
        </div>
    </div>
  )
}

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
        alignItems: 'center'
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

export default SideMenu