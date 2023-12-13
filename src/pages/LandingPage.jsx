import React from 'react';
import { Colors, Dimensions } from '../data/Constants';
import Navbar from '../components/shared/Navbar';
import LandingPageImage from '../assets/landingImg.png';
import Button from '../components/shared/Button';
import { TbSwipe, TbHeartHandshake } from 'react-icons/tb';
import { useNavigate } from 'react-router-dom';
import { MdFastfood } from 'react-icons/md';

function LandingPage() {
  const navigate = useNavigate();

  const navigateToLogin = () => {
    navigate('login');
  };

  // New function to navigate to the home page
  const navigateToHome = () => {
    navigate('/home'); 
  };

  return (
    <div style={styles.pageContainer}>
      <Navbar />
      <div style={styles.heroSection}>
        <h4 style={styles.heroText}>Find Your Perfect Bite</h4>
        <Button buttonText={'Create Account'} buttonWidth={300} buttonHeight={60} onClick={navigateToLogin} />
      </div>
      <div style={styles.featuresSection}>
        <div style={styles.featureCard}>
          <TbSwipe size={190} />
          <h3 style={styles.featuresHeader}>Swiping</h3>
          <p style={styles.featuresText}>Explore a variety of food spots by swiping through our curated selection. Your preferences refine our recommendations, ensuring each swipe brings you closer to your ideal dining experience.</p>
          <Button buttonText={'Go to Home'} onClick={navigateToHome} />
        </div>
        <div style={styles.featureCard}>
          <MdFastfood size={190} />
          <h3 style={styles.featuresHeader}>Suggestions</h3>
          <p style={styles.featuresText}>Get personalized suggestions tailored to your tastes and location. Whether you're planning a special date or a casual outing with friends, we help you discover the perfect spot.</p>
          <Button buttonText={'Go to Home'} onClick={navigateToHome} />
        </div>
        <div style={styles.featureCard}>
          <TbHeartHandshake size={190} />
          <h3 style={styles.featuresHeader}>Merging</h3>
          <p style={styles.featuresText}>Connect with friends on Tastebudz to merge your favorite foods and find places that everyone will love. It's the ideal way to plan group outings without the hassle.</p>
          <Button buttonText={'Go to Home'} onClick={navigateToHome} />
        </div>
      </div>
      <div style={styles.authForm}>
        {/* Authentication form can be added here */}
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

export default LandingPage;
