import React from 'react';
import Navbar from '../components/shared/Navbar';
import SideMenu from '../components/home/SideMenu';
import FilterMenu from '../components/home/FilterMenu';
import FriendsList from '../components/home/FriendsList';
import SwipeView from '../components/shared/SwipeView';

function HomePage() {
    return (
        <div style={styles.homeContainer}>
            {/* Customize Navbar status */}
            <Navbar auth={true}/>
            <div style={styles.mainContent}>
                {/* SideMenu can also be made dynamic based on page context */}
                <SideMenu style={styles.sideMenu}/>
                <div style={styles.contentView}>
                    {/* SwipeView can be enhanced for better user interaction */}
                    <SwipeView/>
                    <div style={styles.infoView}>
                        {/* Ensure FilterMenu interacts with FriendsList */}
                        <FilterMenu/>
                        {/* Populate FriendsList with dynamic content */}
                        <FriendsList/>
                    </div>
                </div>
            </div>
        </div>
    );
}

// Enhance styles 
const styles = {
    homeContainer: {
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh',
        // Add more styling for overall layout aesthetics
    },
    mainContent: {
        display: 'flex',
        flex: 1,
        flexDirection: 'row',
        alignItems: 'stretch',
        width: '100%',
        '@media (max-width: 768px)': {
            flexDirection: 'column',
        },
    },
    sideMenu: {
        '@media (max-width: 768px)': {
            display: 'none',
        },
        // Add styling for side menu
    },
    contentView: {
        display: 'flex',
        flexDirection: 'column',
        flex: 1,
        padding: '20px',
        // Additional responsive styling if needed
    },
    infoView: {
        display: 'flex',
        flexDirection: 'column',
        width: '35rem',
        flex: 1,
        padding: '20px',
        gap: '20px',
        '@media (max-width: 1200px)': {
            width: 'auto',
        },
        // Style adjustments for information view
    },
};

export default HomePage;

