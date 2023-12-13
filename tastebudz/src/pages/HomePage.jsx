import React from 'react'
import Navbar from '../components/shared/Navbar'
import SideMenu from '../components/home/SideMenu'
import FilterMenu from '../components/home/FilterMenu'
import FriendsList from '../components/home/FriendsList'
import SwipeView from '../components/shared/SwipeView'

function HomePage() {
    

    return (
    <div style={styles.homeContainer}>
        <div style={styles.homeContent}>
            <Navbar auth={true}/>
            <div style={styles.homeView}>
                <SideMenu/>
                <SwipeView/>
                <div style={styles.infoView}>
                    <FilterMenu/>
                    <FriendsList/>
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

    infoView: {
        display: 'flex',
        flexDirection: 'column',
        width: '35rem',
        flex: 1,
        padding: 50,
        gap: 100
        
    },

    

}

export default HomePage