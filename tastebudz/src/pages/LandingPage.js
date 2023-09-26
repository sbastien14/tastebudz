import React from 'react'
import {Colors, Dimensions} from '../data/Constants'
import Navbar from '../components/Navbar'

function LandingPage() {
  return (
  <div style={styles.pageContainer}>
    <Navbar></Navbar>
    <div style={styles.heroSection}>
      <h4 style={styles.heroText}>Test text</h4>
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
    fontSize: Dimensions.LARGE,
    width: '100%',
    height: '100vh',
    flexDirection: 'row',
    backgroundColor: Colors.ACCENT
  },

  heroText: {
    textTransform: 'uppercase',
    color: 'white'
  }

}

export default LandingPage