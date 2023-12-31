import React from 'react'
import {Colors, Dimensions} from '../data/Constants'
import Navbar from '../components/shared/Navbar'
import LandingPageImage from '../assets/landingImg.png'
import Button from '../components/shared/Button'
import {TbSwipe, TbHeartHandshake} from 'react-icons/tb'
import {MdFastfood} from 'react-icons/md'


function LandingPage() {
  return (
  <div style={styles.pageContainer}>
    <Navbar></Navbar>
    <div style={styles.heroSection}>
      <h4 style={styles.heroText}>Find Your Perfect Bite</h4>
      <Button buttonText={'Create Account'} buttonWidth={300} buttonHeight={60}></Button>
    </div>
    <div style={styles.featuresSection}>
        <div style={styles.featureCard}>
          <TbSwipe size={190}/>
          <h3 style={styles.featuresHeader}>Swiping</h3>
          <p style={styles.featuresText}> Quibusdam, corporis tempore temporibus ad in numquam assumenda ratione, fuga non libero nihil asperiores vel. Hic maxime dignissimos cumque a culpa.</p>
        </div>
        <div style={styles.featureCard}>
          <MdFastfood size={190}/>
          <h3 style={styles.featuresHeader}>Suggestions</h3>
          <p style={styles.featuresText}> Molestias, quia! Tempora quis sint porro assumenda temporibus laudantium molestiae, soluta quaerat eveniet fugit delectus, minus qui aliquam minima.</p>
        </div>
        <div style={styles.featureCard}>
          <TbHeartHandshake size={190}/>
          <h3 style={styles.featuresHeader}>Merging</h3>
          <p style={styles.featuresText}> voluptatem qui quasi accusamus voluptas praesentium exercitationem, nostrum sunt est, doloremque architecto consectetur non! Neque ea numquam accusamus dolorem dolores libero reiciendis.</p>
        </div>
    </div>
    <div style={styles.authForm}>

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
  },

  featuresSection: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    height: '90vh',
    backgroundColor: Colors.ACCENT,
    padding: 50
  },

  featureCard: {
    height: 600,
    width: 500,
    fontSize: Dimensions.SMALL * 1.2,
    backgroundColor: 'whitesmoke',
    color: Colors.PRIMARY,
    textAlign: 'center',
    padding: 20,
    borderRadius: 10
  },

  featuresText: {
    fontWeight: 'semibold',
    textTransform: 'uppercase',
    textAlign: 'center',
    padding: 20
  },

  featuresHeader: {
    letterSpacing: 5,
    fontWeight: 'bold',
    fontSize: Dimensions.LARGE * 1.5,
    textTransform: 'uppercase'
  }

}

export default LandingPage