import React from 'react'
import { Colors, Dimensions } from '../../data/Constants'
import ProfilePicture from '../../assets/testProfilePicture.jpeg'

function FriendsList() {
    const testFriendsList = [1, 2, 3, 4,5,6]

    return (
        <div style={styles.friendsListContainer}>
            <h3 style={styles.friendHeader}>Friends</h3>
            {
                testFriendsList.map((friend) => (
                    <div style={styles.userID}>
                        <img style={styles.userImg} src={ProfilePicture} alt=''/>
                        <div style={styles.userTag}>
                            <h3>John Doe</h3>
                            <p>@DoeboyJohn</p>
                        </div>
                    </div>
                ))
            }
        </div>
    )
}

const styles = {
    friendsListContainer: {
        display: 'flex',
        flexDirection: 'column',
        flex: 0.7,
        // height: 800,
        width: '38rem',
        borderRadius: 5,
        backgroundColor: Colors.GRAY,
        filter: `drop-shadow(-5px 5px ${Colors.SHADOW_GRAY})`,
    },

    friendHeader: {
        fontSize: Dimensions.MEDIUM * 1.2,
        textTransform: 'uppercase',
        letterSpacing: 2,
        textAlign: 'left',
        padding: '10px 2rem'
    },

    userImg: {
        marginRight: 20,
        width: 65,
        height: 65, 
        borderRadius: '100%', 
        objectFit: 'cover'
    },

    userID: {
        display: 'flex',
        alignItems: 'center',
        textTransform: 'uppercase',
        letterSpacing: 2,
        lineHeight: 0.5,
        padding: '1rem 2rem',
        // color: Colors.PRIMARY,
        borderTop: `2px solid ${Colors.SHADOW_GRAY}`,
    }
}

export default FriendsList