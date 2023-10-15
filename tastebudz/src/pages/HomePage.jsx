import React from 'react'
import Navbar from '../components/shared/Navbar'
import { Colors, Dimensions } from '../data/Constants'
import SideMenu from '../components/home/SideMenu'
import FilterMenu from '../components/home/FilterMenu'
import {BsArrowLeft, BsArrowRight} from 'react-icons/bs'
import ReviewCard from '../components/shared/ReviewCard'


function HomePage() {
    let testMap = [1,2,3]

    return (
    <div style={styles.homeContainer}>
        <div style={styles.homeContent}>
            <Navbar/>
            <div style={styles.homeView}>
                <SideMenu/>
                <div style={styles.swipeView}>
                    <button style={styles.swipeAction}><BsArrowLeft color='white'/></button>
                    <div style={styles.swipeContainer}>
                        <div style={styles.restaurantCard}>

                        </div>
                        <div style={styles.restaurantReviews}>
                            {
                                testMap.map((review) => (
                                    <ReviewCard/>
                                ))
                                    
                                
                            }
                        </div>
                        
                        
                    </div>
                    <button style={styles.swipeAction}><BsArrowRight color='white'/></button>
                </div>
                <div style={styles.infoView}>
                    <div style={styles.friendsList}>

                    </div>
                    <FilterMenu/>
                </div>
            </div>
        </div>
        
    </div>
  )
}

const styles = {
    homeContainer: {
        display: 'flex',
        minHeight: '100vh',
        flexDirection: 'column'
    },

    homeContent: {
        display: 'flex',
        minHeight: '100vh',
        flexDirection: 'column'
    },

    homeView: {
        display: 'flex',
        flex: 1
        
    },

    swipeView: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        backgroundColor: 'white',
        padding: 50,
        flex: 3,
    },

    restaurantReviews: {
        display: 'flex'
    },

    infoView: {
        display: 'flex',
        
        width: '35rem',
        flex: 1,
        padding: 50,
        justifyContent: 'center',
        
    },

    swipeAction: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: 150,
        width: 150,
        fontSize: 50,
        borderRadius: 180,
        border: 'none',
        filter: `drop-shadow(-5px 5px ${Colors.SHADOW_GRAY})`,
        // backgroundColor: '#F3F5F7',
        backgroundColor: Colors.SECONDARY,
        cursor: 'pointer'
    }

    
   



}

export default HomePage