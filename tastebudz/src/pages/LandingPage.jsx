import React from 'react'
import {Colors, Dimensions} from '../data/Constants'
import Navbar from '../components/shared/Navbar'
import LandingPageImage from '../assets/landingImg.png'
import Button from '../components/shared/Button'

function LandingPage() {
  return (
  <div style={styles.pageContainer}>
    <Navbar></Navbar>
    <div style={styles.heroSection}>
      <h4 style={styles.heroText}>Find Your Perfect Bite</h4>
      <Button buttonText={'Create Account'} buttonWidth={300} buttonHeight={60}></Button>
    </div>
  </div>
  )
}

const styles = {
  pageContainer : {
    position: 'relative',
  },

  heroSection: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    // fontSize: Dimensions.LARGE,
    width: '100%',
    height: '100vh',
    flexDirection: 'column',
    background: `linear-gradient(0deg, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url(${LandingPageImage})`,
    backgroundSize: 'cover',
  },

  heroText: {
    textTransform: 'uppercase',
    letterSpacing: 10,
    fontSize: '7rem',
    color: 'white',
  }

}

export default LandingPage